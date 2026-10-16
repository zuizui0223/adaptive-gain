"""A randomized cue protocol must retain abstentions and missing observations.

For all synthetic trial tables, the 'trials' are NOT independent bees.
The intervals bound completions of the finite-sample Horvitz-Thompson score;
they are not confidence intervals for population causal effects.
"""
import math
from dataclasses import replace
import pytest

from adaptive_gain.action_outcome_bounds import (
    ActionOutcomeTrial,
    bound_randomized_action_policy,
)
from adaptive_gain.policy_support import CueReportTrial, evaluate_randomized_second_cue_policy

POLICY = {0: 2, 1: 1}


def synthetic_records(*, include_abstention=False):
    """Exactly 200 randomized records; 100 match the policy, 20 are unobserved."""
    rows=[]
    for a in (0,1):
        for assigned in (1,2):
            matched = assigned == POLICY[a]
            if matched:
                if include_abstention:
                    # 20 missing, 10 observed abstain, 63 correct, 7 wrong
                    n_correct, n_wrong = (32,3) if a==0 else (31,4)
                    statuses = (['choice']* (n_correct+n_wrong) +
                                ['abstain']*5 + ['unobserved']*10)
                    decisions = ([1]*n_correct + [0]*n_wrong + [None]*15)
                else:
                    statuses=['choice']*40 + ['unobserved']*10
                    decisions=[1]*36 + [0]*4 + [None]*10
            else:
                statuses=['choice']*50
                decisions=[1]*25 + [0]*25
            assert len(statuses) == len(decisions) == 50
            for status, is_correct in zip(statuses, decisions):
                # Target=0 throughout the artificial list; action=0 is correct.
                action = (0 if is_correct else 1) if is_correct is not None else None
                rows.append(ActionOutcomeTrial(
                    trial_id=f'trial{len(rows):03d}', bee_id=f'bee{len(rows)//5:03d}',
                    target=0, context_bit=a, second_cue=assigned,
                    assignment_probability=0.5,
                    outcome_status=status, final_action=action,
                ))
    assert len(rows)==200
    return rows


def test_partial_identification_interval_contains_two_extreme_completions():
    trials=synthetic_records()
    r=bound_randomized_action_policy(trials,POLICY)
    assert (r.randomized_trials, r.matched_trials,r.matched_missing)==(200,100,20)
    assert (r.matched_choices,r.matched_abstentions)==(80,0)
    assert r.matched_by_context==((0,50),(1,50))
    assert (r.lower_ht,r.upper_ht)==pytest.approx((.72,.92))
    assert r.width==pytest.approx(.20)
    assert r.ess_matched==pytest.approx(100)
    assert r.unique_bees==40
    for missing_action, expected in ((0,.92),(1,.72)):
        observed=[replace(t,outcome_status='choice',final_action=missing_action)
                  if t.outcome_status=='unobserved' else t for t in trials]
        exact=bound_randomized_action_policy(observed,POLICY)
        assert exact.lower_ht==pytest.approx(expected)
        assert exact.upper_ht==pytest.approx(expected)


def test_bounds_preserve_sign_ambiguity_after_cost_and_baseline():
    r=bound_randomized_action_policy(synthetic_records(),POLICY)
    baseline=.75
    maintenance=.05
    assert r.lower_ht-baseline-maintenance==pytest.approx(-.08)
    assert r.upper_ht-baseline-maintenance==pytest.approx(.12)
    assert r.lower_ht < baseline+maintenance < r.upper_ht


def test_dropping_observed_abstentions_misstates_choice_accuracy():
    r=bound_randomized_action_policy(synthetic_records(include_abstention=True),POLICY)
    assert (r.matched_choices,r.matched_abstentions,r.matched_missing)==(70,10,20)
    assert (r.matched_correct,r.matched_wrong)==(63,7)
    assert r.lower_ht==pytest.approx(.63)
    assert r.upper_ht==pytest.approx(.83)
    assert r.matched_correct/r.matched_choices==pytest.approx(.9)
    assert r.lower_ht!=pytest.approx(.9)


def test_wrong_action_penalty_widens_missingness_bounds_both_directions():
    r=bound_randomized_action_policy(synthetic_records(),POLICY,
                                     correct_reward=1,error_cost=3)
    assert (r.lower_ht,r.upper_ht)==pytest.approx((-.12,.68))
    assert r.width==pytest.approx(.80)
    assert r.upper_ht>=r.lower_ht


def test_full_report_estimator_matches_prior_module_for_same_action():
    trials=[]
    for t in synthetic_records():
        if t.outcome_status=='unobserved':
            t=replace(t,outcome_status='choice',final_action=0)
        trials.append(t)
    bounded=bound_randomized_action_policy(trials,POLICY)
    cue=[CueReportTrial(t.trial_id,t.bee_id,t.target,t.context_bit,
                        t.second_cue,t.final_action,t.assignment_probability)
         for t in trials]
    old=evaluate_randomized_second_cue_policy(cue,POLICY)
    assert bounded.lower_ht==bounded.upper_ht==pytest.approx(old.estimated_reward)


def test_actual_observed_abstention_is_not_inferred_from_missing_cue_report():
    t=synthetic_records()[0]
    # The validation logic requires a decision observation for an abstention.
    with pytest.raises(ValueError,match='status'):
        bound_randomized_action_policy(
            [replace(x,outcome_status='abstain',final_action=0) if x==t else x
             for x in synthetic_records()],POLICY)


@pytest.mark.parametrize('bad',[
    lambda t: replace(t,outcome_status='unknown'),
    lambda t: replace(t,outcome_status='choice',final_action=None),
    lambda t: replace(t,outcome_status='unobserved',final_action=0),
    lambda t: replace(t,outcome_status='abstain',final_action=1),
    lambda t: replace(t,assignment_probability=0),
    lambda t: replace(t,assignment_probability=float('nan')),
    lambda t: replace(t,context_bit=3),
    lambda t: replace(t,target=3),
    lambda t: replace(t,second_cue=0),
    lambda t: replace(t,bee_id=''),
    lambda t: replace(t,trial_id=''),
])
def test_invalid_or_ambiguous_records_fail_closed(bad):
    rows=synthetic_records()
    rows[0]=bad(rows[0])
    with pytest.raises(ValueError):
        bound_randomized_action_policy(rows,POLICY)


def test_unobserved_policy_branch_rejected_even_if_other_context_present():
    rows=[t for t in synthetic_records() if not (
        t.context_bit==0 and t.second_cue==2)]
    with pytest.raises(ValueError,match='support'):
        bound_randomized_action_policy(rows,POLICY)


def test_duplicate_ids_invalid_policy_and_no_trials_rejected():
    trials=synthetic_records()
    trials[2]=replace(trials[2],trial_id=trials[0].trial_id)
    with pytest.raises(ValueError,match='duplicate'):
        bound_randomized_action_policy(trials,POLICY)
    with pytest.raises(ValueError,match='policy'):
        bound_randomized_action_policy(synthetic_records(),{0:2})
    with pytest.raises(ValueError,match='trial'):
        bound_randomized_action_policy([],POLICY)


@pytest.mark.parametrize('kwargs',[
    dict(correct_reward=0),dict(correct_reward=-1),dict(correct_reward=math.inf),
    dict(error_cost=-1),dict(error_cost=math.nan),dict(error_cost=math.inf),
])
def test_invalid_reward_parameters_fail_closed(kwargs):
    with pytest.raises(ValueError):
        bound_randomized_action_policy(synthetic_records(),POLICY,**kwargs)


def test_non_half_assignment_probabilities_are_used_as_logged():
    data=[]
    for a in (0,1):
        # Exact 100 assignments per context: 30 C,70 B at A=0;
        # 60 B,40 C at A=1. In both matched arms, 80% correct actions.
        if a==0:
            cells=((2,30,.3),(1,70,.7))
        else:
            cells=((1,60,.6),(2,40,.4))
        for cue,n,propensity in cells:
            for k in range(n):
                correct = k < (int(n*.8) if cue==POLICY[a] else n//2)
                data.append(ActionOutcomeTrial(
                    trial_id=f'trial{len(data)}',bee_id=f'bee{len(data)//10}',
                    target=1,context_bit=a,second_cue=cue,
                    assignment_probability=propensity,outcome_status='choice',
                    final_action=(1 if correct else 0),
                ))
    r=bound_randomized_action_policy(data,POLICY)
    assert r.matched_trials == 90
    assert r.lower_ht==r.upper_ht==pytest.approx(.8)
    assert r.ess_matched < 90
