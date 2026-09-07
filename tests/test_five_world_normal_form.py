from fractions import Fraction

from adaptive_gain import (
    adaptive_minimum_resolution,
    routing_information_receipt,
    task_pair_antichain_bound,
)
from adaptive_gain.five_world_normal_form import (
    FIVE_WORLD_IRREDUCIBLE_STRICT_GAIN_SIGNATURE,
    FIVE_WORLD_STRICT_SIGNATURES,
    canonical_five_world_separator_signature,
    enumerate_two_plus_three_three_query_universe,
    five_world_irreducible_raw_symmetry_orbit_size,
    five_world_irreducible_standard_task,
    five_world_normal_form_receipt,
)
from adaptive_gain.minimal_normal_form import minimal_strict_gain_standard_task


def test_unique_irreducible_five_world_standard_form_is_strict_and_deletion_irreducible():
    task = five_world_irreducible_standard_task()
    receipt = five_world_normal_form_receipt(task)
    assert receipt.canonical_separator_signature == FIVE_WORLD_IRREDUCIBLE_STRICT_GAIN_SIGNATURE
    assert receipt.strict_class == "irreducible_five_world_core"
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
    assert receipt.exact_strict_gain
    assert receipt.strict_balanced_four_world_deletion_count == 0
    assert receipt.irreducible_against_majority_world_deletion
    assert receipt.matches_unique_irreducible_normal_form
    assert receipt.exact_irreducible_strict_gain
    assert receipt.strict_classification_agrees_with_exact_solver
    assert receipt.irreducible_classification_agrees_with_exact_solver


def test_irreducible_five_world_standard_form_has_positive_information_at_an_optimal_root():
    task = five_world_irreducible_standard_task()
    adaptive = adaptive_minimum_resolution(task)
    assert adaptive.minimum_worst_path_cost == 2
    assert adaptive.selected_policy is not None
    information = routing_information_receipt(task, adaptive.selected_policy)
    assert information.root_query in {"q_route_left", "q_route_right"}
    assert 0.0 < information.root_direct_target_information_bits < 0.1
    assert information.branch_dependent_next_action
    assert not information.zero_direct_information_routing_witness
    assert information.total_policy_target_information_bits > 0.9


def test_new_five_world_core_has_same_minimal_fixed_pair_kernel_as_four_world_core():
    four = task_pair_antichain_bound(minimal_strict_gain_standard_task())
    five = task_pair_antichain_bound(five_world_irreducible_standard_task())
    assert four.canonical_signatures == (1, 2, 4)
    assert five.canonical_signatures == (1, 2, 4)
    assert four.minimal_separator_antichain_size == five.minimal_separator_antichain_size == 3
    assert four.raw_cross_target_pair_count == 4
    assert five.raw_cross_target_pair_count == 6


def test_irreducible_standard_form_declared_raw_symmetry_orbit_has_288_labeled_tasks():
    assert five_world_irreducible_raw_symmetry_orbit_size() == 288


def test_complete_five_world_universe_has_one_new_irreducible_strict_orbit():
    summary = enumerate_two_plus_three_three_query_universe()
    assert summary.total_tasks == 32_768
    assert summary.unresolved_tasks == 17_928
    assert dict(summary.cost_pair_counts) == {
        "None:None": 17_928,
        "1:1": 5_768,
        "2:2": 6_336,
        "2:3": 2_016,
        "3:3": 720,
    }
    assert summary.strict_gain_tasks == 2_016
    assert dict(summary.strict_signature_counts) == {
        (7, 9, 49): 288,
        (7, 14, 54): 288,
        (7, 27, 42): 576,
        (14, 21, 45): 576,
        (7, 28, 42): 288,
    }
    assert set(dict(summary.strict_signature_counts)) == set(FIVE_WORLD_STRICT_SIGNATURES)
    assert dict(summary.strict_deletion_count_distribution) == {0: 288, 1: 1_152, 2: 576}
    assert summary.irreducible_strict_gain_tasks == 288
    assert dict(summary.irreducible_signature_counts) == {
        FIVE_WORLD_IRREDUCIBLE_STRICT_GAIN_SIGNATURE: 288
    }
    assert summary.irreducible_symmetry_orbit_count == 1
    assert summary.strict_gain_cost_pairs == ((2, 3),)
    assert summary.maximum_strict_cost_ratio == Fraction(3, 2)
    assert summary.strict_classification_disagreement_count == 0
    assert summary.irreducible_classification_disagreement_count == 0
