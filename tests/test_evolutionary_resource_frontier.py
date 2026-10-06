import math

import pytest

from adaptive_gain.evolutionary_resource_frontier import (
    binary_evolutionary_resource_corners,
    exponential_max_viable_adaptive_depth,
    exponential_required_gap,
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
