import math

import pytest

from adaptive_gain.urgency_policy_phases import (
    depth_mass_profile,
    discounted_profile_value,
    high_urgency_signature,
    pairwise_polynomial_coefficients,
    polynomial_value,
    profile_moments,
)


def test_registered_log_two_profiles_have_exact_polynomial_crossing():
    balanced = depth_mass_profile([2, 2, 2, 2], [0.25] * 4)
    priority = depth_mass_profile([1, 2, 3, 3], [0.25] * 4)

    coeffs = pairwise_polynomial_coefficients(priority, balanced)
    z = 0.5
    assert polynomial_value(coeffs, z) == pytest.approx(0.0)

    mu = math.log(2.0)
    assert discounted_profile_value(priority, discount_rate=mu) == pytest.approx(
        discounted_profile_value(balanced, discount_rate=mu)
    )


def test_low_urgency_prefers_lower_mean_cost():
    balanced = depth_mass_profile([2, 2, 2, 2], [0.25] * 4)
    priority = depth_mass_profile([1, 2, 3, 3], [0.25] * 4)

    assert profile_moments(balanced, max_order=1)[0] == pytest.approx(2.0)
    assert profile_moments(priority, max_order=1)[0] == pytest.approx(2.25)

    mu = 1e-4
    assert discounted_profile_value(balanced, discount_rate=mu) > discounted_profile_value(
        priority, discount_rate=mu
    )


def test_high_urgency_prefers_earlier_left_tail():
    balanced = depth_mass_profile([2, 2, 2, 2], [0.25] * 4)
    priority = depth_mass_profile([1, 2, 3, 3], [0.25] * 4)

    assert high_urgency_signature(priority) < high_urgency_signature(balanced)

    mu = 10.0
    assert discounted_profile_value(priority, discount_rate=mu) > discounted_profile_value(
        balanced, discount_rate=mu
    )


def test_equal_mean_profiles_can_differ_at_second_order():
    spread = depth_mass_profile([1, 3], [0.5, 0.5])
    concentrated = depth_mass_profile([2, 2], [0.5, 0.5])

    spread_moments = profile_moments(spread, max_order=2)
    concentrated_moments = profile_moments(concentrated, max_order=2)

    assert spread_moments[0] == pytest.approx(concentrated_moments[0])
    assert spread_moments[1] > concentrated_moments[1]

    mu = 1e-3
    assert discounted_profile_value(spread, discount_rate=mu) > discounted_profile_value(
        concentrated, discount_rate=mu
    )
