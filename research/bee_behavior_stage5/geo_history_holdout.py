"""Stage 5 bee-specific held-out route prediction accounting for verified flower geometry.

Physical positions: 10 labeled flowers, original Pasquaretta et al. 2019
Figure 2 (x,y metres). Original source bytes/positions checked before
using any animal visits. Single colony, observational.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import itertools
import json
import math
from pathlib import Path

from heldout_flower_history import ALPHA,BETA,MIN_TRAIN_VISITS,MIN_TEST_TRANSITIONS,MIN_ELIGIBLE_BEES
from heldout_flower_history import static_probs,transition_probs
from bout_transition_analysis import PHYSICAL_FLOWERS

LAMBDA_CANDIDATES=(0.0,0.025,0.05,0.1,0.2,0.4,0.8)
POSITION_PDF_SHA="7f275a219fe0128d30f70cf6d812ab41d4b64727a740102549e8362b83d4ff8b"
VISUAL_ESTIMATE_M=9.6
MODES=("M0_static","Mgeo_distance","M1_previous","Mgeo_plus_history")
PRIMARY_METRIC="switch_conditioned_nll"
PRIMARY_CONTRAST=("Mgeo_distance","Mgeo_plus_history")

def verify_geometry(path:Path):
    r=json.loads(path.read_text())
    if r.get("original_figure_pdf_sha256")!=POSITION_PDF_SHA:
        raise ValueError("NO_GO_FIG2_SHA_MISMATCH")
    if r.get("source_doi")!="10.1186/s40462-019-0150-z":
        raise ValueError("NO_GO_UNVERIFIED_SOURCE_DOI")
    if r.get("position_units")!="metres":
        raise ValueError("NO_GO_COORDINATE_UNITS")
    got=r.get("coordinates",{})
    if set(got)!=set(PHYSICAL_FLOWERS):
        raise ValueError("NO_GO_UNVERIFIED_PHYSICAL_FLOWER_IDS")
    coords={}
    for fid,v in got.items():
        if not isinstance(v,list) or len(v)!=2:
            raise ValueError("NO_GO_BAD_PHYSICAL_COORDINATE")
        x,y=map(float,v)
        if not (math.isfinite(x) and math.isfinite(y) and
                0<=x<=20 and 0<=y<=44):
            raise ValueError("NO_GO_FIGURE_COORDINATE_OUTSIDE_CAGE")
        coords[fid]=(x,y)
    if len(set(coords.values()))!=10:
        raise ValueError("NO_GO_DUPLICATE_PHYSICAL_POINTS")
    dist={(a,b):math.dist(coords[a],coords[b])
          for a in PHYSICAL_FLOWERS for b in PHYSICAL_FLOWERS}
    if abs(dist["1","4"]-9.0)>.2 or abs(dist["1","6"]-15.8)>.2:
        raise ValueError("NO_GO_FIGURE_DISTANCE_CONTRADICTS_ARTICLE")
    if max(dist.values())<=15:
        raise ValueError("NO_GO_PHYSICAL_ARRAY_UNIMPLAUSIBLY_SMALL")
    return dist,{
        "status":"ORIGINAL_PUBLISHER_FIG2_EXACT_LABELS_AUDITED",
        "original_figure_pdf_url":r["original_figure_pdf_url"],
        "original_figure_sha256":r["original_figure_pdf_sha256"],
        "ten_original_coordinate_labels":r["coordinates"],
        "example_F1_F4_m":dist["1","4"],
        "example_F1_F6_m":dist["1","6"],
        "source_reported_F1_F4_nearest_m":9.0,
        "source_reported_F1_F6_second_m":15.8,
        "source_estimated_visibility_m":VISUAL_ESTIMATE_M,
        "adjacent_options_by_origin":{
            a:sum(0<dist[a,b]<=VISUAL_ESTIMATE_M for b in PHYSICAL_FLOWERS)
            for a in PHYSICAL_FLOWERS},
        "not_measured_visual_detection_or_flight_path":True,
    }

def geo_probs(static,origin,flowers,dist,lam):
    if lam not in LAMBDA_CANDIDATES:
        raise ValueError("unregistered spatial decay parameter")
    logits=[math.log(static[f])-lam*dist[origin,f] for f in flowers]
    maxv=max(logits)
    exps=[math.exp(v-maxv) for v in logits]
    mass=sum(exps)
    p={f:q/mass for f,q in zip(flowers,exps)}
    if not all(math.isfinite(v) and v>0 for v in p.values()):
        raise ValueError("NO_GO_NONPOSITIVE_GEO_PROBABILITY")
    return p

def geo_history_probs(origin,transitions,spatial_prior,flowers):
    n=sum(transitions.get((origin,f),0) for f in flowers)
    p={f:(transitions.get((origin,f),0)+BETA*spatial_prior[f])/(n+BETA)
       for f in flowers}
    if abs(sum(p.values())-1)>1e-10:
        raise ValueError("NO_GO_UNNORMALIZED_HISTORY")
    return p

def split_bouts(bouts):
    days=sorted({x["day"] for x in bouts})
    if len(days)<2:
        raise ValueError("NO_GO_BEFORE_AFTER_DAYS")
    final_day=days[-1]
    members=sorted({x["bee"] for x in bouts})
    per_bee={}
    for bee in members:
        rows=sorted(
            (x for x in bouts if x["bee"]==bee),
            key=lambda x:(x["day"],x["start_time_seconds"],x["bout"]))
        early=[x for x in rows if x["day"]<final_day]
        heldout=[x for x in rows if x["day"]==final_day]
        trainvisits=[f for b in early for f in b["flowers"]]
        trainpairs=Counter(
            (a,b) for bout in early
            for a,b in zip(bout["flowers"][:-1],bout["flowers"][1:]))
        testpairs=[(a,b) for bout in heldout
                   for a,b in zip(bout["flowers"][:-1],bout["flowers"][1:])]
        per_bee[bee]=dict(early_visits=trainvisits,early_pairs=trainpairs,
                          test_pairs=testpairs,train_bouts=len(early),
                          test_bouts=len(heldout))
    return final_day,per_bee

def choose_global_lambda(per_bee,dist,flowers=PHYSICAL_FLOWERS):
    """One predeclared global lambda chosen on earlier-day *training* pairs."""
    raw_counts={bee:Counter(g["early_visits"])
                for bee,g in per_bee.items()}
    train_dist={bee:static_probs(g["early_visits"],flowers)
                for bee,g in per_bee.items() if g["early_visits"]}
    audit={}
    for lam in LAMBDA_CANDIDATES:
        total_loss=0.0
        ntotal=0
        for bee,g in per_bee.items():
            if bee not in train_dist:continue
            static=train_dist[bee]
            for (origin,nextflower),count in g["early_pairs"].items():
                p=geo_probs(static,origin,flowers,dist,lam)[nextflower]
                total_loss-=count*math.log(p)
                ntotal+=count
        if not ntotal:raise ValueError("NO_GO_MISSING_TRAIN_TRANSITIONS")
        audit[str(lam)]={
            "mean_train_loss_nats_per_transition":total_loss/ntotal,
            "train_transitions":ntotal}
    chosen=min(LAMBDA_CANDIDATES,key=lambda x:(
        audit[str(x)]["mean_train_loss_nats_per_transition"],x))
    return chosen,audit

def conditional_switch_probability(p,origin,dest):
    if dest==origin:raise ValueError("conditioned choice requires actual move")
    rem=1-p[origin]
    if rem<=0 or not math.isfinite(rem):
        raise ValueError("NO_GO_SWITCH_RENORMALIZATION")
    value=p[dest]/rem
    if value<=0 or value>1+1e-10:raise ValueError("invalid switch probability")
    return value

def _signflip(values):
    if len(values)>16:return None
    observed=abs(sum(values)/len(values))
    count=0
    for signs in itertools.product([-1,1],repeat=len(values)):
        v=abs(sum(a*b for a,b in zip(signs,values))/len(values))
        if v+1e-12>=observed:count+=1
    return count/(2**len(values))

def analyze_geo(bouts,dist,geo_audit):
    cutoff,per_bee=split_bouts(bouts)
    lam,training_grid=choose_global_lambda(per_bee,dist)
    perbee=[]
    exclusions=[]
    source_total=0
    source_self=0
    all_distances=[]
    for bee,g in per_bee.items():
        train=g["early_visits"]
        tp=g["early_pairs"]
        pairs=g["test_pairs"]
        if len(train)<MIN_TRAIN_VISITS or len(pairs)<MIN_TEST_TRANSITIONS:
            exclusions.append({"tag":bee,"reason":"prior frozen bee support",
                               "train_visits":len(train),"test_pairs":len(pairs)})
            continue
        m0=static_probs(train,PHYSICAL_FLOWERS)
        score={model:{"full_nll":0.0,"switch_nll":0.0,
                      "binary_repeat_nll":0.0} for model in MODES}
        nself=0
        nswitch=0
        measured_distances=[]
        for prev,nxt in pairs:
            if prev not in PHYSICAL_FLOWERS or nxt not in PHYSICAL_FLOWERS:
                raise ValueError("NO_GO_OUTSIDE_PHYSICAL_ARRAY")
            pgeo=geo_probs(m0,prev,PHYSICAL_FLOWERS,dist,lam)
            p1=transition_probs(prev,tp,m0,PHYSICAL_FLOWERS)
            phist=geo_history_probs(prev,tp,pgeo,PHYSICAL_FLOWERS)
            pp={"M0_static":m0,"Mgeo_distance":pgeo,
                "M1_previous":p1,"Mgeo_plus_history":phist}
            same=prev==nxt
            nself+=int(same)
            nswitch+=int(not same)
            measured_distances.append(dist[prev,nxt])
            for name,probs in pp.items():
                if not math.isclose(sum(probs.values()),1,abs_tol=1e-10):
                    raise ValueError("NO_GO_PREDICTION_NOT_NORMALIZED")
                chosen_prob=probs[nxt]
                if chosen_prob<=0:
                    raise ValueError("NO_GO_PREDICTION_ZERO")
                score[name]["full_nll"]-=math.log(chosen_prob)
                prob_repeat=probs[prev] if same else 1-probs[prev]
                if prob_repeat<=0:
                    raise ValueError("NO_GO_SELF_REPEAT_PREDICTION_ZERO")
                score[name]["binary_repeat_nll"]-=math.log(prob_repeat)
                if not same:
                    score[name]["switch_nll"]-=math.log(
                        conditional_switch_probability(probs,prev,nxt))
        per_model={}
        for name,totals in score.items():
            per_model[name]={
                "full_nll":totals["full_nll"]/len(pairs),
                "binary_repeat_nll":totals["binary_repeat_nll"]/len(pairs),
                "switch_conditional_nll":(
                    totals["switch_nll"]/nswitch if nswitch else None)}
        perbee.append({
            "tag":bee,"training_visits":len(train),
            "training_within_bout_pairs":sum(tp.values()),
            "heldout_within_bout_pairs":len(pairs),
            "heldout_self_repeat_pairs":nself,
            "heldout_distinct_flower_pairs":nswitch,
            "heldout_switch_fraction":nswitch/len(pairs),
            "mean_distance_between_distinct_flowers_m":(
                sum(d for d,(a,b) in zip(measured_distances,pairs) if a!=b)/nswitch
                if nswitch else None),
            "between_flower_pair_within_approx_visible_radius":sum(
                d<=VISUAL_ESTIMATE_M+1e-10 and a!=b
                for d,(a,b) in zip(measured_distances,pairs)),
            "within_bee_models":per_model
        })
        source_total+=len(pairs)
        source_self+=nself
        all_distances.extend(measured_distances)
    supported=[p for p in perbee if p["heldout_distinct_flower_pairs"]>=5]
    report={
        "status":"NOT_FITTED",
        "original_figure_meter_geometry":geo_audit,
        "original_source_last_day_heldout":cutoff,
        "time_policy":"fit days<last day only, test last day, previous observed flower known before its next flower",
        "train_only_lambda_grid":training_grid,
        "selected_lambda_per_m":lam,
        "physical_flower_candidates":list(PHYSICAL_FLOWERS),
        "models":list(MODES),
        "primary_metric":"mean per bee switch-conditional nll, previous target excluded from nine alternative destinations by renormalization",
        "primary_contrast":"Mgeo_distance minus Mgeo_plus_history on switch-only",
        "heldout_pairs":source_total,
        "heldout_self_repeat_pairs":source_self,
        "heldout_between_flower_pairs":source_total-source_self,
        "self_repeat_fraction":source_self/source_total if source_total else None,
        "heldout_transitions_nonself_within_source_visibility_distance":sum(
            p["between_flower_pair_within_approx_visible_radius"] for p in perbee),
        "per_bee":perbee,"excluded_bee_tags":exclusions,
        "primary_qualifying_bee_tags":len(supported),
        "narrative_firewall":"One colony and one static geometric 10-flower array; no measured flight trajectories, sensory query ordering or fitness"
    }
    if source_total!=1550 or len(perbee)!=10:
        report["status"]="NO_GO_SOURCE_STAGE4_POPULATION_DISAGREEMENT"
        return report
    if len(supported)<MIN_ELIGIBLE_BEES:
        report["status"]="NO_GO_INSUFFICIENT_SWITCH_TRANSITIONS"
        return report
    def summarize_contrast(left,right,field,items):
        comparisons=[
            bee["within_bee_models"][left][field]-
            bee["within_bee_models"][right][field]
            for bee in items]
        if not all(math.isfinite(x) for x in comparisons):
            raise ValueError("NO_GO_NONFINITE_GEOMETRY_CONTRAST")
        return {
            "mean_bee_equal_gain_nats":sum(comparisons)/len(comparisons),
            "bee_gain_positive":sum(x>0 for x in comparisons),
            "bee_gain_negative":sum(x<0 for x in comparisons),
            "within_one_colony_signflip_p_descriptive":_signflip(comparisons),
            "per_bee_gains_nats":{bee["tag"]:v for bee,v in zip(items,comparisons)}
        }
    report["all_transition_model_mean_bee_equal_nll"]={
        model:sum(p["within_bee_models"][model]["full_nll"] for p in perbee)/len(perbee)
        for model in MODES
    }
    report["switch_transition_model_mean_bee_equal_nll"]={
        model:sum(p["within_bee_models"][model]["switch_conditional_nll"]
                   for p in supported)/len(supported)
        for model in MODES
    }
    report["switch_primary_geo_to_geo_history_gain"]=summarize_contrast(
        "Mgeo_distance","Mgeo_plus_history","switch_conditional_nll",supported)
    report["switch_geo_to_markov_gain"]=summarize_contrast(
        "Mgeo_distance","M1_previous","switch_conditional_nll",supported)
    report["switch_static_to_geometry_gain"]=summarize_contrast(
        "M0_static","Mgeo_distance","switch_conditional_nll",supported)
    report["all_geo_to_geo_history_gain"]=summarize_contrast(
        "Mgeo_distance","Mgeo_plus_history","full_nll",perbee)
    report["all_static_to_geometry_gain"]=summarize_contrast(
        "M0_static","Mgeo_distance","full_nll",perbee)
    report["self_repeat_binary_nll_bee_equal"]={
        model:sum(p["within_bee_models"][model]["binary_repeat_nll"] for p in perbee)/len(perbee)
        for model in MODES}
    report["status"]="FITTED_HELDOUT_SOURCE_GEOMETRY_DESCRIPTIVE"
    return report
