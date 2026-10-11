"""Exact binary continuous-time environmental cue decision value.

Contrasts statistical state information with its incremental *optimal action*
value. These results assume stationary ecological occupancy and a symmetric
correct-action reward, not evolving sensing architecture or biological fitness.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


def _rates(up_rate: float, down_rate: float) -> tuple[float, float]:
    values = (float(up_rate), float(down_rate))
    if not all(math.isfinite(v) and v > 0 for v in values):
        raise ValueError("both switching rates must be finite and strictly positive")
    return values


def _lag(lag: float) -> float:
    lag = float(lag)
    if not math.isfinite(lag) or lag < 0:
        raise ValueError("lag must be finite and nonnegative")
    return lag


def stationary_probability_one(up_rate: float, down_rate: float) -> float:
    """0 -> 1 at up_rate, 1 -> 0 at down_rate."""
    u, d = _rates(up_rate, down_rate)
    return u / (u + d)


def conditional_probability_one(initial_state: int, lag: float,
                                up_rate: float, down_rate: float) -> float:
    u, d = _rates(up_rate, down_rate)
    t = _lag(lag)
    if initial_state not in (0, 1):
        raise ValueError("initial_state must be 0 or 1")
    pi1 = u / (u + d)
    z = math.exp(-(u + d) * t)
    return pi1 + (float(initial_state) - pi1) * z


@dataclass(frozen=True)
class DecisionExpiryReceipt:
    lag: float
    stationary_one: float
    conditional_one_after_zero: float
    conditional_one_after_one: float
    action_after_zero: int
    action_after_one: int
    blind_action: int
    blind_accuracy: float
    optimal_cue_accuracy: float
    decision_value: float
    mutual_information_nats: float
    finite_expiry_time: float | None


def finite_action_value_expiry(up_rate: float, down_rate: float) -> float | None:
    """First lag after which a symmetric-payoff binary optimal action ignores cue.

    None means exact finite extinction does not occur (symmetric prior).
    """
    u, d = _rates(up_rate, down_rate)
    pi1 = u / (u + d)
    major = max(pi1, 1 - pi1)
    minor = 1 - major
    if math.isclose(major, minor, abs_tol=0.0, rel_tol=1e-14):
        return None
    return math.log(2 * major / (major - minor)) / (u + d)


def _kl_bernoulli(p: float, q: float) -> float:
    first = 0.0 if p <= 0 else p * math.log(p / q)
    second = 0.0 if p >= 1 else (1 - p) * math.log((1 - p) / (1 - q))
    return first + second


def decision_receipt(lag: float, up_rate: float, down_rate: float) -> DecisionExpiryReceipt:
    """Bayes-optimal action under symmetric 0/1 correct-classification reward.

    State at observation is sampled from the stationary distribution. Neither
    actor can query again. At probability 0.5 an arbitrary tie chooses state 1.
    """
    t = _lag(lag)
    u, d = _rates(up_rate, down_rate)
    pi1 = u / (u + d)
    p0 = conditional_probability_one(0, t, u, d)
    p1 = conditional_probability_one(1, t, u, d)
    a0, a1 = (int(p0 >= .5), int(p1 >= .5))
    accuracy = ((1 - pi1) * max(p0, 1 - p0)
                + pi1 * max(p1, 1 - p1))
    blind = max(pi1, 1 - pi1)
    value = max(0.0, accuracy - blind)
    mi = ((1 - pi1) * _kl_bernoulli(p0, pi1)
          + pi1 * _kl_bernoulli(p1, pi1))
    return DecisionExpiryReceipt(t, pi1, p0, p1, a0, a1,
                                 int(pi1 >= .5), blind, accuracy,
                                 value, max(0.0, mi),
                                 finite_action_value_expiry(u, d))
