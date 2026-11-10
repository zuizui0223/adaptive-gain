"""Stage16 exact Bayes-optimal access-mode value with free guessing.

No observations of bees, no trained animal policy, no real cost calibration.
Root signal has reliability s∈[1/2,1]; U and V leaves are perfectly observed
when requested, iid fair binary worlds. Each leaf request costs c≥0 in
normalized utility units. One correct target scores +1, a wrong guess 0.

Contingent access: after the noisy root signal, choose relevant leaf or guess.
Precommit: before the root signal, choose a FIRST leaf or no leaf, may pay for
the second AFTER root observation if that first cue becomes irrelevant.
"""
from __future__ import annotations
import json
import math
from pathlib import Path


def _check(root_reliability, leaf_cost):
    for name,value in (("root_reliability",root_reliability),("leaf_cost",leaf_cost)):
        if type(value) not in (float,int) or not math.isfinite(value):
            raise ValueError("NO_GO_INVALID_EXACT_MODEL_PARAMETER_"+name)
    if not (0.5<=root_reliability<=1):
        raise ValueError("NO_GO_ROOT_RELIABILITY_OUTSIDE_NONINVERTED_RANGE")
    if leaf_cost<0:
        raise ValueError("NO_GO_NEGATIVE_OBSERVATION_COST")


def best_values(root_reliability,leaf_cost):
    """Closed-form Bayesian decision value with guessing and optional second cue.

    The leaf variables are iid fair, and an independently noisy root bit is
    observed by both access modes. With posterior root reliability s, one
    context-relevant leaf raises correct-choice probability from 1/2 to
    (1+s)/2. A precommitted leaf alone gives accuracy 3/4; a conditionally
    requested second leaf (with probability 1/2) recovers (1+s)/2.
    """
    _check(root_reliability,leaf_cost)
    s=float(root_reliability);c=float(leaf_cost)
    success_relevant=(1+s)/2
    active_options={
        "guess_without_leaf":0.5,
        "query_relevant_leaf_after_root":success_relevant-c,
    }
    precommit_options={
        "guess_without_leaf":0.5,
        "request_one_precommitted_leaf":0.75-c,
        "request_second_if_first_contextually_irrelevant":success_relevant-1.5*c,
    }
    # With exact ties, prefer zero-cost/zero-request policies. This choice
    # affects only the descriptive label, never the mathematical envelope.
    a=max(active_options.items(),key=lambda kv:kv[1])
    p=max(precommit_options.items(),key=lambda kv:kv[1])
    gain=a[1]-p[1]
    if gain<-1e-11:
        raise ValueError("NO_GO_BAYES_CONTINGENT_VALUE_BELOW_PRECOMMIT")
    return {
        "root_reliability":s,
        "leaf_cost_in_correctness_reward_units":c,
        "contingent_net":a[1],
        "precommit_net":p[1],
        "value_of_contingency":max(0.,gain),
        "optimal_contingent_policy":a[0],
        "optimal_precommit_policy":p[0],
        "contingent_candidate_values":active_options,
        "precommit_candidate_values":precommit_options,
        "root_only_guessing_value":0.5,
        "leaf_observation_accuracy_assumed":1.0,
        "may_skip_first_leaf":True,
        "empirical":False,
        "not_a_model_of_any_observed_animal":True,
    }



def mandatory_first_leaf_values(root_reliability,leaf_cost):
    """Actual Stage15 mandatory-first-request policy class, no root-only stop.

    The first leaf has already been committed or selected in the original
    design; the animal cannot choose to forgo it. It can skip a SECOND
    request after seeing the first. This is different from the optional-
    start rational benchmark in best_values.
    """
    _check(root_reliability,leaf_cost)
    s=float(root_reliability);c=float(leaf_cost)
    contingent=(1+s)/2-c
    precommit=max(.75-c,(1+s)/2-1.5*c)
    gain=contingent-precommit
    expected=min((s-.5)/2,c/2)
    if abs(gain-expected)>1e-10:
        raise ValueError("NO_GO_MANDATORY_QUERY_CLOSED_FORM_FAILED")
    return {
        "root_reliability":s,
        "leaf_cost_in_correctness_reward_units":c,
        "contingent_net":contingent,
        "precommit_net":precommit,
        "value_of_contingency":max(0.,gain),
        "may_skip_first_leaf":False,
        "precommit_can_decline_second_leaf":True,
        "mandatory_high_cost_utilities_can_be_negative":True,
        "empirical":False,
    }


def theoretical_ceiling(root_reliability):
    """Exact maximum of access-value over c≥0, in this restricted game.

    For .5≤s≤.75, maximum (s-.5)/2 on plateau c∈[s-.5,.25].
    For .75≤s≤1, maximum s/6 at c=s/3.
    """
    _check(root_reliability,0.)
    s=float(root_reliability)
    if s<=.75:
        lo=max(0.,s-.5)
        hi=.25
        cost=(lo+hi)/2
        high=(s-.5)/2
        plateau=[lo,hi]
    else:
        cost=s/3
        high=s/6
        plateau=[cost,cost]
    check=best_values(s,cost)["value_of_contingency"]
    if abs(check-high)>1e-10:
        raise ValueError("NO_GO_EXACT_FRONTIER_CEILING_NOT_ATTAINED")
    return {
        "root_reliability":s,
        "max_value_of_contingency":high,
        "attaining_leaf_cost":cost,
        "optimal_cost_plateau":plateau,
        "not_empirical_or_colony_variance":True
    }


def decision_grid():
    reliabilities=(.5,.55,.6,.7,.75,.8,.9,1.)
    costs=(0.,.01,.05,.10,.15,.20,.25,.30,1/3,.35,.4,.50,.6)
    rows=[{**best_values(s,c),
           "mandatory_first_leaf_comparator":mandatory_first_leaf_values(s,c)}
          for s in reliabilities for c in costs]
    return {
        "status":"EXACT_ANALYTICAL_BAYES_DECISION_FRONTIER",
        "worlds":8,
        "root_signal_accuracy_values":reliabilities,
        "leaf_cost_values":costs,
        "rows":rows,
        "max_by_root_accuracy":[theoretical_ceiling(s) for s in reliabilities],
        "no_real_animals":True,
        "no_behavioral_effect_estimated":True,
        "no_real_cost_units_calibrated":True,
        "stage15_existing_protocol_makes_first_leaf_mandatory":True,
        "optional_first_leaf_model_requires_a_different_future_ability_to_decline":True,
        "no_root_or_leaf_errors_measured_from_any_animals":True,
    }


if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="stage16_exact_outputs")
    root=Path(ap.parse_args().out)
    root.mkdir(parents=True,exist_ok=True)
    result=decision_grid()
    (root/"stage16_exact_query_value_frontier.json").write_text(
        json.dumps(result,indent=2,allow_nan=False))
    examples=[best_values(s,c) for s,c in ((1.,.1),(.6,.2),(1.,1/3),(.75,.4),(.5,.1))]
    print("STAGE16_EXACT_QUERY_VALUE_EXAMPLES "+
          json.dumps({"status":result["status"],"examples":examples,
                     "source_animals":0},allow_nan=False))
