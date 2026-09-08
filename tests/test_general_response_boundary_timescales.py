import pytest

from adaptive_gain.general_evolutionary_response import general_response_thresholds
from adaptive_gain.general_response_boundary_timescales import (
    lower_boundary_critical_slowing_approximation,
    lower_boundary_damping_time,
    lower_boundary_dominant_eigenvalue,
    summarize_lower_boundary_timescale,
)


def test_lower_boundary_has_unit_eigenvalue_limit():
    alpha = 0.7
    phi = 0.5
    lower = general_response_thresholds(alpha, phi).lower_stability_gain
    assert lower == pytest.approx(-0.3)

    values = []
    for delta in (1e-2, 1e-3, 1e-4):
        rho = lower_boundary_dominant_eigenvalue(
            lower + delta,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
        values.append(rho)
        assert 0.0 < rho < 1.0
    assert values[0] < values[1] < values[2] < 1.0


def test_lower_critical_slowing_matches_asymptotic():
    alpha = 0.6
    phi = 0.7
    lower = general_response_thresholds(alpha, phi).lower_stability_gain
    for delta in (1e-4, 1e-5, 1e-6):
        G = lower + delta
        exact = lower_boundary_damping_time(
            G,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
        approx = lower_boundary_critical_slowing_approximation(
            G,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
        assert exact / approx == pytest.approx(1.0, rel=2e-3)


def test_parent_alpha_one_reduces_to_tau_asymptotic_one_over_G():
    alpha = 1.0
    phi = 0.8
    lower = general_response_thresholds(alpha, phi).lower_stability_gain
    assert lower == pytest.approx(0.0)
    for G in (1e-4, 1e-5, 1e-6):
        approx = lower_boundary_critical_slowing_approximation(
            G,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
        assert approx == pytest.approx(1.0 / G)
        exact = lower_boundary_damping_time(
            G,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
        assert exact / approx == pytest.approx(1.0, rel=2e-3)


def test_summary_is_consistent():
    alpha = 0.5
    phi = 0.4
    lower = general_response_thresholds(alpha, phi).lower_stability_gain
    summary = summarize_lower_boundary_timescale(
        lower + 1e-4,
        evolutionary_persistence=alpha,
        community_memory=phi,
    )
    assert summary.lower_stability_gain == pytest.approx(lower)
    assert summary.distance_to_lower_boundary == pytest.approx(1e-4)
    assert summary.damping_time == pytest.approx(
        lower_boundary_damping_time(
            lower + 1e-4,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
    )
    assert summary.scaled_ratio == pytest.approx(1.0, rel=2e-3)


def test_lower_boundary_helpers_reject_oscillatory_or_unstable_points():
    alpha = 0.8
    phi = 0.5
    thresholds = general_response_thresholds(alpha, phi)
    with pytest.raises(ValueError):
        lower_boundary_dominant_eigenvalue(
            thresholds.lower_stability_gain,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
    with pytest.raises(ValueError):
        lower_boundary_dominant_eigenvalue(
            thresholds.oscillation_gain + 0.1,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
