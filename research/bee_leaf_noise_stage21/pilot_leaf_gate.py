"""Stage21 SYNTHETIC-only blinded original leaf-bit recognition pilot contract.

This code never ingests real bee observations. A future independently
approved original U/V pilot must verify true class labels, video timing,
leaf cue identity, light/odor leakage and colony-identified repeated trials.
The theorem here assumes SYMMETRIC binary leaf errors. An overall hit-rate
is not a sufficient substitute for two true-bit class sensitivities.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse
import json
import math
from pathlib import Path
from leaf_channel import optimal_values

THEOREM_Q=.2
THEOREM_COST=.25
ROOT_S0=.8
ROOT_S1=.6

def synthetic_source():
    records=[]
    for col,bee,accuracy in (
        ("QA_C1","QA_B1",{"U":4,"V":5}),
        ("QA_C2","QA_B1",{"U":5,"V":4})
    ):
        for leaf in ("U","V"):
            for truth in (0,1):
                for i in range(5):
                    report=truth if i<accuracy[leaf] else 1-truth
                    records.append({
                        "trial_id":f"{col}_{bee}_{leaf}_T{truth}_{i+1:02d}",
                        "colony_id":col,"bee_id":bee,
                        "leaf_type":leaf,"source_true_bit":truth,
                        "source_reported_bit":report,
                        "source_pilot_phase":"blinded_leaf_only_classification",
                        "root_r_visible":False,
                        "target_reward_position_visible":False,
                        "source_leaf_image_video_verified":True,
                        "source_bit_concealed_until_feedback":True,
                        "cue_on_time_s":.5,
                        "response_time_s":1.2,
                        "feedback_time_s":2.,
                        "source_is_mock_only":True
                    })
    return records

def audit_pilot(rows):
    if not isinstance(rows,list) or not rows:
        raise ValueError("NO_GO_EMPTY_ORIGINAL_LEAF_CLASSIFICATION")
    ids=set()
    counts=defaultdict(lambda:{"n":0,"correct":0})
    percol=defaultdict(set)
    for row in rows:
        ident=row.get("trial_id")
        if not isinstance(ident,str) or not ident or ident in ids:
            raise ValueError("NO_GO_DUPLICATE_ORIGINAL_TRIAL_ID")
        ids.add(ident)
        if row.get("source_is_mock_only") is not True:
            raise ValueError("NO_GO_REAL_ANIMAL_SOURCE_NOT_AUTHORIZED_IN_PUBLIC_QA")
        if row.get("source_pilot_phase")!="blinded_leaf_only_classification" or (
              row.get("root_r_visible") is not False) or (
              row.get("target_reward_position_visible") is not False) or (
              row.get("source_leaf_image_video_verified") is not True) or (
              row.get("source_bit_concealed_until_feedback") is not True):
            raise ValueError("NO_GO_LEAF_PILOT_NOT_BLINDED")
        colony=row.get("colony_id");bee=row.get("bee_id")
        if not isinstance(colony,str) or not colony or not isinstance(bee,str) or not bee:
            raise ValueError("NO_GO_MISSING_ORIGINAL_BEE_COLONY_ID")
        leaf=row.get("leaf_type")
        truth=row.get("source_true_bit")
        reported=row.get("source_reported_bit")
        if leaf not in ("U","V") or type(truth) is not int or truth not in (0,1) or (
             type(reported) is not int or reported not in (0,1)):
            raise ValueError("NO_GO_INVALID_SOURCE_LEAF_CLASS_OR_RESPONSE")
        times=[row.get(name) for name in
            ("cue_on_time_s","response_time_s","feedback_time_s")]
        if any(type(t) not in (float,int) or not math.isfinite(t) for t in times) or (
             not 0<=times[0]<times[1]<times[2]):
            raise ValueError("NO_GO_SOURCE_LEAF_FEEDBACK_TIMING")
        cell=counts[(colony,bee,leaf,truth)]
        cell["n"]+=1
        cell["correct"]+=int(truth==reported)
        percol[colony].add(bee)
    by_bee=defaultdict(dict)
    all_classes=Counter()
    for (colony,bee,leaf,truth),record in sorted(counts.items()):
        if record["n"]<2:
            raise ValueError("NO_GO_INSUFFICIENT_SOURCE_LEAF_BIT_CLASS")
        by_bee[(colony,bee)][(leaf,truth)]=record["correct"]/record["n"]
        all_classes[(leaf,truth,"n")]+=record["n"]
        all_classes[(leaf,truth,"correct")]+=record["correct"]
    enriched=[]
    symmetric=True
    bycol=defaultdict(list)
    for (colony,bee),lookup in sorted(by_bee.items()):
        required={(leaf,bit) for leaf in ("U","V") for bit in (0,1)}
        if set(lookup)!=required:
            raise ValueError("NO_GO_MISSING_SOURCE_LEAF_BIT_CLASS")
        au0,au1=lookup[("U",0)],lookup[("U",1)]
        av0,av1=lookup[("V",0)],lookup[("V",1)]
        if any(v<.5 for v in (au0,au1,av0,av1)):
            raise ValueError("NO_GO_SOURCE_LEAF_RELIABILITY_BELOW_ORIENTATION_DOMAIN")
        symmetric_this=(au0==au1 and av0==av1)
        symmetric=symmetric and symmetric_this
        x={"colony_id":colony,"bee_id":bee,
           "U_true0_to_report0":au0,"U_true1_to_report1":au1,
           "V_true0_to_report0":av0,"V_true1_to_report1":av1,
           "symmetric_leaf_error_model_applicable":symmetric_this}
        if symmetric_this:
            x["idealized_gain_given_fixed_assumed_root_and_cost"]=optimal_values(
                THEOREM_Q,THEOREM_COST,ROOT_S0,ROOT_S1,au0,av0)["value_of_contingency"]
        else:
            x["idealized_gain_given_fixed_assumed_root_and_cost"]=None
        enriched.append(x);bycol[colony].append(x)
    pooled={}
    for leaf in ("U","V"):
        class_rates={
          str(bit):all_classes[(leaf,bit,"correct")]/all_classes[(leaf,bit,"n")]
          for bit in (0,1)}
        pooled[leaf]=(all_classes[(leaf,0,"correct")]+all_classes[(leaf,1,"correct")])/(
                       all_classes[(leaf,0,"n")]+all_classes[(leaf,1,"n")])
    if symmetric:
        colony_gains={col:sum(x["idealized_gain_given_fixed_assumed_root_and_cost"]
                    for x in entries)/len(entries) for col,entries in bycol.items()}
        equalcol=sum(colony_gains.values())/len(colony_gains)
        pooled_gain=optimal_values(THEOREM_Q,THEOREM_COST,ROOT_S0,ROOT_S1,
                                    pooled["U"],pooled["V"])["value_of_contingency"]
    else:
        equalcol=None;pooled_gain=None
    return {
       "status":"SYNTHETIC_BLINDED_LEAF_CHANNEL_PILOT_QA" if symmetric
          else "NO_GO_ASYMMETRIC_LEAF_CONFUSION_NEEDS_DIFFERENT_THEOREM",
       "source_mock_trials":len(rows),
       "source_mock_bees":len(by_bee),
       "source_mock_colonies":len(bycol),
       "source_true_bit_specific_counts":{
           "__".join(map(str,key)):int(val) for key,val in sorted(all_classes.items())},
       "per_fake_bee_true_bit_class_sensitivities":enriched,
       "per_leaf_source_marginal_accuracy":pooled,
       "symmetric_error_assumption_checked_per_source_bee":symmetric,
       "equal_colony_mean_theoretical_gain":equalcol,
       "gain_at_pooled_accuracies":pooled_gain,
       "source_semantics":{"by_true_bit_class":True,
                           "U_biased_prior_not_a_license_for_all_zero_answers":True,
                           "root_not_available_during_leaf_pilot":True,
                           "classification_before_reward_feedback":True},
       "assumed_root_sensitivities_not_measured":[ROOT_S0,ROOT_S1],
       "assumed_normalized_cost_not_measured":THEOREM_COST,
       "real_bees":0,
       "not_a_real_organism_measurement":True,
       "no_animal_sensor_or_reward_calibration_performed":True
    }

def run(root):
    root=Path(root);root.mkdir(exist_ok=True,parents=True)
    data=audit_pilot(synthetic_source())
    if data["status"]!="SYNTHETIC_BLINDED_LEAF_CHANNEL_PILOT_QA":
        raise ValueError("NO_GO_MOCK_LEAF_CHANNEL_NOT_SYMMETRIC")
    outfile=root/"stage21_mock_leaf_pilot_qa.json"
    outfile.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE21_MOCK_LEAF_PILOT_SOURCE_QA "+json.dumps({
        "status":data["status"],"mock_trials":data["source_mock_trials"],
        "fake_colonies":data["source_mock_colonies"],
        "fake_animals":data["source_mock_bees"],
        "pooled_UV_accuracy":data["per_leaf_source_marginal_accuracy"],
        "gain_from_average_UV":data["gain_at_pooled_accuracies"],
        "colony_average_theory_gain":data["equal_colony_mean_theoretical_gain"],
        "live_bees":data["real_bees"]
    },ensure_ascii=False,allow_nan=False),flush=True)
    return data

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",default="stage21_exact_outputs")
    run(p.parse_args().out)
