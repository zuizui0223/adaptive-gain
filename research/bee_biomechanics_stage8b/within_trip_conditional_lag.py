"""Stage8b: source-trip-conditioned lag predictors and constrained negative control.

New control is EXPLORATORY/POSTHOC relative to the Stage8 positive M0→M1
result. Original Cambridge source has individually tagged bees from 3
colonies, but *Flower ID is NOT a physical flower location*.

Conditioned permutations preserve actual next-visit H/V outcomes, exact
source within-bee trip and uninterrupted segment, and fixed earlier-bout
M0/M1/M2 parameters. They randomize source-coded PREDECESSOR STATES only;
null records do not represent physically plausible reconstructed bee tracks.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from pathlib import Path
from statistics import mean
import hashlib
import json
import math
import random
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bee_biomechanics_stage8"))
from episode_audit import (ORIGINAL_OBS_SHA256,native_rows,source_episode_audit)
from heldout_experience_choice import (
    true_visited_pairs,split_bee_source_trips,fit_probabilities,score_edges,
    evaluate
)

SHUFFLES=199
SEED=20261028
FROZEN_STAGE8_BEE_GAIN=0.051525510437894245
FROZEN_STAGE8_DRINK_GAIN=0.004750769848322038
SOURCE_POP=(61592,38,3)
FROZEN_TEST=(36,3,1234)
MIN_ORIENTATION_EXCHANGEABLE_EDGES=200
MIN_DRINK_EXCHANGEABLE_EDGES=100
MIN_TAGS=10
MIN_PER_BEE=5

def contiguous_segments(edges):
    """Split adjacent source edges without crossing a real trip or rest.

    The connecting source episode has equal original row index:
    prior edge's next == current edge's previous episode.
    """
    sorted_edges=sorted(edges,key=lambda x:x["source_prev_first"])
    output=[]
    current=[]
    for edge in sorted_edges:
        if current:
            prev=current[-1]
            if (prev["trip"] != edge["trip"] or
                prev["source_next_first"] != edge["source_prev_first"]):
                output.append(current)
                current=[]
            elif (prev["colony"],prev["bee"])!=(edge["colony"],edge["bee"]):
                raise ValueError("NO_GO_SEGMENT_CROSSES_BEE")
        current.append(edge)
    if current:output.append(current)
    if sum(len(x) for x in output)!=len(edges):
        raise ValueError("NO_GO_SEGMENT_ROW_MULTIPLICATION")
    return output


def eligibility(bees):
    summary={"all_source_heldout_test_pairs":sum(len(b["test_pairs"]) for b in bees),
             "heldout_original_bees":len(bees),
             "distinct_colonies":len({b["colony"] for b in bees}),
             "original_uninterrupted_segments":0,
             "source_test_segment_pair_sizes":Counter(),
             "primary_mixed_orientation_exchangeable_pair_count":0,
             "primary_bees_ge5_exchangeable_pairs":0,
             "secondary_mixed_drink_exchangeable_pair_count":0,
             "secondary_bees_ge5_exchangeable_pairs":0}
    perbee=[]
    for b in bees:
        segments=contiguous_segments(b["test_pairs"])
        oriented=0;drank=0
        for seg in segments:
            summary["original_uninterrupted_segments"]+=1
            summary["source_test_segment_pair_sizes"][str(len(seg))]+=1
            if len(seg)>1 and len({e["previous_orientation"] for e in seg})>1:
                oriented+=len(seg)
            for h in ("horizontal","vertical"):
                group=[x for x in seg if x["previous_orientation"]==h]
                if len(group)>1 and len({x["previous_recorded_drink"] for x in group})>1:
                    drank+=len(group)
        summary["primary_mixed_orientation_exchangeable_pair_count"]+=oriented
        summary["secondary_mixed_drink_exchangeable_pair_count"]+=drank
        summary["primary_bees_ge5_exchangeable_pairs"]+=oriented>=MIN_PER_BEE
        summary["secondary_bees_ge5_exchangeable_pairs"]+=drank>=MIN_PER_BEE
        perbee.append({"colony":b["colony"],"tag":b["bee"],
                       "test_true_pairs":len(b["test_pairs"]),
                       "segments":len(segments),
                       "primary_exchangeable_pairs":oriented,
                       "secondary_exchangeable_pairs":drank})
    summary["source_test_segment_pair_sizes"]=dict(summary["source_test_segment_pair_sizes"])
    summary["per_bee_exchangeability"]=perbee
    summary["primary_gate"]="PASS" if (
        summary["primary_mixed_orientation_exchangeable_pair_count"]>=MIN_ORIENTATION_EXCHANGEABLE_EDGES
        and summary["primary_bees_ge5_exchangeable_pairs"]>=MIN_TAGS
    ) else "NO_GO_INSUFFICIENT_WITHIN_SEGMENT_ORIENTATION_MIX"
    summary["secondary_gate"]="PASS" if (
        summary["secondary_mixed_drink_exchangeable_pair_count"]>=MIN_DRINK_EXCHANGEABLE_EDGES
        and summary["secondary_bees_ge5_exchangeable_pairs"]>=MIN_TAGS
    ) else "NO_GO_INSUFFICIENT_WITHIN_ORIENTATION_DRINK_MIX"
    return summary


def permuted_test_edges(test, rng, mode):
    if mode not in ("orientation_and_drink","drink_given_orientation"):
        raise ValueError("NO_GO_INVALID_LOCKED_SHUFFLE_MODE")
    segments=contiguous_segments(test)
    new=[]
    changed=0
    for segment in segments:
        local=[dict(e) for e in segment]
        if mode=="orientation_and_drink":
            states=[(x["previous_orientation"],x["previous_recorded_drink"])
                    for x in local]
            rng.shuffle(states)
            for r,(o,d) in zip(local,states):
                if (r["previous_orientation"],r["previous_recorded_drink"])!=(o,d):
                    changed+=1
                r["previous_orientation"]=o
                r["previous_recorded_drink"]=d
        else:
            for orient in ("horizontal","vertical"):
                ids=[i for i,x in enumerate(local)
                     if x["previous_orientation"]==orient]
                flags=[local[i]["previous_recorded_drink"] for i in ids]
                rng.shuffle(flags)
                for i,new_flag in zip(ids,flags):
                    changed+=int(local[i]["previous_recorded_drink"]!=new_flag)
                    local[i]["previous_recorded_drink"]=new_flag
        # Critical outcome firewall: all next flower choices and their real
        # original row indices remain unchanged; only source prior labels
        # are conditionally reassigned for this statistical null.
        for a,z in zip(segment,local):
            assert a["next_horizontal"]==z["next_horizontal"]
            assert a["source_prev_first"]==z["source_prev_first"]
            assert a["source_next_first"]==z["source_next_first"]
            assert a["trip"]==z["trip"]
            assert a["colony"]==z["colony"] and a["bee"]==z["bee"]
        new.extend(local)
    if len(new)!=len(test):
        raise ValueError("NO_GO_MALFORMED_PSEUDO_TEST_POPULATION")
    return new,changed


def _signed_effect(bees,models_by_bee,mode=None,rng=None):
    percol=defaultdict(list)
    details=[]
    changes=0
    for b in bees:
        key=(b["colony"],b["bee"])
        training=models_by_bee[key]
        tests=b["test_pairs"]
        if mode is not None:
            tests,nchanged=permuted_test_edges(tests,rng,mode)
            changes+=nchanged
        scores,_=score_edges(tests,training)
        col=b["colony"]
        g01=scores["M0"]-scores["M1"]
        g12=scores["M1"]-scores["M2"]
        percol[col].append((g01,g12))
        details.append({"tag":b["bee"],"colony":col,
                        "heldout_pairs":len(tests),
                        "M0_to_M1_gain":g01,
                        "M1_to_M2_gain":g12,
                        "M0_nll":scores["M0"],
                        "M1_nll":scores["M1"],
                        "M2_nll":scores["M2"]})
    if len(percol)!=3:
        raise ValueError("NO_GO_MISSING_INDEPENDENT_SOURCE_COLONY")
    cvals=[
        {"colony":c,"source_bees":len(pairs),
         "M0_to_M1_mean":mean(x[0] for x in pairs),
         "M1_to_M2_mean":mean(x[1] for x in pairs)}
        for c,pairs in sorted(percol.items())
    ]
    return {
        "source_bees":len(details),"source_colonies":len(cvals),
        "source_test_pairs":sum(d["heldout_pairs"] for d in details),
        "M0_to_M1_gain_colony_equal":mean(x["M0_to_M1_mean"] for x in cvals),
        "M1_to_M2_gain_colony_equal":mean(x["M1_to_M2_mean"] for x in cvals),
        "M0_to_M1_gain_bee_equal":mean(d["M0_to_M1_gain"] for d in details),
        "M1_to_M2_gain_bee_equal":mean(d["M1_to_M2_gain"] for d in details),
        "M0_equal_bee_nll":mean(d["M0_nll"] for d in details),
        "M1_equal_bee_nll":mean(d["M1_nll"] for d in details),
        "M2_equal_bee_nll":mean(d["M2_nll"] for d in details),
        "per_colony":cvals,"per_bee":details,
        "source_previous_labels_reassigned":changes
    }


def _one_null(bees,models,actual,mode,permutations,seed,primary):
    rng=random.Random(seed)
    actual_gain=actual["M0_to_M1_gain_colony_equal" if primary else
                       "M1_to_M2_gain_colony_equal"]
    empirical=[]
    changed=[]
    for trial in range(permutations):
        val=_signed_effect(bees,models,mode=mode,rng=rng)
        # M0 must remain identical even under primary; M1 must remain
        # identical under secondary conditional-on-orientation shuffles.
        if abs(val["M0_equal_bee_nll"]-actual["M0_equal_bee_nll"])>1e-11:
            raise ValueError("NO_GO_RESHUFFLED_NEXT_OUTCOME_OR_CHANGED_M0")
        if not primary and abs(val["M1_equal_bee_nll"]-actual["M1_equal_bee_nll"])>1e-11:
            raise ValueError("NO_GO_SECONDARY_CHANGED_PREVIOUS_ORIENTATION")
        empirical.append(val["M0_to_M1_gain_colony_equal" if primary
                            else "M1_to_M2_gain_colony_equal"])
        changed.append(val["source_previous_labels_reassigned"])
    empirical.sort()
    mnull=mean(empirical)
    return {
        "status":"COMPUTED_SOURCE_SEGMENT_CONDITIONAL_LAG_NULL",
        "mode":mode,"permutations":permutations,"seed":seed,
        "actual_colony_equal_gain":actual_gain,
        "mean_null_colony_equal_gain":mnull,
        "actual_minus_null_mean_nats":actual_gain-mnull,
        "null_min":empirical[0],"null_max":empirical[-1],
        "null_q05":empirical[int(.05*(permutations-1))],
        "null_q50":empirical[int(.5*(permutations-1))],
        "null_q95":empirical[int(.95*(permutations-1))],
        "one_tailed_positive_association_p":(
            1+sum(x>=actual_gain-1e-12 for x in empirical))/(permutations+1),
        "MC_minimum_p":1/(permutations+1),
        "mean_predecessor_label_reassignments_per_shuffle":mean(changed),
        "minimum_predecessor_label_reassignments":min(changed),
        "not_realizable_physical_routes_or_randomized_cognitive_cues":True,
    }


def analyze(episodes,source_qa,original_source_rows,permutations=SHUFFLES,seed=SEED,
            expected_source=True):
    result,prior_scored=evaluate(episodes,source_qa,original_source_rows,
                                 expected_original=SOURCE_POP if expected_source else None)
    if result["status"]!="FITTED_ORIGINAL_CAMBRIDGE_HELDOUT_BEE_CHOICE":
        return {"status":"NO_GO_PREVIOUS_SOURCE_HELDOUT_SUPPORT",
                "original_stage8_report":result}
    edges,first,qa=true_visited_pairs(episodes,original_source_rows)
    bees,excluded=split_bee_source_trips(edges,first)
    if len(bees)!=result["eligible_bees"]:
        raise ValueError("NO_GO_SOURCE_STAGE8_BEE_CONTRACT_CHANGED")
    baseline={ (a["colony"],a["bee"]):fit_probabilities(a["train_pairs"])
               for a in bees}
    source_effect=_signed_effect(bees,baseline)
    source_receipt={
        "stage":"Stage8b_exploratory_conditional_lag",
        "source_doi":"10.17863/CAM.100572",
        "source_original_sha256":ORIGINAL_OBS_SHA256,
        "locked_previous_models":{
            "M0_source_stage8":"α=0.5",
            "M1_source_stage8":"β=10",
            "M2_source_stage8":"γ=10"},
        "original_stage8_status":result["status"],
        "original_stage8_model_reconciliation":{
            "bees":result["eligible_bees"],
            "colonies":result["eligible_independent_colonies"],
            "source_heldout_edges":result["heldout_source_next_flower_orientation_decisions"],
            "M0_to_M1_bee_gain":result["M0_to_M1_bee_equal_gain"],
            "M1_to_M2_bee_gain":result["primary_M1_to_M2_gain_bee_equal"],
        },
        "observed_lag_scores":source_effect,
        "source_original_3_colonies_not_36_independent_colonies":True,
        "source_episode_flower_id_not_actual_physical_location":True,
    }
    if expected_source:
        if (result["eligible_bees"],result["eligible_independent_colonies"],
            result["heldout_source_next_flower_orientation_decisions"])!=FROZEN_TEST:
            raise ValueError("NO_GO_FROZEN_HELDOUT_EDGES_CHANGED")
        if abs(source_effect["M0_to_M1_gain_bee_equal"]-FROZEN_STAGE8_BEE_GAIN)>1e-10:
            raise ValueError("NO_GO_FROZEN_STAGE8_ORIENTATION_GAIN_CHANGED")
        if abs(source_effect["M1_to_M2_gain_bee_equal"]-FROZEN_STAGE8_DRINK_GAIN)>1e-10:
            raise ValueError("NO_GO_FROZEN_STAGE8_DRINK_GAIN_CHANGED")
    supported=eligibility(bees)
    source_receipt["conditional_exchangeability_gate"]=supported
    if supported["primary_gate"]=="PASS":
        source_receipt["orientation_given_original_segment_null"]=_one_null(
            bees,baseline,source_effect,"orientation_and_drink",
            permutations,seed,primary=True)
    else:
        source_receipt["orientation_given_original_segment_null"]={
            "status":supported["primary_gate"]}
    if supported["secondary_gate"]=="PASS":
        source_receipt["drink_given_source_orientation_and_segment_null"]=_one_null(
            bees,baseline,source_effect,"drink_given_orientation",
            permutations,seed,primary=False)
    else:
        source_receipt["drink_given_source_orientation_and_segment_null"]={
            "status":supported["secondary_gate"]}
    source_receipt["status"]="STAGE8B_CONDITIONAL_NULLS_COMPLETED_OR_EXPLICIT_NO_GO"
    return source_receipt


def run(root:Path):
    raw=(root/"Observation_data.csv").read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_OBS_SHA256:
        raise ValueError("NO_GO_STAGE8B_ORIGINAL_CAMBRIDGE_CSV_SHA256_CHANGED")
    original_rows=native_rows(raw)
    episodes,qa=source_episode_audit(original_rows)
    data=analyze(episodes,qa,original_rows)
    root.mkdir(parents=True,exist_ok=True)
    (root/"stage8b_trip_conditioned_lag_null_results.json").write_text(
        json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE8B_LAG_NULL_RESULT "+json.dumps(data,ensure_ascii=False,allow_nan=False),flush=True)
    print("STAGE8B_CONDITIONAL_ANALYSIS_COMPLETE",flush=True)
    return data
