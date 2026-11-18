import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = (
    ROOT
    / "validation"
    / "villavicencio_two_season_detection_gate_v1.json"
)


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_detection_gate_keeps_six_transition_core():
    data = _gate()
    assert data["primary_scope"] == "strict_dated_core_2008_2010"
    assert len(data["transitions"]) == 6


def test_detection_gate_is_fail_closed():
    data = _gate()
    rule = data["promotion_rule"]
    assert "at least five of six" in rule
    assert "Do not fit or interpret" in rule


def test_detection_gate_requires_optimizer_and_curvature_checks():
    gate = _gate()["identifiability_gate"]
    assert gate["optimizer_converged"] is True
    assert gate["multi_start_nll_range_max"] == 0.000001
    assert gate["hessian_positive_definite"] is True
    assert gate["finite_logit_standard_errors"] is True
    assert "0.01" in gate["detection_probability_interior"]


def test_detection_gate_blocks_rewiring_overclaim():
    ceiling = _gate()["claim_ceiling"].lower()
    assert "identifiability" in ceiling
    assert "rewiring" in ceiling
