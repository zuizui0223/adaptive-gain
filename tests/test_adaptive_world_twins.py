from itertools import product

from adaptive_gain import FiniteTask, Query, World
from adaptive_gain.adaptive_world_twins import (
    adaptive_world_twin_compressed_minimum_resolution,
    static_target_relevant_world_twin_quotient,
    target_relevant_world_twin_classes,
)
from adaptive_gain.target_pair_incidence import target_pair_incidence_task


def _set_partitions(n):
    rows = []

    def rec(prefix, next_label):
        if len(prefix) == n:
            rows.append(tuple(prefix))
            return
        for label in range(next_label + 1):
            prefix.append(label)
            rec(prefix, max(next_label, label + 1))
            prefix.pop()

    rec([0], 1)
    return tuple(rows)


def _balanced_worlds():
    return (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )


def test_complete_four_world_partition_triples_preserve_adaptive_cost_under_dynamic_twins():
    partitions = _set_partitions(4)
    worlds = _balanced_worlds()
    checked = collapsed = states = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        receipt = adaptive_world_twin_compressed_minimum_resolution(task)
        assert receipt.cost_agrees_with_direct_solver
        collapsed += receipt.world_occurrences_collapsed
        states += receipt.canonical_search_states
        checked += 1
    assert checked == 15 ** 3 == 3_375
    assert collapsed > 0
    assert states > 0


def test_static_world_twin_quotient_can_remove_distinct_pure_outcomes_safely():
    worlds = (
        World("a0", 0), World("a1", 0),
        World("b0", 1), World("b1", 1),
    )
    task = FiniteTask(
        worlds,
        (
            Query("direct", 1, (0, 0, 1, 1)),
            # Same-target worlds can receive different outcomes here, but every
            # such cell is target-pure, so cross-target separation profiles match.
            Query("pure_split", 2, ("a0", "a1", "b0", "b1")),
        ),
    )
    incidence = target_pair_incidence_task(task)
    classes = target_relevant_world_twin_classes(
        incidence,
        world_mask=(1 << 4) - 1,
    )
    assert {frozenset(row.member_world_names) for row in classes} == {
        frozenset({"a0", "a1"}), frozenset({"b0", "b1"})
    }

    quotient, receipt = static_target_relevant_world_twin_quotient(task)
    assert len(quotient.worlds) == 2
    assert receipt.collapsed_world_count == 2
    assert receipt.adaptive_cost_preserved
    assert receipt.fixed_cost_preserved
    assert receipt.original_adaptive_cost == receipt.quotient_adaptive_cost == 1
    assert receipt.original_fixed_cost == receipt.quotient_fixed_cost == 1


def test_twins_can_emerge_only_after_an_opposite_world_routes_away():
    worlds = (
        World("a0", 0), World("a1", 0),
        World("b0", 1), World("b1", 1),
    )
    task = FiniteTask(
        worlds,
        (
            # outcome 0 leaves mixed child {a0,a1,b0}; b1 exits pure.
            Query("route", 1, (0, 0, 0, 1)),
            # At root a0/a1 differ relative to b1, so they are not twins.
            # Inside {a0,a1,b0}, both separate from b0 and become twins.
            Query("finish", 1, ("x", "y", "z", "x")),
        ),
    )
    incidence = target_pair_incidence_task(task)
    root_classes = target_relevant_world_twin_classes(
        incidence,
        world_mask=(1 << 4) - 1,
    )
    assert all(set(row.member_world_names) != {"a0", "a1"} for row in root_classes)

    child_mask = (1 << 0) | (1 << 1) | (1 << 2)
    child_classes = target_relevant_world_twin_classes(
        incidence,
        world_mask=child_mask,
        remaining_query_mask=1 << 1,
    )
    assert any(set(row.member_world_names) == {"a0", "a1"} for row in child_classes)

    receipt = adaptive_world_twin_compressed_minimum_resolution(task)
    assert receipt.minimum_worst_path_cost == 2
    assert receipt.cost_agrees_with_direct_solver
    assert receipt.world_occurrences_collapsed > 0
    assert receipt.maximum_single_state_collapse >= 1
