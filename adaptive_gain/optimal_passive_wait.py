"""Exact optimization of no-information action delay in a moving ecology.

The previous waiting_control.py requires a same-duration WAIT comparator
against an optional refreshed observation. An organism may instead choose
a different delay *without sensing*. This module offers the stronger
predeclared wait-horizon competitor.

For each old report, terminal action time is a+t with t in [0,T].
On a stationary binary CTMC, the expected performance from choosing
action j at final time is a sum of two exponentials. Its optimum over
a finite interval is attained at an endpoint or its single stationary
point (if the latter exists). We enumerate these candidates exactly
up to floating-point arithmetic. The terminal action is Bayes-optimal.

No information is acquired during waiting; costs remain nonnegative and
environment state changes while time passes. No population selection claim.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from .waiting_control import waiting_control_decomposition


@dataclass(frozen=True)
class PassiveTimingReceipt:
    """One report's Bayes-optimal passive delay and its expected payoff."""
    wait_duration: float
    expected_reward: float
    considered_times: tuple[float, ...]


@dataclass(frozen=True)
class FlexibleWaitingComparison:
    """Information-specific query gain against freely chosen waiting."""
    old_report_weights: tuple[float, float]
    optimal_no_query_delays: tuple[float, float]
    optimal_no_query_branch_values: tuple[float, float]
    query_branch_values: tuple[float, float]
    conditional_query_policy: tuple[str, str]
    best_no_query_reward: float
    always_query_reward: float
    conditional_query_reward: float
    query_access_gain: float
    conditional_query_premium: float
    matched_wait_query_premium: float


def passive_timing_optimum(
    *,
    posterior_at_old_cue: float,
    alpha: float,
    beta: float,
    cue_age: float,
    terminal_delay: float,
    max_wait: float,
    opportunity_hazard: float,
    reward0: float,
    reward1: float,
) -> PassiveTimingReceipt:
    """Maximize no-query payoff over t in [0, max_wait], exactly for CTMC.

    Validation assumes posterior at old-cue time, continuous waiting
    through a stationary two-state Markov environment, a nonnegative
    independent opportunity hazard, and positive correct-action rewards.
    """
    values=(posterior_at_old_cue, alpha, beta, cue_age, terminal_delay,
            max_wait, opportunity_hazard, reward0, reward1)
    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("all passive-timing parameters must be finite")
    if not 0 <= posterior_at_old_cue <= 1:
        raise ValueError("posterior_at_old_cue must be a probability")
    if min(alpha, beta, reward0, reward1) <= 0:
        raise ValueError("rates and rewards must be positive")
    if min(cue_age, terminal_delay, max_wait, opportunity_hazard) < 0:
        raise ValueError("times and hazard must be nonnegative")
    k=alpha+beta
    if not math.isfinite(k) or not math.isfinite(reward0 + reward1):
        raise ValueError("rate/reward sums must be finite")
    pi1=alpha/k
    pi0=1-pi1
    initial_relax=(posterior_at_old_cue-pi1)*math.exp(
        -k*(cue_age+terminal_delay))
    # For action0: r0 [pi0 - initial_relax*exp(-k*t)] * exp(-mu*t)
    # For action1: r1 [pi1 + initial_relax*exp(-k*t)] * exp(-mu*t)
    terms=(
        (reward0*pi0, -reward0*initial_relax),
        (reward1*pi1, reward1*initial_relax)
    )
    candidates={0.0, float(max_wait)}
    mu=opportunity_hazard
    if mu>0:
        for A,B in terms:
            if B<0:
                z= -mu*A/((mu+k)*B)
                if 0<z<1:
                    stationary=-math.log(z)/k
                    if 0<stationary<max_wait:
                        candidates.add(stationary)
    def value(t: float) -> float:
        p1=pi1+initial_relax*math.exp(-k*t)
        return math.exp(-mu*(terminal_delay+t))*max(
            reward0*(1-p1), reward1*p1
        )
    times=tuple(sorted(candidates))
    best=max(times,key=value)
    return PassiveTimingReceipt(best, value(best), times)


def compare_with_optimal_passive_wait(
    alpha: float,
    beta: float,
    *,
    cue_age: float,
    sampling_delay: float,
    terminal_delay: float,
    opportunity_hazard: float,
    reward0: float,
    reward1: float,
    query_cost: float,
    max_wait: float,
    old_cue_error_rate: float=0.0,
    refresh_cue_error_rate: float=0.0,
) -> FlexibleWaitingComparison:
    """Contrast query option against a stronger NO QUERY WAIT/SKIP policy.

    max_wait must be >= sampling_delay so that this comparator strictly
    contains the matched WAIT control. The no-query actor observes the
    old report and can choose ANY passive wait in [0,max_wait].
    """
    if not math.isfinite(max_wait) or max_wait<sampling_delay:
        raise ValueError("max_wait must cover the query acquisition duration")
    paired=waiting_control_decomposition(
        alpha,beta,cue_age=cue_age,sampling_delay=sampling_delay,
        terminal_delay=terminal_delay,opportunity_hazard=opportunity_hazard,
        reward0=reward0,reward1=reward1,query_cost=query_cost,
        old_cue_error_rate=old_cue_error_rate,
        refresh_cue_error_rate=refresh_cue_error_rate
    )
    weight=paired.old_report_weights
    pi1=alpha/(alpha+beta)
    q=pi1*(1-old_cue_error_rate)+(1-pi1)*old_cue_error_rate
    posterior=(
        pi1*old_cue_error_rate/(1-q),
        pi1*(1-old_cue_error_rate)/q
    )
    optimal=tuple(passive_timing_optimum(
        posterior_at_old_cue=p,alpha=alpha,beta=beta,
        cue_age=cue_age,terminal_delay=terminal_delay,
        max_wait=max_wait,opportunity_hazard=opportunity_hazard,
        reward0=reward0,reward1=reward1
    ) for p in posterior)
    M=tuple(x.expected_reward for x in optimal)
    Q=paired.query_with_cue_by_old_report
    no_query=sum(weight[j]*M[j] for j in (0,1))
    universal_query=sum(weight[j]*Q[j] for j in (0,1))
    contingent=sum(weight[j]*max(M[j],Q[j]) for j in (0,1))
    access=max(0.0, contingent-no_query)
    premium=max(0.0, contingent-max(no_query,universal_query))
    return FlexibleWaitingComparison(
        old_report_weights=weight,
        optimal_no_query_delays=tuple(x.wait_duration for x in optimal),
        optimal_no_query_branch_values=M,
        query_branch_values=Q,
        conditional_query_policy=tuple(
            "query" if Q[j]>M[j] else "no-query"
            for j in (0,1)),
        best_no_query_reward=no_query,
        always_query_reward=universal_query,
        conditional_query_reward=contingent,
        query_access_gain=access,
        conditional_query_premium=premium,
        matched_wait_query_premium=paired.conditional_query_premium
    )



@dataclass(frozen=True)
class FlexibleWaitingPrecisionReceipt:
    lower_error: float | None
    upper_error: float | None
    peak_error: float | None
    peak_query_control_premium: float
    no_query_reward_at_peak: float
    fixed_policy_tie_at_peak: bool


def flexible_wait_precision_window(
    *,
    iterations: int = 70,
    **parameters,
) -> FlexibleWaitingPrecisionReceipt:
    """Blackwell-ordered query premium against any permitted wait time.

    Every no-query competitor may condition waiting duration in
    [0,max_wait] on the old cue. Q(eps) is nonincreasing under cue
    garbling while optimal passive waiting is quality-independent.
    With two reports the relative premium is weakly unimodal, and
    the interior maximum is at universal-query/no-query indifference.

    Numerical bisection provides estimates, not certified intervals.
    """
    if iterations<1 or iterations>1000:
        raise ValueError("iterations must lie in [1,1000]")
    if "refresh_cue_error_rate" in parameters:
        raise ValueError("refresh_cue_error_rate is optimized")

    def model(err: float) -> FlexibleWaitingComparison:
        return compare_with_optimal_passive_wait(
            refresh_cue_error_rate=err, **parameters
        )

    def increment(err: float, idx: int) -> float:
        x=model(err)
        return (
            x.query_branch_values[idx] -
            x.optimal_no_query_branch_values[idx]
        )

    def root(j: int) -> float:
        lo, hi=0.0,0.5
        if increment(lo,j)<=0:
            return lo
        if increment(hi,j)>=0:
            return hi
        for _ in range(iterations):
            mid=(lo+hi)/2
            if increment(mid,j)>0:
                lo=mid
            else:
                hi=mid
        return (lo+hi)/2

    a,b=sorted((root(0),root(1)))
    if b-a<1e-12:
        return FlexibleWaitingPrecisionReceipt(
            None,None,None,0.0,0.0,False
        )

    def diff(err:float) -> float:
        x=model(err)
        return x.always_query_reward-x.best_no_query_reward

    if diff(a)<=0:
        peak=a
    elif diff(b)>=0:
        peak=b
    else:
        lo,hi=a,b
        for _ in range(iterations):
            m=(lo+hi)/2
            if diff(m)>0:
                lo=m
            else:
                hi=m
        peak=(lo+hi)/2
    x=model(peak)
    return FlexibleWaitingPrecisionReceipt(
        a,b,peak,x.conditional_query_premium,
        x.best_no_query_reward,
        math.isclose(diff(peak),0,abs_tol=1e-9),
    )


def flexible_wait_log_maintenance_ceiling(
    *,
    baseline_fitness:float,
    iterations:int=70,
    **parameters,
) -> float:
    """Model-specific upper log-fitness debit for *optional information*.

    The comparison includes a fully optimized no-query timing policy.
    This is not a measured controller genotype or realized fitness.
    """
    w0=float(baseline_fitness)
    if not math.isfinite(w0) or w0<=0:
        raise ValueError("baseline_fitness must be positive and finite")
    optimal=flexible_wait_precision_window(
        iterations=iterations,**parameters
    )
    if optimal.peak_error is None:
        return 0.0
    x=compare_with_optimal_passive_wait(
        refresh_cue_error_rate=optimal.peak_error,**parameters
    )
    comparator=max(
        x.best_no_query_reward,x.always_query_reward
    )
    return math.log1p(
        x.conditional_query_premium/(w0+comparator)
    )


