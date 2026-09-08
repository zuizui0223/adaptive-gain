from adaptive_gain.balanced_binary_twenty_two_world_depth_five_upper import (
    CF18_PRIVATE_COMPONENT_TYPES,
    audit_exact_balanced_twenty_two_world_depth_five_upper,
)


def test_twenty_two_world_depth_five_upper_receipt() -> None:
    receipt = audit_exact_balanced_twenty_two_world_depth_five_upper()
    assert receipt.theorem_holds
    assert receipt.world_count == 22
    assert receipt.certified_upper_bound == 18
    assert receipt.fixed_cost_cap == 19
    assert receipt.cap19_identity_safe_external_cuts == 3
    assert receipt.cap19_safe_external_subsets_checked == 8
    assert receipt.cap19_depth_five_survivors == 0


def test_cf18_private_pair_barrier() -> None:
    receipt = audit_exact_balanced_twenty_two_world_depth_five_upper()
    assert receipt.cf18_private_component_types == CF18_PRIVATE_COMPONENT_TYPES
    assert len(CF18_PRIVATE_COMPONENT_TYPES) == 8
    assert receipt.cf18_private_forest_forms == 60
    assert receipt.cf18_private_query_matrices == 4742
    assert receipt.cf18_private_depth_five_hits == 0
