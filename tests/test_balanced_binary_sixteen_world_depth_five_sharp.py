from adaptive_gain.balanced_binary_sixteen_world_depth_five_sharp import (
    audit_exact_balanced_sixteen_world_depth_five_sharp,
)


def test_sixteen_world_depth_five_is_twelve() -> None:
    receipt = audit_exact_balanced_sixteen_world_depth_five_sharp()
    assert receipt.theorem_holds
    assert receipt.sharp_depth_five_value == 12
    assert (receipt.constructive_adaptive_cost, receipt.constructive_fixed_cost) == (4, 12)


def test_all_safe_cut_subsets_force_depth_seven_for_cap_thirteen() -> None:
    receipt = audit_exact_balanced_sixteen_world_depth_five_sharp()
    assert receipt.safe_external_cut_count == 3
    assert receipt.query_counts_by_safe_subset == (13, 14, 14, 15, 14, 15, 15, 16)
    assert receipt.twelve_query_subfamily_counts == (13, 91, 91, 455, 91, 455, 455, 1820)
    assert receipt.unique_witness_pair_counts == (13, 13, 28, 28, 28, 28, 43, 43)
    assert receipt.mandatory_pair_adaptive_depths == (7,) * 8
