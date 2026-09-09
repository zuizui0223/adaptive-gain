from math import ceil, log2

import pytest

from adaptive_gain.binary_oscillation_scope_formula import (
    binary_gap_capacity_at_depth,
    binary_gap_corner_audit,
    binary_scope_formula_matches_bounded_arity_ceiling,
    first_binary_scope_for_stable_oscillation,
    first_binary_scope_for_structural_gap,
    minimum_binary_adaptive_depth_for_gap,
)


def test_gap_capacity_sequence():
    # 2^h - 1 - h for h=1..6.
    assert [binary_gap_capacity_at_depth(h) for h in range(1, 7)] == [0, 1, 4, 11, 26, 57]


def test_first_scope_for_small_required_gaps():
    expected = {
        1: (2, 4, 3, 3),
        2: (3, 6, 5, 5),
        3: (3, 7, 6, 6),
        4: (3, 8, 7, 7),
        5: (4, 10, 9, 9),
        11: (4, 16, 15, 15),
        12: (5, 18, 17, 17),
    }
    for q, (h, n, m, e) in expected.items():
        receipt = first_binary_scope_for_structural_gap(q)
        assert receipt.minimum_adaptive_depth == h
        assert receipt.minimum_world_count == n
        assert receipt.minimum_query_count == m
        assert receipt.minimum_productive_frontier_edge_count == e
        assert binary_scope_formula_matches_bounded_arity_ceiling(q)


def test_minimum_depth_is_exact_not_just_sufficient():
    for q in range(1, 101):
        h = minimum_binary_adaptive_depth_for_gap(q)
        assert binary_gap_capacity_at_depth(h) >= q
        if h > 1:
            assert binary_gap_capacity_at_depth(h - 1) < q


def test_logarithmic_routing_overhead_has_two_point_bracket():
    for q in range(1, 1001):
        k = ceil(log2(q + 1))
        h = minimum_binary_adaptive_depth_for_gap(q)
        assert h in (k, k + 1)


def test_constructive_corner_directly_attains_theorem_for_solver_sized_gaps():
    # These corners stay below the exact solver's 20-query cap.
    for q in (1, 2, 3, 4, 5, 11):
        audit = binary_gap_corner_audit(q)
        assert audit.theorem_holds
        assert audit.direct_check_performed
        assert audit.observed_adaptive_cost == audit.expected_adaptive_cost
        assert audit.observed_fixed_cost == audit.expected_fixed_cost
        assert audit.observed_fixed_cost - audit.observed_adaptive_cost == q
        assert audit.observed_frontier_edge_count == audit.expected_query_count


def test_large_corner_remains_constructive_without_forcing_exponential_solver():
    audit = binary_gap_corner_audit(26)
    assert audit.theorem_holds
    assert not audit.direct_check_performed
    assert audit.expected_adaptive_cost == 5
    assert audit.expected_fixed_cost == 31
    assert audit.expected_world_count == 32


def test_canonical_response_geometry_recovers_six_five_five_corner():
    receipt = first_binary_scope_for_stable_oscillation(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        gain_per_structural_gap=0.125,
    )
    assert receipt.stable_integer_oscillation_possible
    assert receipt.minimum_oscillatory_gap == 2
    assert receipt.maximum_stable_gap == 7
    scope = receipt.minimum_binary_scope
    assert scope is not None
    assert scope.minimum_adaptive_depth == 3
    assert scope.minimum_world_count == 6
    assert scope.minimum_query_count == 5
    assert scope.minimum_productive_frontier_edge_count == 5


def test_response_geometry_can_require_only_gap_one():
    receipt = first_binary_scope_for_stable_oscillation(
        evolutionary_persistence=0.8,
        community_memory=0.5,
        gain_per_structural_gap=0.125,
    )
    assert receipt.minimum_oscillatory_gap == 1
    assert receipt.stable_integer_oscillation_possible
    scope = receipt.minimum_binary_scope
    assert scope is not None
    assert (scope.minimum_adaptive_depth, scope.minimum_world_count) == (2, 4)
    assert (scope.minimum_query_count, scope.minimum_productive_frontier_edge_count) == (3, 3)


def test_integer_ladder_can_skip_stable_oscillation_entirely():
    # alpha=1, phi=1/2 gives G_osc=1/8 and G_+=1. With a=1.1,
    # the first oscillatory integer gap is 1 but that same gap is already unstable.
    receipt = first_binary_scope_for_stable_oscillation(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        gain_per_structural_gap=1.1,
    )
    assert receipt.minimum_oscillatory_gap == 1
    assert receipt.maximum_stable_gap == 0
    assert not receipt.stable_integer_oscillation_possible
    assert receipt.minimum_binary_scope is None


def test_invalid_required_gap_is_rejected():
    with pytest.raises(ValueError):
        first_binary_scope_for_structural_gap(0)
    with pytest.raises(ValueError):
        minimum_binary_adaptive_depth_for_gap(-1)
