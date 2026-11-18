"""Summarize annual clean-opportunity versus focal-plant effort sensitivity."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


SCOPES = {
    "strict_core_2008_2011": 3,
    "near_core_2007_2011": 4,
    "all_annual_2006_2011": 5,
}
MODELS = (
    "effort_only",
    "opportunity_only",
    "opportunity_plus_effort",
)


def _read(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _log_loss(rows, probability_field="probability"):
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(
            max(float(row[probability_field]), 1e-8),
            1 - 1e-8,
        )
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _brier(rows, probability_field="probability"):
    return sum(
        (float(row[probability_field]) - int(row["outcome"])) ** 2
        for row in rows
    ) / len(rows)


def _auc(rows):
    y = [int(row["outcome"]) for row in rows]
    p = [float(row["probability"]) for row in rows]
    positives = sum(y)
    negatives = len(y) - positives
    if positives == 0 or negatives == 0:
        return None
    ordered = sorted(zip(p, y), key=lambda item: item[0])
    rank_sum = 0.0
    rank = 1
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = (rank + (rank + end - index - 1)) / 2
        rank_sum += average_rank * sum(v for _, v in ordered[index:end])
        rank += end - index
        index = end
    return (
        rank_sum - positives * (positives + 1) / 2
    ) / (positives * negatives)


def _metrics(rows):
    ll = _log_loss(rows)
    null_ll = _log_loss(rows, "null_probability")
    brier = _brier(rows)
    null_brier = _brier(rows, "null_probability")
    return {
        "n": len(rows),
        "events": sum(int(row["outcome"]) for row in rows),
        "log_loss": ll,
        "relative_log_loss_reduction_vs_null": (
            None if null_ll == 0 else (null_ll - ll) / null_ll
        ),
        "brier_improvement_vs_null": null_brier - brier,
        "roc_auc": _auc(rows),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("folds", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    predictions = _read(args.predictions)
    folds = _read(args.folds)

    grouped = defaultdict(list)
    for row in predictions:
        grouped[
            (
                row["analysis_scope"],
                row["risk_set"],
                row["transition"],
                row["model"],
            )
        ].append(row)

    fold_state = defaultdict(list)
    for row in folds:
        fold_state[
            (
                row["analysis_scope"],
                row["risk_set"],
                row["model"],
            )
        ].append(row)

    scopes = {}
    for scope, expected in SCOPES.items():
        transitions = sorted(
            {
                transition
                for s, _, transition, model in grouped
                if s == scope and model == "opportunity_plus_effort"
            }
        )
        if len(transitions) != expected:
            raise SystemExit(
                f"{scope}: expected {expected} transitions, found {len(transitions)}"
            )

        endpoints = {}
        for risk in ("gain", "loss"):
            model_results = {}
            for model in MODELS:
                pooled = []
                per_fold = {}
                for transition in transitions:
                    rows = grouped[(scope, risk, transition, model)]
                    if not rows:
                        raise SystemExit(
                            f"{scope}/{risk}/{transition}/{model}: missing"
                        )
                    pooled.extend(rows)
                    per_fold[transition] = _metrics(rows)

                receipts = fold_state[(scope, risk, model)]
                if len(receipts) != expected:
                    raise SystemExit(
                        f"{scope}/{risk}/{model}: fold count mismatch"
                    )
                all_converged = all(
                    _bool(row["converged"])
                    and int(row["coefficient_count"])
                    == int(row["finite_coefficient_count"])
                    for row in receipts
                )
                if not all_converged:
                    raise SystemExit(
                        f"{scope}/{risk}/{model}: convergence failure"
                    )
                model_results[model] = {
                    **_metrics(pooled),
                    "folds": per_fold,
                }

            combined = model_results["opportunity_plus_effort"]
            effort = model_results["effort_only"]
            opportunity = model_results["opportunity_only"]
            opportunity_increment = (
                effort["log_loss"] - combined["log_loss"]
            )
            effort_increment = (
                opportunity["log_loss"] - combined["log_loss"]
            )
            opportunity_fold_increment = {
                transition: (
                    effort["folds"][transition]["log_loss"]
                    - combined["folds"][transition]["log_loss"]
                )
                for transition in transitions
            }
            effort_fold_increment = {
                transition: (
                    opportunity["folds"][transition]["log_loss"]
                    - combined["folds"][transition]["log_loss"]
                )
                for transition in transitions
            }

            endpoints[risk] = {
                "models": model_results,
                "opportunity_increment_beyond_effort": {
                    "delta_log_loss": opportunity_increment,
                    "positive_fold_count": sum(
                        value > 0
                        for value in opportunity_fold_increment.values()
                    ),
                    "fold_count": len(opportunity_fold_increment),
                    "fold_delta_log_loss": opportunity_fold_increment,
                },
                "effort_increment_beyond_opportunity": {
                    "delta_log_loss": effort_increment,
                    "positive_fold_count": sum(
                        value > 0
                        for value in effort_fold_increment.values()
                    ),
                    "fold_count": len(effort_fold_increment),
                    "fold_delta_log_loss": effort_fold_increment,
                },
            }

        scopes[scope] = {
            "transitions": transitions,
            "endpoints": endpoints,
        }

    primary = scopes["strict_core_2008_2011"]["endpoints"]
    result = {
        "schema": (
            "adaptive-gain-villavicencio-opportunity-effort-control-v1"
        ),
        "date": "2026-09-29",
        "status": "post_result_opportunity_effort_sensitivity_complete",
        "analysis_status": (
            "post-result effort-adjustment sensitivity; not detection-"
            "corrected and not confirmatory"
        ),
        "scopes": scopes,
        "primary_read": {
            "gain_opportunity_increment_positive_all_folds": (
                primary["gain"]["opportunity_increment_beyond_effort"][
                    "positive_fold_count"
                ]
                == primary["gain"]["opportunity_increment_beyond_effort"][
                    "fold_count"
                ]
            ),
            "loss_opportunity_increment_positive_all_folds": (
                primary["loss"]["opportunity_increment_beyond_effort"][
                    "positive_fold_count"
                ]
                == primary["loss"]["opportunity_increment_beyond_effort"][
                    "fold_count"
                ]
            ),
        },
        "ecological_read": (
            "This sensitivity asks whether the clean current opportunity "
            "surface carries information beyond focal-plant census counts. "
            "It does not make binary link turnover detection-corrected."
        ),
        "claim_ceiling": (
            "Post-result effort-adjustment sensitivity only. A positive "
            "opportunity increment can rule out focal-plant census count as a "
            "complete explanation of the predictive association, but cannot "
            "identify true rewiring, remove pollinator-side detection effects, "
            "establish causality, strict forecasting, or routeability."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
