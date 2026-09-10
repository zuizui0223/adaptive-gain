import math

import pytest

from adaptive_gain.feedback_transient_bounds import (
    damped_period_from_loop_gain,
    largest_stable_integer_gap,
    restoring_gain_per_gap,
    smallest_damped_integer_gap,
    structural_transient_ceiling,
)


def test_integer_gap_envelopes_match_direct_enumeration():
    for gap_upper in range(0, 11):
        for a in (0.05, 0.125, 0.2, 1 / 3, 0.5, 1.0):
            brute_stable = [g for g in range(1, gap_upper + 1) if a * g < 1.0]
            expected_stable = max(brute_stable) if brute_stable else None
            assert largest_stable_integer_gap(gap_upper, a) == expected_stable

            for phi in (0.0, 0.2, 0.5, 0.8):
                threshold = (1.0 - phi) / 4.0
                brute_damped = [
                    g
                    for g in range(1, gap_upper + 1)
                    if threshold < a * g < 1.0
                ]
                expected_damped = min(brute_damped) if brute_damped else None
                assert smallest_damped_integer_gap(gap_upper, a, phi) == expected_damped


def test_payoff_scope_excludes_damped_transients_entirely():
    receipt = structural_transient_ceiling(
        4,
        3,
        2,
        2,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
        community_memory=0.5,
    )
    assert receipt.structural_gap_upper_bound == 1
    assert receipt.gain_per_integer_gap == pytest.approx(0.125)
    assert receipt.maximum_stable_gap == 1
    assert receipt.maximum_stable_loop_gain == pytest.approx(0.125)
    assert receipt.minimum_damped_gap is None
    assert not receipt.damped_phase_structurally_possible
    assert receipt.damping_time_upper_bound is None
    assert receipt.oscillation_period_upper_bound is None


def test_medium_binary_scope_has_finite_damped_time_ceiling():
    receipt = structural_transient_ceiling(
        12,
        12,
        3,
        2,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
        community_memory=0.5,
    )
    assert receipt.structural_gap_upper_bound == 4
    assert receipt.maximum_stable_gap == 4
    assert receipt.maximum_stable_loop_gain == pytest.approx(0.5)
    assert receipt.minimum_damped_gap == 2
    assert receipt.minimum_damped_loop_gain == pytest.approx(0.25)
    assert receipt.damped_phase_structurally_possible
    assert receipt.damping_time_upper_bound == pytest.approx(6.952118993564411)
    assert receipt.oscillation_period_upper_bound == pytest.approx(19.528125814614466)


def test_large_gap_scope_is_capped_by_strict_stability_boundary():
    # With a=1/8, L=1 occurs at integer gap 8 and is not stable.  Even if the
    # structural scope allows larger gaps, the largest stable integer gap is 7.
    assert largest_stable_integer_gap(100, 0.125) == 7
    assert smallest_damped_integer_gap(100, 0.125, 0.5) == 2


def test_frontier_edge_cap_can_remove_all_damped_transients():
    receipt = structural_transient_ceiling(
        12,
        12,
        3,
        2,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
        community_memory=0.5,
        frontier_edge_cap=3,
    )
    assert receipt.structural_gap_upper_bound == 0
    assert receipt.maximum_stable_gap is None
    assert receipt.minimum_damped_gap is None
    assert not receipt.damped_phase_structurally_possible


def test_period_decreases_and_damping_time_increases_across_damped_phase():
    phi = 0.5
    period_low = damped_period_from_loop_gain(0.25, phi)
    period_high = damped_period_from_loop_gain(0.75, phi)
    assert period_low > period_high

    from adaptive_gain.feedback_loop_gain import damping_time_from_loop_gain

    damping_low = damping_time_from_loop_gain(0.25, phi)
    damping_high = damping_time_from_loop_gain(0.75, phi)
    assert damping_low < damping_high


def test_restoring_gain_per_gap_matches_structural_scaling():
    assert restoring_gain_per_gap(
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    ) == pytest.approx(0.125)


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        largest_stable_integer_gap(-1, 0.1)
    with pytest.raises(ValueError):
        largest_stable_integer_gap(3, -0.1)
    with pytest.raises(ValueError):
        restoring_gain_per_gap(
            lambda_cost=1.0,
            feedback_strength=0.5,
            equilibrium_frequency=0.5,
        )
    with pytest.raises(ValueError):
        damped_period_from_loop_gain(0.1, 0.5)


def test_period_formula_is_finite_inside_damped_phase():
    value = damped_period_from_loop_gain(0.5, 0.5)
    assert math.isfinite(value)
    assert value == pytest.approx(12.0)
