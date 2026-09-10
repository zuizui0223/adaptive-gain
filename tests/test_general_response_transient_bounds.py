import pytest

from adaptive_gain.general_evolutionary_response import general_response_thresholds
from adaptive_gain.general_response_transient_bounds import (
    general_structural_transient_ceiling,
    generalized_damped_damping_time,
    generalized_damped_period,
    largest_generalized_stable_integer_gap,
    smallest_generalized_damped_integer_gap,
)


def test_parent_haploid_transient_envelope_is_recovered():
    # alpha=1, phi=.5, gain/gap=.125: parent thresholds Gosc=.125, Gplus=1.
    minimal = general_structural_transient_ceiling(
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
    assert minimal.structural_gap_upper_bound == 1
    assert minimal.minimum_damped_gap is None
    assert not minimal.damped_phase_structurally_possible

    medium = general_structural_transient_ceiling(
        12,
        12,
        3,
        2,
        evolutionary_persistence=1.0,
        community_memory=0.5,
        lambda_cost=1.0,
        selection_responsiveness=1.0,
        ecological_feedback_slope=-0.125,
    )
    assert medium.structural_gap_upper_bound == 4
    assert medium.minimum_damped_gap == 2
    assert medium.maximum_stable_gap == 4
    assert medium.minimum_damped_gain == pytest.approx(0.25)
    assert medium.maximum_stable_gain == pytest.approx(0.5)
    assert medium.damping_time_upper_bound == pytest.approx(6.952118993564411)
    assert medium.oscillation_period_upper_bound == pytest.approx(19.528125814614466)


def test_general_response_changes_integer_damped_envelope_for_same_scope():
    result = general_structural_transient_ceiling(
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
    assert result.oscillation_gain == pytest.approx(0.045)
    assert result.upper_stability_gain == pytest.approx(1.2)
    assert result.minimum_damped_gap == 1
    assert result.maximum_stable_gap == 4
    assert result.minimum_damped_gain == pytest.approx(0.125)
    assert result.maximum_stable_gain == pytest.approx(0.5)
    assert result.damping_time_upper_bound == pytest.approx(4.642709646291457)
    assert result.oscillation_period_upper_bound == pytest.approx(21.04927235012761)


def test_minimal_scope_can_be_damped_when_alpha_is_below_one():
    result = general_structural_transient_ceiling(
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
    assert result.structural_gap_upper_bound == 1
    assert result.minimum_damped_gap == 1
    assert result.maximum_stable_gap == 1
    assert result.damping_time_upper_bound == pytest.approx(2.2585623060109636)
    assert result.oscillation_period_upper_bound == pytest.approx(17.224120463999498)


def test_strict_upper_boundary_is_not_counted_as_stable():
    # alpha=.8, phi=.5 gives Gplus=1.2. With a=.3, gap=4 is exactly 1.2
    # and must therefore be excluded from the stable envelope.
    thresholds = general_response_thresholds(0.8, 0.5)
    assert thresholds.upper_stability_gain == pytest.approx(1.2)
    assert largest_generalized_stable_integer_gap(10, 0.3, 1.2) == 3


def test_integer_envelopes_match_direct_small_enumeration():
    for gap_upper in range(0, 9):
        for a in (0.05, 0.125, 0.2, 0.3, 0.5):
            for alpha, phi in ((1.0, 0.5), (0.8, 0.5), (0.4, 0.8)):
                thresholds = general_response_thresholds(alpha, phi)
                stable = [
                    g for g in range(1, gap_upper + 1)
                    if a * g < thresholds.upper_stability_gain
                ]
                damped = [
                    g for g in range(1, gap_upper + 1)
                    if thresholds.oscillation_gain < a * g < thresholds.upper_stability_gain
                ]
                assert largest_generalized_stable_integer_gap(
                    gap_upper, a, thresholds.upper_stability_gain
                ) == (max(stable) if stable else None)
                assert smallest_generalized_damped_integer_gap(
                    gap_upper,
                    a,
                    thresholds.oscillation_gain,
                    thresholds.upper_stability_gain,
                ) == (min(damped) if damped else None)


def test_damping_increases_and_period_decreases_with_generalized_gain():
    alpha = 0.8
    phi = 0.5
    low = 0.125
    high = 0.5
    assert generalized_damped_damping_time(
        low,
        evolutionary_persistence=alpha,
        community_memory=phi,
    ) < generalized_damped_damping_time(
        high,
        evolutionary_persistence=alpha,
        community_memory=phi,
    )
    assert generalized_damped_period(
        low,
        evolutionary_persistence=alpha,
        community_memory=phi,
    ) > generalized_damped_period(
        high,
        evolutionary_persistence=alpha,
        community_memory=phi,
    )


def test_frontier_edge_cap_removes_generalized_damped_phase():
    result = general_structural_transient_ceiling(
        12,
        12,
        3,
        2,
        evolutionary_persistence=0.8,
        community_memory=0.5,
        lambda_cost=10.0,
        selection_responsiveness=2.0,
        ecological_feedback_slope=-0.5,
        frontier_edge_cap=3,
    )
    assert result.structural_gap_upper_bound == 0
    assert not result.damped_phase_structurally_possible
    assert result.damping_time_upper_bound is None
    assert result.oscillation_period_upper_bound is None
