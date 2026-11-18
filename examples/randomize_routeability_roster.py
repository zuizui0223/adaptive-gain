"""Randomize an architecture-neutral eligible roster in complete colony blocks."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from adaptive_gain.routeability_roster_randomization import (
    randomize_roster_complete_colony_blocks,
)

FORBIDDEN_COLUMNS = {
    "architecture",
    "access",
    "access_mode",
    "budget",
    "treatment",
    "treatment_cell",
    "training_accuracy",
    "test_accuracy",
    "accuracy",
    "outcome",
    "success",
    "correct",
    "reward",
    "h1",
    "h2",
}


def _read_roster(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or ())
        required = {"individual_id", "colony_id"}
        if not required <= fields:
            raise ValueError(
                f"roster CSV must contain {sorted(required)}"
            )
        leaked = sorted(
            column
            for column in fields
            if column.strip().lower() in FORBIDDEN_COLUMNS
        )
        if leaked:
            raise ValueError(
                "eligible roster contains forbidden treatment/outcome columns: "
                + ", ".join(leaked)
            )
        rows = [
            (row["individual_id"], row["colony_id"])
            for row in reader
        ]
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("roster_csv", type=Path)
    parser.add_argument("assignments_csv", type=Path)
    parser.add_argument("unassigned_csv", type=Path)
    parser.add_argument("receipt_json", type=Path)
    parser.add_argument("--individuals-per-cell", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--eligibility-rule", required=True)
    args = parser.parse_args()

    eligibility_rule = args.eligibility_rule.strip()
    if not eligibility_rule:
        raise ValueError("eligibility-rule must be non-empty")
    if any(
        token in eligibility_rule.lower()
        for token in (
            "routeable accuracy",
            "bypass accuracy",
            "architecture-specific accuracy",
            "test accuracy",
            "h1",
            "h2",
        )
    ):
        raise ValueError(
            "eligibility-rule appears to depend on focal treatment performance"
        )

    roster = _read_roster(args.roster_csv)
    assignments, unassigned, receipt = randomize_roster_complete_colony_blocks(
        roster,
        individuals_per_cell=args.individuals_per_cell,
        seed=args.seed,
    )

    assignment_fields = [
        "individual_id",
        "colony_id",
        "complete_block_id",
        "architecture",
        "access_mode",
        "budget",
        "treatment_cell",
        "counterbalance_profile",
    ]
    with args.assignments_csv.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=assignment_fields)
        writer.writeheader()
        writer.writerows(asdict(row) for row in assignments)

    with args.unassigned_csv.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["individual_id", "colony_id"])
        writer.writerows(unassigned)

    result = {
        "schema": "adaptive-gain-routeability-roster-randomization-v1",
        "roster_sha256": hashlib.sha256(
            args.roster_csv.read_bytes()
        ).hexdigest(),
        "assignments_sha256": hashlib.sha256(
            args.assignments_csv.read_bytes()
        ).hexdigest(),
        "unassigned_sha256": hashlib.sha256(
            args.unassigned_csv.read_bytes()
        ).hexdigest(),
        "eligibility_rule": eligibility_rule,
        "randomization_seed": args.seed,
        "receipt": asdict(receipt),
        "focal_treatment_or_outcome_columns_used": False,
        "claim_ceiling": (
            "Complete within-colony treatment randomization only; "
            "eligibility must already be architecture-neutral."
        ),
    }
    args.receipt_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
