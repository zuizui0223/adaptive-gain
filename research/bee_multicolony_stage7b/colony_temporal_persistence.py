"""Stage 7b: multicolony, *collective* nectar-use temporal persistence.

Science grain: robotic flower sensor events are identified to experimental
COLONY and flower, NOT individual bee. Reproduces original author's
2-second filtering exactly before the new experiment.

Pre-registered in PROTOCOL_ROBOTIC_FLOWER_2026_10_28.md:
- 5 minute fixed nonoverlapping bins within each colony/day/hour
- >=3 sensor visit clusters per bin and >=4 eligible bins per hour
- only adjacent eligible 5-minute bin pairs, never bridge gaps/hours/days
- within-colony mean of smoothed nectar-share absolute adjacent differences
- >=10 eligible pairs/colony, >=8 qualifying colonies
- 199 within-hour permutations of *whole* (n,q,device) bin records;
  keep ineligible slots unpermuted and no individual-bee attribution.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from datetime import datetime
import argparse
import json
import math
import random
from pathlib import Path

from reproduce_original_sensor_cleaning import (
    AUTHOR_EXPECTED_CLEANED_EVENTS,ORIGINAL_MD5,run as source_cleaning
)

BIN_SECONDS=300
MIN_BIN_VISITS=3
MIN_BINS_PER_HOUR=4
MIN_PAIRS_PER_COLONY=10
MIN_COLONIES=8
PERMUTATIONS=199
SEED=20261028

def _empty_bin():
    return {"n":0,"q":0,"devices":Counter()}

def prepare_hours(events,required_events=AUTHOR_EXPECTED_CLEANED_EVENTS):
    """Never assume 54k independent bees; each event belongs to one colony."""
    if required_events is not None and len(events)!=required_events:
        raise ValueError("NO_GO_PUBLISHED_PROCESSED_EVENT_COUNT_MISMATCH")
    all_colonies=set()
    hour_bins=defaultdict(lambda:[_empty_bin() for _ in range(12)])
    colonydays=set()
    all_nectar=Counter()
    invalid=[]
    for idx,r in enumerate(events):
        colony=str(r.get("colony","")).strip()
        day=str(r.get("day","")).strip()
        ts=r.get("timestamp_local")
        nectar=r.get("nectar")
        flower=r.get("flower_id")
        if not colony or not day or not isinstance(ts,datetime):
            invalid.append({"row":idx,"problem":"no source colony/date/time"})
            continue
        if ts.date().isoformat()!=day:
            invalid.append({"row":idx,"problem":"source local day and stamp mismatch"})
            continue
        if nectar not in ("control","quercetin"):
            invalid.append({"row":idx,"problem":"unclassified original reward source"})
            continue
        if not isinstance(flower,int) or flower<=0:
            invalid.append({"row":idx,"problem":"no valid source robotic flower"})
            continue
        minute=ts.minute
        binidx=minute//5
        if not 0<=binidx<12:
            raise ValueError("NO_GO_BAD_FIVE_MINUTE_INDEX")
        key=(colony,day,ts.hour)
        slot=hour_bins[key][binidx]
        slot["n"]+=1
        slot["q"]+=int(nectar=="quercetin")
        slot["devices"][flower]+=1
        colonydays.add((colony,day))
        all_colonies.add(colony)
        all_nectar[nectar]+=1
    if invalid:
        raise ValueError("NO_GO_ORIGINAL_ROBOTIC_SOURCE_FIELDS_INVALID "+
                         str(Counter(v["problem"] for v in invalid)))
    if sum(all_nectar.values())!=len(events):
        raise ValueError("NO_GO_COLLECTIVE_REWARD_COUNTS_LOST")
    # Source/cage event streams have no individual bee tag; no "previous
    # bee flower" can be constructed from chronological device log rows.
    hourly=[]
    source_eligible_bins=0
    source_eligible_hours=0
    adjacent_pairs=0
    eligible_visits=0
    for (colony,day,hour),values in sorted(hour_bins.items()):
        ok=tuple(i for i,x in enumerate(values) if x["n"]>=MIN_BIN_VISITS)
        if len(ok)<MIN_BINS_PER_HOUR:continue
        source_eligible_hours+=1
        okset=set(ok)
        pairs=tuple((i,i+1) for i in range(11)
                    if i in okset and i+1 in okset)
        if not pairs:continue
        source_eligible_bins+=len(ok)
        adjacent_pairs+=len(pairs)
        eligible_visits+=sum(values[i]["n"] for i in ok)
        hourly.append({"key":(colony,day,hour),
                       "bins":tuple(values),
                       "eligible_positions":ok,
                       "pair_indices":pairs})
    receipt={
        "source_processed_robotic_events":len(events),
        "source_original_distinct_colonies":len(all_colonies),
        "source_original_colony_days":len(colonydays),
        "total_native_colony_day_hour_slots":len(hour_bins),
        "hour_blocks_with_ge4_eligible_5minute_bins":source_eligible_hours,
        "hour_blocks_eligible_and_adjacent_pairs":len(hourly),
        "eligible_source_bins_in_relevant_hours":source_eligible_bins,
        "eligible_adjacent_5minute_pairs_all_colonies":adjacent_pairs,
        "source_events_within_eligible_5minute_hour_positions":eligible_visits,
        "source_nectar_types":dict(all_nectar),
        "all_colony_ids_source":sorted(all_colonies),
        "source_timestamp_clock":"original local Europe/Brussels HH:MM:SS; within recorded day and hour only",
        "min_visits_per_bin":MIN_BIN_VISITS,
        "min_bins_per_hour":MIN_BINS_PER_HOUR,
        "adjacency":"5min index i and i+1 within same source colony day local hour, never bridge missing slots",
        "inference_unit":"original experimental colony, NOT source sensor events or bee individual"
    }
    return hourly,receipt

def _smooth_share(binrecord):
    n=binrecord["n"];q=binrecord["q"]
    if n<MIN_BIN_VISITS or not 0<=q<=n:
        raise ValueError("NO_GO_INVALID_BIN_N_OR_Q_FOR_SMOOTHING")
    return (q+0.5)/(n+1.0)

def evaluate_hour_blocks(hours, shuffled=None):
    """Per-colony sums/denominators on fixed original eligible pair support."""
    sums=defaultdict(float)
    pairs=Counter()
    block_counts=Counter()
    for block_i,h in enumerate(hours):
        key=h["key"]
        colony=key[0]
        bins=h["bins"] if shuffled is None else shuffled[block_i]
        if any(bins[i]["n"]<MIN_BIN_VISITS for i in h["eligible_positions"]):
            raise ValueError("NO_GO_PERMUTATION_CHANGED_ELIGIBLE_BIN_POSITIONS")
        block_counts[colony]+=1
        for i,j in h["pair_indices"]:
            sums[colony]+=abs(_smooth_share(bins[i])-_smooth_share(bins[j]))
            pairs[colony]+=1
    return sums,pairs,block_counts

def qualified_colonies(hours,receipt):
    sums,pairs,blocks=evaluate_hour_blocks(hours)
    source_colonies=receipt["all_colony_ids_source"]
    valid=[c for c in source_colonies if pairs[c]>=MIN_PAIRS_PER_COLONY]
    rejected=[{"colony":c,"valid_adjacent_pairs":int(pairs[c]),
               "eligible_hour_blocks":int(blocks[c])}
              for c in source_colonies if c not in valid]
    percolony=[{"colony":c,"valid_adjacent_pairs":int(pairs[c]),
                "eligible_hour_blocks":int(blocks[c]),
                "observed_adjacent_reward_share_absdiff":sums[c]/pairs[c]}
               for c in valid]
    result={
        "status":"COLONY_TEMPORAL_SUPPORT_PASSED" if len(valid)>=MIN_COLONIES
                 else "NO_GO_COLONY_LEVEL_HOUR_MATCHING",
        "minimum_pairs_per_colony":MIN_PAIRS_PER_COLONY,
        "minimum_independent_source_colonies":MIN_COLONIES,
        "eligible_source_colonies":len(valid),
        "excluded_source_colonies":rejected,
        "qualifying_colony_data":percolony,
        "observed_equal_colony_mean_D":(
            sum(c["observed_adjacent_reward_share_absdiff"] for c in percolony)/len(percolony)
            if percolony else None),
        "visit_weighted_inference":False,
        "raw_54k_sensor_events_are_not_independent_animals":True
    }
    return result,valid,pairs

def _shuffle_source_hour(h,rng):
    # Permute entire original 5-minute bin records, which contain the observed
    # (n,q,flower count) as one inseparable object. Keep all other bin slots.
    r=list(h["bins"])
    positions=h["eligible_positions"]
    values=[r[i] for i in positions]
    rng.shuffle(values)
    for i,value in zip(positions,values):r[i]=value
    return tuple(r)

def conditional_temporal_test(events,required_events=AUTHOR_EXPECTED_CLEANED_EVENTS,
                              permutations=PERMUTATIONS,seed=SEED):
    if permutations<1:raise ValueError("NO_GO_PERMUTATION_COUNT")
    hours,source=prepare_hours(events,required_events=required_events)
    q,qualifying,pair_count=qualified_colonies(hours,source)
    result={
        "study":"independent 2026 KU Leuven RDR 18-colony robotic-flower self-medication experiment",
        "source_doi":"10.48804/UIIVLP",
        "status":q["status"],
        "original_source_grain":source,
        "admission":q,
        "statistics_definition":"D_colony = mean adjacent within-hour 5min |(q_i+.5)/(n_i+1)-(q_j+.5)/(n_j+1)|, min 3 original cleaned sensor events in each bin",
        "null":"within (colony, date, hour), randomize entire observed eligible five-min (n,q,device) records only; preserve ineligible positions and true hour totals",
        "not_individual_bee_routes_or_visual_flower_perception":True,
        "permutations":permutations,
        "seed":seed
    }
    if q["status"]!="COLONY_TEMPORAL_SUPPORT_PASSED":
        return result
    count=Counter()
    sum_null_colony=Counter()
    null=[]
    rng=random.Random(seed)
    real=q["observed_equal_colony_mean_D"]
    for replicate in range(permutations):
        shuffled=[_shuffle_source_hour(h,rng) for h in hours]
        vals,denom,blocks=evaluate_hour_blocks(hours,shuffled=shuffled)
        if any(denom[c]!=pair_count[c] for c in qualifying):
            raise ValueError("NO_GO_SHUFFLED_SOURCE_PAIR_DENOMINATOR_CHANGED")
        m=sum(vals[c]/denom[c] for c in qualifying)/len(qualifying)
        null.append(m)
        for c in qualifying:sum_null_colony[c]+=vals[c]/denom[c]
    if len(null)!=permutations:raise ValueError("NO_GO_MISSING_NULL_REPLICATES")
    mean_null=sum(null)/len(null)
    sorted_null=sorted(null)
    percolony=[]
    for base in q["qualifying_colony_data"]:
        tag=base["colony"]
        null_mean=sum_null_colony[tag]/permutations
        percolony.append({
            **base,
            "shuffled_hour_preserving_mean_D":null_mean,
            "extra_local_temporal_smoothness_null_minus_observed":(
                null_mean-base["observed_adjacent_reward_share_absdiff"])
        })
    result["observed_vs_conditional_null"]={
        "observed_equal_colony_mean_D":real,
        "randomized_equal_colony_mean_D_mean":mean_null,
        "randomized_equal_colony_mean_D_q05":sorted_null[int(.05*(permutations-1))],
        "randomized_equal_colony_mean_D_q50":sorted_null[int(.5*(permutations-1))],
        "randomized_equal_colony_mean_D_q95":sorted_null[int(.95*(permutations-1))],
        "observed_minus_randomized_D":real-mean_null,
        "extra_local_smoothness_null_minus_observed_D":mean_null-real,
        "one_tailed_Monte_Carlo_p_for_temporal_smoothness":(
            1+sum(x<=real+1e-12 for x in null))/(permutations+1),
        "resolution":1/(permutations+1),
        "source_colonies_with_positive_local_smoothness":sum(
            x["extra_local_temporal_smoothness_null_minus_observed"]>0
            for x in percolony),
        "source_colonies_with_negative_local_smoothness":sum(
            x["extra_local_temporal_smoothness_null_minus_observed"]<0
            for x in percolony),
        "source_colonies_with_zero_local_smoothness":sum(
            x["extra_local_temporal_smoothness_null_minus_observed"]==0
            for x in percolony),
        "per_colony_effect_and_support":percolony,
        "do_not_treat_199_randomizations_as_199_independent_experiments":True
    }
    result["status"]="COMPUTED_COLONY_LEVEL_WITHIN_HOUR_TEMPORAL_PERSISTENCE"
    return result

def run(root:Path):
    events,reconstruction=source_cleaning(root)
    if reconstruction["status"]!="MATCHES_PUBLISHED_AUTHOR_COUNTS":
        raise ValueError("NO_GO_ORIGINAL_R_PROCESSING_NOT_RECONCILED")
    result=conditional_temporal_test(events)
    result["original_source_author_processing_reproduction"]={
        "source_md5":ORIGINAL_MD5,
        "raw_original_sensor_rows":reconstruction["original_source_cleaning_receipt"]["original_sensor_rows"],
        "exact_duplicate_sensor_records":reconstruction["original_source_cleaning_receipt"]["source_exact_duplicate_rows"],
        "post_author_2sec_clustered_events":AUTHOR_EXPECTED_CLEANED_EVENTS,
        "source_reproduced":True
    }
    out=root/"colony_reward_temporal_persistence.json"
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE7B_COLONY_TEMPORAL_RESULT "+json.dumps(result,ensure_ascii=False,allow_nan=False),flush=True)
    print("STAGE7B_COLONY_TEMPORAL_COMPLETE",flush=True)
    return result

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="rdr_multicolony_source")
    a=ap.parse_args()
    run(Path(a.out))
