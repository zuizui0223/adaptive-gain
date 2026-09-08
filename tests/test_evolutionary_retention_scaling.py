from math import sqrt

import pytest

from adaptive_gain.evolutionary_timescale_filter import (
    ar1_partial_sum_factor,
    ar1_rms_retention_ratio,
    asymptotic_ar1_coherence_multiplier,
)


def test_closed_form_equivalent_to_covariance_sum_over_broad_grid():
    for horizon in (1, 2, 3, 7, 25, 100):
        for phi in (-0.95, -0.6, -0.1, 0.0, 0.3, 0.75, 0.95):
            direct = horizon + 2.0 * sum(
                (horizon - k) * (phi ** k)
                for k in range(1, horizon)
            )
            assert ar1_partial_sum_factor(horizon, phi) == pytest.approx(
                direct, rel=1e-11, abs=1e-11
            )


def test_sqrt_h_scaled_retention_converges_to_coherence_constant():
    horizon = 100_000
    for phi in (-0.8, -0.3, 0.0, 0.4, 0.8):
        scaled = sqrt(horizon) * ar1_rms_retention_ratio(horizon, phi)
        expected = sqrt(asymptotic_ar1_coherence_multiplier(phi))
        assert scaled == pytest.approx(expected, rel=2e-4, abs=2e-4)


def test_activity_linear_but_rms_retained_fraction_shrinks_for_finite_correlation_time():
    for phi in (-0.5, 0.0, 0.5):
        short = ar1_rms_retention_ratio(100, phi)
        long = ar1_rms_retention_ratio(10_000, phi)
        assert long < short
        # A hundred-fold increase in horizon should reduce the asymptotic ratio
        # by about ten-fold once the correlation time is small relative to H.
        assert (long / short) == pytest.approx(0.1, rel=0.08)


def test_perfect_endpoints_are_singular_limits():
    # Perfect persistence never loses directional retention.
    assert ar1_rms_retention_ratio(10_000, 1.0) == pytest.approx(1.0)
    # Perfect alternation cancels every complete two-generation cycle.
    assert ar1_rms_retention_ratio(10_000, -1.0) == pytest.approx(0.0)
