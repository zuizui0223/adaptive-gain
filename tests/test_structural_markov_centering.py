from math import inf

import pytest

from adaptive_gain.extremal_routing_family import extremal_routing_task
from adaptive_gain.structural_markov_centering import (
    centered_structural_crossover_horizon,
    control_invariant_asymptotic_variance,
    critical_control_cost,
    structural_gaps,
    structural_selection_rewards,
    summarize_structural_centering,
)
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def _community():
    stationary = (1 / 3, 1 / 3, 1 / 3)
    transition = (
        (0.7, 0.0, 0.3),
        (0.0, 0.7, 0.3),
        (0.3, 0.3, 0.4),
    )
    tasks = (
        routing_bypass_control(),   # gap 0
        payoff_routing_task(),      # gap 1
        extremal_routing_task(3),   # gap 2
    )
    return stationary, transition, tasks


def test_existing_tasks_supply_exact_gap_vector_zero_one_two():
    _, _, tasks = _community()
    assert structural_gaps(tasks) == (0, 1, 2)


def test_critical_control_cost_centers_stationary_selection():
    stationary, transition, tasks = _community()
    kappa_star = critical_control_cost(stationary, transition, tasks, lambda_cost=1.0)
    assert kappa_star == pytest.approx(1.0)
    rewards = structural_selection_rewards(
        tasks,
        lambda_cost=1.0,
        control_cost=kappa_star,
    )
    assert rewards == pytest.approx((-1.0, 0.0, 1.0))
    assert centered_structural_crossover_horizon(
        stationary,
        transition,
        tasks,
        lambda_cost=1.0,
        control_cost=kappa_star,
    ) == inf


def test_state_independent_control_cost_does_not_change_asymptotic_fluctuation_scale():
    stationary, transition, tasks = _community()
    values = [
        control_invariant_asymptotic_variance(
            stationary,
            transition,
            tasks,
            lambda_cost=1.3,
            control_cost=kappa,
        )
        for kappa in (0.0, 0.2, 1.3, 2.0, 5.0)
    ]
    assert max(values) - min(values) < 1e-10


def test_crossover_diverges_quadratically_near_critical_control_cost():
    stationary, transition, tasks = _community()
    kappa_star = critical_control_cost(stationary, transition, tasks)
    h_far = centered_structural_crossover_horizon(
        stationary, transition, tasks, control_cost=kappa_star - 0.2
    )
    h_near = centered_structural_crossover_horizon(
        stationary, transition, tasks, control_cost=kappa_star - 0.1
    )
    assert h_near == pytest.approx(4.0 * h_far)


def test_same_fluctuations_can_switch_between_directional_trend_and_long_term_stasis():
    stationary, transition, tasks = _community()
    below = summarize_structural_centering(
        stationary, transition, tasks, control_cost=0.8
    )
    centered = summarize_structural_centering(
        stationary, transition, tasks, control_cost=1.0
    )
    above = summarize_structural_centering(
        stationary, transition, tasks, control_cost=1.2
    )

    assert below.stationary_mean_selection == pytest.approx(0.2)
    assert centered.stationary_mean_selection == pytest.approx(0.0)
    assert above.stationary_mean_selection == pytest.approx(-0.2)
    assert below.asymptotic_variance_rate == pytest.approx(centered.asymptotic_variance_rate)
    assert above.asymptotic_variance_rate == pytest.approx(centered.asymptotic_variance_rate)
    assert centered.crossover_horizon == inf
    assert below.crossover_horizon == pytest.approx(above.crossover_horizon)


def test_lambda_scales_fluctuation_variance_quadratically():
    stationary, transition, tasks = _community()
    base = control_invariant_asymptotic_variance(
        stationary, transition, tasks, lambda_cost=1.0, control_cost=0.0
    )
    doubled = control_invariant_asymptotic_variance(
        stationary, transition, tasks, lambda_cost=2.0, control_cost=100.0
    )
    assert doubled == pytest.approx(4.0 * base)


def test_invalid_inputs_raise():
    stationary, transition, tasks = _community()
    with pytest.raises(ValueError):
        critical_control_cost(stationary, transition, tasks, lambda_cost=-1.0)
    with pytest.raises(ValueError):
        summarize_structural_centering(
            stationary, transition, tasks, control_cost=-0.1
        )
