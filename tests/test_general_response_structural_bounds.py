import pytest

from adaptive_gain.general_response_structural_bounds import (
    general_structural_phase_exclusion,
    generalized_gain_per_structural_gap,
    generalized_structural_gain_upper_bound,
)


def test_parent_haploid_scope_recovers_parent_phase_exclusion():
    # Parent centered witness has e=eta*p*(1-p)=-0.125.
    result = general_structural_phase_exclusion(
        4,
        3,
        2,
        2,
        evolutionary_persistence=1.0,
        community_memory=0.5,
        lambda_cost=1.0,
        selection_responsiveness=1.0,
        ecological_feedback_slope=-0.125,
    )
    assert result.structural_gap_upper_bound == 1
    assert result.generalized_gain_per_gap == pytest.approx(0.125)
    assert result.generalized_gain_upper_bound == pytest.approx(0.125)
    assert result.lower_stability_gain == pytest.approx(0.0)
    assert result.oscillation_gain == pytest.approx(0.125)
    assert result.upper_stability_gain == pytest.approx(1.0)
    assert not result.damped_oscillation_possible
    assert not result.upper_instability_possible


def test_same_structural_scope_can_allow_damping_under_intrinsic_evolutionary_decay():
    # Keep the same structural and per-gap gain ceiling, but alpha=0.7 changes
    # the response geometry.  G_osc=(.7-.5)^2/[4*.5]=.02.
    result = general_structural_phase_exclusion(
        4,
        3,
        2,
        2,
        evolutionary_persistence=0.7,
        community_memory=0.5,
        lambda_cost=1.0,
        selection_responsiveness=1.0,
        ecological_feedback_slope=-0.125,
    )
    assert result.generalized_gain_upper_bound == pytest.approx(0.125)
    assert result.oscillation_gain == pytest.approx(0.02)
    assert result.damped_oscillation_possible
    assert not result.upper_instability_possible


def test_medium_scope_allows_damping_but_excludes_upper_instability():
    # Gap upper bound is 4. With per-gap gain .125, Gmax=.5.
    result = general_structural_phase_exclusion(
        12,
        12,
        3,
        2,
        evolutionary_persistence=0.8,
        community_memory=0.5,
        lambda_cost=1.0,
        selection_responsiveness=1.0,
        ecological_feedback_slope=-0.125,
    )
    assert result.structural_gap_upper_bound == 4
    assert result.generalized_gain_upper_bound == pytest.approx(0.5)
    assert result.oscillation_gain == pytest.approx(0.045)
    assert result.upper_stability_gain == pytest.approx(1.2)
    assert result.damped_oscillation_possible
    assert not result.upper_instability_possible


def test_stronger_response_can_make_upper_instability_not_excluded():
    result = general_structural_phase_exclusion(
        12,
        12,
        3,
        2,
        evolutionary_persistence=0.8,
        community_memory=0.5,
        lambda_cost=1.0,
        selection_responsiveness=1.0,
        ecological_feedback_slope=-0.4,
    )
    assert result.generalized_gain_upper_bound == pytest.approx(1.6)
    assert result.upper_stability_gain == pytest.approx(1.2)
    assert result.upper_instability_possible


def test_frontier_edge_cap_eliminates_generalized_structural_gain():
    result = general_structural_phase_exclusion(
        12,
        12,
        3,
        2,
        evolutionary_persistence=0.8,
        community_memory=0.9,
        lambda_cost=5.0,
        selection_responsiveness=2.0,
        ecological_feedback_slope=-0.5,
        frontier_edge_cap=3,
    )
    assert result.structural_gap_upper_bound == 0
    assert result.generalized_gain_upper_bound == pytest.approx(0.0)
    assert not result.damped_oscillation_possible
    assert not result.upper_instability_possible


def test_gain_per_gap_factorization():
    value = generalized_gain_per_structural_gap(
        lambda_cost=2.0,
        selection_responsiveness=0.5,
        ecological_feedback_slope=-0.3,
    )
    assert value == pytest.approx(0.3)
    upper = generalized_structural_gain_upper_bound(
        12,
        12,
        3,
        2,
        lambda_cost=2.0,
        selection_responsiveness=0.5,
        ecological_feedback_slope=-0.3,
    )
    assert upper == pytest.approx(1.2)


def test_nonrestoring_structural_bound_inputs_are_rejected():
    with pytest.raises(ValueError):
        generalized_gain_per_structural_gap(
            lambda_cost=1.0,
            selection_responsiveness=1.0,
            ecological_feedback_slope=0.1,
        )
