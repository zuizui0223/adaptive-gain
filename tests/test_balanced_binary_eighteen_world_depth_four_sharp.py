from adaptive_gain.balanced_binary_eighteen_world_depth_four_sharp import (
    ADMISSIBLE_COMPONENT_SIZE_TYPES,
    audit_exact_balanced_eighteen_world_depth_four_sharp,
)


def test_eighteen_world_depth_four_sharp_receipt() -> None:
    receipt = audit_exact_balanced_eighteen_world_depth_four_sharp()
    assert receipt.theorem_holds
    assert receipt.world_count == 18
    assert receipt.sharp_depth_four_value == 13
    assert (receipt.constructive_adaptive_cost, receipt.constructive_fixed_cost) == (4, 13)
    assert receipt.restricted_cap_saturation_depth == 8


def test_eighteen_world_exhaustive_upper_counts() -> None:
    receipt = audit_exact_balanced_eighteen_world_depth_four_sharp()
    assert receipt.component_partitions_checked == 47
    assert receipt.admissible_component_size_types == ADMISSIBLE_COMPONENT_SIZE_TYPES
    assert len(ADMISSIBLE_COMPONENT_SIZE_TYPES) == 6
    assert receipt.minimum_bundle_configurations == 1222
    assert receipt.identifying_bundle_configurations == 1207
    assert receipt.collision_bundle_configurations == 15
    assert receipt.balanced_extra_cut_classes == 24310


def test_no_fourteen_query_depth_four_survivor() -> None:
    receipt = audit_exact_balanced_eighteen_world_depth_four_sharp()
    assert receipt.identifying_fixed_safe_candidates == 65864
    assert receipt.identifying_depth_four_candidates == 134
    assert receipt.identifying_singleton_depth_four_survivors == 0
    assert receipt.collision_fixed_safe_candidates == 84326
    assert receipt.collision_depth_four_candidates == 21448
    assert receipt.collision_singleton_depth_four_survivors == 0
