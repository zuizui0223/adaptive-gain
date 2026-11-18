import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_detection_overdispersion_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_overdispersion_stress_fires_frozen_model_sensitivity_rule():
    data = _result()
    assert data["status"] == "latent_transition_inference_model_sensitive"
    rule = data["frozen_sensitivity_rule"]
    assert rule["beta_binomial_preferred_transition_count"] == 6
    assert rule["state_transition_boundary_count"] == 6
    assert rule["model_sensitivity_rule_met"] is True


def test_beta_binomial_is_materially_preferred_in_every_transition():
    transitions = _result()["transition_results"]
    assert len(transitions) == 6
    for row in transitions.values():
        assert row["beta_binomial_preferred"] is True
        assert row["delta_aic_beta_minus_binomial"] < -10
        assert row["state_transition_boundary"] is True


def test_overdispersion_result_blocks_detection_corrected_rewiring():
    data = _result()
    assert "true latent gain or loss rates" in data["not_established"]
    ceiling = data["claim_ceiling"].lower()
    assert "6/6" in ceiling
    assert "model-dependent" in ceiling
    assert "identified ecological response" in ceiling
