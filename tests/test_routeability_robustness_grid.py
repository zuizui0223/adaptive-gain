import json
import subprocess
import sys
from pathlib import Path

import pytest

from adaptive_gain.routeability_robustness_grid import (
    BASELINE_PROFILE_NAMES,
    NUISANCE_PROFILES,
    balanced_colony_block_counts,
    build_frozen_robustness_scenarios,
)


ROOT = Path(__file__).resolve().parents[1]
GATE = (
    ROOT
    / "validation"
    / "routeability_nuisance_robustness_grid_gate_v1.json"
)
EXPORTER = ROOT / "examples" / "build_routeability_robustness_grid.py"


def _nuisance(**overrides):
    payload = {
        "focal_architecture_access_contrast_opened": False,
        "pooled_success_fraction": 0.78,
        "pooled_timeout_fraction": 0.03,
        "randomized_individual_dropout_fraction": 0.10,
        "trials_per_individual": 8,
        "individual_sd_logit": 0.40,
        "colony_sd_logit": 0.12,
    }
    payload.update(overrides)
    return payload


def test_gate_profile_names_match_code():
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    assert tuple(gate["robustness_policy"]["baseline_profiles"]) == (
        BASELINE_PROFILE_NAMES
    )
    assert gate["robustness_policy"]["nuisance_profiles"] == NUISANCE_PROFILES
    assert gate["robustness_policy"]["sesoi"]["h1"] == 0.10
    assert gate["robustness_policy"]["sesoi"]["h2"] == 0.10


def test_balanced_colony_blocks_are_complete_and_deterministic():
    assert balanced_colony_block_counts(16, 4) == (4, 4, 4, 4)
    assert balanced_colony_block_counts(20, 3) == (7, 7, 6)
    with pytest.raises(ValueError, match="multiple of four"):
        balanced_colony_block_counts(18, 3)
    with pytest.raises(ValueError, match="cannot exceed"):
        balanced_colony_block_counts(8, 9)


def test_robustness_grid_has_same_twelve_ids_at_every_candidate_n():
    scenarios = build_frozen_robustness_scenarios(
        _nuisance(),
        candidate_individuals_per_cell=[4, 8, 12, 16],
        colony_count=4,
        simulations_per_scenario=250,
        seed_base=20260929,
    )
    assert len(scenarios) == 48

    by_n = {}
    for row in scenarios:
        n = row["simulation"]["individuals_per_cell"]
        by_n.setdefault(n, []).append(row)

        assert row["sesoi"] == {
            "h1_probability_interaction": 0.10,
            "h2_probability_localization": 0.10,
            "provenance": "practical_decision_threshold",
        }
        counts = row["simulation"]["colony_block_counts"]
        assert sum(counts) == n
        assert max(counts) - min(counts) <= 1

    assert set(by_n) == {4, 8, 12, 16}
    reference = {row["robustness_id"] for row in by_n[4]}
    assert len(reference) == 12
    for n in (8, 12, 16):
        assert {row["robustness_id"] for row in by_n[n]} == reference


def test_pilot_anchor_and_stress_rules_are_mechanical():
    scenarios = build_frozen_robustness_scenarios(
        _nuisance(),
        candidate_individuals_per_cell=[4],
        colony_count=4,
        simulations_per_scenario=100,
        seed_base=7,
    )
    lookup = {row["robustness_id"]: row for row in scenarios}

    nominal = lookup["pilot_anchored__nominal"]
    assert nominal["baseline"]["bypass_fixed_by_budget"] == {
        "1": pytest.approx(0.58),
        "2": pytest.approx(0.68),
        "3": pytest.approx(0.78),
    }
    assert nominal["simulation"]["individual_sd_logit"] == pytest.approx(0.40)
    assert nominal["simulation"]["colony_sd_logit"] == pytest.approx(0.12)
    assert nominal["simulation"]["dropout_fraction"] == pytest.approx(0.10)
    assert nominal["simulation"]["timeout_fraction"] == pytest.approx(0.03)

    combined = lookup["hard_center__combined_stress"]
    assert combined["simulation"]["individual_sd_logit"] == pytest.approx(0.60)
    assert combined["simulation"]["colony_sd_logit"] == pytest.approx(0.18)
    assert combined["simulation"]["dropout_fraction"] == pytest.approx(0.15)
    assert combined["simulation"]["timeout_fraction"] == pytest.approx(0.08)


def test_grid_starts_at_smallest_colony_feasible_counterbalanced_n():
    scenarios = build_frozen_robustness_scenarios(
        _nuisance(),
        candidate_individuals_per_cell=[8, 12],
        colony_count=6,
        simulations_per_scenario=100,
        seed_base=1,
    )
    assert {
        row["simulation"]["individuals_per_cell"]
        for row in scenarios
    } == {8, 12}
    assert all(
        len(row["simulation"]["colony_block_counts"]) == 6
        for row in scenarios
    )
    assert all(
        min(row["simulation"]["colony_block_counts"]) >= 1
        for row in scenarios
    )


def test_grid_rejects_candidate_n_gaps_or_start_above_four():
    with pytest.raises(ValueError, match="every multiple of four"):
        build_frozen_robustness_scenarios(
            _nuisance(),
            candidate_individuals_per_cell=[8, 12],
            colony_count=4,
            simulations_per_scenario=100,
            seed_base=1,
        )

    with pytest.raises(ValueError, match="every multiple of four"):
        build_frozen_robustness_scenarios(
            _nuisance(),
            candidate_individuals_per_cell=[4, 12],
            colony_count=4,
            simulations_per_scenario=100,
            seed_base=1,
        )


def test_grid_rejects_non_multiple_candidate_n_and_opened_focal_contrast():
    with pytest.raises(ValueError, match="multiple of four"):
        build_frozen_robustness_scenarios(
            _nuisance(),
            candidate_individuals_per_cell=[14],
            colony_count=2,
            simulations_per_scenario=100,
            seed_base=1,
        )


    with pytest.raises(ValueError, match="positive integer"):
        build_frozen_robustness_scenarios(
            _nuisance(),
            candidate_individuals_per_cell=[12.5],
            colony_count=2,
            simulations_per_scenario=100,
            seed_base=1,
        )

    with pytest.raises(ValueError, match="closed focal contrast"):
        build_frozen_robustness_scenarios(
            _nuisance(focal_architecture_access_contrast_opened=True),
            candidate_individuals_per_cell=[4],
            colony_count=4,
            simulations_per_scenario=100,
            seed_base=1,
        )


def test_grid_fails_closed_instead_of_clipping_invalid_pilot_anchor():
    with pytest.raises(ValueError, match="exceeds 1-timeout_fraction"):
        build_frozen_robustness_scenarios(
            _nuisance(
                pooled_success_fraction=0.99,
                pooled_timeout_fraction=0.03,
            ),
            candidate_individuals_per_cell=[4],
            colony_count=4,
            simulations_per_scenario=100,
            seed_base=1,
        )


def test_robustness_exporter_derives_gapless_grid_from_operational_max(tmp_path):
    nuisance_path = tmp_path / "nuisance.json"
    planning_path = tmp_path / "planning.json"
    output_path = tmp_path / "robustness.json"
    nuisance_path.write_text(json.dumps(_nuisance()), encoding="utf-8")
    planning_path.write_text(
        json.dumps(
            {
                "operational_max_individuals_per_cell": 16,
                "colony_count": 4,
                "simulations_per_scenario": 100,
                "seed_base": 20260929,
                "alpha_two_sided": 0.05,
            }
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            str(nuisance_path),
            str(planning_path),
            str(output_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["operational_max_individuals_per_cell"] == 16
    assert result["candidate_individuals_per_cell"] == [4, 8, 12, 16]
    assert result["scenario_count_per_N"] == 12
    assert len(result["scenarios"]) == 48


def test_robustness_exporter_rejects_hand_listed_candidate_n(tmp_path):
    nuisance_path = tmp_path / "nuisance.json"
    planning_path = tmp_path / "planning.json"
    output_path = tmp_path / "robustness.json"
    nuisance_path.write_text(json.dumps(_nuisance()), encoding="utf-8")
    planning_path.write_text(
        json.dumps(
            {
                "candidate_individuals_per_cell": [4, 8, 12],
                "colony_count": 4,
                "simulations_per_scenario": 100,
                "seed_base": 1,
            }
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            str(nuisance_path),
            str(planning_path),
            str(output_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "operational_max_individuals_per_cell" in completed.stderr
