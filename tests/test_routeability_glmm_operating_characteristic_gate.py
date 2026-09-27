import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "routeability_glmm_operating_characteristic_gate_v1.json"


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_glmm_oc_gate_keeps_final_n_unfrozen_until_real_inputs_exist():
    data = _gate()
    assert data["status"] == "simulator_code_ready_pilot_inputs_pending"
    assert data["final_N_promotion_rule"]["final_N_status"] == "not frozen"
    required = data["final_N_promotion_rule"]["required"]
    assert any("procedural pilot nuisance receipt" in item for item in required)
    assert any("external H1/H2 SESOI" in item for item in required)
    assert any("multiple plausible nuisance/baseline scenarios" in item for item in required)


def test_glmm_oc_gate_counts_fit_failures_against_operating_characteristics():
    data = _gate()
    sim = data["simulation"]
    assert "fit failures count as H1/H2 failures" in sim["fit_failure_policy"]
    assert "singularity is reported" in sim["singular_fit_policy"]
    assert "delta-method fixed-effect uncertainty" in sim["contrast_estimation"]


def test_glmm_oc_gate_blocks_theory_ceiling_and_favorable_scenario_selection():
    data = _gate()
    forbidden_effects = data["inputs"]["sesoi"]["forbidden"]
    assert "theoretical 0.25 information ceiling as behavioral effect size" in forbidden_effects
    assert "opened focal pilot H1/H2 estimate" in forbidden_effects
    assert "most favorable scenario" in data["final_N_promotion_rule"]["forbidden"]


def test_glmm_oc_gate_separates_ci_fixture_from_scientific_power_result():
    data = _gate()
    assert "arbitrary synthetic nuisance/effect values" in data["software_fixture_boundary"]
    assert "never scientific planning results" in data["software_fixture_boundary"]
    assert "does not justify a biological N" in data["claim_ceiling"]


def test_glmm_oc_gate_uses_population_average_probability_contrasts():
    data = _gate()
    sim = data["simulation"]
    assert "population-average primary-success probabilities" in sim["cell_probability_semantics"]
    assert "integrating over the prespecified combined individual+colony" in sim[
        "random_effect_calibration"
    ]
    assert "population-average H1/H2" in sim["contrast_estimation"]
    assert "conditional on fitted variance components" in sim["contrast_estimation"]
    assert "do not add a second delta-method term" in sim["variance_component_uncertainty"]
