from itertools import product

from adaptive_gain import FiniteTask, Query, World
from adaptive_gain.adaptive_two_sided_kernel import (
    adaptive_two_sided_kernel_minimum_resolution,
)


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


def test_complete_four_world_partition_triples_preserve_exact_cost_under_two_sided_kernel():
    partitions = _set_partitions(4)
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    checked = states = world_collapsed = query_pruned = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        receipt = adaptive_two_sided_kernel_minimum_resolution(task)
        assert receipt.cost_agrees_with_direct_solver
        states += receipt.canonical_search_states
        world_collapsed += receipt.world_occurrences_collapsed
        query_pruned += receipt.refinement_dominated_query_occurrences_pruned
        checked += 1
    assert checked == 15 ** 3 == 3_375
    assert states > 0
    assert world_collapsed > 0
    assert query_pruned > 0


def test_two_sided_kernel_uses_both_world_and_query_reductions_on_one_task():
    worlds = (
        World("a0", 0), World("a1", 0),
        World("b0", 1), World("b1", 1),
    )
    task = FiniteTask(
        worlds,
        (
            # route can create a mixed child where a0/a1 become twins.
            Query("route", 1, (0, 0, 0, 1)),
            # finer and cheaper than coarse on the target-relevant pairs.
            Query("fine", 1, ("x", "y", "z", "x")),
            Query("coarse", 2, (0, 0, 1, 0)),
        ),
    )
    receipt = adaptive_two_sided_kernel_minimum_resolution(task)
    assert receipt.cost_agrees_with_direct_solver
    assert receipt.minimum_worst_path_cost == 2
    assert receipt.world_occurrences_collapsed > 0
    assert receipt.refinement_dominated_query_occurrences_pruned > 0
