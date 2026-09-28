"""Build a same-site same-week focal-response-excluded opportunity surface.

This is a stricter robustness surface than the week-only repaired baseline.
A plant-pollinator dyad receives spatiotemporal opportunity only when the focal
plant is flowering and the focal pollinator is observed on another plant in
the same site and ISO week. The focal dyad's own visit never contributes to
pollinator activity.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path


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


def _bool(value):
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"unrecognized boolean value: {value!r}")


def _week(value):
    text = "" if value is None else str(value).strip()
    if not text:
        return None
    try:
        return int(date.fromisoformat(text).isocalendar().week)
    except ValueError:
        return None


def _codes(path: Path, field: str):
    return {
        str(row[field]).strip()
        for row in _read(path)
        if str(row.get(field, "")).strip()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("visits", type=Path)
    parser.add_argument("plant_names", type=Path)
    parser.add_argument("pollinator_names", type=Path)
    parser.add_argument("stage1_dyads", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    plant_codes = _codes(args.plant_names, "plant_code")
    pollinator_codes = _codes(args.pollinator_names, "pol_code")

    plant_cells = defaultdict(set)
    pollinator_cell_plants = defaultdict(set)
    positive_links = defaultdict(set)

    for row in _read(args.visits):
        year = _integer(row.get("year"))
        site = str(row.get("site", "")).strip()
        plant = str(row.get("codigo.p", "")).strip()
        pollinator = str(row.get("codigo.i", "")).strip()
        flowers = _number(row.get("no.fl.obs"))
        visits = _number(row.get("no.fl.visit"))
        week = _week(row.get("date"))

        if year is None or not plant:
            continue

        if (
            plant in plant_codes
            and flowers is not None
            and flowers > 0
            and week is not None
            and site
        ):
            plant_cells[(year, plant)].add((site, week))

        positive = (
            visits is not None
            and visits > 0
            and pollinator in pollinator_codes
        )
        if not positive:
            continue

        if plant in plant_codes:
            positive_links[year].add((plant, pollinator))

        if week is not None and site:
            pollinator_cell_plants[(year, site, week, pollinator)].add(plant)

    output = []
    mismatch = 0
    for row in _read(args.stage1_dyads):
        previous_year = int(row["previous_period"])
        current_year = int(row["current_period"])
        plant = str(row["plant"]).strip()
        pollinator = str(row["pollinator"]).strip()
        previous_link = _bool(row["previous_link"])
        current_link = _bool(row["current_link"])

        if previous_link != ((plant, pollinator) in positive_links[previous_year]):
            mismatch += 1
        if current_link != ((plant, pollinator) in positive_links[current_year]):
            mismatch += 1

        p_cells = plant_cells.get((current_year, plant), set())
        q_cells = {
            (site, week)
            for site, week in {
                cell
                for year, site, week, q in pollinator_cell_plants
                if year == current_year and q == pollinator
            }
            if pollinator_cell_plants[
                (current_year, site, week, pollinator)
            ] - {plant}
        }
        overlap = p_cells & q_cells

        if previous_link:
            risk_set = "loss"
            outcome = int(not current_link)
        else:
            risk_set = "gain"
            outcome = int(current_link)

        output.append(
            {
                **row,
                "transition": f"{previous_year}->{current_year}",
                "risk_set": risk_set,
                "outcome": outcome,
                "siteweek_focal_excluded_overlap_cells": len(overlap),
                "plant_flowering_siteweeks": len(p_cells),
                "pollinator_otherplant_active_siteweeks": len(q_cells),
                "siteweek_opportunity_positive": int(bool(overlap)),
            }
        )

    if mismatch:
        raise SystemExit(
            f"raw response disagrees with Stage-1 response in {mismatch} states"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(output[0]) if output else []
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)


if __name__ == "__main__":
    main()
