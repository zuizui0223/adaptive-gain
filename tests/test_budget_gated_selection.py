from math import log

import pytest

from adaptive_gain.budget_gated_selection import (
    budget_fitness_state,
    budget_frequency_path,
    budget_resolution_state,
    budget_selection_path,
    maximum_maintenance_cost_for_adaptive_advantage,
)
from adaptive_gain.structural_eco_evolution import (
    evolutionary_selection_activity,
    evolutionary_selection_retention,
    evolutionary_selection_retention_ratio,
)
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def test_strict_task_has_exact_adaptive_only_budget_window():
    task = payoff_routing_task()
    below = budget_resolution_state(task, 1)
    window = budget_resolution_state(task, 2)
    above = budget_resolution_state(task, 3)

    assert (below.adaptive_resolves, below.fixed_resolves) == (False, False)
    assert not below.adaptive_only_window
    assert (window.adaptive_resolves, window.fixed_resolves) == (True, False)
    assert window.adaptive_only_window
    assert (above.adaptive_resolves, above.fixed_resolves) == (True, True)
    assert not above.adaptive_only_window


def test_no_gain_control_has_no_adaptive_only_budget():
    task = routing_bypass_control()
    for budget in (0, 1, 2, 3, 10):
        state = budget_resolution_state(task, budget)
        assert not state.adaptive_only_window


def test_selection_threshold_inside_adaptive_only_window():
    task = payoff_routing_task()
    critical = maximum_maintenance_cost_for_adaptive_advantage(
        baseline_fitness=1.0, resolution_benefit=1.0
    )
    assert critical == pytest.approx(log(2.0))

    favoured = budget_fitness_state(
        task,
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=critical - 0.1,
    )
    neutral = budget_fitness_state(
        task,
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=critical,
    )
    disfavoured = budget_fitness_state(
        task,
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=critical + 0.1,
    )
    assert favoured.log_fitness_ratio > 0
    assert neutral.log_fitness_ratio == pytest.approx(0.0)
    assert disfavoured.log_fitness_ratio < 0


def test_same_budget_can_reverse_selection_between_strict_and_bypass_states():
    strict = payoff_routing_task()       # C_A=2, C_F=3: adaptive only at B=2
    bypass = routing_bypass_control()     # C_A=C_F=2: both resolve at B=2
    half_log2 = 0.5 * log(2.0)

    selection = budget_selection_path(
        (strict, bypass, strict, bypass),
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=half_log2,
    )
    assert selection == pytest.approx(
        (half_log2, -half_log2, half_log2, -half_log2)
    )
    assert evolutionary_selection_activity(selection) == pytest.approx(4 * half_log2)
    assert evolutionary_selection_retention(selection) == pytest.approx(0.0)
    assert evolutionary_selection_retention_ratio(selection) == pytest.approx(0.0)

    path = budget_frequency_path(
        0.27,
        (strict, bypass, strict, bypass),
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=half_log2,
    )
    assert path[1] != pytest.approx(path[0])
    assert path[2] == pytest.approx(path[0])
    assert path[4] == pytest.approx(path[0])


def test_below_budget_both_fail_and_maintenance_cost_selects_against_adaptive():
    state = budget_fitness_state(
        payoff_routing_task(),
        1,
        baseline_fitness=1.0,
        resolution_benefit=3.0,
        contingent_maintenance_log_cost=0.2,
    )
    assert not state.resolution.adaptive_resolves
    assert not state.resolution.fixed_resolves
    assert state.log_fitness_ratio == pytest.approx(-0.2)


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        budget_resolution_state(payoff_routing_task(), -1)
    with pytest.raises(ValueError):
        budget_fitness_state(payoff_routing_task(), 2, baseline_fitness=0)
    with pytest.raises(ValueError):
        budget_fitness_state(payoff_routing_task(), 2, resolution_benefit=-1)
    with pytest.raises(ValueError):
        budget_selection_path((payoff_routing_task(),), (1, 2))
