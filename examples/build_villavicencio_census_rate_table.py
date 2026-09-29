"""Build an effort-standardized census-incidence response for Villavicencio.

Each row is one focal plant-pollinator dyad across one adjacent subseason
transition. The current response is the number of identifiable 5-min focal-
plant censuses in which the focal pollinator was detected, out of the number
of identifiable focal-plant censuses.

The candidate surface and current opportunity predictor exclude the focal
interaction: a pollinator must be independently detected on another plant in
both periods, and current site-week opportunity is defined only from visits to
other plants.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import date
from pathlib import Path


PRIMARY_TRANSITIONS = (
    ("2008_early", "2008_mid"),
    ("2008_mid", "2008_late"),
    ("2009_early", "2009_mid"),
    ("2009_mid", "2009_late"),
    ("2010_early", "2010_mid"),
    ("2010_mid", "2010_late"),
)


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


def _period(year: int, date_text: str) -> tuple[str, int] | None:
    text = "" if date_text is None else str(date_text).strip()
    if not text:
        return None
    try:
        observed = date.fromisoformat(text)
    except ValueError:
        return None
    if observed < date(year, 11, 1):
        season = "early"
    elif observed <= date(year, 11, 30):
        season = "mid"
    else:
        season = "late"
    return f"{year}_{season}", int(observed.isocalendar().week)


def _codes(path: Path, field: str) -> set[str]:
    return {
        str(row[field]).strip()
        for row in _read(path)
        if str(row.get(field, "")).strip()
    }


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("visits", type=Path)
    parser.add_argument("plant_names", type=Path)
    parser.add_argument("pollinator_names", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    trait_plants = _codes(args.plant_names, "plant_code")
    trait_pollinators = _codes(args.pollinator_names, "pol_code")

    # One record per identifiable 5-min focal-plant census.
    census_visitors: dict[
        tuple[str, str, str, str, str],
        set[str],
    ] = {}
    census_siteweek: dict[
        tuple[str, str, str, str, str],
        tuple[str, int],
    ] = {}

    # For focal-response-excluded pollinator activity.
    pollinator_cell_plants = defaultdict(set)

    missing_obs_time_rows = 0
    for row in _read(args.visits):
        site = str(row.get("site", "")).strip()
        year = _integer(row.get("year"))
        date_text = str(row.get("date", "")).strip()
        plant = str(row.get("codigo.p", "")).strip()
        obs_time = str(row.get("obs.time", "")).strip()
        if not site or year is None or not date_text or not plant:
            continue

        parsed = _period(year, date_text)
        if parsed is None:
            continue
        period, week = parsed

        if not obs_time or obs_time.lower() in {"na", "nan", "none"}:
            missing_obs_time_rows += 1
            continue

        key = (period, site, date_text, plant, obs_time)
        census_visitors.setdefault(key, set())
        census_siteweek[key] = (site, week)

        visits = _number(row.get("no.fl.visit")) or 0.0
        pollinator = str(row.get("codigo.i", "")).strip()
        if visits <= 0 or pollinator not in trait_pollinators:
            continue

        if plant in trait_plants:
            census_visitors[key].add(pollinator)

        # Any sampled plant may establish independent pollinator activity.
        pollinator_cell_plants[(period, site, week, pollinator)].add(plant)

    plant_period_censuses = defaultdict(list)
    for key, visitors in census_visitors.items():
        period, site, date_text, plant, obs_time = key
        if plant not in trait_plants:
            continue
        plant_period_censuses[(period, plant)].append(
            (key, visitors, census_siteweek[key])
        )

    rows = []
    transition_summary = []
    for previous_period, current_period in PRIMARY_TRANSITIONS:
        previous_plants = {
            plant
            for period, plant in plant_period_censuses
            if period == previous_period
        }
        current_plants = {
            plant
            for period, plant in plant_period_censuses
            if period == current_period
        }
        shared_plants = previous_plants & current_plants

        transition_rows = 0
        transition_current_successes = 0
        transition_current_trials = 0

        for plant in sorted(shared_plants):
            previous_censuses = plant_period_censuses[
                (previous_period, plant)
            ]
            current_censuses = plant_period_censuses[
                (current_period, plant)
            ]
            n_previous = len(previous_censuses)
            n_current = len(current_censuses)
            if n_previous < 1 or n_current < 1:
                continue

            current_plant_cells = {
                siteweek for _, _, siteweek in current_censuses
            }
            if not current_plant_cells:
                continue

            for pollinator in sorted(trait_pollinators):
                def otherplant_cells(period):
                    return {
                        (site, week)
                        for (
                            candidate_period,
                            site,
                            week,
                            candidate_pollinator,
                        ), plants in pollinator_cell_plants.items()
                        if candidate_period == period
                        and candidate_pollinator == pollinator
                        and (plants - {plant})
                    }

                previous_other_cells = otherplant_cells(previous_period)
                current_other_cells = otherplant_cells(current_period)
                if not previous_other_cells or not current_other_cells:
                    continue

                y_previous = sum(
                    pollinator in visitors
                    for _, visitors, _ in previous_censuses
                )
                y_current = sum(
                    pollinator in visitors
                    for _, visitors, _ in current_censuses
                )

                smoothed_previous = (
                    y_previous + 0.5
                ) / (n_previous + 1.0)
                history_logit = _logit(smoothed_previous)

                overlap_cells = (
                    current_plant_cells & current_other_cells
                )
                opportunity_fraction = (
                    len(overlap_cells) / len(current_plant_cells)
                )

                rows.append(
                    {
                        "transition": (
                            f"{previous_period}->{current_period}"
                        ),
                        "previous_period": previous_period,
                        "current_period": current_period,
                        "plant": plant,
                        "pollinator": pollinator,
                        "previous_success_censuses": y_previous,
                        "previous_trials": n_previous,
                        "current_success_censuses": y_current,
                        "current_trials": n_current,
                        "previous_smoothed_rate": smoothed_previous,
                        "previous_rate_logit": history_logit,
                        "current_siteweek_opportunity_fraction": (
                            opportunity_fraction
                        ),
                        "current_siteweek_overlap_cells": len(
                            overlap_cells
                        ),
                        "current_plant_siteweek_cells": len(
                            current_plant_cells
                        ),
                        "current_pollinator_otherplant_siteweek_cells": (
                            len(current_other_cells)
                        ),
                    }
                )
                transition_rows += 1
                transition_current_successes += y_current
                transition_current_trials += n_current

        transition_summary.append(
            {
                "transition": (
                    f"{previous_period}->{current_period}"
                ),
                "candidate_dyad_rows": transition_rows,
                "current_success_censuses": (
                    transition_current_successes
                ),
                "current_dyad_census_trials": (
                    transition_current_trials
                ),
            }
        )

    if not rows:
        raise SystemExit("census-rate analysis table is empty")

    expected = {
        f"{a}->{b}" for a, b in PRIMARY_TRANSITIONS
    }
    observed = {row["transition"] for row in rows}
    if observed != expected:
        raise SystemExit(
            f"missing primary transitions: {sorted(expected - observed)}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "schema": (
            "adaptive-gain-villavicencio-census-rate-table-v1"
        ),
        "date": "2026-09-29",
        "primary_scope": "strict_dated_core_2008_2010",
        "transition_count": len(PRIMARY_TRANSITIONS),
        "candidate_dyad_rows": len(rows),
        "total_current_dyad_census_trials": sum(
            int(row["current_trials"]) for row in rows
        ),
        "total_current_success_censuses": sum(
            int(row["current_success_censuses"])
            for row in rows
        ),
        "missing_obs_time_rows_excluded": missing_obs_time_rows,
        "transition_summary": transition_summary,
        "candidate_surface": (
            "plant censused in both periods and pollinator independently "
            "detected on another plant in both periods"
        ),
        "focal_response_excluded_from_candidate_surface": True,
        "focal_response_excluded_from_opportunity": True,
        "response": (
            "current focal interaction positive 5-min censuses out of "
            "current focal-plant 5-min censuses"
        ),
    }
    args.summary.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
