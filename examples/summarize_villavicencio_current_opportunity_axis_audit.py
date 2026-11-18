"""Summarize the retrospective current-opportunity marginal-axis audit."""

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
MODELS = ("marginal_full", "plant_only", "pollinator_only")


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _log_loss(rows):
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row["probability"]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


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


def _classification(pooled, folds):
    positive = sum(value > 0 for value in folds.values())
    if pooled > 0 and positive == len(folds):
        return "reproducible_incremental_information"
    if pooled > 0 and positive > 0:
        return "positive_but_fold_unstable"
    return "no_reproducible_incremental_information"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("folds", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    predictions = _read(args.predictions)
    folds = _read(args.folds)

    grouped = defaultdict(list)
    fold_state = defaultdict(list)
    for row in predictions:
        grouped[
            (
                row["analysis_scope"],
                row["risk_set"],
                row["transition"],
                row["model"],
            )
        ].append(row)
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
                if s == scope and model == "marginal_full"
            }
        )
        if len(transitions) != expected:
            raise SystemExit(
                f"{scope}: expected {expected} transitions, found {len(transitions)}"
            )

        endpoints = {}
        for risk in ("gain", "loss"):
            metrics = {}
            for model in MODELS:
                pooled_rows = []
                fold_metrics = {}
                for transition in transitions:
                    rows = grouped[(scope, risk, transition, model)]
                    if not rows:
                        raise SystemExit(
                            f"{scope}/{risk}/{transition}/{model}: no predictions"
                        )
                    pooled_rows.extend(rows)
                    fold_metrics[transition] = {
                        "log_loss": _log_loss(rows),
                        "roc_auc": _auc(rows),
                    }

                receipts = fold_state[(scope, risk, model)]
                if len(receipts) != expected:
                    raise SystemExit(
                        f"{scope}/{risk}/{model}: expected {expected} fold receipts"
                    )
                if not all(
                    _bool(row["converged"])
                    and int(row["finite_coefficient_count"])
                    == int(row["coefficient_count"])
                    for row in receipts
                ):
                    raise SystemExit(
                        f"{scope}/{risk}/{model}: model convergence failure"
                    )

                metrics[model] = {
                    "n": len(pooled_rows),
                    "events": sum(int(row["outcome"]) for row in pooled_rows),
                    "log_loss": _log_loss(pooled_rows),
                    "roc_auc": _auc(pooled_rows),
                    "folds": fold_metrics,
                }

            full = metrics["marginal_full"]
            plant_only = metrics["plant_only"]
            pollinator_only = metrics["pollinator_only"]

            plant_folds = {
                transition: (
                    pollinator_only["folds"][transition]["log_loss"]
                    - full["folds"][transition]["log_loss"]
                )
                for transition in transitions
            }
            pollinator_folds = {
                transition: (
                    plant_only["folds"][transition]["log_loss"]
                    - full["folds"][transition]["log_loss"]
                )
                for transition in transitions
            }
            plant_increment = pollinator_only["log_loss"] - full["log_loss"]
            pollinator_increment = plant_only["log_loss"] - full["log_loss"]

            if risk == "gain":
                endpoint_axis_difference = (
                    pollinator_increment - plant_increment
                )
                fold_axis_difference = {
                    transition: (
                        pollinator_folds[transition]
                        - plant_folds[transition]
                    )
                    for transition in transitions
                }
                directional_label = (
                    "pollinator_activity_increment_minus_plant_availability_increment"
                )
            else:
                endpoint_axis_difference = (
                    plant_increment - pollinator_increment
                )
                fold_axis_difference = {
                    transition: (
                        plant_folds[transition]
                        - pollinator_folds[transition]
                    )
                    for transition in transitions
                }
                directional_label = (
                    "plant_availability_increment_minus_pollinator_activity_increment"
                )

            endpoints[risk] = {
                "marginal_full": full,
                "plant_only": plant_only,
                "pollinator_only": pollinator_only,
                "plant_availability_increment": {
                    "delta_log_loss": plant_increment,
                    "fold_delta_log_loss": plant_folds,
                    "positive_fold_count": sum(
                        value > 0 for value in plant_folds.values()
                    ),
                    "classification": _classification(
                        plant_increment,
                        plant_folds,
                    ),
                },
                "pollinator_activity_increment": {
                    "delta_log_loss": pollinator_increment,
                    "fold_delta_log_loss": pollinator_folds,
                    "positive_fold_count": sum(
                        value > 0 for value in pollinator_folds.values()
                    ),
                    "classification": _classification(
                        pollinator_increment,
                        pollinator_folds,
                    ),
                },
                "endpoint_axis_asymmetry": {
                    "definition": directional_label,
                    "difference": endpoint_axis_difference,
                    "fold_difference": fold_axis_difference,
                    "positive_fold_count": sum(
                        value > 0 for value in fold_axis_difference.values()
                    ),
                    "fold_count": len(fold_axis_difference),
                },
            }

        scopes[scope] = {
            "transition_count": len(transitions),
            "transitions": transitions,
            "endpoints": endpoints,
        }

    primary = scopes["strict_core_2008_2011"]["endpoints"]
    result = {
        "schema": (
            "adaptive-gain-villavicencio-current-opportunity-axis-audit-v1"
        ),
        "date": "2026-09-28",
        "status": "retrospective_axis_decomposition_complete",
        "analysis_status": (
            "post_result_hypothesis_generating_decomposition; not confirmatory"
        ),
        "scopes": scopes,
        "primary_pattern": {
            "gain_pollinator_activity_increment_larger": (
                primary["gain"]["endpoint_axis_asymmetry"]["difference"] > 0
            ),
            "loss_plant_availability_increment_larger": (
                primary["loss"]["endpoint_axis_asymmetry"]["difference"] > 0
            ),
            "gain_direction_positive_folds": (
                f'{primary["gain"]["endpoint_axis_asymmetry"]["positive_fold_count"]}'
                f'/{primary["gain"]["endpoint_axis_asymmetry"]["fold_count"]}'
            ),
            "loss_direction_positive_folds": (
                f'{primary["loss"]["endpoint_axis_asymmetry"]["positive_fold_count"]}'
                f'/{primary["loss"]["endpoint_axis_asymmetry"]["fold_count"]}'
            ),
        },
        "ecological_read": (
            "Within the clean current-state marginal opportunity surface, "
            "gain discrimination can be decomposed into plant flowering "
            "availability and pollinator activity on other plants, and the "
            "same decomposition can be compared with loss. Directional "
            "differences are retrospective predictive-information patterns, "
            "not causal process estimates."
        ),
        "claim_ceiling": (
            "Post-result held-out predictive-information decomposition only. "
            "Do not interpret the larger endpoint-specific axis as a causal "
            "mechanism, a sampling-effort-independent ecological process, or "
            "routeability."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
