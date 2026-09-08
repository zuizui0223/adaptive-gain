from fractions import Fraction

from adaptive_gain.balanced_binary_small_scope import (
    canonical_exact_balanced_query_masks,
    classify_exact_balanced_world_count,
    exact_balanced_eight_world_five_query_task,
    exact_balanced_first_above_three_halves_audit,
    target_multiplicity_profiles,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution


def test_symmetry_reduced_balanced_partition_counts():
    assert len(canonical_exact_balanced_query_masks(4)) == 3
    assert len(canonical_exact_balanced_query_masks(6)) == 10
    assert len(target_multiplicity_profiles(4)) == 4
    assert len(target_multiplicity_profiles(6)) == 10


def test_complete_four_world_exact_balance_scope_has_no_gain():
    receipt = classify_exact_balanced_world_count(4)
    assert receipt.theorem_holds
    assert receipt.balanced_partition_classes == 3
    assert receipt.target_multiplicity_profiles == 4
    assert receipt.representative_query_families == 28
    assert receipt.maximum_ratio == Fraction(1, 1)


def test_complete_six_world_exact_balance_scope_caps_ratio_at_three_halves():
    receipt = classify_exact_balanced_world_count(6)
    assert receipt.theorem_holds
    assert receipt.balanced_partition_classes == 10
    assert receipt.target_multiplicity_profiles == 10
    assert receipt.representative_query_families == 10_230
    assert receipt.resolved_representatives == 9_184
    assert receipt.maximum_ratio == Fraction(3, 2)
    assert (2, 3) in receipt.maximizing_cost_pairs


def test_eight_world_five_query_exact_balance_witness_is_five_over_three():
    task = exact_balanced_eight_world_five_query_task()
    assert len(task.worlds) == 8
    assert len(task.queries) == 5
    for query in task.queries:
        assert set(query.outcomes) <= {0, 1}
        assert sum(value == 0 for value in query.outcomes) == 4
        assert sum(value == 1 for value in query.outcomes) == 4
    assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 3
    assert fixed_minimum_resolution(task).minimum_cost == 5


def test_first_exact_balanced_scope_above_three_halves_is_8_worlds_5_queries():
    receipt = exact_balanced_first_above_three_halves_audit()
    assert receipt.theorem_holds
    assert receipt.world_count == 8
    assert receipt.query_count == 5
    assert receipt.adaptive_cost == 3
    assert receipt.fixed_cost == 5
    assert receipt.ratio == Fraction(5, 3)
    assert receipt.all_queries_exactly_balanced
    assert receipt.private_pair_for_every_query
    assert receipt.smaller_even_world_counts_at_most_three_halves
    assert receipt.fewer_than_five_queries_at_most_three_halves
