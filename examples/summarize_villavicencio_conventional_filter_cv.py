"""Summarize held-out conventional-filter predictions without refitting models."""

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


def _log_loss(y, p):
    total = 0.0
    for outcome, probability in zip(y, p):
        probability = min(max(probability, 1e-8), 1 - 1e-8)
        total -= outcome * math.log(probability) + (1 - outcome) * math.log(
            1 - probability
        )
    return total / len(y)


def _brier(y, p):
    return sum(
        (probability - outcome) ** 2
        for outcome, probability in zip(y, p)
    ) / len(y)


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


def _metrics(rows):
    y = [int(row["outcome"]) for row in rows]
    model = [float(row["model_probability"]) for row in rows]
    null = [float(row["null_probability"]) for row in rows]
    model_log_loss = _log_loss(y, model)
    null_log_loss = _log_loss(y, null)
    model_brier = _brier(y, model)
    null_brier = _brier(y, null)
    return {
        "n": len(rows),
        "events": sum(y),
        "event_fraction": sum(y) / len(y),
        "model_log_loss": model_log_loss,
        "null_log_loss": null_log_loss,
        "heldout_log_loss_improvement": null_log_loss - model_log_loss,
        "relative_log_loss_reduction": (
            None
            if null_log_loss == 0
            else (null_log_loss - model_log_loss) / null_log_loss
        ),
        "model_brier": model_brier,
        "null_brier": null_brier,
        "heldout_brier_improvement": null_brier - model_brier,
        "model_roc_auc": _auc(y, model),
        "null_roc_auc": _auc(y, null),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("folds", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    predictions = _read(args.predictions)
    folds = _read(args.folds)

    by_scope_risk = defaultdict(list)
    by_scope_risk_transition = defaultdict(list)
    for row in predictions:
        scope = row["analysis_scope"]
        risk = row["risk_set"]
        transition = row["transition"]
        by_scope_risk[(scope, risk)].append(row)
        by_scope_risk_transition[(scope, risk, transition)].append(row)

    fold_by_scope_risk = defaultdict(list)
    for row in folds:
        fold_by_scope_risk[(row["analysis_scope"], row["risk_set"])].append(row)

    scopes = {}
    for scope, expected_fold_count in EXPECTED_FOLDS.items():
        endpoints = {}
        for risk in ("gain", "loss"):
            rows = by_scope_risk[(scope, risk)]
            if not rows:
                raise SystemExit(f"no held-out predictions for {scope}/{risk}")
            aggregate = _metrics(rows)
            risk_folds = fold_by_scope_risk[(scope, risk)]
            if len(risk_folds) != expected_fold_count:
                raise SystemExit(
                    f"expected {expected_fold_count} folds for {scope}/{risk}"
                )

            fold_metrics = {}
            transitions = sorted(
                transition
                for s, r, transition in by_scope_risk_transition
                if s == scope and r == risk
            )
            for transition in transitions:
                fold_metrics[transition] = _metrics(
                    by_scope_risk_transition[(scope, risk, transition)]
                )

            all_converged = all(
                row["converged"].strip().lower() == "true"
                for row in risk_folds
            )
            endpoint_pass = (
                all_converged
                and aggregate["heldout_log_loss_improvement"] > 0
                and math.isfinite(aggregate["model_log_loss"])
            )
            endpoints[risk] = {
                **aggregate,
                "fold_count": len(risk_folds),
                "all_folds_converged": all_converged,
                "endpoint_gate": "PASS" if endpoint_pass else "FAIL",
                "folds": fold_metrics,
            }

        scopes[scope] = {
            "role": (
                "primary"
                if scope == PRIMARY_SCOPE
                else "sampling-effort sensitivity"
            ),
            "endpoints": endpoints,
        }

    primary = scopes[PRIMARY_SCOPE]["endpoints"]
    promoted = any(
        primary[risk]["endpoint_gate"] == "PASS"
        for risk in ("gain", "loss")
    )
    result = {
        "schema": "adaptive-gain-villavicencio-conventional-filter-cv-v1",
        "analysis_scope": "annual detection-sensitive fallback",
        "primary_scope": PRIMARY_SCOPE,
        "decision_equivalence_inferred": False,
        "predictor_tuning_after_outcome": False,
        "scopes": scopes,
        "promotion_gate": (
            "PASS_primary_scope_at_least_one_endpoint_predictive"
            if promoted
            else "FAIL_primary_scope_no_endpoint_predictive"
        ),
        "interpretation": (
            "A PASS means the frozen conventional filters carry reproducible "
            "information about annual link dynamics in the sampling-consistent "
            "primary scope. It does not validate routeability or "
            "decision-structural turnover."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
