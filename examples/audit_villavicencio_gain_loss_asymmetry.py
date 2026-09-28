"""Audit gain-versus-loss predictive asymmetry after conventional-filter CV.

This is a post-result diagnostic. It does not refit the ecological models and
must not be interpreted as confirmatory evidence for routeability or causality.

The audit addresses the large difference in gain/loss event prevalence by:
1. converting held-out posterior odds to likelihood-ratio scale using the
   training-fold null prevalence;
2. applying a common 0.5 event prior;
3. scoring with equal total weight on events and non-events.

ROC AUC is reported unchanged because it is prevalence-invariant.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


EXPECTED_FOLDS = {
    "strict_core_2008_2011": 3,
    "near_core_2007_2011": 4,
    "all_annual_2006_2011": 5,
}


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _auc(y, p):
    positives = sum(y)
    negatives = len(y) - positives
    if positives == 0 or negatives == 0:
        return None

    ordered = sorted(zip(p, y), key=lambda item: item[0])
    rank_sum = 0.0
    index = 0
    rank = 1
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = (rank + (rank + end - index - 1)) / 2
        rank_sum += average_rank * sum(
            outcome for _, outcome in ordered[index:end]
        )
        rank += end - index
        index = end

    return (
        rank_sum - positives * (positives + 1) / 2
    ) / (positives * negatives)


def _rebase_probability(probability, training_prevalence, target_prevalence=0.5):
    eps = 1e-8
    p = min(max(float(probability), eps), 1 - eps)
    pi = min(max(float(training_prevalence), eps), 1 - eps)
    target = min(max(float(target_prevalence), eps), 1 - eps)

    posterior_odds = p / (1 - p)
    training_prior_odds = pi / (1 - pi)
    likelihood_ratio = posterior_odds / training_prior_odds
    target_prior_odds = target / (1 - target)
    target_odds = likelihood_ratio * target_prior_odds
    return target_odds / (1 + target_odds)


def _balanced_metrics(rows, probability_field, training_prevalence):
    y = [int(row["outcome"]) for row in rows]
    raw_p = [float(row[probability_field]) for row in rows]
    p = [
        _rebase_probability(value, training_prevalence)
        for value in raw_p
    ]

    positives = sum(y)
    negatives = len(y) - positives
    if positives == 0 or negatives == 0:
        raise ValueError("balanced scoring requires both outcome classes")

    weights = [
        0.5 / positives if outcome else 0.5 / negatives
        for outcome in y
    ]
    log_loss = sum(
        weight
        * (
            -outcome * math.log(probability)
            - (1 - outcome) * math.log(1 - probability)
        )
        for outcome, probability, weight in zip(y, p, weights)
    )
    brier = sum(
        weight * (probability - outcome) ** 2
        for outcome, probability, weight in zip(y, p, weights)
    )

    return {
        "n": len(y),
        "events": positives,
        "auc": _auc(y, raw_p),
        "balanced_log_loss": log_loss,
        "balanced_log_loss_reduction_vs_half": (
            (math.log(2) - log_loss) / math.log(2)
        ),
        "balanced_brier": brier,
        "balanced_brier_improvement_vs_half": 0.25 - brier,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline_predictions", type=Path)
    parser.add_argument("ablation_predictions", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    baseline = _read(args.baseline_predictions)
    ablation = _read(args.ablation_predictions)

    baseline_groups = defaultdict(list)
    training_prevalence = {}
    for row in baseline:
        key = (
            row["analysis_scope"],
            row["risk_set"],
            row["transition"],
        )
        baseline_groups[key].append(row)
        null_probability = float(row["null_probability"])
        if key in training_prevalence:
            if not math.isclose(
                training_prevalence[key],
                null_probability,
                rel_tol=0,
                abs_tol=1e-12,
            ):
                raise ValueError(f"{key}: null probability varies within fold")
        else:
            training_prevalence[key] = null_probability

    ablation_groups = defaultdict(list)
    for row in ablation:
        key = (
            row["analysis_scope"],
            row["risk_set"],
            row["transition"],
            row["model"],
        )
        ablation_groups[key].append(row)

    scopes = {}
    for scope, expected_fold_count in EXPECTED_FOLDS.items():
        transitions = sorted(
            {
                transition
                for s, _, transition in baseline_groups
                if s == scope
            }
        )
        if len(transitions) != expected_fold_count:
            raise ValueError(
                f"{scope}: expected {expected_fold_count} transitions, "
                f"found {len(transitions)}"
            )

        fold_results = {}
        for transition in transitions:
            endpoints = {}
            for risk in ("gain", "loss"):
                base_key = (scope, risk, transition)
                base_rows = baseline_groups[base_key]
                if not base_rows:
                    raise ValueError(f"{base_key}: no baseline rows")

                prior = training_prevalence[base_key]
                baseline_metrics = _balanced_metrics(
                    base_rows,
                    "model_probability",
                    prior,
                )

                full_rows = ablation_groups[
                    (scope, risk, transition, "full")
                ]
                drop_rows = ablation_groups[
                    (scope, risk, transition, "drop_phenology")
                ]
                if len(full_rows) != len(base_rows) or len(drop_rows) != len(base_rows):
                    raise ValueError(
                        f"{base_key}: baseline/ablation row count mismatch"
                    )
                if [row["outcome"] for row in full_rows] != [
                    row["outcome"] for row in drop_rows
                ]:
                    raise ValueError(
                        f"{base_key}: full/drop phenology outcomes differ"
                    )

                full_metrics = _balanced_metrics(
                    full_rows,
                    "probability",
                    prior,
                )
                drop_metrics = _balanced_metrics(
                    drop_rows,
                    "probability",
                    prior,
                )
                endpoints[risk] = {
                    **baseline_metrics,
                    "training_event_prevalence": prior,
                    "phenology_drop_balanced_log_loss_penalty": (
                        drop_metrics["balanced_log_loss"]
                        - full_metrics["balanced_log_loss"]
                    ),
                    "phenology_drop_balanced_brier_penalty": (
                        drop_metrics["balanced_brier"]
                        - full_metrics["balanced_brier"]
                    ),
                    "phenology_drop_auc_penalty": (
                        full_metrics["auc"] - drop_metrics["auc"]
                    ),
                }

            gain = endpoints["gain"]
            loss = endpoints["loss"]
            fold_results[transition] = {
                "gain": gain,
                "loss": loss,
                "gain_minus_loss": {
                    "auc_gap": gain["auc"] - loss["auc"],
                    "balanced_log_loss_reduction_gap": (
                        gain["balanced_log_loss_reduction_vs_half"]
                        - loss["balanced_log_loss_reduction_vs_half"]
                    ),
                    "balanced_brier_improvement_gap": (
                        gain["balanced_brier_improvement_vs_half"]
                        - loss["balanced_brier_improvement_vs_half"]
                    ),
                    "phenology_drop_balanced_log_loss_penalty_gap": (
                        gain["phenology_drop_balanced_log_loss_penalty"]
                        - loss["phenology_drop_balanced_log_loss_penalty"]
                    ),
                    "phenology_drop_balanced_brier_penalty_gap": (
                        gain["phenology_drop_balanced_brier_penalty"]
                        - loss["phenology_drop_balanced_brier_penalty"]
                    ),
                    "phenology_drop_auc_penalty_gap": (
                        gain["phenology_drop_auc_penalty"]
                        - loss["phenology_drop_auc_penalty"]
                    ),
                },
            }

        contrast_fields = (
            "auc_gap",
            "balanced_log_loss_reduction_gap",
            "balanced_brier_improvement_gap",
            "phenology_drop_balanced_log_loss_penalty_gap",
            "phenology_drop_balanced_brier_penalty_gap",
            "phenology_drop_auc_penalty_gap",
        )
        direction_counts = {
            field: {
                "positive_folds": sum(
                    fold_results[transition]["gain_minus_loss"][field] > 0
                    for transition in transitions
                ),
                "fold_count": len(transitions),
            }
            for field in contrast_fields
        }
        scopes[scope] = {
            "folds": fold_results,
            "direction_counts": direction_counts,
        }

    result = {
        "schema": "adaptive-gain-villavicencio-gain-loss-asymmetry-audit-v1",
        "analysis_role": (
            "post-result diagnostic prompted by the observed gain-loss skill "
            "contrast; not a preregistered confirmatory test"
        ),
        "target_event_prevalence": 0.5,
        "decision_equivalence_inferred": False,
        "scopes": scopes,
        "interpretation": (
            "A consistently positive gain-minus-loss contrast means the frozen "
            "conventional filters separate future link gains more strongly than "
            "future link losses under a common-prevalence scoring surface. "
            "Phenology-drop contrasts quantify whether static dyad-level "
            "phenological overlap contributes more to gain than loss prediction."
        ),
        "claim_ceiling": (
            "Exploratory held-out predictive asymmetry only; no causal "
            "assembly/disassembly claim and no routeability inference."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
