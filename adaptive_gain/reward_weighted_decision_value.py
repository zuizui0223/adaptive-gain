"""Reward-weighted extinction of old cue's optimal *decision* value.

The environmental process is an irreducible stationary binary CTMC.
A perfect initial-state observation can be used at lag t. At the decision,
action 0 receives r0>0 if state 0, and action 1 receives r1>0 if state 1;
all mismatches pay zero. This is an immediate-reward decision model, NOT
a claim about ecological fitness, adaptive sensing architecture, or C_A/C_F.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from .decision_value_expiry import (
    conditional_probability_one,
    stationary_probability_one,
)


def _positive_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and > 0")
    return value


def _parameters(up_rate: float, down_rate: float, reward_zero: float,
                reward_one: float) -> tuple[float, float, float, float]:
    u = _positive_finite("up_rate", up_rate)
    d = _positive_finite("down_rate", down_rate)
    r0 = _positive_finite("reward_zero", reward_zero)
    r1 = _positive_finite("reward_one", reward_one)
    if not math.isfinite(u + d) or not math.isfinite(r0 + r1):
        raise ValueError("rates and rewards must have finite sums")
    return u, d, r0, r1


def optimal_action_threshold(reward_zero: float, reward_one: float) -> float:
    """Probability of state 1 above which action 1 is payoff-optimal."""
    r0 = _positive_finite("reward_zero", reward_zero)
    r1 = _positive_finite("reward_one", reward_one)
    if not math.isfinite(r0 + r1):
        raise ValueError("rewards must have a finite sum")
    return r0 / (r0 + r1)


def weighted_value_expiry(up_rate: float, down_rate: float,
                          reward_zero: float, reward_one: float) -> float | None:
    """Exact first finite time after which both cue-conditioned actions agree.

    None if prior lies on the reward-sensitive action threshold: cue value
    remains strictly positive at every finite lag, but tends to zero.
    Equality is mathematical equality at supplied floating-point parameters;
    near equality gives a large but finite t*, not a false infinite expiry.
    """
    u, d, r0, r1 = _parameters(up_rate, down_rate, reward_zero, reward_one)
    prior = u / (u + d)
    threshold = r0 / (r0 + r1)
    rate_sum = u + d
    if prior == threshold:
        return None
    if prior > threshold:
        return math.log(prior / (prior - threshold)) / rate_sum
    return math.log((1 - prior) / (threshold - prior)) / rate_sum


@dataclass(frozen=True)
class RewardWeightedReceipt:
    lag: float
    prior_one: float
    action_threshold: float
    oldcue_zero_action: int
    oldcue_one_action: int
    blind_action: int
    blind_expected_reward: float
    cue_expected_reward: float
    marginal_decision_value: float
    expiry_time: float | None


def reward_weighted_receipt(lag: float, up_rate: float, down_rate: float,
                            reward_zero: float, reward_one: float
                            ) -> RewardWeightedReceipt:
    u, d, r0, r1 = _parameters(up_rate, down_rate, reward_zero, reward_one)
    t = float(lag)
    if not math.isfinite(t) or t < 0:
        raise ValueError("lag must be finite and nonnegative")
    prior = stationary_probability_one(u, d)
    p0 = conditional_probability_one(0, t, u, d)
    p1 = conditional_probability_one(1, t, u, d)
    threshold = r0 / (r0 + r1)
    act0, act1 = int(p0 >= threshold), int(p1 >= threshold)
    blind = max(r0 * (1 - prior), r1 * prior)
    cue = ((1 - prior) * max(r0 * (1 - p0), r1 * p0)
           + prior * max(r0 * (1 - p1), r1 * p1))
    return RewardWeightedReceipt(
        lag=t, prior_one=prior, action_threshold=threshold,
        oldcue_zero_action=act0, oldcue_one_action=act1,
        blind_action=int(prior >= threshold), blind_expected_reward=blind,
        cue_expected_reward=cue,
        marginal_decision_value=max(0.0, cue - blind),
        expiry_time=weighted_value_expiry(u, d, r0, r1),
    )


def reward_weighted_value_closed_form(
    lag: float,
    up_rate: float,
    down_rate: float,
    reward_zero: float,
    reward_one: float,
) -> float:
    """Exact rectified-exponential value of a perfect past-state cue.

    V(t)=[A*exp(-(up+down)*t)-B]_+, where
    A=(r0+r1)*pi0*pi1;
    B=(r0+r1)*[pi0*(pi1-theta)] if pi1>theta,
      (r0+r1)*[pi1*(theta-pi1)] if pi1<theta.
    At theta==pi1 the physical information value has no finite zero.
    """
    u, d, r0, r1 = _parameters(up_rate, down_rate, reward_zero, reward_one)
    t = float(lag)
    if not math.isfinite(t) or t < 0:
        raise ValueError("lag must be finite and nonnegative")
    pi1 = u / (u + d)
    pi0 = 1 - pi1
    theta = r0 / (r0 + r1)
    a = (r0 + r1) * pi0 * pi1
    b = (r0 + r1) * (
        pi0 * (pi1 - theta) if pi1 >= theta
        else pi1 * (theta - pi1)
    )
    return max(0.0, a * math.exp(-(u + d) * t) - b)


def last_profitable_cue_age(
    up_rate: float,
    down_rate: float,
    reward_zero: float,
    reward_one: float,
    *,
    cue_use_cost: float = 0.0,
) -> float:
    """Exclusive lag horizon for value(t)>cue_use_cost.

    Returns 0 when no lag is beneficial, inf when always positive at every
    finite lag (zero cost and prior exactly on action threshold). A cue-use
    cost here is an additive *per-decision reward debit*, NOT an inherited
    architecture's log-fitness maintenance cost.
    """
    u, d, r0, r1 = _parameters(up_rate, down_rate, reward_zero, reward_one)
    kcost = float(cue_use_cost)
    if not math.isfinite(kcost) or kcost < 0:
        raise ValueError("cue_use_cost must be finite and nonnegative")
    pi1 = u / (u + d)
    pi0 = 1 - pi1
    theta = r0 / (r0 + r1)
    amplitude = (r0 + r1) * pi0 * pi1
    offset = (r0 + r1) * (
        pi0 * (pi1 - theta) if pi1 >= theta
        else pi1 * (theta - pi1)
    )
    target = offset + kcost
    if target >= amplitude:
        return 0.0
    if target == 0.0:
        return math.inf
    return math.log(amplitude / target) / (u + d)
