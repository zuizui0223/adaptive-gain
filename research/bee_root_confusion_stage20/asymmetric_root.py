"""Stage20 exact optional querying with CLASS-SPECIFIC root recognition errors.

No animals measured. Exact rational 8-state Bayesian decision problem.
s0=P(observed Z=0 | actual R=0) and s1=P(Z=1 | R=1), both >=1/2.
For the fixed q=1/5, cost c=1/4 model on [1/2,1]^2:
  contingent-minus-precommit = max(0,(11*s0+5*s1-11)/40)
This is an exact mathematical decision plane, not bee perceptual data.

Reuse Stage19's exact joint-mass decision operators; Stage20 tests separately
construct a normalized posterior oracle and check the full policy set.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import argparse
import json

from root_noisy import (
    WORLDS, ACTIONS, _parameter, _first_action_values, _best_action, _mass
)

HALF=Fraction(1,2)
ONE=Fraction(1)
Q_EXAMPLE=Fraction(1,5)
C_EXAMPLE=Fraction(1,4)


def _joint_worlds(q,s0,s1,z):
    return {
        (r,u,v):Fraction(1,4)*(q if u else ONE-q)*(
            (s0 if z==0 else ONE-s0)
            if r==0 else (ONE-s1 if z==0 else s1))
        for r,u,v in WORLDS
    }


def _exact(q,c,s0,s1):
    branches={}
    obs_probability={}
    for z in (0,1):
        joint=_joint_worlds(q,s0,s1,z)
        obs_probability[z]=_mass(joint)
        if obs_probability[z]<=0:
            raise ValueError("NO_GO_ROOT_OBSERVATION_IMPOSSIBLE_IN_DOMAIN")
        branches[z]=_first_action_values(joint,c)
    if sum(obs_probability.values(),Fraction(0))!=ONE:
        raise ValueError("NO_GO_ROOT_CONFUSION_DISTRIBUTION_NOT_NORMALIZED")
    cont=sum((branches[z][_best_action(branches[z])] for z in (0,1)),Fraction(0))
    pre_candidates={
        a:sum((branches[z][a] for z in (0,1)),Fraction(0))
        for a in ACTIONS
    }
    pre_action=_best_action(pre_candidates)
    pre=pre_candidates[pre_action]
    if cont<pre:
        raise ValueError("NO_GO_CONTINGENT_CANNOT_BE_WORSE_WHEN_OPTIMAL")
    return branches,obs_probability,cont,pre,pre_action,pre_candidates


def exact_values(q,leaf_cost,sensitivity_r0,specificity_r1):
    """Return exact rational-source derived values, display as JSON-safe floats."""
    q=_parameter("q",q,Fraction(0),HALF)
    c=_parameter("leaf_cost",leaf_cost,Fraction(0))
    s0=_parameter("sensitivity_r0",sensitivity_r0,HALF,ONE)
    s1=_parameter("specificity_r1",specificity_r1,HALF,ONE)
    branch,obs,cont,pre,action,pc=_exact(q,c,s0,s1)
    gain=cont-pre
    fixed=branch[0]["SKIP"]+branch[1]["V"]-pre
    if q==Q_EXAMPLE and c==C_EXAMPLE:
        sharp=max(Fraction(0),(11*s0+5*s1-11)/40)
        if gain!=sharp or pre!=Fraction(13,20):
            raise ValueError("NO_GO_SHARP_CLASS_SPECIFIC_PLANE_MISMATCH")
        if _best_action(branch[0])!="SKIP":
            raise ValueError("NO_GO_ROOT_Z0_UNEXPECTED_QUERY")
        expected_action="V" if 11*s0+5*s1>11 else "SKIP"
        if _best_action(branch[1])!=expected_action:
            raise ValueError("NO_GO_ROOT_Z1_SOURCE_SELECTION_MISMATCH")
    return {
        "status":"EXACT_CLASS_SPECIFIC_ROOT_CONFUSION_DECISION_VALUE",
        "q":float(q),"cost":float(c),
        "s0_P_Z0_given_R0":float(s0),
        "s1_P_Z1_given_R1":float(s1),
        "balanced_accuracy":float((s0+s1)/2),
        "observed_z_probability":{str(z):float(obs[z]) for z in (0,1)},
        "contingent_optimum":float(cont),
        "precommit_optimum":float(pre),
        "value_of_contingency":float(gain),
        "first_action_after_z":{str(z):_best_action(branch[z]) for z in (0,1)},
        "precommitted_action":action,
        "conditional_first_action_values_given_z":{
            str(z):{a:float(branch[z][a]/obs[z]) for a in ACTIONS} for z in (0,1)},
        "fixed_skip0_v1_minus_precommit":float(fixed),
        "source_symmetric_root_errors_not_assumed":True,
        "only_theoretical_perfect_leaf_readout":True,
        "exact_rational_joint_worlds":True,
        "real_bees_observed":0,
    }


def threshold_boundary(s0):
    """s1 strict lower bound at fixed q=.2 c=.25 over s0,s1 in [.5,1]."""
    z=_parameter("sensitivity_r0",s0,HALF,ONE)
    boundary=11*(ONE-z)/5
    return {
        "q":.2,"c":.25,"s0":float(z),
        "s1_threshold_for_positive_value":float(boundary),
        "sharp_positive_iff":"11*s0+5*s1>11",
        "positive_possible_in_theorem_accuracy_domain":bool(boundary<ONE),
        "above_threshold_at_s1_equal_half":bool(HALF>boundary),
        "biological_threshold_not_measured":True
    }


def matched_average_accuracy(s0_a,s1_a,s0_b,s1_b):
    """Counterexample: identical balanced accuracies, different cue-routing value."""
    a=exact_values(.2,.25,s0_a,s1_a)
    b=exact_values(.2,.25,s0_b,s1_b)
    ba=Fraction(str(a["s0_P_Z0_given_R0"]))+Fraction(str(a["s1_P_Z1_given_R1"]))
    bb=Fraction(str(b["s0_P_Z0_given_R0"]))+Fraction(str(b["s1_P_Z1_given_R1"]))
    if ba!=bb:
        raise ValueError("NO_GO_NOT_SAME_BALANCED_ACCURACY")
    return {
        "same_balanced_accuracy":float(ba/2),
        "first_confusion_pair":[s0_a,s1_a],
        "second_confusion_pair":[s0_b,s1_b],
        "first_gain":a["value_of_contingency"],
        "second_gain":b["value_of_contingency"],
        "conclusion":"Balanced recognition accuracy does not identify optimal access value",
        "no_animal_data":True
    }


def decision_grid():
    source=(.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,1.)
    grid=[exact_values(.2,.25,s0,s1) for s0 in source for s1 in source]
    symmetric=[exact_values(.2,.25,s,s) for s in source]
    representative=[
        exact_values(.2,.25,s0,s1) for s0,s1 in
        ((.9,.7),(.7,.9),(.8,.6),(.6,.8),(1.,1.),(.5,.5))
    ]
    individual_A=exact_values(.2,.25,.9,.9)["value_of_contingency"]
    individual_B=exact_values(.2,.25,.5,.5)["value_of_contingency"]
    pooled=exact_values(.2,.25,.7,.7)["value_of_contingency"]
    return {
        "status":"STAGE20_ASYMMETRIC_CONFUSION_EXACT_BAYES_GRID",
        "sharp_fixed_example":"gain=max(0,(11*s0+5*s1-11)/40), q=1/5,c=1/4",
        "strict_criterion":"11*s0+5*s1>11, for 1/2<=s0,s1<=1",
        "source_parameter_levels":source,
        "grid":grid,"symmetric_reduction":symmetric,
        "matched_balanced_accuracy_counterexamples":[
            matched_average_accuracy(.8,.6,.6,.8),
            matched_average_accuracy(.9,.7,.7,.9)
        ],
        "representative_points":representative,
        "individual_vs_pooled_information_gain_example":{
            "two_individual_optimal_gains":[individual_A,individual_B],
            "equal_individual_mean_gain":(individual_A+individual_B)/2,
            "gain_at_average_class_sensitivities":pooled,
            "independent_colony_generalization_not_identified":True
        },
        "no_real_bees_observed":True,
        "per_root_class_accuracy_unmeasured":True,
        "no_actual_root_confusion_matrix":True,
        "source_cost_unit_normalized_not_sec_or_mg":True,
        "leaf_cues_perfect_recognition_assumed":True,
        "simulation_is_idealized_not_animal_fitness":True,
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage20_outputs")
    root=Path(p.parse_args().out)
    root.mkdir(parents=True,exist_ok=True)
    data=decision_grid()
    (root/"stage20_two_class_confusion_frontier.json").write_text(
        json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE20_CONFUSION_CLASS_RESULT "+json.dumps({
        "status":data["status"],
        "grid_cases":len(data["grid"]),
        "matched_accuracy_pairs":data["matched_balanced_accuracy_counterexamples"],
        "individual_vs_pooled":data["individual_vs_pooled_information_gain_example"],
        "actual_bees":0
    },ensure_ascii=False,allow_nan=False),flush=True)
