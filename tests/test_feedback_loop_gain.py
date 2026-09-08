from math import isfinite

import pytest

from adaptive_gain.endogenous_community_feedback import (
    interior_feedback_equilibrium,
    structural_feedback_equilibrium,
)
from adaptive_gain.extremal_routing_family import extremal_routing_task
from adaptive_gain.feedback_loop_gain import (
    binary_family_centered_loop_gain,
    centered_loop_gain_from_gap_contrast,
    critical_slowing_approximation,
    critical_slowing_scaled_ratio,
    damped_phase_spectral_radius,
    damping_time_from_loop_gain,
    k_branch_centered_loop_gain,
    local_damping_time,
    local_oscillation_period,
    local_spectral_radius,
    loop_gain_from_equilibrium,
    oscillation_threshold,
    structural_gap_contrast,
    structural_loop_gain,
    summarize_loop_gain,
    transient_regime,
    unit_circle_instability_period,
    unit_circle_period_long_memory_asymptotic,
)
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def _repo_native_equilibrium(*, phi: float, eta: float):
    return structural_feedback_equilibrium(
        routing_bypass_control(),
        payoff_routing_task(),
        lambda_cost=1.0,
        control_cost=0.5,
        q_base=0.5,
        feedback_strength=eta,
        community_memory=phi,
    )


def test_repo_native_gap_contrast_and_centered_loop_gain():
    low = routing_bypass_control()
    high = payoff_routing_task()
    assert structural_gap_contrast(low, high) == 1
    assert structural_loop_gain(
        low,
        high,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    ) == pytest.approx(0.125)
    assert centered_loop_gain_from_gap_contrast(
        1,
        lambda_cost=1.0,
        feedback_strength=-0.5,
    ) == pytest.approx(0.125)


def test_exact_loop_gain_stability_interval_with_globally_feasible_feedback():
    # Keep q_target(p)=0.5+eta*(p-0.5) inside [0,1] for every p by using
    # |eta|<=1.  Vary the symmetric reward contrast instead to span the exact
    # loop-gain stability boundary L=-eta*Delta_s/4 at p*=1/2.
    cases = (
        (-0.5, 0.5, -0.5, 0.2, True, 0.125),
        (-1.5, 1.5, -1.0, 0.2, True, 0.75),
        (-2.0, 2.0, -1.0, 0.2, False, 1.0),
        (-0.5, 0.5, 0.5, 0.2, False, -0.125),
    )
    for low, high, eta, phi, expected_stable, expected_L in cases:
        eq = interior_feedback_equilibrium(
            low_reward=low,
            high_reward=high,
            q_base=0.5,
            feedback_strength=eta,
            community_memory=phi,
        )
        assert eq.status == "interior_equilibrium"
        L = loop_gain_from_equilibrium(eq)
        assert L == pytest.approx(expected_L)
        assert eq.locally_stable == expected_stable
        assert expected_stable == (0.0 < L < 1.0)


def test_memory_changes_transient_regime_without_changing_loop_gain_or_stability():
    low_memory = _repo_native_equilibrium(phi=0.2, eta=-0.5)
    high_memory = _repo_native_equilibrium(phi=0.8, eta=-0.5)

    assert low_memory.locally_stable
    assert high_memory.locally_stable
    assert loop_gain_from_equilibrium(low_memory) == pytest.approx(0.125)
    assert loop_gain_from_equilibrium(high_memory) == pytest.approx(0.125)

    assert oscillation_threshold(0.2) == pytest.approx(0.2)
    assert oscillation_threshold(0.8) == pytest.approx(0.05)
    assert transient_regime(low_memory) == "stable_nonoscillatory"
    assert transient_regime(high_memory) == "stable_damped_oscillation"


def test_complex_pair_has_finite_damping_time_and_period():
    eq = _repo_native_equilibrium(phi=0.8, eta=-0.5)
    assert transient_regime(eq) == "stable_damped_oscillation"
    rho = local_spectral_radius(eq)
    tau = local_damping_time(eq)
    period = local_oscillation_period(eq)
    assert 0.0 < rho < 1.0
    assert isfinite(tau) and tau > 0.0
    assert period is not None and isfinite(period) and period > 2.0


def test_damped_loop_gain_closed_form_matches_equilibrium_eigenvalues():
    # Delta_s=4 and p*=1/2 make L=-eta.  eta=-0.99 therefore gives L=0.99
    # while keeping q_target globally feasible.
    eq = interior_feedback_equilibrium(
        low_reward=-2.0,
        high_reward=2.0,
        q_base=0.5,
        feedback_strength=-0.99,
        community_memory=0.8,
    )
    assert eq.status == "interior_equilibrium"
    assert transient_regime(eq) == "stable_damped_oscillation"
    L = loop_gain_from_equilibrium(eq)
    assert L == pytest.approx(0.99)
    assert damped_phase_spectral_radius(L, 0.8) == pytest.approx(
        local_spectral_radius(eq)
    )
    assert damping_time_from_loop_gain(L, 0.8) == pytest.approx(
        local_damping_time(eq)
    )


def test_critical_slowing_scaling_as_loop_gain_approaches_unit_circle():
    for phi in (0.2, 0.8, 0.95):
        previous = 0.0
        for L in (0.9, 0.99, 0.999):
            if L <= oscillation_threshold(phi):
                continue
            tau = damping_time_from_loop_gain(L, phi)
            approximation = critical_slowing_approximation(L, phi)
            assert tau > previous
            previous = tau
            assert tau / approximation == pytest.approx(1.0, rel=6e-2)
            if L >= 0.99:
                assert critical_slowing_scaled_ratio(L, phi) == pytest.approx(
                    1.0, rel=1e-2
                )


def test_critical_slowing_scaling_as_community_memory_approaches_one():
    L = 0.5
    previous = 0.0
    for phi in (0.8, 0.9, 0.99, 0.999):
        tau = damping_time_from_loop_gain(L, phi)
        assert tau > previous
        previous = tau
    assert critical_slowing_scaled_ratio(L, 0.99) == pytest.approx(1.0, rel=5e-3)
    assert critical_slowing_scaled_ratio(L, 0.999) == pytest.approx(1.0, rel=1e-3)


def test_strong_feedback_boundary_is_oscillatory_unit_circle_crossing():
    assert unit_circle_instability_period(0.0) == pytest.approx(6.0)
    assert unit_circle_instability_period(0.8) > unit_circle_instability_period(0.2)
    assert unit_circle_instability_period(0.95) > 20.0

    for phi in (0.0, 0.2, 0.8):
        eq = interior_feedback_equilibrium(
            low_reward=-2.0,
            high_reward=2.0,
            q_base=0.5,
            feedback_strength=-1.0,
            community_memory=phi,
        )
        assert loop_gain_from_equilibrium(eq) == pytest.approx(1.0)
        assert eq.eigenvalues is not None
        assert abs(eq.eigenvalues[0]) == pytest.approx(1.0)
        assert abs(eq.eigenvalues[1]) == pytest.approx(1.0)
        assert eq.eigenvalues[0].imag != pytest.approx(0.0)


def test_unit_circle_period_has_long_memory_inverse_square_root_scaling():
    for phi in (0.9, 0.99, 0.999):
        exact = unit_circle_instability_period(phi)
        asymptotic = unit_circle_period_long_memory_asymptotic(phi)
        assert exact / asymptotic == pytest.approx(1.0, rel=5e-3)


def test_positive_feedback_and_strong_negative_feedback_are_distinct_instabilities():
    positive = _repo_native_equilibrium(phi=0.5, eta=0.5)
    assert transient_regime(positive) == "unstable_nonrestoring_feedback"
    assert loop_gain_from_equilibrium(positive) < 0.0

    strong_negative = interior_feedback_equilibrium(
        low_reward=-2.0,
        high_reward=2.0,
        q_base=0.5,
        feedback_strength=-1.0,
        community_memory=0.5,
    )
    assert loop_gain_from_equilibrium(strong_negative) == pytest.approx(1.0)
    assert transient_regime(strong_negative) == "unstable_negative_feedback_overshoot"
    assert not strong_negative.locally_stable


def test_k_branch_family_crosses_nonoscillatory_damped_and_overshoot_regimes():
    phi = 0.5
    assert oscillation_threshold(phi) == pytest.approx(0.125)

    expected = {
        2: "stable_nonoscillatory",
        3: "stable_damped_oscillation",
        8: "stable_damped_oscillation",
        9: "unstable_negative_feedback_overshoot",
    }
    low = routing_bypass_control()
    for k, regime in expected.items():
        high = extremal_routing_task(k)
        gap = structural_gap_contrast(low, high)
        assert gap == k - 1
        L = k_branch_centered_loop_gain(
            k,
            lambda_cost=1.0,
            feedback_strength=-0.5,
        )
        assert L == pytest.approx((k - 1) / 8.0)

        eq = structural_feedback_equilibrium(
            low,
            high,
            lambda_cost=1.0,
            control_cost=(k - 1) / 2.0,
            q_base=0.5,
            feedback_strength=-0.5,
            community_memory=phi,
        )
        assert eq.status == "interior_equilibrium"
        assert eq.phenotype_frequency == pytest.approx(0.5)
        assert eq.high_state_occupancy == pytest.approx(0.5)
        assert loop_gain_from_equilibrium(eq) == pytest.approx(L)
        assert transient_regime(eq) == regime


def test_binary_extremal_family_has_faster_structural_phase_crossing():
    phi = 0.5
    L2 = binary_family_centered_loop_gain(
        2, lambda_cost=1.0, feedback_strength=-0.5
    )
    L3 = binary_family_centered_loop_gain(
        3, lambda_cost=1.0, feedback_strength=-0.5
    )
    L4 = binary_family_centered_loop_gain(
        4, lambda_cost=1.0, feedback_strength=-0.5
    )
    assert L2 == pytest.approx(0.125)
    assert L3 == pytest.approx(0.5)
    assert L4 == pytest.approx(1.375)
    assert L2 <= oscillation_threshold(phi)
    assert oscillation_threshold(phi) < L3 < 1.0
    assert L4 > 1.0


def test_loop_gain_summary_is_self_consistent():
    eq = _repo_native_equilibrium(phi=0.8, eta=-0.5)
    summary = summarize_loop_gain(eq)
    assert summary.loop_gain == pytest.approx(loop_gain_from_equilibrium(eq))
    assert summary.oscillation_threshold == pytest.approx(oscillation_threshold(0.8))
    assert summary.regime == transient_regime(eq)
    assert summary.spectral_radius == pytest.approx(local_spectral_radius(eq))
    assert summary.damping_time == pytest.approx(local_damping_time(eq))
    assert summary.oscillation_period == pytest.approx(local_oscillation_period(eq))


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        oscillation_threshold(1.0)
    with pytest.raises(ValueError):
        unit_circle_instability_period(1.0)
    with pytest.raises(ValueError):
        damped_phase_spectral_radius(0.01, 0.5)
    with pytest.raises(ValueError):
        damping_time_from_loop_gain(1.0, 0.5)
    with pytest.raises(ValueError):
        centered_loop_gain_from_gap_contrast(
            1,
            lambda_cost=-1.0,
            feedback_strength=-0.5,
        )
    with pytest.raises(ValueError):
        binary_family_centered_loop_gain(
            0,
            lambda_cost=1.0,
            feedback_strength=-0.5,
        )
