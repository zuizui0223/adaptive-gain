from itertools import product

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.state_resource_bounds import (
    state_resource_antichain_bound,
    task_state_resource_kernel_bound,
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


def test_closed_form_rank_sizes_and_maxima():
    expected = {
        0: ((1,), (0,), 1),
        1: ((1, 2), (1,), 2),
        2: ((1, 4, 4), (1, 2), 4),
        3: ((1, 6, 12, 8), (2,), 12),
        4: ((1, 8, 24, 32, 16), (3,), 32),
        5: ((1, 10, 40, 80, 80, 32), (3, 4), 80),
    }
    for q, (ranks, maximizing, maximum) in expected.items():
        receipt = state_resource_antichain_bound(q)
        assert receipt.rank_sizes == ranks
        assert receipt.maximizing_ranks == maximizing
        assert receipt.maximum_antichain_bound == maximum


def test_all_four_world_three_query_partitions_obey_lym_bound():
    partitions = _restricted_growth_partitions(4)
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    checked = max_reduced = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        receipt = task_state_resource_kernel_bound(task)
        assert receipt.reduced_rows_form_antichain
        assert receipt.bound_holds
        assert receipt.lym_weight_numerator <= receipt.lym_weight_denominator
        max_reduced = max(max_reduced, receipt.reduced_row_count)
        checked += 1
    assert checked == 15 ** 3 == 3_375
    assert max_reduced == 6
    assert max_reduced < state_resource_antichain_bound(3).maximum_antichain_bound == 12
