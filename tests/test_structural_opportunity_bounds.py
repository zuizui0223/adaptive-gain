from fractions import Fraction

import pytest

from adaptive_gain.structural_opportunity_bounds import (
    opportunity_bound_holds,
    sharp_edge_capped_normalized_opportunity,
    sharp_normalized_opportunity,
    sharp_rank_capped_normalized_opportunity,
    task_structural_opportunity,
)
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def test_task_opportunity_is_exact_budget_window_normalized_by_adaptive_cost():
    strict = task_structural_opportunity(payoff_routing_task())
    assert strict.adaptive_cost == 2
    assert strict.fixed_cost == 3
    assert strict.adaptive_only_budget_count == 1
    assert strict.normalized_opportunity == Fraction(1, 2)
    assert strict.strict_gain

    bypass = task_structural_opportunity(routing_bypass_control())
    assert bypass.adaptive_cost == 2
    assert bypass.fixed_cost == 2
    assert bypass.adaptive_only_budget_count == 0
    assert bypass.normalized_opportunity == 0
    assert not bypass.strict_gain


def test_source_derived_four_world_binary_task_hits_sharp_scope_bound():
    observed = task_structural_opportunity(payoff_routing_task()).normalized_opportunity
    bound = sharp_normalized_opportunity(4, 3, 2)
    assert observed == Fraction(1, 2)
    assert bound == observed
    assert opportunity_bound_holds(payoff_routing_task(), max_arity=2)


def test_edge_count_cap_can_reduce_maximum_normalized_opportunity():
    unrestricted = sharp_normalized_opportunity(12, 12, 2)
    capped = sharp_edge_capped_normalized_opportunity(12, 12, 2, 1)
    assert capped <= unrestricted
    assert capped == 0  # One minimal frontier obligation cannot create strict fixed/adaptive gain.


def test_rank_cap_is_extremally_vacuous_for_normalized_opportunity():
    unrestricted = sharp_normalized_opportunity(12, 12, 2)
    for rank_cap in (1, 2, 5):
        assert sharp_rank_capped_normalized_opportunity(
            12, 12, 2, rank_cap
        ) == unrestricted


def test_normalized_bound_nonnegative():
    for n in range(2, 8):
        for m in range(1, 7):
            for b in range(2, 5):
                assert sharp_normalized_opportunity(n, m, b) >= 0


def test_invalid_nonunit_task_rejected():
    task = payoff_routing_task()
    from adaptive_gain.core import FiniteTask, Query

    altered = FiniteTask(
        task.worlds,
        (Query(task.queries[0].name, 2, task.queries[0].outcomes),) + task.queries[1:],
    )
    with pytest.raises(ValueError):
        task_structural_opportunity(altered)
