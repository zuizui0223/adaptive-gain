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



@dataclass(frozen=True)
class TimingAdjustedPrecisionReceipt:
    """Genuine query-control window against an explicit wait-only alternative."""
    lower_error: float | None
    upper_error: float | None
    peak_error: float | None
    peak_query_control_premium: float
    no_query_timing_reward_at_peak: float
    query_fixed_tie_at_peak: bool
    peak_on_boundary: bool


def timing_adjusted_precision_window(
    *,
    iterations: int = 70,
    **parameters,
) -> TimingAdjustedPrecisionReceipt:
    """Numerically solve the unimodal query premium after WAIT is allowed.

    The old observation can control SKIP or WAIT without ever querying:
    M_o=max(S_o,W_o). A true selective-query controller may instead choose
    Q_o. Both M and Q are compared against universal querying. Along
    symmetric-binary refreshed-cue garbling, Q_o is nonincreasing.
    The timing-adjusted strict premium is
       min(sum w_o(Q_o-M_o)_+, sum w_o(M_o-Q_o)_+).
    Its max is at the fixed-comparator tie if such a tie lies inside
    the strict positive interval.

    This numerical root search is not interval-arithmetic verification.
    """
    if iterations < 1 or iterations > 1000:
        raise ValueError("iterations must lie in [1,1000]")
    if "refresh_cue_error_rate" in parameters:
        raise ValueError("refresh_cue_error_rate is the optimization axis")

    def at(error: float) -> WaitingControlReceipt:
        return waiting_control_decomposition(
            refresh_cue_error_rate=error, **parameters
        )

    def delta(error: float, report: int) -> float:
        x = at(error)
        return (
            x.query_with_cue_by_old_report[report]
            - max(x.skip_by_old_report[report],
                  x.wait_without_cue_by_old_report[report])
        )

    def root(report: int) -> float:
        lower, upper = 0.0, 0.5
        if delta(lower, report) <= 0:
            return lower
        if delta(upper, report) >= 0:
            return upper
        for _ in range(iterations):
            mid = (lower + upper) / 2
            if delta(mid, report) > 0:
                lower = mid
            else:
                upper = mid
        return (lower + upper) / 2

    roots = (root(0), root(1))
    lower, upper = min(roots), max(roots)
    if upper - lower < 1e-12:
        return TimingAdjustedPrecisionReceipt(
            None, None, None, 0.0, 0.0, False, False
        )

    def fixed_difference(err: float) -> float:
        x = at(err)
        return (
            x.universal_query_reward - x.best_no_query_timing_reward
        )

    is_boundary = False
    if fixed_difference(lower) <= 0:
        peak = lower
        is_boundary = True
    elif fixed_difference(upper) >= 0:
        peak = upper
        is_boundary = True
    else:
        left, right = lower, upper
        for _ in range(iterations):
            mid = (left + right) / 2
            if fixed_difference(mid) > 0:
                left = mid
            else:
                right = mid
        peak = (left + right) / 2

    x = at(peak)
    return TimingAdjustedPrecisionReceipt(
        lower, upper, peak,
        x.conditional_query_premium,
        x.best_no_query_timing_reward,
        math.isclose(fixed_difference(peak), 0, abs_tol=1e-9),
        is_boundary,
    )


def timing_adjusted_log_maintenance_ceiling(
    *,
    baseline_fitness: float,
    iterations: int = 70,
    **parameters,
) -> float:
    """Largest pairwise log maintenance debit payable by true query control.

    This keeps the no-query comparator allowed to conditionally WAIT or SKIP
    based on the old report. Constitutive controller cost is separate from
    per-query debit already present in Q.
    """
    w0 = float(baseline_fitness)
    if not math.isfinite(w0) or w0 <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    window = timing_adjusted_precision_window(
        iterations=iterations, **parameters
    )
    if window.peak_error is None:
        return 0.0
    x = waiting_control_decomposition(
        refresh_cue_error_rate=window.peak_error, **parameters
    )
    alternative = max(
        x.best_no_query_timing_reward,
        x.universal_query_reward,
    )
    if w0 + alternative <= 0:
        raise ValueError("comparator gross fitness is not positive")
    return math.log1p(
        x.conditional_query_premium / (w0 + alternative)
    )
