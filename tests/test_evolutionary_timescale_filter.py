import pytest

from adaptive_gain.evolutionary_timescale_filter import (
    ar1_coherence_multiplier,
    ar1_partial_sum_factor,
    ar1_rms_retained_change,
    ar1_rms_retention_ratio,
    asymptotic_ar1_coherence_multiplier,
    coherence_multiplier,
    cumulative_response,
    evolutionary_activity,
    partial_sum_variance,
    retained_change,
    retention_ratio,
    summarize_selection_path,
)


def test_activity_and_retention_separate_reversal_from_stasis():
    beta = (2.0, -2.0, 2.0, -2.0)
    assert evolutionary_activity(beta) == pytest.approx(8.0)
    assert cumulative_response(beta) == pytest.approx(0.0)
    assert retained_change(beta) == pytest.approx(0.0)
    assert retention_ratio(beta) == pytest.approx(0.0)


def test_persistent_direction_is_fully_retained():
    beta = (1.5, 1.5, 1.5)
    assert evolutionary_activity(beta) == pytest.approx(4.5)
    assert retained_change(beta) == pytest.approx(4.5)
    assert retention_ratio(beta) == pytest.approx(1.0)


def test_evolvability_scales_activity_and_retained_change_but_not_ratio():
    beta = (1.0, -0.25, 0.5)
    assert evolutionary_activity(beta, 3.0) == pytest.approx(3.0 * evolutionary_activity(beta))
    assert retained_change(beta, 3.0) == pytest.approx(3.0 * retained_change(beta))
    assert retention_ratio(beta, 3.0) == pytest.approx(retention_ratio(beta))


def test_partial_sum_variance_identity():
    gamma = (4.0, 2.0, 1.0, 0.5)
    expected = 4 * 4.0 + 2 * (3 * 2.0 + 2 * 1.0 + 1 * 0.5)
    assert partial_sum_variance(4, gamma) == pytest.approx(expected)


def test_coherence_multiplier_matches_normalized_covariance_sum():
    rho = (1.0, 0.5, 0.25, 0.125)
    direct = 1.0 + 2.0 * (
        (1 - 1 / 4) * 0.5
        + (1 - 2 / 4) * 0.25
        + (1 - 3 / 4) * 0.125
    )
    assert coherence_multiplier(4, rho) == pytest.approx(direct)


def test_ar1_closed_form_matches_direct_covariance_sum():
    for horizon in range(1, 9):
        for phi in (-1.0, -0.8, -0.2, 0.0, 0.4, 0.9, 1.0):
            direct = horizon + 2.0 * sum(
                (horizon - k) * (phi ** k)
                for k in range(1, horizon)
            )
            assert ar1_partial_sum_factor(horizon, phi) == pytest.approx(direct)


def test_independent_fluctuating_selection_has_sqrt_h_retention_scale():
    for horizon in (1, 4, 25, 100):
        assert ar1_partial_sum_factor(horizon, 0.0) == pytest.approx(float(horizon))
        assert ar1_rms_retention_ratio(horizon, 0.0) == pytest.approx(1.0 / (horizon ** 0.5))


def test_perfect_alternation_cancels_even_horizons():
    for horizon in (2, 4, 10):
        assert ar1_partial_sum_factor(horizon, -1.0) == pytest.approx(0.0)
        assert ar1_rms_retention_ratio(horizon, -1.0) == pytest.approx(0.0)


def test_perfect_persistence_retains_all_activity_in_rms_scale():
    for horizon in (1, 3, 20):
        assert ar1_partial_sum_factor(horizon, 1.0) == pytest.approx(float(horizon * horizon))
        assert ar1_rms_retention_ratio(horizon, 1.0) == pytest.approx(1.0)


def test_ar1_long_horizon_coherence_limit():
    for phi in (-0.5, 0.0, 0.4, 0.8):
        finite = ar1_coherence_multiplier(10000, phi)
        limiting = asymptotic_ar1_coherence_multiplier(phi)
        assert finite == pytest.approx(limiting, rel=5e-4, abs=5e-4)


def test_summary_path():
    s = summarize_selection_path((1.0, -0.5, 0.5))
    assert s.horizon == 3
    assert s.activity == pytest.approx(2.0)
    assert s.signed_response == pytest.approx(1.0)
    assert s.retained_change == pytest.approx(1.0)
    assert s.retention_ratio == pytest.approx(0.5)


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        evolutionary_activity(())
    with pytest.raises(ValueError):
        partial_sum_variance(0, (1.0,))
    with pytest.raises(ValueError):
        ar1_partial_sum_factor(3, 1.2)
    with pytest.raises(ValueError):
        asymptotic_ar1_coherence_multiplier(1.0)
