import math

import pytest

from adaptive_gain.core import (
    FiniteTask,
    Query,
    World,
    adaptive_minimum_resolution,
    fixed_minimum_resolution,
)

from adaptive_gain.opportunity_fitness import (
    exponential_max_window_mass,
    exponential_optimal_closure_rate,
    exponential_window_mass,
    opportunity_selection_margin,
    opportunity_window_mass,
    pathwise_advantage_over_fixed,
)


def exp_survival(rate):
    return lambda c: math.exp(-rate * c)


def test_window_mass_is_survival_difference():
    rate = 0.4
    got = opportunity_window_mass(2.0, 3.0, exp_survival(rate))
    expected = math.exp(-0.8) - math.exp(-1.2)
    assert got == pytest.approx(expected)


def test_payoff_style_witness_has_exact_interior_optimum():
    c_a, c_f = 2.0, 3.0
    rate_star = exponential_optimal_closure_rate(c_a, c_f)
    assert rate_star == pytest.approx(math.log(1.5))
    assert exponential_window_mass(c_a, c_f, rate_star) == pytest.approx(4.0 / 27.0)
    assert exponential_max_window_mass(c_a, c_f) == pytest.approx(4.0 / 27.0)


def test_gap_two_witness_peak():
    c_a, c_f = 2.0, 4.0
    rate_star = exponential_optimal_closure_rate(c_a, c_f)
    assert rate_star == pytest.approx(math.log(2.0) / 2.0)
    assert exponential_window_mass(c_a, c_f, rate_star) == pytest.approx(0.25)


def test_window_is_hump_shaped_around_unique_optimum():
    c_a, c_f = 2.0, 3.0
    rate_star = exponential_optimal_closure_rate(c_a, c_f)
    peak = exponential_window_mass(c_a, c_f, rate_star)
    assert exponential_window_mass(c_a, c_f, rate_star / 3.0) < peak
    assert exponential_window_mass(c_a, c_f, rate_star * 3.0) < peak
    assert exponential_window_mass(c_a, c_f, 0.0) == pytest.approx(0.0)


def test_equal_gap_does_not_imply_equal_fitness_value():
    rate = 0.5
    early = exponential_window_mass(1.0, 2.0, rate)
    late = exponential_window_mass(3.0, 4.0, rate)
    assert early > late


def test_maintenance_cost_subtracts_from_opportunity_benefit():
    rate = 0.4
    surv = exp_survival(rate)
    raw = opportunity_window_mass(2.0, 3.0, surv)
    margin = opportunity_selection_margin(
        2.0,
        3.0,
        surv,
        value=2.0,
        maintenance_cost=0.1,
    )
    assert margin == pytest.approx(2.0 * raw - 0.1)


def test_pathwise_advantage_exceeds_worst_path_window_lower_bound():
    rate = 0.4
    surv = exp_survival(rate)
    adaptive_costs = [1.0, 2.0, 2.0]
    probs = [0.2, 0.3, 0.5]
    c_a = max(adaptive_costs)
    c_f = 3.0

    pathwise = pathwise_advantage_over_fixed(
        adaptive_costs,
        probs,
        c_f,
        surv,
        value=1.0,
    )
    lower_bound = opportunity_window_mass(c_a, c_f, surv)

    assert pathwise > lower_bound


def test_invalid_cost_order_is_rejected():
    with pytest.raises(ValueError):
        exponential_window_mass(3.0, 2.0, 0.5)


def test_optimal_rate_requires_strict_positive_window():
    with pytest.raises(ValueError):
        exponential_optimal_closure_rate(0.0, 2.0)
    with pytest.raises(ValueError):
        exponential_optimal_closure_rate(2.0, 2.0)


def _selected_policy_path_costs(task):
    receipt = adaptive_minimum_resolution(task)
    assert receipt.selected_policy is not None
    query_cost = {q.name: q.cost for q in task.queries}
    by_world = {}

    def walk(node, accrued):
        if node.query is None:
            for name in node.remaining_world_names:
                by_world[name] = accrued
            return
        new_cost = accrued + query_cost[node.query]
        for _, child in node.branches:
            walk(child, new_cost)

    walk(receipt.selected_policy, 0)
    return by_world


def _same_guarantee_pair_tasks():
    worlds = (
        World("a0", 0),
        World("b0", 1),
        World("a1", 0),
        World("b1", 1),
        World("extra0", 0),
    )
    terminal0 = (0, 1, 1, 1, 0)
    terminal1 = (0, 0, 0, 1, 0)

    always_mixed = FiniteTask(
        worlds,
        (
            Query("router", 1, (0, 0, 1, 1, 0)),
            Query("terminal0", 1, terminal0),
            Query("terminal1", 1, terminal1),
        ),
    )
    one_root_pure = FiniteTask(
        worlds,
        (
            Query("router", 1, (0, 0, 1, 1, 2)),
            Query("terminal0", 1, terminal0),
            Query("terminal1", 1, terminal1),
        ),
    )
    return always_mixed, one_root_pure


def test_same_guarantee_pair_can_have_different_pathwise_fitness():
    task_a, task_b = _same_guarantee_pair_tasks()

    for task in (task_a, task_b):
        assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 2
        assert fixed_minimum_resolution(task).minimum_cost == 3

    paths_a = sorted(_selected_policy_path_costs(task_a).values())
    paths_b = sorted(_selected_policy_path_costs(task_b).values())
    assert paths_a == [2, 2, 2, 2, 2]
    assert paths_b == [1, 2, 2, 2, 2]

    rate = 0.5
    surv = exp_survival(rate)
    probs = [0.2] * 5
    fit_a = pathwise_advantage_over_fixed(paths_a, probs, 3.0, surv)
    fit_b = pathwise_advantage_over_fixed(paths_b, probs, 3.0, surv)

    expected_difference = 0.2 * (surv(1.0) - surv(2.0))
    assert fit_b - fit_a == pytest.approx(expected_difference)
    assert fit_b > fit_a
