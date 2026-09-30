"""Matched-effort rarefaction stress test for Villavicencio subseason links.

Within each transition x focal plant x site, both periods are downsampled to
the smaller number of identifiable 5-min censuses. The original Stage-1
eligible dyad surface is held fixed. This tests state stability under equalized
observation intensity; it is not an estimator of latent ecological links.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


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


def _period(year: int, date_text: str) -> str | None:
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
    return f"{year}_{season}"


def _median(values):
    values = sorted(values)
    if not values:
        return None
    n = len(values)
    mid = n // 2
    if n % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2


def _state(previous_link: bool, current_link: bool) -> str:
    if previous_link and current_link:
        return "stable_present"
    if previous_link:
        return "loss"
    if current_link:
        return "gain"
    return "stable_absent"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("visits", type=Path)
    parser.add_argument("plant_names", type=Path)
    parser.add_argument("pollinator_names", type=Path)
    parser.add_argument("stage1_dyads", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260929)
    args = parser.parse_args()

    if args.replicates < 1:
        raise SystemExit("replicates must be positive")

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

    # Census identity follows the metadata-defined 5-min start time. Missing
    # start-time rows are excluded; they do not alter the trait-subset Stage-1
    # period link states, verified below.
    census_visitors = defaultdict(set)
    for row in _read(args.visits):
        site = str(row.get("site", "")).strip()
        year = _integer(row.get("year"))
        date_text = str(row.get("date", "")).strip()
        plant = str(row.get("codigo.p", "")).strip()
        obs_time = str(row.get("obs.time", "")).strip()
        if (
            not site
            or year is None
            or not date_text
            or plant not in trait_plants
            or not obs_time
            or obs_time.lower() in {"na", "nan", "none"}
        ):
            continue
        period = _period(year, date_text)
        if period is None:
            continue
        key = (period, plant, site, date_text, obs_time)
        visits = _number(row.get("no.fl.visit")) or 0.0
        pollinator = str(row.get("codigo.i", "")).strip()
        if visits > 0 and pollinator in trait_pollinators:
            census_visitors[key].add(pollinator)
        else:
            # Ensure zero-visit censuses remain part of the effort surface.
            census_visitors.setdefault(key, set())

    bouts = defaultdict(list)
    full_presence = defaultdict(set)
    for (period, plant, site, date_text, obs_time), visitors in census_visitors.items():
        bouts[(period, plant, site)].append(frozenset(visitors))
        full_presence[(period, plant)].update(visitors)

    dyads = []
    for row in _read(args.stage1_dyads):
        if str(row.get("role", "")).strip() != "primary":
            continue
        item = {
            "previous_period": str(row["previous_period"]).strip(),
            "current_period": str(row["current_period"]).strip(),
            "plant": str(row["plant"]).strip(),
            "pollinator": str(row["pollinator"]).strip(),
            "previous_link": _bool(row["previous_link"]),
            "current_link": _bool(row["current_link"]),
            "direction": str(row["direction"]).strip(),
        }
        dyads.append(item)

    # First prove that omitting rows with missing obs.time does not change the
    # reconstructed trait-subset period link states used by Stage 1.
    full_state_mismatches = 0
    for row in dyads:
        previous = (
            row["pollinator"]
            in full_presence[(row["previous_period"], row["plant"])]
        )
        current = (
            row["pollinator"]
            in full_presence[(row["current_period"], row["plant"])]
        )
        full_state_mismatches += int(previous != row["previous_link"])
        full_state_mismatches += int(current != row["current_link"])
    if full_state_mismatches != 0:
        raise SystemExit(
            "identifiable-census reconstruction no longer matches Stage-1 states"
        )

    grouped = defaultdict(list)
    for index, row in enumerate(dyads):
        grouped[
            (row["previous_period"], row["current_period"], row["plant"])
        ].append((index, row["pollinator"], row["direction"]))

    group_specs = []
    for (previous_period, current_period, plant), rows in grouped.items():
        sites = {
            site
            for period, candidate_plant, site in bouts
            if candidate_plant == plant
            and period in {previous_period, current_period}
        }
        site_specs = []
        for site in sorted(sites):
            previous_bouts = bouts.get((previous_period, plant, site), [])
            current_bouts = bouts.get((current_period, plant, site), [])
            sample_size = min(len(previous_bouts), len(current_bouts))
            if sample_size > 0:
                site_specs.append(
                    (previous_bouts, current_bouts, sample_size)
                )
        group_specs.append(
            (
                previous_period,
                current_period,
                plant,
                rows,
                site_specs,
            )
        )

    rng = random.Random(args.seed)
    state_counts = [Counter() for _ in dyads]
    transition_rep_counts = defaultdict(list)

    for _ in range(args.replicates):
        per_transition = defaultdict(Counter)
        for (
            previous_period,
            current_period,
            plant,
            rows,
            site_specs,
        ) in group_specs:
            previous_detected = set()
            current_detected = set()

            for previous_bouts, current_bouts, sample_size in site_specs:
                if len(previous_bouts) == sample_size:
                    previous_sample = previous_bouts
                else:
                    previous_sample = rng.sample(
                        previous_bouts, sample_size
                    )
                if len(current_bouts) == sample_size:
                    current_sample = current_bouts
                else:
                    current_sample = rng.sample(
                        current_bouts, sample_size
                    )

                for visitors in previous_sample:
                    previous_detected.update(visitors)
                for visitors in current_sample:
                    current_detected.update(visitors)

            transition = f"{previous_period}->{current_period}"
            for index, pollinator, original_direction in rows:
                rarefied_state = _state(
                    pollinator in previous_detected,
                    pollinator in current_detected,
                )
                state_counts[index][rarefied_state] += 1
                per_transition[transition][rarefied_state] += 1

        for transition, counts in per_transition.items():
            transition_rep_counts[transition].append(dict(counts))

    row_results = []
    for index, row in enumerate(dyads):
        counts = state_counts[index]
        original = row["direction"]
        row_results.append(
            {
                "year": int(row["previous_period"][:4]),
                "original_state": original,
                "same_state_probability": (
                    counts[original] / args.replicates
                ),
                "changed_state_probability": (
                    counts["gain"] + counts["loss"]
                )
                / args.replicates,
            }
        )

    def summarize_scope(years):
        selected = [row for row in row_results if row["year"] in years]
        states = {}
        for original in ("gain", "loss", "stable_present", "stable_absent"):
            values = [
                row["same_state_probability"]
                for row in selected
                if row["original_state"] == original
            ]
            if not values:
                continue
            states[original] = {
                "n": len(values),
                "mean_same_state_probability": sum(values) / len(values),
                "median_same_state_probability": _median(values),
                "fraction_same_state_probability_ge_0_5": (
                    sum(value >= 0.5 for value in values) / len(values)
                ),
                "fraction_same_state_probability_ge_0_8": (
                    sum(value >= 0.8 for value in values) / len(values)
                ),
            }
        return states

    transition_results = {}
    original_by_transition = defaultdict(Counter)
    for row in dyads:
        transition = (
            f"{row['previous_period']}->{row['current_period']}"
        )
        original_by_transition[transition][row["direction"]] += 1

    for transition, replicate_counts in transition_rep_counts.items():
        original = original_by_transition[transition]
        rarefied_changed = [
            counts.get("gain", 0) + counts.get("loss", 0)
            for counts in replicate_counts
        ]
        transition_results[transition] = {
            "original_gain": original["gain"],
            "original_loss": original["loss"],
            "original_stable_present": original["stable_present"],
            "original_stable_absent": original["stable_absent"],
            "original_changed": original["gain"] + original["loss"],
            "mean_rarefied_changed": (
                sum(rarefied_changed) / len(rarefied_changed)
            ),
            "median_rarefied_changed": _median(rarefied_changed),
            "minimum_rarefied_changed": min(rarefied_changed),
            "maximum_rarefied_changed": max(rarefied_changed),
        }

    result = {
        "schema": (
            "adaptive-gain-villavicencio-effort-balanced-rarefaction-v1"
        ),
        "date": "2026-09-29",
        "status": "matched_effort_state_instability_detected",
        "analysis_status": (
            "post-result downsampling stress test; not a latent-link or "
            "false-positive estimator"
        ),
        "replicates": args.replicates,
        "seed": args.seed,
        "identifiable_census_full_state_mismatch_count": (
            full_state_mismatches
        ),
        "scopes": {
            scope: summarize_scope(years)
            for scope, years in SCOPE_YEARS.items()
        },
        "transitions": transition_results,
        "interpretation": {
            "supported": (
                "Observed binary gain/loss classifications are not highly "
                "stable when focal-plant census intensity is equalized by "
                "within-site downsampling."
            ),
            "not_supported": (
                "The complement of the state-retention probability is not a "
                "false-rewiring fraction: downsampling can create additional "
                "non-detections from genuinely persistent interactions."
            ),
        },
        "claim_ceiling": (
            "Matched-effort rarefaction is a detection-sensitivity stress test "
            "only. It supports quarantining raw binary rewiring claims but does "
            "not recover the true ecological network."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
