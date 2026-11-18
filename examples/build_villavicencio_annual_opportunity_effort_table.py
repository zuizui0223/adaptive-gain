"""Join raw focal-plant 5-min census counts to the repaired annual opportunity table."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _number(value):
    text = "" if value is None else str(value).strip()
    if not text or text.lower() in {"na", "nan", "none"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _integer(value):
    value = _number(value)
    return None if value is None else int(value)


def _valid_date(value):
    text = "" if value is None else str(value).strip()
    if not text:
        return False
    try:
        date.fromisoformat(text)
    except ValueError:
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("visits", type=Path)
    parser.add_argument("opportunity_table", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    censuses = set()
    for row in _read(args.visits):
        site = str(row.get("site", "")).strip()
        year = _integer(row.get("year"))
        date_text = str(row.get("date", "")).strip()
        plant = str(row.get("codigo.p", "")).strip()
        obs_time = str(row.get("obs.time", "")).strip()
        if (
            not site
            or year is None
            or not _valid_date(date_text)
            or not plant
            or not obs_time
            or obs_time.lower() in {"na", "nan", "none"}
        ):
            continue
        censuses.add((site, year, date_text, plant, obs_time))

    annual_plant_counts = Counter(
        (year, plant)
        for _, year, _, plant, _ in censuses
    )

    rows = []
    missing = 0
    for row in _read(args.opportunity_table):
        previous_year = int(row["previous_period"])
        current_year = int(row["current_period"])
        plant = str(row["plant"]).strip()
        previous = annual_plant_counts[(previous_year, plant)]
        current = annual_plant_counts[(current_year, plant)]
        if previous <= 0 or current <= 0:
            missing += 1
        rows.append(
            {
                **row,
                "previous_plant_censuses": previous,
                "current_plant_censuses": current,
            }
        )

    if missing:
        raise SystemExit(
            f"{missing} repaired annual dyad rows lack positive focal-plant effort"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    annual = Counter(year for _, year, _, _, _ in censuses)
    summary = {
        "schema": "adaptive-gain-villavicencio-annual-opportunity-effort-table-v1",
        "date": "2026-09-29",
        "row_count": len(rows),
        "missing_effort_rows": missing,
        "annual_raw_census_counts": {
            str(year): annual[year]
            for year in sorted(annual)
        },
        "raw_census_identity": [
            "site",
            "year",
            "date",
            "codigo.p",
            "obs.time",
        ],
    }
    args.summary.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
