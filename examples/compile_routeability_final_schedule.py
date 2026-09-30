"""Compile randomized routeability roster assignments into final trial schedule."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from adaptive_gain.routeability_final_schedule import (
    compile_assigned_routeability_schedule,
    final_schedule_audit,
)
from adaptive_gain.routeability_roster_randomization import (
    RouteabilityRosterAssignment,
)


def _read_assignments(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {
            "individual_id",
            "colony_id",
            "complete_block_id",
            "architecture",
            "access_mode",
            "budget",
            "treatment_cell",
            "counterbalance_profile",
        }
        if not required <= set(reader.fieldnames or ()):
            raise ValueError(
                f"assignment CSV must contain {sorted(required)}"
            )
        return [
            RouteabilityRosterAssignment(
                individual_id=row["individual_id"],
                colony_id=row["colony_id"],
                complete_block_id=row["complete_block_id"],
                architecture=row["architecture"],
                access_mode=row["access_mode"],
                budget=int(row["budget"]),
                treatment_cell=row["treatment_cell"],
                counterbalance_profile=row["counterbalance_profile"],
            )
            for row in reader
        ]


def _derived_trial_seed(randomization_seed: int) -> int:
    digest = hashlib.sha256(
        f"routeability-final-trial-schedule-v1|{randomization_seed}".encode("utf-8")
    ).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("assignments_csv", type=Path)
    parser.add_argument("randomization_receipt_json", type=Path)
    parser.add_argument("schedule_csv", type=Path)
    parser.add_argument("schedule_receipt_json", type=Path)
    parser.add_argument("--blocks-per-individual", type=int, required=True)
    args = parser.parse_args()

    randomization = json.loads(
        args.randomization_receipt_json.read_text(encoding="utf-8")
    )
    if randomization.get("schema") != (
        "adaptive-gain-routeability-roster-randomization-v1"
    ):
        raise ValueError("unexpected randomization receipt schema")

    observed_assignment_sha = hashlib.sha256(
        args.assignments_csv.read_bytes()
    ).hexdigest()
    expected_assignment_sha = randomization.get("assignments_sha256")
    if expected_assignment_sha != observed_assignment_sha:
        raise ValueError(
            "assignment CSV SHA-256 does not match randomization receipt"
        )

    randomization_seed = int(randomization["randomization_seed"])
    trial_schedule_seed = _derived_trial_seed(randomization_seed)
    assignments = _read_assignments(args.assignments_csv)
    trials = compile_assigned_routeability_schedule(
        assignments,
        blocks_per_individual=args.blocks_per_individual,
        global_seed=trial_schedule_seed,
    )
    audit = final_schedule_audit(assignments, trials)

    fields = list(asdict(trials[0]))
    with args.schedule_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for trial in trials:
            row = asdict(trial)
            row["revealed_cues"] = ">".join(trial.revealed_cues)
            writer.writerow(row)

    schedule_sha = hashlib.sha256(
        args.schedule_csv.read_bytes()
    ).hexdigest()

    result = {
        "schema": "adaptive-gain-routeability-final-trial-schedule-v1",
        "assignments_sha256": observed_assignment_sha,
        "randomization_receipt_sha256": hashlib.sha256(
            args.randomization_receipt_json.read_bytes()
        ).hexdigest(),
        "randomization_seed": randomization_seed,
        "trial_schedule_seed_derivation": (
            "sha256('routeability-final-trial-schedule-v1|<randomization_seed>')"
        ),
        "trial_schedule_seed": trial_schedule_seed,
        "blocks_per_individual": args.blocks_per_individual,
        "schedule_sha256": schedule_sha,
        "audit": audit,
        "claim_ceiling": (
            "This artifact compiles the frozen randomized roster into a deterministic "
            "trial schedule. It does not replace preregistration, pilot, ethics, or "
            "final power gates."
        ),
    }
    args.schedule_receipt_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
