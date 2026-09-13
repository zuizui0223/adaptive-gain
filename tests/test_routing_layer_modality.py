from fractions import Fraction

import pytest

from adaptive_gain.routing_layer_modality import (
    aggregate_layer_weights,
    aggregate_modal_tilt_threshold,
    degeneracy_chain_bound_is_strict,
    distance_layer_degeneracy,
    full_layer_has_stationary_majority,
    full_layer_stationary_mass,
    majority_boundary_polynomial_coefficients,
    minimum_population_size_for_modal_full_layer,
    minimum_population_size_for_stationary_majority,
    minimum_population_size_for_unique_modal_full_layer,
    modal_gain_layers,
    stationary_majority_excess,
    stationary_majority_tilt_bounds,
    threshold_modal_gain_layers,
    weakest_branch_layer_degeneracy,
)
from adaptive_gain.routing_origin_fixation import (
    full_phase_modal_tilt_threshold,
    gain_layer_degeneracy,
    minimum_population_size_for_modal_full_phase,
)


def test_general_layer_count_matches_bruteforce_small_cases() -> None:
    from itertools import product

    for q in range(1, 5):
        for k in range(1, 5):
            states = tuple(product(range(q + 1), repeat=k))
            for r in range(q + 1):
                observed = sum(min(state) == r for state in states)
                assert weakest_branch_layer_degeneracy(q, k, r) == observed


def test_distance_form_matches_layer_form() -> None:
    for q in range(1, 7):
        for k in range(1, 6):
            for s in range(q + 1):
                assert distance_layer_degeneracy(k, s) == weakest_branch_layer_degeneracy(
                    q, k, q - s
                )


def test_global_bound_is_strict_beyond_adjacent_layer_for_k_at_least_two() -> None:
    for k in range(2, 9):
        threshold = aggregate_modal_tilt_threshold(k)
        assert distance_layer_degeneracy(k, 1) == threshold
        for s in range(2, 9):
            assert degeneracy_chain_bound_is_strict(k, s)
            assert distance_layer_degeneracy(k, s) < threshold**s


def test_threshold_trichotomy_for_general_finite_routing_spaces() -> None:
    for q in range(1, 8):
        for k in range(2, 8):
            threshold = aggregate_modal_tilt_threshold(k)
            assert q not in modal_gain_layers(q, k, threshold - 1)
            assert threshold_modal_gain_layers(q, k) == (q - 1, q)
            assert modal_gain_layers(q, k, threshold + 1) == (q,)


def test_k1_boundary_case_has_all_layers_tied_at_threshold() -> None:
    for q in range(1, 8):
        assert aggregate_modal_tilt_threshold(1) == 1
        assert threshold_modal_gain_layers(q, 1) == tuple(range(q + 1))
        assert modal_gain_layers(q, 1, 2) == (q,)


def test_canonical_k_equals_q_plus_one_matches_existing_pr26_helpers() -> None:
    for q in range(1, 9):
        k = q + 1
        assert aggregate_modal_tilt_threshold(k) == full_phase_modal_tilt_threshold(q)
        for r in range(q + 1):
            assert weakest_branch_layer_degeneracy(q, k, r) == gain_layer_degeneracy(q, r)
        assert minimum_population_size_for_modal_full_layer(
            k, 2
        ) == minimum_population_size_for_modal_full_phase(q, 2)


def test_population_threshold_separates_tied_from_unique_modality() -> None:
    # k=2 gives threshold 3. With a=3 and N=2, theta=3 exactly: tied.
    assert minimum_population_size_for_modal_full_layer(2, 3) == 2
    assert minimum_population_size_for_unique_modal_full_layer(2, 3) == 3
    assert modal_gain_layers(4, 2, 3) == (3, 4)
    assert modal_gain_layers(4, 2, 9) == (4,)


def test_twofold_canonical_population_threshold_is_q_plus_two_and_unique() -> None:
    for q in range(1, 10):
        k = q + 1
        assert minimum_population_size_for_modal_full_layer(k, 2) == q + 2
        assert minimum_population_size_for_unique_modal_full_layer(k, 2) == q + 2


def test_full_layer_stationary_mass_matches_normalized_weights() -> None:
    for q in range(1, 6):
        for k in range(1, 6):
            for theta in (1, 2, 3, Fraction(5, 2)):
                weights = aggregate_layer_weights(q, k, theta)
                expected = weights[-1] / sum(weights, Fraction(0, 1))
                assert full_layer_stationary_mass(q, k, theta) == expected


def test_majority_boundary_polynomial_canonical_q2() -> None:
    # q=2,k=3: theta^2 - 7 theta - 19 = 0.
    assert majority_boundary_polynomial_coefficients(2, 3) == (1, -7, -19)
    assert stationary_majority_excess(2, 3, 9) == -1
    assert stationary_majority_excess(2, 3, 10) == 11
    assert full_layer_stationary_mass(2, 3, 9) == Fraction(81, 163)
    assert full_layer_stationary_mass(2, 3, 10) == Fraction(100, 189)
    assert not full_layer_has_stationary_majority(2, 3, 9)
    assert full_layer_has_stationary_majority(2, 3, 10)


def test_majority_boundary_equals_modal_threshold_when_q_is_one() -> None:
    for k in range(1, 9):
        threshold = aggregate_modal_tilt_threshold(k)
        assert stationary_majority_tilt_bounds(1, k) == (threshold, threshold)
        assert full_layer_stationary_mass(1, k, threshold) == Fraction(1, 2)
        assert stationary_majority_excess(1, k, threshold) == 0


def test_majority_boundary_is_strictly_between_T_and_2T_for_q_at_least_two() -> None:
    for q in range(2, 9):
        for k in range(1, 8):
            threshold = aggregate_modal_tilt_threshold(k)
            lower, upper = stationary_majority_tilt_bounds(q, k)
            assert (lower, upper) == (threshold, 2 * threshold)
            assert stationary_majority_excess(q, k, lower) < 0
            assert stationary_majority_excess(q, k, upper) > 0
            assert full_layer_stationary_mass(q, k, lower) < Fraction(1, 2)
            assert full_layer_stationary_mass(q, k, upper) > Fraction(1, 2)


def test_majority_indicator_tracks_excess_sign_exactly() -> None:
    for q in range(1, 6):
        for k in range(1, 6):
            for theta in range(1, 2 * aggregate_modal_tilt_threshold(k) + 2):
                assert full_layer_has_stationary_majority(q, k, theta) == (
                    stationary_majority_excess(q, k, theta) >= 0
                )


def test_canonical_twofold_majority_population_threshold_has_one_step_gap() -> None:
    # q=1 is the two-layer edge case: theta=4 at N=3 already exceeds T=3.
    assert minimum_population_size_for_stationary_majority(1, 2, 2) == 3

    # For q>=2, k=q+1. At N=q+2, theta=2^k=T+1 but the s=2
    # layer still keeps full mass below one half. The next dyadic tilt is enough
    # because theta_1/2 < 2T < 2^(k+1).
    for q in range(2, 10):
        k = q + 1
        assert not full_layer_has_stationary_majority(q, k, 2**k)
        assert full_layer_has_stationary_majority(q, k, 2 ** (k + 1))
        assert minimum_population_size_for_stationary_majority(q, k, 2) == q + 3


def test_neutral_fitness_step_majority_edge_cases() -> None:
    assert minimum_population_size_for_stationary_majority(1, 1, 1) == 2
    assert minimum_population_size_for_stationary_majority(1, 2, 1) is None
    assert minimum_population_size_for_stationary_majority(2, 1, 1) is None


def test_exact_rational_contract_and_validation() -> None:
    with pytest.raises(TypeError, match="float breaks exact rational arithmetic"):
        aggregate_layer_weights(2, 3, 1.5)
    with pytest.raises(TypeError, match="float breaks exact rational arithmetic"):
        stationary_majority_excess(2, 3, 1.5)
    with pytest.raises(ValueError, match="positive integer"):
        aggregate_modal_tilt_threshold(True)
    with pytest.raises(ValueError, match="at least one"):
        minimum_population_size_for_modal_full_layer(3, Fraction(1, 2))
    with pytest.raises(ValueError, match="at least one"):
        minimum_population_size_for_stationary_majority(2, 3, Fraction(1, 2))
