"""Stage19: exact optional-query decisions with an imperfectly perceived root cue.

MATHEMATICAL SOURCE-FREE ANALYSIS ONLY. No animals or synthetic animal outcomes.
Eight hidden states (R,U,V), R~Bern(.5), U~Bern(q), V~Bern(.5).
Each world and noisy observed root signal Z is sampled independently on
different experimental trials. Root observation accuracy s=P(Z=R)∈[.5,1].
When R=0 the correct target is U; when R=1 it is V. Any paid leaf
request U/V perfectly reveals its bit; a correct final target pays one
normalized unit, a wrong target pays zero, and each leaf costs c.

The producer uses exact Fraction-valued UNNORMALIZED joint mass recursions.
The tests independently reconstruct normalized Bayesian posteriors.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
import math
import json
import argparse
from pathlib import Path

WORLDS=tuple(product((0,1),repeat=3))
ACTIONS=("SKIP","U","V")
THRESHOLD=Fraction(11,16)
EXAMPLE_Q=Fraction(1,5)
EXAMPLE_COST=Fraction(1,4)


def _parameter(name,v,lo,hi=None):
    if type(v) not in (int,float,Fraction) or not math.isfinite(float(v)):
        raise ValueError("NO_GO_INVALID_"+name.upper())
    f=Fraction(str(v)) if not isinstance(v,Fraction) else v
    if f<lo or (hi is not None and f>hi):
        raise ValueError("NO_GO_OUT_OF_BOUNDS_"+name.upper())
    return f


def _target(world):
    r,u,v=world
    return u if r==0 else v


def _root_joint(q,s,z):
    """Return exact *unconditioned* P(world, observed Z=z) masses."""
    return {
        (r,u,v): Fraction(1,4)*(q if u else (1-q))*
        (s if z==r else (1-s))
        for r,u,v in WORLDS
    }


def _mass(rows):
    return sum(rows.values(),Fraction(0))


def _guess(rows):
    return max(
        sum((weight for world,weight in rows.items()
             if _target(world)==k),Fraction(0))
        for k in (0,1)
    )


def _branch(rows,leaf,bit):
    pos=1 if leaf=="U" else 2
    return {world:weight for world,weight in rows.items() if world[pos]==bit}


def _paid_leaf_with_optional_second(rows,leaf,c):
    """First physical leaf is paid; after seeing its bit, second is optional."""
    other="V" if leaf=="U" else "U"
    total=-c*_mass(rows)
    for bit in (0,1):
        sliced=_branch(rows,leaf,bit)
        if not _mass(sliced):
            continue
        no_more=_guess(sliced)
        second=-c*_mass(sliced)+sum(
            (_guess(_branch(sliced,other,next_bit)) for next_bit in (0,1)),
            Fraction(0))
        total+=max(no_more,second)
    return total


def _first_action_values(rows,c):
    return {
        "SKIP":_guess(rows),
        "U":_paid_leaf_with_optional_second(rows,"U",c),
        "V":_paid_leaf_with_optional_second(rows,"V",c)
    }


def _best_action(values):
    # SKIP takes precedence on exact ties: do not imply the animal
    # requested an unnecessary cue merely because information was free.
    return max(ACTIONS,key=lambda name:values[name])


def _raw_optimal(q,c,s):
    branches={z:_first_action_values(_root_joint(q,s,z),c) for z in (0,1)}
    assert all(_mass(_root_joint(q,s,z))==Fraction(1,2) for z in (0,1))
    cont=sum((branches[z][_best_action(branches[z])] for z in (0,1)),Fraction(0))
    precommit_candidates={
        name:sum((branches[z][name] for z in (0,1)),Fraction(0))
        for name in ACTIONS
    }
    precommit_action=_best_action(precommit_candidates)
    precommit=precommit_candidates[precommit_action]
    return branches,cont,precommit,precommit_action,precommit_candidates


def optimal_values(q,c,root_accuracy):
    """Exact dynamic decision optimum with both action sets and real guessing."""
    qq=_parameter("q",q,Fraction(0),Fraction(1,2))
    cc=_parameter("cost",c,Fraction(0))
    ss=_parameter("root_accuracy",root_accuracy,Fraction(1,2),Fraction(1))
    byroot,cont,pre,pre_action,pre_candidates=_raw_optimal(qq,cc,ss)
    gain=cont-pre
    if gain<0:
        raise ValueError("NO_GO_CONDITIONAL_ACCESS_LOWER_THAN_PRECOMMIT")
    fixed=byroot[0]["SKIP"]+byroot[1]["V"]
    return {
        "status":"EXACT_BAYES_OPTIMAL_NOISY_ROOT_ACCESS",
        "q":float(qq),"leaf_query_cost":float(cc),"root_recognition_accuracy":float(ss),
        "contingent_optimum":float(cont),
        "precommit_optimum":float(pre),
        "contingent_minus_precommit":float(gain),
        "optimal_first_after_root":{
            str(z):_best_action(byroot[z]) for z in (0,1)},
        "optimal_first_precommit":pre_action,
        "conditional_action_values":{
            str(z):{name:float(value/Fraction(1,2))
                    for name,value in byroot[z].items()} for z in (0,1)},
        "precommit_candidate_values":{
            name:float(value) for name,value in pre_candidates.items()},
        "fixed_root0_skip_root1_v_minus_optimal_precommit":float(fixed-pre),
        "root_signal_likelihood_biased_by_true_R_only":True,
        "second_leaf_query_optional_after_first":True,
        "perfect_leaf_recognition_ASSUMED":True,
        "exact_fraction_arithmetic_used_for_values":True,
        "no_original_animal_data":True
    }


def threshold_witness():
    """Analytical sharp s-threshold for q=1/5, c=1/4, s∈[1/2,1]."""
    evaluations=[]
    for ss in (Fraction(1,2),Fraction(3,5),Fraction(11,16),Fraction(7,10),
               Fraction(3,4),Fraction(9,10),Fraction(1)):
        branches,cont,pre,_,_= _raw_optimal(EXAMPLE_Q,EXAMPLE_COST,ss)
        expected=max(Fraction(0),Fraction(2,5)*ss-Fraction(11,40))
        if pre!=Fraction(13,20) or cont-pre!=expected:
            raise ValueError("NO_GO_SHARP_ROOT_RECOGNITION_THRESHOLD")
        if _best_action(branches[0])!="SKIP":
            raise ValueError("NO_GO_ROOT0_NOT_SKIP_IN_CLAIMED_REGION")
        if _best_action(branches[1])!=("V" if ss>THRESHOLD else "SKIP"):
            raise ValueError("NO_GO_ROOT1_QUERY_THRESHOLD")
        evaluations.append({
           "s_fraction":str(ss),"root_accuracy":float(ss),
           "contingent_gain":float(cont-pre),
           "fixed_policy_advantage_when_not_optimized":float(
                  branches[0]["SKIP"]+branches[1]["V"]-pre)
        })
    return {
        "status":"EXACT_SHARP_S_THRESHOLD_FOR_ONE_ASYMMETRIC_TASK",
        "q_fraction":"1/5","leaf_cost_fraction":"1/4",
        "threshold_fraction":str(THRESHOLD),
        "threshold_percent":100*float(THRESHOLD),
        "strict_s_condition":"s>11/16",
        "expected_gain_formula":"max(0,2*s/5-11/40)",
        "precommit_optimum_constant_fraction":"13/20",
        "root0_optimum":"SKIP for all s in [1/2,1]",
        "root1_optimum":"SKIP for s<=11/16, V for s>11/16",
        "examples":evaluations,
        "recognition_accuracy_is_an_assumption_not_measured_in_bees":True
    }


def decision_grid():
    q_values=(0.,.10,.20,.35,.50)
    cost_values=(0.,.05,.1,.2,.25,.4,.6)
    s_values=(.5,.6,.65,.6875,.7,.75,.8,.9,1.)
    return {
        "status":"STAGE19_EXACT_NOISY_ROOT_DECISION_SURFACE",
        "description":"Source-free Bayesian decision surface; independent original trials hypothetical",
        "test_example":threshold_witness(),
        "source_parameter_grid":{
            "q":q_values,"normalized_leaf_cost":cost_values,
            "root_recognition_accuracy":s_values},
        "grid":[optimal_values(q,c,s) for q in q_values
                  for c in cost_values for s in s_values],
        "no_original_animal_data":True,
        "no_root_cue_confusion_matrix_measured":True,
        "not_an_actual_recruitment_or_fitness_estimate":True,
        "perfect_leaf_readout_unverified":True,
        "source_cost_has_no_empirical_milligram_or_second_calibration":True,
    }


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="stage19_exact_outputs")
    root=Path(ap.parse_args().out)
    root.mkdir(exist_ok=True,parents=True)
    result=decision_grid()
    (root/"stage19_exact_noisy_root_threshold.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE19_EXACT_THRESHOLD_RESULT "+
          json.dumps({"threshold":result["test_example"],
                      "grid_cases":len(result["grid"]),
                      "original_living_bees_observed":0},
                    ensure_ascii=False,allow_nan=False),flush=True)
