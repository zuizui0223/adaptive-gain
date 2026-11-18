"""Build focal-response-excluded weekly opportunity surfaces for Villavicencio.

The published phenological-overlap matrix is not used here. For each focal
plant-pollinator dyad, opportunity is reconstructed from raw Figshare records
as overlap between:

1. weeks in which the focal plant was observed flowering; and
2. weeks in which the focal pollinator was observed visiting any *other* plant.

Two predictor surfaces are exported for every annual transition:
- current: reconstructed from the target/current year;
- lagged: reconstructed from the previous year only.

Thus the focal dyad's own realized interaction never contributes to either
opportunity predictor. Undated positive visits may define annual response links
but never contribute to weekly opportunity.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path


YEARS = tuple(range(2006, 2012))


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _number(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _integer(value: object) -> int | None:
    number = _number(value)
    if number is None:
        return None
    return int(number)


def _bool(value: object) -> bool:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"unrecognized boolean value: {value!r}")


def _week(value: object) -> int | None:
    text = "" if value is None else str(value).strip()
    if not text:
        return None
    try:
        return int(date.fromisoformat(text).isocalendar().week)
    except ValueError:
        return None


def _code_set(path: Path, field: str) -> set[str]:
    rows = _read_rows(path)
    out = {
        str(row[field]).strip()
        for row in rows
        if str(row.get(field, "")).strip()
    }
    if not out:
        raise ValueError(f"{path}: no codes found in {field}")
    return out


def _opportunity_features(
    year: int,
    plant: str,
    pollinator: str,
    *,
    plant_flowering_weeks: dict[tuple[int, str], set[int]],
    pollinator_week_plants: dict[tuple[int, int, str], set[str]],
) -> tuple[int, int, int, int]:
    plant_weeks = plant_flowering_weeks.get((year, plant), set())
    pollinator_otherplant_weeks = {
        week
        for week in range(1, 54)
        if pollinator_week_plants.get(
            (year, week, pollinator),
            set(),
        )
        - {plant}
    }
    overlap_weeks = plant_weeks & pollinator_otherplant_weeks
    return (
        len(overlap_weeks),
        len(plant_weeks),
        len(pollinator_otherplant_weeks),
        int(bool(overlap_weeks)),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("visits", type=Path)
    parser.add_argument("plant_names", type=Path)
    parser.add_argument("pollinator_names", type=Path)
    parser.add_argument("stage1_dyads", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    plant_codes = _code_set(args.plant_names, "plant_code")
    pollinator_codes = _code_set(args.pollinator_names, "pol_code")

    positive_links_by_year: dict[int, set[tuple[str, str]]] = {
        year: set() for year in YEARS
    }
    dated_positive_links: set[tuple[str, str]] = set()
    plant_flowering_weeks: dict[tuple[int, str], set[int]] = defaultdict(set)
    pollinator_week_plants: dict[tuple[int, int, str], set[str]] = defaultdict(set)

    undated_positive_rows_trait_subset = 0

    for row in _read_rows(args.visits):
        year = _integer(row.get("year"))
        plant = str(row.get("codigo.p", "")).strip()
        pollinator = str(row.get("codigo.i", "")).strip()
        flowers = _number(row.get("no.fl.obs"))
        visits = _number(row.get("no.fl.visit"))
        week = _week(row.get("date"))

        if year not in YEARS or not plant:
            continue

        if (
            plant in plant_codes
            and flowers is not None
            and flowers > 0
            and week is not None
        ):
            plant_flowering_weeks[(year, plant)].add(week)

        positive_visit = (
            visits is not None
            and visits > 0
            and pollinator
            and pollinator in pollinator_codes
        )
        if not positive_visit:
            continue

        if plant in plant_codes:
            positive_links_by_year[year].add((plant, pollinator))
            if week is None:
                undated_positive_rows_trait_subset += 1
            else:
                dated_positive_links.add((plant, pollinator))

        if week is not None:
            # Any sampled plant may provide independent evidence that the
            # pollinator was active; the focal plant is removed dyad by dyad.
            pollinator_week_plants[(year, week, pollinator)].add(plant)

    stage1_rows = _read_rows(args.stage1_dyads)
    output_rows: list[dict[str, object]] = []
    response_mismatch_count = 0

    for row in stage1_rows:
        previous_year = int(row["previous_period"])
        current_year = int(row["current_period"])
        plant = str(row["plant"]).strip()
        pollinator = str(row["pollinator"]).strip()
        previous_link = _bool(row["previous_link"])
        current_link = _bool(row["current_link"])

        raw_previous_link = (
            plant,
            pollinator,
        ) in positive_links_by_year.get(previous_year, set())
        raw_current_link = (
            plant,
            pollinator,
        ) in positive_links_by_year.get(current_year, set())
        if previous_link != raw_previous_link or current_link != raw_current_link:
            response_mismatch_count += 1

        (
            current_overlap,
            current_plant_weeks,
            current_pollinator_weeks,
            current_positive,
        ) = _opportunity_features(
            current_year,
            plant,
            pollinator,
            plant_flowering_weeks=plant_flowering_weeks,
            pollinator_week_plants=pollinator_week_plants,
        )
        (
            lagged_overlap,
            lagged_plant_weeks,
            lagged_pollinator_weeks,
            lagged_positive,
        ) = _opportunity_features(
            previous_year,
            plant,
            pollinator,
            plant_flowering_weeks=plant_flowering_weeks,
            pollinator_week_plants=pollinator_week_plants,
        )

        if previous_link:
            risk_set = "loss"
            outcome = int(not current_link)
        else:
            risk_set = "gain"
            outcome = int(current_link)

        output_rows.append(
            {
                **row,
                "transition": f"{previous_year}->{current_year}",
                "risk_set": risk_set,
                "outcome": outcome,
                "target_year": current_year,
                "focal_excluded_overlap_weeks": current_overlap,
                "plant_flowering_weeks": current_plant_weeks,
                "pollinator_otherplant_active_weeks": current_pollinator_weeks,
                "focal_excluded_opportunity_positive": current_positive,
                "lagged_focal_excluded_overlap_weeks": lagged_overlap,
                "lagged_plant_flowering_weeks": lagged_plant_weeks,
                "lagged_pollinator_otherplant_active_weeks": lagged_pollinator_weeks,
                "lagged_focal_excluded_opportunity_positive": lagged_positive,
            }
        )

    if response_mismatch_count:
        raise SystemExit(
            "raw Figshare response disagrees with Stage-1 annual response in "
            f"{response_mismatch_count} dyad rows"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(output_rows[0]) if output_rows else []
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    all_dyads = {
        (plant, pollinator)
        for plant in plant_codes
        for pollinator in pollinator_codes
    }
    ever_linked = set().union(
        *(positive_links_by_year[year] for year in YEARS)
    )

    opportunity_positive_any_year: set[tuple[str, str]] = set()
    annual_support = {}
    for year in YEARS:
        year_positive: set[tuple[str, str]] = set()
        for plant, pollinator in all_dyads:
            overlap, _, _, positive = _opportunity_features(
                year,
                plant,
                pollinator,
                plant_flowering_weeks=plant_flowering_weeks,
                pollinator_week_plants=pollinator_week_plants,
            )
            if positive and overlap > 0:
                year_positive.add((plant, pollinator))
        opportunity_positive_any_year |= year_positive
        realized = positive_links_by_year[year]
        annual_support[str(year)] = {
            "realized_link_count": len(realized),
            "opportunity_positive_count": len(year_positive),
            "opportunity_positive_realized_count": len(
                year_positive & realized
            ),
            "opportunity_positive_unrealized_count": len(
                year_positive - realized
            ),
        }

    never_linked = all_dyads - ever_linked
    only_undated_ever_linked = ever_linked - dated_positive_links
    support_positive = len(opportunity_positive_any_year)

    risk_summary = {}
    for risk in ("gain", "loss"):
        rows = [row for row in output_rows if row["risk_set"] == risk]
        events = [row for row in rows if int(row["outcome"]) == 1]
        nonevents = [row for row in rows if int(row["outcome"]) == 0]

        def _fraction(group, field):
            if not group:
                return None
            return sum(int(row[field]) for row in group) / len(group)

        risk_summary[risk] = {
            "n": len(rows),
            "events": len(events),
            "current_opportunity_positive_fraction": _fraction(
                rows, "focal_excluded_opportunity_positive"
            ),
            "current_event_opportunity_positive_fraction": _fraction(
                events, "focal_excluded_opportunity_positive"
            ),
            "current_nonevent_opportunity_positive_fraction": _fraction(
                nonevents, "focal_excluded_opportunity_positive"
            ),
            "lagged_opportunity_positive_fraction": _fraction(
                rows, "lagged_focal_excluded_opportunity_positive"
            ),
            "lagged_event_opportunity_positive_fraction": _fraction(
                events, "lagged_focal_excluded_opportunity_positive"
            ),
            "lagged_nonevent_opportunity_positive_fraction": _fraction(
                nonevents, "lagged_focal_excluded_opportunity_positive"
            ),
        }

    summary = {
        "schema": (
            "adaptive-gain-villavicencio-focal-excluded-opportunity-table-v1"
        ),
        "date": "2026-09-28",
        "row_count": len(output_rows),
        "response_mismatch_count": response_mismatch_count,
        "trait_subset": {
            "plant_count": len(plant_codes),
            "pollinator_count": len(pollinator_codes),
            "dyad_surface": len(all_dyads),
        },
        "support_audit": {
            "ever_linked_count": len(ever_linked),
            "never_linked_count": len(never_linked),
            "opportunity_positive_any_year_count": support_positive,
            "opportunity_positive_ever_linked_count": len(
                opportunity_positive_any_year & ever_linked
            ),
            "opportunity_positive_never_linked_count": len(
                opportunity_positive_any_year & never_linked
            ),
            "probability_ever_linked_given_opportunity_positive": (
                len(opportunity_positive_any_year & ever_linked)
                / support_positive
                if support_positive
                else None
            ),
            "opportunity_support_nested_in_ever_linked": (
                len(opportunity_positive_any_year & never_linked) == 0
            ),
        },
        "annual_support": annual_support,
        "date_completeness": {
            "undated_positive_visit_rows_trait_subset": (
                undated_positive_rows_trait_subset
            ),
            "ever_linked_dyads_without_any_dated_positive_visit": len(
                only_undated_ever_linked
            ),
        },
        "risk_sets_all_annual": risk_summary,
        "focal_response_exclusion": True,
        "current_year_surface": True,
        "one_year_lagged_surface": True,
        "published_phenological_overlap_used": False,
        "published_aggregate_flower_abundance_used": False,
    }
    args.summary.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
