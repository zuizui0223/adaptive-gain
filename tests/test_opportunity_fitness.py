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
    opportunity_log_selection,
    hard_budget_log_selection,
    pairwise_architecture_log_selection,
    empirical_timely_success_probability,
    empirical_pairwise_log_selection,
    opportunity_log_recovery_exponential,
    opportunity_architecture_thresholds_exponential,
    opportunity_architecture_value_exponential,
    opportunity_uniform_recovery_parameters,
    opportunity_architecture_optimum_uniform,
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


def test_stochastic_log_selection_recovers_hard_budget_three_regions():
    c_a, c_f = 2.0, 3.0
    w0, value, kappa = 1.0, 1.0, 0.2

    below = hard_budget_log_selection(
        c_a,
        c_f,
        1.0,
        baseline_fitness=w0,
        resolution_value=value,
        maintenance_log_cost=kappa,
    )
    middle = hard_budget_log_selection(
        c_a,
        c_f,
        2.0,
        baseline_fitness=w0,
        resolution_value=value,
        maintenance_log_cost=kappa,
    )
    above = hard_budget_log_selection(
        c_a,
        c_f,
        3.0,
        baseline_fitness=w0,
        resolution_value=value,
        maintenance_log_cost=kappa,
    )

    assert below == pytest.approx(-kappa)
    assert middle == pytest.approx(math.log(2.0) - kappa)
    assert above == pytest.approx(-kappa)


def test_soft_opportunity_selection_is_positive_without_maintenance_when_strict():
    rate = 0.5
    s = opportunity_log_selection(
        2.0,
        3.0,
        exp_survival(rate),
        baseline_fitness=1.0,
        resolution_value=2.0,
        maintenance_log_cost=0.0,
    )
    assert s > 0.0


def test_weak_value_limit_recovers_window_mass_coefficient():
    c_a, c_f = 2.0, 3.0
    rate = 0.4
    surv = exp_survival(rate)
    epsilon = 1e-7

    exact = opportunity_log_selection(
        c_a,
        c_f,
        surv,
        baseline_fitness=1.0,
        resolution_value=epsilon,
        maintenance_log_cost=0.0,
    )
    first_order = epsilon * opportunity_window_mass(c_a, c_f, surv)

    assert exact == pytest.approx(first_order, rel=1e-6, abs=1e-14)


def test_comparator_semantics_can_reverse_pairwise_selection():
    surv = exp_survival(0.5)

    # Canonical r=a=b=1 two-branch runtime costs:
    # preindexed P = 1, contingent A = 2, universal fixed U = 3.
    s_a_vs_u = pairwise_architecture_log_selection(
        2.0,
        3.0,
        surv,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    s_a_vs_p = pairwise_architecture_log_selection(
        2.0,
        1.0,
        surv,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )

    assert s_a_vs_u > 0.0
    assert s_a_vs_p < 0.0


def test_architecture_overhead_can_reverse_runtime_ordering():
    surv = exp_survival(0.5)

    # P is faster at runtime, but sufficiently larger constitutive overhead
    # can make the contingent architecture fitter overall.
    s_a_vs_p = pairwise_architecture_log_selection(
        2.0,
        1.0,
        surv,
        baseline_fitness=1.0,
        resolution_value=1.0,
        focal_maintenance_log_cost=0.0,
        comparator_maintenance_log_cost=1.0,
    )
    assert s_a_vs_p > 0.0



def test_empirical_overlap_recovers_deterministic_deadline_case():
    q = empirical_timely_success_probability([2.0, 2.0], [1.0, 2.0, 3.0])
    assert q == pytest.approx(2.0 / 3.0)


def test_equal_mean_completion_times_can_reverse_under_different_opportunities():
    # Same mean completion time (=2), different early/late tails.
    architecture_x = [1.0, 3.0]
    architecture_y = [2.0, 2.0]

    short_windows = [1.5]
    long_windows = [2.5]

    s_short = empirical_pairwise_log_selection(
        architecture_x,
        architecture_y,
        short_windows,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    s_long = empirical_pairwise_log_selection(
        architecture_x,
        architecture_y,
        long_windows,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )

    assert sum(architecture_x) / 2 == sum(architecture_y) / 2 == 2.0
    assert s_short > 0.0
    assert s_long < 0.0


def test_nonresolution_can_be_encoded_as_infinite_completion_time():
    q = empirical_timely_success_probability(
        [1.0, math.inf],
        [2.0],
    )
    assert q == pytest.approx(0.5)



def test_opportunity_generated_recovery_is_convex():
    kwargs = dict(
        baseline_completion_cost=4.0,
        closure_rate=0.7,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    r0 = opportunity_log_recovery_exponential(0.0, **kwargs)
    r1 = opportunity_log_recovery_exponential(1.0, **kwargs)
    r2 = opportunity_log_recovery_exponential(2.0, **kwargs)

    assert r0 == pytest.approx(0.0)
    assert (r2 - r1) > (r1 - r0)


def test_local_global_threshold_gap_is_strict():
    local, global_threshold = opportunity_architecture_thresholds_exponential(
        2.0,
        baseline_completion_cost=4.0,
        closure_rate=0.7,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    assert 0.0 < local < global_threshold


def test_finite_jump_barrier_exists_between_thresholds():
    kwargs = dict(
        baseline_completion_cost=4.0,
        closure_rate=0.7,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    local, global_threshold = opportunity_architecture_thresholds_exponential(
        2.0,
        **kwargs,
    )
    k = (local + global_threshold) / 2.0

    epsilon = 1e-5
    near_zero = opportunity_architecture_value_exponential(
        epsilon,
        architecture_cost_per_saving=k,
        **kwargs,
    )
    full = opportunity_architecture_value_exponential(
        2.0,
        architecture_cost_per_saving=k,
        **kwargs,
    )

    assert near_zero < 0.0
    assert full > 0.0



def test_uniform_opportunity_has_partial_routing_regime():
    d, a = opportunity_uniform_recovery_parameters(
        baseline_completion_cost=4.0,
        opportunity_upper_bound=6.0,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    assert d > 0.0
    max_saving = 2.0

    lower = a / (1.0 + a * max_saving)
    upper = a
    k = (lower + upper) / 2.0

    optimum = opportunity_architecture_optimum_uniform(
        max_saving,
        baseline_completion_cost=4.0,
        opportunity_upper_bound=6.0,
        architecture_cost_per_saving=k,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    assert 0.0 < optimum < max_saving


def test_uniform_opportunity_endpoint_regimes():
    _, a = opportunity_uniform_recovery_parameters(
        baseline_completion_cost=4.0,
        opportunity_upper_bound=6.0,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    max_saving = 2.0
    lower = a / (1.0 + a * max_saving)

    none = opportunity_architecture_optimum_uniform(
        max_saving,
        baseline_completion_cost=4.0,
        opportunity_upper_bound=6.0,
        architecture_cost_per_saving=a * 1.1,
    )
    full = opportunity_architecture_optimum_uniform(
        max_saving,
        baseline_completion_cost=4.0,
        opportunity_upper_bound=6.0,
        architecture_cost_per_saving=lower * 0.9,
    )

    assert none == pytest.approx(0.0)
    assert full == pytest.approx(max_saving)
