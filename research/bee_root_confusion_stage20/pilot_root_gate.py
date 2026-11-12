"""Stage20 optional ROOT CUE pilot source contract, SYNTHETIC-ONLY.

Do not use this QA demonstrator to certify human or animal source data.
Real studies require source-verified independent colony identity, video,
hidden true root, classification before feedback, separate U/V learning
and preregistered source-specific uncertainty intervals. No real bees.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from asymmetric_root import exact_values

STUDY_Q=.2
STUDY_COST=.25

def synthetic_source():
    """Two entirely invented colonies; equal class counts, unlike expected field noise."""
    rows=[]
    for colony,source_bee,correct_n in (
          ("QA_C1","QA_B1",9),("QA_C2","QA_B1",5)):
        for truth in (0,1):
            for i in range(10):
                reported=truth if i<correct_n else 1-truth
                rows.append({
                    "trial_id":f"{colony}_{source_bee}_ROOT{truth}_{i+1:02d}",
                    "colony_id":colony,"bee_id":source_bee,
                    "source_phase":"independent_blinded_root_cue_classification_pilot",
                    "true_root_r":truth,
                    "reported_root_z":reported,
                    "cue_on_time_s":.5,
                    "report_time_s":1.2,
                    "feedback_time_s":2.,
                    "original_classification_video_verified":True,
                    "true_bit_concealed_until_feedback":True,
                    "additional_leaf_accessible":False,
                    "source_is_synthetic_QA_only":True,
                })
    return rows

def _fraction(numerator,denominator):
    if denominator<=0:
        raise ValueError("NO_GO_EMPTY_ORIGINAL_ROOT_CLASS")
    return numerator/denominator

def audit_pilot(rows):
    if not isinstance(rows,list) or not rows:
        raise ValueError("NO_GO_EMPTY_ORIGINAL_PILOT")
    known=set()
    by_bee=defaultdict(lambda:defaultdict(lambda:{"n":0,"correct":0}))
    bycol=defaultdict(set)
    totals={0:{"n":0,"correct":0},1:{"n":0,"correct":0}}
    for row in rows:
        trial=row.get("trial_id")
        if not isinstance(trial,str) or not trial:
            raise ValueError("NO_GO_MISSING_SOURCE_TRIAL_ID")
        if trial in known:
            raise ValueError("NO_GO_DUPLICATE_TRIAL_ORIGINAL_ID")
        known.add(trial)
        if row.get("source_is_synthetic_QA_only") is not True:
            raise ValueError("NO_GO_REAL_PILOT_NOT_AUTHORIZED_IN_MOCK")
        if (row.get("source_phase")!="independent_blinded_root_cue_classification_pilot" or
            row.get("additional_leaf_accessible") is not False):
            raise ValueError("NO_GO_NOT_INDEPENDENT_ROOT_CLASSIFICATION")
        if (row.get("original_classification_video_verified") is not True or
            row.get("true_bit_concealed_until_feedback") is not True):
            raise ValueError("NO_GO_NOT_BLINDED_SOURCE_ROOT_CLASSIFICATION")
        col=row.get("colony_id");bee=row.get("bee_id")
        if not isinstance(col,str) or not col or not isinstance(bee,str) or not bee:
            raise ValueError("NO_GO_MISSING_SOURCE_BEE_COLONY_ID")
        r=row.get("true_root_r");z=row.get("reported_root_z")
        if type(r) is not int or r not in (0,1) or type(z) is not int or z not in (0,1):
            raise ValueError("NO_GO_SOURCE_ROOT_CLASS_OR_REPORTED_BIT")
        t0=row.get("cue_on_time_s")
        t1=row.get("report_time_s")
        t2=row.get("feedback_time_s")
        if (any(type(t) not in (float,int) or not math.isfinite(t) for t in (t0,t1,t2))
            or not 0<=t0<t1<t2):
            raise ValueError("NO_GO_SOURCE_FEEDBACK_OR_TIMING")
        key=(col,bee)
        cell=by_bee[key][r]
        cell["n"]+=1
        cell["correct"]+=int(r==z)
        totals[r]["n"]+=1
        totals[r]["correct"]+=int(r==z)
        bycol[col].add(bee)
    by_bee_record=[]
    by_col_vals=defaultdict(list)
    for (col,bee),classes in sorted(by_bee.items()):
        if set(classes)!={0,1} or min(classes[k]["n"] for k in (0,1))<2:
            raise ValueError("NO_GO_INSUFFICIENT_PER_BEE_ROOT_CLASS_PILOT_TRIALS")
        s0=_fraction(classes[0]["correct"],classes[0]["n"])
        s1=_fraction(classes[1]["correct"],classes[1]["n"])
        # Real class sensitivities below .5 are OUTSIDE this theorem's
        # label-orientation assumptions; do not silently swap classes.
        if s0<.5 or s1<.5:
            raise ValueError("NO_GO_MOCK_ROOT_CLASS_BELOW_THEOREM_DOMAIN")
        x=exact_values(STUDY_Q,STUDY_COST,s0,s1)
        row={"colony_id":col,"bee_id":bee,"R0_trials":classes[0]["n"],
             "R1_trials":classes[1]["n"],"R0_correct":classes[0]["correct"],
             "R1_correct":classes[1]["correct"],"s0":s0,"s1":s1,
             "theoretical_access_gain_at_idealized_fixed_q_and_cost":x["value_of_contingency"]}
        by_bee_record.append(row)
        by_col_vals[col].append(row)
    cols=[]
    for colony,bees in sorted(by_col_vals.items()):
        mean=lambda name:sum(row[name] for row in bees)/len(bees)
        cols.append({"colony_id":colony,"source_bees":len(bees),
                     "bee_equal_s0":mean("s0"),"bee_equal_s1":mean("s1"),
                     "bee_equal_math_gain":mean("theoretical_access_gain_at_idealized_fixed_q_and_cost")})
    pooled_s0=_fraction(totals[0]["correct"],totals[0]["n"])
    pooled_s1=_fraction(totals[1]["correct"],totals[1]["n"])
    pooled=exact_values(STUDY_Q,STUDY_COST,pooled_s0,pooled_s1)["value_of_contingency"]
    equal_colony=sum(x["bee_equal_math_gain"] for x in cols)/len(cols)
    return {
        "status":"SYNTHETIC_CLASS_SPECIFIC_ROOT_PILOT_AUDIT",
        "source_trials":len(rows),"fake_source_colonies":len(cols),
        "fake_source_bees":len(by_bee_record),
        "per_fake_bee_source_cells":by_bee_record,
        "per_fake_colony_source_means":cols,
        "pooled_class_specific":{"s0":pooled_s0,"s1":pooled_s1,
                                 "R0_n":totals[0]["n"],"R1_n":totals[1]["n"]},
        "gain_at_pooled_class_accuracies":pooled,
        "equal_colony_mean_math_gain":equal_colony,
        "mean_of_nonlinear_gain_not_equal_gain_at_mean":True,
        "no_root_precision_confidence_intervals_estimated":True,
        "no_qualifying_real_pilot_done":True,
        "no_real_colony_recruitment":True,
        "not_a_real_organism_measurement":True,
        "q_and_cost_are_frozen_theoretical_hypotheses_only":[STUDY_Q,STUDY_COST]
    }

def run(root):
    root=Path(root)
    root.mkdir(parents=True,exist_ok=True)
    data=audit_pilot(synthetic_source())
    out=root/"stage20_mock_root_pilot_quality.json"
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE20_SYNTHETIC_ROOT_PILOT_CONTRACT "+json.dumps({
        "status":data["status"],
        "fake_trials":data["source_trials"],
        "fake_bees":data["fake_source_bees"],
        "fake_colonies":data["fake_source_colonies"],
        "fake_class_accuracy":data["pooled_class_specific"],
        "equal_colony_mean_idealized_gain":data["equal_colony_mean_math_gain"],
        "idealized_gain_at_pooled_class_accuracy":data["gain_at_pooled_class_accuracies"],
        "actual_animals":0
    },ensure_ascii=False,allow_nan=False),flush=True)
    return data

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage20_outputs")
    run(p.parse_args().out)
