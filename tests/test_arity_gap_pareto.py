from math import ceil, log

import pytest

from adaptive_gain.arity_gap_pareto import (
    arity_gap_pareto_frontier,
    audit_arity_gap_pareto_point,
    full_bary_internal_capacity,
    minimum_adaptive_depth_for_gap,
    minimum_productive_frontier_edges_for_gap,
    minimum_query_count_for_gap,
    minimum_world_count_for_gap,
    unrestricted_world_gap_ceiling,
)


def test_full_bary_capacity_and_depth_examples():
    assert [full_bary_internal_capacity(h, 3) for h in range(1, 5)] == [1, 4, 13, 40]
    assert minimum_adaptive_depth_for_gap(2, 3) == 2
    assert minimum_adaptive_depth_for_gap(3, 4) == 2
    assert minimum_adaptive_depth_for_gap(5, 3) == 3


def test_minimum_world_count_is_independent_of_allowed_arity():
    # The unrestricted-arity ceiling first reaches q exactly at the binary formula.
    for q in range(1, 41):
        n_star = minimum_world_count_for_gap(q)
        assert unrestricted_world_gap_ceiling(n_star) >= q
        assert unrestricted_world_gap_ceiling(n_star - 1) < q


def test_query_and_frontier_minimum_decrease_with_higher_arity():
    q = 3
    assert minimum_query_count_for_gap(q, 2) == 6
    assert minimum_query_count_for_gap(q, 4) == 5
    assert minimum_productive_frontier_edges_for_gap(q, 4) == 5
    assert minimum_world_count_for_gap(q) == 7


def test_q3_b4_has_two_exact_pareto_points():
    frontier = arity_gap_pareto_frontier(3, 4)
    assert [
        (p.world_count, p.query_count, p.productive_frontier_edge_count, p.adaptive_depth)
        for p in frontier
    ] == [
        (8, 5, 5, 2),
        (7, 6, 6, 3),
    ]

    for point in frontier:
        audit = audit_arity_gap_pareto_point(point)
        assert audit.theorem_holds
        assert audit.direct_check_performed
        assert audit.observed_adaptive_cost == point.adaptive_depth
        assert audit.observed_fixed_cost == point.query_count
        assert audit.observed_fixed_cost - audit.observed_adaptive_cost == 3
        assert audit.observed_frontier_edge_count == point.productive_frontier_edge_count


def test_increasing_arity_can_split_one_corner_into_a_tradeoff():
    # At q=3, ternary sensing still has one componentwise minimum. Allowing
    # quaternary outcomes lowers the query/frontier minimum to five but that
    # improvement cannot coexist with the seven-world minimum, creating a
    # two-point Pareto frontier rather than a single better corner.
    ternary = arity_gap_pareto_frontier(3, 3)
    quaternary = arity_gap_pareto_frontier(3, 4)
    assert [
        (p.world_count, p.query_count, p.adaptive_depth) for p in ternary
    ] == [(7, 6, 3)]
    assert [
        (p.world_count, p.query_count, p.adaptive_depth) for p in quaternary
    ] == [(8, 5, 2), (7, 6, 3)]


def test_some_higher_arity_gaps_have_no_tradeoff_and_hit_both_minima():
    # q=2,b=3 reaches the arity-independent world minimum and the ternary
    # query/frontier minimum at the same point.
    frontier = arity_gap_pareto_frontier(2, 3)
    assert len(frontier) == 1
    point = frontier[0]
    assert (point.world_count, point.query_count, point.adaptive_depth) == (6, 4, 2)
    audit = audit_arity_gap_pareto_point(point)
    assert audit.theorem_holds


def test_q8_b3_exhibits_world_query_tradeoff():
    frontier = arity_gap_pareto_frontier(8, 3)
    assert [
        (p.world_count, p.query_count, p.adaptive_depth)
        for p in frontier
    ] == [
        (14, 11, 3),
        (13, 12, 4),
    ]


def test_routing_depth_has_log_b_two_point_bracket():
    for b in range(2, 8):
        for q in range(1, 501):
            # k is the first depth whose full b-ary internal count reaches q,
            # before paying the additive depth term in the gap requirement.
            k = ceil(log((b - 1) * q + 1, b))
            h = minimum_adaptive_depth_for_gap(q, b)
            assert h in (k, k + 1)


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        minimum_adaptive_depth_for_gap(0, 2)
    with pytest.raises(ValueError):
        minimum_adaptive_depth_for_gap(1, 1)
    with pytest.raises(ValueError):
        arity_gap_pareto_frontier(0, 3)
