"""Separate moving-environment wait value from fresh-cue information value.

Counterfactuals for a stationary two-state Markov ecology:
S: act without refresh after terminal_delay;
W: wait sampling_delay with NO new observation or query cost, then act;
Q: spend the same sampling_delay gathering a noisy fresh observation,
   pay per-query cost, then act optimally using both old and fresh cues.

The W control prevents rewarding a "query" for the passage of time alone.
All rewards are one-encounter performance, not measured population fitness.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from .selective_refresh import selective_refresh


@dataclass(frozen=True)
class WaitingControlReceipt:
    old_report_weights: tuple[float, float]
    skip_by_old_report: tuple[float, float]
    wait_without_cue_by_old_report: tuple[float, float]
    query_with_cue_by_old_report: tuple[float, float]
    gross_fresh_information_value_by_old_report: tuple[float, float]
    net_query_over_wait_by_old_report: tuple[float, float]
    no_query_timing_policy: tuple[str, str]
    conditional_query_policy: tuple[str, str]
    best_no_query_timing_reward: float
    universal_query_reward: float
    conditional_query_reward: float
    query_access_gain: float
    conditional_query_premium: float
    timing_only_conditional_premium: float
    best_fixed_three_schedule_reward: float
    conditional_three_vs_fixed_three_gain: float
    original_two_schedule_premium: float


def waiting_control_decomposition(
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
    refresh_cue_error_rate: float = 0.0,
) -> WaitingControlReceipt:
    """Bayes-optimal SKIP / WAIT / QUERY decomposition.

    A sensor-specific conditional premium compares conditional query use
    against *both* (i) a no-query controller allowed to switch between
    skip and waiting after seeing the old report and (ii) universal
    querying with optimized post-query action. Thus the information
    premium is identically zero when the fresh cue is uninformative
    and acquisition costs are nonnegative.

    The broader three-schedule comparison separately tests conditional
    control over skip/wait/query versus a choice of one global schedule.
    It can remain positive for an uninformative fresh cue because waiting
    schedules differ by old report. Do not call this information value.
    """
    primitive = selective_refresh(
        alpha, beta,
        cue_age=cue_age, sampling_delay=sampling_delay,
        terminal_delay=terminal_delay,
        opportunity_hazard=opportunity_hazard,
        reward0=reward0, reward1=reward1,
        query_cost=query_cost,
        old_cue_error_rate=old_cue_error_rate,
        refresh_cue_error_rate=refresh_cue_error_rate,
    )
    pi1 = alpha / (alpha + beta)
    pi0 = 1 - pi1
    error = old_cue_error_rate
    p_report1 = pi1 * (1 - error) + pi0 * error
    weights = (1 - p_report1, p_report1)
    post = (
        pi1 * error / weights[0],
        pi1 * (1 - error) / weights[1],
    )

    def state1_after(p: float, t: float) -> float:
        return pi1 + (p - pi1) * math.exp(-(alpha + beta) * t)

    def terminal_value(p: float) -> float:
        return max(reward0 * (1 - p), reward1 * p)

    wait = tuple(
        math.exp(-opportunity_hazard * (sampling_delay + terminal_delay))
        * terminal_value(
            state1_after(p, cue_age + sampling_delay + terminal_delay)
        )
        for p in post
    )
    skip = primitive.skip_by_old_cue
    query = primitive.refresh_by_old_cue
    gross_info = tuple(query[i] + query_cost - wait[i] for i in (0, 1))
    # A signal can always be ignored; tiny negative discrepancies are
    # floating-point roundoff, but a larger negative is an implementation bug.
    if min(gross_info) < -1e-10:
        raise ArithmeticError("a fresh observation degraded information value")
    gross_info = tuple(max(0.0, x) for x in gross_info)
    net_over_wait = tuple(query[i] - wait[i] for i in (0, 1))
    no_query = tuple(max(skip[i], wait[i]) for i in (0, 1))

    def mean(v: tuple[float, float]) -> float:
        return sum(weights[i] * v[i] for i in (0, 1))

    timed = mean(no_query)
    always_query = mean(query)
    cond_query = sum(
        weights[i] * max(no_query[i], query[i]) for i in (0, 1)
    )
    best_fixed_three = max(mean(skip), mean(wait), always_query)
    conditional_three = sum(
        weights[i] * max(skip[i], wait[i], query[i])
        for i in (0, 1)
    )
    timing_only = timed - max(mean(skip), mean(wait))
    access = cond_query - timed
    conditional_query_premium = cond_query - max(timed, always_query)

    # All analytically nonnegative amounts may have tiny negative
    # machine error near indifference; clamp only that roundoff.
    if min(timing_only, access, conditional_query_premium) < -1e-10:
        raise ArithmeticError("baseline containment violated")
    return WaitingControlReceipt(
        old_report_weights=weights,
        skip_by_old_report=skip,
        wait_without_cue_by_old_report=wait,
        query_with_cue_by_old_report=query,
        gross_fresh_information_value_by_old_report=gross_info,
        net_query_over_wait_by_old_report=net_over_wait,
        no_query_timing_policy=tuple(
            "wait" if wait[i] > skip[i] else "skip" for i in (0, 1)
        ),
        conditional_query_policy=tuple(
            "query" if query[i] > no_query[i] else
            ("wait" if wait[i] > skip[i] else "skip")
            for i in (0, 1)
        ),
        best_no_query_timing_reward=timed,
        universal_query_reward=always_query,
        conditional_query_reward=cond_query,
        query_access_gain=max(0.0, access),
        conditional_query_premium=max(0.0, conditional_query_premium),
        timing_only_conditional_premium=max(0.0, timing_only),
        best_fixed_three_schedule_reward=best_fixed_three,
        conditional_three_vs_fixed_three_gain=max(
            0.0, conditional_three - best_fixed_three
        ),
        original_two_schedule_premium=primitive.strict_conditional_gain,
    )
