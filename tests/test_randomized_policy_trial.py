"""Independent finite-policy tests and holdout overfitting counterexamples."""
import copy
import itertools

import pytest

from adaptive_gain.randomized_policy_trial import (
    FrozenQueryPolicy, by_cluster_holdout, evaluate_frozen_policy,
    fit_then_holdout_evaluate, learn_query_policy,
    validate_design_probabilities, validate_target,
)

PROBS = {o: {a: 1/3 for a in ("passive","sham","query")} for o in (0,1)}
TARGET = {0: .2, 1: .8}


def _clustered_fixture(
    *,
    clusters=16,
    repeats=20,
    probabilities=None,
    prefix="Subject",
):
    """Exact finite per-cell successes; randomness is arm ASSIGNMENT in RCT.

    Deterministic balanced toy outcomes are used to test algebra, not to
    demonstrate a realistic sampling distribution or infer causality.
    """
    probabilities = probabilities or {
        0: {"passive": .70, "sham": .65, "query": .90},
        1: {"passive": .80, "sham": .70, "query": .75},
    }
    out=[]
    for i in range(clusters):
        for old, arm in itertools.product((0,1),("passive","sham","query")):
            k=round(probabilities[old][arm]*repeats)
            for j in range(repeats):
                out.append({
                    "cluster":f"{prefix}_{i:03d}",
                    "old_report":old,
                    "assigned_arm":arm,
                    "assignment_probability":1/3,
                    "reward":float(j<k),
                })
    return out


def test_exact_policy_values_differ_from_zero_mean_universal_query():
    train=_clustered_fixture(clusters=4,prefix="Train")
    test=_clustered_fixture(clusters=12,prefix="Test")
    frozen=learn_query_policy(train)
    assert frozen == FrozenQueryPolicy("query","passive")
    receipt=evaluate_frozen_policy(
        test,frozen,target_old_report_weights=TARGET,
        assignment_probabilities=PROBS,
        bootstrap_repetitions=100,seed=7,
    )
    assert receipt.conditional_reward == pytest.approx(.82)
    assert receipt.always_passive_reward == pytest.approx(.78)
    assert receipt.always_query_reward == pytest.approx(.78)
    assert receipt.always_sham_reward == pytest.approx(.69)
    assert receipt.query_minus_sham == pytest.approx(.09)
    assert receipt.conditional_minus_best_fixed == pytest.approx(.04)
    assert receipt.conditional_minus_passive == pytest.approx(.04)
    assert receipt.conditional_minus_query == pytest.approx(.04)
    assert receipt.simultaneous_95_percent_gain_lower == pytest.approx(.04)
    assert receipt.conditional_better_than_both_fixed_at_approx_95_percent
    assert receipt.independent_clusters == 12
    assert receipt.evaluated_cluster_bootstrap_replicates == 100


def test_training_gain_can_be_false_positive_out_of_sample():
    train = _clustered_fixture(
        clusters=4,prefix="Train",
        probabilities={
            0:{"passive":.5,"sham":.5,"query":.7},
            1:{"passive":.7,"sham":.5,"query":.5}
        },
    )
    test = _clustered_fixture(
        clusters=12,prefix="Test",
        probabilities={
            0:{"passive":.6,"sham":.6,"query":.6},
            1:{"passive":.6,"sham":.6,"query":.6}
        },
    )
    frozen=learn_query_policy(train)
    training=evaluate_frozen_policy(
        train,frozen,target_old_report_weights={0:.5,1:.5},
        assignment_probabilities=PROBS,
        bootstrap_repetitions=100
    )
    heldout=evaluate_frozen_policy(
        test,frozen,target_old_report_weights={0:.5,1:.5},
        assignment_probabilities=PROBS,
        bootstrap_repetitions=100
    )
    assert frozen == FrozenQueryPolicy("query","passive")
    assert training.conditional_minus_best_fixed == pytest.approx(.10)
    assert heldout.conditional_minus_best_fixed == pytest.approx(0)
    assert heldout.simultaneous_95_percent_gain_lower <= 1e-12
    assert not heldout.conditional_better_than_both_fixed_at_approx_95_percent


def test_cluster_splitting_never_leaks_subject_or_colony():
    rows=_clustered_fixture(clusters=20)
    train,test=by_cluster_holdout(rows,test_fraction=.4,seed=331)
    s1={r["cluster"] for r in train}
    s2={r["cluster"] for r in test}
    assert len(s1)==12 and len(s2)==8
    assert not s1.intersection(s2)
    a=fit_then_holdout_evaluate(
        rows,target_old_report_weights=TARGET,
        assignment_probabilities=PROBS,
        test_fraction=.4,split_seed=331,
        bootstrap_repetitions=100,
    )
    b=fit_then_holdout_evaluate(
        rows,target_old_report_weights=TARGET,
        assignment_probabilities=PROBS,
        test_fraction=.4,split_seed=331,
        bootstrap_repetitions=100,
    )
    assert a==b
    assert a.conditional_minus_best_fixed==pytest.approx(.04)
    assert a.independent_clusters==8


def test_deployment_weight_is_not_experimental_old_cue_frequency():
    trials=_clustered_fixture(clusters=12)
    pi=FrozenQueryPolicy("query","passive")
    natural=evaluate_frozen_policy(
        trials,pi,target_old_report_weights=TARGET,
        assignment_probabilities=PROBS,bootstrap_repetitions=40
    )
    artificially_balanced=evaluate_frozen_policy(
        trials,pi,target_old_report_weights={0:.5,1:.5},
        assignment_probabilities=PROBS,bootstrap_repetitions=40
    )
    assert natural.conditional_minus_best_fixed==pytest.approx(.04)
    assert artificially_balanced.conditional_minus_best_fixed==pytest.approx(.025)
    assert natural.target_old_report_weights == (.2,.8)


def test_invalid_randomization_weights_and_posivity_fail_closed():
    trial=_clustered_fixture(clusters=8)
    pi=FrozenQueryPolicy("query","passive")
    args=dict(target_old_report_weights=TARGET,
              assignment_probabilities=PROBS,
              bootstrap_repetitions=40)
    with pytest.raises(ValueError,match="target report weights"):
        validate_target({0:.3,1:.8})
    with pytest.raises(ValueError,match="assignment probabilities"):
        validate_design_probabilities({
            0:{"passive":.5,"sham":.5,"query":0},
            1:PROBS[1]
        })
    with pytest.raises(ValueError,match="randomization probability"):
        changed=copy.deepcopy(trial)
        changed[0]["assignment_probability"]=.9
        evaluate_frozen_policy(changed,pi,**args)
    with pytest.raises(ValueError,match="positivity failure"):
        truncated=[
            x for x in trial
            if not (x["old_report"]==0 and x["assigned_arm"]=="sham")
        ]
        evaluate_frozen_policy(truncated,pi,**args)
    with pytest.raises(ValueError,match="old_report"):
        bad=copy.deepcopy(trial)
        bad[0]["old_report"]=2
        evaluate_frozen_policy(bad,pi,**args)
    with pytest.raises(ValueError,match="independent biological clusters"):
        single=[dict(x,cluster="AllSame") for x in trial]
        evaluate_frozen_policy(single,pi,**args)
    with pytest.raises(ValueError,match="bootstrap draws"):
        evaluate_frozen_policy(trial,pi,**dict(args,bootstrap_repetitions=5))
    with pytest.raises(ValueError,match="test_fraction"):
        by_cluster_holdout(trial,test_fraction=1.0)
