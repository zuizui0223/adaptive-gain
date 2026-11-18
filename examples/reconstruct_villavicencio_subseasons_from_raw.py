"""Reconstruct Villavicencio 18-subseason interaction networks from raw dates.

Dryad documents three subseasons for each study year:
- early: before November 1;
- mid: November 1 through November 30;
- late: after November 30.

The declared study-year field is authoritative, so January 2007 observations
belonging to study year 2006 are assigned to 2006_late.

Only the frozen 45 x 135 trait-available code subset is exported. Positive
visit rows lacking a date are never silently assigned to a subseason.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path


YEARS = tuple(range(2006, 2012))
SUBSEASONS = ("early", "mid", "late")


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _number(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _integer(value):
    value = _number(value)
    return None if value is None else int(value)


def _codes(path: Path, field: str):
    out = {
        str(row[field]).strip()
        for row in _read(path)
        if str(row.get(field, "")).strip()
    }
    if not out:
        raise ValueError(f"{path}: no codes in {field}")
    return out


def _parse_date(value):
    text = "" if value is None else str(value).strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def _subseason(study_year: int, observed_date: date) -> str:
    early_end = date(study_year, 11, 1)
    mid_end = date(study_year, 11, 30)
    if observed_date < early_end:
        return "early"
    if observed_date <= mid_end:
        return "mid"
    return "late"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("visits", type=Path)
    parser.add_argument("plant_names", type=Path)
    parser.add_argument("pollinator_names", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    plants = _codes(args.plant_names, "plant_code")
    pollinators = _codes(args.pollinator_names, "pol_code")

    weights = defaultdict(float)
    full_annual_links = defaultdict(set)
    dated_annual_links = defaultdict(set)
    undated_rows = []
    dated_positive_rows = 0
    dated_positive_visits = 0.0

    for row in _read(args.visits):
        study_year = _integer(row.get("year"))
        plant = str(row.get("codigo.p", "")).strip()
        pollinator = str(row.get("codigo.i", "")).strip()
        visit_count = _number(row.get("no.fl.visit"))
        observed_date = _parse_date(row.get("date"))

        if (
            study_year not in YEARS
            or plant not in plants
            or pollinator not in pollinators
            or visit_count is None
            or visit_count <= 0
        ):
            continue

        dyad = (plant, pollinator)
        full_annual_links[study_year].add(dyad)

        if observed_date is None:
            undated_rows.append(
                {
                    "year": study_year,
                    "plant": plant,
                    "pollinator": pollinator,
                    "visits": visit_count,
                }
            )
            continue

        subseason = _subseason(study_year, observed_date)
        period = f"{study_year}_{subseason}"
        weights[(period, plant, pollinator)] += visit_count
        dated_annual_links[study_year].add(dyad)
        dated_positive_rows += 1
        dated_positive_visits += visit_count

    args.output_dir.mkdir(parents=True, exist_ok=True)

    interactions_path = args.output_dir / "raw_subseason_interactions_long.csv"
    with interactions_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["period", "plant", "pollinator", "weight"],
        )
        writer.writeheader()
        for (period, plant, pollinator), weight in sorted(weights.items()):
            writer.writerow(
                {
                    "period": period,
                    "plant": plant,
                    "pollinator": pollinator,
                    "weight": weight,
                }
            )

    period_map_path = args.output_dir / "raw_subseason_period_map.csv"
    with period_map_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["period", "year", "subseason", "verified", "basis"],
        )
        writer.writeheader()
        for year in YEARS:
            for subseason in SUBSEASONS:
                writer.writerow(
                    {
                        "period": f"{year}_{subseason}",
                        "year": year,
                        "subseason": subseason,
                        "verified": "true",
                        "basis": "externally_documented_Dryad_methods_boundary",
                    }
                )

    period_counts = {}
    for year in YEARS:
        for subseason in SUBSEASONS:
            period = f"{year}_{subseason}"
            period_rows = [
                (plant, pollinator, weight)
                for (p, plant, pollinator), weight in weights.items()
                if p == period
            ]
            period_counts[period] = {
                "link_count": len(period_rows),
                "visit_count": sum(weight for _, _, weight in period_rows),
            }

    undated_by_year = defaultdict(lambda: {"rows": 0, "visits": 0.0})
    for row in undated_rows:
        bucket = undated_by_year[str(row["year"])]
        bucket["rows"] += 1
        bucket["visits"] += row["visits"]

    annual_completeness = {}
    for year in YEARS:
        missing = full_annual_links[year] - dated_annual_links[year]
        annual_completeness[str(year)] = {
            "full_positive_link_count": len(full_annual_links[year]),
            "dated_reconstructable_link_count": len(dated_annual_links[year]),
            "links_only_in_undated_rows": len(missing),
            "complete_link_support": len(missing) == 0,
        }

    summary = {
        "schema": "adaptive-gain-villavicencio-raw-subseason-reconstruction-v1",
        "date": "2026-09-29",
        "period_count": 18,
        "trait_subset": {
            "plant_count": len(plants),
            "pollinator_count": len(pollinators),
        },
        "boundary_rule": {
            "early": "before November 1",
            "mid": "November 1 through November 30 inclusive",
            "late": "after November 30",
            "study_year_authoritative": True,
        },
        "dated_positive_rows": dated_positive_rows,
        "dated_positive_visits": dated_positive_visits,
        "undated_positive_rows": len(undated_rows),
        "undated_positive_visits": sum(row["visits"] for row in undated_rows),
        "undated_by_year": dict(undated_by_year),
        "periods": period_counts,
        "annual_completeness": annual_completeness,
        "all_periods_nonempty": all(
            item["link_count"] > 0 for item in period_counts.values()
        ),
        "published_rdata_bytes_used": False,
        "decision_equivalence_inferred": False,
    }
    (args.output_dir / "raw_subseason_reconstruction_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
