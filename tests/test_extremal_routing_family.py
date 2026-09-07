from fractions import Fraction

from adaptive_gain.core import FiniteTask, Query, adaptive_minimum_resolution, fixed_minimum_resolution
from adaptive_gain.extremal_routing_family import (
    binary_extremal_routing_family_audit,
    binary_extremal_routing_task,
    extremal_routing_family_audit,
    extremal_routing_task,
    first_unit_cost_ratio_above_three_halves_receipt,
    unit_cost_ratio_upper_bound_by_world_count,
)
from adaptive_gain.frontier_decomposition import productive_frontier_policy_decomposition


def _delete_world(task: FiniteTask, index: int) -> FiniteTask:
    worlds = tuple(world for i, world in enumerate(task.worlds) if i != index)
    queries = tuple(
        Query(
            query.name,
            query.cost,
            tuple(outcome for i, outcome in enumerate(query.outcomes) if i != index),
        )
        for query in task.queries
    )
    return FiniteTask(worlds, queries)


def test_extremal_family_exact_cost_formula_and_frontier_singletons():
    for k in range(2, 9):
        receipt = extremal_routing_family_audit(k)
        assert receipt.theorem_holds
        assert receipt.world_count == 2 * k
        assert receipt.query_count == k + 1
        assert receipt.adaptive_cost == 2
        assert receipt.fixed_cost == k + 1
        assert receipt.additive_gain == k - 1
        assert receipt.ratio == Fraction(k + 1, 2)
        assert receipt.every_query_frontier_mandatory
        assert receipt.minimal_frontier_edges == tuple(1 << q for q in range(k + 1))


def test_extremal_family_has_no_internal_or_external_fixed_bypass():
    for k in range(2, 7):
        receipt = productive_frontier_policy_decomposition(extremal_routing_task(k))
        assert receipt.agrees_with_direct_decomposition
        assert receipt.adaptive_cost == 2
        assert receipt.fixed_cost == k + 1
        assert receipt.policy_union_cost == k + 1
        assert receipt.policy_union_restricted_fixed_cost == k + 1
        assert receipt.branch_exclusive_overhead == k - 1
        assert receipt.realized_adaptive_gain == k - 1
        assert receipt.internal_union_redundancy == 0
        assert receipt.external_shortcut_discount == 0


def test_ratio_is_unbounded_along_multivalued_router_family():
    ratios = [extremal_routing_family_audit(k).ratio for k in (2, 3, 5, 10)]
    assert ratios == [Fraction(3, 2), Fraction(2, 1), Fraction(3, 1), Fraction(11, 2)]
    assert ratios == sorted(ratios)


def test_binary_family_direct_solver_matches_formula_for_small_depths():
    expected = {
        1: (2, 2, Fraction(1, 1)),
        2: (3, 4, Fraction(4, 3)),
        3: (4, 8, Fraction(2, 1)),
    }
    for depth, target in expected.items():
        receipt = binary_extremal_routing_family_audit(depth, direct_check=True)
        assert receipt.theorem_holds
        assert (receipt.expected_adaptive_cost, receipt.expected_fixed_cost, receipt.expected_ratio) == target
        assert (receipt.direct_adaptive_cost, receipt.direct_fixed_cost) == target[:2]
        assert receipt.lower_bound_minimum == depth + 1


def test_binary_family_ratio_is_unbounded_without_running_large_exact_solver():
    ratios = [
        binary_extremal_routing_family_audit(depth, direct_check=False).expected_ratio
        for depth in (1, 2, 3, 4, 6, 8)
    ]
    assert ratios == [
        Fraction(1, 1),
        Fraction(4, 3),
        Fraction(2, 1),
        Fraction(16, 5),
        Fraction(64, 7),
        Fraction(256, 9),
    ]
    assert ratios == sorted(ratios)


def test_binary_task_has_only_binary_outcomes():
    task = binary_extremal_routing_task(3)
    assert all(set(query.outcomes) <= {0, 1} for query in task.queries)
    assert len(task.worlds) == 16
    assert len(task.queries) == 11


def test_six_world_four_query_member_is_first_unit_cost_scope_above_three_halves():
    receipt = first_unit_cost_ratio_above_three_halves_receipt()
    assert receipt.maximum_possible_ratio_under_bound == Fraction(3, 2)
    assert receipt.ratio_above_threshold_impossible
    assert receipt.minimum_query_count_if_threshold_exceeded == 4
    assert (receipt.witness_world_count, receipt.witness_query_count) == (6, 4)
    assert receipt.witness_ratio == 2
    assert unit_cost_ratio_upper_bound_by_world_count(4) == Fraction(3, 2)
    assert unit_cost_ratio_upper_bound_by_world_count(5) == Fraction(3, 2)


def test_k3_ratio_above_three_halves_disappears_after_any_world_deletion():
    task = extremal_routing_task(3)
    assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 2
    assert fixed_minimum_resolution(task).minimum_cost == 4
    for i in range(len(task.worlds)):
        reduced = _delete_world(task, i)
        ca = adaptive_minimum_resolution(reduced).minimum_worst_path_cost
        cf = fixed_minimum_resolution(reduced).minimum_cost
        assert ca is not None and cf is not None
        assert Fraction(cf, ca) <= Fraction(3, 2)
