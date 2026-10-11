"""A comparator sensitivity model for context staleness in contingent sensing.

This does not replace the exact finite C_A/C_F theorem: C_F compares against
a universal fixed bundle, while this module compares a distinct preindexed
repertoire P against a currently refreshed context-routing architecture A.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


def _nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def _unit_interval(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} must be finite and in [0, 1]")
    return value


def stale_context_probability(turnover_rate: float, memory_lag: float) -> float:
    """P(current context differs from remembered context).

    Binary symmetric continuous-time Markov context; the earlier context was
    observed perfectly memory_lag before behavioral commitment. The current
    state disagrees with the old one with probability at most one half.
    """
    rate = _nonnegative("turnover_rate", turnover_rate)
    lag = _nonnegative("memory_lag", memory_lag)
    return -0.5 * math.expm1(-2.0 * rate * lag)


@dataclass(frozen=True)
class ContextValue:
    """Expected timely success fractions for A versus P."""

    context_flip_probability: float
    adaptive: float
    preindexed: float
    advantage: float


def completion_comparator(
    *,
    context_flip_probability: float,
    opportunity_hazard: float,
    routing_time: float,
    terminal_time: float,
    stale_relative_success: float = 0.0,
) -> ContextValue:
    """Compare runtime opportunity value of two declared architectures.

    A refreshes the present context for routing_time and then acquires the
    context-appropriate terminal cue for terminal_time. P uses the terminal
    program selected by an earlier context observation. A stale program earns
    a fraction stale_relative_success of the normal timely payoff. P cannot
    re-query or detect staleness: allowing that defines a different policy.
    Conditional opportunity survival is exponential with opportunity_hazard.
    This is modeled performance, not measured biological fitness.
    """
    q = _unit_interval("context_flip_probability", context_flip_probability)
    mu = _nonnegative("opportunity_hazard", opportunity_hazard)
    r = _nonnegative("routing_time", routing_time)
    a = _nonnegative("terminal_time", terminal_time)
    f = _unit_interval("stale_relative_success", stale_relative_success)
    a_reward = math.exp(-mu * (r + a))
    p_reward = (1.0 - q * (1.0 - f)) * math.exp(-mu * a)
    return ContextValue(q, a_reward, p_reward, a_reward - p_reward)


def critical_staleness(
    *,
    opportunity_hazard: float,
    routing_time: float,
    terminal_time: float = 0.0,
    stale_relative_success: float = 0.0,
    reward_value: float = 1.0,
    additive_control_cost: float = 0.0,
) -> float | None:
    """q threshold for strictly positive additive A-minus-P benefit.

    A return of None means that no q in [0,1] repays the controller. In the
    symmetric Markov context, feasible finite positive q is further below 0.5.
    """
    mu = _nonnegative("opportunity_hazard", opportunity_hazard)
    r = _nonnegative("routing_time", routing_time)
    a = _nonnegative("terminal_time", terminal_time)
    f = _unit_interval("stale_relative_success", stale_relative_success)
    v = _nonnegative("reward_value", reward_value)
    k = _nonnegative("additive_control_cost", additive_control_cost)
    if v == 0.0 or f == 1.0:
        return None
    e = math.exp(-mu * a)
    if e == 0.0:
        return None
    threshold = (-math.expm1(-mu * r) + k / (v * e)) / (1.0 - f)
    return threshold if threshold < 1.0 else None


def log_selection_a_vs_p(
    value: ContextValue,
    *,
    baseline_fitness: float,
    reward_value: float = 1.0,
    log_maintenance_difference: float = 0.0,
) -> float:
    """Log selection of A over P for W_j=e^-kappa_j(w0+v*value_j)."""
    w0 = float(baseline_fitness)
    if not math.isfinite(w0) or w0 <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    v = _nonnegative("reward_value", reward_value)
    d = float(log_maintenance_difference)
    if not math.isfinite(d):
        raise ValueError("log_maintenance_difference must be finite")
    return (math.log(w0 + v * value.adaptive)
            - math.log(w0 + v * value.preindexed) - d)


def coupled_volatility_net_gain(
    *,
    turnover_rate: float,
    memory_lag: float,
    hazard_per_turnover: float,
    routing_time: float,
    terminal_time: float,
    stale_relative_success: float = 0.0,
    reward_value: float = 1.0,
    additive_control_cost: float = 0.0,
) -> float:
    """A minus P when opportunity hazard is assumed to be alpha * turnover.

    This is an illustrative ecological coupling, not an empirically estimated
    relation. Additive controller cost is in expected-reward units, not log
    fitness units.
    """
    nu = _nonnegative("turnover_rate", turnover_rate)
    lag = _nonnegative("memory_lag", memory_lag)
    alpha = _nonnegative("hazard_per_turnover", hazard_per_turnover)
    v = _nonnegative("reward_value", reward_value)
    k = _nonnegative("additive_control_cost", additive_control_cost)
    value = completion_comparator(
        context_flip_probability=stale_context_probability(nu, lag),
        opportunity_hazard=alpha * nu,
        routing_time=routing_time,
        terminal_time=terminal_time,
        stale_relative_success=stale_relative_success,
    )
    return v * value.advantage - k


def coupled_never_advantage(
    *,
    memory_lag: float,
    hazard_per_turnover: float,
    routing_time: float,
    stale_relative_success: float = 0.0,
) -> bool:
    """Exact no-positive-performance condition for the coupled model.

    A cannot exceed P in timely performance for any nu>=0 exactly when
    (1-f)*memory_lag <= hazard_per_turnover*routing_time. Otherwise it
    exceeds P for sufficiently small positive nu, before controller cost.
    """
    delta = _nonnegative("memory_lag", memory_lag)
    alpha = _nonnegative("hazard_per_turnover", hazard_per_turnover)
    r = _nonnegative("routing_time", routing_time)
    f = _unit_interval("stale_relative_success", stale_relative_success)
    return delta * (1.0 - f) <= alpha * r
