"""Parse original wide foraging-bout table; evaluate bee routes without event-time fabrication.

Source: Pasquaretta et al. (2019), Movement Ecology 7:4, original
supplementary Dataset S1, publisher-byte SHA-256 source gate.

Each source CSV row is ONE BOUT, followed by ORDERED VISITED FLOWER IDs
in anonymous CSV slots. No exact time for an individual flower landing is
recorded in Dataset S1. Do not infer social encounter/displacement status.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import itertools
import json
import math
import re

from heldout_flower_history import (
    ALPHA,BETA,MIN_TRAIN_VISITS,MIN_TEST_TRANSITIONS,MIN_ELIGIBLE_BEES,
    static_probs,transition_probs,
)

EXPECTED_SOURCE_PREFIX=("day","bee","foraging bout","start_time","end_time","duration")
PHYSICAL_FLOWERS=tuple(str(i) for i in range(1,11))
PUBLISHER_CSV_SHA256="0d30b0957c4b18602beebf60a915e03bee26142a8593f252badd77881b5e9dfe"

def as_source_integer(value,field):
    raw=str(value).strip()
    if not re.fullmatch(r"\d+",raw):
        raise ValueError(f"NO_GO_INVALID_SOURCE_{field}: value {raw!r}")
    return int(raw)

def parse_bouts(records,meta):
    if meta.get("source_layout")!="one_foraging_bout_per_row_ordered_unnamed_visit_slots":
        raise ValueError("NO_GO_EXPECTED_ORIGINAL_WIDE_BOUT_LAYOUT")
    if tuple(meta["columns"][:6])!=EXPECTED_SOURCE_PREFIX:
        raise ValueError("NO_GO_SOURCE_METADATA_ROLE_MISMATCH")
    slots=[f"visit_slot_{i:03d}" for i in range(
        1,meta["source_unnamed_ordered_visit_slots"]+1)]
    bouts=[]
    bee_days=defaultdict(list)
    across=Counter()
    seen=set()
    bounds=[]
    for source_row_no,r in enumerate(records,start=2):
        day=as_source_integer(r["day"],"DAY")
        bee=str(r["bee"]).strip()
        boutno=as_source_integer(r["foraging bout"],"BOUT")
        start=as_source_integer(r["start_time"],"START")
        end=as_source_integer(r["end_time"],"END")
        duration=as_source_integer(r["duration"],"DURATION")
        if not bee:raise ValueError("NO_GO_EMPTY_BEE_ID")
        if not (1<=day<=366 and 0<=start<=86400 and 0<=end<=86400 and end>=start):
            raise ValueError("NO_GO_BOUT_TIME_RANGE")
        if (bee,day,boutno) in seen:
            raise ValueError("NO_GO_DUPLICATED_BOUT_ID")
        seen.add((bee,day,boutno))
        rawvisits=[str(r[k]).strip() for k in slots]
        vals=[v for v in rawvisits if v]
        if vals and rawvisits[:len(vals)]!=vals:
            raise ValueError("NO_GO_GAP_INSIDE_VISIT_ORDER_SLOTS")
        if any(v not in PHYSICAL_FLOWERS for v in vals):
            raise ValueError("NO_GO_VISIT_OUTSIDE_SOURCE_TEN_FLOWER_ARRAY")
        across.update(vals)
        bounds.append((start,end,duration))
        bout={"source_line":source_row_no,"day":day,"bee":bee,"bout":boutno,
              "start_time_seconds":start,"end_time_seconds":end,
              "recorded_duration_seconds":duration,"flowers":vals}
        bouts.append(bout)
        bee_days[(bee,day)].append(bout)
    chrono_errors=0
    for key,seq in bee_days.items():
        seen_starts=set()
        for x in seq:
            if x["start_time_seconds"] in seen_starts:chrono_errors+=1
            seen_starts.add(x["start_time_seconds"])
        seq.sort(key=lambda x:(x["start_time_seconds"],x["bout"]))
        # Chronological order uses the published start time. Distant trips
        # do not imply within-bout flight time. Detect overlap but do not
        # automatically infer social interactions from it.
    pairs=sum(max(len(b["flowers"])-1,0) for b in bouts)
    discrepancy=sum(abs(end-start-duration)>1 for start,end,duration in bounds)
    overlaps=sum(
        sum(a["end_time_seconds"]>b["start_time_seconds"]
            for a,b in zip(seq,seq[1:]))
        for seq in bee_days.values())
    if chrono_errors:
        raise ValueError(f"NO_GO_DUPLICATED_BEE_DAY_BOUT_START: {chrono_errors}")
    audit={
        "source_original_bout_rows":len(records),
        "raw_bout_row_count":len(bouts),
        "source_ordered_flower_visit_slots":len(slots),
        "original_recorded_total_visits":sum(len(b["flowers"]) for b in bouts),
        "original_recorded_within_bout_transitions":pairs,
        "distinct_bee_tags":len({b["bee"] for b in bouts}),
        "distinct_physical_flower_ids_visited":len(across),
        "published_physical_array_size":len(PHYSICAL_FLOWERS),
        "source_data_days":sorted({b["day"] for b in bouts}),
        "per_day_bouts":dict(sorted(Counter(b["day"] for b in bouts).items())),
        "per_day_visits":dict(sorted(Counter(
            {day:sum(len(b["flowers"]) for b in bouts if b["day"]==day)
             for day in {b["day"] for b in bouts}}).items())) if False else {
             str(day):sum(len(b["flowers"]) for b in bouts if b["day"]==day)
             for day in sorted({b["day"] for b in bouts})},
        "bout_visit_count_median":sorted(len(b["flowers"]) for b in bouts)[len(bouts)//2],
        "max_recorded_flower_visits_per_bout":max(map(lambda b:len(b["flowers"]),bouts)),
        "empty_flower_visit_bouts":sum(not b["flowers"] for b in bouts),
        "duration_mismatch_gt1second_rows":discrepancy,
        "recorded_bout_overlaps_same_tag":overlaps,
        "same_bee_day_identical_bout_start_count":chrono_errors,
        "original_paper_all_visits_6205_aligned":sum(len(b["flowers"]) for b in bouts)==6205,
        "published_2019_reported_total_visits":6205,
        "published_2019_reported_social_interactions":628,
        "source_social_encounter_columns_present":False,
        "social_displacement_outcomes_available":False,
        "per_flower_precise_timestamp_available":False,
        "sequence_is_order_of_visits_within_each_bout_only":True,
        "source_bout_count_original_not_a_prior_population_estimate":True
    }
    return bouts,audit

def history_holdout_on_bouts(bouts,flowers=PHYSICAL_FLOWERS):
    """Chronological last-day evaluation, never joining successive trips."""
    universe=tuple(flowers)
    if len(universe)<2:raise ValueError("NO_GO_AVAILABLE_FLOWER_UNIVERSE")
    if any(any(f not in universe for f in bout["flowers"]) for bout in bouts):
        raise ValueError("NO_GO_ORIGINAL_VISIT_NOT_IN_KNOWN_ARRAY")
    days=sorted({b["day"] for b in bouts})
    if len(days)<2:raise ValueError("NO_GO_SINGLE_EXPERIMENTAL_DAY")
    final_day=days[-1]
    bees=sorted({b["bee"] for b in bouts})
    groups=defaultdict(list)
    for bout in bouts:
        groups[bout["bee"]].append(bout)
    perbee=[]
    exclusions=[]
    for bee in bees:
        records=sorted(groups[bee],key=lambda b:(b["day"],b["start_time_seconds"],b["bout"]))
        train=[b for b in records if b["day"]<final_day]
        test=[b for b in records if b["day"]==final_day]
        trainvisits=[f for b in train for f in b["flowers"]]
        train_pairs=Counter(
            pair for b in train for pair in zip(b["flowers"][:-1],b["flowers"][1:]))
        test_pairs=[
            pair for b in test for pair in zip(b["flowers"][:-1],b["flowers"][1:])]
        if len(trainvisits)<MIN_TRAIN_VISITS or len(test_pairs)<MIN_TEST_TRANSITIONS:
            exclusions.append({"bee":bee,"training_flower_visits":len(trainvisits),
                               "heldout_within_bout_transitions":len(test_pairs),
                               "reason":"INSUFFICIENT_INDIVIDUAL_LONGITUDINAL_SUPPORT"})
            continue
        prior=static_probs(trainvisits,universe)
        l0=l1=0.0
        for previous,nxt in test_pairs:
            l0-=math.log(prior[nxt])
            l1-=math.log(transition_probs(previous,train_pairs,prior,universe)[nxt])
        n=len(test_pairs)
        perbee.append({
            "bee":bee,"earlier_day_train_visits":len(trainvisits),
            "earlier_day_train_within_bout_transitions":sum(train_pairs.values()),
            "heldout_last_day_within_bout_transitions":n,
            "mean_M0_static_nll_nats":l0/n,
            "mean_M1_previous_flower_nll_nats":l1/n,
            "M1_minus_M0_gain_nats":(l0-l1)/n,
            "source_bouts_heldout":len(test)})
    report={
        "status":"NO_GO_TOO_FEW_BEE_TAGS" if len(perbee)<MIN_ELIGIBLE_BEES else "FITTED_HELDOUT_BEHAVIORAL_DESCRIPTIVE",
        "source_days":days,"last_source_day_heldout":final_day,
        "available_physical_flower_count":len(universe),
        "heldout_only_within_bout_transitions":True,
        "individual_arrival_times_are_unobserved":True,
        "train_last_day_excluded":True,
        "M0_alpha":ALPHA,"M1_beta":BETA,
        "training_policy":"all source days strictly earlier than globally final recorded day",
        "perbee":perbee,"insufficient_bees":exclusions,
        "bee_count_evaluable":len(perbee),
        "claim_limit":"One colony; prediction/history from observed movement is not source-level sensory information, wind, competition treatment or adaptive fitness"
    }
    if len(perbee)<MIN_ELIGIBLE_BEES:return report
    values=[b["M1_minus_M0_gain_nats"] for b in perbee]
    report["mean_per_bee_gain_nats"]=sum(values)/len(values)
    report["median_per_bee_gain_nats"]=sorted(values)[len(values)//2]
    report["bees_with_positive_gain"]=sum(x>0 for x in values)
    report["bees_with_negative_gain"]=sum(x<0 for x in values)
    report["heldout_within_bout_transitions_total"]=sum(
        b["heldout_last_day_within_bout_transitions"] for b in perbee)
    report["weighted_gain_nats_per_transition_descriptive_only"]=sum(
        b["M1_minus_M0_gain_nats"]*b["heldout_last_day_within_bout_transitions"]
        for b in perbee)/report["heldout_within_bout_transitions_total"]
    if len(values)<=16:
        observed=abs(sum(values)/len(values))
        n_exceed=0
        for signs in itertools.product((-1,1),repeat=len(values)):
            perm=abs(sum(s*v for s,v in zip(signs,values))/len(values))
            if perm+1e-12>=observed:n_exceed+=1
        report["single_colony_bee_signflip_descriptive_p"]=n_exceed/(2**len(values))
    return report
