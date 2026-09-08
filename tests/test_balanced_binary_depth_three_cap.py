from adaptive_gain.balanced_binary_depth_three_cap import (
    audit_exact_balanced_depth_three_fixed_cost_cap,
    exact_balanced_depth_three_cap_witness,
    exact_balanced_six_world_three_query_task,
    sharp_exact_balanced_depth_three_fixed_cost_cap,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution


def _pair(task):
    return (
        adaptive_minimum_resolution(task).minimum_worst_path_cost,
        fixed_minimum_resolution(task).minimum_cost,
    )


def _balanced(task):
    half = len(task.worlds) // 2
    return all(
        set(query.outcomes) <= {0, 1}
        and sum(value == 0 for value in query.outcomes) == half
        and sum(value == 1 for value in query.outcomes) == half
        for query in task.queries
    )


def test_six_world_base_witness_is_exact_balanced_and_cost_three_fixed():
    task = exact_balanced_six_world_three_query_task()
    assert _balanced(task)
    assert _pair(task) == (2, 3)


def test_depth_three_cap_formula_has_unique_ten_world_defect():
    expected = {
        6: 3,
        8: 5,
        10: 6,
        12: 7,
        14: 7,
        16: 7,
        20: 7,
    }
    for world_count, cap in expected.items():
        assert sharp_exact_balanced_depth_three_fixed_cost_cap(world_count) == cap


def test_depth_three_cap_witnesses_attain_every_closed_regime():
    expected_pairs = {
        6: (2, 3),
        8: (3, 5),
        10: (3, 6),
        12: (3, 7),
        14: (3, 7),
    }
    for world_count, pair in expected_pairs.items():
        task = exact_balanced_depth_three_cap_witness(world_count)
        assert _balanced(task)
        assert _pair(task) == pair


def test_depth_three_cap_receipts_close_the_exception_and_stable_tail():
    for world_count in (6, 8, 10, 12, 14):
        receipt = audit_exact_balanced_depth_three_fixed_cost_cap(world_count)
        assert receipt.sharp_fixed_cost_cap == sharp_exact_balanced_depth_three_fixed_cost_cap(world_count)
        assert receipt.witness_adaptive_cost <= 3
        assert receipt.witness_fixed_cost == receipt.sharp_fixed_cost_cap
        assert receipt.universal_tree_cap == 7
        assert receipt.universal_global_balance_cap == world_count - 3
        assert receipt.ten_world_exception_used == (world_count == 10)
        assert receipt.theorem_holds
