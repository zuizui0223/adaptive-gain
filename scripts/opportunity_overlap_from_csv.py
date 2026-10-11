"""Compute opportunity-weighted performance from empirical completion-time CSV files.

Input completion CSV:
    architecture,completion_time
where completion_time is a nonnegative number or "inf".

Input opportunity CSV:
    opportunity_limit
with finite nonnegative values.

The plug-in estimator treats completion times and opportunity limits as
independent empirical samples and computes P(T <= B) over their Cartesian
product. Use only when that independence/composition is biologically justified.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

from adaptive_gain.opportunity_fitness import (
    empirical_pairwise_log_selection,
    empirical_timely_success_probability,
)


def _read_completion_times(path: Path) -> dict[str, list[float]]:
    rows: dict[str, list[float]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"architecture", "completion_time"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(
                "completion CSV requires architecture,completion_time columns"
            )
        for row in reader:
            architecture = row["architecture"].strip()
            if not architecture:
                raise ValueError("architecture labels must be nonempty")
            raw = row["completion_time"].strip().lower()
            value = math.inf if raw in {"inf", "infinity"} else float(raw)
            if math.isnan(value) or value < 0:
                raise ValueError("completion_time must be nonnegative or inf")
            rows[architecture].append(value)
    if not rows:
        raise ValueError("completion CSV contained no observations")
    return dict(rows)


def _read_opportunity_limits(path: Path) -> list[float]:
    values: list[float] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "opportunity_limit" not in reader.fieldnames:
            raise ValueError("opportunity CSV requires opportunity_limit column")
        for row in reader:
            value = float(row["opportunity_limit"])
            if not math.isfinite(value) or value < 0:
                raise ValueError("opportunity limits must be finite and nonnegative")
            values.append(value)
    if not values:
        raise ValueError("opportunity CSV contained no observations")
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--completion-csv", required=True, type=Path)
    parser.add_argument("--opportunity-csv", required=True, type=Path)
    parser.add_argument("--focal", required=True)
    parser.add_argument("--comparator", required=True)
    parser.add_argument("--baseline-fitness", type=float, default=1.0)
    parser.add_argument("--resolution-value", type=float, default=1.0)
    parser.add_argument("--focal-maintenance-log-cost", type=float, default=0.0)
    parser.add_argument("--comparator-maintenance-log-cost", type=float, default=0.0)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()

    completion = _read_completion_times(args.completion_csv)
    limits = _read_opportunity_limits(args.opportunity_csv)

    if args.focal not in completion:
        raise ValueError(f"unknown focal architecture: {args.focal}")
    if args.comparator not in completion:
        raise ValueError(f"unknown comparator architecture: {args.comparator}")

    q = {
        name: empirical_timely_success_probability(times, limits)
        for name, times in completion.items()
    }

    selection = empirical_pairwise_log_selection(
        completion[args.focal],
        completion[args.comparator],
        limits,
        baseline_fitness=args.baseline_fitness,
        resolution_value=args.resolution_value,
        focal_maintenance_log_cost=args.focal_maintenance_log_cost,
        comparator_maintenance_log_cost=args.comparator_maintenance_log_cost,
    )

    result = {
        "scope": "independent_empirical_completion_and_opportunity_samples",
        "completion_csv": str(args.completion_csv),
        "opportunity_csv": str(args.opportunity_csv),
        "n_completion": {name: len(v) for name, v in completion.items()},
        "n_opportunity": len(limits),
        "timely_success_probability": q,
        "focal": args.focal,
        "comparator": args.comparator,
        "pairwise_log_selection": selection,
        "baseline_fitness": args.baseline_fitness,
        "resolution_value": args.resolution_value,
        "focal_maintenance_log_cost": args.focal_maintenance_log_cost,
        "comparator_maintenance_log_cost": args.comparator_maintenance_log_cost,
    }

    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output_json is not None:
        args.output_json.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
