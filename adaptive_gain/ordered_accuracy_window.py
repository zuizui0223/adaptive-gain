"""Accuracy-ordered conditional re-query envelope and root certificate.

Under fixed acquisition costs/times and a Blackwell ordered family of
refreshed cues, each branch's optimized refresh payoff is nonincreasing
as error rises. Conditional advantage over the BETTER of the two
precommitted schedules is the min of nonincreasing positive option
value P and nondecreasing negative option value N. Therefore the
relative control premium is unimodal (weakly), and its positive
region is an interval. This is an elementary decision-theoretic
consequence and not a new biological selection theorem.

This module computes numerical bisection certificates for the
specific symmetric binary-refresh error family in selective_refresh.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any

from .selective_refresh import selective_refresh


@dataclass(frozen=True)
class AccuracyWindowReceipt:
    lower_error: float | None
    upper_error: float | None
    peak_error: float | None
    peak_conditional_premium: float
    lower_branch: int | None
    upper_branch: int | None
    comparator_tie_at_peak: bool
    peak_on_boundary: bool


def _value(error: float, params: dict[str, Any]):
    return selective_refresh(
        refresh_cue_error_rate=error, **params
    )


def _increment(result, old_report: int) -> float:
    return (
        result.refresh_by_old_cue[old_report]
        - result.skip_by_old_cue[old_report]
    )


def _crossing(
    old_report: int, params: dict[str, Any], *, iterations: int
) -> float:
    """First error with branch refresh advantage <= 0 on [0, 0.5].

    Exactly 0 if already nonpositive at perfect refreshed accuracy;
    exactly 0.5 if positive until uninformative refreshed sensing.
    No claim about floating-point certified interval arithmetic.
    """
    lo, hi = 0.0, 0.5
    if _increment(_value(lo, params), old_report) <= 0:
        return lo
    if _increment(_value(hi, params), old_report) >= 0:
        return hi
    for _ in range(iterations):
        mid = (lo + hi) / 2
        if _increment(_value(mid, params), old_report) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def precision_window(
    *,
    iterations: int = 70,
    **selective_refresh_parameters: Any,
) -> AccuracyWindowReceipt:
    """Locate contingent-value window and peak of relative adaptivity.

    Assumes error in [0,0.5], Blackwell-ordered binary observation,
    fixed nonnegative acquisition cost/time, and two possible old
    observation labels. Returns None boundaries if strict gain is absent
    (up to a specified floating-point tolerance).
    """
    if iterations < 1 or iterations > 1000:
        raise ValueError("iterations must be between 1 and 1000")
    if "refresh_cue_error_rate" in selective_refresh_parameters:
        raise ValueError("refresh_cue_error_rate is optimized, not an input")

    params = dict(selective_refresh_parameters)
    roots = [
        _crossing(i, params, iterations=iterations) for i in (0, 1)
    ]
    order = sorted(range(2), key=lambda j: roots[j])
    low, high = roots[order[0]], roots[order[1]]
    if high - low <= 1e-12:
        return AccuracyWindowReceipt(
            None, None, None, 0.0, None, None, False, False
        )

    def fixed_difference(error: float) -> float:
        result = _value(error, params)
        return result.uniform_refresh_reward - result.uniform_skip_reward

    f_low = fixed_difference(low)
    f_high = fixed_difference(high)

    # This function is nonincreasing by Blackwell degradation. The
    # relative premium is min(P, N), maximized where P=N, equivalently
    # where the two fixed comparator schedules tie, if inside the window.
    is_boundary = False
    if f_low <= 0:
        peak = low
        is_boundary = True
    elif f_high >= 0:
        peak = high
        is_boundary = True
    else:
        left, right = low, high
        for _ in range(iterations):
            mid = (left + right) / 2
            if fixed_difference(mid) > 0:
                left = mid
            else:
                right = mid
        peak = (left + right) / 2

    chosen = _value(peak, params)
    gain = chosen.strict_conditional_gain
    return AccuracyWindowReceipt(
        low, high, peak, gain,
        order[0], order[1],
        math.isclose(fixed_difference(peak), 0, abs_tol=1e-9),
        is_boundary,
    )
