import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "routeability_procedural_pilot_gate_v1.json"
DOC = ROOT / "manuscript" / "ROUTEABILITY_PROCEDURAL_PILOT_V1.md"


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_pilot_gate_forbids_focal_effect_estimation():
    data = _gate()
    assert data["status"] == "prospective_nuisance_pilot_frozen_no_focal_effect_estimation"
    forbidden = data["pilot_B"]["forbidden"]
    assert "architecture-specific accuracy" in forbidden
    assert "architecture x access contrast" in forbidden
    assert "B=2 data" in forbidden
    assert "H1 or H2 estimates" in forbidden


def test_pilot_gate_freezes_response_window_without_treatment_tuning():
    data = _gate()
    rule = data["pilot_A"]["response_window_rule"]
    assert "smallest prespecified candidate window" in rule
    assert "at least 95%" in rule
    assert "predeclared upper bound" in rule


def test_pilot_gate_does_not_set_final_n_from_theory_or_focal_pilot():
    data = _gate()
    policy = data["sample_size_policy"]
    assert policy["theoretical_ceiling_as_effect_size"] is False
    assert policy["pilot_focal_effect_as_power_target"] is False
    assert policy["final_N_status"] == "not frozen"
    assert "operating-characteristic surface" in policy["next_product"]


def test_pilot_document_keeps_operational_claim_ceiling():
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "It must **not** estimate the confirmatory architecture × access interaction",
        "not used as the power target",
        "It is not an empirical test of environmental routeability",
    ):
        assert phrase in text
