"""Stage22: EXACT 8-world Bayesian source acquisition with four leaf bit errors.

No bee observations. Root R and hidden U/V are independently redrawn each
trial (R,V fair; U~Bern(q)). Root readout Z has class-specific rates s0,s1.
Each paid leaf cue is allowed ONCE; its displayed 0/1 bit has separate
class-correct probabilities aU0,aU1 and aV0,aV1. The first action can be
SKIP/U/V either after Z (contingent) or before Z (precommit). A second,
other leaf can be requested after the first; guessing without either is
permitted. The exact unnormalized joint-mass dynamic program uses Fraction.
Independent unit tests use normalized posterior distributions instead.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json,math

WORLDS=tuple(product((0,1),repeat=3))
ACTIONS=("SKIP","U","V")
HALF=F(1,2)
ONE=F(1)
Q=F(1,5)
C=F(1,4)

def _check(name,val,lo,hi=None):
    if type(val) not in (int,float,F) or not math.isfinite(float(val)):
        raise ValueError("NO_GO_NONFINITE_OR_INVALID_"+name.upper())
    number=val if isinstance(val,F) else F(str(val))
    if number<lo or (hi is not None and number>hi):
        raise ValueError("NO_GO_OUT_OF_SCOPE_"+name.upper())
    return number

def _mass(d):
    return sum(d.values(),F(0))

def _target(w):
    r,u,v=w
    return u if r==0 else v

def _guess(d):
    return max(sum((wt for world,wt in d.items() if _target(world)==k),F(0))
               for k in (0,1))

def _root_joint(q,s0,s1,z):
    return {
        (r,u,v):F(1,4)*(q if u else ONE-q)*(
            (s0 if z==0 else ONE-s0) if r==0
            else (ONE-s1 if z==0 else s1))
        for r,u,v in WORLDS
    }

def _leaf_joint(d,leaf,bit,aU0,aU1,aV0,aV1):
    pos=1 if leaf=="U" else 2
    correct0,correct1=(aU0,aU1) if leaf=="U" else (aV0,aV1)
    return {
       w:wt*((correct0 if bit==0 else ONE-correct0)
             if w[pos]==0 else (ONE-correct1 if bit==0 else correct1))
       for w,wt in d.items()
    }

def _first_paid_leaf(d,leaf,c,aU0,aU1,aV0,aV1):
    other="V" if leaf=="U" else "U"
    result=-c*_mass(d)
    for bit in (0,1):
        after=_leaf_joint(d,leaf,bit,aU0,aU1,aV0,aV1)
        stop=_guess(after)
        buy_second=-c*_mass(after)
        buy_second+=sum((_guess(_leaf_joint(
             after,other,b2,aU0,aU1,aV0,aV1)) for b2 in (0,1)),F(0))
        result+=max(stop,buy_second)
    return result

def _options(d,c,aU0,aU1,aV0,aV1):
    return {
      "SKIP":_guess(d),
      "U":_first_paid_leaf(d,"U",c,aU0,aU1,aV0,aV1),
      "V":_first_paid_leaf(d,"V",c,aU0,aU1,aV0,aV1)
    }

def _best(options):
    # On exact ties prefer no expenditure (SKIP first).
    return max(ACTIONS,key=lambda k:options[k])

def _solver(q,c,s0,s1,aU0,aU1,aV0,aV1):
    source={z:_options(_root_joint(q,s0,s1,z),c,aU0,aU1,aV0,aV1)
            for z in (0,1)}
    obs={z:_mass(_root_joint(q,s0,s1,z)) for z in (0,1)}
    if sum(obs.values(),F(0))!=ONE:
        raise ValueError("NO_GO_BAYES_SOURCE_NOT_NORMALIZED")
    active=sum((source[z][_best(source[z])] for z in (0,1)),F(0))
    static={act:sum((source[z][act] for z in (0,1)),F(0)) for act in ACTIONS}
    fixed_action=_best(static)
    pre=static[fixed_action]
    if active<pre:
        raise ValueError("NO_GO_CONDITIONAL_BAYES_DOMINANCE_VIOLATED")
    return active,pre,source,obs,fixed_action

def exact_values(q,c,s0,s1,aU0,aU1,aV0,aV1):
    q=_check("q",q,F(0),HALF)
    c=_check("leaf_cost",c,F(0))
    s0=_check("root_r0_correctness",s0,HALF,ONE)
    s1=_check("root_r1_correctness",s1,HALF,ONE)
    aU0=_check("u_true0_correctness",aU0,HALF,ONE)
    aU1=_check("u_true1_correctness",aU1,HALF,ONE)
    aV0=_check("v_true0_correctness",aV0,HALF,ONE)
    aV1=_check("v_true1_correctness",aV1,HALF,ONE)
    active,pre,branches,obs,pre_action=_solver(q,c,s0,s1,aU0,aU1,aV0,aV1)
    gain=active-pre
    if q==Q and c==C:
        # Sharp theorem: U's information contribution cannot pay for .25
        # when its biased prior has q=.2. Optimal precommit SKIPs.
        result=max(F(0),s1*(aV0+aV1-F(3,2))/4+
                   (ONE-s0)*(F(3,20)*aV0-F(3,20)*aV1-F(11,40)))
        if gain!=result or pre!=F(13,20) or pre_action!="SKIP":
            raise ValueError("NO_GO_SHARP_FOUR_CLASS_VALUE_NOT_MATCHED")
        if _best(branches[0])!="SKIP":
            raise ValueError("NO_GO_ROOT_Z0_SOURCE_UNEXPECTED_QUERY")
        if _best(branches[1])!=("V" if gain>0 else "SKIP"):
            raise ValueError("NO_GO_ROOT_Z1_QUERY_RULE_MISMATCH")
    return {
      "status":"EXACT_FOUR_CLASS_PAID_LEAF_CONFUSION_BAYES",
      "q":float(q),"leaf_cost":float(c),
      "s0_root_true0":float(s0),"s1_root_true1":float(s1),
      "U_true0_to_report0":float(aU0),
      "U_true1_to_report1":float(aU1),
      "V_true0_to_report0":float(aV0),
      "V_true1_to_report1":float(aV1),
      "u_balanced_bit_accuracy":float((aU0+aU1)/2),
      "v_balanced_bit_accuracy":float((aV0+aV1)/2),
      "contingent_optimum":float(active),
      "precommit_optimum":float(pre),
      "gain":float(gain),
      "first_action_after_z":{str(z):_best(branches[z]) for z in (0,1)},
      "first_action_precommit":pre_action,
      "observed_z_probability":{str(z):float(obs[z]) for z in (0,1)},
      "one_query_per_source_at_most":True,
      "no_live_animal_data":True,
      "cost_utility_is_normalized_assumed":True,
    }

def sharp_example():
    first=exact_values(.2,.25,.8,.6,.5,.5,1.,.9)
    second=exact_values(.2,.25,.8,.6,1.,1.,.9,1.)
    return {
      "root_class_correctness":[.8,.6],
      "exact_sharp_gain":"max(0, 0.18*aV0 + 0.12*aV1 - 0.28)",
      "exact_v_true0_more_important_than_true1_in_this_example":True,
      "matched_mean_V_bit_accuracy":.95,
      "aV0_1_aV1_0point9_gain":first["gain"],
      "aV0_0point9_aV1_1_gain":second["gain"],
      "ratio_of_positive_gains":first["gain"]/second["gain"],
      "not_an_observed_bee_effect":True
    }

def source_free_grid():
    roots=((.5,.5),(.6,.8),(.8,.6),(.9,.7),(.7,.9),(1.,1.))
    u_profiles=((.5,.5),(.8,.7),(1.,.9))
    v_profiles=((.5,.5),(.8,1.),(.9,.9),(.9,1.),(1.,.9),(1.,1.))
    rows=[exact_values(.2,.25,s0,s1,u0,u1,v0,v1)
          for s0,s1 in roots for u0,u1 in u_profiles for v0,v1 in v_profiles]
    return {
       "status":"STAGE22_FOUR_LEAF_BIT_ERRORS_EXACT_BAYES",
       "grid":rows,
       "sharp_q20_cost_quarter_formula":
          "max(0, s1*(v0+v1-3/2)/4 + (1-s0)*(3*v0/20-3*v1/20-11/40))",
       "worked_example":sharp_example(),
       "no_real_bee_data":True,
       "no_leaf_recognition_confusion_measured":True,
       "all_payoff_costs_hypothetical":True,
       "all_pilot_animal_recruitment":0,
    }

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="stage22_exact_outputs")
    folder=Path(ap.parse_args().out);folder.mkdir(parents=True,exist_ok=True)
    data=source_free_grid()
    (folder/"stage22_four_leaf_errors_math.json").write_text(
        json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE22_FOUR_CLASS_EXACT_MATH "+
          json.dumps({"status":data["status"],"n_cells":len(data["grid"]),
                      "example":data["worked_example"],"live_animals":0},
                     ensure_ascii=False,allow_nan=False),flush=True)
