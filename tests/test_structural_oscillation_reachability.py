import pytest

from adaptive_gain.structural_oscillation_reachability import (
    bounded_arity_gap_ceiling_over_adaptive_depth,
    first_binary_oscillation_scope_receipt,
    maximum_integer_gap_for_stable_response,
    minimum_integer_gap_for_oscillation,
)


def test_canonical_integer_gap_window():
    assert minimum_integer_gap_for_oscillation(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        gain_per_structural_gap=0.125,
    ) == 2
    assert maximum_integer_gap_for_stable_response(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        gain_per_structural_gap=0.125,
    ) == 7


def test_strict_integer_boundaries_remain_excluded_at_equality():
    # alpha=1, phi=0.2 gives G_osc=0.2 and G_+=1.  With a=0.1,
    # gap 2 lies exactly on the oscillation boundary and gap 10 lies exactly on
    # the upper stability boundary, so the strict integer window is 3..9.
    assert minimum_integer_gap_for_oscillation(
        evolutionary_persistence=1.0,
        community_memory=0.2,
        gain_per_structural_gap=0.1,
    ) == 3
    assert maximum_integer_gap_for_stable_response(
        evolutionary_persistence=1.0,
        community_memory=0.2,
        gain_per_structural_gap=0.1,
    ) == 9


def test_general_response_geometry_can_lower_required_structural_gap():
    # alpha=0.8, phi=0.5 gives G_osc=0.045, so one structural-gap unit
    # already crosses the complex-eigenvalue threshold when a=1/8.
    assert minimum_integer_gap_for_oscillation(
        evolutionary_persistence=0.8,
        community_memory=0.5,
        gain_per_structural_gap=0.125,
    ) == 1


def test_binary_structural_gap_ceiling_excludes_smaller_scopes():
    # Any binary task on at most five worlds has inherited gap ceiling <=1.
    assert bounded_arity_gap_ceiling_over_adaptive_depth(5, 20, 2) == 1
    # Once binary trees are saturated, four declared queries still cap gap at 1.
    assert bounded_arity_gap_ceiling_over_adaptive_depth(16, 4, 2) == 1
    # A productive-frontier edge cap of four also caps binary gap at one.
    assert bounded_arity_gap_ceiling_over_adaptive_depth(
        16,
        16,
        2,
        frontier_edge_cap=4,
    ) == 1
    # Six worlds and five binary queries are the first joint scope with ceiling 2.
    assert bounded_arity_gap_ceiling_over_adaptive_depth(6, 5, 2) == 2
    assert bounded_arity_gap_ceiling_over_adaptive_depth(
        6,
        5,
        2,
        frontier_edge_cap=5,
    ) == 2


def test_first_binary_oscillation_scope_is_exact_constructive_witness():
    receipt = first_binary_oscillation_scope_receipt()
    assert receipt.theorem_holds
    assert receipt.minimum_oscillatory_gap == 2
    assert receipt.maximum_stable_gap == 7
    assert receipt.binary_worlds_below_threshold == 5
    assert receipt.binary_queries_below_threshold == 4
    assert receipt.binary_frontier_edges_below_threshold == 4
    assert (receipt.witness_world_count, receipt.witness_query_count) == (6, 5)
    assert receipt.witness_max_arity == 2
    assert receipt.witness_frontier_edge_count == 5
    assert receipt.witness_adaptive_cost == 3
    assert receipt.witness_fixed_cost == 5
    assert receipt.witness_gap == 2
    assert receipt.witness_generalized_gain == pytest.approx(0.25)
    assert receipt.witness_stable
    assert receipt.witness_oscillatory


def test_invalid_gain_per_gap_is_rejected():
    with pytest.raises(ValueError):
        minimum_integer_gap_for_oscillation(
            evolutionary_persistence=1.0,
            community_memory=0.5,
            gain_per_structural_gap=0.0,
        )
