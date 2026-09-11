from __future__ import annotations

from fractions import Fraction

import pytest

from adaptive_gain.routing_stationary_nonidentifiability import (
    canonical_q2_mutation_bias_contradiction,
    gain_path_certificate_for_target_stationary_distribution,
    gain_path_support_is_exact,
    neutral_measure_for_target_stationary_distribution,
    stationary_nonidentifiability_receipt,
)
from adaptive_gain.routing_reversible_certificate import (
    selected_detailed_balance_holds,
    selected_layer_distribution_from_tilt,
    selected_stationary_distribution,
    shortest_support_distance_to_gain,
    validate_reversible_mutation_certificate,
)


def test_arbitrary_positive_rational_targets_are_constructed_exactly() -> None:
    cases = (
        ((Fraction(1, 3), Fraction(2, 3)), Fraction(3, 2)),
        ((Fraction(1, 6), Fraction(1, 3), Fraction(1, 2)), Fraction(2, 1)),
        ((Fraction(1, 10), Fraction(2, 10), Fraction(3, 10), Fraction(4, 10)), Fraction(5, 2)),
    )
    for target, theta in cases:
        cert = gain_path_certificate_for_target_stationary_distribution(target, theta)
        validate_reversible_mutation_certificate(cert)
        assert gain_path_support_is_exact(cert) is True
        assert selected_layer_distribution_from_tilt(cert, theta) == target
        assert selected_stationary_distribution(cert, 2, theta) == target
        assert selected_detailed_balance_holds(cert, 2, theta) is True
        assert shortest_support_distance_to_gain(cert, len(target) - 1) == len(target) - 1


def test_neutral_measure_exactly_cancels_declared_selection_tilt() -> None:
    target = (Fraction(1, 10), Fraction(3, 10), Fraction(6, 10))
    theta = Fraction(3, 1)
    mu = neutral_measure_for_target_stationary_distribution(target, theta)
    raw = tuple(mu[r] * theta**r for r in range(3))
    z = sum(raw, Fraction(0, 1))
    assert tuple(value / z for value in raw) == target


def test_fixed_path_support_can_generate_opposite_stationary_phase_conclusions() -> None:
    witness = canonical_q2_mutation_bias_contradiction()
    assert witness.theta == 2
    assert witness.full_favored_distribution == (
        Fraction(1, 10), Fraction(1, 5), Fraction(7, 10)
    )
    assert witness.full_disfavored_distribution == (
        Fraction(7, 10), Fraction(1, 5), Fraction(1, 10)
    )
    assert witness.full_favored_mass == Fraction(7, 10) > Fraction(1, 2)
    assert witness.full_disfavored_mass == Fraction(1, 10)
    assert witness.shortest_full_phase_distance_both == 2

    favored = gain_path_certificate_for_target_stationary_distribution(
        witness.full_favored_distribution, witness.theta
    )
    disfavored = gain_path_certificate_for_target_stationary_distribution(
        witness.full_disfavored_distribution, witness.theta
    )
    assert favored.gains == disfavored.gains == (0, 1, 2)
    assert gain_path_support_is_exact(favored) is True
    assert gain_path_support_is_exact(disfavored) is True
    assert shortest_support_distance_to_gain(favored, 2) == 2
    assert shortest_support_distance_to_gain(disfavored, 2) == 2


def test_receipt_freezes_q_theta_support_and_exact_target() -> None:
    target = (Fraction(2, 10), Fraction(3, 10), Fraction(5, 10))
    receipt = stationary_nonidentifiability_receipt(target, Fraction(2, 1))
    assert receipt.required_gap == 2
    assert receipt.theta == 2
    assert receipt.target_distribution == target
    assert sum(receipt.neutral_measure, Fraction(0, 1)) == 1
    assert receipt.shortest_full_phase_distance == 2
    assert receipt.support_is_local_gain_path is True
    assert receipt.exact_selected_stationary_verified is True


def test_edge_scale_changes_rates_but_not_neutral_or_selected_stationary_law() -> None:
    target = (Fraction(1, 5), Fraction(1, 5), Fraction(3, 5))
    theta = Fraction(2, 1)
    slow = gain_path_certificate_for_target_stationary_distribution(
        target, theta, edge_scale=Fraction(1, 4)
    )
    fast = gain_path_certificate_for_target_stationary_distribution(
        target, theta, edge_scale=Fraction(3, 4)
    )
    assert slow.neutral_measure == fast.neutral_measure
    assert slow.proposal != fast.proposal
    assert selected_stationary_distribution(slow, 2, theta) == target
    assert selected_stationary_distribution(fast, 2, theta) == target


def test_validation_rejects_zero_mass_bad_normalization_or_small_tilt() -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        gain_path_certificate_for_target_stationary_distribution(
            (Fraction(1, 2), Fraction(1, 2), Fraction(0, 1)), 2
        )
    with pytest.raises(ValueError, match="sum exactly to one"):
        gain_path_certificate_for_target_stationary_distribution(
            (Fraction(1, 2), Fraction(1, 4)), 2
        )
    with pytest.raises(ValueError, match="at least one"):
        gain_path_certificate_for_target_stationary_distribution(
            (Fraction(1, 2), Fraction(1, 2)), Fraction(1, 2)
        )
    with pytest.raises(ValueError, match=r"\(0,1\]"):
        gain_path_certificate_for_target_stationary_distribution(
            (Fraction(1, 2), Fraction(1, 2)), 2, edge_scale=0
        )
