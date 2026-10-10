"""Independent brute-force tests for payoff-relevant decision-value expiry."""
import itertools
import math

import pytest

from adaptive_gain.decision_value_expiry import (
    decision_receipt, finite_action_value_expiry,
    stationary_probability_one, conditional_probability_one,
)


def test_stationary_prior_and_symmetric_half_life():
    r = decision_receipt(math.log(2) / 2, 1, 1)
    assert r.stationary_one == pytest.approx(.5)
    assert r.conditional_one_after_zero == pytest.approx(.25)
    assert r.conditional_one_after_one == pytest.approx(.75)
    assert r.decision_value == pytest.approx(.25)
    assert r.finite_expiry_time is None


def test_sharp_finite_expiry_in_skewed_occupancy():
    tcrit = math.log(8 / 3)
    assert stationary_probability_one(.8, .2) == pytest.approx(.8)
    assert finite_action_value_expiry(.8, .2) == pytest.approx(tcrit)
    before = decision_receipt(.5, .8, .2)
    after = decision_receipt(1.2, .8, .2)
    assert before.decision_value == pytest.approx(.32 * math.exp(-.5) - .12)
    assert before.decision_value > 0
    assert after.decision_value == pytest.approx(0)
    assert after.action_after_zero == after.action_after_one == after.blind_action == 1
    assert after.mutual_information_nats > 0
    assert decision_receipt(tcrit, .8, .2).decision_value == pytest.approx(0, abs=1e-13)


def test_random_grid_exact_bayes_policy_not_only_follow_old_cue():
    for up, down, t in itertools.product(
        (.1, .2, .8, 1.4), (.1, .2, .8, 1.4), (0, .01, .2, 1, 2, 10)
    ):
        x = decision_receipt(t, up, down)
        p0 = conditional_probability_one(0, t, up, down)
        p1 = conditional_probability_one(1, t, up, down)
        scores = []
        for a0, a1 in itertools.product((0, 1), repeat=2):
            prob0 = p0 if a0 else 1 - p0
            prob1 = p1 if a1 else 1 - p1
            scores.append((1 - x.stationary_one) * prob0
                          + x.stationary_one * prob1)
        assert x.optimal_cue_accuracy == pytest.approx(max(scores))
        assert x.decision_value >= 0
        if up != down and t > x.finite_expiry_time + 1e-8:
            assert x.decision_value == pytest.approx(0, abs=1e-12)
            assert x.mutual_information_nats > 0


def test_symmetry_and_assumptions():
    assert finite_action_value_expiry(.2, .8) == pytest.approx(
        finite_action_value_expiry(.8, .2))
    assert decision_receipt(.3, .2, .8).decision_value == pytest.approx(
        decision_receipt(.3, .8, .2).decision_value)
    for args in ((0, .5), (-.1, 1), (.2, float("nan"))):
        with pytest.raises(ValueError):
            finite_action_value_expiry(*args)
    with pytest.raises(ValueError):
        decision_receipt(-1, .8, .2)
