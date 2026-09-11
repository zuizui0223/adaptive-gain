from __future__ import annotations

from fractions import Fraction

import pytest

from adaptive_gain.routing_mutation_bias_nonidentifiability import (
    fixed_support_nonidentifiability_receipt,
    neutral_measure_for_target_selected_distribution,
    normalize_positive_distribution,
    reversible_path_certificate_for_target_distribution,
)
from adaptive_gain.routing_reversible_certificate import (
    selected_detailed_balance_holds,
    selected_layer_distribution_from_tilt,
    selected_stationary_distribution,
    shortest_support_distance_to_gain,
)


def test_arbitrary_positive_target_is_reproduced_exactly_on_same_gain_path() -> None:
    cases = (
        ((1, 2, 5), 2),
        ((3, 1, 4, 7), Fraction(3, 2)),
        ((2, 9), Fraction(5, 3)),
    )
    for raw_target, theta in cases:
        target = normalize_positive_distribution(raw_target)
        cert = reversible_path_certificate_for_target_distribution(raw_target, theta)
        assert selected_layer_distribution_from_tilt(cert, theta) == target
        q = len(target) - 1
        assert tuple(shortest_support_distance_to_gain(cert, r) for r in range(q + 1)) == tuple(
            range(q + 1)
        )


def test_neutral_measure_is_exact_inverse_fitness_tilt_reweighting() -> None:
    target = (Fraction(1, 10), Fraction(1, 5), Fraction(7, 10))
    theta = Fraction(2, 1)
    mu = neutral_measure_for_target_selected_distribution(target, theta)
    ratios = tuple(mu[r] * theta**r / target[r] for r in range(len(target)))
    assert len(set(ratios)) == 1
    assert sum(mu, Fraction(0, 1)) == 1


def test_same_q_theta_and_path_support_can_reverse_full_phase_conclusion() -> None:
    # Same gains {0,1,2}, same theta=2, same path support 0<->1<->2.
    majority_full = (Fraction(1, 10), Fraction(1, 10), Fraction(4, 5))
    minority_full = (Fraction(9, 20), Fraction(9, 20), Fraction(1, 10))
    receipt = fixed_support_nonidentifiability_receipt(majority_full, minority_full, 2)
    assert receipt.required_gap == 2
    assert receipt.theta == 2
    assert receipt.support_distances_a == (0, 1, 2)
    assert receipt.support_distances_b == (0, 1, 2)
    assert receipt.full_mass_a == Fraction(4, 5)
    assert receipt.full_mass_b == Fraction(1, 10)
    assert receipt.neutral_measure_a != receipt.neutral_measure_b


def test_constructed_theta_two_certificate_matches_full_origin_fixation_chain() -> None:
    # N=2, fitness_step=2 gives theta=2 exactly.
    target = (Fraction(1, 10), Fraction(1, 10), Fraction(4, 5))
    cert = reversible_path_certificate_for_target_distribution(target, 2)
    pi = selected_stationary_distribution(cert, population_size=2, fitness_step=2)
    assert pi == target
    assert selected_detailed_balance_holds(cert, population_size=2, fitness_step=2)


def test_edge_scale_changes_rates_but_not_selected_stationary_law_or_support_distance() -> None:
    target = (Fraction(2, 7), Fraction(1, 7), Fraction(4, 7))
    slow = reversible_path_certificate_for_target_distribution(target, 2, edge_scale=Fraction(1, 8))
    fast = reversible_path_certificate_for_target_distribution(target, 2, edge_scale=Fraction(1, 2))
    assert slow.proposal != fast.proposal
    assert slow.neutral_measure == fast.neutral_measure
    assert selected_layer_distribution_from_tilt(slow, 2) == target
    assert selected_layer_distribution_from_tilt(fast, 2) == target
    assert shortest_support_distance_to_gain(slow, 2) == 2
    assert shortest_support_distance_to_gain(fast, 2) == 2


def test_validation() -> None:
    with pytest.raises(ValueError, match="at least two"):
        normalize_positive_distribution((1,))
    with pytest.raises(ValueError, match="strictly positive"):
        normalize_positive_distribution((1, 0))
    with pytest.raises(ValueError, match="theta must be positive"):
        neutral_measure_for_target_selected_distribution((1, 1), 0)
    with pytest.raises(ValueError, match="edge_scale"):
        reversible_path_certificate_for_target_distribution((1, 1), 2, edge_scale=0)
    with pytest.raises(ValueError, match="same gain levels"):
        fixed_support_nonidentifiability_receipt((1, 1), (1, 1, 1), 2)
