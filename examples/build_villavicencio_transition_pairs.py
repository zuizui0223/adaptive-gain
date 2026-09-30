"""Build the frozen Villavicencio transition list from a verified period map."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

SUBSEASONS = ("early", "mid", "late")


def read_period_map(path: Path):
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"period", "year", "subseason", "verified"}
        if not required <= set(reader.fieldnames or ()):
            raise ValueError(f"period map must contain {sorted(required)}")
        for row in reader:
            verified = row["verified"].strip().lower()
            if verified not in {"1", "true", "yes", "y"}:
                raise ValueError(
                    f"period {row['period']!r} is not explicitly verified"
                )
            year = int(row["year"])
            subseason = row["subseason"].strip().lower()
            if subseason not in SUBSEASONS:
                raise ValueError(
                    f"subseason must be one of {SUBSEASONS}, got {subseason!r}"
                )
            rows.append((row["period"], year, subseason))
    return rows


def build_transition_rows(period_rows):
    if len(period_rows) != 18:
        raise ValueError("expected exactly 18 verified period rows")

    lookup = {}
    for period, year, subseason in period_rows:
        key = (year, subseason)
        if key in lookup:
            raise ValueError(f"duplicate year/subseason mapping: {key!r}")
        lookup[key] = period

    years = sorted({year for _, year, _ in period_rows})
    if len(years) != 6:
        raise ValueError("expected exactly six years")
    if years != list(range(years[0], years[0] + 6)):
        raise ValueError("years must form one consecutive six-year sequence")

    expected = {(year, subseason) for year in years for subseason in SUBSEASONS}
    if set(lookup) != expected:
        missing = sorted(expected - set(lookup))
        extra = sorted(set(lookup) - expected)
        raise ValueError(f"incomplete 3x6 period map; missing={missing!r}, extra={extra!r}")

    transitions = []
    for year in years:
        transitions.append(
            (lookup[(year, "early")], lookup[(year, "mid")], "primary")
        )
        transitions.append(
            (lookup[(year, "mid")], lookup[(year, "late")], "primary")
        )

    for previous_year, current_year in zip(years, years[1:]):
        transitions.append(
            (
                lookup[(previous_year, "late")],
                lookup[(current_year, "early")],
                "sensitivity",
            )
        )

    return transitions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("period_map", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    transitions = build_transition_rows(read_period_map(args.period_map))
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["previous_period", "current_period", "role"])
        writer.writerows(transitions)


if __name__ == "__main__":
    main()
