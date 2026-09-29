"""Audit sampling effort and detection sensitivity for Villavicencio subseasons.

The raw metadata define obs.time as the start time of a 5-min observation
period. A census is therefore identified by site x study-year x date x focal
plant x obs.time. The exact annual counts are checked against Chacoff et al.
(2018) Table 1 before any subseason diagnostic is accepted.

This module is a post-result bias audit. It does not estimate true latent links
and must not be used to relabel observed binary turnover as ecological rewiring.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


PUBLISHED_ANNUAL_CENSUSES = {
    2006: 532,
    2007: 372,
    2008: 530,
    2009: 836,
    2010: 460,
    2011: 988,
}

SCOPE_YEARS = {
    "strict_dated_core_2008_2010": {2008, 2009, 2010},
    "core_sites_2008_2011": {2008, 2009, 2010, 2011},
    "all_2006_2011": {2006, 2007, 2008, 2009, 2010, 2011},
}


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


def _bool(value):
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"unrecognized boolean value: {value!r}")


def _subseason(study_year: int, text: str) -> str | None:
    text = "" if text is None else str(text).strip()
    if not text:
        return None
    try:
        observed = date.fromisoformat(text)
    except ValueError:
        return None
    if observed < date(study_year, 11, 1):
        return "early"
    if observed <= date(study_year, 11, 30):
        return "mid"
    return "late"


def _auc(y, score):
    positives = sum(y)
    negatives = len(y) - positives
    if positives == 0 or negatives == 0:
        return None
    ordered = sorted(zip(score, y), key=lambda item: item[0])
    rank_sum = 0.0
    rank = 1
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = (rank + (rank + end - index - 1)) / 2
        rank_sum += average_rank * sum(v for _, v in ordered[index:end])
        rank += end - index
        index = end
    return (
        rank_sum - positives * (positives + 1) / 2
    ) / (positives * negatives)


def _chao2_bias_corrected(incidences):
    s_obs = len(incidences)
    q1 = sum(value == 1 for value in incidences)
    q2 = sum(value == 2 for value in incidences)
    estimate = s_obs + (q1 * (q1 - 1)) / (2 * (q2 + 1))
    completeness = None if estimate <= 0 else s_obs / estimate
    return {
        "observed_links": s_obs,
        "q1_single_census_links": q1,
        "q2_double_census_links": q2,
        "chao2_bias_corrected": estimate,
        "observed_fraction_of_chao2": completeness,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("visits", type=Path)
    parser.add_argument("plant_names", type=Path)
    parser.add_argument("pollinator_names", type=Path)
    parser.add_argument("stage1_dyads", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--plant-effort-output", type=Path, required=True)
    args = parser.parse_args()

    trait_plants = {
        str(row["plant_code"]).strip()
        for row in _read(args.plant_names)
        if str(row.get("plant_code", "")).strip()
    }
    trait_pollinators = {
        str(row["pol_code"]).strip()
        for row in _read(args.pollinator_names)
        if str(row.get("pol_code", "")).strip()
    }

    census_rows = {}
    positive_link_census = defaultdict(set)
    missing_obs_time_rows = 0
    dated_rows = 0

    for row in _read(args.visits):
        site = str(row.get("site", "")).strip()
        year = _integer(row.get("year"))
        date_text = str(row.get("date", "")).strip()
        plant = str(row.get("codigo.p", "")).strip()
        obs_time = str(row.get("obs.time", "")).strip()
        if not site or year is None or not date_text or not plant:
            continue
        subseason = _subseason(year, date_text)
        if subseason is None:
            continue
        dated_rows += 1
        if not obs_time or obs_time.lower() in {"na", "nan", "none"}:
            missing_obs_time_rows += 1
            continue

        period = f"{year}_{subseason}"
        key = (site, year, date_text, plant, obs_time)
        census_rows[key] = {
            "site": site,
            "year": year,
            "date": date_text,
            "plant": plant,
            "obs_time": obs_time,
            "period": period,
        }

        visits = _number(row.get("no.fl.visit")) or 0.0
        pollinator = str(row.get("codigo.i", "")).strip()
        if visits > 0 and plant in trait_plants and pollinator in trait_pollinators:
            positive_link_census[(period, plant, pollinator)].add(key)

    annual_counts = Counter()
    period_censuses = Counter()
    period_sites = defaultdict(set)
    period_dates = defaultdict(set)
    period_site_dates = defaultdict(set)
    period_plants = defaultdict(set)
    plant_period_censuses = Counter()

    for record in census_rows.values():
        year = record["year"]
        period = record["period"]
        plant = record["plant"]
        annual_counts[year] += 1
        period_censuses[period] += 1
        period_sites[period].add(record["site"])
        period_dates[period].add(record["date"])
        period_site_dates[period].add((record["site"], record["date"]))
        period_plants[period].add(plant)
        plant_period_censuses[(period, plant)] += 1

    annual_validation = {}
    exact_match_years = []
    discrepancies = {}
    for year, expected in PUBLISHED_ANNUAL_CENSUSES.items():
        observed = annual_counts[year]
        difference = observed - expected
        match = difference == 0
        if match:
            exact_match_years.append(year)
        else:
            discrepancies[str(year)] = difference
        annual_validation[str(year)] = {
            "observed_unique_5min_censuses": observed,
            "published_total_censuses": expected,
            "difference_raw_minus_published": difference,
            "exact_match": match,
        }

    expected_discrepancies = {"2010": 3}
    census_identity_validated = (
        exact_match_years == [2006, 2007, 2008, 2009, 2011]
        and discrepancies == expected_discrepancies
    )
    if not census_identity_validated:
        raise SystemExit(
            "raw census identity changed: "
            f"exact={exact_match_years!r}, discrepancies={discrepancies!r}"
        )

    periods = []
    for year in range(2006, 2012):
        for subseason in ("early", "mid", "late"):
            period = f"{year}_{subseason}"
            periods.append(
                {
                    "period": period,
                    "censuses": period_censuses[period],
                    "minutes": 5 * period_censuses[period],
                    "sites": len(period_sites[period]),
                    "sampled_dates": len(period_dates[period]),
                    "site_days": len(period_site_dates[period]),
                    "focal_plants": len(period_plants[period]),
                }
            )

    # Incidence-based link completeness on the exact 45 x 135 Stage-1 subset.
    by_period_link_incidence = defaultdict(list)
    for (period, plant, pollinator), census_keys in positive_link_census.items():
        by_period_link_incidence[period].append(len(census_keys))
    completeness = {
        period: _chao2_bias_corrected(by_period_link_incidence[period])
        for period in [row["period"] for row in periods]
    }

    # Export plant-period effort so the held-out effort-only diagnostic can
    # reuse exactly the same census reconstruction.
    args.plant_effort_output.parent.mkdir(parents=True, exist_ok=True)
    with args.plant_effort_output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["period", "plant", "censuses", "minutes"],
        )
        writer.writeheader()
        for (period, plant), count in sorted(plant_period_censuses.items()):
            writer.writerow(
                {
                    "period": period,
                    "plant": plant,
                    "censuses": count,
                    "minutes": 5 * count,
                }
            )

    plant_effort = plant_period_censuses
    changed_rows = []
    endpoint_effort = {
        "gain": {0: [], 1: []},
        "loss": {0: [], 1: []},
    }

    for row in _read(args.stage1_dyads):
        if str(row.get("role", "")).strip() != "primary":
            continue
        previous_period = str(row["previous_period"]).strip()
        current_period = str(row["current_period"]).strip()
        plant = str(row["plant"]).strip()
        previous_link = _bool(row["previous_link"])
        current_link = _bool(row["current_link"])
        previous_effort = plant_effort[(previous_period, plant)]
        current_effort = plant_effort[(current_period, plant)]
        score = math.log1p(current_effort) - math.log1p(previous_effort)

        if previous_link:
            risk = "loss"
            outcome = int(not current_link)
        else:
            risk = "gain"
            outcome = int(current_link)
        endpoint_effort[risk][outcome].append(
            {
                "previous_censuses": previous_effort,
                "current_censuses": current_effort,
                "delta_censuses": current_effort - previous_effort,
                "delta_log_censuses": score,
            }
        )

        if previous_link != current_link:
            year = int(previous_period[:4])
            changed_rows.append(
                {
                    "year": year,
                    "direction": "gain" if current_link else "loss",
                    "score": score,
                }
            )

    def mean(values):
        return None if not values else sum(values) / len(values)

    endpoint_summary = {}
    for risk in ("gain", "loss"):
        endpoint_summary[risk] = {}
        for outcome in (0, 1):
            values = endpoint_effort[risk][outcome]
            endpoint_summary[risk][str(outcome)] = {
                "n": len(values),
                "mean_previous_censuses": mean(
                    [item["previous_censuses"] for item in values]
                ),
                "mean_current_censuses": mean(
                    [item["current_censuses"] for item in values]
                ),
                "mean_delta_censuses": mean(
                    [item["delta_censuses"] for item in values]
                ),
                "mean_delta_log_censuses": mean(
                    [item["delta_log_censuses"] for item in values]
                ),
            }

    direction_auc = {}
    for scope, years in SCOPE_YEARS.items():
        selected = [row for row in changed_rows if row["year"] in years]
        y = [int(row["direction"] == "gain") for row in selected]
        score = [row["score"] for row in selected]
        direction_auc[scope] = {
            "changed_dyads": len(selected),
            "gains": sum(y),
            "losses": len(y) - sum(y),
            "auc_effort_increase_ranks_gain_over_loss": _auc(y, score),
        }

    observed_fractions = [
        item["observed_fraction_of_chao2"]
        for item in completeness.values()
        if item["observed_fraction_of_chao2"] is not None
    ]

    result = {
        "schema": "adaptive-gain-villavicencio-subseason-effort-audit-v1",
        "date": "2026-09-29",
        "status": "effort_semantics_resolved_detection_sensitivity_material",
        "analysis_status": (
            "post-result bias audit; sampling effort is now reconstructable, "
            "but true link state is not identified"
        ),
        "census_semantics": {
            "unit": "5-min focal-plant observation census",
            "identity": ["site", "year", "date", "codigo.p", "obs.time"],
            "annual_validation": annual_validation,
            "census_identity_validated_with_documented_2010_discrepancy": (
                census_identity_validated
            ),
            "exact_match_years": exact_match_years,
            "raw_minus_published_discrepancies": discrepancies,
            "dated_rows_considered": dated_rows,
            "rows_missing_obs_time_excluded_from_exact_census_identity": (
                missing_obs_time_rows
            ),
        },
        "subseason_effort": periods,
        "trait_subset_chao2_completeness": {
            "periods": completeness,
            "minimum_observed_fraction": min(observed_fractions),
            "maximum_observed_fraction": max(observed_fractions),
            "interpretation": (
                "incidence Chao2 indicates incomplete binary-link detection "
                "within many subseasons; this is descriptive and does not "
                "supply corrected dyad states"
            ),
        },
        "endpoint_effort_contrast": endpoint_summary,
        "changed_dyad_direction_effort_auc": direction_auc,
        "ecological_read": {
            "supported": (
                "The raw-data meaning of effort is no longer unresolved: 5-min "
                "census counts are reconstructable, with exact agreement to "
                "published annual totals in five years and a documented raw "
                "excess of three censuses in 2010. Focal-plant census effort is "
                "strongly aligned with observed gain/loss direction, so binary "
                "link turnover is materially detection-sensitive."
            ),
            "important_boundary": (
                "Census allocation is partly coupled to flowering availability, "
                "so the effort association cannot be called pure observer bias. "
                "It nevertheless prevents observed zero/nonzero transitions from "
                "being identified as true ecological rewiring."
            ),
        },
        "not_established": [
            "true interaction absence when a link is unobserved",
            "sampling-effort-corrected rewiring",
            "fraction of the 853 observed changes that are biological rather than detection-driven",
            "routeability",
        ],
        "claim_ceiling": (
            "Use the reconstructed 18-period binary response for feasibility "
            "and detection audits only. Until a detection-standardized response "
            "is used, describe gain/loss as observed-link turnover rather than "
            "ecological rewiring."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
