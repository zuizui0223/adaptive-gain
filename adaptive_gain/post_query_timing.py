"""Two-stage ecological information control with optimal post-query timing.

An old noisy observation O reports a past binary Markov environmental state.
At commitment, an agent may:
  P: use O and wait any t in [0,T] without new observation, then act;
  Q: spend fixed sampling time r<=T, purchase a noisy new observation Y of
     X(r) at cost K, choose an additional delay d(Y,O) in [0,T-r],
     and finally take its Bayes-optimal terminal action.

Opportunity remains available to time t with probability exp(-mu*t).
State continues to switch during all acquisition and action delays.

The comparison is explicitly against an OLD-CUE-CONDITIONAL passive-timing
controller and universal Q. A real evolved sensor/control cost, genotype
fitness effect, multi-round sensing and disturbance from measuring the
environment are not identified here.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from .optimal_passive_wait import passive_timing_optimum


@dataclass(frozen=True)
class PostQueryTimingReceipt:
    old_report_weights: tuple[float, float]
    optimal_passive_delay_by_old_report: tuple[float, float]
    passive_reward_by_old_report: tuple[float, float]
    query_reward_by_old_report: tuple[float, float]
    query_report_probabilities: tuple[tuple[float, float], tuple[float, float]]
    postquery_delay_by_old_and_new_report: tuple[
        tuple[float | None, float | None],
        tuple[float | None, float | None],
    ]
    acquisition_policy_by_old_report: tuple[str, str]
    best_passive_reward: float
    universal_query_reward: float
    conditional_policy_reward: float
    query_access_value: float
    conditional_query_premium: float


def query_then_optimal_timing(
    alpha: float,
    beta: float,
    *,
    cue_age: float,
    sampling_delay: float,
    terminal_delay: float,
    max_total_wait: float,
    opportunity_hazard: float,
    reward0: float,
    reward1: float,
    query_cost: float,
    old_cue_error_rate: float = 0.0,
    refresh_cue_error_rate: float = 0.0,
) -> PostQueryTimingReceipt:
    """Bayes-optimal three-stage query and terminal timing for a fixed horizon.

    Per-old-report branches are optimized exactly using the CTMC's
    endpoint/stationary-point passive-timing calculation. For a new label
    with probability zero, its post-query delay is None and it contributes
    zero to expected reward. A higher signal error only worsens a
    Blackwell-ordered experiment at unchanged elapsed time and cost.
    """
    values = (alpha, beta, cue_age, sampling_delay, terminal_delay,
              max_total_wait, opportunity_hazard, reward0, reward1,
              query_cost, old_cue_error_rate, refresh_cue_error_rate)
    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("all parameters must be finite")
    if min(alpha, beta, reward0, reward1) <= 0:
        raise ValueError("rates and correct-action rewards must be positive")
    if min(cue_age, sampling_delay, terminal_delay,
           opportunity_hazard, query_cost) < 0:
        raise ValueError("times, hazard and acquisition cost must be nonnegative")
    if max_total_wait < sampling_delay:
        raise ValueError("max_total_wait must include sampling_delay")
    if not 0 <= old_cue_error_rate <= .5:
        raise ValueError("old_cue_error_rate must lie in [0,0.5]")
    if not 0 <= refresh_cue_error_rate <= .5:
        raise ValueError("refresh_cue_error_rate must lie in [0,0.5]")
    if not math.isfinite(alpha + beta) or not math.isfinite(reward0 + reward1):
        raise ValueError("rate/reward sums must be finite")

    pi1 = alpha / (alpha + beta)
    pi0 = 1 - pi1
    eps_old = old_cue_error_rate
    w1 = pi1 * (1 - eps_old) + pi0 * eps_old
    weights = (1 - w1, w1)
    posterior = (pi1 * eps_old / weights[0],
                 pi1 * (1 - eps_old) / weights[1])

    def transition(p: float, elapsed: float) -> float:
        return pi1 + (p - pi1) * math.exp(-(alpha + beta) * elapsed)

    passive = []
    query = []
    reporting = []
    post_delays = []
    for prior_at_old in posterior:
        passive_outcome = passive_timing_optimum(
            posterior_at_old_cue=prior_at_old,
            alpha=alpha, beta=beta,
            cue_age=cue_age,
            terminal_delay=terminal_delay,
            max_wait=max_total_wait,
            opportunity_hazard=opportunity_hazard,
            reward0=reward0, reward1=reward1,
        )
        passive.append(passive_outcome)
        p_now = transition(prior_at_old, cue_age + sampling_delay)
        likelihood = []
        delays = []
        total_after_query = 0.0
        for y in (0, 1):
            probability_y = (
                (1 - p_now) * (1 - refresh_cue_error_rate if y == 0 else refresh_cue_error_rate)
                + p_now * (1 - refresh_cue_error_rate if y == 1 else refresh_cue_error_rate)
            )
            likelihood.append(probability_y)
            if probability_y <= 0:
                delays.append(None)
                continue
            posterior1 = p_now * (
                (1 - refresh_cue_error_rate) if y == 1 else refresh_cue_error_rate
            ) / probability_y
            continuation = passive_timing_optimum(
                posterior_at_old_cue=posterior1,
                alpha=alpha, beta=beta,
                cue_age=0,
                terminal_delay=terminal_delay,
                max_wait=max_total_wait-sampling_delay,
                opportunity_hazard=opportunity_hazard,
                reward0=reward0, reward1=reward1,
            )
            delays.append(continuation.wait_duration)
            total_after_query += probability_y * continuation.expected_reward
        query.append(
            math.exp(-opportunity_hazard * sampling_delay)
            * total_after_query - query_cost
        )
        reporting.append(tuple(likelihood))
        post_delays.append(tuple(delays))

    M = tuple(v.expected_reward for v in passive)
    Q = tuple(query)
    weights = tuple(weights)
    noquery_value = sum(weights[o]*M[o] for o in (0, 1))
    universal_query = sum(weights[o]*Q[o] for o in (0, 1))
    conditional = sum(weights[o]*max(M[o], Q[o]) for o in (0, 1))
    return PostQueryTimingReceipt(
        old_report_weights=weights,
        optimal_passive_delay_by_old_report=tuple(v.wait_duration for v in passive),
        passive_reward_by_old_report=M,
        query_reward_by_old_report=Q,
        query_report_probabilities=tuple(reporting),
        postquery_delay_by_old_and_new_report=tuple(post_delays),
        acquisition_policy_by_old_report=tuple(
            "query" if Q[o] > M[o] else "passive" for o in (0, 1)
        ),
        best_passive_reward=noquery_value,
        universal_query_reward=universal_query,
        conditional_policy_reward=conditional,
        query_access_value=max(0.0, conditional-noquery_value),
        conditional_query_premium=max(
            0.0, conditional-max(noquery_value, universal_query)
        ),
    )
