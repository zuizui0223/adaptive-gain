"""Reproduce partial-identification bounds from bee active-information trials.

Source: He et al. 2026 preprint DOI 10.64898/2026.09.15.751944.
Pinned GitHub data:
https://github.com/Cuixiaojian21/bee_metacognition/blob/7f886394b4de872ecdb19ca4ea214ec321d5dce9/data/4_active_information_seeking_trials.csv
Git blob 26259c9071c6d73141d56b9bedd396cab1a04491.

This script reads a LOCAL copy of the public original file; it does not
ship third-party data. Regular-trial REQUEST is actual platform landing.
Free-Cue has auto-delivered information and must not enter REQUEST bounds.
The bounds measure nonidentification of a causal effect of voluntary
information purchase on CORRECTNESS, not true ecological fitness.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from adaptive_gain.partial_identification import binary_action_accuracy_bounds

DIFFICULTIES = ("Easy", "Hard", "Impossible")
REQUIRED = {
    "Trial_ID", "Bee_ID", "Difficulty", "Trial_Type", "Info_Requested",
    "Actually_Landed_On_Platform", "Is_Post_Request_Correct",
    "Is_Post_Non_Request_Correct",
}
SOURCE_COMMIT = "7f886394b4de872ecdb19ca4ea214ec321d5dce9"
SOURCE_BLOB_SHA = "26259c9071c6d73141d56b9bedd396cab1a04491"


def parse_binary(raw: str, name: str) -> int:
    if raw not in ("0", "1", "0.0", "1.0"):
        raise ValueError(f"{name} is not binary: {raw!r}")
    return int(float(raw))


def source_outcome_counts(handle) -> dict:
    reader = csv.DictReader(handle)
    if not REQUIRED.issubset(reader.fieldnames or []):
        raise ValueError("required columns missing")
    trials = set()
    groups = {
        d: {
            "n_regular": 0,
            "request_correct": 0, "request_wrong": 0,
            "no_request_correct": 0, "no_request_wrong": 0,
            "n_free": 0, "free_correct": 0,
        }
        for d in DIFFICULTIES
    }
    for row in reader:
        tid = row["Trial_ID"]
        if tid in trials:
            raise ValueError("duplicate Trial_ID")
        trials.add(tid)
        if row["Difficulty"] not in DIFFICULTIES:
            raise ValueError("unknown task difficulty")
        z = groups[row["Difficulty"]]
        label = row["Trial_Type"]
        landed = parse_binary(row["Actually_Landed_On_Platform"], "landing")
        info = parse_binary(row["Info_Requested"], "delivery/request")
        post = row["Is_Post_Request_Correct"]
        non = row["Is_Post_Non_Request_Correct"]
        if (post != "") == (non != ""):
            raise ValueError("exactly one correctness field must be present")
        correct = parse_binary(post if post != "" else non, "correct")
        if label == "Regular":
            if info != landed:
                raise ValueError("Regular request/landing mismatch")
            if (post != "") != bool(landed):
                raise ValueError("Regular outcome is not in correct branch")
            z["n_regular"] += 1
            field = (
                ("request_" if landed else "no_request_")
                + ("correct" if correct else "wrong")
            )
            z[field] += 1
        elif label == "Random_Free_Cue":
            if info != 1 or post == "":
                raise ValueError("Free-Cue should indicate delivered post cue")
            z["n_free"] += 1
            z["free_correct"] += correct
        else:
            raise ValueError("unknown trial type")
    return groups


def analyze(groups: dict) -> dict:
    result = {}
    for d in DIFFICULTIES:
        g = groups[d]
        n = g["n_regular"]
        if n <= 0:
            raise ValueError(f"no Regular trials for {d}")
        bounds = binary_action_accuracy_bounds(
            action_success=g["request_correct"],
            action_failure=g["request_wrong"],
            no_action_success=g["no_request_correct"],
            no_action_failure=g["no_request_wrong"],
        )
        if bounds.n != n:
            raise ValueError(f"inconsistent Regular counts for {d}")
        nfree = g["n_free"]
        result[d] = {
            **g,
            "n_request": bounds.action_count,
            "n_no_request": bounds.no_action_count,
            "observed_request_accuracy": bounds.observed_action_success_rate,
            "observed_no_request_accuracy": bounds.observed_no_action_success_rate,
            "naive_conditional_accuracy_difference": bounds.naive_conditional_difference,
            "sharp_ate_lower": bounds.ate_lower,
            "sharp_ate_upper": bounds.ate_upper,
            "observed_free_accuracy": g["free_correct"]/nfree if nfree else None,
            "observed_regular_overall_accuracy": (
                g["request_correct"] + g["no_request_correct"]
            )/n,
            "free_minus_regular_overall_accuracy_descriptive": (
                g["free_correct"]/nfree
                - (g["request_correct"] + g["no_request_correct"])/n
                if nfree else None
            ),
        }
    return {
        "source_commit": SOURCE_COMMIT,
        "source_blob_sha": SOURCE_BLOB_SHA,
        "regular_trials_by_difficulty": result,
        "status": "PARTIAL_IDENTIFICATION_SIGN_UNRESOLVED_IN_ALL_THREE_DIFFICULTIES",
        "claim_ceiling": (
            "No causal point estimate for the effect of self-selected "
            "information requests, no Blackwell precision ordering, "
            "no dynamic environmental state or fitness effect."
        ),
    }


def verify_against_receipt(current: dict, receipt: dict):
    for difficulty in DIFFICULTIES:
        actual = current["regular_trials_by_difficulty"][difficulty]
        old = receipt["regular_trials_by_difficulty"][difficulty]
        for k, value in actual.items():
            if k not in old:
                raise ValueError(f"missing frozen field {difficulty}/{k}")
            if old[k] != value:
                raise ValueError(f"frozen receipt differs: {difficulty}/{k}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify-receipt", type=Path)
    args = parser.parse_args()
    with args.input.open("r", encoding="utf-8-sig", newline="") as f:
        out = analyze(source_outcome_counts(f))
    if args.verify_receipt is not None:
        frozen = json.loads(args.verify_receipt.read_text(encoding="utf-8"))
        verify_against_receipt(out, frozen)
    serialized = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()
