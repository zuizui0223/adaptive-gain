"""Independent latent-state brute force for optimal timing after noisy querying.

The oracle enumerates old true state, old observation, new true state,
new observation and final state; terminal actions and post-query delays
are optimized on a fine deterministic time grid, without calling the
closed-form timing optimizer inside post_query_timing.py.
"""
import itertools
import math

import pytest

from adaptive_gain.post_query_timing import query_then_optimal_timing
from adaptive_gain.optimal_passive_wait import compare_with_optimal_passive_wait


def _grid_oracle(alpha, beta, age, sample, terminal, horizon,
                 hazard, r0, r1, cost, old_error, new_error,
                 subdivisions=600):
    pi1=alpha/(alpha+beta)
    prior=(1-pi1,pi1)

    def transition(x,t,y):
        p=pi1+(x-pi1)*math.exp(-(alpha+beta)*t)
        return p if y else (1-p)

    def emit(y,x,error):
        return 1-error if y==x else error

    weights=[]
    passive_branches=[]
    query_branches=[]
    for old in (0,1):
        w=sum(prior[x]*emit(old,x,old_error) for x in (0,1))
        weights.append(w)

        # Optimize a terminal action at any permissible passive wait.
        passive=max(
            math.exp(-hazard*(terminal+horizon*i/subdivisions))*
            sum(prior[x]*emit(old,x,old_error)*
                transition(x,age+terminal+horizon*i/subdivisions,z)*
                (r0 if z==0 else r1)
                for x in (0,1) for z in (0,1) if z==action)/w
            for action in (0,1) for i in range(subdivisions+1)
        )
        passive_branches.append(passive)

        # Each refreshed report independently selects action AND wait.
        gross=0
        for y in (0,1):
            score=max(
                math.exp(-hazard*(sample+terminal+
                                 (horizon-sample)*i/subdivisions))*
                sum(
                    prior[x]*emit(old,x,old_error)*
                    transition(x,age+sample,now)*
                    emit(y,now,new_error)*
                    transition(now,terminal+
                               (horizon-sample)*i/subdivisions,z)*
                    (r0 if z==0 else r1)
                    for x in (0,1)
                    for now in (0,1)
                    for z in (0,1) if z==action
                )/w
                for action in (0,1) for i in range(subdivisions+1)
            )
            gross+=score
        query_branches.append(gross-cost)

    conditional=sum(
        weights[o]*max(passive_branches[o],query_branches[o])
        for o in (0,1))
    no_query=sum(weights[o]*passive_branches[o] for o in (0,1))
    universal=sum(weights[o]*query_branches[o] for o in (0,1))
    return {
        "weights":tuple(weights),
        "passive":tuple(passive_branches),
        "query":tuple(query_branches),
        "conditional":conditional,
        "no_query":no_query,
        "universal":universal,
        "premium":conditional-max(no_query,universal),
    }


def test_old_and_new_reports_can_both_influence_when_to_act():
    kw=dict(
        alpha=.8,beta=.2,cue_age=.05,sampling_delay=.15,
        terminal_delay=.1,max_total_wait=.5,
        opportunity_hazard=.01,reward0=1,reward1=2,
        query_cost=0,old_cue_error_rate=0,
        refresh_cue_error_rate=.1,
    )
    r=query_then_optimal_timing(**kw)
    assert r.acquisition_policy_by_old_report == ("query","passive")
    # Old report 0 leads to QUERY, and the newly observed label 1
    # postpones terminal action, while label 0 permits immediate action.
    assert r.postquery_delay_by_old_and_new_report[0][0] == pytest.approx(0)
    assert r.postquery_delay_by_old_and_new_report[0][1] > .3
    assert r.conditional_query_premium > 0


def test_canonical_strict_information_premium_survives_post_query_waiting():
    params=dict(alpha=.8,beta=.2,cue_age=1.2,sampling_delay=.15,
                terminal_delay=.1,max_total_wait=.5,
                opportunity_hazard=.25,reward0=1,reward1=1,
                query_cost=.03,old_cue_error_rate=0,
                refresh_cue_error_rate=.11)
    expanded=query_then_optimal_timing(**params)
    previous=compare_with_optimal_passive_wait(
        max_wait=.5,
        **{k:v for k,v in params.items() if k!="max_total_wait"}
    )
    assert expanded.passive_reward_by_old_report == pytest.approx(
        previous.optimal_no_query_branch_values,abs=1e-12)
    for j in (0,1):
        assert expanded.query_reward_by_old_report[j] + 1e-12 >= (
            previous.query_branch_values[j]
        )
    assert expanded.conditional_policy_reward + 1e-12 >= (
        previous.conditional_query_reward
    )
    assert expanded.conditional_query_premium > .0379


def test_uninformative_fresh_cue_cannot_beat_passive_waiting():
    n=0
    for age,r0,r1,olderr in itertools.product(
        (.1,1.2),(1,4),(1,4),(0,.08,.5)
    ):
        out=query_then_optimal_timing(
            .8,.2,cue_age=age,sampling_delay=.15,
            terminal_delay=.1,max_total_wait=.5,
            opportunity_hazard=.25,reward0=r0,reward1=r1,
            query_cost=.015,old_cue_error_rate=olderr,
            refresh_cue_error_rate=.5,
        )
        assert out.query_access_value == pytest.approx(0,abs=1e-12)
        assert out.conditional_query_premium == pytest.approx(0,abs=1e-12)
        assert out.acquisition_policy_by_old_report == ("passive","passive")
        n+=1
    assert n==24


def test_independent_latent_state_trajectory_enumeration():
    checked=0
    for alpha,beta,age,olderr,newerr,r0,r1 in itertools.product(
        (.2,.8),(.2,.8),(.1,1.2),
        (0,.08),(.03,.2),(1,4),(1,4)
    ):
        spec=dict(
            alpha=alpha,beta=beta,cue_age=age,
            sampling_delay=.15,terminal_delay=.1,
            max_total_wait=.5,opportunity_hazard=.25,
            reward0=r0,reward1=r1,query_cost=.03,
            old_cue_error_rate=olderr,
            refresh_cue_error_rate=newerr,
        )
        truth=query_then_optimal_timing(**spec)
        brute=_grid_oracle(
            alpha,beta,age,.15,.1,.5,.25,r0,r1,.03,
            olderr,newerr,subdivisions=120
        )
        assert truth.old_report_weights == pytest.approx(
            brute["weights"],abs=1e-12)
        for o in (0,1):
            assert truth.passive_reward_by_old_report[o] + 1e-12 >= (
                brute["passive"][o])
            assert truth.query_reward_by_old_report[o] + 1e-12 >= (
                brute["query"][o])
            assert truth.query_reward_by_old_report[o] - brute["query"][o] < .005
            assert truth.passive_reward_by_old_report[o] - brute["passive"][o] < .005
        assert truth.conditional_policy_reward + 1e-12 >= (
            brute["conditional"])
        checked+=1
    assert checked==128


def test_parameter_validation_and_equal_horizon_fairness():
    p=dict(alpha=.8,beta=.2,cue_age=.1,sampling_delay=.15,
        terminal_delay=.1,max_total_wait=.5,
        opportunity_hazard=.25,reward0=1,reward1=1,query_cost=.03)
    with pytest.raises(ValueError):
        query_then_optimal_timing(**dict(p,max_total_wait=.1))
    with pytest.raises(ValueError):
        query_then_optimal_timing(**dict(p,refresh_cue_error_rate=.8))
    with pytest.raises(ValueError):
        query_then_optimal_timing(**dict(p,alpha=0))
