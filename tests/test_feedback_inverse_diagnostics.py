import pytest

from adaptive_gain.endogenous_community_feedback import structural_feedback_equilibrium
from adaptive_gain.feedback_inverse_diagnostics import (
    full_damped_inverse_diagnostic,
    infer_feedback_from_damping_and_period,
    infer_feedback_from_eigenvalues,
    infer_structural_gap_from_loop_gain,
    structural_scope_compatibility,
)
from adaptive_gain.feedback_loop_gain import damping_time_from_loop_gain
from adaptive_gain.feedback_transient_bounds import damped_period_from_loop_gain
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def test_damped_observables_recover_known_loop_gain_and_memory():
    phi = 0.8
    L = 0.125
    tau = damping_time_from_loop_gain(L, phi)
    period = damped_period_from_loop_gain(L, phi)
    inferred = infer_feedback_from_damping_and_period(tau, period)
    assert inferred.community_memory == pytest.approx(phi, abs=1e-12)
    assert inferred.loop_gain == pytest.approx(L, abs=1e-12)
    assert inferred.damping_time == pytest.approx(tau)
    assert inferred.oscillation_period == pytest.approx(period)


def test_repo_native_eigenvalues_recover_feedback_parameters():
    eq = structural_feedback_equilibrium(
        routing_bypass_control(),
        payoff_routing_task(),
        lambda_cost=1.0,
        control_cost=0.5,
        q_base=0.5,
        feedback_strength=-0.5,
        community_memory=0.8,
    )
    assert eq.eigenvalues is not None
    inferred = infer_feedback_from_eigenvalues(*eq.eigenvalues)
    assert inferred.community_memory == pytest.approx(0.8)
    assert inferred.loop_gain == pytest.approx(0.125)
    assert inferred.spectral_radius is not None
    assert inferred.damping_time is not None
    assert inferred.oscillation_period is not None


def test_loop_gain_recovers_repo_native_integer_structural_gap():
    gap = infer_structural_gap_from_loop_gain(
        0.125,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    )
    assert gap.gain_per_structural_gap == pytest.approx(0.125)
    assert gap.inferred_gap == pytest.approx(1.0)
    assert gap.nearest_integer_gap == 1
    assert gap.distance_to_nearest_integer == pytest.approx(0.0)
    assert gap.unit_cost_integer_compatible


def test_noninteger_inferred_gap_is_flagged_under_unit_cost_model():
    gap = infer_structural_gap_from_loop_gain(
        0.12875,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
        integer_tolerance=1e-3,
    )
    assert gap.inferred_gap == pytest.approx(1.03)
    assert gap.nearest_integer_gap == 1
    assert gap.distance_to_nearest_integer == pytest.approx(0.03)
    assert not gap.unit_cost_integer_compatible


def test_structural_scope_can_accept_or_reject_same_inferred_gap():
    # Gap 4 is too large for the minimal (4,3,2,h=2) scope but fits beneath
    # the inherited upper bound in the larger (12,12,2,h=3) scope.
    minimal = structural_scope_compatibility(4.0, 4, 3, 2, 2)
    larger = structural_scope_compatibility(4.0, 12, 12, 3, 2)
    assert minimal.structural_gap_upper_bound == 1
    assert not minimal.compatible_with_scope
    assert larger.structural_gap_upper_bound == 4
    assert larger.compatible_with_scope


def test_frontier_edge_cap_can_falsify_otherwise_compatible_gap():
    unconstrained = structural_scope_compatibility(2.0, 12, 12, 3, 2)
    constrained = structural_scope_compatibility(
        2.0,
        12,
        12,
        3,
        2,
        frontier_edge_cap=3,
    )
    assert unconstrained.compatible_with_scope
    assert constrained.structural_gap_upper_bound == 0
    assert not constrained.compatible_with_scope


def test_full_inverse_diagnostic_closes_observation_to_structure_loop():
    phi = 0.8
    L = 0.125
    tau = damping_time_from_loop_gain(L, phi)
    period = damped_period_from_loop_gain(L, phi)
    feedback, gap, scope = full_damped_inverse_diagnostic(
        tau,
        period,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
        world_count=4,
        query_count=3,
        adaptive_cost=2,
        max_arity=2,
    )
    assert feedback.community_memory == pytest.approx(0.8)
    assert feedback.loop_gain == pytest.approx(0.125)
    assert gap.inferred_gap == pytest.approx(1.0)
    assert gap.unit_cost_integer_compatible
    assert scope.structural_gap_upper_bound == 1
    assert scope.compatible_with_scope


def test_round_trip_across_damped_parameter_grid():
    for phi in (0.0, 0.2, 0.5, 0.8, 0.95):
        threshold = (1.0 - phi) / 4.0
        for L in (
            threshold + 0.1 * (1.0 - threshold),
            threshold + 0.5 * (1.0 - threshold),
            threshold + 0.9 * (1.0 - threshold),
        ):
            tau = damping_time_from_loop_gain(L, phi)
            period = damped_period_from_loop_gain(L, phi)
            inferred = infer_feedback_from_damping_and_period(tau, period)
            assert inferred.community_memory == pytest.approx(phi, abs=2e-12)
            assert inferred.loop_gain == pytest.approx(L, abs=2e-12)


def test_invalid_observables_and_scalings_raise():
    with pytest.raises(ValueError):
        infer_feedback_from_damping_and_period(-1.0, 10.0)
    with pytest.raises(ValueError):
        infer_feedback_from_damping_and_period(10.0, 1.0)
    with pytest.raises(ValueError):
        infer_structural_gap_from_loop_gain(
            0.2,
            lambda_cost=0.0,
            feedback_strength=-0.5,
            equilibrium_frequency=0.5,
        )
    with pytest.raises(ValueError):
        structural_scope_compatibility(-1.0, 4, 3, 2, 2)
