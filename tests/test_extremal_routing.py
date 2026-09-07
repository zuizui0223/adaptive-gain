from fractions import Fraction

import pytest

from adaptive_gain.extremal_routing import (
    depth_two_fixed_cost_world_bound,
    extremal_routing_receipt,
    k_branch_routing_task,
    ratio_above_three_halves_minimality,
)
from adaptive_gain.minimal_normal_form import (
    MINIMAL_STRICT_GAIN_SIGNATURE,
    canonical_minimal_separator_signature,
)


def test_k2_is_the_existing_unique_minimal_strict_gain_normal_form():
    task = k_branch_routing_task(2)
    assert canonical_minimal_separator_signature(task) == MINIMAL_STRICT_GAIN_SIGNATURE
    receipt = extremal_routing_receipt(2)
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
    assert receipt.fixed_to_adaptive_ratio == Fraction(3, 2)


def test_k3_is_first_constructed_ratio_above_three_halves_scope():
    receipt = extremal_routing_receipt(3)
    assert receipt.world_count == 6
    assert receipt.query_count == 4
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 4)
    assert receipt.adaptive_gain == 2
    assert receipt.fixed_to_adaptive_ratio == 2
    assert receipt.saturates_depth_two_world_bound

    minimal = ratio_above_three_halves_minimality()
    assert minimal.no_task_with_at_most_three_queries_can_exceed
    assert minimal.no_task_with_at_most_five_worlds_can_exceed
    assert minimal.first_scope_certified
    assert minimal.witness_ratio == 2


def test_extremal_family_exact_formulas_and_singleton_frontier():
    for k in range(2, 9):
        receipt = extremal_routing_receipt(k)
        assert receipt.world_count == 2 * k
        assert receipt.query_count == k + 1
        assert receipt.adaptive_cost == 2
        assert receipt.fixed_cost == k + 1
        assert receipt.adaptive_gain == k - 1
        assert receipt.fixed_to_adaptive_ratio == Fraction(k + 1, 2)
        assert receipt.depth_two_world_bound == k + 1
        assert receipt.saturates_depth_two_world_bound
        assert receipt.minimal_productive_sets == tuple(1 << q for q in range(k + 1))
        assert receipt.singleton_frontier_query_names == (
            "router",
            *(f"terminal_{i}" for i in range(1, k + 1)),
        )


def test_depth_two_world_bound_values():
    assert depth_two_fixed_cost_world_bound(1) == 1
    assert depth_two_fixed_cost_world_bound(4) == 3
    assert depth_two_fixed_cost_world_bound(5) == 3
    assert depth_two_fixed_cost_world_bound(6) == 4


@pytest.mark.parametrize("bad", [0, 1, -1, 2.0, None])
def test_extremal_family_rejects_invalid_branch_count(bad):
    with pytest.raises(ValueError):
        k_branch_routing_task(bad)


@pytest.mark.parametrize("bad", [0, -1, 3.5, None])
def test_depth_two_bound_rejects_invalid_world_count(bad):
    with pytest.raises(ValueError):
        depth_two_fixed_cost_world_bound(bad)
