"""Stage22 mock-only pilot contract for FOUR class-conditional U/V readout rates.

This code is never authorized to process living bee observations. Original
approved study would need R0/R1 root confusion, original colony labels,
U0/U1/V0/V1 class recognition and measured information cost/reward.
The toy source emits exactly 80 synthetic image-response records across
two invented colony/bee identities. True bits are explicitly balanced
during this BLINDED sensory pilot despite U~Bern(.2) in the decision model.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse,json,math
from pathlib import Path
from leaf_bit_confusion import exact_values

Q=.2
C=.25
ROOT_S0=.8
ROOT_S1=.6

def fake_leaf_classifications():
    fake_colonies={
      "MOCK_C1":{"U":(8,7),"V":(10,9)},
      "MOCK_C2":{"U":(9,8),"V":(9,10)}
    }
    rows=[]
    for col,source in sorted(fake_colonies.items()):
        bee="MOCK_B1"
        for leaf in ("U","V"):
            for true_bit in (0,1):
                correct_n=source[leaf][true_bit]
                for k in range(10):
                    report=true_bit if k<correct_n else 1-true_bit
                    rows.append({
                      "trial_id":f"{col}_{bee}_{leaf}_TRUE{true_bit}_{k+1:02d}",
                      "colony_id":col,"bee_id":bee,
                      "source_phase":"blinded_U_or_V_single_bit_recognition",
                      "leaf_type":leaf,"true_leaf_bit":true_bit,
                      "reported_leaf_bit":report,
                      "cue_on_time_s":.5,
                      "response_time_s":1.2,
                      "feedback_time_s":2.0,
                      "source_photo_video_verified":True,
                      "root_visible":False,
                      "feeder_reward_position_visible":False,
                      "other_leaf_visible":False,
                      "source_bit_concealed_until_feedback":True,
                      "mock_only":True
                    })
    return rows

def audit_source(records):
    if not isinstance(records,list) or not records:
        raise ValueError("NO_GO_EMPTY_LEAF_SOURCE_PILOT")
    original_ids=set()
    groups=defaultdict(lambda:{"n":0,"correct":0})
    colonies=defaultdict(set)
    for row in records:
        tid=row.get("trial_id")
        if not isinstance(tid,str) or not tid or tid in original_ids:
            raise ValueError("NO_GO_DUPLICATE_SOURCE_TRIAL_ID")
        original_ids.add(tid)
        if row.get("mock_only") is not True:
            raise ValueError("NO_GO_REAL_ANIMAL_DATA_NOT_AUTHORIZED")
        if (row.get("source_phase")!="blinded_U_or_V_single_bit_recognition" or
            row.get("source_photo_video_verified") is not True or
            row.get("source_bit_concealed_until_feedback") is not True or
            row.get("root_visible") is not False or
            row.get("feeder_reward_position_visible") is not False or
            row.get("other_leaf_visible") is not False):
            raise ValueError("NO_GO_LEAF_PILOT_NOT_BLINDED")
        col=row.get("colony_id");bee=row.get("bee_id")
        if not isinstance(col,str) or not col or not isinstance(bee,str) or not bee:
            raise ValueError("NO_GO_ORIGINAL_BEE_COLONY_NOT_RECORDED")
        leaf=row.get("leaf_type")
        if leaf not in ("U","V"):
            raise ValueError("NO_GO_UNKNOWN_LEAF_SOURCE")
        truth=row.get("true_leaf_bit");report=row.get("reported_leaf_bit")
        if type(truth) is not int or truth not in (0,1) or type(report) is not int or report not in (0,1):
            raise ValueError("NO_GO_BIT_NOT_TRUE_BINARY_INTEGER")
        times=[row.get(k) for k in
               ("cue_on_time_s","response_time_s","feedback_time_s")]
        if any(type(t) not in (int,float) or not math.isfinite(t) for t in times) or (
             not 0<=times[0]<times[1]<times[2]):
            raise ValueError("NO_GO_FEEDBACK_BEFORE_LEAF_REPORT")
        counts=groups[(col,bee,leaf,truth)]
        counts["n"]+=1;counts["correct"]+=int(truth==report)
        colonies[col].add(bee)
    per_bee=defaultdict(dict)
    pooled=defaultdict(lambda:{"n":0,"correct":0})
    for (col,bee,leaf,truth),d in sorted(groups.items()):
        if d["n"]<2:
            raise ValueError("NO_GO_TOO_FEW_TRUE_CLASS_EXPOSURES")
        key=(col,bee)
        per_bee[key][(leaf,truth)]=d["correct"]/d["n"]
        stat=pooled[(leaf,truth)]
        stat["n"]+=d["n"];stat["correct"]+=d["correct"]
    for rates in per_bee.values():
        if set(rates)!={(leaf,bit) for leaf in ("U","V") for bit in (0,1)}:
            raise ValueError("NO_GO_MISSING_LEAF_TRUE_BIT_CLASS")
    percol=defaultdict(list)
    animal_rates=[]
    for (col,bee),rates in sorted(per_bee.items()):
        u0,u1,v0,v1=(rates["U",0],rates["U",1],rates["V",0],rates["V",1])
        if any(x<.5 for x in (u0,u1,v0,v1)):
            raise ValueError("NO_GO_CLASS_RECOGNITION_OUTSIDE_THEOREM")
        math_result=exact_values(Q,C,ROOT_S0,ROOT_S1,u0,u1,v0,v1)
        record={"colony":col,"bee":bee,"U0":u0,"U1":u1,"V0":v0,"V1":v1,
                "idealized_optimal_gain":math_result["gain"]}
        percol[col].append(record)
        animal_rates.append(record)
    avgcol={col:sum(x["idealized_optimal_gain"] for x in v)/len(v)
            for col,v in sorted(percol.items())}
    equalcol=sum(avgcol.values())/len(avgcol)
    pooled_rates={"".join((leaf,str(bit))):pooled[leaf,bit]["correct"]/pooled[leaf,bit]["n"]
                  for leaf in ("U","V") for bit in (0,1)}
    at_pool=exact_values(Q,C,ROOT_S0,ROOT_S1,
        pooled_rates["U0"],pooled_rates["U1"],
        pooled_rates["V0"],pooled_rates["V1"])["gain"]
    return {
      "status":"STAGE22_FOUR_CLASS_LEAF_MOCK_SOURCE_VERIFIED",
      "fake_original_rows":len(records),
      "fake_bees":len(animal_rates),
      "fake_colonies":len(colonies),
      "source_records_per_true_leaf_class":{
          "".join((leaf,str(bit))):pooled[leaf,bit]["n"]
          for leaf in ("U","V") for bit in (0,1)},
      "per_fake_bee_four_class_rates":animal_rates,
      "pooled_four_rates":pooled_rates,
      "individual_illustrative_gains_by_colony":avgcol,
      "equal_colony_mean_theoretical_gain":equalcol,
      "gain_at_pooled_class_rates":at_pool,
      "mock_bit_classes_explicitly_balanced_not_U_prior":True,
      "root_and_reward_and_other_leaf_inaccessible":True,
      "all_rates_are_injected_fake_source_qa":True,
      "no_empirical_credible_intervals_or_hierarchical_fit":True,
      "real_animal_observations":0
    }

def run(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    data=audit_source(fake_leaf_classifications())
    (root/"stage22_mock_four_class_pilot.json").write_text(
        json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE22_MOCK_LEAF_FOUR_CLASS_SOURCE_QA "+json.dumps({
        "status":data["status"],"fake_trials":data["fake_original_rows"],
        "class_rates":data["pooled_four_rates"],
        "per_fake_colony_gains":data["individual_illustrative_gains_by_colony"],
        "real_animals":0
    },ensure_ascii=False,allow_nan=False),flush=True)
    return data

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="stage22_exact_outputs")
    run(ap.parse_args().out)
