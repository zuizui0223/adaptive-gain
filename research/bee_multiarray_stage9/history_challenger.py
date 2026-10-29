"""Stage9b: test external turn rule beyond early-train first-order bee history.

This is a post-hoc challenger to Stage9, not independent causal evidence.
Original source data are ephemeral GitHub Actions inputs, not shipped here.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import math
import random

from external_turn_transfer import (
    ALTERNATIVES, FROZEN_EXTERNAL_KAPPA, MIN_BEE_TRIPLETS,
    MIN_BEES_PER_ARRAY, MIN_TEST_TRIPLETS_PER_ARRAY,
    MIN_EXCHANGEABLE_TRIPLETS, MIN_EXCHANGEABLE_BEES,
    MIN_PERMUTABLE_PER_BEE, SEED, PERMUTATIONS,
    static_prior, geo_destination_probs, directed_destination_probs,
)

BETA = 5.0  # Frozen from independent Pasquaretta 2019 Stage 5.
EXPECTED_ARRAY_TRIPLETS = {"1": 608, "2": 687, "3": 663}
RECONCILIATION_TOL = 1e-9


def history_destination_probs(geo, transitions, b, beta=BETA):
    """Train-only B->C switched Markov counts shrunk to four-flower Mgeo."""
    if beta != BETA:
        raise ValueError("NO_GO_HISTORY_BETA_WAS_RETUNED")
    if b in geo or set(geo) != set(ALTERNATIVES) - {b}:
        raise ValueError("NO_GO_WRONG_REAL_SOURCE_ALTERNATIVES")
    if any((not isinstance(v, int)) or v < 0 for v in transitions.values()):
        raise ValueError("NO_GO_INVALID_TRAIN_COUNTS")
    if any(not 0 < v < 1 or not math.isfinite(v) for v in geo.values()):
        raise ValueError("NO_GO_NONFINITE_GEOMETRY_BASELINE")
    if abs(sum(geo.values()) - 1.0) > 1e-10:
        raise ValueError("NO_GO_UNNORMALIZED_GEOMETRY_BASELINE")
    n = sum(transitions.get((b, c), 0) for c in geo)
    p = {c: (transitions.get((b, c), 0) + BETA * geo[c]) / (n + BETA)
         for c in geo}
    if not all(0 < v < 1 for v in p.values()) or abs(sum(p.values()) - 1) > 1e-10:
        raise ValueError("NO_GO_UNNORMALIZED_HISTORY_MODEL")
    return p


def _mean(xs):
    if not xs:
        raise ValueError("NO_GO_EMPTY_GENUINE_SOURCE_SUMMARY")
    return sum(xs) / len(xs)


def _coarse_means(rows, field):
    by_colony = defaultdict(list)
    for r in rows:
        by_colony[r["colony"]].append(r[field])
    return {k: _mean(v) for k, v in sorted(by_colony.items())}


def _per_bee_components(population, coords, lambdas):
    scores = defaultdict(list)
    events = defaultdict(list)
    for key, data in sorted(population.items()):
        colony, bee, array = key
        triples = data["test_triplets"]
        if len(triples) < MIN_BEE_TRIPLETS:
            continue  # EXACT parent Stage9 source eligibility, not retuned.
        prior = static_prior(data["train_visits"])
        transitions = Counter(data["train_switch_pairs"])
        losses = defaultdict(float)
        for e in triples:
            a, b, c = e["a"], e["b"], e["c"]
            geo = geo_destination_probs(prior, coords[array], b, lambdas[array])
            history = history_destination_probs(geo, transitions, b)
            turn = directed_destination_probs(geo, coords[array], a, b,
                                              FROZEN_EXTERNAL_KAPPA)
            history_turn = directed_destination_probs(history, coords[array], a, b,
                                                      FROZEN_EXTERNAL_KAPPA)
            ps = {"Mgeo": geo, "Mturn": turn,
                  "Mhistory": history, "Mhistory_turn": history_turn}
            for name, p in ps.items():
                losses[name] -= math.log(p[c])
            events[array].append({
                "colony": colony, "bee": bee,
                "a": a, "b": b, "c": c,
                # ephemeral true triplets: NEVER included in artifact JSON
                "geo": geo, "history": history,
            })
        n = len(triples)
        row = {"colony": colony, "bee": bee, "array": array,
               "source_genuine_heldout_triplets": n,
               "train_switch_pairs": len(data["train_switch_pairs"]),
               "train_bout_max": data["train_source_max_bout"],
               "test_bout_min": data["test_source_min_bout"]}
        for name in ("Mgeo", "Mturn", "Mhistory", "Mhistory_turn"):
            row[name + "_nll"] = losses[name] / n
        row["direction_over_geo"] = row["Mgeo_nll"] - row["Mturn_nll"]
        row["history_over_geo"] = row["Mgeo_nll"] - row["Mhistory_nll"]
        row["direction_over_history"] = row["Mhistory_nll"] - row["Mhistory_turn_nll"]
        row["history_over_direction"] = row["Mturn_nll"] - row["Mhistory_turn_nll"]
        if row["train_bout_max"] > 15 or row["test_bout_min"] < 16:
            raise ValueError("NO_GO_SOURCE_EARLY_LATE_LEAKAGE")
        scores[array].append(row)
    return scores, events


def _check_parent_source(parent, array, rows):
    original = parent["original_heldout_comparisons_by_array"][array]
    if original["status"] != "HELDOUT_TEST_SUPPORT_PASS":
        raise ValueError("NO_GO_PARENT_ARRAY_SOURCE_SUPPORT")
    target = {
        "bee_equal_Mgeo_nll": _mean([r["Mgeo_nll"] for r in rows]),
        "bee_equal_Mexternalkappa1_nll": _mean([r["Mturn_nll"] for r in rows]),
        "bee_equal_external_direction_gain_nats": _mean([r["direction_over_geo"] for r in rows]),
    }
    for k, value in target.items():
        if abs(original[k] - value) > RECONCILIATION_TOL:
            raise ValueError("NO_GO_PARENT_DIRECTION_SCORE_CHANGED " + k)
    if original["qualifying_original_individuals"] != len(rows):
        raise ValueError("NO_GO_PARENT_BEE_COUNT_CHANGED")
    if original["original_source_test_genuine_triplets"] != sum(
            x["source_genuine_heldout_triplets"] for x in rows):
        raise ValueError("NO_GO_PARENT_TRIPLET_COUNT_CHANGED")
    previous = {(x["colony"], x["bee"]): x for x in original["source_bee_scores"]}
    for x in rows:
        baseline = previous.get((x["colony"], x["bee"]))
        if baseline is None or abs(baseline["Mgeo_nll"] - x["Mgeo_nll"]) > RECONCILIATION_TOL or abs(
                baseline["Mexternal_direction_nll"] - x["Mturn_nll"]) > RECONCILIATION_TOL:
            raise ValueError("NO_GO_PARENT_PER_BEE_DIRECTION_SCORE_CHANGED")
    return True


def conditional_permutation(events, coords, permutations=PERMUTATIONS, seed=SEED):
    """Shuffle true incoming A within bee×B×array without changing any B,C."""
    rng = random.Random(seed)
    results = {}
    for array in ("1", "2", "3"):
        rows = events[array]
        by_b = defaultdict(list)
        for i, r in enumerate(rows):
            by_b[(r["colony"], r["bee"], r["b"])].append(i)
        eligible = set()
        for inds in by_b.values():
            if len(inds) > 1 and len({rows[i]["a"] for i in inds}) > 1:
                eligible.update(inds)
        bee_counts = Counter((rows[i]["colony"], rows[i]["bee"]) for i in eligible)
        gate = len(eligible) >= MIN_EXCHANGEABLE_TRIPLETS and sum(
            v >= MIN_PERMUTABLE_PER_BEE for v in bee_counts.values()) >= MIN_EXCHANGEABLE_BEES
        receipt = {"qualifying_exchangeable_events": len(eligible),
                   "bees_with_ge5_exchangeable": sum(
                       v >= MIN_PERMUTABLE_PER_BEE for v in bee_counts.values()),
                   "original_heldout_triplets": len(rows),
                   "permutations": permutations, "seed": seed}
        if not gate:
            receipt["status"] = "NO_GO_CONDITIONAL_SHUFFLE_SUPPORT"
            results[array] = receipt
            continue
        perbee = defaultdict(list)
        for i, r in enumerate(rows):
            perbee[(r["colony"], r["bee"])].append(i)
        percolony = defaultdict(list)
        for col, bee in perbee:
            percolony[col].append(bee)
        if len(percolony) != 2:
            raise ValueError("NO_GO_NOT_TWO_ORIGINAL_SOURCE_COLONIES")
        def gain_for_labels(labels):
            bee_gains = {}
            for (col, bee), indices in perbee.items():
                scores = []
                for i in indices:
                    e = rows[i]
                    p = directed_destination_probs(
                        e["history"], coords[array], labels[i], e["b"],
                        FROZEN_EXTERNAL_KAPPA)
                    scores.append(math.log(p[e["c"]] / e["history"][e["c"]]))
                bee_gains[(col, bee)] = _mean(scores)
            return _mean([_mean([bee_gains[(col, bee)] for bee in bees])
                          for col, bees in sorted(percolony.items())])
        incoming = [r["a"] for r in rows]
        actual = gain_for_labels(incoming)
        shuffled = []
        changed = []
        for _ in range(permutations):
            sim = list(incoming)
            for inds in by_b.values():
                choices = [sim[i] for i in inds]
                rng.shuffle(choices)
                for i, c in zip(inds, choices):
                    sim[i] = c
            shuffled.append(gain_for_labels(sim))
            changed.append(sum(a != b for a, b in zip(incoming, sim)))
        avg = _mean(shuffled)
        receipt.update({
            "status": "COMPUTED_SOURCE_CONDITIONAL_HISTORY_CHALLENGE_NULL",
            "actual_colony_equal_direction_over_history_nats": actual,
            "null_mean_colony_equal_gain_nats": avg,
            "actual_minus_null_mean_nats": actual-avg,
            "one_sided_conditional_p": (1 + sum(z >= actual-1e-12 for z in shuffled)) / (permutations+1),
            "null_q05": sorted(shuffled)[int(.05*(permutations-1))],
            "null_q95": sorted(shuffled)[int(.95*(permutations-1))],
            "incoming_tags_reassigned_mean": _mean(changed),
            "conditional_null_not_physical_flight_intervention": True,
        })
        results[array] = receipt
    return results


def analyze_history_challenge(population, coords, lambdas, parent,
                              expected_original=True, permutations=PERMUTATIONS):
    """Caller must supply original publisher verified source rows."""
    scores, events = _per_bee_components(population, coords, lambdas)
    if set(scores) != {"1", "2", "3"} or set(lambdas) != {"1", "2", "3"}:
        raise ValueError("NO_GO_THREE_ORIGINAL_ARRAYS_REQUIRED")
    outputs = {}
    for array in ("1", "2", "3"):
        rows = scores[array]
        n = sum(r["source_genuine_heldout_triplets"] for r in rows)
        bycol = _coarse_means(rows, "direction_over_history")
        if len(rows) < MIN_BEES_PER_ARRAY or n < MIN_TEST_TRIPLETS_PER_ARRAY or len(bycol) != 2:
            raise ValueError("NO_GO_SOURCE_HISTORY_CHALLENGE_SUPPORT")
        if expected_original and (n != EXPECTED_ARRAY_TRIPLETS[array] or len(rows) != 29):
            raise ValueError("NO_GO_PARENT_SOURCE_ARRAY_SAMPLES_CHANGED")
        _check_parent_source(parent, array, rows)
        outputs[array] = {
            "source_array": array,
            "qualifying_bees": len(rows),
            "genuine_heldout_triplets": n,
            "original_colonies": 2,
            "bees_positive_direction_over_history": sum(r["direction_over_history"] > 0 for r in rows),
            "colony_equal_direction_over_history_gain_nats": _mean(bycol.values()),
            "bee_equal_direction_over_history_gain_nats": _mean([r["direction_over_history"] for r in rows]),
            "colony_direction_over_history_gains": bycol,
            "bee_equal_history_over_geo_gain_nats": _mean([r["history_over_geo"] for r in rows]),
            "bee_equal_direction_over_geo_gain_nats": _mean([r["direction_over_geo"] for r in rows]),
            "bee_equal_history_over_direction_gain_nats": _mean([r["history_over_direction"] for r in rows]),
            "bee_equal_model_nll": {name: _mean([r[name+"_nll"] for r in rows])
                                   for name in ("Mgeo", "Mturn", "Mhistory", "Mhistory_turn")},
            "colony_and_bee_scores": rows,  # derived scores, not source trajectories
            "both_independent_colonies_positive": all(v > 0 for v in bycol.values()),
            "parent_original_direction_reconciled_exactly": True,
        }
    nulls = conditional_permutation(events, coords, permutations=permutations)
    for array, score in outputs.items():
        null = nulls[array]
        if null["status"].startswith("NO_GO"):
            raise ValueError("NO_GO_HISTORY_CHALLENGE_SHUFFLE_SUPPORT")
        if abs(null["actual_colony_equal_direction_over_history_nats"] -
               score["colony_equal_direction_over_history_gain_nats"]) > RECONCILIATION_TOL:
            raise ValueError("NO_GO_PERMUTATION_ORIGINAL_SCORE_MISMATCH")
    gate = all(z["both_independent_colonies_positive"] for z in outputs.values())
    return {
        "status": "STAGE9B_POST_HOC_HISTORY_CHALLENGE_EVALUATED",
        "source_doi": "10.1038/s41598-017-04919-8",
        "original_source_observation": "within-original-bout next different flower",
        "source_original_colonies": 2,
        "fixed_history_beta": BETA,
        "fixed_external_direction_kappa": FROZEN_EXTERNAL_KAPPA,
        "early_bouts_only": [1,15], "heldout_bouts_only": [16,20],
        "original_arrangements_in_fixed_order": [1,2,3],
        "history_conditioned_direction_descriptively_positive_in_all_six_colony_arrays": gate,
        "source_array_results": outputs,
        "source_conditioned_permutation_null": nulls,
        "model_is_2017_posthoc_falsification_after_2019_direction_replicated": True,
        "not_evidence_of_causal_trajectory_or_information_query_cost": True,
    }
