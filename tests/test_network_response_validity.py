from adaptive_gain.network_response_validity import (
    NetworkResponseEvidence,
    ResponseValidity,
    assess_network_response_validity,
)


def _base(**changes):
    values = dict(
        response_reconstructable=True,
        response_nondegenerate=True,
        effort_semantics_resolved=True,
        binary_detection_audited=True,
        binary_detection_material=False,
        true_absence_independently_supported=True,
        effort_standardized_response_available=True,
        repeated_detection_model_available=True,
        repeated_detection_identifiable=True,
        state_effect_reproducible=True,
        observation_model_robust=True,
        independent_decision_layer=False,
    )
    values.update(changes)
    return NetworkResponseEvidence(**values)


def test_unresolved_effort_stops_at_feasibility():
    result = assess_network_response_validity(
        _base(effort_semantics_resolved=False)
    )
    assert result.response_validity == ResponseValidity.FEASIBILITY_ONLY
    assert result.routeability_bridge_eligible is False


def test_material_detection_without_robust_state_stays_observed_turnover():
    result = assess_network_response_validity(
        _base(
            binary_detection_material=True,
            true_absence_independently_supported=False,
            state_effect_reproducible=False,
            observation_model_robust=False,
        )
    )
    assert (
        result.response_validity
        == ResponseValidity.OBSERVED_LINK_TURNOVER_ONLY
    )
    assert result.routeability_bridge_eligible is False
    assert "observed-link turnover" in result.claim_ceiling


def test_detection_defensible_state_still_needs_decision_layer():
    result = assess_network_response_validity(
        _base(independent_decision_layer=False)
    )
    assert (
        result.response_validity
        == ResponseValidity.DETECTION_DEFENSIBLE_STATE
    )
    assert result.routeability_bridge_eligible is False


def test_routeability_bridge_requires_both_response_and_decision_layer():
    result = assess_network_response_validity(
        _base(independent_decision_layer=True)
    )
    assert (
        result.response_validity
        == ResponseValidity.DETECTION_DEFENSIBLE_STATE
    )
    assert result.routeability_bridge_eligible is True


def test_villavicencio_current_evidence_fails_closed():
    evidence = NetworkResponseEvidence(
        response_reconstructable=True,
        response_nondegenerate=True,
        effort_semantics_resolved=True,
        binary_detection_audited=True,
        binary_detection_material=True,
        true_absence_independently_supported=False,
        effort_standardized_response_available=True,
        repeated_detection_model_available=True,
        repeated_detection_identifiable=True,
        state_effect_reproducible=False,
        observation_model_robust=False,
        independent_decision_layer=False,
    )
    result = assess_network_response_validity(evidence)
    assert (
        result.response_validity
        == ResponseValidity.OBSERVED_LINK_TURNOVER_ONLY
    )
    assert result.routeability_bridge_eligible is False
    assert any("state-side effect" in reason for reason in result.reasons)
    assert any("observation model" in reason for reason in result.reasons)


def test_unaudited_binary_detection_fails_closed():
    result = assess_network_response_validity(
        _base(
            binary_detection_audited=False,
            binary_detection_material=False,
            true_absence_independently_supported=False,
        )
    )
    assert (
        result.response_validity
        == ResponseValidity.OBSERVED_LINK_TURNOVER_ONLY
    )
    assert result.routeability_bridge_eligible is False
    assert any("has not been audited" in reason for reason in result.reasons)
