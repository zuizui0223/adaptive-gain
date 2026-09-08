import pytest

from adaptive_gain.core import adaptive_gain_receipt
from adaptive_gain.extremal_routing_family import extremal_routing_task
from adaptive_gain.feedback_structural_bounds import (
    bounded_arity_gap_upper_bound,
    restoring_loop_gain_upper_bound,
    structural_phase_exclusion,
)
from adaptive_gain.feedback_loop_gain import structural_loop_gain
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def _task_max_arity(task):
    return max(len(set(query.outcomes)) for query in task.queries)


def test_minimal_repo_witness_attains_bounded_arity_gap_bound():
    task = payoff_routing_task()
    receipt = adaptive_gain_receipt(task)
    assert receipt.adaptive_cost == 2
    assert receipt.fixed_cost == 3
    assert len(task.worlds) == 4
    assert len(task.queries) == 3
    assert _task_max_arity(task) == 2

    bound = bounded_arity_gap_upper_bound(4, 3, 2, 2)
    assert bound == 1
    assert receipt.fixed_cost - receipt.adaptive_cost == bound


def test_minimal_scope_excludes_damped_oscillation_at_threshold():
    result = structural_phase_exclusion(
        4,
        3,
        2,
        2,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
        community_memory=0.5,
    )
    assert result.structural_gap_upper_bound == 1
    assert result.loop_gain_upper_bound == pytest.approx(0.125)
    assert result.oscillation_threshold == pytest.approx(0.125)
    assert not result.damped_oscillation_possible
    assert not result.strong_feedback_instability_possible

    actual = structural_loop_gain(
        routing_bypass_control(),
        payoff_routing_task(),
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    )
    assert actual == pytest.approx(result.loop_gain_upper_bound)


def test_binary_scope_can_allow_oscillation_without_allowing_instability():
    # F_2(12,3)=7, hence C_F-C_A<=7-3=4.
    assert bounded_arity_gap_upper_bound(12, 12, 3, 2) == 4
    result = structural_phase_exclusion(
        12,
        12,
        3,
        2,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
        community_memory=0.5,
    )
    assert result.loop_gain_upper_bound == pytest.approx(0.5)
    assert result.damped_oscillation_possible
    assert not result.strong_feedback_instability_possible


def test_stronger_ecological_feedback_can_make_instability_not_excluded():
    result = structural_phase_exclusion(
        12,
        12,
        3,
        2,
        lambda_cost=1.0,
        feedback_strength=-1.2,
        equilibrium_frequency=0.5,
        community_memory=0.5,
    )
    assert result.structural_gap_upper_bound == 4
    assert result.loop_gain_upper_bound == pytest.approx(1.2)
    assert result.damped_oscillation_possible
    assert result.strong_feedback_instability_possible


def test_frontier_edge_cap_can_certify_no_feedback_phase_transition():
    # With h=3 and edge cap E=3, C_F<=3 so the structural gap must be zero.
    assert bounded_arity_gap_upper_bound(
        12, 12, 3, 2, frontier_edge_cap=3
    ) == 0
    result = structural_phase_exclusion(
        12,
        12,
        3,
        2,
        lambda_cost=5.0,
        feedback_strength=-1.0,
        equilibrium_frequency=0.5,
        community_memory=0.9,
        frontier_edge_cap=3,
    )
    assert result.loop_gain_upper_bound == pytest.approx(0.0)
    assert not result.damped_oscillation_possible
    assert not result.strong_feedback_instability_possible


def test_k3_extremal_family_attains_its_scope_gap_bound():
    high = extremal_routing_task(3)
    receipt = adaptive_gain_receipt(high)
    assert receipt.adaptive_cost == 2
    assert receipt.fixed_cost == 4
    n = len(high.worlds)
    m = len(high.queries)
    b = _task_max_arity(high)
    assert (n, m, b) == (6, 4, 3)
    assert bounded_arity_gap_upper_bound(n, m, 2, b) == 2


def test_loop_gain_upper_bound_scales_with_feedback_and_response():
    base = restoring_loop_gain_upper_bound(
        12,
        12,
        3,
        2,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    )
    doubled_lambda = restoring_loop_gain_upper_bound(
        12,
        12,
        3,
        2,
        lambda_cost=2.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    )
    off_center = restoring_loop_gain_upper_bound(
        12,
        12,
        3,
        2,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.2,
    )
    assert doubled_lambda == pytest.approx(2.0 * base)
    assert off_center < base


def test_infeasible_or_nonrestoring_inputs_raise():
    with pytest.raises(ValueError):
        bounded_arity_gap_upper_bound(
            12, 12, 3, 2, frontier_edge_cap=2
        )
    with pytest.raises(ValueError):
        restoring_loop_gain_upper_bound(
            4,
            3,
            2,
            2,
            lambda_cost=1.0,
            feedback_strength=0.1,
            equilibrium_frequency=0.5,
        )
