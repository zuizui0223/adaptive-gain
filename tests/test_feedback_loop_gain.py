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


def test_exact_loop_gain_stability_interval():
    # For every interior equilibrium with positive reward contrast, the Jury
    # inequalities reduce to 0<L<1.
    cases = (
        (-0.5, 0.2, True),
        (-3.0, 0.2, True),
        (-4.0, 0.2, False),
        (0.5, 0.2, False),
    )
    for eta, phi, expected_stable in cases:
        eq = interior_feedback_equilibrium(
            low_reward=-0.5,
            high_reward=0.5,
            q_base=0.5,
            feedback_strength=eta,
            community_memory=phi,
        )
        assert eq.status == "interior_equilibrium"
        L = loop_gain_from_equilibrium(eq)
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
    # eta=-1/2, lambda=1 gives L_k=(k-1)/8 at p*=1/2.
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

        # Midpoint control cost centers state rewards and q*=p*=1/2.
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
    # Delta_g(d)=2^d-(d+1), eta=-1/2, lambda=1.
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
