from math import inf

import pytest

from adaptive_gain.directional_retention import (
    asymptotic_directional_crossover_horizon,
    asymptotic_rms_retention_fraction,
    community_directional_crossover_horizon,
    community_switching_to_mean_and_coherence,
    cumulative_selection_variance,
    directional_signal_to_noise,
    expected_cumulative_selection,
    rms_cumulative_selection,
    rms_retention_fraction,
    stationary_plus_occupancy,
    summarize_community_switching,
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
    for mean_sign in (-0.7, -0.2, 0.0, 0.3, 0.8):
        for phi in (-0.1, 0.0, 0.7):
            assert two_state_markov_feasible(mean_sign, phi)
            observed = rms_retention_fraction(horizon, mean_sign, phi)
            expected = asymptotic_rms_retention_fraction(mean_sign)
            tolerance = 3e-3 if abs(mean_sign) < 0.05 else 8e-4
            assert observed == pytest.approx(expected, abs=tolerance, rel=tolerance)


def test_two_state_markov_feasibility_boundary():
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


def test_community_switching_maps_directly_to_bias_and_coherence():
    # a=P(+|-)=0.3, b=P(-|+)=0.2
    m, phi = community_switching_to_mean_and_coherence(0.3, 0.2)
    assert m == pytest.approx(0.2)
    assert phi == pytest.approx(0.5)
    assert stationary_plus_occupancy(0.3, 0.2) == pytest.approx(0.6)
    a2, b2 = two_state_markov_transition_probabilities(m, phi)
    assert a2 == pytest.approx(0.3)
    assert b2 == pytest.approx(0.2)


def test_community_crossover_closed_form_matches_m_phi_substitution():
    for a, b in ((0.3, 0.2), (0.05, 0.15), (0.6, 0.3), (0.9, 0.7)):
        m, phi = community_switching_to_mean_and_coherence(a, b)
        direct = asymptotic_directional_crossover_horizon(m, phi)
        community = community_directional_crossover_horizon(a, b)
        closed = 4.0 * a * b * (2.0 - a - b) / (((a - b) ** 2) * (a + b))
        assert community == pytest.approx(direct)
        assert community == pytest.approx(closed)


def test_balanced_community_occupancy_has_no_directional_crossover():
    for switch_rate in (0.1, 0.5, 1.0):
        m, phi = community_switching_to_mean_and_coherence(switch_rate, switch_rate)
        assert m == pytest.approx(0.0)
        assert phi == pytest.approx(1.0 - 2.0 * switch_rate)
        assert community_directional_crossover_horizon(switch_rate, switch_rate) == inf


def test_same_occupancy_bias_but_more_persistent_community_delays_trend_emergence():
    # Scaling both transitions by a common factor preserves stationary occupancy
    # and m, while smaller total switching raises phi (longer state persistence).
    fast = summarize_community_switching(0.6, 0.4)
    slow = summarize_community_switching(0.3, 0.2)
    assert fast.mean_sign == pytest.approx(slow.mean_sign)
    assert fast.stationary_plus_occupancy == pytest.approx(slow.stationary_plus_occupancy)
    assert slow.phi > fast.phi
    assert slow.crossover_horizon > fast.crossover_horizon


def test_community_summary_consistent():
    summary = summarize_community_switching(0.3, 0.2)
    assert summary.stationary_plus_occupancy == pytest.approx(0.6)
    assert summary.mean_sign == pytest.approx(0.2)
    assert summary.phi == pytest.approx(0.5)
    assert summary.asymptotic_retained_fraction == pytest.approx(0.2)
    assert summary.crossover_horizon == pytest.approx(
        asymptotic_directional_crossover_horizon(0.2, 0.5)
    )


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
    with pytest.raises(ValueError):
        community_switching_to_mean_and_coherence(0.0, 0.0)
    with pytest.raises(ValueError):
        community_switching_to_mean_and_coherence(1.2, 0.2)
