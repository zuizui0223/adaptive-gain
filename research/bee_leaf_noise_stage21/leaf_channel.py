"""Stage21: all root and leaf signals can be misread, exact finite Bayesian DP.

ZERO real animals or original experimental trials. Each hidden world is
R~Bern(.5), U~Bern(q), V~Bern(.5), independent and resampled with replacement.
R is observed as Z with class-specific accuracies s0,s1 in [.5,1].
U and V, once voluntarily requested, each produce a separate noisy bit
with symmetric channel accuracies aU,aV in [.5,1]; each leaf can be read ONCE.
No-query guesses and optional second source remain available. Both treatment
arms receive root Z; the first SKIP/U/V decision is precommitted before Z
or contingent after Z. Payoff correct1/wrong0 minus c per paid leaf source.

The source oracle works in exact unnormalized Fraction probability masses.
Tests independently construct normalized posterior dynamic programming.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import json
import math

WORLDS=tuple(product((0,1),repeat=3))
ACTIONS=("SKIP","U","V")
HALF=Fraction(1,2)
ONE=Fraction(1)
Q=Fraction(1,5)
C=Fraction(1,4)

def _num(name,value,lower,upper=None):
    if type(value) not in (float,int,Fraction) or not math.isfinite(float(value)):
        raise ValueError("NO_GO_INVALID_"+name.upper())
    v=value if isinstance(value,Fraction) else Fraction(str(value))
    if v<lower or (upper is not None and v>upper):
        raise ValueError("NO_GO_"+name.upper()+"_OUT_OF_DOMAIN")
    return v

def _mass(rows):
    return sum(rows.values(),Fraction(0))

def _guess(rows):
    return max(
        sum((wt for (r,u,v),wt in rows.items()
             if (u if r==0 else v)==target),Fraction(0))
        for target in (0,1))

def _joint_root(q,s0,s1,observed):
    return {
        (r,u,v):Fraction(1,4)*(q if u else ONE-q)*(
            (s0 if observed==0 else ONE-s0)
            if r==0 else (ONE-s1 if observed==0 else s1)
        ) for r,u,v in WORLDS
    }

def _noisy_leaf(rows,leaf,readout,accuracy):
    """Return UNNORMALIZED joint posterior weights after one paid display."""
    pos=1 if leaf=="U" else 2
    return {
        world:wt*(accuracy if world[pos]==readout else ONE-accuracy)
        for world,wt in rows.items()
    }

def _first_request(rows,leaf,c,accuracy_u,accuracy_v):
    accuracies={"U":accuracy_u,"V":accuracy_v}
    other="V" if leaf=="U" else "U"
    total=-c*_mass(rows)
    for first_reading in (0,1):
        posterior=_noisy_leaf(rows,leaf,first_reading,accuracies[leaf])
        value_without_second=_guess(posterior)
        value_second=-c*_mass(posterior)
        for second_reading in (0,1):
            after_second=_noisy_leaf(posterior,other,second_reading,accuracies[other])
            value_second+=_guess(after_second)
        total+=max(value_without_second,value_second)
    return total

def _choice_values(rows,c,a_u,a_v):
    return {
       "SKIP":_guess(rows),
       "U":_first_request(rows,"U",c,a_u,a_v),
       "V":_first_request(rows,"V",c,a_u,a_v),
    }

def _best(actions):
    # Source contract: do not claim an unnecessary real information request
    # when SKIP and request have exactly equal expected utility.
    return max(ACTIONS,key=lambda a:actions[a])

def _solve(q,c,s0,s1,a_u,a_v):
    branches={z:_choice_values(_joint_root(q,s0,s1,z),c,a_u,a_v)
              for z in (0,1)}
    probs={z:_mass(_joint_root(q,s0,s1,z)) for z in (0,1)}
    if sum(probs.values(),Fraction(0))!=ONE:
        raise ValueError("NO_GO_SOURCE_PROBABILITY_MASS_INVALID")
    contingent=sum((branches[z][_best(branches[z])] for z in (0,1)),Fraction(0))
    fixed_options={a:sum((branches[z][a] for z in (0,1)),Fraction(0))
                   for a in ACTIONS}
    pre_action=_best(fixed_options)
    precommit=fixed_options[pre_action]
    if contingent<precommit:
        raise ValueError("NO_GO_CONTINGENT_ACCESS_LOWER_THAN_PRECOMMIT")
    return contingent,precommit,branches,probs,pre_action

def optimal_values(q,leaf_cost,s0,s1,accuracy_u,accuracy_v):
    q=_num("q",q,Fraction(0),HALF)
    c=_num("leaf_cost",leaf_cost,Fraction(0))
    s0=_num("root_r0_accuracy",s0,HALF,ONE)
    s1=_num("root_r1_accuracy",s1,HALF,ONE)
    a_u=_num("paid_u_accuracy",accuracy_u,HALF,ONE)
    a_v=_num("paid_v_accuracy",accuracy_v,HALF,ONE)
    active,pre,branches,probs,pre_action=_solve(q,c,s0,s1,a_u,a_v)
    gain=active-pre
    if q==Q and c==C:
        # Sharp theorem on this exact restricted domain: U is not worth
        # purchasing at cost .25 because even perfect U improves accuracy
        # by no more than q=.2, regardless of the observed root or V.
        formula=max(Fraction(0),(
           s1*(a_v-Fraction(3,4))-Fraction(11,20)*(ONE-s0)
        )/2)
        if gain!=formula or pre!=Fraction(13,20) or pre_action!="SKIP":
            raise ValueError("NO_GO_SHARP_NOISY_LEAF_EXACT_MODEL_MISMATCH")
        if _best(branches[0])!="SKIP":
            raise ValueError("NO_GO_UNEXPECTED_ROOT0_SOURCE_REQUEST")
        expected_z1="V" if formula>0 else "SKIP"
        if _best(branches[1])!=expected_z1:
            raise ValueError("NO_GO_ROOT1_NOISY_V_REQUEST_RULE")
    return {
        "status":"EXACT_NOISY_LEAF_OPTIONAL_QUERY_BAYES",
        "q":float(q),"leaf_cost":float(c),
        "root_s0":float(s0),"root_s1":float(s1),
        "U_recognition_accuracy":float(a_u),
        "V_recognition_accuracy":float(a_v),
        "balanced_leaf_accuracy":float((a_u+a_v)/2),
        "contingent_optimum":float(active),
        "precommit_optimum":float(pre),
        "value_of_contingency":float(gain),
        "first_action_after_z":{str(z):_best(branches[z]) for z in (0,1)},
        "precommit_first_action":pre_action,
        "observed_z_probability":{str(z):float(probs[z]) for z in (0,1)},
        "root_and_paid_leaf_channels_are_distinct":True,
        "one_real_leaf_request_per_original_source_max":True,
        "next_leaf_request_optional_after_first_readout":True,
        "exact_fraction_source_calculation":True,
        "no_real_bees_observed":True,
        "not_darwinian_fitness":True,
    }

def sharp_v_threshold(s0,s1):
    """V-signal accuracy threshold for q=.2,c=.25; any a_U in [.5,1]."""
    s0=_num("root_s0",s0,HALF,ONE)
    s1=_num("root_s1",s1,HALF,ONE)
    threshold=Fraction(3,4)+Fraction(11,20)*(ONE-s0)/s1
    for value in (HALF,ONE):
        found=optimal_values(Q,C,s0,s1,ONE,value)["value_of_contingency"]
        expected=float(max(Fraction(0),(
            s1*(value-Fraction(3,4))-Fraction(11,20)*(ONE-s0))/2))
        if abs(found-expected)>1e-12:
            raise ValueError("NO_GO_SHARP_SOURCE_THRESHOLD_VALIDATION")
    return {
        "root_s0":float(s0),"root_s1":float(s1),
        "threshold_fraction":str(threshold),
        "minimum_v_accuracy_for_strict_positive_gain":float(threshold),
        "strict_positive_gain_possible_with_v_accuracy_at_most_one":threshold<ONE,
        "strict_condition":"V accuracy > 3/4+(11/20)*(1-s0)/s1",
        "fixed_q":"1/5","fixed_cost":"1/4",
        "U_accuracy_irrelevant_to_THIS_specific_theorem":True,
        "leaf_confusion_accuracy_not_observed_in_bees":True,
    }

def decision_grid():
    s0s=(.5,.6,.7,.8,.9,1.)
    s1s=(.5,.6,.8,1.)
    aus=(.5,.7,.85,1.)
    avs=(.5,.75,.9,.95,1.)
    grid=[optimal_values(.2,.25,s0,s1,au,av)
          for s0 in s0s for s1 in s1s for au in aus for av in avs]
    return {
        "status":"STAGE21_SOURCE_FREE_NOISY_LEAF_EXACT_DECISION",
        "n_grid_cases":len(grid),
        "grid":grid,
        "fixed_q_and_c_gain_theorem":
            "max(0,(s1*(accuracy_V-3/4) - (11/20)*(1-s0))/2)",
        "sharp_case_root_s0_08_s1_06":sharp_v_threshold(.8,.6),
        "same_mean_leaf_accuracy_counterexample":[
            optimal_values(.2,.25,.8,.6,.8,1.),
            optimal_values(.2,.25,.8,.6,1.,.8)
        ],
        "no_real_bees":True,
        "no_measured_root_or_leaf_confusion":True,
        "no_leaf_perception_pilot":True,
        "normalized_reward_not_measured_sucrose":True,
        "no_original_animal_ethical_approval":True,
    }

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",default="stage21_exact_outputs")
    root=Path(p.parse_args().out);root.mkdir(parents=True,exist_ok=True)
    result=decision_grid()
    (root/"stage21_noisy_leaf_decision_grid.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE21_EXACT_NOISY_LEAF_RESULT "+json.dumps({
        "status":result["status"],"grid_cases":len(result["grid"]),
        "sharp_example":result["sharp_case_root_s0_08_s1_06"],
        "same_mean_leaf_accuracy_counterexample":[{
            "aU":r["U_recognition_accuracy"],
            "aV":r["V_recognition_accuracy"],
            "mean":r["balanced_leaf_accuracy"],
            "gain":r["value_of_contingency"]
        } for r in result["same_mean_leaf_accuracy_counterexample"]],
        "actual_bees":0
    },ensure_ascii=False,allow_nan=False),flush=True)
