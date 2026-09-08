from adaptive_gain.balanced_binary_depth_four_sharp import (
    audit_exact_balanced_depth_four_sharp,
)


def test_exact_balanced_depth_four_sharp_n12_n14():
    receipt = audit_exact_balanced_depth_four_sharp()

    twelve = receipt.twelve_world
    assert twelve.world_count == 12
    assert twelve.fixed_cost_cap == 9
    assert twelve.safe_external_cut_count == 3
    assert twelve.reachable_partition_counts_by_safe_subset == (
        6727,
        9018,
        13152,
        17471,
        13152,
        17471,
        25750,
        33918,
    )
    assert twelve.cap_retaining_partition_counts_by_safe_subset == (0,) * 8
    assert (twelve.constructive_adaptive_cost, twelve.constructive_fixed_cost) == (4, 8)
    assert twelve.sharp_depth_four_value == 8
    assert twelve.theorem_holds

    fourteen = receipt.fourteen_world
    assert fourteen.world_count == 14
    assert fourteen.fixed_cost_cap == 11
    assert fourteen.safe_external_cut_count == 3
    assert fourteen.reachable_partition_counts_by_safe_subset == (
        25750,
        33918,
        45730,
        59687,
        45730,
        59687,
        81188,
        105064,
    )
    assert fourteen.cap_retaining_partition_counts_by_safe_subset == (0,) * 8
    assert (fourteen.constructive_adaptive_cost, fourteen.constructive_fixed_cost) == (4, 10)
    assert fourteen.sharp_depth_four_value == 10
    assert fourteen.theorem_holds
    assert receipt.theorem_holds
