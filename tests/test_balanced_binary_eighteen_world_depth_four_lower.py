from adaptive_gain.balanced_binary_eighteen_world_depth_four_lower import (
    audit_exact_balanced_eighteen_world_depth_four_lower,
    eighteen_world_thirteen_query_private_pairs,
    exact_balanced_eighteen_world_thirteen_query_depth_four_task,
)


def test_eighteen_world_depth_four_lower_receipt() -> None:
    receipt = audit_exact_balanced_eighteen_world_depth_four_lower()
    assert receipt.theorem_holds
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (4, 13)
    assert receipt.component_sizes == (3, 3, 4, 4, 4)


def test_all_queries_are_exactly_balanced_and_private() -> None:
    task = exact_balanced_eighteen_world_thirteen_query_depth_four_task()
    pairs = eighteen_world_thirteen_query_private_pairs()
    assert len(task.worlds) == 18
    assert len(task.queries) == 13
    for q_index, query in enumerate(task.queries):
        assert sum(value == 0 for value in query.outcomes) == 9
        assert sum(value == 1 for value in query.outcomes) == 9
        left, right = pairs[q_index]
        separating = [
            index
            for index, candidate in enumerate(task.queries)
            if candidate.outcomes[left] != candidate.outcomes[right]
        ]
        assert separating == [q_index]
        assert task.worlds[left].target != task.worlds[right].target
