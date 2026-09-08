from math import inf, sqrt

import pytest

from adaptive_gain.community_markov_selection import (
    rms_retention_fraction,
    structural_rewards_from_tasks,
)
from adaptive_gain.community_spectral_timescale import (
    asymptotic_variance_rate,
    directional_crossover_horizon,
    poisson_solution,
    summarize_community_timescale,
    zero_mean_retention_prefactor,
)
from adaptive_gain.directional_retention import (
    asymptotic_directional_crossover_horizon,
    community_switching_to_mean_and_coherence,
)
from adaptive_gain.extremal_routing_family import extremal_routing_task
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def _two_state(a, b, delta=1.0):
    total = a + b
    stationary = (b / total, a / total)
    transition = ((1.0 - a, a), (b, 1.0 - b))
    rewards = (-delta, delta)
    return stationary, transition, rewards


def _three_state_mode_chain():
    return (
        (1 / 3, 1 / 3, 1 / 3),
        (
            (0.7, 0.0, 0.3),
            (0.0, 0.7, 0.3),
            (0.3, 0.3, 0.4),
        ),
    )


def test_two_state_asymptotic_variance_recovers_phi_factor():
    for a, b in ((0.25, 0.25), (0.3, 0.2), (0.7, 0.5)):
        stationary, transition, rewards = _two_state(a, b, delta=0.8)
        m, phi = community_switching_to_mean_and_coherence(a, b)
        expected = (0.8 ** 2) * (1.0 - m * m) * (1.0 + phi) / (1.0 - phi)
        assert asymptotic_variance_rate(stationary, transition, rewards) == pytest.approx(expected)


def test_two_state_crossover_recovers_previous_asymptotic_formula():
    for a, b in ((0.3, 0.2), (0.6, 0.2), (0.2, 0.5)):
        stationary, transition, rewards = _two_state(a, b)
        m, phi = community_switching_to_mean_and_coherence(a, b)
        assert directional_crossover_horizon(stationary, transition, rewards) == pytest.approx(
            asymptotic_directional_crossover_horizon(m, phi)
        )


def test_three_state_reset_chain_has_one_common_relaxation_factor():
    stationary = (0.2, 0.5, 0.3)
    rewards = (-2.0, 0.4, 1.0)
    mean = sum(stationary[i] * rewards[i] for i in range(3))
    reward_var = sum(stationary[i] * (rewards[i] - mean) ** 2 for i in range(3))

    for alpha in (-0.2, 0.0, 0.4, 0.8):
        transition = tuple(
            tuple(
                alpha * (1.0 if i == j else 0.0) + (1.0 - alpha) * stationary[j]
                for j in range(3)
            )
            for i in range(3)
        )
        expected = reward_var * (1.0 + alpha) / (1.0 - alpha)
        assert asymptotic_variance_rate(stationary, transition, rewards) == pytest.approx(expected)


def test_same_community_chain_can_expose_different_evolutionary_timescales_by_reward_alignment():
    # Symmetric three-state chain with eigenvalues 1, 0.7, 0.1.
    # The two reward vectors have equal stationary variance but align with
    # different community relaxation modes.
    stationary, transition = _three_state_mode_chain()
    slow_reward = (sqrt(3 / 2), -sqrt(3 / 2), 0.0)
    fast_reward = (1 / sqrt(2), 1 / sqrt(2), -sqrt(2))

    slow_var = asymptotic_variance_rate(stationary, transition, slow_reward)
    fast_var = asymptotic_variance_rate(stationary, transition, fast_reward)

    assert sum(stationary[i] * slow_reward[i] for i in range(3)) == pytest.approx(0.0)
    assert sum(stationary[i] * fast_reward[i] for i in range(3)) == pytest.approx(0.0)
    assert sum(stationary[i] * slow_reward[i] ** 2 for i in range(3)) == pytest.approx(1.0)
    assert sum(stationary[i] * fast_reward[i] ** 2 for i in range(3)) == pytest.approx(1.0)
    assert slow_var == pytest.approx(17 / 3)
    assert fast_var == pytest.approx(11 / 9)
    assert slow_var > 4.0 * fast_var


def test_existing_structural_tasks_can_align_selection_with_slow_or_fast_community_modes():
    stationary, transition = _three_state_mode_chain()
    gap2 = extremal_routing_task(3)   # C_A=2, C_F=4 -> gap 2
    gap1 = payoff_routing_task()      # C_A=2, C_F=3 -> gap 1
    gap0 = routing_bypass_control()   # C_A=2, C_F=2 -> gap 0

    # Map structural gaps (2,0,1) to c*(1,-1,0), exactly the slow mode.
    c = sqrt(3 / 2)
    slow_reward = structural_rewards_from_tasks(
        (gap2, gap0, gap1),
        lambda_cost=c,
        control_cost=c,
    )

    # Map structural gaps (2,2,0) to (1/sqrt(2),1/sqrt(2),-sqrt(2)),
    # exactly the fast mode, with the same stationary reward variance one.
    fast_reward = structural_rewards_from_tasks(
        (gap2, gap2, gap0),
        lambda_cost=3 / (2 * sqrt(2)),
        control_cost=sqrt(2),
    )

    assert slow_reward == pytest.approx((sqrt(3 / 2), -sqrt(3 / 2), 0.0))
    assert fast_reward == pytest.approx((1 / sqrt(2), 1 / sqrt(2), -sqrt(2)))
    assert sum(stationary[i] * x * x for i, x in enumerate(slow_reward)) == pytest.approx(1.0)
    assert sum(stationary[i] * x * x for i, x in enumerate(fast_reward)) == pytest.approx(1.0)

    slow_var = asymptotic_variance_rate(stationary, transition, slow_reward)
    fast_var = asymptotic_variance_rate(stationary, transition, fast_reward)
    assert slow_var == pytest.approx(17 / 3)
    assert fast_var == pytest.approx(11 / 9)
    assert slow_var / fast_var == pytest.approx(51 / 11)


def test_zero_mean_prefactor_matches_large_h_finite_retention():
    stationary = (0.5, 0.5)
    transition = ((0.8, 0.2), (0.2, 0.8))
    rewards = (-1.0, 1.0)
    prefactor = zero_mean_retention_prefactor(stationary, transition, rewards)
    assert prefactor == pytest.approx(2.0)
    for horizon in (10_000, 100_000):
        observed = rms_retention_fraction(horizon, stationary, transition, rewards) * sqrt(horizon)
        assert observed == pytest.approx(prefactor, rel=2e-3)


def test_poisson_solution_has_stationary_weighted_mean_zero():
    stationary = (0.2, 0.5, 0.3)
    transition = (
        (0.68, 0.20, 0.12),
        (0.08, 0.80, 0.12),
        (0.08, 0.20, 0.72),
    )
    rewards = (-1.0, 0.2, 1.5)
    h = poisson_solution(stationary, transition, rewards)
    assert sum(stationary[i] * h[i] for i in range(3)) == pytest.approx(0.0, abs=1e-10)


def test_zero_mean_crossover_is_infinite_and_deterministic_reward_is_zero_variance():
    stationary = (0.5, 0.5)
    transition = ((0.75, 0.25), (0.25, 0.75))
    assert directional_crossover_horizon(stationary, transition, (-1.0, 1.0)) == inf

    deterministic = (2.0, 2.0)
    assert asymptotic_variance_rate(stationary, transition, deterministic) == pytest.approx(0.0)
    assert directional_crossover_horizon(stationary, transition, deterministic) == pytest.approx(0.0)


def test_multiple_closed_classes_are_rejected_by_poisson_solver():
    stationary = (0.5, 0.5)
    transition = ((1.0, 0.0), (0.0, 1.0))
    with pytest.raises(ValueError):
        asymptotic_variance_rate(stationary, transition, (-1.0, 1.0))


def test_summary_consistent():
    stationary, transition, rewards = _two_state(0.3, 0.2)
    summary = summarize_community_timescale(stationary, transition, rewards)
    assert summary.state_count == 2
    assert summary.asymptotic_variance_rate == pytest.approx(
        asymptotic_variance_rate(stationary, transition, rewards)
    )
    assert summary.directional_crossover_horizon == pytest.approx(
        directional_crossover_horizon(stationary, transition, rewards)
    )
    assert summary.zero_mean_retention_prefactor is None
