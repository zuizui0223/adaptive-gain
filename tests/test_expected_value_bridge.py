import math

import pytest

from adaptive_gain.expected_value_bridge import (
    four_world_rescue_probability_threshold,
    robust_plus_early_premium,
)


def test_exact_robust_plus_early_premium_decomposition():
    paths = [1.0, 3.0, 3.0, 2.0]
    probs = [0.9, 1 / 30, 1 / 30, 1 / 30]
    value = lambda t: 2.0 ** (-t)

    robust, premium, expected = robust_plus_early_premium(
        paths,
        probs,
        2.0,
        value,
    )

    assert robust == pytest.approx(-0.125)
    direct = sum(p * value(t) for p, t in zip(probs, paths)) - value(2.0)
    assert expected == pytest.approx(direct)
    assert expected == pytest.approx(7 / 15 - 1 / 4)
    assert premium == pytest.approx(expected - robust)


def test_minimax_policy_can_have_zero_robust_gap_but_positive_expected_premium():
    paths = [1.0, 2.0, 2.0, 2.0]
    probs = [0.9, 1 / 30, 1 / 30, 1 / 30]
    value = lambda t: 2.0 ** (-t)

    robust, premium, expected = robust_plus_early_premium(
        paths,
        probs,
        2.0,
        value,
    )

    assert robust == pytest.approx(0.0)
    assert premium > 0.0
    assert expected > 0.0


def test_four_world_rescue_threshold_is_one_quarter_at_log_two():
    threshold = four_world_rescue_probability_threshold(
        discount_rate=math.log(2.0)
    )
    assert threshold == pytest.approx(0.25)


def test_four_world_expected_rescue_above_threshold():
    mu = math.log(2.0)
    p = 0.9
    x = math.exp(-mu)
    adaptive = p * x + (1 - p) / 3.0 * (x * x + 2 * x ** 3)
    fixed = x * x
    assert adaptive > fixed


def test_expected_architecture_cost_ceiling_is_one_quarter_at_log_two():
    mu = math.log(2.0)
    assert four_world_rescue_probability_threshold(
        discount_rate=mu,
        architecture_cost=0.249,
    ) is not None
    assert four_world_rescue_probability_threshold(
        discount_rate=mu,
        architecture_cost=0.25,
    ) is None
