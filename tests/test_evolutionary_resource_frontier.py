import math

import pytest

from adaptive_gain.evolutionary_resource_frontier import (
    binary_evolutionary_resource_corners,
    bounded_arity_evolutionary_depth_corners,
    minimum_world_count_for_fixed_burden,
    exponential_max_viable_adaptive_depth,
    exponential_required_gap,
    full_b_ary_internal_nodes,
    exponential_arity_limited_cost_ceiling,
    exponential_unrestricted_information_cost_ceiling,
    required_fixed_cost_for_value,
)


def test_linear_value_recovers_depth_independent_gap():
    lam = 0.4
    cost = 0.9
    expected_gap = math.floor(cost / lam) + 1
    for h in range(1, 6):
        required = required_fixed_cost_for_value(
            h,
            cost,
            lambda c: -lam * c,
            search_limit=h + 20,
        )
        assert required == h + expected_gap


def test_exponential_closed_form_matches_direct_search():
    mu = 0.3
    value = 1.0
    cost = 0.1
    for h in range(1, 6):
        closed = exponential_required_gap(
            h,
            cost,
            closure_rate=mu,
            resolution_value=value,
        )
        direct = required_fixed_cost_for_value(
            h,
            cost,
            lambda c: value * math.exp(-mu * c),
            search_limit=100,
        )
        if closed is None:
            assert direct is None
        else:
            assert direct == h + closed


def test_exponential_required_gap_grows_with_late_depth_before_inviability():
    mu = 0.3
    cost = 0.1
    gaps = [
        exponential_required_gap(h, cost, closure_rate=mu)
        for h in range(1, 6)
    ]
    finite = [g for g in gaps if g is not None]
    assert finite == sorted(finite)


def test_exponential_max_viable_depth_is_exact():
    mu = 0.3
    cost = 0.1
    hmax = exponential_max_viable_adaptive_depth(
        cost,
        closure_rate=mu,
        resolution_value=1.0,
    )
    assert hmax is not None
    assert cost < math.exp(-mu * hmax)
    assert cost >= math.exp(-mu * (hmax + 1))


def test_binary_natural_history_corner_is_exact_minimum_by_depth():
    corners = binary_evolutionary_resource_corners(
        max_adaptive_depth=8,
        architecture_cost=0.1,
        completion_value=lambda c: math.exp(-0.3 * c),
    )
    assert corners
    for row in corners:
        assert row.minimum_world_count == row.required_fixed_cost + 1
        assert row.minimum_query_count == row.required_fixed_cost
        assert row.required_fixed_cost <= (1 << row.adaptive_depth) - 1


def test_unviable_depth_returns_none_even_with_unlimited_fixed_cost():
    assert exponential_required_gap(
        10,
        0.1,
        closure_rate=0.3,
        resolution_value=1.0,
    ) is None


def test_zero_cost_has_no_finite_maximum_viable_depth():
    assert exponential_max_viable_adaptive_depth(
        0.0,
        closure_rate=0.3,
        resolution_value=1.0,
    ) is None



def test_full_b_ary_internal_node_formula():
    assert full_b_ary_internal_nodes(2, 4) == 15
    assert full_b_ary_internal_nodes(3, 3) == 13
    assert full_b_ary_internal_nodes(4, 2) == 5


def test_binary_global_cost_ceiling_at_mu_point_three():
    ceiling, depths = exponential_arity_limited_cost_ceiling(
        2,
        closure_rate=0.3,
        resolution_value=1.0,
    )
    assert ceiling == pytest.approx(0.2900852153739598)
    assert depths == (4,)


def test_arity_limited_cost_ceiling_is_nondecreasing_in_arity():
    ceilings = [
        exponential_arity_limited_cost_ceiling(
            b,
            closure_rate=0.3,
            resolution_value=1.0,
        )[0]
        for b in range(2, 7)
    ]
    assert ceilings == sorted(ceilings)


def test_unrestricted_information_ceiling_is_exp_minus_two_mu():
    ceiling = exponential_unrestricted_information_cost_ceiling(
        closure_rate=0.3,
        resolution_value=1.0,
    )
    assert ceiling == pytest.approx(math.exp(-0.6))


def test_binary_no_go_cost_point_three_is_above_global_binary_ceiling():
    ceiling, _ = exponential_arity_limited_cost_ceiling(
        2,
        closure_rate=0.3,
    )
    assert 0.30 > ceiling



def test_canonical_binary_resource_corner_mu_point_three_cost_point_two_five():
    corners = binary_evolutionary_resource_corners(
        max_adaptive_depth=8,
        architecture_cost=0.25,
        completion_value=lambda c: math.exp(-0.3 * c),
    )
    assert corners == (
        type(corners[0])(
            adaptive_depth=3,
            required_fixed_cost=7,
            required_gap=4,
            minimum_world_count=8,
            minimum_query_count=7,
        ),
    )



def test_binary_arity_ceiling_approaches_full_value_under_low_urgency():
    ceiling, _ = exponential_arity_limited_cost_ceiling(
        2,
        closure_rate=1e-3,
        resolution_value=1.0,
    )
    assert ceiling > 0.98


def test_binary_arity_ceiling_vanishes_under_high_urgency():
    ceiling, _ = exponential_arity_limited_cost_ceiling(
        2,
        closure_rate=10.0,
        resolution_value=1.0,
    )
    assert ceiling < 1e-8



def test_minimum_world_count_for_declared_burden_depends_on_arity_and_depth():
    assert minimum_world_count_for_fixed_burden(7, 3, 2) == 8
    assert minimum_world_count_for_fixed_burden(7, 3, 3) == 8
    assert minimum_world_count_for_fixed_burden(5, 2, 4) == 8
    assert minimum_world_count_for_fixed_burden(5, 2, 3) is None


def test_higher_arity_can_make_shallower_evolutionary_corner_feasible():
    kwargs = dict(
        max_adaptive_depth=6,
        architecture_cost=0.25,
        completion_value=lambda c: math.exp(-0.3 * c),
    )
    binary = bounded_arity_evolutionary_depth_corners(
        max_arity=2,
        **kwargs,
    )
    ternary = bounded_arity_evolutionary_depth_corners(
        max_arity=3,
        **kwargs,
    )
    quaternary = bounded_arity_evolutionary_depth_corners(
        max_arity=4,
        **kwargs,
    )

    assert binary[0].adaptive_depth == 3
    assert binary[0].minimum_world_count == 8
    assert binary[0].minimum_query_count == 7

    assert ternary[0].adaptive_depth == 3
    assert ternary[0].minimum_world_count == 8
    assert ternary[0].minimum_query_count == 7

    assert quaternary[0].adaptive_depth == 2
    assert quaternary[0].minimum_world_count == 8
    assert quaternary[0].minimum_query_count == 5
