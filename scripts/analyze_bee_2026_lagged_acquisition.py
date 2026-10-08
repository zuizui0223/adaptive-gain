"""Exploratory one-trial lag audit of public 2026 bumblebee cue requests.

Pinned He et al. (2026) active information seeking trial data:
https://github.com/Cuixiaojian21/bee_metacognition/blob/7f886394b4de872ecdb19ca4ea214ec321d5dce9/data/4_active_information_seeking_trials.csv
Git blob SHA 26259c9071c6d73141d56b9bedd396cab1a04491.

Trial_Number is used ONLY within this active-information experiment. It must
not be matched to the separate metacognition decision-latency experiment.

Outcome correctness is structurally recorded in exactly one of the
Post_Request and Post_Non_Request columns. In Random_Free_Cue conditions
Info_Requested indicates information delivery, not a voluntary request.

Estimand: among pairs of consecutive *Regular* trials in the same bee,
the descriptive difference in current voluntary platform-landing rate
after a wrong versus correct preceding decision. Report crude and a
stratified version holding fixed preceding task difficulty, preceding
request behavior, and current within-bee 20-trial order bin. The current
difficulty is analyzed separately. Cluster bootstrap bees (not trials).

This is NOT a causal trial-history effect: error is not randomized,
unmeasured motivation may confound the lag, and a binning/stratification
choice cannot fix that. Zero-cover strata are omitted from standardization.
No source raw data are redistributed by adaptive-gain.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

DIFFICULTIES = ("Easy", "Hard", "Impossible")
TRIAL_TYPES = ("Regular", "Random_Free_Cue")
SOURCE_REPOSITORY = "Cuixiaojian21/bee_metacognition"
SOURCE_COMMIT = "7f886394b4de872ecdb19ca4ea214ec321d5dce9"
SOURCE_BLOB_SHA = "26259c9071c6d73141d56b9bedd396cab1a04491"
SOURCE_PATH = "data/4_active_information_seeking_trials.csv"
REQUIRED = {
    "Bee_ID", "Trial_Number", "Difficulty", "Trial_Type",
    "Info_Requested", "Actually_Landed_On_Platform",
    "Is_Post_Request_Correct", "Is_Post_Non_Request_Correct",
}


def _binary(raw: str, field: str) -> int:
    if raw not in ("0", "1", "0.0", "1.0"):
        raise ValueError(f"{field} must be binary, got {raw!r}")
    return int(float(raw))


def parse_rows(handle) -> dict[str, list[dict]]:
    reader = csv.DictReader(handle)
    if not REQUIRED.issubset(reader.fieldnames or []):
        raise ValueError(f"missing required fields: {sorted(REQUIRED-set(reader.fieldnames or []))}")
    bees: dict[str, list[dict]] = {}
    keys = set()
    for row in reader:
        bee = row["Bee_ID"]
        if not bee:
            raise ValueError("blank Bee_ID")
        trial = int(row["Trial_Number"])
        if trial < 1:
            raise ValueError("Trial_Number must be positive")
        key = (bee, trial)
        if key in keys:
            raise ValueError("duplicate Bee_ID / Trial_Number within experiment")
        keys.add(key)
        d, typ = row["Difficulty"], row["Trial_Type"]
        if d not in DIFFICULTIES or typ not in TRIAL_TYPES:
            raise ValueError("unexpected difficulty or trial type")
        land = _binary(row["Actually_Landed_On_Platform"], "landing")
        info = _binary(row["Info_Requested"], "information delivery/request")
        post, non = row["Is_Post_Request_Correct"], row["Is_Post_Non_Request_Correct"]
        if (post != "") == (non != ""):
            raise ValueError("post and non-request outcomes must be exclusive")
        if typ == "Regular":
            if land != info:
                raise ValueError("Regular information request/landing mismatch")
            if (post != "") != bool(land):
                raise ValueError("Regular outcome must correspond to request")
        else:
            if info != 1 or post == "":
                raise ValueError("Free-Cue trials must be delivery and post outcome")
        correct = _binary(post if post != "" else non, "correctness")
        bees.setdefault(bee, []).append({
            "trial": trial, "difficulty": d, "type": typ,
            "landing": land, "correct": correct,
        })
    for v in bees.values():
        v.sort(key=lambda r: r["trial"])
    return bees


def lag_pairs(bees: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Only consecutive Regular -> Regular pairs, never cross experiments."""
    result = {}
    for bee, rows in bees.items():
        matches = []
        for prev, now in zip(rows, rows[1:]):
            if now["trial"] != prev["trial"] + 1:
                continue
            if prev["type"] != "Regular" or now["type"] != "Regular":
                continue
            matches.append({
                "bee": bee,
                "y": now["landing"],
                "prior_fail": 1 - prev["correct"],
                "cur_diff": now["difficulty"],
                "prev_diff": prev["difficulty"],
                "prev_request": prev["landing"],
                "bin": (now["trial"] - 1) // 20,
            })
        result[bee] = matches
    return result


def difference(rows: list[dict], difficulty: str, *, adjusted: bool) -> dict:
    if difficulty not in DIFFICULTIES:
        raise ValueError("unknown difficulty")
    strata = {}
    for r in rows:
        if r["cur_diff"] != difficulty:
            continue
        key = ((r["prev_diff"], r["prev_request"], r["bin"])
               if adjusted else ("all",))
        counts = strata.setdefault(key, [[0, 0], [0, 0]])
        outcome_index = r["prior_fail"]
        counts[outcome_index][0] += 1
        counts[outcome_index][1] += r["y"]
    weighted = 0.0
    total_weight = 0
    included_strata = 0
    for counts in strata.values():
        success_n, success_y = counts[0]
        failure_n, failure_y = counts[1]
        if not success_n or not failure_n:
            continue
        weight = success_n + failure_n
        weighted += weight * (failure_y / failure_n - success_y / success_n)
        total_weight += weight
        included_strata += 1
    return {
        "fail_minus_success": weighted / total_weight if total_weight else None,
        "included_strata": included_strata,
        "covered_trials": total_weight,
    }


def xorshift32(seed: int):
    state = seed & 0xFFFFFFFF
    if not state:
        raise ValueError("seed must be nonzero")
    while True:
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= state >> 17
        state ^= (state << 5) & 0xFFFFFFFF
        state &= 0xFFFFFFFF
        yield state / 4294967296


def percentile(values: list[float], p: float) -> float:
    if not values or not 0 <= p <= 1:
        raise ValueError("invalid percentile")
    ordered = sorted(values)
    return ordered[min(len(ordered)-1, math.floor(p * len(ordered)))]


def summarize(
    bees: dict[str, list[dict]], *,
    bootstrap_reps: int = 1500, seed: int = 0x5EEC23
) -> dict:
    if bootstrap_reps < 1:
        raise ValueError("bootstrap_reps must be positive")
    pairs = lag_pairs(bees)
    ids = sorted(bees)
    if not ids:
        raise ValueError("no bees")
    clusters = [pairs[bee] for bee in ids]
    all_rows = [x for cluster in clusters for x in cluster]
    generator = xorshift32(seed)
    findings = {}
    for difficulty in DIFFICULTIES:
        raw = difference(all_rows, difficulty, adjusted=False)
        adjusted = difference(all_rows, difficulty, adjusted=True)
        boot = []
        for _ in range(bootstrap_reps):
            resample = []
            for _ in clusters:
                idx = int(next(generator) * len(clusters))
                resample.extend(clusters[idx])
            fitted = difference(resample, difficulty, adjusted=True)
            if fitted["fail_minus_success"] is not None:
                boot.append(fitted["fail_minus_success"])
        if not boot:
            raise ValueError("no bootstrap strata with both preceding outcomes")
        findings[difficulty] = {
            "raw_fail_minus_success": raw["fail_minus_success"],
            "stratified_fail_minus_success": adjusted["fail_minus_success"],
            "included_strata": adjusted["included_strata"],
            "covered_trials": adjusted["covered_trials"],
            "bee_cluster_bootstrap_95": [
                percentile(boot, .025), percentile(boot, .975)
            ],
            "bootstrap_valid_repetitions": len(boot),
        }
    return {
        "schema": "adaptive-gain-bee-2026-one-trial-lag-v1",
        "source": {
            "repository": SOURCE_REPOSITORY,
            "commit": SOURCE_COMMIT,
            "blob_sha": SOURCE_BLOB_SHA,
            "path": SOURCE_PATH,
        },
        "n_bees": len(bees),
        "n_total_trials": sum(len(x) for x in bees.values()),
        "regular_following_regular_pairs": len(all_rows),
        "difficulty": findings,
        "method": (
            "Previous Regular trial correctness versus next Regular trial "
            "platform landing, by next difficulty; adjusted standardization "
            "over preceding difficulty, preceding request, next trial bin "
            "(20-trial quintile), weighted by eligible stratum size. "
            f"Bee cluster bootstrap B={bootstrap_reps}, xorshift32 seed={seed}."
        ),
        "status": "EXPLORATORY_SEQUENCE_ASSOCIATION_NO_CAUSAL_HISTORY_EFFECT",
        "claim_ceiling": (
            "Outcomes were not randomized. Zero-containing strata are excluded "
            "from weighted contrasts. Unmeasured animal state/selection can "
            "confound lagged failures. Confidence intervals covering zero "
            "cannot prove absence of feedback learning or longer memory. "
            "Task-specific IDs cannot be joined to separate latency trials."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bootstrap", type=int, default=1500)
    args = parser.parse_args()
    with args.input.open("r", encoding="utf-8-sig", newline="") as f:
        result = summarize(parse_rows(f), bootstrap_reps=args.bootstrap)
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(output, end="")
    else:
        args.output.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
