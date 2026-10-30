"""Stage13: first-choice-fixed, flower-marginal-preserving original cue-order null.

All recorded visits are real source flower IDs 1..12. Conditional shuffles
are statistical, not alternate feasible bee flights. No timing, reward
intake, wind, sensory acquisition order, or population-level inference.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
import csv
import hashlib
import json
import random

from sequence_grain import parse_positions

ORIGINAL_SHA256="248b8257ac4a756a16704eaedbabd3909f24be1d8bd6d4a64e6bcbb100ee8e65"
N_SHUFFLES=999
SEED=20261030
GROUPS={"test_easy":29,"test_diff":28}
COLONY_COUNTS={"a":4,"b":35,"c":18}

def score_switched(positions,cues):
    """Cue-state persistence among actual switches between different flowers."""
    seq=list(positions)
    cue_set=set(cues)
    if any(not isinstance(v,int) or not 1<=v<=12 for v in seq):
        raise ValueError("NO_GO_INVALID_ORIGINAL_FLOWER_ID")
    if any(not isinstance(v,int) or not 1<=v<=12 for v in cue_set):
        raise ValueError("NO_GO_INVALID_CUE_SET")
    switched=[(a,b) for a,b in zip(seq,seq[1:]) if a!=b]
    n=len(switched)
    if n==0:
        return None,0
    equal=sum((a in cue_set)==(b in cue_set) for a,b in switched)
    return equal/n,n

def shuffle_after_first(positions,rng):
    """Hold first original flower and exactly all visit-count marginals fixed."""
    seq=list(positions)
    if not seq:
        raise ValueError("NO_GO_EMPTY_ORIGINAL_BEE_PATH")
    tail=seq[1:]
    rng.shuffle(tail)
    return [seq[0]]+tail

def _avg(xs):
    if not xs:
        raise ValueError("NO_GO_EMPTY_ORIGINAL_COLONY")
    return sum(xs)/len(xs)

def test_source(rows,permutations=N_SHUFFLES,seed=SEED,expected_original=True):
    if not isinstance(permutations,int) or permutations<1:
        raise ValueError("NO_GO_NONPOSITIVE_CONDITIONAL_PERMUTATIONS")
    if expected_original and (permutations!=N_SHUFFLES or seed!=SEED):
        raise ValueError("NO_GO_RESELECTED_FROZEN_PERMUTATION_RULE")
    source=list(rows)
    if not source:
        raise ValueError("NO_GO_NO_ORIGINAL_TEST_BEES")
    groups=Counter()
    colony_counts=Counter()
    source_keys=set()
    eligible=[]
    excluded=[]
    test_landings=0
    source_switched=0
    for row in source:
        group=str(row.get("group","")).strip()
        if group not in GROUPS:
            raise ValueError("NO_GO_NOT_ORIGINAL_TEST_PHASE")
        colony=str(row.get("colony","")).strip()
        bee=str(row.get("id","")).strip()
        if not colony or not bee:
            raise ValueError("NO_GO_NO_PAIRED_ANIMAL_IDENTIFIERS")
        key=(colony,bee)
        if key in source_keys:
            raise ValueError("NO_GO_DUPLICATE_TEST_BEE "+repr(key))
        source_keys.add(key)
        groups[group]+=1
        colony_counts[colony]+=1
        visits=parse_positions(str(row["landed"]))
        cue_ids=parse_positions(str(row["cue"]))
        if len(cue_ids)!=4 or len(set(cue_ids))!=4:
            raise ValueError("NO_GO_NOT_FOUR_DISTINCT_CUED_FLOWERS")
        test_landings+=len(visits)
        value,n=score_switched(visits,set(cue_ids))
        if value is None or len(set(visits))<2:
            excluded.append({"source_colony":colony,"source_bee":bee,
                             "reason":"NO_REAL_BETWEEN_FLOWER_SWITCHES"})
            continue
        source_switched+=n
        eligible.append({"colony":colony,"visits":visits,
                         "cues":set(cue_ids),"source_switched":n,
                         "actual":value})
    if expected_original:
        if len(source)!=57 or groups!=Counter(GROUPS) or colony_counts!=Counter(COLONY_COUNTS):
            raise ValueError("NO_GO_ORIGINAL_SOURCE_TEST_DESIGN_CHANGED "+repr((len(source),groups,colony_counts)))
        if test_landings!=1308:
            raise ValueError("NO_GO_ORIGINAL_TEST_VISITS_CHANGED")
    source_colonies=sorted(colony_counts)
    eligible_by_colony=defaultdict(list)
    for e in eligible:
        eligible_by_colony[e["colony"]].append(e)
    if any(not eligible_by_colony[c] for c in source_colonies):
        raise ValueError("NO_GO_ORIGINAL_COLONY_WITHOUT_SWITCHES")
    actual_by_colony={c:_avg([e["actual"] for e in eligible_by_colony[c]])
                      for c in source_colonies}
    actual=_avg(list(actual_by_colony.values()))
    rng=random.Random(seed)
    sims=[]
    simulated_by_colony={c:[] for c in source_colonies}
    for iteration in range(permutations):
        by_colony=defaultdict(list)
        for e in eligible:
            visited=shuffle_after_first(e["visits"],rng)
            shuffled,nswitched=score_switched(visited,e["cues"])
            if shuffled is None or nswitched<=0:
                raise ValueError("NO_GO_SHUFFLE_REMOVED_ALL_GENUINE_BEE_SWITCHES")
            by_colony[e["colony"]].append(shuffled)
        colony_means={c:_avg(by_colony[c]) for c in source_colonies}
        for c in source_colonies:
            simulated_by_colony[c].append(colony_means[c])
        sims.append(_avg(list(colony_means.values())))
    null_mean=_avg(sims)
    sorted_null=sorted(sims)
    bycol_diff={c:actual_by_colony[c]-_avg(simulated_by_colony[c]) for c in source_colonies}
    outcome={
       "status":"ORIGINAL_SOURCE_CONDITIONAL_CUE_SEQUENCE_ORDER_EVALUATED",
       "original_source":"Smolla et al 2016 Dryad 10.5061/dryad.3jb68 version 19480",
       "source_test_bee_rows":len(source),
       "source_test_landing_events":test_landings,
       "source_eligible_bees":len(eligible),
       "source_eligible_genuine_switched_transitions":source_switched,
       "source_colonies":len(source_colonies),
       "source_bees_by_colony":dict(sorted(colony_counts.items())),
       "source_eligible_bees_by_colony":{c:len(eligible_by_colony[c]) for c in source_colonies},
       "source_source_technical_exclusions":excluded,
       "original_test_groups":dict(sorted(groups.items())),
       "permutations":permutations,
       "source_conditional_random_seed":seed,
       "first_original_visit_held_fixed_per_bee":True,
       "all_original_flower_use_frequencies_held_fixed_per_bee":True,
       "source_real_flower_switch_only":True,
       "actual_colony_equal_cue_state_persistence":actual,
       "null_mean_colony_equal_cue_state_persistence":null_mean,
       "actual_minus_null_mean":actual-null_mean,
       "null_q05":sorted_null[max(0,int(.05*(permutations-1)))],
       "null_q95":sorted_null[int(.95*(permutations-1))],
       "one_sided_source_conditional_p":(1+sum(z>=actual-1e-12 for z in sims))/(permutations+1),
       "actual_by_colony":actual_by_colony,
       "null_mean_by_colony":{c:_avg(simulated_by_colony[c]) for c in source_colonies},
       "colony_actual_minus_null":bycol_diff,
       "no_source_cue_attention_or_adaptive_query_order_identified":True,
       "no_wind_or_fitness_endpoint_measured":True,
       "only_three_original_colonies_not_population_inference":True,
       "source_conditional_statistical_null_not_physical_intervention":True,
    }
    return outcome

def run(root):
    folder=Path(root)
    raw=(folder/"beeLandings.csv").read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_SHA256:
        raise ValueError("NO_GO_ORIGINAL_SOURCE_SHA256_MISMATCH")
    try:
        text=raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text=raw.decode("latin-1")
    source=list(csv.DictReader(text.splitlines()))
    if len(source)!=114:
        raise ValueError("NO_GO_ORIGINAL_BEE_ROWS_CHANGED")
    tests=[r for r in source if str(r["group"]).strip() in GROUPS]
    if len(tests)!=57:
        raise ValueError("NO_GO_ORIGINAL_TEST_BEES_CHANGED")
    outcome=test_source(tests)
    outcome["original_source_file_sha256"]=ORIGINAL_SHA256
    outcome["pre_outcome_frozen_protocol"]="PROTOCOL_FROZEN_SEQUENCE_TEST_20261030.md"
    outfile=folder/"smolla2016_cue_sequence_test.json"
    outfile.write_text(json.dumps(outcome,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE13_ORIGINAL_CUE_ORDER_RESULT "+
          json.dumps(outcome,ensure_ascii=False,allow_nan=False),flush=True)
    print("STAGE13_ORIGINAL_CUE_ORDER_COMPLETE",flush=True)
    return outcome

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage13_original")
    run(p.parse_args().out)
