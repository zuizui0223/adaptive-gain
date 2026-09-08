from adaptive_gain.balanced_binary_twenty_two_world_depth_five import (
    audit_exact_balanced_twenty_two_world_depth_five,
    exact_balanced_twenty_two_world_seventeen_query_depth_five_task,
    twenty_two_world_seventeen_query_private_pairs,
)


def test_twenty_two_world_depth_five_receipt() -> None:
    receipt = audit_exact_balanced_twenty_two_world_depth_five()
    assert receipt.theorem_holds
    assert receipt.world_count == 22
    assert receipt.query_count == 17
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (5, 17)


def test_all_seventeen_queries_exactly_balanced_and_private() -> None:
    task = exact_balanced_twenty_two_world_seventeen_query_depth_five_task()
    assert all(sum(q.outcomes) == 11 for q in task.queries)
    for qi, (a, b) in enumerate(twenty_two_world_seventeen_query_private_pairs()):
        separating = tuple(i for i, q in enumerate(task.queries) if q.outcomes[a] != q.outcomes[b])
        assert separating == (qi,)
        assert task.worlds[a].target != task.worlds[b].target
