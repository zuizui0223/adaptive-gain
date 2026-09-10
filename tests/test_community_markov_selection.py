from itertools import product

import pytest

from adaptive_gain.community_markov_selection import (
    asymptotic_directional_fraction,
    covariance_sequence,
    cumulative_selection_variance,
    directional_signal_to_noise,
    expected_cumulative_selection,
    expected_selection_activity,
    lag_covariance,
    rms_cumulative_selection,
    rms_retention_fraction,
    stationary_mean_selection,
    structural_rewards_from_tasks,
    summarize_markov_selection,
)
from adaptive_gain.directional_retention import (
    community_switching_to_mean_and_coherence,
    cumulative_selection_variance as two_state_variance,
    expected_cumulative_selection as two_state_mean,
    rms_retention_fraction as two_state_retention,
)
from adaptive_gain.resource_overlap import resource_role_profile_collision


def _two_state_model(a, b, delta=1.0):
    total = a + b
    stationary = (b / total, a / total)  # states (-,+)
    transition = ((1.0 - a, a), (b, 1.0 - b))
    rewards = (-delta, delta)
    return stationary, transition, rewards


def _persistent_three_state_model():
    # P = 0.6 I + 0.4 * 1 pi, so pi is stationary by construction.
    stationary = (0.2, 0.5, 0.3)
    transition = (
        (0.68, 0.20, 0.12),
        (0.08, 0.80, 0.12),
        (0.08, 0.20, 0.72),
    )
    return stationary, transition


def test_two_state_markov_reward_layer_recovers_m_phi_formulas():
    for a, b in ((0.3, 0.2), (0.1, 0.4), (0.7, 0.5)):
        stationary, transition, rewards = _two_state_model(a, b, delta=0.8)
        m, phi = community_switching_to_mean_and_coherence(a, b)
        assert stationary_mean_selection(stationary, transition, rewards) == pytest.approx(0.8 * m)
        for lag in range(5):
            expected_cov = (0.8 ** 2) * (1.0 - m * m) * (phi ** lag)
            assert lag_covariance(lag, stationary, transition, rewards) == pytest.approx(expected_cov)
        for horizon in (1, 2, 5, 20):
            assert expected_cumulative_selection(horizon, stationary, transition, rewards) == pytest.approx(
                two_state_mean(horizon, 0.8, m)
            )
            assert cumulative_selection_variance(horizon, stationary, transition, rewards) == pytest.approx(
                two_state_variance(horizon, 0.8, m, phi)
            )
            assert rms_retention_fraction(horizon, stationary, transition, rewards) == pytest.approx(
                two_state_retention(horizon, m, phi)
            )


def test_finite_state_covariance_matches_bruteforce_path_moments():
    stationary, transition = _persistent_three_state_model()
    rewards = (-1.0, 0.25, 1.5)
    horizon = 4

    weighted_sum = 0.0
    weighted_square = 0.0
    total_prob = 0.0
    for path in product(range(3), repeat=horizon):
        prob = stationary[path[0]]
        for t in range(1, horizon):
            prob *= transition[path[t - 1]][path[t]]
        total = sum(rewards[state] for state in path)
        total_prob += prob
        weighted_sum += prob * total
        weighted_square += prob * total * total

    assert total_prob == pytest.approx(1.0)
    model_mean = expected_cumulative_selection(horizon, stationary, transition, rewards)
    model_var = cumulative_selection_variance(horizon, stationary, transition, rewards)
    assert model_mean == pytest.approx(weighted_sum)
    assert model_var == pytest.approx(weighted_square - weighted_sum * weighted_sum)
    assert rms_cumulative_selection(horizon, stationary, transition, rewards) ** 2 == pytest.approx(
        weighted_square
    )


def test_structural_collision_maps_directly_to_opposite_markov_rewards():
    no_gain, strict = resource_role_profile_collision()
    rewards = structural_rewards_from_tasks(
        (no_gain, strict), lambda_cost=1.0, control_cost=0.5
    )
    assert rewards == pytest.approx((-0.5, 0.5))

    stationary = (0.5, 0.5)
    transition = ((0.75, 0.25), (0.25, 0.75))
    assert stationary_mean_selection(stationary, transition, rewards) == pytest.approx(0.0)
    assert asymptotic_directional_fraction(stationary, transition, rewards) == pytest.approx(0.0)
    assert lag_covariance(1, stationary, transition, rewards) == pytest.approx(0.125)


def test_multistate_mean_and_activity_separate_direction_from_amount():
    stationary, transition = _persistent_three_state_model()
    rewards = (-2.0, 0.4, 1.0)
    mean = stationary_mean_selection(stationary, transition, rewards)
    activity = expected_selection_activity(1, stationary, transition, rewards)
    assert mean == pytest.approx(0.1)
    assert activity == pytest.approx(0.9)
    assert asymptotic_directional_fraction(stationary, transition, rewards) == pytest.approx(1.0 / 9.0)


def test_covariance_sequence_agrees_with_individual_lag_calls():
    stationary, transition, rewards = _two_state_model(0.3, 0.2)
    seq = covariance_sequence(8, stationary, transition, rewards)
    assert seq == pytest.approx(
        tuple(lag_covariance(k, stationary, transition, rewards) for k in range(9))
    )


def test_signal_to_noise_grows_when_stationary_mean_is_nonzero():
    stationary, transition, rewards = _two_state_model(0.3, 0.2)
    assert directional_signal_to_noise(10_000, stationary, transition, rewards) > directional_signal_to_noise(
        100, stationary, transition, rewards
    )


def test_summary_is_consistent():
    stationary, transition, rewards = _two_state_model(0.3, 0.2)
    summary = summarize_markov_selection(100, stationary, transition, rewards)
    assert summary.state_count == 2
    assert summary.expected_cumulative_selection == pytest.approx(
        expected_cumulative_selection(100, stationary, transition, rewards)
    )
    assert summary.cumulative_variance == pytest.approx(
        cumulative_selection_variance(100, stationary, transition, rewards)
    )
    assert summary.rms_retention_fraction == pytest.approx(
        rms_retention_fraction(100, stationary, transition, rewards)
    )


def test_invalid_stationary_or_transition_inputs_raise():
    with pytest.raises(ValueError):
        stationary_mean_selection((0.5, 0.5), ((0.9, 0.1),), (-1.0, 1.0))
    with pytest.raises(ValueError):
        stationary_mean_selection((0.5, 0.5), ((0.9, 0.1), (0.4, 0.6)), (-1.0, 1.0))
    with pytest.raises(ValueError):
        stationary_mean_selection((0.4, 0.4), ((0.8, 0.2), (0.2, 0.8)), (-1.0, 1.0))
