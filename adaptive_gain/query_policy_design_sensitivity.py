"""Illustrative design-sensitivity arithmetic for a two-old-report assay.

NOT an empirical sample-size prescription. Assumes:
- fixed OLD-report probabilities in deployment (omega);
- deliberately assigned laboratory old-report proportions f0,1-f0;
- fixed probability q of *each* PASSIVE and QUERY assignment given O;
- each reward is an independent Bernoulli trial, with no bee/colony
  effects, period effects, measurement error or learned-policy uncertainty;
- the correct mixed acquisition policy is already known;
- no interference across encounters.

Sham is separately randomized; its allocation affects remaining q.
Two independent, one-sided primary contrasts are conditional-minus-PASSIVE
and conditional-minus-QUERY. Use 97.5% lower bounds for BOTH, and require
a nominal 90% power for EACH to yield >=80% intersection power by a union
bound (no independence between the two tests is assumed).
This is a conservative Gaussian approximation for trial-level contrasts.
A user-supplied multiplicative design-effect sensitivity inflates variance
but is not an ICC estimate. Real sample planning requires colony pilot data.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from statistics import NormalDist


@dataclass(frozen=True)
class QueryPowerSensitivity:
    old_zero_fraction_in_lab: float
    old_zero_fraction_in_target: float
    arm_probability_passive: float
    arm_probability_query: float
    target_joint_power: float
    assumed_variance_design_effect: float
    conditional_minus_passive: float
    conditional_minus_query: float
    variance_coefficient_vs_passive: float
    variance_coefficient_vs_query: float
    approximate_total_trials_for_passive_contrast: int
    approximate_total_trials_for_query_contrast: int
    approximate_total_trials_joint_bonferroni_bound: int
    binding_contrast: str


def _unit_open(name: str,value: float) -> float:
    v=float(value)
    if not math.isfinite(v) or not 0<v<1:
        raise ValueError(f"{name} must be finite and strictly between 0 and 1")
    return v


def _bernoulli_prob(name: str, value: float) -> float:
    v=float(value)
    if not math.isfinite(v) or not 0<=v<=1:
        raise ValueError(f"{name} must be in [0,1]")
    return v


def design_sensitivity(
    *,
    target_old_zero: float,
    laboratory_old_zero: float,
    arm_probability_passive: float,
    arm_probability_query: float,
    success_passive_old_zero: float,
    success_query_old_zero: float,
    success_passive_old_one: float,
    success_query_old_one: float,
    target_joint_power: float = .80,
    familywise_alpha: float = .05,
    assumed_variance_design_effect: float = 1.0,
) -> QueryPowerSensitivity:
    """Conservative approximate total trials under independent Bernoulli toy model.

    A separate SHAM arm uses the remaining randomized probability.
    We assume the fixed conditional policy is QUERY after old zero and
    PASSIVE after old one; both branch-specific differences must be >0.
    Otherwise this canonical scenario is a no-go for the stated policy.
    This calculation is a conditional sensitivity *not* statistical
    identification or a sample size target.
    """
    w0=_unit_open("target_old_zero",target_old_zero)
    f0=_unit_open("laboratory_old_zero",laboratory_old_zero)
    pP=_unit_open("arm_probability_passive",arm_probability_passive)
    pQ=_unit_open("arm_probability_query",arm_probability_query)
    if pP+pQ >= 1:
        raise ValueError("reserve positive assignment probability for sham")
    vals=[
        _bernoulli_prob("success_passive_old_zero",success_passive_old_zero),
        _bernoulli_prob("success_query_old_zero",success_query_old_zero),
        _bernoulli_prob("success_passive_old_one",success_passive_old_one),
        _bernoulli_prob("success_query_old_one",success_query_old_one),
    ]
    p0,q0,p1,q1=vals
    power=_unit_open("target_joint_power",target_joint_power)
    alpha=_unit_open("familywise_alpha",familywise_alpha)
    deff=float(assumed_variance_design_effect)
    if not math.isfinite(deff) or deff<1:
        raise ValueError("assumed_variance_design_effect must be >=1")
    dP=w0*(q0-p0)
    dQ=(1-w0)*(p1-q1)
    if dP<=0 or dQ<=0:
        raise ValueError("hypothetical mixed policy does not beat both fixed regimes")
    variance_P=(w0**2/f0)*(
        q0*(1-q0)/pQ+p0*(1-p0)/pP
    )
    variance_Q=((1-w0)**2/(1-f0))*(
        p1*(1-p1)/pP+q1*(1-q1)/pQ
    )
    # For 2 Bonferroni lower bounds, alpha/2 is each one's size.
    # For joint power >=target, conservative each contrast gets >=
    # 1-(1-target)/2 marginal power (union bound).
    zcrit=NormalDist().inv_cdf(1-alpha/2)
    zpower=NormalDist().inv_cdf(1-(1-power)/2)
    nP=math.ceil(deff*(zcrit+zpower)**2*variance_P/dP**2)
    nQ=math.ceil(deff*(zcrit+zpower)**2*variance_Q/dQ**2)
    return QueryPowerSensitivity(
        old_zero_fraction_in_lab=f0,
        old_zero_fraction_in_target=w0,
        arm_probability_passive=pP,
        arm_probability_query=pQ,
        target_joint_power=power,
        assumed_variance_design_effect=deff,
        conditional_minus_passive=dP,
        conditional_minus_query=dQ,
        variance_coefficient_vs_passive=variance_P,
        variance_coefficient_vs_query=variance_Q,
        approximate_total_trials_for_passive_contrast=nP,
        approximate_total_trials_for_query_contrast=nQ,
        approximate_total_trials_joint_bonferroni_bound=max(nP,nQ),
        binding_contrast=("passive" if nP>=nQ else "query"),
    )


def variance_balancing_old_zero_allocation(
    *,
    target_old_zero: float,
    arm_probability_passive: float,
    arm_probability_query: float,
    success_passive_old_zero: float,
    success_query_old_zero: float,
    success_passive_old_one: float,
    success_query_old_one: float,
) -> float:
    """Oracle f0 balancing two contrast sample-size requirements.

    Requires known true arm-specific Bernoulli probabilities; practical
    designs cannot safely use these before an independent pilot.
    f0 is chosen to equalize the normalized variance-to-signal^2 terms
    for the two primary contrasts, not merely raw variance.
    """
    w0=_unit_open("target_old_zero",target_old_zero)
    a=_unit_open("arm_probability_passive",arm_probability_passive)
    b=_unit_open("arm_probability_query",arm_probability_query)
    if a+b>=1:
        raise ValueError("positive SHAM allocation is required")
    p0,q0,p1,q1=[
        _bernoulli_prob("success probability",v)
        for v in (success_passive_old_zero,success_query_old_zero,
                  success_passive_old_one,success_query_old_one)
    ]
    if q0<=p0 or p1<=q1:
        raise ValueError("no-go for the declared old-report conditional policy")
    C0=w0*w0*(p0*(1-p0)/a+q0*(1-q0)/b)/(w0*(q0-p0))**2
    C1=(1-w0)**2*(p1*(1-p1)/a+q1*(1-q1)/b)/((1-w0)*(p1-q1))**2
    return C0/(C0+C1)
