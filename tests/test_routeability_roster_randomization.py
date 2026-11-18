import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

from adaptive_gain.routeability_roster_randomization import (
    randomize_roster_complete_colony_blocks,
)

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "examples" / "randomize_routeability_roster.py"


def _roster(colonies=4, per_colony=60):
    return [
        (f"c{colony}_i{index:03d}", f"c{colony}")
        for colony in range(1, colonies + 1)
        for index in range(1, per_colony + 1)
    ]


def test_complete_colony_blocks_balance_all_twelve_cells_and_profiles():
    assignments, unassigned, receipt = (
        randomize_roster_complete_colony_blocks(
            _roster(),
            individuals_per_cell=20,
            seed=20260927,
        )
    )

    assert len(assignments) == 240
    assert unassigned == ()
    assert receipt.complete_block_count == 20
    assert dict(receipt.assigned_blocks_by_colony) == {
        "c1": 5,
        "c2": 5,
        "c3": 5,
        "c4": 5,
    }
    assert set(dict(receipt.treatment_cell_counts).values()) == {20}
    assert receipt.complete_blocks_valid
    assert receipt.counterbalance_profiles_valid

    by_block = defaultdict(list)
    by_cell_profile = defaultdict(Counter)
    for row in assignments:
        by_block[row.complete_block_id].append(row)
        by_cell_profile[row.treatment_cell][
            row.counterbalance_profile
        ] += 1

    assert len(by_block) == 20
    for rows in by_block.values():
        assert len(rows) == 12
        assert len({row.treatment_cell for row in rows}) == 12
        assert len({row.colony_id for row in rows}) == 1

    for counts in by_cell_profile.values():
        assert counts == {
            "cb0": 5,
            "cb1": 5,
            "cb2": 5,
            "cb3": 5,
        }


def test_roster_randomization_is_seed_deterministic_and_leaves_extras_explicit():
    roster = _roster(per_colony=61)
    a, unassigned_a, _ = randomize_roster_complete_colony_blocks(
        roster,
        individuals_per_cell=20,
        seed=17,
    )
    b, unassigned_b, _ = randomize_roster_complete_colony_blocks(
        roster,
        individuals_per_cell=20,
        seed=17,
    )
    c, _, _ = randomize_roster_complete_colony_blocks(
        roster,
        individuals_per_cell=20,
        seed=18,
    )
    assert a == b
    assert unassigned_a == unassigned_b
    assert a != c
    assert len(unassigned_a) == 4


def test_roster_randomization_rejects_unbalanced_or_insufficient_designs():
    with pytest.raises(ValueError, match="multiple of four"):
        randomize_roster_complete_colony_blocks(
            _roster(),
            individuals_per_cell=18,
            seed=1,
        )

    with pytest.raises(ValueError, match="insufficient complete"):
        randomize_roster_complete_colony_blocks(
            _roster(colonies=2, per_colony=12),
            individuals_per_cell=4,
            seed=1,
        )

    duplicate = [("i1", "c1"), ("i1", "c2")] + _roster(
        colonies=1, per_colony=48
    )
    with pytest.raises(ValueError, match="duplicate individual_id"):
        randomize_roster_complete_colony_blocks(
            duplicate,
            individuals_per_cell=4,
            seed=1,
        )


def test_roster_exporter_records_hash_and_rejects_outcome_columns(tmp_path):
    roster_path = tmp_path / "roster.csv"
    assignments_path = tmp_path / "assignments.csv"
    unassigned_path = tmp_path / "unassigned.csv"
    receipt_path = tmp_path / "receipt.json"

    with roster_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["individual_id", "colony_id"])
        writer.writerows(_roster(colonies=4, per_colony=12))

    completed = subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            str(roster_path),
            str(assignments_path),
            str(unassigned_path),
            str(receipt_path),
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
    assert completed.returncode == 0, completed.stderr

    result = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert len(result["roster_sha256"]) == 64
    assert len(result["assignments_sha256"]) == 64
    assert len(result["unassigned_sha256"]) == 64
    assert result["focal_treatment_or_outcome_columns_used"] is False
    assert result["receipt"]["assigned_individual_count"] == 48
    assert result["receipt"]["complete_blocks_valid"] is True

    with assignments_path.open(newline="", encoding="utf-8") as handle:
        assignments = list(csv.DictReader(handle))
    assert len(assignments) == 48

    bad_roster = tmp_path / "bad_roster.csv"
    with bad_roster.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["individual_id", "colony_id", "training_accuracy"]
        )
        writer.writerow(["i1", "c1", "0.9"])

    completed = subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            str(bad_roster),
            str(assignments_path),
            str(unassigned_path),
            str(receipt_path),
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
    assert completed.returncode != 0
    assert "forbidden treatment/outcome columns" in completed.stderr
