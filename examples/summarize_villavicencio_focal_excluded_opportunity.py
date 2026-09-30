"""Summarize focal-response-excluded opportunity CV for Villavicencio."""

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
MODELS = (
    "current_full",
    "current_drop_pairwise_overlap",
    "lagged_full",
    "lagged_drop_pairwise_overlap",
)


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _log_loss(y, p):
    total = 0.0
    for outcome, probability in zip(y, p):
        probability = min(max(float(probability), 1e-8), 1 - 1e-8)
        total -= outcome * math.log(probability) + (1 - outcome) * math.log(
            1 - probability
        )
    return total / len(y)


def _brier(y, p):
    return sum(
        (float(probability) - outcome) ** 2
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
        "relative_log_loss_reduction": (
            None
            if null_log_loss == 0
            else (null_log_loss - model_log_loss) / null_log_loss
        ),
        "model_brier": model_brier,
        "null_brier": null_brier,
        "brier_improvement": null_brier - model_brier,
        "roc_auc": _auc(y, model),
    }


def _opportunity_rates(table_rows, scope_transitions, risk, *, lagged=False):
    rows = [
        row
        for row in table_rows
        if row["transition"] in scope_transitions
        and row["risk_set"] == risk
    ]
    field = (
        "lagged_focal_excluded_opportunity_positive"
        if lagged
        else "focal_excluded_opportunity_positive"
    )
    positive = [row for row in rows if int(row[field]) == 1]
    zero = [row for row in rows if int(row[field]) == 0]

    def event_rate(group):
        if not group:
            return None
        return sum(int(row["outcome"]) for row in group) / len(group)

    positive_rate = event_rate(positive)
    zero_rate = event_rate(zero)
    return {
        "n": len(rows),
        "opportunity_positive_n": len(positive),
        "opportunity_zero_n": len(zero),
        "event_rate_opportunity_positive": positive_rate,
        "event_rate_opportunity_zero": zero_rate,
        "event_rate_ratio_positive_over_zero": (
            None
            if zero_rate in (None, 0) or positive_rate is None
            else positive_rate / zero_rate
        ),
    }


def _classify_increment(pooled_delta, fold_deltas):
    positive = sum(value > 0 for value in fold_deltas.values())
    if pooled_delta > 0 and positive == len(fold_deltas):
        return "reproducible_incremental_information"
    if pooled_delta > 0 and positive > 0:
        return "positive_but_fold_unstable"
    return "no_reproducible_incremental_information"


def _increment(full, drop, transitions):
    fold_delta_log_loss = {
        transition: (
            drop["folds"][transition]["model_log_loss"]
            - full["folds"][transition]["model_log_loss"]
        )
        for transition in transitions
    }
    fold_delta_brier = {
        transition: (
            drop["folds"][transition]["model_brier"]
            - full["folds"][transition]["model_brier"]
        )
        for transition in transitions
    }
    fold_delta_auc = {
        transition: (
            full["folds"][transition]["roc_auc"]
            - drop["folds"][transition]["roc_auc"]
        )
        for transition in transitions
    }
    pooled_delta_log_loss = drop["model_log_loss"] - full["model_log_loss"]
    return {
        "delta_log_loss_drop_minus_full": pooled_delta_log_loss,
        "delta_brier_drop_minus_full": (
            drop["model_brier"] - full["model_brier"]
        ),
        "delta_auc_full_minus_drop": (
            full["roc_auc"] - drop["roc_auc"]
        ),
        "fold_delta_log_loss": fold_delta_log_loss,
        "fold_delta_brier": fold_delta_brier,
        "fold_delta_auc": fold_delta_auc,
        "positive_log_loss_fold_count": sum(
            value > 0 for value in fold_delta_log_loss.values()
        ),
        "classification": _classify_increment(
            pooled_delta_log_loss,
            fold_delta_log_loss,
        ),
    }


def _current_vs_lagged(current, lagged, transitions):
    return {
        "relative_log_loss_reduction_difference_current_minus_lagged": (
            current["relative_log_loss_reduction"]
            - lagged["relative_log_loss_reduction"]
        ),
        "auc_difference_current_minus_lagged": (
            current["roc_auc"] - lagged["roc_auc"]
        ),
        "brier_improvement_difference_current_minus_lagged": (
            current["brier_improvement"] - lagged["brier_improvement"]
        ),
        "fold_relative_log_loss_skill_difference": {
            transition: (
                current["folds"][transition]["relative_log_loss_reduction"]
                - lagged["folds"][transition]["relative_log_loss_reduction"]
            )
            for transition in transitions
        },
        "current_better_log_loss_skill_fold_count": sum(
            current["folds"][transition]["relative_log_loss_reduction"]
            > lagged["folds"][transition]["relative_log_loss_reduction"]
            for transition in transitions
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("table", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("folds", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    table = _read(args.table)
    predictions = _read(args.predictions)
    folds = _read(args.folds)

    grouped = defaultdict(list)
    fold_groups = defaultdict(list)
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
        fold_groups[
            (
                row["analysis_scope"],
                row["risk_set"],
                row["model"],
            )
        ].append(row)

    scopes = {}
    for scope, expected in EXPECTED_FOLDS.items():
        transitions = sorted(
            {
                transition
                for s, _, transition, model in grouped
                if s == scope and model == "current_full"
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
                fold_metrics = {}
                for transition in transitions:
                    rows = grouped[(scope, risk, transition, model)]
                    if not rows:
                        raise SystemExit(
                            f"{scope}/{risk}/{transition}/{model}: no predictions"
                        )
                    pooled.extend(rows)
                    fold_metrics[transition] = _metrics(rows)

                state = fold_groups[(scope, risk, model)]
                if len(state) != expected:
                    raise SystemExit(
                        f"{scope}/{risk}/{model}: expected {expected} fold receipts"
                    )
                all_converged = all(
                    _bool(row["converged"])
                    and int(row["finite_coefficient_count"])
                    == int(row["coefficient_count"])
                    for row in state
                )
                aggregate = _metrics(pooled)
                aggregate.update(
                    {
                        "fold_count": expected,
                        "all_folds_converged": all_converged,
                        "folds": fold_metrics,
                        "all_folds_positive_log_loss_skill": all(
                            item["relative_log_loss_reduction"] > 0
                            for item in fold_metrics.values()
                        ),
                    }
                )
                model_results[model] = aggregate

            current_full = model_results["current_full"]
            current_drop = model_results["current_drop_pairwise_overlap"]
            lagged_full = model_results["lagged_full"]
            lagged_drop = model_results["lagged_drop_pairwise_overlap"]

            endpoints[risk] = {
                "current": {
                    "full": current_full,
                    "marginal_only": current_drop,
                    "pairwise_overlap_increment": _increment(
                        current_full,
                        current_drop,
                        transitions,
                    ),
                    "opportunity_rates": _opportunity_rates(
                        table,
                        transitions,
                        risk,
                        lagged=False,
                    ),
                },
                "lagged": {
                    "full": lagged_full,
                    "marginal_only": lagged_drop,
                    "pairwise_overlap_increment": _increment(
                        lagged_full,
                        lagged_drop,
                        transitions,
                    ),
                    "opportunity_rates": _opportunity_rates(
                        table,
                        transitions,
                        risk,
                        lagged=True,
                    ),
                },
                "current_vs_lagged": _current_vs_lagged(
                    current_full,
                    lagged_full,
                    transitions,
                ),
            }

        scopes[scope] = {
            "role": (
                "primary"
                if scope == PRIMARY_SCOPE
                else "sampling-effort sensitivity"
            ),
            "transitions": transitions,
            "endpoints": endpoints,
        }

    primary = scopes[PRIMARY_SCOPE]["endpoints"]
    current_signal = all(
        primary[risk]["current"]["full"]["all_folds_converged"]
        and primary[risk]["current"]["full"]["relative_log_loss_reduction"] > 0
        for risk in ("gain", "loss")
    )
    lagged_both_positive = all(
        primary[risk]["lagged"]["full"]["relative_log_loss_reduction"] > 0
        for risk in ("gain", "loss")
    )
    current_better_both = all(
        primary[risk]["current_vs_lagged"][
            "relative_log_loss_reduction_difference_current_minus_lagged"
        ] > 0
        for risk in ("gain", "loss")
    )
    overlap_classes = {
        risk: {
            "current": primary[risk]["current"][
                "pairwise_overlap_increment"
            ]["classification"],
            "lagged": primary[risk]["lagged"][
                "pairwise_overlap_increment"
            ]["classification"],
        }
        for risk in ("gain", "loss")
    }

    if current_signal and current_better_both and not lagged_both_positive:
        status = "retrospective_current_state_signal_lagged_control_not_recovered"
    elif current_signal:
        status = "retrospective_current_state_signal_present"
    else:
        status = "retrospective_repair_mixed"

    result = {
        "schema": (
            "adaptive-gain-villavicencio-focal-excluded-opportunity-cv-v1"
        ),
        "date": "2026-09-28",
        "status": status,
        "analysis_status": (
            "post_leakage_repair; current-year analysis is retrospective and "
            "contemporaneous; one-year-lagged models are past-only negative "
            "controls; not preregistered or causal"
        ),
        "primary_scope": PRIMARY_SCOPE,
        "published_phenological_overlap_used": False,
        "published_aggregate_flower_abundance_used": False,
        "focal_response_excluded_from_opportunity": True,
        "scopes": scopes,
        "primary_overlap_classification": overlap_classes,
        "primary_current_signal": current_signal,
        "primary_lagged_both_positive": lagged_both_positive,
        "primary_current_better_than_lagged_both_endpoints": current_better_both,
        "ecological_read": (
            "The repaired analysis separates three questions: whether a clean "
            "current-year availability/activity surface discriminates annual "
            "link dynamics, whether dyad-specific weekly overlap adds information "
            "beyond the two marginal opportunity components, and whether the "
            "same construction has past-only one-year-lagged predictive value. "
            "A current-only pattern supports current ecological opportunity, "
            "not stable dyad propensity or strict forecasting."
        ),
        "claim_ceiling": (
            "Retrospective focal-response-excluded opportunity association only. "
            "Current-year skill cannot establish pair-specific temporal matching "
            "unless the overlap increment is reproducible, and failure of the "
            "lagged control limits the result to current-state ecology. None of "
            "these analyses establishes causality, decision equivalence, or "
            "routeability."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
