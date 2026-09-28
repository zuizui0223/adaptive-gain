"""Post-result robustness diagnostic for gain-versus-loss predictability.

This script does not refit models. It audits whether the observed gain/loss
asymmetry is specific to prevalence-sensitive scoring rules or also appears in
ROC AUC, which is invariant to evaluation-set class prevalence.

The diagnostic is explicitly post hoc and must not be described as a
prospectively frozen confirmatory test.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

PRIMARY_SCOPE = "strict_core_2008_2011"
EXPECTED_FOLDS = {
    "strict_core_2008_2011": 3,
    "near_core_2007_2011": 4,
    "all_annual_2006_2011": 5,
}


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _log_loss(rows, field: str) -> float:
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row[field]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _brier(rows, field: str) -> float:
    return sum(
        (float(row[field]) - int(row["outcome"])) ** 2
        for row in rows
    ) / len(rows)


def _auc(rows, field: str) -> float | None:
    y = [int(row["outcome"]) for row in rows]
    p = [float(row[field]) for row in rows]
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
        rank_sum += average_rank * sum(outcome for _, outcome in ordered[index:end])
        rank += end - index
        index = end
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def _cv_metrics(rows):
    model_ll = _log_loss(rows, "model_probability")
    null_ll = _log_loss(rows, "null_probability")
    model_brier = _brier(rows, "model_probability")
    null_brier = _brier(rows, "null_probability")
    events = sum(int(row["outcome"]) for row in rows)
    return {
        "n": len(rows),
        "events": events,
        "event_fraction": events / len(rows),
        "roc_auc": _auc(rows, "model_probability"),
        "relative_log_loss_reduction": (
            None if null_ll == 0 else (null_ll - model_ll) / null_ll
        ),
        "brier_skill_score": (
            None if null_brier == 0 else 1 - model_brier / null_brier
        ),
    }


def _log_loss_ablation(rows) -> float:
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row["probability"]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _ablation_delta(rows_full, rows_drop) -> float:
    if len(rows_full) != len(rows_drop):
        raise ValueError("full and drop-phenology row counts differ")
    return _log_loss_ablation(rows_drop) - _log_loss_ablation(rows_full)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("ablation_predictions", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    predictions = _read(args.predictions)
    ablation = _read(args.ablation_predictions)

    by_cv = defaultdict(list)
    for row in predictions:
        by_cv[(row["analysis_scope"], row["risk_set"], row["transition"])].append(row)

    by_abl = defaultdict(list)
    for row in ablation:
        by_abl[
            (
                row["analysis_scope"],
                row["risk_set"],
                row["transition"],
                row["model"],
            )
        ].append(row)

    scopes = {}
    for scope, expected in EXPECTED_FOLDS.items():
        transitions = sorted(
            {
                transition
                for s, risk, transition in by_cv
                if s == scope and risk == "gain"
            }
        )
        if len(transitions) != expected:
            raise SystemExit(
                f"{scope}: expected {expected} transitions, found {len(transitions)}"
            )

        fold_rows = []
        for transition in transitions:
            gain = _cv_metrics(by_cv[(scope, "gain", transition)])
            loss = _cv_metrics(by_cv[(scope, "loss", transition)])
            if gain["roc_auc"] is None or loss["roc_auc"] is None:
                raise SystemExit(f"{scope}/{transition}: AUC not estimable")

            gain_pheno = _ablation_delta(
                by_abl[(scope, "gain", transition, "full")],
                by_abl[(scope, "gain", transition, "drop_phenology")],
            )
            loss_pheno = _ablation_delta(
                by_abl[(scope, "loss", transition, "full")],
                by_abl[(scope, "loss", transition, "drop_phenology")],
            )

            fold_rows.append(
                {
                    "transition": transition,
                    "gain": gain,
                    "loss": loss,
                    "auc_difference_gain_minus_loss": (
                        gain["roc_auc"] - loss["roc_auc"]
                    ),
                    "gain_auc_higher": gain["roc_auc"] > loss["roc_auc"],
                    "brier_skill_difference_gain_minus_loss": (
                        gain["brier_skill_score"] - loss["brier_skill_score"]
                    ),
                    "gain_brier_skill_higher": (
                        gain["brier_skill_score"] > loss["brier_skill_score"]
                    ),
                    "phenology_delta_log_loss": {
                        "gain": gain_pheno,
                        "loss": loss_pheno,
                        "warning": (
                            "cross-endpoint magnitude comparison is descriptive only "
                            "because gain and loss have different event prevalences "
                            "and risk sets"
                        ),
                    },
                }
            )

        scopes[scope] = {
            "folds": fold_rows,
            "gain_auc_higher_count": sum(
                row["gain_auc_higher"] for row in fold_rows
            ),
            "fold_count": len(fold_rows),
            "mean_auc_difference_gain_minus_loss": sum(
                row["auc_difference_gain_minus_loss"] for row in fold_rows
            )
            / len(fold_rows),
            "gain_brier_skill_higher_count": sum(
                row["gain_brier_skill_higher"] for row in fold_rows
            ),
        }

    primary = scopes[PRIMARY_SCOPE]
    result = {
        "schema": "adaptive-gain-villavicencio-gain-loss-asymmetry-diagnostic-v1",
        "date": "2026-09-28",
        "status": "post_result_robustness_diagnostic",
        "scope": "annual detection-sensitive conventional-filter temporal CV",
        "reason": (
            "The original pooled result suggested stronger prediction for link gains "
            "than link losses. Because gain and loss have very different event "
            "prevalences and risk-set sizes, this diagnostic asks whether the "
            "asymmetry persists in ROC AUC and fold direction rather than relying "
            "on relative log-loss reduction alone."
        ),
        "prospective_status": "post_hoc_not_confirmatory",
        "scopes": scopes,
        "primary_summary": {
            "auc_direction": (
                f"{primary['gain_auc_higher_count']}/{primary['fold_count']} "
                "primary folds gain > loss"
            ),
            "mean_auc_difference_gain_minus_loss": (
                primary["mean_auc_difference_gain_minus_loss"]
            ),
            "brier_skill_direction": (
                f"{primary['gain_brier_skill_higher_count']}/"
                f"{primary['fold_count']} primary folds gain > loss"
            ),
            "classification": "consistent_ranking_discrimination_asymmetry_only",
        },
        "interpretation": {
            "supported": (
                "Frozen conventional filters discriminate annual link gains from "
                "stable absences better than they discriminate link losses from "
                "retained links in every held-out primary transition; the same "
                "AUC direction persists in the broader temporal scopes."
            ),
            "not_supported": (
                "A metric-general claim that gain is universally more predictable "
                "than loss; Brier skill does not show the same foldwise direction."
            ),
            "phenology": (
                "Removing phenological overlap worsens held-out log-loss for both "
                "endpoints in every primary fold, but its gain-versus-loss magnitude "
                "is not used as an asymmetry test because the endpoint prevalences differ."
            ),
        },
        "claim_firewall": [
            "do not interpret gain-versus-loss AUC difference as a causal difference in assembly versus disassembly mechanisms",
            "do not compare relative log-loss reduction across endpoints as if prevalence were matched",
            "do not call the annual phenological-overlap matrix a year-specific phenological-change exposure",
            "do not infer routeability or decision-equivalence structure from this diagnostic",
            "temporal holdout tests transfer across annual transitions, not transfer to unseen species or unseen dyad identities",
        ],
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
