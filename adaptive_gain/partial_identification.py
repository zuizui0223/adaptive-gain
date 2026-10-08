"""Sharp nonparametric bounds on a binary action's binary outcome effect.

A is a binary self-selected action (e.g. actively purchasing a cue), Y
is a binary observed outcome (e.g. correct choice). Under consistency
and stable potential outcomes, but NO ignorability / randomization or
monotone treatment effects, calculate the sharp Manski missing-
counterfactual bounds for E[Y(1)-Y(0)].

The bounds quantify NON-identification, not the causal benefit of
observed requesting. They cannot replace an informative/sham randomized
intervention nor identify fitness effects of evolved architectures.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BinaryActionBounds:
    n: int
    action_count: int
    no_action_count: int
    action_success_count: int
    no_action_success_count: int
    observed_action_success_rate: float | None
    observed_no_action_success_rate: float | None
    naive_conditional_difference: float | None
    ate_lower: float
    ate_upper: float


def binary_action_accuracy_bounds(
    action_success: int,
    action_failure: int,
    no_action_success: int,
    no_action_failure: int,
) -> BinaryActionBounds:
    """Sharp finite-sample potential-outcome completion bounds.

    The unobserved Y(0) of every action-taking encounter and unobserved
    Y(1) of every action-avoiding encounter can be assigned arbitrarily
    to 0 or 1. The lower bound chooses Y(1)=0 for all unexposed and
    Y(0)=1 for all exposed; the upper bound reverses those choices.
    These extreme completions are feasible and attain the bounds.

    Inputs are nonnegative integer cell counts for 2x2 (A,Y). No
    stochastic confidence interval is computed; uncertainty is
    identification uncertainty from missing counterfactual outcomes.
    """
    items = (action_success, action_failure,
             no_action_success, no_action_failure)
    if any(not isinstance(v, int) or isinstance(v, bool) or v < 0
           for v in items):
        raise ValueError("all four outcome-by-action counts must be nonnegative integers")
    a1y1, a1y0, a0y1, a0y0 = items
    n_action = a1y1 + a1y0
    n_no_action = a0y1 + a0y0
    n = n_action + n_no_action
    if n == 0:
        raise ValueError("at least one observation is required")
    treated_rate = a1y1/n_action if n_action else None
    control_rate = a0y1/n_no_action if n_no_action else None
    naive = (
        treated_rate-control_rate
        if treated_rate is not None and control_rate is not None
        else None
    )
    lower = (a1y1 - a0y1 - n_action)/n
    upper = (a1y1 + n_no_action - a0y1)/n
    return BinaryActionBounds(
        n=n,
        action_count=n_action,
        no_action_count=n_no_action,
        action_success_count=a1y1,
        no_action_success_count=a0y1,
        observed_action_success_rate=treated_rate,
        observed_no_action_success_rate=control_rate,
        naive_conditional_difference=naive,
        ate_lower=lower,
        ate_upper=upper,
    )
