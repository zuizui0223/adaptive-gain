import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_latent_opportunity_decomposition_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_latent_opportunity_state_rule_fails_decisively():
    data = _result()
    frozen = data["frozen_rule_result"]
    assert data["status"] == (
        "latent_opportunity_state_effect_not_general_detection_component_common"
    )
    assert frozen["state_supported_transition_count"] == 1
    assert frozen["required_state_supported_transition_count"] == 5
    assert frozen["general_state_promotion_rule_met"] is False


def test_detection_component_is_more_common_than_state_component():
    frozen = _result()["frozen_rule_result"]
    assert frozen["detection_supported_transition_count"] == 4
    assert (
        frozen["detection_supported_transition_count"]
        > frozen["state_supported_transition_count"]
    )


def test_only_first_transition_has_state_support():
    transitions = _result()["transition_results"]
    supported = [
        transition
        for transition, row in transitions.items()
        if row["state_component_supported"]
    ]
    assert supported == ["2008_early->2008_mid"]


def test_detection_supported_transitions_are_frozen():
    transitions = _result()["transition_results"]
    supported = {
        transition
        for transition, row in transitions.items()
        if row["detection_component_supported"]
    }
    assert supported == {
        "2008_early->2008_mid",
        "2008_mid->2008_late",
        "2010_early->2010_mid",
        "2010_mid->2010_late",
    }


def test_latent_opportunity_result_blocks_rewiring_promotion():
    data = _result()
    assert any(
        "universal current-opportunity rewiring mechanism" in item
        for item in data["not_established"]
    )
    ceiling = data["claim_ceiling"].lower()
    assert "state-side support is 1/6" in ceiling
    assert "detection-side support" in ceiling

def test_stricter_optimizer_sensitivity_only_weakens_support():
    data = _result()["post_result_optimizer_reliability_sensitivity"]
    assert data["strict_state_supported_transition_count"] == 0
    assert data["strict_detection_supported_transition_count"] == 2
    assert "post-result robustness only" in data["role"]

