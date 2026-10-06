import math

import pytest

from adaptive_gain.core import FiniteTask, Query, World, fixed_minimum_resolution
from adaptive_gain.bounded_arity_extremal_bounds import (
    bounded_arity_unit_cost_witness_at_depth,
)
from adaptive_gain.policy_fitness import discounted_fitness_optimal_policy
from adaptive_gain.bounded_arity_extremal_bounds import shallow_leaf_expected_value_witness
from adaptive_gain.core import fixed_minimum_resolution
from adaptive_gain.policy_fitness import discounted_fitness_optimal_policy
from adaptive_gain.evolutionary_resource_frontier import (
    binary_evolutionary_resource_corners,
    bounded_arity_evolutionary_depth_corners,
    minimum_world_count_for_fixed_burden,
    exponential_max_viable_adaptive_depth,
    exponential_required_gap,
    full_b_ary_internal_nodes,
    exponential_arity_limited_cost_ceiling,
    exponential_unrestricted_information_cost_ceiling,
    exponential_unrestricted_expected_information_cost_ceiling,
    exponential_unrestricted_expected_cost_ceiling,
    exponential_robust_expected_cost_regime,
    exponential_minimum_robust_cue_arity,
    required_fixed_cost_for_value,
    minimum_one_step_mass_for_expected_repayment,
    exponential_minimum_one_step_mass_for_expected_repayment,
    exponential_near_max_value_scaling,
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



def test_near_maximal_value_scaling_binary_witness():
    receipt = exponential_near_max_value_scaling(
        2,
        closure_rate=1e-3,
        epsilon=0.1,
    )
    assert receipt.witness_adaptive_depth == 12
    assert receipt.witness_fixed_cost == 4095
    assert receipt.witness_world_count == 4096
    assert receipt.witness_query_count == 4095
    assert receipt.witness_value_fraction >= 0.9
    assert receipt.witness_adaptive_depth >= receipt.lower_adaptive_depth
    assert receipt.witness_adaptive_depth <= receipt.upper_adaptive_depth
    assert receipt.witness_fixed_cost >= receipt.required_fixed_cost_lower


def test_near_maximal_value_scaling_is_linear_size_log_depth_order():
    epsilon = 0.1
    receipts = [
        exponential_near_max_value_scaling(
            2,
            closure_rate=mu,
            epsilon=epsilon,
        )
        for mu in (2e-3, 1e-3, 5e-4)
    ]

    # Fixed burden grows on the 1/mu scale.
    scaled_fixed = [
        r.closure_rate * r.witness_fixed_cost
        for r in receipts
    ]
    assert max(scaled_fixed) / min(scaled_fixed) < 2.1

    # Adaptive depth grows only logarithmically as the opportunity timescale doubles.
    depth_increments = [
        receipts[i + 1].witness_adaptive_depth
        - receipts[i].witness_adaptive_depth
        for i in range(len(receipts) - 1)
    ]
    assert all(0 <= step <= 2 for step in depth_increments)


def test_higher_arity_changes_constants_not_near_maximal_orders():
    rows = [
        exponential_near_max_value_scaling(
            b,
            closure_rate=1e-3,
            epsilon=0.1,
        )
        for b in (2, 3, 4)
    ]
    assert all(r.witness_value_fraction >= 0.9 for r in rows)
    assert rows[0].witness_adaptive_depth > rows[1].witness_adaptive_depth
    assert rows[1].witness_adaptive_depth >= rows[2].witness_adaptive_depth



def test_minimum_robust_cue_arity_canonical_example():
    assert exponential_minimum_robust_cue_arity(
        0.30,
        closure_rate=0.3,
        resolution_value=1.0,
    ) == 3


def test_binary_is_enough_below_binary_global_ceiling():
    assert exponential_minimum_robust_cue_arity(
        0.20,
        closure_rate=0.3,
        resolution_value=1.0,
    ) == 2


def test_no_finite_arity_above_unrestricted_information_ceiling():
    absolute = exponential_unrestricted_information_cost_ceiling(
        closure_rate=0.3,
        resolution_value=1.0,
    )
    assert exponential_minimum_robust_cue_arity(
        absolute,
        closure_rate=0.3,
        resolution_value=1.0,
    ) is None
    assert exponential_minimum_robust_cue_arity(
        absolute + 0.01,
        closure_rate=0.3,
        resolution_value=1.0,
    ) is None



def test_scalable_arity_ceiling_can_be_reentrant_in_urgency():
    kwargs = dict(
        max_arity=10,
        resolution_value=1.0,
    )
    cost = 0.97630

    values = [
        exponential_arity_limited_cost_ceiling(
            closure_rate=mu,
            **kwargs,
        )[0]
        for mu in (0.0045, 0.0048, 0.0051, 0.0060)
    ]

    assert values[0] > cost
    assert values[1] < cost
    assert values[2] > cost
    assert values[3] < cost


def test_each_fixed_depth_exponential_robust_value_is_unimodal():
    b = 10
    h = 4
    fixed = full_b_ary_internal_nodes(b, h)
    mu_star = math.log(fixed / h) / (fixed - h)

    def value(mu):
        return math.exp(-mu * h) - math.exp(-mu * fixed)

    peak = value(mu_star)
    assert value(mu_star * 0.8) < peak
    assert value(mu_star * 1.2) < peak



def test_unrestricted_expected_ceiling_exceeds_robust_ceiling():
    mu = 0.3
    robust = exponential_unrestricted_information_cost_ceiling(
        closure_rate=mu,
        resolution_value=1.0,
    )
    expected = exponential_unrestricted_expected_cost_ceiling(
        closure_rate=mu,
        resolution_value=1.0,
    )
    assert robust == pytest.approx(math.exp(-0.6))
    assert expected == pytest.approx(math.exp(-0.3))
    assert expected > robust
    assert expected / robust == pytest.approx(math.exp(mu))


def test_cost_point_six_is_expected_only_possible_at_mu_point_three():
    assert exponential_robust_expected_cost_regime(
        0.60,
        closure_rate=0.3,
        resolution_value=1.0,
    ) == "expected_only_possible"


def _skewed_expected_rescue_task():
    rare = bounded_arity_unit_cost_witness_at_depth(
        8,
        7,
        2,
        3,
    )
    common_target = rare.worlds[0].target
    worlds = (World("common", common_target),) + tuple(
        World(f"rare_{w.name}", w.target)
        for w in rare.worlds
    )

    root = Query(
        "common_vs_rare",
        1,
        (0,) + tuple(1 for _ in rare.worlds),
    )

    extended_queries = [root]
    for q in rare.queries:
        common_outcome = q.outcomes[0]
        extended_queries.append(
            Query(
                f"rare_{q.name}",
                q.cost,
                (common_outcome,) + tuple(q.outcomes),
            )
        )

    return FiniteTask(worlds, tuple(extended_queries))


def test_explicit_binary_task_has_positive_expected_value_above_robust_ceiling():
    task = _skewed_expected_rescue_task()
    fixed = fixed_minimum_resolution(task)
    assert fixed.minimum_cost == 7

    p_common = 0.99
    rare_mass = (1.0 - p_common) / 8.0
    probs = (p_common,) + tuple(rare_mass for _ in range(8))
    mu = 0.3

    adaptive = discounted_fitness_optimal_policy(
        task,
        probs,
        discount_rate=mu,
    )
    assert adaptive.selected_policy is not None

    fixed_value = math.exp(-mu * fixed.minimum_cost)
    expected_advantage = (
        adaptive.expected_discounted_completion_value
        - fixed_value
    )

    # K=0.60 lies above the unrestricted robust ceiling exp(-0.6),
    # but this finite binary task still repays it in expectation.
    assert 0.60 > math.exp(-0.6)
    assert expected_advantage > 0.60



def test_expected_global_ceiling_exceeds_robust_global_ceiling():
    mu = 0.3
    robust = exponential_unrestricted_information_cost_ceiling(
        closure_rate=mu,
        resolution_value=1.0,
    )
    expected = exponential_unrestricted_expected_information_cost_ceiling(
        closure_rate=mu,
        resolution_value=1.0,
    )
    assert robust == pytest.approx(math.exp(-0.6))
    assert expected == pytest.approx(math.exp(-0.3))
    assert expected > robust


def test_binary_frequency_skew_can_pay_cost_above_absolute_robust_ceiling():
    mu = 0.3
    cost = 0.60
    task = shallow_leaf_expected_value_witness(
        rare_depth=3,
        max_arity=2,
    )
    fixed = fixed_minimum_resolution(task)
    assert fixed.minimum_cost == 8

    probs = [0.95] + [0.05 / (len(task.worlds) - 1)] * (len(task.worlds) - 1)
    adaptive = discounted_fitness_optimal_policy(
        task,
        probs,
        discount_rate=mu,
    )
    assert adaptive.selected_policy is not None
    assert adaptive.world_path_costs is not None

    expected_advantage = (
        adaptive.expected_discounted_completion_value
        - math.exp(-mu * fixed.minimum_cost)
    )
    robust_absolute = math.exp(-2.0 * mu)

    assert expected_advantage > cost
    assert cost > robust_absolute



def test_expected_rescue_one_step_mass_threshold_canonical_value():
    threshold = exponential_minimum_one_step_mass_for_expected_repayment(
        0.60,
        closure_rate=0.3,
        resolution_value=1.0,
    )
    assert threshold == pytest.approx(0.26659691914156886)


def test_one_step_mass_threshold_has_robust_and_impossible_endpoints():
    mu = 0.3
    robust = math.exp(-2.0 * mu)
    expected = math.exp(-mu)

    assert exponential_minimum_one_step_mass_for_expected_repayment(
        robust - 0.01,
        closure_rate=mu,
    ) == pytest.approx(0.0)

    assert exponential_minimum_one_step_mass_for_expected_repayment(
        expected,
        closure_rate=mu,
    ) is None


def test_generic_one_step_mass_threshold_interpolates_linearly_in_band():
    threshold = minimum_one_step_mass_for_expected_repayment(
        0.5,
        value_at_one=0.8,
        value_at_two=0.4,
        asymptotic_value=0.1,
    )
    # robust ceiling = 0.3, expected ceiling = 0.7
    # threshold = (0.5-0.3)/(0.8-0.4) = 0.5
    assert threshold == pytest.approx(0.5)
