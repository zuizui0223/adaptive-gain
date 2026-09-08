from math import isclose

import pytest

from adaptive_gain.noisy_temporal_routing import (
    FIXED_QUERY_PAIRS,
    best_noisy_fixed_two_query_accuracy,
    fixed_accuracy_formula,
    noisy_adaptive_two_query_accuracy,
    noisy_evolutionary_net_gain,
    noisy_fixed_pair_accuracy,
    noisy_gain_formula,
    noisy_temporal_adaptive_gain,
    noisy_temporal_routing_receipt,
    optimal_noisy_adaptive_two_query_accuracy,
    optimal_noisy_routing_rule,
    routing_signal,
    signed_routing_term,
    specialist_signal,
    temporal_signal,
)
from adaptive_gain.temporal_routing import temporal_adaptive_gain


@pytest.mark.parametrize(
    "rho,a,b",
    [
        (0.0, 0.5, 0.5),
        (0.0, 1.0, 1.0),
        (0.2, 0.6, 0.7),
        (0.35, 0.8, 0.9),
        (0.5, 1.0, 1.0),
        (0.65, 0.8, 0.9),
        (0.8, 0.6, 0.7),
        (1.0, 1.0, 1.0),
    ],
)
def test_every_fixed_pair_matches_closed_form(rho, a, b):
    expected = fixed_accuracy_formula(b)
    for pair in FIXED_QUERY_PAIRS:
        assert isclose(noisy_fixed_pair_accuracy(rho, a, b, pair), expected)
    assert isclose(best_noisy_fixed_two_query_accuracy(rho, a, b), expected)


@pytest.mark.parametrize(
    "rho,a,b",
    [
        (0.1, 0.55, 0.6),
        (0.2, 0.8, 0.7),
        (0.4, 0.95, 0.85),
        (0.5, 0.8, 0.9),
        (0.6, 0.95, 0.85),
        (0.8, 0.8, 0.7),
        (0.9, 0.55, 0.6),
    ],
)
def test_adaptive_rules_match_signed_factorization(rho, a, b):
    fixed = fixed_accuracy_formula(b)
    signed = signed_routing_term(rho, a, b)
    assert isclose(
        noisy_adaptive_two_query_accuracy(rho, a, b, "persistence"),
        fixed + signed,
    )
    assert isclose(
        noisy_adaptive_two_query_accuracy(rho, a, b, "alternation"),
        fixed - signed,
    )
    assert isclose(
        optimal_noisy_adaptive_two_query_accuracy(rho, a, b),
        fixed + abs(signed),
    )
    assert isclose(noisy_temporal_adaptive_gain(rho, a, b), abs(signed))
    assert isclose(noisy_gain_formula(rho, a, b), abs(signed))


def test_noiseless_limit_recovers_temporal_theorem():
    for rho in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0):
        assert isclose(noisy_temporal_adaptive_gain(rho, 1.0, 1.0), temporal_adaptive_gain(rho))


@pytest.mark.parametrize(
    "rho,a,b",
    [
        (0.5, 1.0, 1.0),
        (0.9, 0.5, 1.0),
        (0.9, 1.0, 0.5),
        (0.5, 0.5, 0.5),
    ],
)
def test_gain_collapses_when_any_signal_is_at_chance(rho, a, b):
    assert isclose(noisy_gain_formula(rho, a, b), 0.0)
    assert isclose(noisy_temporal_adaptive_gain(rho, a, b), 0.0)
    assert optimal_noisy_routing_rule(rho, a, b) == "indifferent"


def test_rule_tracks_sign_of_temporal_predictability():
    assert optimal_noisy_routing_rule(0.9, 0.8, 0.9) == "persistence"
    assert optimal_noisy_routing_rule(0.1, 0.8, 0.9) == "alternation"
    assert optimal_noisy_routing_rule(0.5, 0.8, 0.9) == "indifferent"


def test_positive_and_negative_predictability_are_symmetric_in_gain():
    assert isclose(noisy_gain_formula(0.9, 0.75, 0.85), noisy_gain_formula(0.1, 0.75, 0.85))


def test_gain_is_monotone_in_routing_reliability_above_chance():
    gains = [noisy_gain_formula(0.9, a, 0.9) for a in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)]
    assert gains == sorted(gains)


def test_gain_is_monotone_in_specialist_reliability_above_chance():
    gains = [noisy_gain_formula(0.9, 0.9, b) for b in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)]
    assert gains == sorted(gains)


def test_signal_helpers_are_chance_centered():
    assert isclose(temporal_signal(0.5), 0.0)
    assert isclose(temporal_signal(1.0), 1.0)
    assert isclose(temporal_signal(0.0), -1.0)
    assert isclose(routing_signal(0.5), 0.0)
    assert isclose(routing_signal(1.0), 1.0)
    assert isclose(specialist_signal(0.5), 0.0)
    assert isclose(specialist_signal(1.0), 1.0)


def test_evolutionary_control_cost_creates_multiplicative_threshold():
    raw = noisy_gain_formula(0.9, 0.8, 0.9)
    assert raw > 0.0
    assert noisy_evolutionary_net_gain(
        0.9, 0.8, 0.9, accuracy_value=2.0, routing_control_cost=2.0 * raw - 0.01
    ) > 0.0
    assert noisy_evolutionary_net_gain(
        0.9, 0.8, 0.9, accuracy_value=2.0, routing_control_cost=2.0 * raw + 0.01
    ) < 0.0


def test_receipt_matches_closed_forms():
    receipt = noisy_temporal_routing_receipt(0.8, 0.75, 0.9)
    assert isclose(receipt.fixed_accuracy, fixed_accuracy_formula(0.9))
    assert isclose(receipt.adaptive_gain, noisy_gain_formula(0.8, 0.75, 0.9))
    assert receipt.optimal_rule == "persistence"


@pytest.mark.parametrize(
    "rho,a,b",
    [
        (-0.01, 0.8, 0.8),
        (1.01, 0.8, 0.8),
        (0.8, 0.49, 0.8),
        (0.8, 1.01, 0.8),
        (0.8, 0.8, 0.49),
        (0.8, 0.8, 1.01),
    ],
)
def test_invalid_probabilities_are_rejected(rho, a, b):
    with pytest.raises(ValueError):
        noisy_temporal_routing_receipt(rho, a, b)


def test_negative_fitness_parameters_are_rejected():
    with pytest.raises(ValueError):
        noisy_evolutionary_net_gain(0.8, 0.8, 0.8, accuracy_value=-1.0)
    with pytest.raises(ValueError):
        noisy_evolutionary_net_gain(0.8, 0.8, 0.8, routing_control_cost=-1.0)
