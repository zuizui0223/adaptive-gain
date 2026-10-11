"""Audited randomized-offer benchmark from 2026 bumble bee trial outcomes.

Source: He et al. (2026), "Uncertainty-Guided Decision-Making in
Bumble Bees", bioRxiv DOI 10.64898/2026.09.15.751944.
Pinned raw data (NOT redistributed):
https://github.com/Cuixiaojian21/bee_metacognition/blob/7f886394b4de872ecdb19ca4ea214ec321d5dce9/data/4_active_information_seeking_trials.csv
Git blob: 26259c9071c6d73141d56b9bedd396cab1a04491.

Estimand: correctness when the experiment AUTOMATICALLY presents a
predictive free cue (Random_Free_Cue) versus normal optional request
policy (Regular), WITHIN difficulty.

The authors say Free-Cue trials were randomly interleaved in 20% of
trials. If assignment was as described and properly concealed, the
difference can be interpreted as an intention-to-treat effect of this
WHOLE trial condition, not the effect of voluntary purchase or the
information itself at fixed sensory, reward, motor and timing contexts.

This is an exploratory independent reanalysis, not an evolutionary
adaptivity advantage and not a novel phenomenon established here.
No per-trial decision-time outcome is available in THIS experiment.

Standard library only. Source bytes remain at the authors' repository.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

SOURCE_COMMIT = "7f886394b4de872ecdb19ca4ea214ec321d5dce9"
SOURCE_BLOB_SHA = "26259c9071c6d73141d56b9bedd396cab1a04491"
SOURCE_PATH = "data/4_active_information_seeking_trials.csv"
DIFFICULTIES = ("Easy", "Hard", "Impossible")
REQUIRED_COLUMNS = {
    "Trial_ID", "Bee_ID", "Trial_Number", "Difficulty", "Trial_Type",
    "Info_Requested", "Actually_Landed_On_Platform",
    "Is_Post_Request_Correct", "Is_Post_Non_Request_Correct",
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
    ).hexdigest()


def parse_trials(handle) -> dict[str, list[dict]]:
    reader = csv.DictReader(handle)
    if not REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
        raise ValueError("required columns missing")
    bees = {}
    ids = set()
    ordinal_ids = set()
    for r in reader:
        identifier = r["Trial_ID"]
        bee = r["Bee_ID"]
        trial = int(r["Trial_Number"])
        key = (bee, trial)
        if not identifier or not bee or identifier in ids or key in ordinal_ids:
            raise ValueError("missing/duplicate trial key")
        ids.add(identifier)
        ordinal_ids.add(key)
        if not 1 <= trial <= 100:
            raise ValueError("expected 100-trial source design")
        if r["Difficulty"] not in DIFFICULTIES:
            raise ValueError("invalid difficulty")
        typ = r["Trial_Type"]
        if typ not in ("Regular", "Random_Free_Cue"):
            raise ValueError("invalid trial type")
        landing, info = r["Actually_Landed_On_Platform"], r["Info_Requested"]
        if landing not in ("0", "1") or info not in ("0", "1"):
            raise ValueError("landing/delivery must be binary")
        post, non = r["Is_Post_Request_Correct"], r["Is_Post_Non_Request_Correct"]
        if (post != "") == (non != ""):
            raise ValueError("exactly one correctness field must be observed")
        if typ == "Regular":
            if landing != info or (post != "") != (landing == "1"):
                raise ValueError("Regular request/landing/outcome inconsistency")
        else:
            if info != "1" or post == "":
                raise ValueError("Free-Cue is automatic delivery, not voluntary action")
        observed = post if post != "" else non
        if observed not in ("0", "1", "0.0", "1.0"):
            raise ValueError("invalid correctness outcome")
        bees.setdefault(bee, []).append({
            "trial": trial,
            "difficulty": r["Difficulty"],
            "free": int(typ == "Random_Free_Cue"),
            "landed": int(landing),
            "correct": int(float(observed)),
        })
    for arr in bees.values():
        arr.sort(key=lambda x: x["trial"])
    return bees


def empty():
    return {"n": 0, "correct": 0, "landing": 0}


def add(dst, r):
    dst["n"] += 1
    dst["correct"] += r["correct"]
    dst["landing"] += r["landed"]


def rate(g):
    return g["correct"] / g["n"] if g["n"] else None


def contrasts(clusters: list[tuple[str, list[dict]]]):
    groups = {d: [empty(), empty()] for d in DIFFICULTIES}
    paired = {d: [] for d in DIFFICULTIES}
    paired_signs = {}
    for bee, trials in clusters:
        cell = {d: [empty(), empty()] for d in DIFFICULTIES}
        for r in trials:
            add(cell[r["difficulty"]][r["free"]], r)
        for d in DIFFICULTIES:
            for z in (0, 1):
                g, local = groups[d][z], cell[d][z]
                for key in ("n", "correct", "landing"):
                    g[key] += local[key]
            a, b = cell[d]
            if a["n"] and b["n"]:
                paired[d].append(rate(b) - rate(a))
    output = {}
    for d in DIFFICULTIES:
        regular, free = groups[d]
        if not regular["n"] or not free["n"]:
            raise ValueError(f"empty Regular or Free-Cue outcome cell: {d}")
        values = paired[d]
        output[d] = {
            "regular": regular,
            "free": free,
            "regular_accuracy": rate(regular),
            "free_accuracy": rate(free),
            "free_minus_regular_accuracy": rate(free) - rate(regular),
            "within_bee_paired_mean": (
                sum(values) / len(values) if values else None
            ),
            "paired_bees": len(values),
            "paired_bee_signs": {
                "positive": sum(v > 0 for v in values),
                "negative": sum(v < 0 for v in values),
                "zero": sum(v == 0 for v in values),
            },
        }
    return output


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


def bounds(values: list[float]) -> list[float]:
    if not values:
        raise ValueError("no bootstrap values")
    a = sorted(values)
    return [a[int(.025 * len(a))], a[int(.975 * len(a))]]


def analyze(bees: dict[str, list[dict]], *,
            bootstrap_repetitions: int = 3000,
            seed: int = 0x7A4408) -> dict:
    if not bees or bootstrap_repetitions < 1:
        raise ValueError("nonempty source and positive bootstrap count required")
    clusters = sorted(bees.items())
    expected = contrasts(clusters)
    draws = {d: {"trial_weighted": [], "bee_paired": []} for d in DIFFICULTIES}
    random = xorshift32(seed)
    for _ in range(bootstrap_repetitions):
        selected = [
            clusters[int(next(random) * len(clusters))]
            for _ in clusters
        ]
        result = contrasts(selected)
        for d in DIFFICULTIES:
            draws[d]["trial_weighted"].append(
                result[d]["free_minus_regular_accuracy"]
            )
            if result[d]["within_bee_paired_mean"] is not None:
                draws[d]["bee_paired"].append(
                    result[d]["within_bee_paired_mean"]
                )
    for d in DIFFICULTIES:
        expected[d]["bee_cluster_bootstrap_95"] = bounds(
            draws[d]["trial_weighted"]
        )
        expected[d]["paired_bee_bootstrap_95"] = bounds(
            draws[d]["bee_paired"]
        )
    landing_check = free_arm_landing_accuracy_audit(
        clusters, bootstrap_repetitions=bootstrap_repetitions
    )

    trial_order = {}
    for b in range(5):
        a, end = b * 20 + 1, (b + 1) * 20
        by_difficulty = {}
        for d in DIFFICULTIES:
            g = [empty(), empty()]
            for _, ar in clusters:
                for row in ar:
                    if a <= row["trial"] <= end and row["difficulty"] == d:
                        add(g[row["free"]], row)
            if not g[0]["n"] or not g[1]["n"]:
                raise ValueError(f"empty trial-order bin {b} difficulty {d}")
            by_difficulty[d] = {
                "n_regular": g[0]["n"], "n_free": g[1]["n"],
                "free_minus_regular_accuracy": rate(g[1]) - rate(g[0]),
            }
        trial_order[f"{a}-{end}"] = by_difficulty

    precondition = {d: [empty(), empty()] for d in DIFFICULTIES}
    # Negative-control descriptive balance: assignment of current Free cue
    # against correctness on preceding trial, which has already occurred.
    for _, ar in clusters:
        for old, new in zip(ar, ar[1:]):
            if new["trial"] != old["trial"] + 1:
                continue
            group = precondition[new["difficulty"]][new["free"]]
            group["n"] += 1
            group["correct"] += old["correct"]
    previous_outcome_balance = {}
    for d in DIFFICULTIES:
        regular, free = precondition[d]
        previous_outcome_balance[d] = {
            "n_previous_before_regular": regular["n"],
            "n_previous_before_free": free["n"],
            "previous_correct_free_minus_regular": rate(free) - rate(regular),
        }

    free_hist = {}
    for _, ar in clusters:
        nfree = sum(x["free"] for x in ar)
        free_hist[str(nfree)] = free_hist.get(str(nfree), 0) + 1

    return {
        "schema": "adaptive-gain-bee-2026-random-free-cue-offer-accuracy-v1",
        "source": {
            "repository": "Cuixiaojian21/bee_metacognition",
            "commit": SOURCE_COMMIT,
            "path": SOURCE_PATH,
            "blob_sha": SOURCE_BLOB_SHA,
        },
        "n_bees": len(bees),
        "n_trials": sum(len(x) for _, x in clusters),
        "free_cue_trials_per_bee_histogram": free_hist,
        "accuracy_by_difficulty": expected,
        "free_arm_landing_accuracy_control": landing_check,
        "trial_order_20_bins": trial_order,
        "negative_control_previous_correctness": previous_outcome_balance,
        "uncertainty_method": (
            f"bee-cluster bootstrap B={bootstrap_repetitions}; "
            f"xorshift32 seed={seed} (0x{seed:x}); "
            "percentiles 2.5/97.5"
        ),
        "assignment_contract": (
            "Source preprint describes interleaved Random_Free_Cue trials "
            "on 20 percent of each bee's trials; complete randomization "
            "protocol/sequence generation was not independently audited."
        ),
        "estimand": (
            "Outcome difference for assignment to automatically delivered "
            "predictive Free-Cue trial versus Regular optional-query trial, "
            "within task difficulty; NOT the causal effect of voluntarily "
            "requesting a cue nor information-only effect at fixed "
            "timing/reward/salience."
        ),
        "status": "DESCRIPTIVE_RANDOM_FREE_CUE_POLICY_CONTRAST__CAUSAL_ITT_CONDITIONAL_ON_REPORTED_RANDOMIZATION",
        "claim_ceiling": (
            "Random assignment, if implemented as described, supports a "
            "trial-condition intention-to-treat accuracy effect. Free-Cue "
            "changes cue delivery, timing/salience and potentially "
            "reward/cue approach behavior together; do not label its "
            "difference a pure information-value or evolutionary "
            "adaptive-gain selection coefficient."
        ),
    }



def free_arm_landing_accuracy_audit(
    clusters: list[tuple[str, list[dict]]], *,
    bootstrap_repetitions: int = 3000,
    seed: int = 0x5C29E3,
) -> dict:
    """Within automatically informed trials, compare LANDING groups.

    Information is automatically delivered in every Free-Cue trial.
    Platform landing is still self-selected. This is a negative-control
    style DESCRIPTIVE check for possible motor/attention associations,
    NOT the causal effect of landing or a time-matched sham trial.
    """
    if bootstrap_repetitions < 1:
        raise ValueError("bootstrap_repetitions must be positive")

    def per_group(sample):
        result = {
            d: [empty(), empty()] for d in DIFFICULTIES
        }
        for _, arr in sample:
            for r in arr:
                if r["free"]:
                    add(result[r["difficulty"]][r["landed"]], r)
        return result

    by_diff = per_group(clusters)
    rng = xorshift32(seed)
    sampled_effects = {d: [] for d in DIFFICULTIES}
    for _ in range(bootstrap_repetitions):
        sampled = [
            clusters[int(next(rng) * len(clusters))]
            for _ in clusters
        ]
        group = per_group(sampled)
        for d in DIFFICULTIES:
            no_land, land = group[d]
            if land["n"] and no_land["n"]:
                sampled_effects[d].append(rate(land) - rate(no_land))
    output = {}
    for d in DIFFICULTIES:
        no_land, land = by_diff[d]
        if not land["n"] or not no_land["n"] or not sampled_effects[d]:
            raise ValueError(f"missing Free-Cue landing subgroup {d}")
        output[d] = {
            "free_landed": land,
            "free_not_landed": no_land,
            "accuracy_if_landed": rate(land),
            "accuracy_if_not_landed": rate(no_land),
            "landing_minus_no_landing": rate(land) - rate(no_land),
            "bee_cluster_bootstrap_95": bounds(sampled_effects[d]),
        }
    return {
        "by_difficulty": output,
        "method": (
            f"Free-Cue arm only, all automatically receive predictive signal; "
            f"bee-cluster bootstrap B={bootstrap_repetitions}; "
            f"xorshift32 seed={seed} (0x{seed:x})"
        ),
        "status": "SELF_SELECTED_FREE_CUE_LANDING_ASSOCIATION_NOT_MOTOR_CAUSAL_EFFECT",
    }


def verify_receipt(result: dict, frozen: dict, tol: float = 1e-9):
    if result["source"] != frozen["source"]:
        raise ValueError("source pinned identity differs")
    if result["n_trials"] != frozen["n_trials"] or result["n_bees"] != frozen["n_bees"]:
        raise ValueError("trial/bee counts differ")
    for d in DIFFICULTIES:
        r, f = result["accuracy_by_difficulty"][d], frozen["accuracy_by_difficulty"][d]
        for name in ("free_minus_regular_accuracy", "within_bee_paired_mean",
                     "bee_cluster_bootstrap_95", "paired_bee_bootstrap_95"):
            a, b = r[name], f[name]
            if isinstance(a, list):
                if len(a) != len(b) or any(abs(x-y) > tol for x, y in zip(a,b)):
                    raise ValueError(f"frozen interval differs {d} {name}")
            elif abs(a-b) > tol:
                raise ValueError(f"frozen effect differs {d} {name}")
        control_a = result["free_arm_landing_accuracy_control"]["by_difficulty"][d]
        control_b = frozen["free_arm_landing_accuracy_control"]["by_difficulty"][d]
        for name in ("landing_minus_no_landing", "bee_cluster_bootstrap_95"):
            a, b = control_a[name], control_b[name]
            if isinstance(a, list):
                if len(a) != len(b) or any(abs(x-y) > tol for x,y in zip(a,b)):
                    raise ValueError(f"frozen landing control differs {d} {name}")
            elif abs(a-b) > tol:
                raise ValueError(f"frozen landing control differs {d} {name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify-receipt", type=Path)
    parser.add_argument("--verify-source-blob", action="store_true")
    parser.add_argument("--bootstrap", type=int, default=3000)
    options = parser.parse_args()
    if options.verify_source_blob:
        current = git_blob_sha(options.input.read_bytes())
        if current != SOURCE_BLOB_SHA:
            raise ValueError(
                f"source Git blob mismatch: expected {SOURCE_BLOB_SHA}, observed {current}"
            )
    with options.input.open("r", encoding="utf-8-sig", newline="") as handle:
        bees = parse_trials(handle)
    outcome = analyze(bees, bootstrap_repetitions=options.bootstrap)
    if options.verify_receipt:
        frozen = json.loads(options.verify_receipt.read_text(encoding="utf-8"))
        verify_receipt(outcome, frozen)
    payload = json.dumps(outcome, ensure_ascii=False, indent=2) + "\n"
    if options.output:
        options.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
