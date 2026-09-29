import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from adaptive_gain.routeability_final_n_selection import (
    FinalNRule,
    select_final_individuals_per_cell,
)

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "examples" / "select_routeability_final_n.py"


FIELDS = [
    "scenario_id",
    "robustness_id",
    "individuals_per_cell",
    "simulations",
    "trials_per_individual",
    "colony_count",
    "individual_sd_logit",
    "colony_sd_logit",
    "dropout_fraction",
    "timeout_fraction",
    "alpha_two_sided",
    "p_KF_B1", "p_KC_B1", "p_RF_B1", "p_RC_B1",
    "p_KF_B2", "p_KC_B2", "p_RF_B2", "p_RC_B2",
    "p_KF_B3", "p_KC_B3", "p_RF_B3", "p_RC_B3",
    "fit_success_fraction",
    "h1_directional_rejection_fraction",
    "h2_hierarchical_pass_fraction",
    "expected_h1_delta_b2",
    "expected_h2_localization",
    "sesoi_provenance",
]


def _write_surface(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _rows():
    rows = [
        {
            "scenario_id": "n8_a",
            "robustness_id": "a",
            "individuals_per_cell": 8,
            "simulations": 1000,
            "trials_per_individual": 8,
            "fit_success_fraction": 0.99,
            "h1_directional_rejection_fraction": 0.82,
            "h2_hierarchical_pass_fraction": 0.70,
            "expected_h1_delta_b2": 0.12,
            "expected_h2_localization": 0.10,
            "sesoi_provenance": "practical_decision_threshold",
        },
        {
            "scenario_id": "n8_b",
            "robustness_id": "b",
            "individuals_per_cell": 8,
            "simulations": 1000,
            "trials_per_individual": 8,
            "fit_success_fraction": 0.98,
            "h1_directional_rejection_fraction": 0.81,
            "h2_hierarchical_pass_fraction": 0.79,
            "expected_h1_delta_b2": 0.12,
            "expected_h2_localization": 0.10,
            "sesoi_provenance": "practical_decision_threshold",
        },
        {
            "scenario_id": "n12_a",
            "robustness_id": "a",
            "individuals_per_cell": 12,
            "simulations": 1000,
            "trials_per_individual": 8,
            "fit_success_fraction": 0.99,
            "h1_directional_rejection_fraction": 0.86,
            "h2_hierarchical_pass_fraction": 0.84,
            "expected_h1_delta_b2": 0.12,
            "expected_h2_localization": 0.10,
            "sesoi_provenance": "practical_decision_threshold",
        },
        {
            "scenario_id": "n12_b",
            "robustness_id": "b",
            "individuals_per_cell": 12,
            "simulations": 1000,
            "trials_per_individual": 8,
            "fit_success_fraction": 0.97,
            "h1_directional_rejection_fraction": 0.83,
            "h2_hierarchical_pass_fraction": 0.81,
            "expected_h1_delta_b2": 0.12,
            "expected_h2_localization": 0.10,
            "sesoi_provenance": "practical_decision_threshold",
        },
        {
            "scenario_id": "n16_a",
            "robustness_id": "a",
            "individuals_per_cell": 16,
            "simulations": 1000,
            "trials_per_individual": 8,
            "fit_success_fraction": 1.00,
            "h1_directional_rejection_fraction": 0.92,
            "h2_hierarchical_pass_fraction": 0.90,
            "expected_h1_delta_b2": 0.12,
            "expected_h2_localization": 0.10,
            "sesoi_provenance": "practical_decision_threshold",
        },
        {
            "scenario_id": "n16_b",
            "robustness_id": "b",
            "individuals_per_cell": 16,
            "simulations": 1000,
            "trials_per_individual": 8,
            "fit_success_fraction": 1.00,
            "h1_directional_rejection_fraction": 0.91,
            "h2_hierarchical_pass_fraction": 0.88,
            "expected_h1_delta_b2": 0.12,
            "expected_h2_localization": 0.10,
            "sesoi_provenance": "practical_decision_threshold",
        },
    ]
    rows.extend(
        [
            {
                "scenario_id": "n4_a",
                "robustness_id": "a",
                "individuals_per_cell": 4,
                "simulations": 1000,
                "trials_per_individual": 8,
                "fit_success_fraction": 0.97,
                "h1_directional_rejection_fraction": 0.72,
                "h2_hierarchical_pass_fraction": 0.55,
                "expected_h1_delta_b2": 0.12,
                "expected_h2_localization": 0.10,
                "sesoi_provenance": "practical_decision_threshold",
            },
            {
                "scenario_id": "n4_b",
                "robustness_id": "b",
                "individuals_per_cell": 4,
                "simulations": 1000,
                "trials_per_individual": 8,
                "fit_success_fraction": 0.96,
                "h1_directional_rejection_fraction": 0.70,
                "h2_hierarchical_pass_fraction": 0.50,
                "expected_h1_delta_b2": 0.12,
                "expected_h2_localization": 0.10,
                "sesoi_provenance": "practical_decision_threshold",
            },
        ]
    )


    profiles = {
        "a": {
            "colony_count": 4,
            "individual_sd_logit": 0.5,
            "colony_sd_logit": 0.2,
            "dropout_fraction": 0.10,
            "timeout_fraction": 0.05,
            "alpha_two_sided": 0.05,
            "p_KF_B1": 0.50, "p_KC_B1": 0.51,
            "p_RF_B1": 0.50, "p_RC_B1": 0.53,
            "p_KF_B2": 0.60, "p_KC_B2": 0.62,
            "p_RF_B2": 0.58, "p_RC_B2": 0.72,
            "p_KF_B3": 0.70, "p_KC_B3": 0.71,
            "p_RF_B3": 0.70, "p_RC_B3": 0.73,
        },
        "b": {
            "colony_count": 4,
            "individual_sd_logit": 0.8,
            "colony_sd_logit": 0.3,
            "dropout_fraction": 0.15,
            "timeout_fraction": 0.08,
            "alpha_two_sided": 0.05,
            "p_KF_B1": 0.45, "p_KC_B1": 0.46,
            "p_RF_B1": 0.45, "p_RC_B1": 0.48,
            "p_KF_B2": 0.55, "p_KC_B2": 0.57,
            "p_RF_B2": 0.53, "p_RC_B2": 0.67,
            "p_KF_B3": 0.65, "p_KC_B3": 0.66,
            "p_RF_B3": 0.65, "p_RC_B3": 0.68,
        },
    }
    for row in rows:
        row.update(profiles[row["robustness_id"]])
    return rows


def _rule():
    return FinalNRule(
        minimum_fit_success_fraction=0.95,
        minimum_h1_directional_rejection_fraction=0.80,
        minimum_h2_hierarchical_pass_fraction=0.80,
        minimum_scenarios_per_n=2,
        minimum_simulations_per_scenario=1000,
        counterbalance_multiple=4,
    )


def test_final_n_selector_chooses_smallest_n_passing_every_scenario(tmp_path):
    surface = tmp_path / "surface.csv"
    _write_surface(surface, _rows())

    receipt = select_final_individuals_per_cell(surface, _rule())

    assert receipt.selected_individuals_per_cell == 12
    assert receipt.total_randomized_individuals == 144
    assert receipt.evaluated_n_values == (4, 8, 12, 16)

    by_n = {
        row.individuals_per_cell: row
        for row in receipt.candidate_receipts
    }
    assert by_n[4].passes is False
    assert by_n[8].passes is False
    assert by_n[12].passes is True
    assert by_n[16].passes is True
    assert by_n[8].worst_h2_hierarchical_pass_fraction == 0.70
    assert by_n[12].worst_h2_hierarchical_pass_fraction == 0.81
    assert by_n[12].robustness_ids == ("a", "b")


def test_final_n_selector_requires_all_robustness_scenarios_to_pass(tmp_path):
    surface = tmp_path / "surface.csv"
    rows = _rows()
    rows[3]["h1_directional_rejection_fraction"] = 0.79
    _write_surface(surface, rows)

    receipt = select_final_individuals_per_cell(surface, _rule())
    assert receipt.selected_individuals_per_cell == 16


def test_final_n_selector_rejects_sparse_n_or_no_passing_n(tmp_path):
    surface = tmp_path / "surface.csv"
    sparse = [_rows()[0], *_rows()[2:]]
    _write_surface(surface, sparse)
    with pytest.raises(ValueError, match="exact same robustness_id set"):
        select_final_individuals_per_cell(surface, _rule())

    no_pass = _rows()
    for row in no_pass:
        row["h2_hierarchical_pass_fraction"] = 0.5
    _write_surface(surface, no_pass)
    with pytest.raises(ValueError, match="no evaluated individuals-per-cell"):
        select_final_individuals_per_cell(surface, _rule())


def test_final_n_selector_rejects_missing_smaller_or_intermediate_candidate_n(tmp_path):
    surface = tmp_path / "surface.csv"

    missing_minimum = [
        row for row in _rows()
        if int(row["individuals_per_cell"]) != 4
    ]
    _write_surface(surface, missing_minimum)
    with pytest.raises(ValueError, match="every counterbalanced value"):
        select_final_individuals_per_cell(surface, _rule())

    missing_intermediate = [
        row for row in _rows()
        if int(row["individuals_per_cell"]) != 8
    ]
    _write_surface(surface, missing_intermediate)
    with pytest.raises(ValueError, match="every counterbalanced value"):
        select_final_individuals_per_cell(surface, _rule())


def test_final_n_selector_rejects_unbalanced_n(tmp_path):
    surface = tmp_path / "surface.csv"
    rows = _rows()
    rows[0]["individuals_per_cell"] = 10
    rows[1]["individuals_per_cell"] = 10
    _write_surface(surface, rows)
    with pytest.raises(ValueError, match="not a multiple"):
        select_final_individuals_per_cell(surface, _rule())


def test_final_n_exporter_hashes_surface_and_rule(tmp_path):
    surface = tmp_path / "surface.csv"
    rule = tmp_path / "rule.json"
    output = tmp_path / "receipt.json"
    _write_surface(surface, _rows())
    rule.write_text(
        json.dumps(
            {
                "minimum_fit_success_fraction": 0.95,
                "minimum_h1_directional_rejection_fraction": 0.80,
                "minimum_h2_hierarchical_pass_fraction": 0.80,
                "minimum_scenarios_per_n": 2,
                "minimum_simulations_per_scenario": 1000,
                "counterbalance_multiple": 4,
            }
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            str(surface),
            str(rule),
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["selected_individuals_per_cell"] == 12
    assert receipt["total_randomized_individuals"] == 144
    assert receipt["power_surface_sha256"] == hashlib.sha256(
        surface.read_bytes()
    ).hexdigest()
    assert receipt["rule_sha256"] == hashlib.sha256(
        rule.read_bytes()
    ).hexdigest()
    assert receipt["schema"] == "adaptive-gain-routeability-final-n-selection-v1"


def test_final_n_selector_requires_same_robustness_set_at_every_n(tmp_path):
    surface = tmp_path / "surface.csv"
    rows = _rows()
    rows[3]["robustness_id"] = "c"
    _write_surface(surface, rows)

    with pytest.raises(ValueError, match="exact same robustness_id set"):
        select_final_individuals_per_cell(surface, _rule())


def test_final_n_selector_rejects_effect_drift_across_robustness_surface(tmp_path):
    surface = tmp_path / "surface.csv"
    rows = _rows()
    rows[-1]["expected_h1_delta_b2"] = 0.15
    _write_surface(surface, rows)

    with pytest.raises(ValueError, match="mixes H1/H2 SESOI"):
        select_final_individuals_per_cell(surface, _rule())


def test_final_n_selector_rejects_mixed_sesoi_provenance_or_trial_design(tmp_path):
    surface = tmp_path / "surface.csv"

    mixed_h1 = _rows()
    mixed_h1[-1]["expected_h1_delta_b2"] = 0.20
    _write_surface(surface, mixed_h1)
    with pytest.raises(ValueError, match="mixes H1/H2 SESOI"):
        select_final_individuals_per_cell(surface, _rule())

    mixed_provenance = _rows()
    mixed_provenance[-1]["sesoi_provenance"] = "independent_prior_study"
    _write_surface(surface, mixed_provenance)
    with pytest.raises(ValueError, match="mixes or omits SESOI provenance"):
        select_final_individuals_per_cell(surface, _rule())

    mixed_trials = _rows()
    mixed_trials[-1]["trials_per_individual"] = 12
    _write_surface(surface, mixed_trials)
    with pytest.raises(ValueError, match="one frozen positive trials_per_individual"):
        select_final_individuals_per_cell(surface, _rule())


def test_final_n_selector_rejects_same_label_with_changed_nuisance_surface(tmp_path):
    surface = tmp_path / "surface.csv"
    rows = _rows()
    rows[2]["timeout_fraction"] = 0.20
    _write_surface(surface, rows)

    with pytest.raises(ValueError, match="changes nuisance, baseline"):
        select_final_individuals_per_cell(surface, _rule())


def test_final_n_selector_freezes_monte_carlo_precision(tmp_path):
    surface = tmp_path / "surface.csv"

    mixed = _rows()
    mixed[-1]["simulations"] = 2000
    _write_surface(surface, mixed)
    with pytest.raises(ValueError, match="one frozen simulation count"):
        select_final_individuals_per_cell(surface, _rule())

    too_few = _rows()
    for row in too_few:
        row["simulations"] = 500
    _write_surface(surface, too_few)
    with pytest.raises(ValueError, match="frozen minimum is 1000"):
        select_final_individuals_per_cell(surface, _rule())
