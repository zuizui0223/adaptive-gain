from adaptive_gain.balanced_binary_sixteen_world_depth_four_sharp import (
    audit_exact_balanced_sixteen_world_depth_four_sharp,
)


def test_exact_balanced_sixteen_world_depth_four_is_sharp():
    receipt = audit_exact_balanced_sixteen_world_depth_four_sharp()
    assert receipt.world_count == 16
    assert receipt.fixed_cost_cap == 13
    assert receipt.safe_external_cut_count == 3
    assert receipt.reachable_partition_counts_by_safe_subset == (
        81188,
        105064,
        133669,
        171496,
        133669,
        171496,
        219882,
        279840,
    )
    assert receipt.cap_retaining_partition_counts_by_safe_subset == (0,) * 8
    assert (receipt.constructive_adaptive_cost, receipt.constructive_fixed_cost) == (4, 12)
    assert receipt.sharp_depth_four_value == 12
    assert receipt.theorem_holds
