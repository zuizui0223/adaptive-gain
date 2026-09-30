"""Export a deterministic balanced schedule for the direct routeability experiment."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

from adaptive_gain.routeability_experiment_schedule import (
    build_between_subject_routeability_schedule,
    schedule_balance_audit,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("schedule_csv", type=Path)
    parser.add_argument("receipt_json", type=Path)
    parser.add_argument("--individuals-per-cell", type=int, required=True)
    parser.add_argument("--blocks-per-individual", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()

    trials = build_between_subject_routeability_schedule(
        individuals_per_cell=args.individuals_per_cell,
        blocks_per_individual=args.blocks_per_individual,
        seed=args.seed,
    )
    audit = schedule_balance_audit(trials)

    rows = []
    for trial in trials:
        row = asdict(trial)
        row["revealed_cues"] = ">".join(trial.revealed_cues)
        rows.append(row)

    fields = list(rows[0]) if rows else []
    with args.schedule_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    receipt = {
        "schema": "adaptive-gain-routeability-experiment-schedule-v1",
        "design": "between-subject architecture x access x budget",
        "individuals_per_cell": args.individuals_per_cell,
        "blocks_per_individual": args.blocks_per_individual,
        "trials_per_individual": 4 * args.blocks_per_individual,
        "seed": args.seed,
        "audit": audit,
        "sample_size_status": (
            "placeholder_for_schedule_validation_not_final_powered_sample_size"
        ),
        "claim_ceiling": (
            "The schedule freezes randomization and counterbalancing mechanics. "
            "It does not set the definitive biological sample size."
        ),
    }
    args.receipt_json.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
