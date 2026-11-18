import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

from adaptive_gain.routeability_experiment_schedule import (
    build_between_subject_routeability_schedule,
    schedule_balance_audit,
)

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "examples" / "build_routeability_experiment_schedule.py"


def test_schedule_balances_twelve_between_subject_cells():
    trials = build_between_subject_routeability_schedule(
        individuals_per_cell=4,
        blocks_per_individual=2,
        seed=20260927,
    )
    audit = schedule_balance_audit(trials)

    assert audit["treatment_cell_count"] == 12
    assert audit["individual_count"] == 48
    assert audit["trial_count"] == 384
    assert set(audit["cell_sizes"].values()) == {4}
    assert audit["single_cell_per_individual"]
    assert audit["individual_state_balance"]
    assert audit["individual_terminal_position_balance"]
    assert audit["individual_order_balance"]
    assert audit["symbol_profiles_balanced_within_cells"]


def test_each_individual_sees_uniform_states_and_no_permanent_terminal_side():
    trials = build_between_subject_routeability_schedule(
        individuals_per_cell=4,
        blocks_per_individual=3,
        seed=17,
    )
    by_individual = defaultdict(list)
    for trial in trials:
        by_individual[trial.individual_id].append(trial)

    for rows in by_individual.values():
        assert Counter(row.state for row in rows) == {
            "w0": 3, "w1": 3, "w2": 3, "w3": 3
        }
        assert Counter(row.terminal_position_swap for row in rows) == {
            False: 6, True: 6
        }
        assert {row.q_left_position for row in rows} == {"window_A", "window_B"}
        assert {row.q_right_position for row in rows} == {"window_A", "window_B"}


def test_b2_contingent_schedule_uses_frozen_context_routing_rule():
    trials = build_between_subject_routeability_schedule(
        individuals_per_cell=4,
        blocks_per_individual=1,
        seed=3,
    )
    rows = [
        row for row in trials
        if row.budget == 2 and row.access_mode == "contingent"
    ]
    assert rows
    for row in rows:
        assert row.revealed_cues[0] == "q_route"
        expected = "q_right" if row.q_route_logical == 0 else "q_left"
        assert row.revealed_cues[1] == expected


def test_fixed_access_is_state_independent_within_budget():
    trials = build_between_subject_routeability_schedule(
        individuals_per_cell=4,
        blocks_per_individual=2,
        seed=11,
    )
    by_individual = defaultdict(list)
    for row in trials:
        if row.access_mode == "fixed" and row.budget in (1, 2):
            by_individual[row.individual_id].append(row)

    for rows in by_individual.values():
        budget = rows[0].budget
        if budget == 1:
            assert Counter(row.revealed_cues for row in rows) == {
                ("q_left",): 4,
                ("q_right",): 4,
            }
        else:
            assert Counter(row.revealed_cues for row in rows) == {
                ("q_left", "q_right"): 4,
                ("q_right", "q_left"): 4,
            }


def test_b3_access_arms_receive_complete_information():
    trials = build_between_subject_routeability_schedule(
        individuals_per_cell=4,
        blocks_per_individual=1,
        seed=19,
    )
    rows = [row for row in trials if row.budget == 3]
    assert rows
    for row in rows:
        assert set(row.revealed_cues) == {"q_left", "q_route", "q_right"}
        assert row.revealed_cues[0] == "q_route"


def test_schedule_is_deterministic_for_seed_and_rejects_unbalanced_cell_size():
    a = build_between_subject_routeability_schedule(
        individuals_per_cell=4, blocks_per_individual=1, seed=101
    )
    b = build_between_subject_routeability_schedule(
        individuals_per_cell=4, blocks_per_individual=1, seed=101
    )
    c = build_between_subject_routeability_schedule(
        individuals_per_cell=4, blocks_per_individual=1, seed=102
    )
    assert a == b
    assert a != c

    with pytest.raises(ValueError):
        build_between_subject_routeability_schedule(
            individuals_per_cell=6, blocks_per_individual=1, seed=1
        )


def test_schedule_exporter_emits_csv_and_balance_receipt(tmp_path):
    csv_path = tmp_path / "schedule.csv"
    json_path = tmp_path / "receipt.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            str(csv_path),
            str(json_path),
            "--individuals-per-cell",
            "4",
            "--blocks-per-individual",
            "1",
            "--seed",
            "20260927",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    receipt = json.loads(json_path.read_text(encoding="utf-8"))
    assert receipt["audit"]["treatment_cell_count"] == 12
    assert receipt["audit"]["symbol_profiles_balanced_within_cells"]
    assert "not_final_powered_sample_size" in receipt["sample_size_status"]

    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 192
    assert {row["budget"] for row in rows} == {"1", "2", "3"}
