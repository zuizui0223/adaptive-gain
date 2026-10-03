from math import isclose

import pytest

from adaptive_gain.temporal_routing import (
    FIXED_QUERY_PAIRS,
    adaptive_two_query_accuracy,
    best_fixed_two_query_accuracy,
    evolutionary_net_gain,
    fixed_pair_accuracy,
    optimal_adaptive_two_query_accuracy,
    optimal_routing_rule,
    temporal_adaptive_gain,
    temporal_autocorrelation,
    temporal_routing_receipt,
)


@pytest.mark.parametrize("rho", [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
def test_every_fixed_two_query_bundle_has_three_quarters_accuracy(rho):
    assert all(isclose(fixed_pair_accuracy(rho, pair), 0.75) for pair in FIXED_QUERY_PAIRS)
    assert isclose(best_fixed_two_query_accuracy(rho), 0.75)


@pytest.mark.parametrize("rho", [0.0, 0.2, 0.5, 0.8, 1.0])
def test_adaptive_formulas(rho):
    assert isclose(adaptive_two_query_accuracy(rho, "persistence"), (1.0 + rho) / 2.0)
    assert isclose(adaptive_two_query_accuracy(rho, "alternation"), 1.0 - rho / 2.0)
    expected_optimum = 0.75 + abs(2.0 * rho - 1.0) / 4.0
    assert isclose(optimal_adaptive_two_query_accuracy(rho), expected_optimum)
    assert isclose(temporal_adaptive_gain(rho), abs(2.0 * rho - 1.0) / 4.0)


def test_gain_vanishes_exactly_at_temporal_independence():
    assert temporal_routing_receipt(0.5).optimal_rule == "indifferent"
    assert isclose(temporal_adaptive_gain(0.5), 0.0)
    assert temporal_adaptive_gain(0.49) > 0.0
    assert temporal_adaptive_gain(0.51) > 0.0


def test_predictable_persistence_and_predictable_alternation_are_symmetric():
    assert optimal_routing_rule(0.9) == "persistence"
    assert optimal_routing_rule(0.1) == "alternation"
    assert isclose(temporal_adaptive_gain(0.9), temporal_adaptive_gain(0.1))
    assert isclose(optimal_adaptive_two_query_accuracy(0.0), 1.0)
    assert isclose(optimal_adaptive_two_query_accuracy(1.0), 1.0)


def test_signed_autocorrelation_controls_gain_magnitude():
    for rho in (0.1, 0.4, 0.5, 0.6, 0.9):
        phi = temporal_autocorrelation(rho)
        assert isclose(temporal_adaptive_gain(rho), abs(phi) / 4.0)


def test_evolutionary_control_cost_creates_selection_threshold():
    assert isclose(evolutionary_net_gain(0.9, accuracy_value=2.0, routing_control_cost=0.3), 0.1)
    assert evolutionary_net_gain(0.9, accuracy_value=2.0, routing_control_cost=0.41) < 0.0


@pytest.mark.parametrize("rho", [-0.01, 1.01])
def test_rho_outside_probability_range_is_rejected(rho):
    with pytest.raises(ValueError):
        temporal_routing_receipt(rho)
