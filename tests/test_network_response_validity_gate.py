import json
from pathlib import Path

from adaptive_gain.network_response_validity import (
    NetworkResponseEvidence,
    ResponseValidity,
    assess_network_response_validity,
)

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "network_response_validity_gate_v1.json"


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_frozen_villavicencio_fixture_matches_classifier():
    data = _gate()["villavicencio_fixture"]
    evidence = NetworkResponseEvidence(
        response_reconstructable=data["response_reconstructable"],
        response_nondegenerate=data["response_nondegenerate"],
        effort_semantics_resolved=data["effort_semantics_resolved"],
        binary_detection_audited=data["binary_detection_audited"],
        binary_detection_material=data["binary_detection_material"],
        binary_state_detection_defensible=data[
            "binary_state_detection_defensible"
        ],
        true_absence_independently_supported=data[
            "true_absence_independently_supported"
        ],
        effort_standardized_response_available=data[
            "effort_standardized_response_available"
        ],
        repeated_detection_model_available=data[
            "repeated_detection_model_available"
        ],
        repeated_detection_identifiable=data[
            "repeated_detection_identifiable"
        ],
        state_effect_reproducible=data["state_effect_reproducible"],
        observation_model_robust=data["observation_model_robust"],
        independent_decision_layer=data["independent_decision_layer"],
    )
    result = assess_network_response_validity(evidence)
    assert result.response_validity.value == data[
        "expected_response_validity"
    ]
    assert result.routeability_bridge_eligible is data[
        "expected_routeability_bridge_eligible"
    ]


def test_gate_requires_response_validity_before_routeability():
    gate = _gate()
    assert "detection_defensible_state" in gate["routeability_bridge_rule"]
    assert "independently measured" in gate["routeability_bridge_rule"]


def test_gate_is_fail_closed_for_detection_sensitive_networks():
    result = assess_network_response_validity(
        NetworkResponseEvidence(
            response_reconstructable=True,
            response_nondegenerate=True,
            effort_semantics_resolved=True,
            binary_detection_audited=True,
            binary_detection_material=True,
            binary_state_detection_defensible=False,
            true_absence_independently_supported=False,
            effort_standardized_response_available=True,
            repeated_detection_model_available=True,
            repeated_detection_identifiable=True,
            state_effect_reproducible=False,
            observation_model_robust=False,
            independent_decision_layer=True,
        )
    )
    assert result.response_validity == ResponseValidity.OBSERVED_LINK_TURNOVER_ONLY
    # Even an independent decision layer cannot rescue an invalid response.
    assert result.routeability_bridge_eligible is False
