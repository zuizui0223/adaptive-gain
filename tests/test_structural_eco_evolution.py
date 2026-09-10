import pytest

from adaptive_gain.extremal_routing_family import extremal_routing_task
from adaptive_gain.structural_eco_evolution import (
    cumulative_log_odds_change,
    evolutionary_selection_activity,
    evolutionary_selection_retention,
    evolutionary_selection_retention_ratio,
    frequency_path,
    structural_selection_decomposition,
    structural_selection_path,
    structural_selection_state,
    symmetric_switching_control_cost,
    update_frequency_by_log_fitness_ratio,
)
from adaptive_gain.witnesses import (
    partial_external_bypass_gain_control,
    partial_internal_bypass_gain_control,
    payoff_routing_task,
    routing_bypass_control,
)


def test_strict_task_maps_gap_to_log_fitness_selection():
    state = structural_selection_state(
        payoff_routing_task(), lambda_cost=2.0, control_cost=0.5
    )
    assert state.adaptive_cost == 2
    assert state.fixed_cost == 3
    assert state.structural_gap == 1
    assert state.log_fitness_ratio == pytest.approx(1.5)


def test_no_gain_state_is_selected_against_when_control_cost_positive():
    state = structural_selection_state(
        routing_bypass_control(), lambda_cost=2.0, control_cost=0.5
    )
    assert state.structural_gap == 0
    assert state.log_fitness_ratio == pytest.approx(-0.5)


def test_existing_decomposition_becomes_selection_decomposition():
    state = structural_selection_decomposition(
        partial_external_bypass_gain_control(), lambda_cost=1.7, control_cost=0.2
    )
    assert state.identity_holds
    assert state.structural_gap == 1
    assert state.branch_exclusive_opportunity == 2
    assert state.external_shortcut_discount == 1
    assert state.internal_union_redundancy == 0
    assert state.log_fitness_ratio == pytest.approx(1.5)


def test_internal_redundancy_channel_is_preserved():
    state = structural_selection_decomposition(
        partial_internal_bypass_gain_control(), lambda_cost=1.0, control_cost=0.0
    )
    assert state.branch_exclusive_opportunity == 2
    assert state.external_shortcut_discount == 0
    assert state.internal_union_redundancy == 1
    assert state.structural_gap == 1
    assert state.log_fitness_ratio == pytest.approx(1.0)


def test_extremal_branch_diversity_can_generate_large_structural_selection():
    state = structural_selection_state(
        extremal_routing_task(6), lambda_cost=0.4, control_cost=0.3
    )
    assert state.adaptive_cost == 2
    assert state.fixed_cost == 7
    assert state.structural_gap == 5
    assert state.log_fitness_ratio == pytest.approx(1.7)


def test_exact_log_odds_addition_under_selection():
    p0 = 0.2
    selection = (0.7, -0.1, 0.4)
    path = frequency_path(p0, selection)
    final_direct = update_frequency_by_log_fitness_ratio(
        p0, sum(selection)
    )
    assert path[-1] == pytest.approx(final_direct)
    assert cumulative_log_odds_change(selection) == pytest.approx(1.0)


def test_strong_short_term_selection_can_cancel_exactly_over_two_states():
    high = payoff_routing_task()       # gap 1
    low = routing_bypass_control()     # gap 0
    kappa = symmetric_switching_control_cost(1, 0, lambda_cost=1.0)
    selection = structural_selection_path(
        (high, low), lambda_cost=1.0, control_cost=kappa
    )
    assert selection == pytest.approx((0.5, -0.5))
    assert evolutionary_selection_activity(selection) == pytest.approx(1.0)
    assert evolutionary_selection_retention(selection) == pytest.approx(0.0)
    assert evolutionary_selection_retention_ratio(selection) == pytest.approx(0.0)

    path = frequency_path(0.13, selection)
    assert path[1] != pytest.approx(path[0])
    assert path[2] == pytest.approx(path[0])


def test_persistent_same_sign_selection_is_fully_retained():
    selection = (0.4, 0.4, 0.4, 0.4)
    assert evolutionary_selection_activity(selection) == pytest.approx(1.6)
    assert evolutionary_selection_retention(selection) == pytest.approx(1.6)
    assert evolutionary_selection_retention_ratio(selection) == pytest.approx(1.0)


def test_partial_cancellation_has_intermediate_retention():
    selection = (1.0, -0.4, 0.8, -0.2)
    assert evolutionary_selection_activity(selection) == pytest.approx(2.4)
    assert evolutionary_selection_retention(selection) == pytest.approx(1.2)
    assert evolutionary_selection_retention_ratio(selection) == pytest.approx(0.5)
