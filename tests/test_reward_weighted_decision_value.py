"""Independent enumeration of reward-weighted state-contingent decisions."""
import itertools
import math

import pytest

from adaptive_gain.decision_value_expiry import conditional_probability_one
from adaptive_gain.reward_weighted_decision_value import (
    optimal_action_threshold,
    reward_weighted_receipt,
    weighted_value_expiry,
    reward_weighted_value_closed_form,
    last_profitable_cue_age,
)


def _independent_best_reward(t, up, down, reward0, reward1):
    """Brute-force four fixed old-cue-to-action maps (no optimization helper)."""
    prior1 = up / (up + down)
    p = (
        conditional_probability_one(0, t, up, down),
        conditional_probability_one(1, t, up, down),
    )
    all_policy_rewards = []
    for action0, action1 in itertools.product((0, 1), repeat=2):
        values = []
        for action, state1prob in ((action0, p[0]), (action1, p[1])):
            values.append(reward1 * state1prob if action else reward0 * (1 - state1prob))
        all_policy_rewards.append((1 - prior1) * values[0] + prior1 * values[1])
    return max(all_policy_rewards)


def test_symmetric_rewards_recover_previous_exact_boundary():
    r = reward_weighted_receipt(.5, .8, .2, 1, 1)
    assert r.expiry_time == pytest.approx(math.log(8 / 3))
    assert r.marginal_decision_value == pytest.approx(.32 * math.exp(-.5) - .12)
    assert r.oldcue_zero_action == 0
    assert r.oldcue_one_action == 1


def test_asymmetric_payoffs_can_shorten_or_extend_cue_lifetime():
    # Occupancy is 80:20 in every case: the payoff matrix changes only.
    shorter = reward_weighted_receipt(1, .8, .2, 1, 2)
    ordinary = reward_weighted_receipt(1, .8, .2, 1, 1)
    longer = reward_weighted_receipt(1, .8, .2, 2, 1)
    critical = reward_weighted_receipt(1, .8, .2, 4, 1)
    assert shorter.expiry_time == pytest.approx(math.log(12 / 7))
    assert ordinary.expiry_time == pytest.approx(math.log(8 / 3))
    assert longer.expiry_time == pytest.approx(math.log(6))
    assert critical.expiry_time is None
    assert shorter.marginal_decision_value == pytest.approx(0)
    assert ordinary.marginal_decision_value == pytest.approx(0)
    assert longer.marginal_decision_value > 0
    assert critical.marginal_decision_value > 0
    assert critical.action_threshold == pytest.approx(.8)


def test_no_finite_expiry_when_reward_threshold_equals_prior():
    for t in (0, .1, 1, 2, 10, 20):
        r = reward_weighted_receipt(t, .8, .2, 4, 1)
        assert r.expiry_time is None
        assert r.marginal_decision_value > 0
        assert (r.oldcue_zero_action, r.oldcue_one_action) == (0, 1)
    assert reward_weighted_receipt(20, .8, .2, 4, 1).marginal_decision_value < (
        reward_weighted_receipt(1, .8, .2, 4, 1).marginal_decision_value)


def test_all_four_policies_independently_enumerated_in_large_grid():
    cases = 0
    for u, d, r0, r1, t in itertools.product(
        (.2, .8, 1.4), (.2, .8, 1.4), (1., 2., 4.),
        (1., 2., 4.), (0., .01, .3, 1., 2., 5.),
    ):
        result = reward_weighted_receipt(t, u, d, r0, r1)
        brute = _independent_best_reward(t, u, d, r0, r1)
        assert result.cue_expected_reward == pytest.approx(brute)
        assert result.marginal_decision_value >= 0
        if result.expiry_time is not None and t > result.expiry_time + 1e-7:
            assert result.marginal_decision_value == pytest.approx(0, abs=1e-11)
        cases += 1
    assert cases == 486


def test_relabeling_states_and_rewards_preserves_value():
    for t in (.01, .4, 1., 5.):
        a = reward_weighted_receipt(t, .8, .2, 4, 1)
        b = reward_weighted_receipt(t, .2, .8, 1, 4)
        assert a.marginal_decision_value == pytest.approx(b.marginal_decision_value)


def test_invalid_parameters_are_rejected():
    for args in ((0, .2, 1, 1), (.2, -.1, 1, 1),
                 (.2, .1, 0, 1), (.2, .1, 1, float("inf"))):
        with pytest.raises(ValueError):
            weighted_value_expiry(*args)
    with pytest.raises(ValueError):
        reward_weighted_receipt(-1, .8, .2, 1, 1)
    assert optimal_action_threshold(4, 1) == pytest.approx(.8)


def test_exact_closed_form_against_bayes_enumeration():
    n = 0
    for u, d, r0, r1, t in itertools.product(
        (.1, .2, .8, 1.7), (.2, .8, 1.7),
        (.5, 1, 2, 4), (.5, 1, 2, 4), (0, .01, .5, 1, 3, 12),
    ):
        closed = reward_weighted_value_closed_form(t, u, d, r0, r1)
        brute = _independent_best_reward(t, u, d, r0, r1)
        prior = u / (u + d)
        blind = max((1 - prior) * r0, prior * r1)
        assert closed == pytest.approx(max(0., brute - blind), abs=1e-12)
        n += 1
    assert n == 1152


def test_cost_turns_infinite_information_lifetime_into_finite_use_horizon():
    assert last_profitable_cue_age(.8, .2, 4, 1) == math.inf
    horizon = last_profitable_cue_age(.8, .2, 4, 1, cue_use_cost=.1)
    assert horizon == pytest.approx(math.log(8))
    assert reward_weighted_value_closed_form(horizon, .8, .2, 4, 1) == pytest.approx(.1)
    assert last_profitable_cue_age(.8, .2, 4, 1, cue_use_cost=.8) == 0.
    assert last_profitable_cue_age(.8, .2, 1, 1) == pytest.approx(math.log(8/3))


def test_action_value_cost_horizon_is_sharp_across_payoffs():
    for r0, r1, cost in ((1, 1, .01), (2, 1, .01), (4, 1, .1),
                         (1, 2, .02)):
        h = last_profitable_cue_age(.8, .2, r0, r1, cue_use_cost=cost)
        assert math.isfinite(h) and h > 0.
        assert reward_weighted_value_closed_form(h-.001, .8, .2, r0, r1) > cost
        assert reward_weighted_value_closed_form(h+.001, .8, .2, r0, r1) < cost


def test_closed_form_and_cost_validate_inputs():
    with pytest.raises(ValueError):
        last_profitable_cue_age(.8, .2, 1, 1, cue_use_cost=-.1)
    with pytest.raises(ValueError):
        reward_weighted_value_closed_form(float("inf"), .8, .2, 1, 1)
