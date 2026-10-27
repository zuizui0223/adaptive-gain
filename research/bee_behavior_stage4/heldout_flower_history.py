"""Source-independent, leakage-free individual bee transition prediction.

Models:
 M0: each tagged bee's static flower preference (Dirichlet .5).
 M1: previous physical flower -> next flower transitions (Dirichlet
     shrinkage beta=5 toward the same bee's M0, *all from train only*).
The test split is last *monitored day* per bee (when source dates exist).
No wind, competitor-cue perception, flower reward or causal routeability
is inferred from a positive log-loss gain.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import itertools
import math

ALPHA = 0.5
BETA = 5.0
MIN_TRAIN_VISITS = 20
MIN_TEST_TRANSITIONS = 5
MIN_ELIGIBLE_BEES = 5

def _required_row(r):
    req=("bee","flower","day","timestamp")
    if not all(k in r for k in req):
        raise ValueError("missing strictly canonical event fields: "+str(req))
    if any(r[k] is None or str(r[k]).strip()=="" for k in req):
        raise ValueError("canonical event has missing bee/flower/day/timestamp")
    return tuple(r[k] for k in req)

def validate_events(events, available_flowers):
    flowers=tuple(sorted(set(available_flowers)))
    if len(flowers)<2:raise ValueError("at least two physically present flowers required")
    if not events:raise ValueError("no canonical source events")
    unused=set(flowers)
    groups=defaultdict(list)
    source_event_keys=set()
    for row in events:
        bee,flower,day,stamp=_required_row(row)
        if flower not in flowers:raise ValueError("observed flower absent from physical array")
        unused.discard(flower)
        key=(bee,day,stamp)
        if key in source_event_keys:
            # Simultaneous arrival timestamps are not ordered decisions. The
            # source adapter must identify and explicitly quarantine them.
            raise ValueError("ambiguous same-bee same-day timestamp; NO_GO_SEQUENCE_TIE")
        source_event_keys.add(key)
        groups[(bee,day)].append((stamp,flower))
    for key,seq in groups.items():
        try:seq.sort(key=lambda x:x[0])
        except TypeError as e:raise ValueError("timestamps not comparable") from e
        if len(seq)!=len({x[0] for x in seq}):raise ValueError("ambiguous same-bee timestamp")
    return groups,flowers,{"input_source_events":len(events),
                           "observed_physical_flowers":len(flowers)-len(unused),
                           "physically_present_array_flowers":len(flowers),
                           "bee_day_groups":len(groups),
                           "bees":len({k[0] for k in groups}),
                           "unvisited_available_flower_ids_count":len(unused)}

def static_probs(training_visits,flowers):
    counts=Counter(training_visits)
    n=len(training_visits)
    return {f:(counts[f]+ALPHA)/(n+ALPHA*len(flowers)) for f in flowers}

def transition_probs(prev,counts,static,flowers):
    total=sum(counts.get((prev,next_flower),0) for next_flower in flowers)
    return {f:(counts.get((prev,f),0)+BETA*static[f])/(total+BETA)
            for f in flowers}

def paired_predict(events, available_flowers, last_day=None):
    """Return held-out proper scores by bee and explicit no-go receipt.

    If last_day is None, use the *last source day over all bees*, not a
    cherry-picked last day that maximizes effect. Within-day transitions
    only, avoiding invented nest-bout transitions across nights.
    """
    groups,flowers,gr=validate_events(events,available_flowers)
    all_days=sorted({k[1] for k in groups})
    if len(all_days)<2:raise ValueError("NO_GO_NO_TEMPORAL_HOLDOUT")
    cutoff=all_days[-1] if last_day is None else last_day
    if cutoff not in all_days:raise ValueError("holdout day absent")
    bees=sorted({k[0] for k in groups})
    perbee=[]
    no_go=[]
    for bee in bees:
        train_events=[]
        train_transitions=Counter()
        test_transitions=[]
        for day in all_days:
            seq=groups.get((bee,day),[])
            ordered=[f for ts,f in seq]
            if day<cutoff:
                train_events.extend(ordered)
                train_transitions.update(zip(ordered[:-1],ordered[1:]))
            elif day==cutoff:
                test_transitions.extend(zip(ordered[:-1],ordered[1:]))
            else:
                raise ValueError("holdout cutoff not the last day: future data would be ignored")
        if len(train_events)<MIN_TRAIN_VISITS or len(test_transitions)<MIN_TEST_TRANSITIONS:
            no_go.append({"bee":str(bee),"train_visits":len(train_events),
                          "heldout_transitions":len(test_transitions),
                          "reason":"INSUFFICIENT_BEE_TRAIN_OR_TEST"})
            continue
        static=static_probs(train_events,flowers)
        model0_loss=0.0
        model1_loss=0.0
        for prev,nextflower in test_transitions:
            p0=static[nextflower]
            p1=transition_probs(prev,train_transitions,static,flowers)[nextflower]
            if p0<=0 or p1<=0:raise AssertionError("positive smoothing contract broken")
            model0_loss-=math.log(p0)
            model1_loss-=math.log(p1)
        n=len(test_transitions)
        perbee.append({"bee":str(bee),"training_visits":len(train_events),
                       "training_transitions":sum(train_transitions.values()),
                       "heldout_transitions":n,
                       "loss_M0_static_nats_per_transition":model0_loss/n,
                       "loss_M1_previous_flower_nats_per_transition":model1_loss/n,
                       "M1_gain_nats_per_transition":(model0_loss-model1_loss)/n})
    out={
        "status":"source_event_gate_passed",
        "holdout_day":str(cutoff),
        "source_data_grain":gr,
        "minimum_train_visits_per_bee":MIN_TRAIN_VISITS,
        "minimum_test_transitions_per_bee":MIN_TEST_TRANSITIONS,
        "minimum_individual_bees":MIN_ELIGIBLE_BEES,
        "M0_smoothing_alpha":ALPHA,"M1_shrinkage_beta":BETA,
        "feature_source":"physical flower identity and previous visit only",
        "split_policy":"train days strictly earlier than globally final source day",
        "no_future_leakage":"frozen transition matrix; previous test flower is known only when observed before predicted next landing",
        "per_bee":perbee,"excluded_bees":no_go,
        "not_a_wind_intervention_or_cue_sequence_observation":True}
    if len(perbee)<MIN_ELIGIBLE_BEES:
        out["status"]="NO_GO_TOO_FEW_INDEPENDENT_BEE_TAGS_FOR_HOLDOUT"
        return out
    gains=[x["M1_gain_nats_per_transition"] for x in perbee]
    out["bee_mean_M1_gain_nats_per_transition"]=sum(gains)/len(gains)
    out["bee_median_M1_gain_nats_per_transition"]=sorted(gains)[len(gains)//2]
    out["gain_positive_bees"]=sum(x>0 for x in gains)
    out["gain_negative_bees"]=sum(x<0 for x in gains)
    out["total_heldout_transitions"]=sum(x["heldout_transitions"] for x in perbee)
    out["microaveraged_gain_descriptive_only"]=(
        sum(x["M1_gain_nats_per_transition"]*x["heldout_transitions"] for x in perbee)
        /out["total_heldout_transitions"])
    # Sign flips treat bee tags as sampling units; from one colony this is
    # only a descriptive directional sensitivity, not independent colonies.
    if len(gains)<=16:
        observed=abs(sum(gains)/len(gains))
        exceed=0
        for signs in itertools.product((-1,1),repeat=len(gains)):
            mean=abs(sum(s*x for s,x in zip(signs,gains))/len(gains))
            if mean+1e-12>=observed:exceed+=1
        out["within_colony_bee_sign_flip_p_descriptive"]=exceed/(2**len(gains))
    return out
