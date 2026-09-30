import math

from adaptive_gain.detection_effort_identity import (
    finite_binary_turnover_balance,
    finite_binary_turnover_timeseries,
    finite_weighted_turnover_balance,
    binary_transition_conservation,
    observed_gain_log_odds_vs_loss,
    period_detection_probability,
    persistent_observed_transition_probabilities,
    persistent_transition_from_census_effort,
)


def test_period_detection_probability_matches_at_least_once_formula():
    assert period_detection_probability(0.2, 0) == 0.0
    assert math.isclose(
        period_detection_probability(0.2, 3),
        1 - 0.8**3,
        rel_tol=0,
        abs_tol=1e-15,
    )


def test_persistent_transition_probabilities_sum_to_one():
    result = persistent_observed_transition_probabilities(0.3, 0.7)
    total = sum(
        result[key]
        for key in (
            "gain",
            "loss",
            "stable_present",
            "stable_absent",
        )
    )
    assert math.isclose(total, 1.0, rel_tol=0, abs_tol=1e-15)


def test_gain_minus_loss_identity_is_exact():
    for q1, q2 in ((0.1, 0.8), (0.8, 0.1), (0.4, 0.4), (0.0, 1.0)):
        result = persistent_observed_transition_probabilities(q1, q2)
        assert math.isclose(
            result["gain_minus_loss"],
            result["q_current_minus_q_previous"],
            rel_tol=0,
            abs_tol=1e-15,
        )


def test_more_censuses_bias_persistent_link_toward_observed_gain():
    result = persistent_transition_from_census_effort(
        p_previous=0.1,
        n_previous=3,
        p_current=0.1,
        n_current=12,
    )
    assert result["q_current"] > result["q_previous"]
    assert result["gain"] > result["loss"]
    assert result["gain_minus_loss"] > 0


def test_fewer_censuses_bias_persistent_link_toward_observed_loss():
    result = persistent_transition_from_census_effort(
        p_previous=0.1,
        n_previous=12,
        p_current=0.1,
        n_current=3,
    )
    assert result["q_current"] < result["q_previous"]
    assert result["gain"] < result["loss"]
    assert result["gain_minus_loss"] < 0


def test_equal_period_detection_makes_gain_loss_symmetric():
    result = persistent_observed_transition_probabilities(0.6, 0.6)
    assert math.isclose(result["gain"], result["loss"])
    assert math.isclose(
        observed_gain_log_odds_vs_loss(0.6, 0.6),
        0.0,
        abs_tol=1e-15,
    )


def test_gain_loss_odds_ratio_equals_detectability_odds_ratio():
    for q1, q2 in ((0.2, 0.7), (0.7, 0.2), (0.4, 0.6)):
        result = persistent_observed_transition_probabilities(q1, q2)
        observed_ratio = result["gain"] / result["loss"]
        detectability_odds_ratio = (
            (q2 / (1 - q2)) / (q1 / (1 - q1))
        )
        assert math.isclose(
            observed_ratio,
            detectability_odds_ratio,
            rel_tol=1e-14,
            abs_tol=0.0,
        )
        assert math.isclose(
            math.exp(observed_gain_log_odds_vs_loss(q1, q2)),
            detectability_odds_ratio,
            rel_tol=1e-14,
            abs_tol=0.0,
        )


def test_binary_flow_identity_needs_no_independence():
    # Deliberately non-product joint table.
    result = binary_transition_conservation(
        p00=0.10,
        p01=0.20,
        p10=0.05,
        p11=0.65,
    )
    assert math.isclose(
        result["gain_minus_loss"],
        0.15,
        rel_tol=0,
        abs_tol=1e-15,
    )
    assert math.isclose(
        result["current_minus_previous_presence"],
        0.15,
        rel_tol=0,
        abs_tol=1e-15,
    )
    assert math.isclose(result["previous_presence"], 0.70)
    assert math.isclose(result["current_presence"], 0.85)


def test_finite_network_gain_loss_balance_equals_edge_count_change():
    previous = [0, 0, 1, 1, 1, 0, 1]
    current = [1, 0, 1, 0, 1, 1, 0]
    result = finite_binary_turnover_balance(previous, current)

    assert result["gains"] == 2
    assert result["losses"] == 2
    assert result["gain_minus_loss"] == 0
    assert result["previous_edges"] == 4
    assert result["current_edges"] == 4
    assert result["edge_count_change"] == 0


def test_finite_network_gain_surplus_is_exactly_edge_count_increase():
    previous = [0, 0, 0, 1, 1]
    current = [1, 1, 0, 1, 0]
    result = finite_binary_turnover_balance(previous, current)

    assert result["gains"] == 2
    assert result["losses"] == 1
    assert result["gain_minus_loss"] == 1
    assert result["edge_count_change"] == 1


def test_binary_timeseries_balance_telescopes_to_endpoint_change():
    states = [
        [0, 0, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 1, 0, 1],
    ]
    result = finite_binary_turnover_timeseries(states)

    assert result["time_points"] == 4
    assert result["cumulative_gains"] == 3
    assert result["cumulative_losses"] == 3
    assert result["cumulative_gain_minus_loss"] == 0
    assert result["endpoint_edge_change"] == 0


def test_weighted_turnover_balance_equals_total_weight_change():
    result = finite_weighted_turnover_balance(
        [0.0, 2.0, 1.5, 4.0],
        [1.0, 1.0, 3.0, 2.5],
    )

    assert math.isclose(result["strengthening"], 2.5)
    assert math.isclose(result["weakening"], 2.5)
    assert math.isclose(result["strengthening_minus_weakening"], 0.0)
    assert math.isclose(result["total_weight_change"], 0.0)


def test_weighted_turnover_rejects_negative_or_nonfinite_weights():
    import pytest

    with pytest.raises(ValueError):
        finite_weighted_turnover_balance([0.0, -1.0], [0.0, 1.0])
    with pytest.raises(ValueError):
        finite_weighted_turnover_balance([0.0, math.inf], [0.0, 1.0])
