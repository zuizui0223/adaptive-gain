from math import sqrt

import pytest

from adaptive_gain.endogenous_community_feedback import (
    feedback_step,
    interior_feedback_equilibrium,
    phenotype_dependent_transition_matrix,
    simulate_structural_feedback,
    structural_feedback_equilibrium,
    structural_feedback_rewards,
    target_high_state_occupancy,
)
from adaptive_gain.extremal_routing_family import extremal_routing_task
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def _gap01_tasks():
    return routing_bypass_control(), payoff_routing_task()


def test_repo_native_gap_zero_one_rewards_are_equal_and_opposite_at_midpoint_cost():
    low, high = _gap01_tasks()
    rewards = structural_feedback_rewards(
        low,
        high,
        lambda_cost=1.0,
        control_cost=0.5,
    )
    assert rewards == pytest.approx((-0.5, 0.5))


def test_phenotype_dependent_transition_has_requested_stationary_occupancy_and_memory():
    p = 0.8
    q_base = 0.5
    eta = -0.5
    phi = 0.8
    q_target = target_high_state_occupancy(
        p,
        q_base=q_base,
        feedback_strength=eta,
    )
    transition = phenotype_dependent_transition_matrix(
        p,
        q_base=q_base,
        feedback_strength=eta,
        community_memory=phi,
    )
    a = transition[0][1]
    b = transition[1][0]
    assert q_target == pytest.approx(0.35)
    assert a / (a + b) == pytest.approx(q_target)
    assert 1.0 - a - b == pytest.approx(phi)


def test_negative_feedback_stabilizes_repo_native_interior_equilibrium():
    low, high = _gap01_tasks()
    eq = structural_feedback_equilibrium(
        low,
        high,
        lambda_cost=1.0,
        control_cost=0.5,
        q_base=0.5,
        feedback_strength=-1.0,
        community_memory=0.8,
    )
    assert eq.status == "interior_equilibrium"
    assert eq.phenotype_frequency == pytest.approx(0.5)
    assert eq.high_state_occupancy == pytest.approx(0.5)
    assert eq.reward_contrast == pytest.approx(1.0)
    assert eq.locally_stable
    assert eq.jury_conditions is not None
    assert all(value > 0.0 for value in eq.jury_conditions)
    assert eq.eigenvalues is not None
    assert abs(eq.eigenvalues[0]) == pytest.approx(sqrt(0.85))
    assert abs(eq.eigenvalues[1]) == pytest.approx(sqrt(0.85))


def test_positive_feedback_destabilizes_same_interior_equilibrium():
    low, high = _gap01_tasks()
    eq = structural_feedback_equilibrium(
        low,
        high,
        lambda_cost=1.0,
        control_cost=0.5,
        q_base=0.5,
        feedback_strength=0.5,
        community_memory=0.8,
    )
    assert eq.phenotype_frequency == pytest.approx(0.5)
    assert eq.high_state_occupancy == pytest.approx(0.5)
    assert not eq.locally_stable
    assert eq.jury_conditions is not None
    assert eq.jury_conditions[0] < 0.0


def test_community_memory_changes_transient_eigenvalues_but_not_equilibrium_or_stability_boundary():
    low, high = _gap01_tasks()
    fast = structural_feedback_equilibrium(
        low,
        high,
        lambda_cost=1.0,
        control_cost=0.5,
        q_base=0.5,
        feedback_strength=-1.0,
        community_memory=0.2,
    )
    slow = structural_feedback_equilibrium(
        low,
        high,
        lambda_cost=1.0,
        control_cost=0.5,
        q_base=0.5,
        feedback_strength=-1.0,
        community_memory=0.8,
    )
    assert fast.locally_stable and slow.locally_stable
    assert fast.phenotype_frequency == pytest.approx(slow.phenotype_frequency)
    assert fast.high_state_occupancy == pytest.approx(slow.high_state_occupancy)
    assert fast.eigenvalues is not None and slow.eigenvalues is not None
    assert max(abs(x) for x in slow.eigenvalues) > max(abs(x) for x in fast.eigenvalues)


def test_too_strong_negative_feedback_can_overshoot_when_structural_reward_contrast_is_large():
    low = routing_bypass_control()      # gap 0
    high = extremal_routing_task(3)    # gap 2
    # lambda=3 -> reward contrast Delta_s=6; kappa=3 centers q*=1/2.
    stable = structural_feedback_equilibrium(
        low,
        high,
        lambda_cost=3.0,
        control_cost=3.0,
        q_base=0.5,
        feedback_strength=-0.5,
        community_memory=0.5,
    )
    unstable = structural_feedback_equilibrium(
        low,
        high,
        lambda_cost=3.0,
        control_cost=3.0,
        q_base=0.5,
        feedback_strength=-1.0,
        community_memory=0.5,
    )
    assert stable.reward_contrast == pytest.approx(6.0)
    assert stable.locally_stable
    assert not unstable.locally_stable
    assert unstable.jury_conditions is not None
    assert unstable.jury_conditions[2] < 0.0


def test_negative_feedback_simulation_converges_to_interior_equilibrium():
    low, high = _gap01_tasks()
    p_path, q_path, s_path = simulate_structural_feedback(
        low,
        high,
        initial_frequency=0.8,
        initial_high_occupancy=0.8,
        generations=250,
        lambda_cost=1.0,
        control_cost=0.5,
        q_base=0.5,
        feedback_strength=-1.0,
        community_memory=0.8,
    )
    assert p_path[-1] == pytest.approx(0.5, abs=1e-5)
    assert q_path[-1] == pytest.approx(0.5, abs=1e-5)
    assert abs(s_path[-1]) < 1e-5
    assert any(abs(p_path[t + 1] - p_path[t]) > 1e-4 for t in range(20))


def test_positive_feedback_simulation_runs_toward_boundary():
    low, high = _gap01_tasks()
    p_path, q_path, _ = simulate_structural_feedback(
        low,
        high,
        initial_frequency=0.6,
        initial_high_occupancy=0.6,
        generations=200,
        lambda_cost=1.0,
        control_cost=0.5,
        q_base=0.5,
        feedback_strength=0.5,
        community_memory=0.8,
    )
    assert p_path[-1] > 0.99
    assert q_path[-1] > 0.74


def test_direct_step_matches_mean_selection_and_relaxation_equations():
    p_next, q_next, selection = feedback_step(
        0.6,
        0.7,
        low_reward=-0.5,
        high_reward=0.5,
        q_base=0.5,
        feedback_strength=-0.5,
        community_memory=0.8,
    )
    assert selection == pytest.approx(0.2)
    assert q_next == pytest.approx(0.8 * 0.7 + 0.2 * 0.45)
    assert p_next > 0.6


def test_invalid_global_feedback_geometry_rejected():
    with pytest.raises(ValueError):
        target_high_state_occupancy(
            0.5,
            q_base=0.5,
            feedback_strength=1.2,
        )
    with pytest.raises(ValueError):
        interior_feedback_equilibrium(
            low_reward=-0.5,
            high_reward=0.5,
            q_base=0.5,
            feedback_strength=-0.5,
            community_memory=1.0,
        )
