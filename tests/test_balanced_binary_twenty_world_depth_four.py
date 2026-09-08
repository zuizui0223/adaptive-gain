from adaptive_gain.balanced_binary_twenty_world_depth_four import (
    audit_exact_balanced_twenty_world_depth_four,
    exact_balanced_depth_four_ceiling_witness,
    exact_balanced_twenty_world_fifteen_query_depth_four_task,
    twenty_world_fifteen_query_private_pairs,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution


def test_twenty_world_witness_exact_cost_pair() -> None:
    task = exact_balanced_twenty_world_fifteen_query_depth_four_task()
    assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 4
    assert fixed_minimum_resolution(task).minimum_cost == 15


def test_twenty_world_queries_are_exactly_balanced_and_private() -> None:
    task = exact_balanced_twenty_world_fifteen_query_depth_four_task()
    assert all(sum(x == 0 for x in q.outcomes) == 10 for q in task.queries)
    assert all(sum(x == 1 for x in q.outcomes) == 10 for q in task.queries)
    for query_index, (left, right) in enumerate(twenty_world_fifteen_query_private_pairs()):
        separating = tuple(
            i for i, query in enumerate(task.queries)
            if query.outcomes[left] != query.outcomes[right]
        )
        assert separating == (query_index,)
        assert task.worlds[left].target != task.worlds[right].target


def test_complementary_padding_preserves_ceiling_family() -> None:
    for world_count in (20, 22, 24):
        task = exact_balanced_depth_four_ceiling_witness(world_count)
        half = world_count // 2
        assert len(task.queries) == 15
        assert all(sum(x == 0 for x in q.outcomes) == half for q in task.queries)
        assert all(sum(x == 1 for x in q.outcomes) == half for q in task.queries)
        assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 4
        assert fixed_minimum_resolution(task).minimum_cost == 15


def test_twenty_world_receipt() -> None:
    receipt = audit_exact_balanced_twenty_world_depth_four()
    assert receipt.theorem_holds
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (4, 15)
    assert receipt.complete_tree_internal_nodes == 15
    assert receipt.complete_tree_distinct_query_labels == 15
