from __future__ import annotations

from fractions import Fraction

import pytest

from adaptive_gain.routing_rate_scale_nonidentifiability import (
    expected_full_phase_hitting_attempts,
    lazy_scaled_matrix_identity_holds,
    rate_scale_nonidentifiability_receipt,
    selected_transition_matrix,
)
from adaptive_gain.routing_reversible_certificate import selected_stationary_distribution
from adaptive_gain.routing_stationary_nonidentifiability import (
    gain_path_certificate_for_target_stationary_distribution,
)


TARGET_Q2 = (Fraction(1, 10), Fraction(1, 5), Fraction(7, 10))


def test_selected_matrix_is_exact_lazy_rescaling() -> None:
    for eps in (Fraction(1, 2), Fraction(1, 3), Fraction(3, 4)):
        assert lazy_scaled_matrix_identity_holds(TARGET_Q2, 2, eps)
        p_eps = selected_transition_matrix(TARGET_Q2, 2, edge_scale=eps)
        p_one = selected_transition_matrix(TARGET_Q2, 2, edge_scale=1)
        for i in range(len(p_one)):
            for j in range(len(p_one)):
                expected = eps * p_one[i][j] + ((1 - eps) if i == j else 0)
                assert p_eps[i][j] == expected


def test_stationary_distribution_is_invariant_to_absolute_rate_scale() -> None:
    expected = TARGET_Q2
    for eps in (Fraction(1, 1), Fraction(1, 2), Fraction(1, 3), Fraction(1, 10)):
        cert = gain_path_certificate_for_target_stationary_distribution(TARGET_Q2, 2, edge_scale=eps)
        observed = selected_stationary_distribution(cert, population_size=2, fitness_step=2)
        assert observed == expected


def test_canonical_q2_hitting_time_scales_exactly() -> None:
    h1 = expected_full_phase_hitting_attempts(TARGET_Q2, 2, edge_scale=1)
    assert h1 == Fraction(585, 56)
    assert expected_full_phase_hitting_attempts(TARGET_Q2, 2, edge_scale=Fraction(1, 2)) == Fraction(585, 28)
    assert expected_full_phase_hitting_attempts(TARGET_Q2, 2, edge_scale=Fraction(1, 3)) == Fraction(1755, 56)


def test_general_hitting_time_is_inverse_scale_for_small_q() -> None:
    cases = (
        ((Fraction(1, 3), Fraction(2, 3)), 2),
        ((Fraction(1, 10), Fraction(2, 10), Fraction(7, 10)), 2),
        ((Fraction(1, 20), Fraction(3, 20), Fraction(6, 20), Fraction(10, 20)), 3),
    )
    for target, theta in cases:
        baseline = expected_full_phase_hitting_attempts(target, theta, edge_scale=1)
        for eps in (Fraction(1, 2), Fraction(1, 4)):
            scaled = expected_full_phase_hitting_attempts(target, theta, edge_scale=eps)
            assert scaled == baseline / eps


def test_receipt_holds_stationarity_distance_and_timing_separately() -> None:
    receipt = rate_scale_nonidentifiability_receipt(TARGET_Q2, 2, Fraction(1, 3))
    assert receipt.required_gap == 2
    assert receipt.shortest_full_phase_distance == 2
    assert receipt.stationary_distribution == TARGET_Q2
    assert receipt.baseline_expected_attempts == Fraction(585, 56)
    assert receipt.scaled_expected_attempts == Fraction(1755, 56)
    assert receipt.timing_inflation == 3
    assert receipt.lazy_matrix_identity_verified is True


def test_validation() -> None:
    with pytest.raises(ValueError, match="edge_scale"):
        selected_transition_matrix(TARGET_Q2, 2, edge_scale=0)
    with pytest.raises(ValueError, match="edge_scale"):
        selected_transition_matrix(TARGET_Q2, 2, edge_scale=Fraction(3, 2))
