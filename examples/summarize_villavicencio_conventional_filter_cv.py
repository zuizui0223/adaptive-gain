"""Summarize held-out conventional-filter predictions without refitting models."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


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
    return sum((probability - outcome) ** 2 for outcome, probability in zip(y, p)) / len(y)


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
        rank_sum += average_rank * sum(outcome for _, outcome in ordered[index:end])
        rank += end - index
        index = end

    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def _metrics(rows):
    y = [int(row["outcome"]) for row in rows]
    model = [float(row["model_probability"]) for row in rows]
    null = [float(row["null_probability"]) for row in rows]
    return {
        "n": len(rows),
        "events": sum(y),
        "event_fraction": sum(y) / len(y),
        "model_log_loss": _log_loss(y, model),
        "null_log_loss": _log_loss(y, null),
        "heldout_log_loss_improvement": _log_loss(y, null) - _log_loss(y, model),
        "model_brier": _brier(y, model),
        "null_brier": _brier(y, null),
        "heldout_brier_improvement": _brier(y, null) - _brier(y, model),
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

    by_risk = defaultdict(list)
    by_risk_transition = defaultdict(list)
    for row in predictions:
        risk = row["risk_set"]
        transition = row["transition"]
        by_risk[risk].append(row)
        by_risk_transition[(risk, transition)].append(row)

    fold_by_risk = defaultdict(list)
    for row in folds:
        fold_by_risk[row["risk_set"]].append(row)

    endpoints = {}
    for risk in ("gain", "loss"):
        rows = by_risk[risk]
        if not rows:
            raise SystemExit(f"no held-out predictions for {risk}")
        aggregate = _metrics(rows)
        risk_folds = fold_by_risk[risk]
        if len(risk_folds) != 5:
            raise SystemExit(f"expected five temporal folds for {risk}")

        fold_metrics = {}
        for transition in sorted(
            transition for r, transition in by_risk_transition if r == risk
        ):
            fold_metrics[transition] = _metrics(
                by_risk_transition[(risk, transition)]
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

    promoted = any(
        endpoints[risk]["endpoint_gate"] == "PASS"
        for risk in ("gain", "loss")
    )
    result = {
        "schema": "adaptive-gain-villavicencio-conventional-filter-cv-v1",
        "analysis_scope": "annual detection-sensitive fallback",
        "decision_equivalence_inferred": False,
        "predictor_tuning_after_outcome": False,
        "endpoints": endpoints,
        "promotion_gate": (
            "PASS_at_least_one_endpoint_predictive"
            if promoted
            else "FAIL_no_endpoint_predictive"
        ),
        "interpretation": (
            "A PASS means the frozen conventional filters carry reproducible "
            "information about annual link dynamics in held-out transitions. "
            "It does not validate routeability or decision-structural turnover."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
