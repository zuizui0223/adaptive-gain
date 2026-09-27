import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from adaptive_gain.routeability_experiment_power import RouteabilitySESoi
from adaptive_gain.routeability_operating_characteristics import (
    build_probability_scenario_from_sesoi,
    scenario_rows,
)

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "examples" / "build_routeability_glmm_simulation_scenarios.py"


def _sesoi():
    return RouteabilitySESoi(
        h1_probability_interaction=0.12,
        h2_probability_localization=0.10,
        provenance="practical_decision_threshold",
    )


def test_probability_surface_realizes_h1_and_h2_exactly():
    surface = build_probability_scenario_from_sesoi(
        _sesoi(),
        bypass_fixed_by_budget={1: 0.55, 2: 0.60, 3: 0.70},
        bypass_access_effect_by_budget={1: 0.01, 2: 0.02, 3: 0.01},
        routeable_fixed_effect_by_budget={1: -0.01, 2: -0.02, 3: -0.01},
    )
    p = surface.cell_probabilities
    deltas = {}
    for budget in (1, 2, 3):
        deltas[budget] = (
            p[("routeable", "contingent", budget)]
            - p[("routeable", "fixed", budget)]
            - p[("bypass_control", "contingent", budget)]
            + p[("bypass_control", "fixed", budget)]
        )
    assert deltas[2] == pytest.approx(0.12)
    assert deltas[1] == pytest.approx(0.02)
    assert deltas[3] == pytest.approx(0.02)
    assert deltas[2] - 0.5 * (deltas[1] + deltas[3]) == pytest.approx(0.10)
    assert len(scenario_rows(surface)) == 12


def test_probability_surface_rejects_cells_outside_probability_range():
    with pytest.raises(ValueError):
        build_probability_scenario_from_sesoi(
            RouteabilitySESoi(0.4, 0.4, "practical_decision_threshold"),
            bypass_fixed_by_budget={1: 0.9, 2: 0.9, 3: 0.9},
            bypass_access_effect_by_budget={1: 0.05, 2: 0.05, 3: 0.05},
            routeable_fixed_effect_by_budget={1: 0.05, 2: 0.05, 3: 0.05},
        )


def test_scenario_exporter_emits_validated_flattened_cells(tmp_path):
    config = tmp_path / "config.json"
    output = tmp_path / "scenarios.csv"
    config.write_text(
        json.dumps(
            {
                "scenarios": [
                    {
                        "scenario_id": "pilot_grid_1",
                        "sesoi": {
                            "h1_probability_interaction": 0.12,
                            "h2_probability_localization": 0.10,
                            "provenance": "external_biological_criterion",
                        },
                        "baseline": {
                            "bypass_fixed_by_budget": {"1": 0.50, "2": 0.60, "3": 0.70},
                            "bypass_access_effect_by_budget": {"1": 0.01, "2": 0.02, "3": 0.01},
                            "routeable_fixed_effect_by_budget": {"1": 0.00, "2": -0.02, "3": 0.00},
                        },
                        "simulation": {
                            "simulations": 100,
                            "individuals_per_cell": 20,
                            "trials_per_individual": 12,
                            "colony_count": 4,
                            "individual_sd_logit": 0.8,
                            "colony_sd_logit": 0.3,
                            "dropout_fraction": 0.1,
                            "timeout_fraction": 0.05,
                            "alpha_two_sided": 0.05,
                            "seed": 20260927,
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [sys.executable, str(EXPORTER), str(config), str(output)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    row = rows[0]
    assert row["scenario_id"] == "pilot_grid_1"
    assert float(row["expected_h1_delta_b2"]) == pytest.approx(0.12)
    assert float(row["expected_h2_localization"]) == pytest.approx(0.10)
    assert int(row["individuals_per_cell"]) == 20
    for column in ("p_KF_B1", "p_KC_B1", "p_RF_B1", "p_RC_B1", "p_KF_B3", "p_RC_B3"):
        assert 0 < float(row[column]) < 1


def test_scenario_exporter_rejects_theory_ceiling_as_effect_provenance(tmp_path):
    config = tmp_path / "config.json"
    output = tmp_path / "scenarios.csv"
    config.write_text(
        json.dumps(
            {
                "scenarios": [
                    {
                        "scenario_id": "bad",
                        "sesoi": {
                            "h1_probability_interaction": 0.25,
                            "h2_probability_localization": 0.25,
                            "provenance": "theoretical_information_ceiling",
                        },
                        "baseline": {
                            "bypass_fixed_by_budget": {"1": 0.4, "2": 0.4, "3": 0.4},
                            "bypass_access_effect_by_budget": {"1": 0, "2": 0, "3": 0},
                            "routeable_fixed_effect_by_budget": {"1": 0, "2": 0, "3": 0},
                        },
                        "simulation": {
                            "simulations": 10,
                            "individuals_per_cell": 4,
                            "trials_per_individual": 4,
                            "colony_count": 1,
                            "individual_sd_logit": 0,
                            "colony_sd_logit": 0,
                            "dropout_fraction": 0,
                            "timeout_fraction": 0,
                            "seed": 1,
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [sys.executable, str(EXPORTER), str(config), str(output)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "forbidden SESOI provenance" in completed.stderr
