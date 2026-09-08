from adaptive_gain.balanced_binary_twenty_two_world_depth_five_upper import (
    CF18_PRIVATE_COMPONENT_TYPES,
    audit_exact_balanced_twenty_two_world_depth_five_upper,
)


def test_twenty_two_world_depth_five_sharp_receipt() -> None:
    receipt = audit_exact_balanced_twenty_two_world_depth_five_upper()
    assert receipt.theorem_holds
    assert receipt.world_count == 22
    assert receipt.certified_upper_bound == 17
    assert receipt.sharp_depth_five_value == 17
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
    assert receipt.cf18_identifying_matrices == 4725
    assert receipt.cf18_collision_matrices == 17


def test_cf18_identifying_basis_exchange_is_empty() -> None:
    receipt = audit_exact_balanced_twenty_two_world_depth_five_upper()
    assert receipt.identifying_individual_safe_depth_five_survivors == 96
    assert receipt.identifying_pairwise_root_survivors == 22
    assert receipt.identifying_maximal_pairwise_safe_survivors == 0


def test_cf18_collision_basis_exchange_is_empty() -> None:
    receipt = audit_exact_balanced_twenty_two_world_depth_five_upper()
    assert receipt.collision_isomorphism_classes == 2
    assert receipt.collision_large_class_size == 16
    assert receipt.collision_large_class_safe_external_cuts == 87519
    assert receipt.collision_external_orbits == 37
    assert receipt.collision_universal_external_cuts == 5
    assert receipt.collision_nonuniversal_orbits == 32
    assert receipt.collision_maximal_pairwise_safe_cliques_checked == 25512
    assert receipt.collision_depth_five_survivors == 0
