"""Dynamic two-state ecological decision: selective refresh vs fixed refresh.

State X follows a stationary binary CTMC (0->1 at alpha, 1->0 at beta).
At time -cue_age a prior observation of X was acquired, optionally with\na symmetric binary error rate old_cue_error_rate. At time 0,
the agent may skip or refresh *conditional on that previous observation*.
Skipping acts after terminal_delay. Refreshing waits sampling_delay, observes
the current X perfectly, then acts after terminal_delay. The environment
may change during either period. Payoff is reward0/reward1 for a correct
terminal-state action, zero otherwise; environmental opportunity survives
independently with exponential hazard opportunity_hazard. Every attempted
refresh incurs additive query_cost in immediate expected-reward units.

This model has a *moving world*; it is not the static deterministic C_A/C_F
frontier theorem, nor evidence of a heritable evolved sensing architecture.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


def _probability_one(start: float, lag: float, alpha: float, beta: float) -> float:
    pi1 = alpha / (alpha + beta)
    return pi1 + (start - pi1) * math.exp(-(alpha + beta) * lag)


def _optimal_reward(probability_one: float, reward0: float, reward1: float) -> float:
    return max(reward0 * (1.0 - probability_one), reward1 * probability_one)


@dataclass(frozen=True)
class SelectiveRefreshResult:
    skip_by_old_cue: tuple[float, float]
    refresh_by_old_cue: tuple[float, float]
    selective_policy: tuple[str, str]
    selective_expected_reward: float
    best_precommitted_policy: str
    best_precommitted_reward: float
    strict_conditional_gain: float
    uniform_skip_reward: float
    uniform_refresh_reward: float


def selective_refresh(
    alpha: float,
    beta: float,
    *,
    cue_age: float,
    sampling_delay: float,
    terminal_delay: float,
    opportunity_hazard: float,
    reward0: float = 1.0,
    reward1: float = 1.0,
    query_cost: float = 0.0,
    old_cue_error_rate: float = 0.0,
) -> SelectiveRefreshResult:
    """Exact two-stage Bayes optimization over refresh/skip scheduling.

    Fixed comparator: commit to always refresh or never refresh before the
    previous cue's outcome is seen; each may still choose the terminal action
    optimally using its available cue(s). All have the same old observation.

    query_cost is paid whenever refresh is attempted, even if the opportunity
    closes before completion. No future rewards or population-genetic fitness.
    """
    values = (alpha, beta, cue_age, sampling_delay, terminal_delay,
              opportunity_hazard, reward0, reward1, query_cost,
              old_cue_error_rate)
    if not all(math.isfinite(float(x)) for x in values):
        raise ValueError("all parameters must be finite")
    if min(alpha, beta, reward0, reward1) <= 0:
        raise ValueError("switching rates and correct-action rewards must be >0")
    if min(cue_age, sampling_delay, terminal_delay,
           opportunity_hazard, query_cost) < 0:
        raise ValueError("time, hazard and query cost must be nonnegative")
    if not 0.0 <= old_cue_error_rate <= 0.5:
        raise ValueError("old_cue_error_rate must be between zero and one half")
    if not math.isfinite(alpha + beta) or not math.isfinite(reward0 + reward1):
        raise ValueError("rate and reward sums must be finite")

    pi1 = alpha / (alpha + beta)
    error = old_cue_error_rate
    probability_old_observation_one = pi1 * (1 - error) + (1 - pi1) * error
    observation_probabilities = (
        1 - probability_old_observation_one,
        probability_old_observation_one,
    )
    initial_state_posteriors = (
        pi1 * error / observation_probabilities[0],
        pi1 * (1 - error) / observation_probabilities[1],
    )
    survival_skip = math.exp(-opportunity_hazard * terminal_delay)
    survival_refresh = math.exp(
        -opportunity_hazard * (sampling_delay + terminal_delay)
    )
    final_reward_after_new_signal = tuple(
        _optimal_reward(
            _probability_one(new, terminal_delay, alpha, beta),
            reward0, reward1,
        )
        for new in (0, 1)
    )
    skip = []
    refresh = []
    for observed_old, posterior_at_cue in enumerate(initial_state_posteriors):
        old_posterior = _probability_one(
            posterior_at_cue, cue_age + terminal_delay, alpha, beta
        )
        skip.append(
            survival_skip * _optimal_reward(old_posterior, reward0, reward1)
        )
        probability_new_one = _probability_one(
            posterior_at_cue, cue_age + sampling_delay, alpha, beta
        )
        refresh.append(
            survival_refresh * (
                (1 - probability_new_one) * final_reward_after_new_signal[0]
                + probability_new_one * final_reward_after_new_signal[1]
            ) - query_cost
        )

    p0, p1 = observation_probabilities
    fixed_skip = p0 * skip[0] + p1 * skip[1]
    fixed_refresh = p0 * refresh[0] + p1 * refresh[1]
    adaptive = p0 * max(skip[0], refresh[0]) + p1 * max(skip[1], refresh[1])
    fixed = max(fixed_skip, fixed_refresh)
    return SelectiveRefreshResult(
        tuple(skip), tuple(refresh),
        tuple("refresh" if new > old else "skip"
              for old, new in zip(skip, refresh)),
        adaptive,
        "skip" if fixed_skip >= fixed_refresh else "refresh",
        fixed,
        max(0.0, adaptive - fixed),
        fixed_skip,
        fixed_refresh,
    )
