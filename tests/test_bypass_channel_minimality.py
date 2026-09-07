from itertools import product

from adaptive_gain.bypass_channel_minimality import bypass_channel_query_minimality
from adaptive_gain.core import FiniteTask, Query, World, adaptive_minimum_resolution
from adaptive_gain.frontier_transversals import frontier_transversal_policy_decomposition


def _set_partitions(items):
    """Canonical set partitions represented by restricted-growth strings."""
    n = len(items)
    rows = []
    def rec(prefix, maximum):
        if len(prefix) == n:
            rows.append(tuple(prefix))
            return
        for value in range(maximum + 2):
            rec(prefix + [value], max(maximum, value))
    rec([0], 0)
    return tuple(rows)


def test_two_query_arbitrary_partition_unequal_cost_scope_has_no_bypass():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    partitions = _set_partitions(range(4))
    assert len(partitions) == 15
    checked = resolved = 0
    for maps in product(partitions, repeat=2):
        for costs in product((1, 2), repeat=2):
            task = FiniteTask(
                worlds,
                tuple(Query(f"q{i}", costs[i], maps[i]) for i in range(2)),
            )
            checked += 1
            adaptive = adaptive_minimum_resolution(task)
            if adaptive.minimum_worst_path_cost is None:
                continue
            resolved += 1
            decomposition = frontier_transversal_policy_decomposition(task)
            assert decomposition.internal_union_redundancy == 0
            assert decomposition.external_shortcut_discount == 0
    assert checked == 15 ** 2 * 2 ** 2 == 900
    assert resolved > 0


def test_three_query_complete_balanced_binary_scope_has_no_external_shortcut():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    patterns = tuple(product((0, 1), repeat=4))
    checked = resolved = external_positive = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        checked += 1
        adaptive = adaptive_minimum_resolution(task)
        if adaptive.minimum_worst_path_cost is None:
            continue
        resolved += 1
        decomposition = frontier_transversal_policy_decomposition(task)
        external_positive += int((decomposition.external_shortcut_discount or 0) > 0)
    assert checked == 16 ** 3 == 4_096
    assert resolved == 2_408
    assert external_positive == 0


def test_query_count_lower_bounds_are_sharp():
    receipt = bypass_channel_query_minimality()
    assert receipt.internal_minimum_declared_queries == 3
    assert receipt.external_minimum_declared_queries == 4
    assert receipt.internal_bound_attained
    assert receipt.external_bound_attained
    assert receipt.internal_witness_redundancy == 1
    assert receipt.external_witness_discount == 1
