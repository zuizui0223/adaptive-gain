"""Independent check of the strongest passive waiting comparator."""
import itertools
import math

import pytest

from adaptive_gain.optimal_passive_wait import (
    passive_timing_optimum, compare_with_optimal_passive_wait
)


def _direct_no_information_wait_value(
    *, posterior_at_old_cue, alpha, beta, cue_age, terminal_delay,
    waiting, opportunity_hazard, reward0, reward1,
):
    pi1=alpha/(alpha+beta)
    p1=pi1+(posterior_at_old_cue-pi1)*math.exp(
        -(alpha+beta)*(cue_age+terminal_delay+waiting)
    )
    return math.exp(-opportunity_hazard*(terminal_delay+waiting))*max(
        reward0*(1-p1),reward1*p1
    )


def test_exact_passive_wait_extremum_matches_independent_dense_time_grid():
    checked=0
    for p0, alpha, beta, age, cost_time, hazard, r0, r1 in itertools.product(
        (0.0, .17, .5, .9, 1.0),
        (.2, .8), (.2, .8), (.1, 1.2),
        (.1, .2), (0., .05, .25), (1., 4.), (1., 4.),
    ):
        kw=dict(
            posterior_at_old_cue=p0, alpha=alpha, beta=beta,
            cue_age=age, terminal_delay=cost_time, max_wait=.5,
            opportunity_hazard=hazard, reward0=r0, reward1=r1,
        )
        x=passive_timing_optimum(**kw)
        independent=max(
            _direct_no_information_wait_value(
                **{k:v for k,v in kw.items() if k!="max_wait"},
                waiting=i/200
            )
            for i in range(101)
        )
        assert x.expected_reward + 1e-12 >= independent
        assert x.expected_reward == pytest.approx(
            _direct_no_information_wait_value(
                **{k:v for k,v in kw.items() if k!="max_wait"},
                waiting=x.wait_duration
            )
        )
        assert 0 <= x.wait_duration <= .5
        checked+=1
    assert checked == 960


def test_canonical_optimal_wait_is_longer_than_matched_query_time():
    base=dict(
        alpha=.8,beta=.2,cue_age=1.2,sampling_delay=.15,
        terminal_delay=.1, opportunity_hazard=.25,
        reward0=1,reward1=1,query_cost=.03,max_wait=.5,
    )
    x=compare_with_optimal_passive_wait(
        refresh_cue_error_rate=.11225411408084168, **base
    )
    assert x.optimal_no_query_delays[0] == pytest.approx(
        .3094379124341003, abs=1e-10
    )
    assert x.optimal_no_query_delays[1] == pytest.approx(0, abs=1e-12)
    assert x.best_no_query_reward == pytest.approx(
        .7822730559560074, abs=1e-10
    )
    assert x.conditional_query_premium == pytest.approx(
        .039083537, abs=1e-5
    )
    assert x.conditional_query_premium < x.matched_wait_query_premium
    assert x.conditional_query_policy == ("query", "no-query")


def test_flexible_waiting_yields_smaller_query_control_window():
    base=dict(
        alpha=.8,beta=.2,cue_age=1.2,sampling_delay=.15,
        terminal_delay=.1,opportunity_hazard=.25,
        reward0=1,reward1=1,query_cost=.03,max_wait=.5,
    )
    for error,positive in ((0,False),(.05,False),(.06,True),
                           (.12,True),(.33,True),(.34,False),
                           (.5,False)):
        x=compare_with_optimal_passive_wait(
            refresh_cue_error_rate=error,**base)
        assert (x.conditional_query_premium > 1e-10) == positive
        assert x.query_access_gain >= 0
        assert x.conditional_query_premium <= (
            x.matched_wait_query_premium+1e-12
        )


def test_uninformative_refresh_and_optimized_wait_cannot_create_information():
    x=compare_with_optimal_passive_wait(
        .8,.2,cue_age=.1,sampling_delay=.15,terminal_delay=.15,
        opportunity_hazard=.25,reward0=1,reward1=4,
        query_cost=.015,max_wait=.5,refresh_cue_error_rate=.5
    )
    assert x.conditional_query_premium == pytest.approx(0,abs=1e-12)
    assert x.query_access_gain == pytest.approx(0,abs=1e-12)
    assert x.conditional_query_policy == ("no-query","no-query")


def test_bad_flexible_waiting_horizon_and_parameter_inputs_are_rejected():
    with pytest.raises(ValueError):
        compare_with_optimal_passive_wait(
            .8,.2,cue_age=.1,sampling_delay=.15,terminal_delay=.15,
            opportunity_hazard=.25,reward0=1,reward1=4,
            query_cost=.015,max_wait=.1,refresh_cue_error_rate=.5
        )
    with pytest.raises(ValueError):
        passive_timing_optimum(
            posterior_at_old_cue=1.1,alpha=.8,beta=.2,
            cue_age=.1,terminal_delay=.1,max_wait=.5,
            opportunity_hazard=.25,reward0=1,reward1=4
        )
