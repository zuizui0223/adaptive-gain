from math import inf

import pytest

from adaptive_gain.directional_retention import (
    asymptotic_directional_crossover_horizon,
    asymptotic_rms_retention_fraction,
    cumulative_selection_variance,
    directional_signal_to_noise,
    expected_cumulative_selection,
    rms_cumulative_selection,
    rms_retention_fraction,
    summarize_directional_retention,
    two_state_markov_feasible,
    two_state_markov_transition_probabilities,
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
    # This shared phi grid is Markov-feasible even for |m|=0.8.
    for mean_sign in (-0.7, -0.2, 0.0, 0.3, 0.8):
        for phi in (-0.1, 0.0, 0.7):
            assert two_state_markov_feasible(mean_sign, phi)
            observed = rms_retention_fraction(horizon, mean_sign, phi)
            expected = asymptotic_rms_retention_fraction(mean_sign)
            tolerance = 3e-3 if abs(mean_sign) < 0.05 else 8e-4
            assert observed == pytest.approx(expected, abs=tolerance, rel=tolerance)


def test_two_state_markov_feasibility_boundary():
    # For m=0.8, phi_min=-(1-0.8)/(1+0.8)=-1/9.
    assert two_state_markov_feasible(0.8, -0.1)
    assert not two_state_markov_feasible(0.8, -0.2)
    with pytest.raises(ValueError):
        two_state_markov_transition_probabilities(0.8, -0.2)


def test_two_state_markov_transition_probabilities_recover_stationary_bias():
    plus_from_minus, minus_from_plus = two_state_markov_transition_probabilities(0.2, 0.5)
    assert plus_from_minus == pytest.approx(0.3)
    assert minus_from_plus == pytest.approx(0.2)
    stationary_plus = plus_from_minus / (plus_from_minus + minus_from_plus)
    assert 2.0 * stationary_plus - 1.0 == pytest.approx(0.2)
    assert 1.0 - plus_from_minus - minus_from_plus == pytest.approx(0.5)


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
    assert two_state_markov_feasible(mean_sign, phi)
    mean = expected_cumulative_selection(horizon, delta, mean_sign)
    variance = cumulative_selection_variance(horizon, delta, mean_sign, phi)
    rms = rms_cumulative_selection(horizon, delta, mean_sign, phi)
    assert rms * rms == pytest.approx(mean * mean + variance)


def test_crossover_horizon_matches_signal_to_noise_transition_asymptotically():
    for mean_sign, phi in ((0.1, 0.0), (0.2, 0.5), (0.15, -0.4)):
        assert two_state_markov_feasible(mean_sign, phi)
        hx = asymptotic_directional_crossover_horizon(mean_sign, phi)
        assert hx > 0.0
        H = max(1, round(hx))
        snr = directional_signal_to_noise(H, mean_sign, phi)
        assert 0.5 <= snr <= 2.0
        assert directional_signal_to_noise(max(H * 100, 100), mean_sign, phi) > snr


def test_crossover_horizon_increases_with_positive_temporal_coherence():
    mean_sign = 0.1
    negative = asymptotic_directional_crossover_horizon(mean_sign, -0.5)
    independent = asymptotic_directional_crossover_horizon(mean_sign, 0.0)
    positive = asymptotic_directional_crossover_horizon(mean_sign, 0.5)
    assert negative < independent < positive


def test_small_directional_bias_delays_emergence_quadratically():
    phi = 0.2
    h_large_bias = asymptotic_directional_crossover_horizon(0.2, phi)
    h_small_bias = asymptotic_directional_crossover_horizon(0.1, phi)
    assert h_small_bias > 3.5 * h_large_bias


def test_zero_bias_never_has_directional_crossover_and_full_bias_is_immediate():
    assert asymptotic_directional_crossover_horizon(0.0, 0.0) == inf
    assert asymptotic_directional_crossover_horizon(1.0, 0.0) == 0.0
    assert directional_signal_to_noise(100, 0.0, 0.5) == pytest.approx(0.0)
    assert directional_signal_to_noise(100, 1.0, 0.5) == inf


def test_summary_consistent():
    summary = summarize_directional_retention(20, 0.5, 0.2, 0.4)
    assert summary.expected_cumulative_selection == pytest.approx(2.0)
    assert summary.rms_cumulative_selection / (0.5 * 20) == pytest.approx(
        summary.rms_retention_fraction
    )
    assert summary.directional_signal_to_noise == pytest.approx(
        directional_signal_to_noise(20, 0.2, 0.4)
    )


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        rms_retention_fraction(0, 0.0, 0.0)
    with pytest.raises(ValueError):
        rms_retention_fraction(10, 1.2, 0.0)
    with pytest.raises(ValueError):
        rms_retention_fraction(10, 0.0, 1.2)
    with pytest.raises(ValueError):
        asymptotic_directional_crossover_horizon(0.2, 1.0)
