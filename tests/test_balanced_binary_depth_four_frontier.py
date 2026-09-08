from adaptive_gain.balanced_binary_depth_four_frontier import (
    audit_exact_balanced_depth_four_constructive_frontier,
    exact_balanced_fourteen_world_ten_query_depth_four_task,
    exact_balanced_twelve_world_eight_query_depth_four_task,
    fourteen_world_ten_query_private_pairs,
    twelve_world_eight_query_private_pairs,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution


def _assert_private_pairs(task, pairs):
    assert len(pairs) == len(task.queries)
    for query_index, (left, right) in enumerate(pairs):
        separating = [
            index
            for index, query in enumerate(task.queries)
            if query.outcomes[left] != query.outcomes[right]
        ]
        assert separating == [query_index]
        assert task.worlds[left].target != task.worlds[right].target


def _assert_exact_balance(task):
    half = len(task.worlds) // 2
    for query in task.queries:
        assert sum(outcome == 0 for outcome in query.outcomes) == half
        assert sum(outcome == 1 for outcome in query.outcomes) == half


def test_twelve_world_eight_query_depth_four_witness():
    task = exact_balanced_twelve_world_eight_query_depth_four_task()
    _assert_exact_balance(task)
    _assert_private_pairs(task, twelve_world_eight_query_private_pairs())
    assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 4
    assert fixed_minimum_resolution(task).minimum_cost == 8


def test_fourteen_world_ten_query_depth_four_witness():
    task = exact_balanced_fourteen_world_ten_query_depth_four_task()
    _assert_exact_balance(task)
    _assert_private_pairs(task, fourteen_world_ten_query_private_pairs())
    assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 4
    assert fixed_minimum_resolution(task).minimum_cost == 10


def test_depth_four_constructive_frontier_receipt():
    receipt = audit_exact_balanced_depth_four_constructive_frontier()
    assert receipt.depth_three_flattening_cap == 7
    assert (receipt.twelve_world.adaptive_cost, receipt.twelve_world.fixed_cost) == (4, 8)
    assert (receipt.fourteen_world.adaptive_cost, receipt.fourteen_world.fixed_cost) == (4, 10)
    assert receipt.theorem_holds
