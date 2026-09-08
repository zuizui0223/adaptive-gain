import pytest

from adaptive_gain.directional_retention import (
    asymptotic_rms_retention_fraction,
    cumulative_selection_variance,
    expected_cumulative_selection,
    rms_cumulative_selection,
    rms_retention_fraction,
    summarize_directional_retention,
)
from adaptive_gain.evolutionary_timescale_filter import ar1_rms_retention_ratio


def test_zero_mean_reduces_to_existing_zero_mean_retention_formula():
    for horizon in (1, 10, 1000):
        for phi in (-0.7, 0.0, 0.6):
            assert rms_retention_fraction(horizon, 0.0, phi) == pytest.approx(
                ar1_rms_retention_ratio(horizon, phi)
            )


def test_nonzero_mean_creates_linear_expected_accumulation():
    assert expected_cumulative_selection(100, 0.4, 0.25) == pytest.approx(10.0)
    assert expected_cumulative_selection(100, 0.4, -0.25) == pytest.approx(-10.0)


def test_long_horizon_retention_converges_to_absolute_directional_bias():
    horizon = 1_000_000
    for mean_sign in (-0.7, -0.2, 0.0, 0.3, 0.8):
        for phi in (-0.6, 0.0, 0.7):
            observed = rms_retention_fraction(horizon, mean_sign, phi)
            expected = asymptotic_rms_retention_fraction(mean_sign)
            tolerance = 3e-3 if abs(mean_sign) < 0.05 else 8e-4
            assert observed == pytest.approx(expected, abs=tolerance, rel=tolerance)


def test_any_fixed_nonzero_bias_dominates_sqrt_h_fluctuations_eventually():
    mean_sign = 0.1
    phi = 0.5
    short = rms_retention_fraction(100, mean_sign, phi)
    long = rms_retention_fraction(1_000_000, mean_sign, phi)
    assert long < short
    assert long == pytest.approx(0.1, rel=2e-3)


def test_fully_directional_sign_has_unit_retention_independent_of_phi():
    for mean_sign in (-1.0, 1.0):
        for phi in (-1.0, -0.2, 0.8, 1.0):
            assert cumulative_selection_variance(50, 2.0, mean_sign, phi) == pytest.approx(0.0)
            assert rms_retention_fraction(50, mean_sign, phi) == pytest.approx(1.0)


def test_rms_identity_mean_squared_plus_variance():
    horizon = 37
    delta = 0.8
    mean_sign = 0.3
    phi = -0.4
    mean = expected_cumulative_selection(horizon, delta, mean_sign)
    variance = cumulative_selection_variance(horizon, delta, mean_sign, phi)
    rms = rms_cumulative_selection(horizon, delta, mean_sign, phi)
    assert rms * rms == pytest.approx(mean * mean + variance)


def test_summary_consistent():
    summary = summarize_directional_retention(20, 0.5, 0.2, 0.4)
    assert summary.expected_cumulative_selection == pytest.approx(2.0)
    assert summary.rms_cumulative_selection / (0.5 * 20) == pytest.approx(
        summary.rms_retention_fraction
    )


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        rms_retention_fraction(0, 0.0, 0.0)
    with pytest.raises(ValueError):
        rms_retention_fraction(10, 1.2, 0.0)
    with pytest.raises(ValueError):
        rms_retention_fraction(10, 0.0, 1.2)
