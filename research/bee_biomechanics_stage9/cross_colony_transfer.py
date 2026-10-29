"""Stage 9: leave-one-colony-out transfer of a source bee orientation-history effect.

Target bee's stationary H/V preference (M0) uses its own EARLIER true bouts,
but the transferred orientation adjustment is learned from the TWO OTHER
source colonies' EARLIER bouts only. Never claim fully out-of-colony
predictions of a bee's own baseline, physical spatial movement or memory.

Original 2023 Cambridge Apollo visit-episode source, 36 completed bees and
3 independent colonies; original Time(ms) is duration, Flower ID is episode.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from math import exp,log,log1p
from pathlib import Path
import random
from statistics import mean
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"bee_biomechanics_stage8"))
sys.path.insert(0,str(HERE.parent/"bee_biomechanics_stage8b"))

from episode_audit import ORIGINAL_OBS_SHA256,native_rows,source_episode_audit
from heldout_experience_choice import (
    evaluate,true_visited_pairs,split_bee_source_trips,
    fit_probabilities,score_edges,ALPHA,BETA
)
from within_trip_conditional_lag import (
    permuted_test_edges,eligibility,
    FROZEN_STAGE8_BEE_GAIN,FROZEN_STAGE8_DRINK_GAIN,FROZEN_TEST
)

TREATMENTS=("Control","Low Difference","High Difference")
PREVIOUS=("horizontal","vertical")
MIN_DONOR_CELL=15
PERMUTATIONS=199
SEED=20261029
EPS=1e-12

def logit(x):
    if not 0<x<1:raise ValueError("NO_GO_SOURCE_PROBABILITY_NOT_STRICT")
    return log(x)-log1p(-x)

def invlogit(x):
    if x>=0:return 1.0/(1.0+exp(-x))
    t=exp(x)
    return t/(1+t)

def _source_treatment(bee):
    labels={r["source_treatment"] for r in
            [*bee["train_pairs"],*bee["test_pairs"]]}
    if len(labels)!=1:
        raise ValueError("NO_GO_EXPERIMENTAL_TREATMENT_CHANGED_WITHIN_BEE")
    value=next(iter(labels))
    if value not in TREATMENTS:
        raise ValueError("NO_GO_UNREGISTERED_SOURCE_TREATMENT "+str(value))
    return value

def donor_effects(bee_inputs,heldout_colony,
                  require_coverage=True):
    """Return source-donor-only log-odds adjustments and support ledger."""
    colony_ids={b["colony"] for b in bee_inputs}
    if len(colony_ids)!=3 or heldout_colony not in colony_ids:
        raise ValueError("NO_GO_NOT_THREE_SOURCE_COLONIES")
    donors=[b for b in bee_inputs if b["colony"]!=heldout_colony]
    if len({b["colony"] for b in donors})!=2:
        raise ValueError("NO_GO_NOT_TWO_INDEPENDENT_DONOR_COLONIES")
    pooled=defaultdict(list)
    origin_by_treatment=defaultdict(set)
    for b in donors:
        trt=_source_treatment(b)
        pooled[trt].extend(b["train_pairs"])
        origin_by_treatment[trt].add(b["colony"])
    failures=[]
    effects={}
    audit=[]
    for t in TREATMENTS:
        rows=pooled[t]
        count_all=len(rows)
        count_h=sum(bool(x["next_horizontal"]) for x in rows)
        source_pool_colonies=len(origin_by_treatment[t])
        if source_pool_colonies!=2:
            failures.append(f"{heldout_colony}:{t}: <2 donor colonies")
        if not rows:
            failures.append(f"{heldout_colony}:{t}: no training outcomes")
            continue
        p_all=(count_h+ALPHA)/(count_all+2*ALPHA)
        for o in PREVIOUS:
            group=[x for x in rows if x["previous_orientation"]==o]
            n=len(group)
            h=sum(bool(x["next_horizontal"]) for x in group)
            if n<MIN_DONOR_CELL:
                failures.append(f"{heldout_colony}:{t}:{o}: n={n} <{MIN_DONOR_CELL}")
            p_cond=(h+BETA*p_all)/(n+BETA)
            delta=logit(p_cond)-logit(p_all)
            if not (-100<delta<100):
                raise ValueError("NO_GO_TRANSFERRABLE_DELTA_DIVERGED")
            effects[(t,o)]=delta
            audit.append({
                "heldout_colony":heldout_colony,
                "donor_source_colonies":sorted(origin_by_treatment[t]),
                "treatment":t,"previous_orientation":o,
                "donor_early_pairs_for_treatment":count_all,
                "donor_early_horizontal_next_for_treatment":count_h,
                "donor_early_pairs_in_previous_orientation":n,
                "donor_early_horizontal_next_in_previous_orientation":h,
                "donor_treatment_marginal":p_all,
                "donor_previous_orientation_conditional":p_cond,
                "donor_logit_adjustment":delta
            })
    if require_coverage and failures:
        return None,{"status":"NO_GO_DONOR_TREATMENT_ORIENTATION_COVERAGE",
                     "reasons":failures,"source_cell_receipt":audit}
    if len(effects)!=6 or failures:
        raise ValueError("NO_GO_DONOR_MISSING_ORIENTATION_CELL")
    return effects,{"status":"PASS_DONOR_ONLY_TRAINING_SUPPORT",
                    "source_cell_receipt":audit,
                    "source_eligible_bees_donors":len(donors),
                    "source_donor_colonies":sorted({x["colony"] for x in donors}),
                    "source_target_colony":heldout_colony}

def static_and_transferred_model(bee,donor_delta):
    t=_source_treatment(bee)
    fitted=fit_probabilities(bee["train_pairs"])
    p0=fitted["M0"]
    trans={
        previous:invlogit(logit(p0)+donor_delta[(t,previous)])
        for previous in PREVIOUS
    }
    if not all(EPS<x<1-EPS for x in trans.values()):
        raise ValueError("NO_GO_INVALID_SOURCE_TRANSFER_FORECAST")
    return {"static":p0,"personal_previous":fitted["M1"],
            "cross_colony_transfer":trans,
            "source_treatment":t,
            "source_early_pairs":len(bee["train_pairs"]),
            "source_colony":bee["colony"],
            "donor_only_previous_orientation_delta":{
                previous:donor_delta[(t,previous)] for previous in PREVIOUS}}

def _loss(p,y):
    if not 0<p<1:raise ValueError("NO_GO_ZERO_ONE_FORECAST")
    return -log(p if y else 1-p)

def score_colony_transfer(bees,fitted,mode=None,rng=None):
    """Prediction/score, preserving individual and original source test grain."""
    per_bee=[]
    percol=defaultdict(list)
    nreassigned=0
    for b in bees:
        key=(b["colony"],b["bee"])
        model=fitted[key]
        records=b["test_pairs"]
        if mode is not None:
            records,nchanges=permuted_test_edges(records,rng,mode)
            nreassigned+=nchanges
        accum={"M0":0.,"Mpersonal":0.,"Mtransfer":0.}
        for r in records:
            p=r["previous_orientation"]
            if p not in PREVIOUS:
                raise ValueError("NO_GO_NONORIENTATION_PREDECESSOR")
            y=bool(r["next_horizontal"])
            accum["M0"]+=_loss(model["static"],y)
            accum["Mpersonal"]+=_loss(model["personal_previous"][p],y)
            accum["Mtransfer"]+=_loss(model["cross_colony_transfer"][p],y)
        n=len(records)
        means={k:v/n for k,v in accum.items()}
        row={
            "source_colony":b["colony"],"bee_tag":b["bee"],
            "source_treatment":model["source_treatment"],
            "source_early_trip_count":b["early_fitting_trips"],
            "source_heldout_later_trip_count":b["heldout_later_trips"],
            "source_heldout_true_next_choice_edges":n,
            "mean_heldout_NLL_by_model":means,
            "M0_to_Mtransfer_gain":means["M0"]-means["Mtransfer"],
            "M0_to_Mpersonal_gain":means["M0"]-means["Mpersonal"],
            "Mtransfer_to_Mpersonal_gain":means["Mtransfer"]-means["Mpersonal"]
        }
        per_bee.append(row)
        percol[b["colony"]].append(row)
    bycol=[]
    for colony,items in sorted(percol.items()):
        bycol.append({
            "colony":colony,
            "bee_tags":len(items),
            "heldout_next_choice_edges":sum(x["source_heldout_true_next_choice_edges"] for x in items),
            "M0_to_Mtransfer_mean_bee_gain":mean(x["M0_to_Mtransfer_gain"] for x in items),
            "M0_to_Mpersonal_mean_bee_gain":mean(x["M0_to_Mpersonal_gain"] for x in items),
            "Mtransfer_to_Mpersonal_mean_bee_gain":mean(x["Mtransfer_to_Mpersonal_gain"] for x in items),
            "transfer_bees_with_positive_gain":sum(x["M0_to_Mtransfer_gain"]>0 for x in items),
            "nll_bee_equal_by_model":{
                z:mean(x["mean_heldout_NLL_by_model"][z] for x in items)
                for z in ("M0","Mpersonal","Mtransfer")
            }
        })
    if len(bycol)!=3 or any(x["bee_tags"]!=12 for x in bycol):
        raise ValueError("NO_GO_STAGE9_ORIGINAL_THREE_COLONY_EQUAL_BEE_POPULATION")
    return {
        "source_n_bees":len(per_bee),
        "source_n_independent_colonies":len(bycol),
        "source_next_choice_events":sum(x["source_heldout_true_next_choice_edges"] for x in per_bee),
        "M0_to_Mtransfer_colony_equal_gain":mean(x["M0_to_Mtransfer_mean_bee_gain"] for x in bycol),
        "M0_to_Mtransfer_bee_equal_gain":mean(x["M0_to_Mtransfer_gain"] for x in per_bee),
        "M0_to_Mpersonal_colony_equal_gain":mean(x["M0_to_Mpersonal_mean_bee_gain"] for x in bycol),
        "Mtransfer_to_Mpersonal_colony_equal_gain":mean(x["Mtransfer_to_Mpersonal_mean_bee_gain"] for x in bycol),
        "source_colonies_with_positive_transfer_gain":sum(x["M0_to_Mtransfer_mean_bee_gain"]>0 for x in bycol),
        "source_bees_with_positive_transfer_gain":sum(x["M0_to_Mtransfer_gain"]>0 for x in per_bee),
        "source_bees_with_negative_transfer_gain":sum(x["M0_to_Mtransfer_gain"]<0 for x in per_bee),
        "equal_colony_mean_NLL_by_model":{
            z:mean(x["nll_bee_equal_by_model"][z] for x in bycol)
            for z in ("M0","Mpersonal","Mtransfer")
        },
        "per_colony":bycol,
        "per_bee":per_bee,
        "reassigned_predecessor_state_labels":nreassigned
    }

def _source_null(bees,fitted,observed,shuffle_count=PERMUTATIONS,seed=SEED):
    """Original Stage8b within genuine trip-segment previous-state null."""
    support=eligibility(bees)
    report={"source_admission":support,
            "permutations_fixed_before_source_results":shuffle_count,
            "seed":seed,
            "stage8b_identical_source_segment_definition":True,
            "source_donor_transfer_models_frozen":True,
            "current_and_next_actual_flower_orientations_not_modified":True}
    if support["primary_gate"]!="PASS":
        report["status"]="NO_GO_CONDITIONAL_EXCHANGEABILITY"
        return report
    rng=random.Random(seed)
    null=[]
    per_col=defaultdict(list)
    changed=[]
    for j in range(shuffle_count):
        v=score_colony_transfer(bees,fitted,mode="orientation_and_drink",rng=rng)
        if (v["source_next_choice_events"]!=observed["source_next_choice_events"] or
            abs(v["equal_colony_mean_NLL_by_model"]["M0"]-
                observed["equal_colony_mean_NLL_by_model"]["M0"])>1e-12):
            raise ValueError("NO_GO_SOURCE_TEST_OUTCOME_CHANGED_DURING_NULL")
        null.append(v["M0_to_Mtransfer_colony_equal_gain"])
        changed.append(v["reassigned_predecessor_state_labels"])
        for c in v["per_colony"]:
            per_col[c["colony"]].append(c["M0_to_Mtransfer_mean_bee_gain"])
    actual=observed["M0_to_Mtransfer_colony_equal_gain"]
    ordered=sorted(null)
    report.update({
        "status":"COMPUTED_ORIGINAL_SOURCE_CROSSCOLONY_CONDITIONAL_LAG_NULL",
        "source_original_observed_transfer_gain":actual,
        "null_mean_transfer_gain":mean(null),
        "actual_minus_null_mean_transfer_gain":actual-mean(null),
        "null_min_transfer_gain":min(null),
        "null_max_transfer_gain":max(null),
        "null_q05":ordered[int(.05*(shuffle_count-1))],
        "null_q50":ordered[int(.5*(shuffle_count-1))],
        "null_q95":ordered[int(.95*(shuffle_count-1))],
        "one_sided_positive_tail_conditional_p":(
            1+sum(x>=actual-1e-12 for x in null))/(shuffle_count+1),
        "minimum_possible_p":1/(shuffle_count+1),
        "mean_prev_state_labels_reassigned":mean(changed),
        "source_per_colony_observed_minus_null":[
            {"colony":c["colony"],
             "observed_transfer_gain":c["M0_to_Mtransfer_mean_bee_gain"],
             "null_mean_transfer_gain":mean(per_col[c["colony"]]),
             "actual_minus_null_mean":c["M0_to_Mtransfer_mean_bee_gain"]-mean(per_col[c["colony"]])}
            for c in observed["per_colony"]],
        "source_shuffles_not_independent_experimental_colonies":True
    })
    return report

def analyze(episodes,source_qa,source_actions,
            expected_original=True,permutations=PERMUTATIONS,seed=SEED):
    """Leave each original colony completely out of *other-colony* effect fit."""
    first,_=evaluate(episodes,source_qa,source_actions,
                     expected_original=(61592,38,3) if expected_original else None)
    if first["status"]!="FITTED_ORIGINAL_CAMBRIDGE_HELDOUT_BEE_CHOICE":
        return {"status":"NO_GO_PREVIOUS_SOURCE_EXPERIMENT_SUPPORT",
                "stage8_model":first}
    pairs,first_trip,_=true_visited_pairs(episodes,source_actions)
    bees,ignored=split_bee_source_trips(pairs,first_trip)
    if expected_original:
        if (len(bees),len({b["colony"] for b in bees}),
            sum(len(b["test_pairs"]) for b in bees))!=(36,3,1234):
            raise ValueError("NO_GO_STAGE8_BEE_TRIP_SOURCE_POPULATION_DRIFT")
        if abs(first["M0_to_M1_bee_equal_gain"]-
               FROZEN_STAGE8_BEE_GAIN)>1e-10:
            raise ValueError("NO_GO_STAGE8_PREVIOUS_ORIENTATION_BASELINE_CHANGED")
        if abs(first["primary_M1_to_M2_gain_bee_equal"]-
               FROZEN_STAGE8_DRINK_GAIN)>1e-10:
            raise ValueError("NO_GO_STAGE8_PREVIOUS_DRINK_BASELINE_CHANGED")
    bybee={(b["colony"],b["bee"]):b for b in bees}
    if len(bybee)!=len(bees):
        raise ValueError("NO_GO_BEE_ID_OVERLAP_SOURCE")
    source_treatments=Counter(_source_treatment(b) for b in bees)
    if set(source_treatments)!=set(TREATMENTS):
        raise ValueError("NO_GO_ORIGINAL_TREATMENT_GROUPS_MISSING")
    donor_receipts=[]
    donor={}
    for colony in sorted({b["colony"] for b in bees}):
        effects,admit=donor_effects(bees,colony)
        donor_receipts.append(admit)
        if effects is None:
            return {"status":"NO_GO_DONOR_TREATMENT_ORIENTATION_COVERAGE",
                    "source_treatment_support":dict(source_treatments),
                    "source_fold_admission":donor_receipts}
        donor[colony]=effects
    fit={}
    for b in bees:
        m=static_and_transferred_model(b,donor[b["colony"]])
        fit[(b["colony"],b["bee"])]=m
    observed=score_colony_transfer(bees,fit)
    if expected_original:
        if abs(observed["M0_to_Mpersonal_colony_equal_gain"]-
               FROZEN_STAGE8_BEE_GAIN)>1e-10:
            raise ValueError("NO_GO_PERSONAL_HISTORICAL_BENCHMARK_CHANGED")
        if observed["source_next_choice_events"]!=1234:
            raise ValueError("NO_GO_INVALID_SOURCE_HELDOUT_FORECAST_POPULATION")
    null=_source_null(bees,fit,observed,permutations,seed)
    return {
        "status":"COMPLETED_CROSSCOLONY_BEE_ORIENTATION_TRANSFER",
        "original_article_doi":"10.1016/j.isci.2023.108071",
        "original_dataset_doi":"10.17863/CAM.100572",
        "original_source_csv_sha256":ORIGINAL_OBS_SHA256,
        "original_36_bee_stage8_numerical_reconciliation":{
            "M0_to_Mpersonal_bee_gain":first["M0_to_M1_bee_equal_gain"],
            "M1_to_M2_bee_gain":first["primary_M1_to_M2_gain_bee_equal"],
            "original_heldout_next_orientation_events":first[
                "heldout_source_next_flower_orientation_decisions"]},
        "source_treatment_n_bees":dict(source_treatments),
        "source_donor_support_and_learned_logit_adjustments":donor_receipts,
        "source_actual_heldout_colony_transfer":observed,
        "original_segment_conditional_null":null,
        "frozen_inference_ceiling":"one laboratory source with three colonies, physically unmapped flower IDs, no individual visual cue event times, no causal memory, wind, plant interactions or fitness. Transfer of previous H/V association is distinct from transfer of entire individual behavior."
    }

def run(root):
    original=root/"Observation_data.csv"
    raw=original.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_OBS_SHA256:
        raise ValueError("NO_GO_CAMBRIDGE_ORIGINAL_OBSERVATION_BYTES_CHANGED")
    actions=native_rows(raw)
    episodes,qa=source_episode_audit(actions)
    result=analyze(episodes,qa,actions)
    out=root/"bee_stage9_crosscolony_transfer_results.json"
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("BEE_STAGE9_COLONY_TRANSFER "+json.dumps(result,ensure_ascii=False,allow_nan=False),flush=True)
    print("BEE_STAGE9_COLONY_TRANSFER_COMPLETE",flush=True)
    if result["status"]!="COMPLETED_CROSSCOLONY_BEE_ORIENTATION_TRANSFER":
        raise ValueError("NO_GO_STAGE9_TRANSFER_SOURCE_SUPPORT")
    return result

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="bee_stage9_source")
    args=parser.parse_args()
    result=run(Path(args.out))
    if result["status"]!="COMPLETED_CROSSCOLONY_BEE_ORIENTATION_TRANSFER":
        raise SystemExit(2)
