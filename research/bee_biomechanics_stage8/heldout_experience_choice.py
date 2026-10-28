"""Stage 8 original Cambridge 3-colony bee visit outcome-history forecast.

Observed outcome is NEXT TOUCHED flower ORIENTATION, not physical location,
next drink amount, wind, individual flight direction or visual cue acquisition.

M0: each bee's early-trip static next-horizontal preference, α=.5.
M1: previous visited orientation, β=10 smoothing toward M0.
M2: previous visited orientation + whether any previous *Drink action,
    γ=10 smoothing toward M1. Training is strictly earlier 70% of
    recorded Micro-rough test foraging trips, heldout remaining trips.
No sorting by action Time(ms): that is per-action duration, not event stamp.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from math import ceil,log,isfinite
from pathlib import Path
import argparse
import hashlib
import json
import random

from episode_audit import (
    native_rows,source_episode_audit,ORIGINAL_OBS_SHA256,
    ORIGINAL_MASS_SHA256,EXPECTED_SOURCE_OBSERVATION_ROWS
)

ALPHA=0.5
BETA=10.0
GAMMA=10.0
TRAIN_FRACTION=0.70
SURFACE="Micro-rough"
NO_GO_INCOMPLETE_BEES={"Yellow 4","Green 47"}
MIN_TRAIN_PAIRS=10
MIN_TEST_PAIRS=5
MIN_BEES=10
MIN_COLONIES=3
MIN_TOTAL_TEST=100
MIN_VERTICAL_HOVER_TEST=100
SHUFFLES=199
RNG_SEED=20261028

def true_visited_pairs(episodes,original_rows):
    """Adjacent episode pairs within same bee, original trip and test surface.

    A recorded nest exit or flight-arena rest between flower visits is an
    interruption; skip these rather than fabricate immediate next handling.
    No between-trip/event-phase transitions or physical flower locations.
    """
    visits=defaultdict(list)
    skip=Counter()
    # Source order strictly original input index, because Time(ms) is not
    # a timestamp and 'Flower ID' is NOT a persistent place identity.
    for e in episodes:
        if e["surface"]!=SURFACE:continue
        if e["orientation"] not in ("horizontal","vertical"):
            skip["ambiguous_source_visit_orientation"]+=1
            continue
        k=(e["colony"],e["bee"])
        visits[k].append(e)
    edges=defaultdict(list)
    all_trip_first={}
    numtrips=Counter()
    for key,group in visits.items():
        group.sort(key=lambda e:e["source_first_row"])
        prev=None
        seen_trips=set()
        for e in group:
            trip=e["trip"]
            if not trip or trip in ("NA","N/A","#N/A","nan"):
                skip["invalid_source_bout"]+=1
                prev=None
                continue
            tk=(key[0],key[1],trip)
            all_trip_first[tk]=min(e["source_first_row"],all_trip_first.get(tk,e["source_first_row"]))
            seen_trips.add(trip)
            if prev is None:
                prev=e;continue
            if prev["trip"]!=trip or prev["surface"]!=e["surface"]:
                skip["between_bout_or_surface"]+=1
                prev=e;continue
            if prev["source_last_row"]>=e["source_first_row"]:
                raise ValueError("NO_GO_CAMBRIDGE_NONMONOTONIC_SOURCE_VISITS")
            # Protect chronology if source rows of a different bee are
            # interleaved; only original focal-bee interruptions matter.
            gap=original_rows[prev["source_last_row"]+1:e["source_first_row"]]
            interrupted=any(
                x["Bee"]==key[1] and x["Colony"]==key[0] and
                x["Observation"] in ("rest","boutStartStop")
                for x in gap)
            if interrupted:
                skip["genuine_rest_or_bout_marker_in_between"]+=1
                prev=e;continue
            edges[key].append({
                "colony":key[0],"bee":key[1],"trip":trip,
                "previous_orientation":prev["orientation"],
                "previous_recorded_drink":bool(prev["drank"]),
                "previous_recorded_hover":bool(prev["hover_observed"]),
                "next_horizontal":e["orientation"]=="horizontal",
                "source_prev_first":prev["source_first_row"],
                "source_next_first":e["source_first_row"],
                "previous_episode_order_gap":e["source_first_row"]-prev["source_last_row"],
                "source_treatment":e["treatment"],
                "not_individual_perceived_flower_options":True
            })
            prev=e
        numtrips[key]=len(seen_trips)
    return edges,all_trip_first,{
        "source_test_surface":SURFACE,
        "source_test_surface_visit_episode_count":sum(len(x) for x in visits.values()),
        "bee_keys_with_test_phase_visits":len(visits),
        "source_test_trip_count":sum(numtrips.values()),
        "source_adjacent_candidate_true_pairs":sum(len(v) for v in edges.values()),
        "source_true_pair_exclusions":dict(skip),
        "source_order_not_sorted_by_action_duration":True,
        "flower_ID_is_per_episode_not_physical_location":True
    }

def split_bee_source_trips(edges,trip_first):
    """Freeze by first source row of each original micro-rough trip, per bee."""
    populations=[]
    perbee=[]
    excluded=[]
    for (colony,bee),all_edges in sorted(edges.items()):
        if bee in NO_GO_INCOMPLETE_BEES:
            excluded.append({"bee":bee,"colony":colony,"reason":"source_author_incomplete_test_bee"})
            continue
        dates=[(row,trip) for (c,b,trip),row in trip_first.items()
               if (c,b)==(colony,bee)]
        ordered=sorted(dates,key=lambda z:(z[0],z[1]))
        if len({t for _,t in ordered})!=len(ordered):
            raise ValueError("NO_GO_DUPLICATED_SOURCE_TRIP_SEQUENCE")
        if len(ordered)<2:
            excluded.append({"bee":bee,"colony":colony,"reason":"fewer_than_two_test_trips"})
            continue
        ntrain=max(1,min(len(ordered)-1,ceil(TRAIN_FRACTION*len(ordered))))
        first={trip for _,trip in ordered[:ntrain]}
        later={trip for _,trip in ordered[ntrain:]}
        train=[x for x in all_edges if x["trip"] in first]
        test=[x for x in all_edges if x["trip"] in later]
        if len(train)<MIN_TRAIN_PAIRS or len(test)<MIN_TEST_PAIRS:
            excluded.append({"bee":bee,"colony":colony,
                             "reason":"insufficient_earlier_or_heldout_pairs",
                             "source_trips":len(ordered),
                             "train_pairs":len(train),"heldout_pairs":len(test)})
            continue
        if set(x["trip"] for x in train) & set(x["trip"] for x in test):
            raise ValueError("NO_GO_TEST_BOUT_LEAKAGE")
        perbee.append({"colony":colony,"bee":bee,
                       "micro_rough_actual_trips":len(ordered),
                       "early_fitting_trips":len(first),
                       "heldout_later_trips":len(later),
                       "train_pairs":train,"test_pairs":test})
    return perbee,excluded

def fit_probabilities(training):
    """All model probabilities positive: M2 nested toward M1 toward M0."""
    n=len(training);total=sum(int(t["next_horizontal"]) for t in training)
    p0=(total+ALPHA)/(n+2*ALPHA)
    by_prev=defaultdict(lambda:[0,0])
    by_prev_drink=defaultdict(lambda:[0,0])
    for r in training:
        s=int(r["next_horizontal"])
        key=r["previous_orientation"]
        by_prev[key][0]+=1
        by_prev[key][1]+=s
        kd=(key,int(r["previous_recorded_drink"]))
        by_prev_drink[kd][0]+=1
        by_prev_drink[kd][1]+=s
    m1={}
    for k in ("horizontal","vertical"):
        nn,yy=by_prev[k]
        m1[k]=(yy+BETA*p0)/(nn+BETA)
    m2={}
    for k in ("horizontal","vertical"):
        for drank in (0,1):
            nn,yy=by_prev_drink[(k,drank)]
            m2[(k,drank)]=(yy+GAMMA*m1[k])/(nn+GAMMA)
    if not all(0<p<1 for p in [p0,*m1.values(),*m2.values()]):
        raise ValueError("NO_GO_ZERO_OR_ONE_FORECAST_PROBABILITY")
    return {"M0":p0,"M1":m1,"M2":m2,
            "train_edges":n,
            "train_prev_orientation_counts":{
                k:by_prev[k][0] for k in ("horizontal","vertical")},
            "train_prev_orientation_drink_counts":{
                f"{k}_{drank}":by_prev_drink[(k,drank)][0]
                for k in ("horizontal","vertical") for drank in (0,1)}}

def _logloss(p,y):
    if not 0<p<1:raise ValueError("NO_GO_LOGLOSS_OUTSIDE_OPEN_PROBABILITY")
    return -log(p if y else (1-p))

def score_edges(test,fit):
    s={"M0":0.,"M1":0.,"M2":0.}
    per=[]
    for edge in test:
        key=edge["previous_orientation"]
        drank=int(edge["previous_recorded_drink"])
        y=bool(edge["next_horizontal"])
        prob={"M0":fit["M0"],"M1":fit["M1"][key],
              "M2":fit["M2"][(key,drank)]}
        losses={name:_logloss(p,y) for name,p in prob.items()}
        for k,v in losses.items():s[k]+=v
        per.append({"previous_orientation":key,"previous_recorded_drink":drank,
                    "previous_recorded_hover":bool(edge["previous_recorded_hover"]),
                    "next_horizontal":y,"trip":edge["trip"],
                    "loss_by_model":losses})
    return {k:v/len(test) for k,v in s.items()},per

def evaluate(events,source_qa,original_source_rows=None,expected_original=(61592,38,3)):
    if expected_original is not None:
        if (source_qa["original_action_rows"],source_qa["original_source_bee_keys"],
            source_qa["original_colonies"])!=tuple(expected_original):
            raise ValueError("NO_GO_ORIGINAL_CAMBRIDGE_POPULATION_CHANGED")
    pairs,trip_first,source_pair= true_visited_pairs(events,original_source_rows)
    bees,excluded=split_bee_source_trips(pairs,trip_first)
    report={
        "status":"SOURCE_QUALITY_READY_MODEL_NO_GO",
        "source_authored_input":"Cambridge Apollo DOI 10.17863/CAM.100572",
        "source_figure":"No actual physical flower position or flow trajectory present",
        "source_first_test_surface":SURFACE,
        "source_own_exclusion_bees":sorted(NO_GO_INCOMPLETE_BEES),
        "source_visit_qa":source_qa,
        "source_pair_qa":source_pair,
        "source_heldout_eligibility_exclusions":excluded,
        "models":"M0 static bee next orientation α=.5; M1 previous orientation β=10; M2 previous orientation and actual recorded drink action γ=10",
        "holdout":"earliest ceil(70% of physical source Micro-rough foraging trips) to fit, entire later trips to score; never create cross-bout transitions",
        "no_physical_flower_spatial_id":True,
        "source_previous_drink_is_observed_proboscis_action_not_realized_nectar_volume":True,
        "all_actual_actions_are_one_of_original_nine_labels":True,
        "per_bee":[],
    }
    n_bees=len(bees);colony_count=len({x["colony"] for x in bees})
    n_test=sum(len(x["test_pairs"]) for x in bees)
    report["eligible_bees"]=n_bees
    report["eligible_independent_colonies"]=colony_count
    report["heldout_source_next_flower_orientation_decisions"]=n_test
    if n_bees<MIN_BEES or colony_count<MIN_COLONIES or n_test<MIN_TOTAL_TEST:
        report["status"]="NO_GO_LATER_TRIP_OR_COLONY_SUPPORT"
        return report,None
    group_results=[]
    scored_by_bee=[]
    training_models={}
    for bee in bees:
        fit=fit_probabilities(bee["train_pairs"])
        mean_losses,events_scored=score_edges(bee["test_pairs"],fit)
        r={
            "bee":bee["bee"],"colony":bee["colony"],
            "source_early_train_trips":bee["early_fitting_trips"],
            "source_later_test_trips":bee["heldout_later_trips"],
            "source_train_pairs":len(bee["train_pairs"]),
            "source_holdout_pairs":len(bee["test_pairs"]),
            "heldout_next_horizontal_fraction":sum(
                int(x["next_horizontal"]) for x in bee["test_pairs"])/len(bee["test_pairs"]),
            "trained_prev_egg_proportions_by_source_outcome":fit["train_prev_orientation_drink_counts"],
            "mean_nll_nats_by_model":mean_losses,
            "M0_to_M1_gain":mean_losses["M0"]-mean_losses["M1"],
            "M1_to_M2_primary_gain":mean_losses["M1"]-mean_losses["M2"],
        }
        group_results.append(r)
        scored_by_bee.append((bee,fit,events_scored))
        training_models[(bee["colony"],bee["bee"])]=fit
    bycolony=defaultdict(list)
    for p in group_results:bycolony[p["colony"]].append(p)
    colony_results=[
        {"colony":c,"bees":len(xs),
         "primary_bee_equal_gain_mean":sum(x["M1_to_M2_primary_gain"] for x in xs)/len(xs),
         "primary_bees_positive":sum(x["M1_to_M2_primary_gain"]>0 for x in xs),
         "baseline_M0_to_M1_bee_equal_mean":sum(x["M0_to_M1_gain"] for x in xs)/len(xs)}
        for c,xs in sorted(bycolony.items())
    ]
    mean_primary=sum(c["primary_bee_equal_gain_mean"] for c in colony_results)/len(colony_results)
    primary_bee_equal=sum(x["M1_to_M2_primary_gain"] for x in group_results)/n_bees
    total_obs=sum(x["source_holdout_pairs"] for x in group_results)
    test_vertical_hover=[
        {"bee":x["bee"],"colony":x["colony"],
         "n_vertical_hover":sum(
            e["previous_orientation"]=="vertical" and e["previous_recorded_hover"]
            for e in bee["test_pairs"])}
        for x,bee in zip(group_results,bees)
    ]
    report["per_bee"]=group_results
    report["colonies"]=colony_results
    report["primary_M1_to_M2_gain_bee_equal"]=primary_bee_equal
    report["primary_M1_to_M2_gain_colony_equal"]=mean_primary
    report["primary_bees_with_gain_positive"]=sum(x["M1_to_M2_primary_gain"]>0 for x in group_results)
    report["primary_bees_with_gain_negative"]=sum(x["M1_to_M2_primary_gain"]<0 for x in group_results)
    report["primary_colonies_with_gain_positive"]=sum(x["primary_bee_equal_gain_mean"]>0 for x in colony_results)
    report["M0_to_M1_bee_equal_gain"]=sum(x["M0_to_M1_gain"] for x in group_results)/n_bees
    report["M0_to_M1_colony_equal_gain"]=sum(x["baseline_M0_to_M1_bee_equal_mean"] for x in colony_results)/len(colony_results)
    report["mean_bee_equal_nll"]={
        key:sum(x["mean_nll_nats_by_model"][key] for x in group_results)/n_bees
        for key in ("M0","M1","M2")}
    report["source_test_episodes_prev_vertical_hover_support"]={
        "total_triplet_eligible_events":sum(x["n_vertical_hover"] for x in test_vertical_hover),
        "bees_with_at_least_5_vertical_hover_events":sum(x["n_vertical_hover"]>=5 for x in test_vertical_hover),
        "by_bee":test_vertical_hover}
    eligible_hover=[(a,b,c) for a,b,c in scored_by_bee
                    if sum(e["previous_orientation"]=="vertical" and e["previous_recorded_hover"]
                           for e in a["test_pairs"])>=5]
    if (len(eligible_hover)>=MIN_BEES and
        sum(1 for a,b,c in eligible_hover for e in a["test_pairs"]
            if e["previous_orientation"]=="vertical" and e["previous_recorded_hover"])>=MIN_VERTICAL_HOVER_TEST):
        support=[]
        for bee,fit,events_scored in eligible_hover:
            subset=[x for x in events_scored
                    if x["previous_orientation"]=="vertical" and x["previous_recorded_hover"]]
            gain=sum(e["loss_by_model"]["M1"]-e["loss_by_model"]["M2"] for e in subset)/len(subset)
            support.append({"bee":bee["bee"],"colony":bee["colony"],
                            "events":len(subset),"gain":gain})
        report["vertical_hover_drink_observation_sensitivity"]={
            "status":"FITTED_DESCRIPTIVE",
            "eligible_bees":len(support),
            "source_test_edges":sum(x["events"] for x in support),
            "mean_bee_equal_gain":sum(x["gain"] for x in support)/len(support),
            "per_bee":support}
    else:
        report["vertical_hover_drink_observation_sensitivity"]={
            "status":"NO_GO_INSUFFICIENT_MATCHED_VERTICAL_HOVER_SUPPORT"}
    report["status"]="FITTED_ORIGINAL_CAMBRIDGE_HELDOUT_BEE_CHOICE"
    return report,scored_by_bee

def run(root):
    raw=(root/"Observation_data.csv").read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_OBS_SHA256:
        raise ValueError("NO_GO_STAGE8_PINNED_PUBLISHER_SOURCE_CHANGED")
    rows=native_rows(raw)
    from episode_audit import source_episode_audit
    episodes,qa=source_episode_audit(rows)
    result,training=evaluate(episodes,qa,rows)
    (root/"bee_stage8_heldout_experience_choice.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE8_HELDOUT_EXPERIENCE_CHOICE "+
          json.dumps(result,ensure_ascii=False,allow_nan=False),flush=True)
    print("STAGE8_HELDOUT_EXPERIENCE_COMPLETE",flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage8_source")
    args=p.parse_args()
    run(Path(args.out))
