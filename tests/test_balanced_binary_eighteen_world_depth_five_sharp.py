from adaptive_gain.balanced_binary_eighteen_world_depth_five_sharp import (
    audit_exact_balanced_eighteen_world_depth_five_sharp,
    eighteen_world_fourteen_query_depth_five_private_pairs,
    exact_balanced_eighteen_world_fourteen_query_depth_five_task,
)


def test_eighteen_world_depth_five_sharp_value() -> None:
    receipt = audit_exact_balanced_eighteen_world_depth_five_sharp()
    assert receipt.theorem_holds
    assert receipt.sharp_depth_five_value == 14
    assert (receipt.witness_adaptive_cost, receipt.witness_fixed_cost) == (5, 14)


def test_cap_fifteen_requires_depth_eight() -> None:
    receipt = audit_exact_balanced_eighteen_world_depth_five_sharp()
    assert receipt.fourteen_query_subfamily_counts == (15, 120, 120, 680, 120, 680, 680, 3060)
    assert receipt.cap_unique_witness_pair_counts == (15, 15, 36, 36, 36, 36, 57, 57)
    assert receipt.cap_mandatory_pair_adaptive_depths == (8,) * 8


def test_fourteen_query_witness_is_exact_balanced_and_private() -> None:
    task = exact_balanced_eighteen_world_fourteen_query_depth_five_task()
    pairs = eighteen_world_fourteen_query_depth_five_private_pairs()
    assert len(task.worlds) == 18
    assert len(task.queries) == 14
    for query_index, query in enumerate(task.queries):
        assert sum(x == 0 for x in query.outcomes) == 9
        assert sum(x == 1 for x in query.outcomes) == 9
        left, right = pairs[query_index]
        separating = tuple(
            i for i, candidate in enumerate(task.queries)
            if candidate.outcomes[left] != candidate.outcomes[right]
        )
        assert separating == (query_index,)
        assert task.worlds[left].target != task.worlds[right].target
