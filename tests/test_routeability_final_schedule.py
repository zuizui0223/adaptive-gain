import csv
import json
import random
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

import pytest

from adaptive_gain.routeability_final_schedule import (
    compile_assigned_routeability_schedule,
    final_schedule_audit,
)
from adaptive_gain.routeability_roster_randomization import (
    randomize_roster_complete_colony_blocks,
)

ROOT = Path(__file__).resolve().parents[1]
RANDOMIZER = ROOT / "examples" / "randomize_routeability_roster.py"
COMPILER = ROOT / "examples" / "compile_routeability_final_schedule.py"


def _roster(colonies=4, per_colony=12):
    return [
        (f"c{colony}_i{index:03d}", f"c{colony}")
        for colony in range(1, colonies + 1)
        for index in range(1, per_colony + 1)
    ]


def test_compiled_schedule_preserves_actual_assignments_and_balance():
    assignments, _, _ = randomize_roster_complete_colony_blocks(
        _roster(),
        individuals_per_cell=4,
        seed=20260927,
    )
    trials = compile_assigned_routeability_schedule(
        assignments,
        blocks_per_individual=2,
        global_seed=123456,
    )
    audit = final_schedule_audit(assignments, trials)

    assert audit["assignment_individual_count"] == 48
    assert audit["scheduled_individual_count"] == 48
    assert audit["trial_count"] == 48 * 8
    assert audit["individual_identity_match"]
    assert audit["assignment_fidelity"]
    assert audit["individual_state_balance"]
    assert audit["individual_terminal_position_balance"]
    assert audit["individual_order_balance"]

    assignment_by_id = {row.individual_id: row for row in assignments}
    for trial in trials:
        assignment = assignment_by_id[trial.individual_id]
        assert trial.colony_id == assignment.colony_id
        assert trial.complete_block_id == assignment.complete_block_id
        assert trial.treatment_cell == assignment.treatment_cell
        assert trial.counterbalance_profile == assignment.counterbalance_profile


def test_compiled_schedule_is_invariant_to_assignment_csv_order():
    assignments, _, _ = randomize_roster_complete_colony_blocks(
        _roster(),
        individuals_per_cell=4,
        seed=17,
    )
    shuffled = list(assignments)
    random.Random(999).shuffle(shuffled)

    a = compile_assigned_routeability_schedule(
        assignments,
        blocks_per_individual=2,
        global_seed=888,
    )
    b = compile_assigned_routeability_schedule(
        shuffled,
        blocks_per_individual=2,
        global_seed=888,
    )
    c = compile_assigned_routeability_schedule(
        assignments,
        blocks_per_individual=2,
        global_seed=889,
    )

    assert a == b
    assert a != c


def test_compiler_rejects_assignment_treatment_or_profile_mismatch():
    assignments, _, _ = randomize_roster_complete_colony_blocks(
        _roster(),
        individuals_per_cell=4,
        seed=5,
    )
    first = assignments[0]

    bad_cell = list(assignments)
    bad_cell[0] = type(first)(
        **{
            **asdict(first),
            "treatment_cell": "routeable__fixed__B99",
        }
    )
    with pytest.raises(ValueError, match="treatment_cell mismatch"):
        compile_assigned_routeability_schedule(
            bad_cell,
            blocks_per_individual=1,
            global_seed=1,
        )

    bad_profile = list(assignments)
    bad_profile[0] = type(first)(
        **{
            **asdict(first),
            "counterbalance_profile": "unknown",
        }
    )
    with pytest.raises(ValueError, match="unknown counterbalance profile"):
        compile_assigned_routeability_schedule(
            bad_profile,
            blocks_per_individual=1,
            global_seed=1,
        )


def test_randomizer_to_final_schedule_export_chain_is_hash_locked(tmp_path):
    roster = tmp_path / "roster.csv"
    assignments = tmp_path / "assignments.csv"
    unassigned = tmp_path / "unassigned.csv"
    randomization_receipt = tmp_path / "randomization.json"
    schedule = tmp_path / "schedule.csv"
    schedule_receipt = tmp_path / "schedule.json"

    with roster.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["individual_id", "colony_id"])
        writer.writerows(_roster())

    randomized = subprocess.run(
        [
            sys.executable,
            str(RANDOMIZER),
            str(roster),
            str(assignments),
            str(unassigned),
            str(randomization_receipt),
            "--individuals-per-cell",
            "4",
            "--seed",
            "20260927",
            "--eligibility-rule",
            "architecture-neutral apparatus engagement completed",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert randomized.returncode == 0, randomized.stderr

    randomization = json.loads(
        randomization_receipt.read_text(encoding="utf-8")
    )
    assert len(randomization["assignments_sha256"]) == 64
    assert len(randomization["unassigned_sha256"]) == 64

    compiled = subprocess.run(
        [
            sys.executable,
            str(COMPILER),
            str(assignments),
            str(randomization_receipt),
            str(schedule),
            str(schedule_receipt),
            "--blocks-per-individual",
            "2",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert compiled.returncode == 0, compiled.stderr

    receipt = json.loads(schedule_receipt.read_text(encoding="utf-8"))
    assert receipt["assignments_sha256"] == randomization["assignments_sha256"]
    assert len(receipt["schedule_sha256"]) == 64
    assert receipt["audit"]["assignment_fidelity"] is True
    assert receipt["audit"]["trial_count"] == 48 * 8

    with schedule.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 48 * 8
    assert {"individual_id", "colony_id", "complete_block_id", "revealed_cues"} <= set(
        rows[0]
    )


def test_final_schedule_compiler_rejects_tampered_assignment_csv(tmp_path):
    roster = tmp_path / "roster.csv"
    assignments = tmp_path / "assignments.csv"
    unassigned = tmp_path / "unassigned.csv"
    randomization_receipt = tmp_path / "randomization.json"
    schedule = tmp_path / "schedule.csv"
    schedule_receipt = tmp_path / "schedule.json"

    with roster.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["individual_id", "colony_id"])
        writer.writerows(_roster())

    completed = subprocess.run(
        [
            sys.executable,
            str(RANDOMIZER),
            str(roster),
            str(assignments),
            str(unassigned),
            str(randomization_receipt),
            "--individuals-per-cell",
            "4",
            "--seed",
            "1",
            "--eligibility-rule",
            "architecture-neutral engagement",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    assignments.write_text(
        assignments.read_text(encoding="utf-8") + "\n",
        encoding="utf-8",
    )

    compiled = subprocess.run(
        [
            sys.executable,
            str(COMPILER),
            str(assignments),
            str(randomization_receipt),
            str(schedule),
            str(schedule_receipt),
            "--blocks-per-individual",
            "1",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert compiled.returncode != 0
    assert "SHA-256 does not match" in compiled.stderr
