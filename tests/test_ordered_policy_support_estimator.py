"""Randomization-based two-stage cue policy evaluation: fail-closed controls."""
from fractions import Fraction as F

import pytest

from adaptive_gain.policy_support import (
    CueReportTrial,
    evaluate_randomized_second_cue_policy,
)

from test_ordered_policy_support import randomized_distribution, target_policy


def synthetic_complete_log(s=F(9, 10), g0=F(1, 2), g1=F(1, 2)):
    """A synthetic census matching the exact randomized population distribution."""
    rows = randomized_distribution(s, g0, g1)
    trials = []
    for (world, context, query, readout), mass in sorted(rows.items()):
        n = mass * 160
        assert n.denominator == 1
        propensity = g0 if (context == 0 and query == 2) else (
            1-g0 if context == 0 else (g1 if query == 2 else 1-g1)
        )
        for _ in range(int(n)):
            trials.append(CueReportTrial(
                trial_id=str(len(trials)+1), bee_id=f"synthetic_{world}",
                target=world, context_bit=context, second_cue=query,
                second_report=readout, assignment_probability=float(propensity),
            ))
    assert len(trials) == 160
    return trials


def test_ipw_reproduces_exact_counterfactual_accuracy_for_fixed_prespecified_policy():
    trials = synthetic_complete_log()
    receipt = evaluate_randomized_second_cue_policy(
        trials, {0:2,1:1}, correct_reward=1.0, error_cost=0.0
    )
    assert receipt.trials == 160
    assert receipt.estimated_reward == pytest.approx(0.825)
    assert receipt.self_normalized_reward == pytest.approx(0.825)
    assert receipt.effective_sample_size == pytest.approx(80)
    assert receipt.total_matched == 80
    assert receipt.matched_by_context == ((0, 40), (1, 40))


@pytest.mark.parametrize("s,expected", [(F(3,4),0.75), (F(9,10),0.825)])
def test_policy_value_estimator_under_stable_vs_reactive_observation(s,expected):
    receipt = evaluate_randomized_second_cue_policy(
        synthetic_complete_log(s=s), {0:2,1:1}
    )
    assert receipt.estimated_reward == pytest.approx(expected)


def test_no_observed_policy_arm_in_context_rejects_identification():
    base=synthetic_complete_log()
    logged=[t for t in base if t.second_cue==1]
    # Without any cue-C report under A=0, the target policy's value cannot
    # be estimated from the deployed fixed A->B log, even with true targets.
    with pytest.raises(ValueError, match='support'):
        evaluate_randomized_second_cue_policy(logged,{0:2,1:1})


def test_missing_second_readout_is_not_silently_dropped():
    log=synthetic_complete_log()
    t=log[0]
    log[0]=CueReportTrial(t.trial_id,t.bee_id,t.target,t.context_bit,t.second_cue,
                          None,t.assignment_probability)
    with pytest.raises(ValueError, match='missing'):
        evaluate_randomized_second_cue_policy(log,{0:2,1:1})


def test_unrecorded_propensity_and_invalid_policy_rejected():
    log=synthetic_complete_log()
    t=log[0]
    log[0]=CueReportTrial(t.trial_id,t.bee_id,t.target,t.context_bit,t.second_cue,
                          t.second_report,0.0)
    with pytest.raises(ValueError, match='propensity'):
        evaluate_randomized_second_cue_policy(log,{0:2,1:1})
    with pytest.raises(ValueError, match='policy'):
        evaluate_randomized_second_cue_policy(synthetic_complete_log(),{0:2})


def test_duplicated_trial_ids_rejected():
    trials=synthetic_complete_log()
    trials[0]=CueReportTrial(trials[1].trial_id,trials[0].bee_id,trials[0].target,
                             trials[0].context_bit,trials[0].second_cue,
                             trials[0].second_report,trials[0].assignment_probability)
    with pytest.raises(ValueError, match='duplicate'):
        evaluate_randomized_second_cue_policy(trials,{0:2,1:1})


def test_wrong_choice_loss_estimator_can_be_negative_without_clipping():
    log=synthetic_complete_log()
    r=evaluate_randomized_second_cue_policy(log,{0:2,1:1},error_cost=3)
    assert r.estimated_reward == pytest.approx(0.825-3*0.175)
    assert r.self_normalized_reward == pytest.approx(0.825-3*0.175)
