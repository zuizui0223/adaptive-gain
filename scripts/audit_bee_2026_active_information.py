"""Reproduce a narrow source-schema audit of bee information requests (2026).

Source: He et al., bioRxiv doi:10.64898/2026.09.15.751944.
Raw data: https://github.com/Cuixiaojian21/bee_metacognition
Pinned source commit: 7f886394b4de872ecdb19ca4ea214ec321d5dce9
Pinned data git-blob SHA: 26259c9071c6d73141d56b9bedd396cab1a04491
File: data/4_active_information_seeking_trials.csv.

Information DELIVERED and the active ACTION TO REQUEST it have different
meaning in Random_Free_Cue trials. This script deliberately summarizes
Info_Requested and Actually_Landed_On_Platform separately, and produces
a clustered (bee-level) descriptive bootstrap for Free-versus-Regular
landing-rate differences at each task difficulty.

A difference in platform landing rates is NOT a causal estimate of the
payoff value of information; Free-Cue changes the stimulus context and
possibly motivation. No information-age or wait-vs-query effect is
identified from this dataset. Raw third-party data are not redistributed.
"""
from __future__ import annotations

from collections import defaultdict
import argparse
import csv
import json
import math
from pathlib import Path
from typing import TextIO

SOURCE_REPO = "Cuixiaojian21/bee_metacognition"
SOURCE_COMMIT = "7f886394b4de872ecdb19ca4ea214ec321d5dce9"
SOURCE_BLOB_SHA = "26259c9071c6d73141d56b9bedd396cab1a04491"
SOURCE_PATH = "data/4_active_information_seeking_trials.csv"
SOURCE_URL = (
    f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/"
    + SOURCE_PATH
)
DIFFICULTIES = ("Easy", "Hard", "Impossible")
TRIAL_TYPES = ("Regular", "Random_Free_Cue")
REQUIRED_COLUMNS = {
    "Trial_ID", "Bee_ID", "Difficulty", "Trial_Type",
    "Info_Requested", "Actually_Landed_On_Platform",
}


def parse_trials(handle: TextIO) -> list[dict]:
    reader = csv.DictReader(handle)
    if not REQUIRED_COLUMNS.issubset(set(reader.fieldnames or ())):
        raise ValueError("missing required raw-trial columns")
    rows = []
    ids = set()
    for record in reader:
        key = record["Trial_ID"]
        if key in ids:
            raise ValueError(f"duplicate Trial_ID: {key}")
        ids.add(key)
        for col in ("Info_Requested", "Actually_Landed_On_Platform"):
            if record[col] not in ("0", "1"):
                raise ValueError(f"{col} must contain 0/1, got {record[col]!r}")
            record[col] = int(record[col])
        if record["Trial_Type"] not in TRIAL_TYPES:
            raise ValueError(f"unexpected trial type {record['Trial_Type']!r}")
        if record["Difficulty"] not in DIFFICULTIES:
            raise ValueError(f"unexpected difficulty {record['Difficulty']!r}")
        if not record["Bee_ID"]:
            raise ValueError("Bee_ID is blank")
        rows.append(record)
    return rows


def group_zero():
    return {"n": 0, "land": 0, "info": 0}


def xorshift32(seed: int):
    """Reproduce deterministic V8 bootstrap choices without NumPy."""
    state = seed & 0xFFFFFFFF
    if state == 0:
        raise ValueError("seed must not be zero")
    while True:
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= state >> 17
        state ^= (state << 5) & 0xFFFFFFFF
        state &= 0xFFFFFFFF
        yield state / 4294967296


def percentile_index(sample: list[float], fraction: float):
    ordered = sorted(sample)
    return ordered[min(len(ordered)-1, math.floor(fraction*len(ordered)))]


def summarize_trials(
    rows: list[dict],
    *,
    bootstrap_repetitions: int = 3000,
    seed: int = 0x8E4C19,
) -> dict:
    if bootstrap_repetitions < 1:
        raise ValueError("bootstrap_repetitions must be positive")

    keys = tuple(f"{typ}|{diff}" for typ in TRIAL_TYPES
                 for diff in DIFFICULTIES)
    overall = {key: group_zero() for key in keys}
    by_bee = {}
    for row in rows:
        key = row["Trial_Type"]+"|"+row["Difficulty"]
        bee = by_bee.setdefault(
            row["Bee_ID"], {k: group_zero() for k in keys}
        )
        for dest in (overall[key], bee[key]):
            dest["n"] += 1
            dest["land"] += row["Actually_Landed_On_Platform"]
            dest["info"] += row["Info_Requested"]

    bee_ids = sorted(by_bee)
    bees = [by_bee[bee] for bee in bee_ids]
    n_bees = len(bees)
    if n_bees == 0:
        raise ValueError("no trials found")

    disagreements = {
        "Regular": 0,
        "Random_Free_Cue": 0,
    }
    for row in rows:
        if row["Info_Requested"] != row["Actually_Landed_On_Platform"]:
            disagreements[row["Trial_Type"]] += 1

    bootstrap = {d: [] for d in DIFFICULTIES}
    rng = xorshift32(seed)
    for _ in range(bootstrap_repetitions):
        accumulated = {key: group_zero() for key in keys}
        for i in range(n_bees):
            bee = bees[int(next(rng)*n_bees)]
            for key in keys:
                for field in ("n", "land", "info"):
                    accumulated[key][field] += bee[key][field]
        for diff in DIFFICULTIES:
            reg = accumulated["Regular|"+diff]
            free = accumulated["Random_Free_Cue|"+diff]
            if reg["n"] and free["n"]:
                bootstrap[diff].append(
                    free["land"]/free["n"] - reg["land"]/reg["n"]
                )

    comparisons = {}
    for diff in DIFFICULTIES:
        reg = overall["Regular|"+diff]
        free = overall["Random_Free_Cue|"+diff]
        if not reg["n"] or not free["n"] or not bootstrap[diff]:
            raise ValueError(f"insufficient {diff} trial-type counts")
        comparisons[diff] = {
            "regular_landing": reg["land"]/reg["n"],
            "free_landing": free["land"]/free["n"],
            "free_minus_regular": (
                free["land"]/free["n"] - reg["land"]/reg["n"]
            ),
            "bee_cluster_bootstrap_95": [
                percentile_index(bootstrap[diff], .025),
                percentile_index(bootstrap[diff], .975),
            ],
        }

    within_bee = {}
    for diff in DIFFICULTIES:
        paired = []
        for bee in bees:
            reg = bee["Regular|"+diff]
            free = bee["Random_Free_Cue|"+diff]
            if reg["n"] and free["n"]:
                paired.append(
                    free["land"]/free["n"] - reg["land"]/reg["n"]
                )
        sorted_paired = sorted(paired)
        within_bee[diff] = {
            "n_paired": len(paired),
            "n_missing": n_bees-len(paired),
            "mean": sum(paired)/len(paired) if paired else None,
            "median": sorted_paired[len(paired)//2] if paired else None,
            "positive": sum(x > 0 for x in paired),
            "negative": sum(x < 0 for x in paired),
            "zero": sum(x == 0 for x in paired),
        }

    return {
        "source_repository": SOURCE_REPO,
        "source_commit": SOURCE_COMMIT,
        "source_blob_sha": SOURCE_BLOB_SHA,
        "source_path": SOURCE_PATH,
        "source_url": SOURCE_URL,
        "n_trials": len(rows),
        "n_bees": n_bees,
        "per_bee_trial_count_min": min(
            sum(v["n"] for v in bee.values()) for bee in bees
        ),
        "per_bee_trial_count_max": max(
            sum(v["n"] for v in bee.values()) for bee in bees
        ),
        "groups": overall,
        "request_landing_disagreements": disagreements,
        "landing_comparisons": comparisons,
        "within_bee_differences": within_bee,
        "uncertainty_method": (
            f"bee cluster bootstrap; B={bootstrap_repetitions}; "
            f"xorshift32 seed={seed}; percentiles 2.5 and 97.5"
        ),
        "status": "DESCRIPTIVE_SCHEMA_AND_LANDING_AUDIT_NOT_INFORMATION_FITNESS",
        "claim_ceiling": (
            "Free-Cue and Regular differences in platform landing "
            "do not identify optional information's payoff value, "
            "environmental state drift or optimized passive timing. "
            "Info_Requested is a delivery indicator on Free-Cue trials."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True,
                        help="local copy of public trial-level CSV")
    parser.add_argument("--output", type=Path,
                        help="optional output JSON path")
    parser.add_argument("--bootstrap", type=int, default=3000)
    args = parser.parse_args()
    with args.input.open("r", encoding="utf-8-sig", newline="") as f:
        result = summarize_trials(
            parse_trials(f), bootstrap_repetitions=args.bootstrap
        )
    payload = json.dumps(result, indent=2, ensure_ascii=False)+"\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
