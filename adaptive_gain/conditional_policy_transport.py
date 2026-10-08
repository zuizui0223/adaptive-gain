"""Conditional cue policy under deployment old-report frequency shift.

A two-report, two-acquisition-policy comparison with FIXED
old-report-conditional expected reward differences:
  d0 = E[R|old=0, QUERY] - E[R|old=0, PASSIVE] > 0
  d1 = E[R|old=1, PASSIVE] - E[R|old=1, QUERY] > 0.

A conditional policy queries after old report 0 and remains passive after
old report 1. The target probability w=Pr_deployment(old report 0) is
allowed to differ from the laboratory sampling distribution.

The exact advantage against the BETTER fixed program is
  G(w) = min(w*d0, (1-w)*d1).
The optimal target mixture is w*=d1/(d0+d1) with maximum
d0*d1/(d0+d1). An additive, per-encounter-equivalent control cost K
is repaid only when K<max(G) and w lies strictly between K/d0 and
1-K/d1.

These are elementary conditioning/mixture identities, not a new
information-value theorem or naturally evolved sensory strategy.

CRUCIAL: Varying the frequency of old REPORTS while keeping the
conditional advantages d0,d1 fixed is a target *covariate reweighting*
scenario. Changing actual ecological state occupancy usually changes
posterior beliefs, transition probabilities and both d0,d1. The model
is NOT an unconditional ecological-prevalence manipulation theorem.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class ConditionalControlFrequency:
    rare_report_probability: float
    query_after_rare_advantage: float
    skip_after_common_advantage: float
    extra_reward_over_always_passive: float
    extra_reward_over_always_query: float
    extra_reward_over_best_fixed: float


@dataclass(frozen=True)
class MixtureViabilityWindow:
    maximum_gain: float
    target_probability_at_maximum: float
    controller_cost_per_encounter_equivalent: float
    strictly_profitable_old_zero_frequency_interval: tuple[float,float] | None
    interpretation: str


def _finite_positive(name: str, value: float) -> float:
    v=float(value)
    if not math.isfinite(v) or v<=0:
        raise ValueError(f"{name} must be strictly positive and finite")
    return v


def conditional_frequency_gain(
    *,
    old_zero_probability: float,
    query_advantage_given_old_zero: float,
    passive_advantage_given_old_one: float,
) -> ConditionalControlFrequency:
    """Compare a frozen mixed sensing controller to both fixed alternatives."""
    w=float(old_zero_probability)
    if not math.isfinite(w) or not 0<=w<=1:
        raise ValueError("old_zero_probability must belong to [0,1]")
    a=_finite_positive("query_advantage_given_old_zero",
                       query_advantage_given_old_zero)
    b=_finite_positive("passive_advantage_given_old_one",
                       passive_advantage_given_old_one)
    gain_p=w*a
    gain_q=(1-w)*b
    return ConditionalControlFrequency(
        rare_report_probability=w,
        query_after_rare_advantage=a,
        skip_after_common_advantage=b,
        extra_reward_over_always_passive=gain_p,
        extra_reward_over_always_query=gain_q,
        extra_reward_over_best_fixed=min(gain_p,gain_q),
    )


def mixture_viability_window(
    *,
    query_advantage_given_old_zero: float,
    passive_advantage_given_old_one: float,
    additional_controller_cost: float,
) -> MixtureViabilityWindow:
    """Strict additive control profitability in a frozen conditional kernel.

    Cost is expressed in per-encounter-equivalent expected-reward units
    AFTER arm-specific cue/time costs were accounted for in the branch
    rewards. Do not automatically substitute a constitutive log-fitness
    maintenance cost without an encounter-to-fitness conversion.
    """
    a=_finite_positive("query_advantage_given_old_zero",
                       query_advantage_given_old_zero)
    b=_finite_positive("passive_advantage_given_old_one",
                       passive_advantage_given_old_one)
    k=float(additional_controller_cost)
    if not math.isfinite(k) or k<0:
        raise ValueError("additional_controller_cost must be finite and nonnegative")
    wstar=b/(a+b)
    maxgain=a*b/(a+b)
    # An exact threshold can round a few ulps above its caller's binary
    # floating representation (e.g. 0.2*0.05/0.25 vs literal 0.04).
    # Do not manufacture an extremely narrow viability interval at equality.
    feasible=(k<maxgain and not math.isclose(
        k,maxgain,rel_tol=1e-12,abs_tol=1e-15
    ))
    window=(k/a,1-k/b) if feasible else None
    return MixtureViabilityWindow(
        maximum_gain=maxgain,
        target_probability_at_maximum=wstar,
        controller_cost_per_encounter_equivalent=k,
        strictly_profitable_old_zero_frequency_interval=window,
        interpretation=(
            "Frozen conditional reward kernel, target old-REPORT mixture "
            "reweighted; changing ecological state occupancy may also "
            "change conditional reward advantages, invalidating a naive "
            "frequency-only ecological prediction."
        ),
    )
