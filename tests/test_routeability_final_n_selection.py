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
    return [
        {
            "scenario_id": "n8_a",
            "robustness_id": "a",
            "individuals_per_cell": 8,
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
            "fit_success_fraction": 1.00,
            "h1_directional_rejection_fraction": 0.91,
            "h2_hierarchical_pass_fraction": 0.88,
            "expected_h1_delta_b2": 0.12,
            "expected_h2_localization": 0.10,
            "sesoi_provenance": "practical_decision_threshold",
        },
    ]


def _rule():
    return FinalNRule(
        minimum_fit_success_fraction=0.95,
        minimum_h1_directional_rejection_fraction=0.80,
        minimum_h2_hierarchical_pass_fraction=0.80,
        minimum_scenarios_per_n=2,
        counterbalance_multiple=4,
    )


def test_final_n_selector_chooses_smallest_n_passing_every_scenario(tmp_path):
    surface = tmp_path / "surface.csv"
    _write_surface(surface, _rows())

    receipt = select_final_individuals_per_cell(surface, _rule())

    assert receipt.selected_individuals_per_cell == 12
    assert receipt.total_randomized_individuals == 144
    assert receipt.evaluated_n_values == (8, 12, 16)

    by_n = {
        row.individuals_per_cell: row
        for row in receipt.candidate_receipts
    }
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
    with pytest.raises(ValueError, match="robustness scenarios"):
        select_final_individuals_per_cell(surface, _rule())

    no_pass = _rows()
    for row in no_pass:
        row["h2_hierarchical_pass_fraction"] = 0.5
    _write_surface(surface, no_pass)
    with pytest.raises(ValueError, match="no evaluated individuals-per-cell"):
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

    with pytest.raises(ValueError, match="same frozen H1/H2 SESOI"):
        select_final_individuals_per_cell(surface, _rule())
