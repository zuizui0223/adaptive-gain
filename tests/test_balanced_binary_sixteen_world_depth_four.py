from adaptive_gain.balanced_binary_sixteen_world_depth_four import (
    audit_exact_balanced_sixteen_world_depth_four,
    exact_balanced_sixteen_world_twelve_query_depth_four_task,
    sixteen_world_depth_four_policy,
    sixteen_world_twelve_query_private_pairs,
)


def test_exact_balanced_sixteen_world_depth_four_witness():
    task = exact_balanced_sixteen_world_twelve_query_depth_four_task()
    assert len(task.worlds) == 16
    assert len(task.queries) == 12
    assert len(sixteen_world_twelve_query_private_pairs()) == 12
    assert sixteen_world_depth_four_policy()[0] == 7

    receipt = audit_exact_balanced_sixteen_world_depth_four()
    assert receipt.world_count == 16
    assert receipt.query_count == 12
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (4, 12)
    assert receipt.component_sizes == (2, 3, 4, 7)
    assert receipt.all_queries_exactly_balanced
    assert receipt.all_private_pairs_query_unique
    assert receipt.all_private_pairs_cross_target
    assert receipt.theorem_holds
