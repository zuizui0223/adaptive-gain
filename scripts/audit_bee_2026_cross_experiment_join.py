"""Reject invalid trial-level joins between two public bee behavioral tasks.

Source: He et al. (2026), bioRxiv DOI 10.64898/2026.09.15.751944.
Original data: https://github.com/Cuixiaojian21/bee_metacognition
Pinned commit: 7f886394b4de872ecdb19ca4ea214ec321d5dce9

Source files (not redistributed here):
- data/4_active_information_seeking_trials.csv
  git blob 26259c9071c6d73141d56b9bedd396cab1a04491
- data/3_decision_process_metrics.csv
  git blob 833bf8f2f1e15839050bac6a1e217a031390bb5f

TRIAL IDs are reused across tasks. Identical numeric Trial_ID, Bee_ID and
Trial_Number values do not show that a latency belongs to an information
request. In the source, identical keys often have different task difficulty.
Consequently NEVER perform a trial-level regression joining these files.
A descriptive cross-task BEE-level association is allowed as exploratory
only; it cannot establish the impact of requesting information on latency.

Standard library only, no network access and no raw third-party data copied.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

REQUIRED_ACTIVE = {
    "Trial_ID", "Bee_ID", "Trial_Number", "Difficulty", "Trial_Type",
    "Info_Requested", "Actually_Landed_On_Platform",
}
REQUIRED_LATENCY = {
    "Trial_ID", "Bee_ID", "Trial_Number", "Difficulty",
    "Decision_Latency_ms",
}
DIFFICULTIES = ("Easy", "Hard", "Impossible")
TRIAL_TYPES = ("Regular", "Random_Free_Cue")


def load_rows(path: Path, required: set[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"required columns absent: {sorted(required-set(reader.fieldnames or []))}")
        rows = list(reader)
    keys = set()
    for row in rows:
        key = (row["Trial_ID"], row["Bee_ID"], row["Trial_Number"])
        if key in keys:
            raise ValueError(f"duplicate composite key in {path}: {key}")
        keys.add(key)
        if row["Difficulty"] not in DIFFICULTIES:
            raise ValueError(f"unknown difficulty {row['Difficulty']!r}")
    return rows


def pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) != len(y) or len(x) < 3:
        return None
    xm = sum(x)/len(x)
    ym = sum(y)/len(y)
    xx = sum((v-xm)**2 for v in x)
    yy = sum((v-ym)**2 for v in y)
    if xx <= 0 or yy <= 0:
        return None
    return sum((a-xm)*(b-ym) for a,b in zip(x,y))/math.sqrt(xx*yy)


def xorshift32(seed: int):
    state = seed & 0xFFFFFFFF
    if state == 0:
        raise ValueError("seed must be nonzero")
    while True:
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= state >> 17
        state ^= (state << 5) & 0xFFFFFFFF
        state &= 0xFFFFFFFF
        yield state / 4294967296


def two_sided_permutation_p(
    x: list[float], y: list[float], *,
    replicates: int, random_source
) -> float | None:
    observed = pearson(x,y)
    if observed is None:
        return None
    extreme = 0
    for _ in range(replicates):
        shuffled = y[:]
        for i in range(len(shuffled)-1,0,-1):
            j = int(next(random_source)*(i+1))
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        value = pearson(x, shuffled)
        if value is not None and abs(value) >= abs(observed):
            extreme += 1
    return (extreme+1)/(replicates+1)


def audit(
    active: list[dict[str, str]],
    latency: list[dict[str, str]],
    *,
    permutation_replicates: int = 5000,
    seed: int = 0x229184,
) -> dict:
    if permutation_replicates < 1:
        raise ValueError("permutation_replicates must be positive")

    index = {
        (r["Trial_ID"],r["Bee_ID"],r["Trial_Number"]):r
        for r in latency
    }
    if len(index)!=len(latency):
        raise ValueError("duplicate latency composite keys")
    keys_active = {
        (r["Trial_ID"],r["Bee_ID"],r["Trial_Number"])
        for r in active
    }
    if len(keys_active)!=len(active):
        raise ValueError("duplicate active composite keys")

    coincidences=0
    disagreement=0
    confusion = {
        d:{e:0 for e in DIFFICULTIES}
        for d in DIFFICULTIES
    }
    order_counts = {
        f"{lo}-{lo+19}":{
            type_name:{difficulty:{"n":0,"landings":0} for difficulty in DIFFICULTIES}
            for type_name in TRIAL_TYPES
        }
        for lo in (1,21,41,61,81)
    }
    active_bee = defaultdict(dict)
    latency_bee = defaultdict(dict)
    free_per_bee = defaultdict(int)
    info_request_means = {}
    for r in active:
        key=(r["Trial_ID"],r["Bee_ID"],r["Trial_Number"])
        matching=index.get(key)
        if matching is not None:
            coincidences+=1
            confusion[r["Difficulty"]][matching["Difficulty"]]+=1
            if r["Difficulty"]!=matching["Difficulty"]:
                disagreement+=1
        bee=r["Bee_ID"]
        d=r["Difficulty"]
        if r["Trial_Type"] not in TRIAL_TYPES:
            raise ValueError("unsupported trial type")
        trial=int(r["Trial_Number"])
        if not 1<=trial<=100:
            raise ValueError("expected Trial_Number from 1 to 100")
        bin_start=((trial-1)//20)*20+1
        record=order_counts[f"{bin_start}-{bin_start+19}"][r["Trial_Type"]][d]
        record["n"]+=1
        landing=int(r["Actually_Landed_On_Platform"])
        if landing not in (0,1):
            raise ValueError("landing must be 0/1")
        record["landings"]+=landing
        if r["Trial_Type"]=="Random_Free_Cue":
            free_per_bee[bee]+=1
        if r["Trial_Type"]=="Regular":
            accum=active_bee[bee].setdefault(d,[0,0])
            accum[0]+=1
            accum[1]+=landing
    for r in latency:
        bee=r["Bee_ID"]
        d=r["Difficulty"]
        milliseconds=float(r["Decision_Latency_ms"])
        if not math.isfinite(milliseconds) or milliseconds<0:
            raise ValueError("invalid decision latency")
        acc=latency_bee[bee].setdefault(d,[0,0.0])
        acc[0]+=1
        acc[1]+=milliseconds

    blocks={}
    for bin_label,types in order_counts.items():
        blocks[bin_label]={}
        for d in DIFFICULTIES:
            regular=types["Regular"][d]
            free=types["Random_Free_Cue"][d]
            regular_rate=regular["landings"]/regular["n"] if regular["n"] else None
            free_rate=free["landings"]/free["n"] if free["n"] else None
            blocks[bin_label][d]={
                "regular_n":regular["n"],"free_n":free["n"],
                "regular_platform_landing_rate":regular_rate,
                "free_platform_landing_rate":free_rate,
                "free_minus_regular_landing_difference":(
                    free_rate-regular_rate
                    if free_rate is not None and regular_rate is not None
                    else None
                ),
            }
    rng=xorshift32(seed)
    bee_associations={}
    for d in DIFFICULTIES:
        shared=sorted(
            bee for bee in (set(active_bee)&set(latency_bee))
            if d in active_bee[bee] and d in latency_bee[bee]
        )
        x=[active_bee[bee][d][1]/active_bee[bee][d][0] for bee in shared]
        y=[latency_bee[bee][d][1]/latency_bee[bee][d][0] for bee in shared]
        bee_associations[d]={
            "n_bees":len(shared),
            "regular_platform_landing_fraction_vs_other_task_latency_pearson_r":
                pearson(x,y),
            "two_sided_bee_label_permutation_p":
                two_sided_permutation_p(
                    x,y,replicates=permutation_replicates,
                    random_source=rng
                ),
            "scope":"CROSS-TASK BEE-LEVEL DESCRIPTIVE ASSOCIATION; NOT TRIAL MATCHING OR CAUSAL EFFECT",
        }
    free_hist={}
    for bee,number in free_per_bee.items():
        free_hist[str(number)]=free_hist.get(str(number),0)+1
    return {
        "source":{
            "repository":"Cuixiaojian21/bee_metacognition",
            "source_commit":"7f886394b4de872ecdb19ca4ea214ec321d5dce9",
            "active_blob_sha":"26259c9071c6d73141d56b9bedd396cab1a04491",
            "latency_blob_sha":"833bf8f2f1e15839050bac6a1e217a031390bb5f",
        },
        "active_trials":len(active),
        "latency_trials":len(latency),
        "identical_numeric_triplet_keys":coincidences,
        "matching_task_difficulty_at_identical_triplet_keys":
            coincidences-disagreement,
        "mismatched_task_difficulty_at_identical_triplet_keys":
            disagreement,
        "mismatch_fraction":disagreement/coincidences if coincidences else None,
        "task_difficulty_confusion":confusion,
        "free_cue_trials_per_bee_histogram":free_hist,
        "within_trial_order_quintiles":blocks,
        "bee_level_exploration":bee_associations,
        "permutation_method":f"xorshift32 seed={seed}, B={permutation_replicates}; within difficulty",
        "verdict":"HOLD_NO_CROSS_EXPERIMENT_TRIAL_LEVEL_LATENCY_JOIN",
        "interpretation":(
            "The same numeric Trial_ID, Bee_ID, Trial_Number are reused across "
            "different tasks; mismatching difficulty demonstrates they are "
            "not shared trial events. Never regress active requests on "
            "Decision_Latency_ms after merging these files on those IDs. "
            "Same-bee cross-task associations are exploratory traits only, "
            "not individual-trial effects."
        ),
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--active",type=Path,required=True)
    parser.add_argument("--latency",type=Path,required=True)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--permutations",type=int,default=5000)
    args=parser.parse_args()
    result=audit(
        load_rows(args.active,REQUIRED_ACTIVE),
        load_rows(args.latency,REQUIRED_LATENCY),
        permutation_replicates=args.permutations,
    )
    text=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.write_text(text,encoding="utf-8")
    else:
        print(text,end="")


if __name__=="__main__":
    main()
