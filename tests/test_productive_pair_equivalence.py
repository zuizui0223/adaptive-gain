from itertools import product

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.productive_frontier_saturation import (
    four_query_productive_frontier_saturation_receipt,
    four_query_sperner_saturation_task,
    minimum_worlds_for_cross_target_pairs,
)
from adaptive_gain.productive_pair_equivalence import (
    cross_target_pair_separator_sets,
    minimal_cross_target_separator_sets,
    productive_pair_equivalence_audit,
)


def _restricted_growth_partitions(n: int):
    rows = []
    def rec(prefix, maximum):
        if len(prefix) == n:
            rows.append(tuple(prefix))
            return
        for value in range(maximum + 2):
            rec(prefix + (value,), max(maximum, value))
    rec((0,), 0)
    return tuple(rows)


def test_q4_minimal_world_sperner_saturation_witness():
    task = four_query_sperner_saturation_task()
    receipt = four_query_productive_frontier_saturation_receipt()
    assert receipt.frontier_size == receipt.sperner_bound == 6
    assert receipt.minimal_productive_sets == (3, 5, 6, 9, 10, 12)
    assert receipt.cross_target_pair_count == 6
    assert receipt.world_count == receipt.lower_bound_world_count == 5
    assert receipt.world_count_minimal_for_saturation
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
    assert receipt.strict_adaptive_gain
    assert productive_pair_equivalence_audit(task).frontiers_equal


def test_five_world_saturation_is_world_deletion_minimal_for_frontier_size_six():
    task = four_query_sperner_saturation_task()
    for removed in range(len(task.worlds)):
        keep = [i for i in range(len(task.worlds)) if i != removed]
        reduced = FiniteTask(
            tuple(task.worlds[i] for i in keep),
            tuple(
                Query(query.name, query.cost, tuple(query.outcomes[i] for i in keep))
                for query in task.queries
            ),
        )
        assert len(minimal_cross_target_separator_sets(reduced)) < 6


def test_pair_count_lower_bound_for_q4_saturation():
    assert minimum_worlds_for_cross_target_pairs(6) == 5
    assert (4 // 2) * (4 - 4 // 2) == 4 < 6
    assert (5 // 2) * (5 - 5 // 2) == 6


def test_all_four_world_three_query_partitions_have_equal_pair_and_state_frontiers():
    partitions = _restricted_growth_partitions(4)
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    checked = disagreements = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        audit = productive_pair_equivalence_audit(task)
        disagreements += int(not audit.frontiers_equal)
        checked += 1
    assert checked == 15 ** 3 == 3_375
    assert disagreements == 0


def test_unresolvable_pair_produces_empty_frontier_edge():
    worlds = (World("a", 0), World("b", 1))
    task = FiniteTask(worlds, (Query("constant", 1, (0, 0)),))
    assert cross_target_pair_separator_sets(task) == (0,)
    assert minimal_cross_target_separator_sets(task) == (0,)
    assert productive_pair_equivalence_audit(task).frontiers_equal
