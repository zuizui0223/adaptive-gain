"""Stage 6: original bee triplet turn direction vs prior-flower history.

Two physically different between-flower steps A->B->C within ONE original
foraging bout. Cosine of publisher Figure 2 endpoint displacement vectors
is a *position geometry proxy*, not measured individual flight heading.

All λ/κ training uses source days 1..4; original day 5 is never fitted.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import itertools
import json
import math
from pathlib import Path
import random
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bee_behavior_stage4"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bee_behavior_stage5"))
from heldout_flower_history import (
    MIN_ELIGIBLE_BEES,MIN_TEST_TRANSITIONS,MIN_TRAIN_VISITS,
    static_probs
)
from bout_transition_analysis import PHYSICAL_FLOWERS
from geo_history_holdout import (
    verify_geometry,geo_probs,geo_history_probs,
    split_bouts,choose_global_lambda,conditional_switch_probability
)

KAPPA_GRID=(0.0,0.25,0.5,1.0,2.0,4.0)
FROZEN_LAMBDA=0.05
SHUFFLES=199
RNG_SEED=20261028
PRIMARY="Mturn_to_Mturn_history"
MODELS=("Mgeo","Mgeo_history","Mturn","Mturn_history")
COORD_PATH=Path(__file__).resolve().parents[1]/"bee_behavior_stage5"/"flower_positions_figure2_verified.json"


def source_triplets(bouts):
    """Count and preserve valid A!=B!=C 3-flower events within true bouts only."""
    events=[]
    source={"bouts":len(bouts),"visits":0,"within_bout_adjacent_pairs":0,
            "within_bout_total_triplets":0,"invalid_first_step_repeat":0,
            "invalid_second_step_repeat":0}
    for bout in bouts:
        seq=bout["flowers"]
        source["visits"]+=len(seq)
        source["within_bout_adjacent_pairs"]+=max(0,len(seq)-1)
        for first,mid,last in zip(seq[:-2],seq[1:-1],seq[2:]):
            source["within_bout_total_triplets"]+=1
            if first==mid:
                source["invalid_first_step_repeat"]+=1
            if mid==last:
                source["invalid_second_step_repeat"]+=1
            if first==mid or mid==last:
                continue
            events.append({"bee":bout["bee"],"day":bout["day"],
                           "bout":bout["bout"],"a":first,"b":mid,"c":last})
    source["eligible_distinct_step_triplets"]=len(events)
    return events,source


def cosine_turn(coords,a,b,c):
    v=(coords[b][0]-coords[a][0],coords[b][1]-coords[a][1])
    w=(coords[c][0]-coords[b][0],coords[c][1]-coords[b][1])
    vlen=math.hypot(*v);wlen=math.hypot(*w)
    if vlen<=0 or wlen<=0:raise ValueError("NO_GO_DIRECTION_UNDEFINED_ZERO_STEP")
    ans=(v[0]*w[0]+v[1]*w[1])/(vlen*wlen)
    if not math.isfinite(ans) or not -1.0000001<=ans<=1.0000001:
        raise ValueError("NO_GO_BAD_TURNING_COSINE")
    return max(-1.0,min(1.0,ans))


def _switched(probs,current):
    denom=1-probs[current]
    if denom<=0 or not math.isfinite(denom):
        raise ValueError("NO_GO_ZERO_NONCURRENT_PROBABILITY")
    result={f:probs[f]/denom for f in PHYSICAL_FLOWERS if f!=current}
    if abs(sum(result.values())-1)>1e-10 or not all(
        math.isfinite(p) and p>0 for p in result.values()
    ):raise ValueError("NO_GO_INVALID_SWITCH_BASE_PROBS")
    return result


def turned(probs,coords,a,b,kappa):
    """Same kappa for Mgeo and Mgeo+history; 9 candidate physical flowers."""
    if kappa not in KAPPA_GRID:
        raise ValueError("unregistered curvature parameter")
    if a==b:raise ValueError("incoming vector undefined")
    w={f:math.log(prob)+kappa*cosine_turn(coords,a,b,f)
       for f,prob in probs.items()}
    if set(w)!=set(PHYSICAL_FLOWERS)-{b}:
        raise ValueError("NO_GO_MISSING_OR_INVENTED_PHYSICAL_DESTINATIONS")
    maximum=max(w.values())
    exps={f:math.exp(v-maximum) for f,v in w.items()}
    total=sum(exps.values())
    return {f:v/total for f,v in exps.items()}


def choose_kappa(training_triplets,training,dist,coords):
    """Select kappa once using training triplets and Mgeo WITHOUT history."""
    if not training_triplets:raise ValueError("NO_GO_NO_TRAINING_TRIPLETS")
    stats={}
    store={}
    for bee,data in training.items():
        if data["early_visits"]:
            store[bee]=static_probs(data["early_visits"],PHYSICAL_FLOWERS)
    for kappa in KAPPA_GRID:
        neg=0.;n=0
        for event in training_triplets:
            bee,a,b,c=event["bee"],event["a"],event["b"],event["c"]
            if bee not in store:
                raise ValueError("NO_GO_TRAINING_TAG_UNAVAILABLE")
            pgeo=geo_probs(store[bee],b,PHYSICAL_FLOWERS,dist,FROZEN_LAMBDA)
            base=_switched(pgeo,b)
            pred=turned(base,coords,a,b,kappa)
            neg-=math.log(pred[c])
            n+=1
        stats[str(kappa)]={"train_triplets":n,
                           "mean_train_conditional_logloss_nats":neg/n}
    chosen=min(KAPPA_GRID,key=lambda x:(
        stats[str(x)]["mean_train_conditional_logloss_nats"],x))
    return chosen,stats


def _mean(values):
    return sum(values)/len(values) if values else None


def _signflip(values):
    if not values or len(values)>16:return None
    observed=abs(_mean(values))
    hits=0
    for signs in itertools.product((-1,1),repeat=len(values)):
        m=abs(_mean([a*b for a,b in zip(signs,values)]))
        if m+1e-12>=observed:hits+=1
    return hits/(2**len(values))


def _predict_for_source_event(event,static,counts,dist,coords,kappa):
    a,b,c=event["a"],event["b"],event["c"]
    geo=geo_probs(static,b,PHYSICAL_FLOWERS,dist,FROZEN_LAMBDA)
    hist=geo_history_probs(b,counts,geo,PHYSICAL_FLOWERS)
    pgeo=_switched(geo,b)
    phist=_switched(hist,b)
    predictions={
        "Mgeo":pgeo[c],
        "Mgeo_history":phist[c],
        "Mturn":turned(pgeo,coords,a,b,kappa)[c],
        "Mturn_history":turned(phist,coords,a,b,kappa)[c]
    }
    if not all(0<v<=1 and math.isfinite(v) for v in predictions.values()):
        raise ValueError("NO_GO_INVALID_MODEL_PROBABILITY")
    return predictions


def fit_direction_models(bouts,coordinates,dist,expected_anchor=(1550,10),
                         expected_lambda=FROZEN_LAMBDA,expected_days=(1,2,3,4,5)):
    final,bee_training=split_bouts(bouts)
    if expected_days is not None and tuple(sorted({r["day"] for r in bouts}))!=tuple(expected_days):
        raise ValueError("NO_GO_WRONG_ORIGINAL_SOURCE_DAYS")
    event_train,train_receipt=source_triplets(
        [r for r in bouts if r["day"]<final])
    event_test,test_receipt=source_triplets(
        [r for r in bouts if r["day"]==final])
    if expected_anchor is not None:
        if (test_receipt["within_bout_adjacent_pairs"],len(bee_training))!=tuple(expected_anchor):
            raise ValueError("NO_GO_STAGE5_ORIGINAL_DAY5_SOURCE_ANCHOR_CHANGED")
    lam,loss=choose_global_lambda(bee_training,dist)
    if expected_lambda is not None and abs(lam-expected_lambda)>1e-10:
        raise ValueError("NO_GO_STAGE5_TRAIN_ONLY_DISTANCE_LAMBDA_CHANGED")
    kappa,kgrid=choose_kappa(event_train,bee_training,dist,coordinates)
    train_static={bee:static_probs(data["early_visits"],PHYSICAL_FLOWERS)
                  for bee,data in bee_training.items() if data["early_visits"]}
    train_counts={bee:data["early_pairs"] for bee,data in bee_training.items()}
    test_grouped=defaultdict(list)
    for record in event_test:test_grouped[record["bee"]].append(record)
    bees=sorted(bee_training)
    result={
        "status":"NO_GO_NOT_FITTED",
        "final_day_heldout":final,
        "physical_geometry_coordinate_count":len(coordinates),
        "source_test_triplets":test_receipt,
        "source_training_triplets":train_receipt,
        "full_original_day5_pairs_expected":1550 if expected_anchor is not None else None,
        "train_only_lambda_candidate_grid":loss,
        "validated_train_only_lambda_per_m":lam,
        "train_only_kappa_candidate_grid":kgrid,
        "selected_train_only_heading_kappa":kappa,
        "target":"9 possible distinct destinations conditional on A!=B and B!=C",
        "model_smoothing":"M0 α=0.5; Mgeo+history β=5 inherited frozen Stage5",
        "no_actual_flight_bearing_observed":True,
        "no_perceptual_cue_order_observed":True,
        "per_bee":[],"no_go_tags":[],
    }
    eligible_records=[]
    for bee in bees:
        source=bee_training[bee]
        tests=test_grouped[bee]
        if len(source["early_visits"])<MIN_TRAIN_VISITS or len(tests)<MIN_TEST_TRANSITIONS:
            result["no_go_tags"].append({
                "tag":bee,"train_visits":len(source["early_visits"]),
                "heldout_eligible_triplets":len(tests)})
            continue
        nll={name:0.0 for name in MODELS}
        cosines=[]
        for e in tests:
            pr=_predict_for_source_event(
                e,train_static[bee],train_counts[bee],dist,coordinates,kappa)
            for name in MODELS:nll[name]-=math.log(pr[name])
            cosines.append(cosine_turn(coordinates,e["a"],e["b"],e["c"]))
        per={
            "tag":bee,"source_earlier_train_visits":len(source["early_visits"]),
            "source_earlier_train_pairs":sum(train_counts[bee].values()),
            "heldout_valid_direction_triplets":len(tests),
            "observed_mean_cosine_two_chord_turn":_mean(cosines),
            "observed_forward_cos_gt0":sum(x>1e-12 for x in cosines),
            "observed_orthogonal_cos_approx0":sum(abs(x)<=1e-12 for x in cosines),
            "observed_reversing_cos_lt0":sum(x<-1e-12 for x in cosines),
            "heldout_models_nll_nats_per_triplet":{
                name:nll[name]/len(tests) for name in MODELS}
        }
        result["per_bee"].append(per)
        eligible_records.extend(tests)
    result["eligible_bee_tags"]=len(result["per_bee"])
    result["eligible_heldout_triplets"]=len(eligible_records)
    if len(result["per_bee"])<MIN_ELIGIBLE_BEES:
        result["status"]="NO_GO_INSUFFICIENT_TAGGED_BEES";return result,None
    def contrast(left,right):
        values=[]
        per={}
        for bee in result["per_bee"]:
            n=bee["heldout_models_nll_nats_per_triplet"]
            v=n[left]-n[right]
            values.append(v);per[bee["tag"]]=v
        return {
            "mean_bee_equal_nll_gain_nats_per_triplet":_mean(values),
            "bee_tags_positive":sum(x>0 for x in values),
            "bee_tags_negative":sum(x<0 for x in values),
            "within_one_colony_signflip_p_descriptive":_signflip(values),
            "per_bee_gains":per}
    result["mean_bee_equal_heldout_nll"]={
        name:_mean([r["heldout_models_nll_nats_per_triplet"][name]
                    for r in result["per_bee"]]) for name in MODELS}
    result["primary_direction_to_direction_plus_history"]=contrast(
        "Mturn","Mturn_history")
    result["secondary_geometry_to_heading"]=contrast("Mgeo","Mturn")
    result["secondary_geometry_history_to_heading_history"]=contrast(
        "Mgeo_history","Mturn_history")
    result["secondary_geometry_to_history_same_triplets"]=contrast(
        "Mgeo","Mgeo_history")
    result["status"]="FITTED_INDIVIDUAL_HELDOUT_DIRECTION_ANALYSIS"
    model_data={
        "eligible_test_events":eligible_records,
        "train_static":train_static,
        "train_counts":train_counts,
        "dist":dist,"coordinates":coordinates,"kappa":kappa,
        "tagged_bees":tuple(x["tag"] for x in result["per_bee"])
    }
    return result,model_data


def incoming_heading_permutation(model_data,n=SHUFFLES,seed=RNG_SEED):
    """Conditional negative control: shuffle incoming A within (bee,current B).

    No outcome values C, beehive history, event occurrence counts or
    current-to-next B->C are permuted. Null is conditional on source graph.
    """
    if n<1:raise ValueError("NO_GO_INVALID_PERMUTATION_COUNT")
    events=model_data["eligible_test_events"]
    by_key=defaultdict(list)
    for i,e in enumerate(events):by_key[(e["bee"],e["b"])].append(i)
    eligible_indices=set()
    for ix in by_key.values():
        if len(ix)>1 and len({events[j]["a"] for j in ix})>1:
            eligible_indices.update(ix)
    tag_support=Counter(events[i]["bee"] for i in eligible_indices)
    receipt={"permutations":n,"seed":seed,"heldout_direction_triplets":len(events),
             "eligible_to_exchange_heading_triplets":len(eligible_indices),
             "eligible_bees_with_5_exchangeable_triplets":
                 sum(v>=5 for v in tag_support.values()),
             "conditioning_key":"(bee_tag, current physical flower B)",
             "preserves":"source actual B,C, bee and all visit/counts and trained estimates",
             "not_a_cue_perception_randomization":True,
             "status":"NO_GO_UNSUPPORTED_PERMUTATION_CELLS"}
    if len(eligible_indices)<100 or receipt["eligible_bees_with_5_exchangeable_triplets"]<5:
        return receipt
    static=model_data["train_static"]
    dist=model_data["dist"];coords=model_data["coordinates"]
    kappa=model_data["kappa"]
    tags=model_data["tagged_bees"]
    nobs=Counter(e["bee"] for e in events)
    geo_logloss={}
    for i,e in enumerate(events):
        b=e["b"];c=e["c"]
        pgeo=geo_probs(static[e["bee"]],b,PHYSICAL_FLOWERS,dist,FROZEN_LAMBDA)
        geo_logloss[i]=-math.log(_switched(pgeo,b)[c])
    baseline={tag:_mean([geo_logloss[i] for i,e in enumerate(events)
                         if e["bee"]==tag]) for tag in tags}
    def test_stat(orientations):
        loss=defaultdict(float)
        for i,e in enumerate(events):
            bee=e["bee"];a=orientations[i];b=e["b"];c=e["c"]
            pgeo=geo_probs(static[bee],b,PHYSICAL_FLOWERS,dist,FROZEN_LAMBDA)
            pturn=turned(_switched(pgeo,b),coords,a,b,kappa)
            loss[bee]-=math.log(pturn[c])
        return _mean([baseline[bee]-loss[bee]/nobs[bee] for bee in tags])
    actual=[e["a"] for e in events]
    observed=test_stat(actual)
    rng=random.Random(seed)
    null=[]
    changed=[]
    for iteration in range(n):
        incoming=list(actual)
        for ix in by_key.values():
            vals=[incoming[j] for j in ix]
            rng.shuffle(vals)
            for j,alt in zip(ix,vals):incoming[j]=alt
        null.append(test_stat(incoming))
        changed.append(sum(a!=b for a,b in zip(actual,incoming)))
    sorted_null=sorted(null)
    receipt.update({
        "status":"COMPUTED_DIRECTION_SHUFFLE_NULL",
        "actual_Mgeo_to_Mturn_mean_bee_gain_nats":observed,
        "shuffled_null_mean_gain_nats":_mean(null),
        "shuffled_null_min_gain_nats":min(null),
        "shuffled_null_max_gain_nats":max(null),
        "shuffled_null_q05":sorted_null[math.floor(.05*(len(null)-1))],
        "shuffled_null_q95":sorted_null[math.floor(.95*(len(null)-1))],
        "observed_minus_shuffled_mean_gain_nats":observed-_mean(null),
        "one_tailed_p_positive_direction_alignment":(
            1+sum(x>=observed-1e-12 for x in null))/(n+1),
        "mean_reassigned_incoming_label_count_per_shuffle":_mean(changed),
        "min_reassigned_incoming_label_count_per_shuffle":min(changed),
        "maximum_p_resolution":1/(n+1)})
    return receipt
