import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = (
    ROOT
    / "validation"
    / "villavicencio_latent_opportunity_decomposition_gate_v1.json"
)


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_latent_decomposition_keeps_four_frozen_models():
    models = _gate()["models_per_transition"]
    assert set(models) == {
        "base",
        "detection_only",
        "state_only",
        "state_plus_detection",
    }


def test_latent_decomposition_state_rule_is_predeclared():
    rule = _gate()["model_comparison"]
    assert "AIC at least 2 lower" in rule["state_evidence_rule"]
    assert "beta_gain > 0" in rule["state_evidence_rule"]
    assert "beta_loss < 0" in rule["state_evidence_rule"]
    assert "at least five of six" in rule["cross_transition_promotion"]


def test_latent_decomposition_detection_competitor_is_explicit():
    rule = _gate()["model_comparison"]["detection_evidence_rule"]
    assert "detection_only" in rule
    assert "beta_detection > 0" in rule


def test_latent_decomposition_cannot_use_pooled_rescue():
    forbidden = _gate()["interpretation"]["forbidden"]
    assert "overriding a failed five-of-six state rule with pooled significance" in forbidden
    ceiling = _gate()["claim_ceiling"].lower()
    assert "detection-only" in ceiling
    assert "rewiring" in ceiling
