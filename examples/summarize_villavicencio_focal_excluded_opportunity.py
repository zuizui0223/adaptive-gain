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


def _opportunity_rates(table_rows, scope_transitions, risk):
    rows = [
        row
        for row in table_rows
        if row["transition"] in scope_transitions
        and row["risk_set"] == risk
    ]
    positive = [
        row
        for row in rows
        if int(row["focal_excluded_opportunity_positive"]) == 1
    ]
    zero = [
        row
        for row in rows
        if int(row["focal_excluded_opportunity_positive"]) == 0
    ]

    def event_rate(group):
        if not group:
            return None
        return sum(int(row["outcome"]) for row in group) / len(group)

    return {
        "n": len(rows),
        "opportunity_positive_n": len(positive),
        "opportunity_zero_n": len(zero),
        "event_rate_opportunity_positive": event_rate(positive),
        "event_rate_opportunity_zero": event_rate(zero),
        "event_rate_ratio_positive_over_zero": (
            None
            if not zero
            or event_rate(zero) in (None, 0)
            else event_rate(positive) / event_rate(zero)
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
            )
        ].append(row)
    for row in folds:
        fold_groups[
            (row["analysis_scope"], row["risk_set"])
        ].append(row)

    scopes = {}
    transition_lookup = {
        scope: sorted(
            {
                row["transition"]
                for row in predictions
                if row["analysis_scope"] == scope
            }
        )
        for scope in EXPECTED_FOLDS
    }

    for scope, expected in EXPECTED_FOLDS.items():
        transitions = transition_lookup[scope]
        if len(transitions) != expected:
            raise SystemExit(
                f"{scope}: expected {expected} transitions, found {len(transitions)}"
            )
        endpoints = {}
        for risk in ("gain", "loss"):
            pooled = []
            fold_metrics = {}
            for transition in transitions:
                rows = grouped[(scope, risk, transition)]
                if not rows:
                    raise SystemExit(
                        f"{scope}/{risk}/{transition}: no predictions"
                    )
                pooled.extend(rows)
                fold_metrics[transition] = _metrics(rows)

            state = fold_groups[(scope, risk)]
            if len(state) != expected:
                raise SystemExit(
                    f"{scope}/{risk}: expected {expected} fold receipts"
                )
            all_converged = all(
                _bool(row["converged"])
                and int(row["finite_coefficient_count"])
                == int(row["coefficient_count"])
                for row in state
            )
            endpoint = _metrics(pooled)
            endpoint.update(
                {
                    "fold_count": expected,
                    "all_folds_converged": all_converged,
                    "folds": fold_metrics,
                    "all_folds_positive_log_loss_skill": all(
                        item["relative_log_loss_reduction"] > 0
                        for item in fold_metrics.values()
                    ),
                    "opportunity_rates": _opportunity_rates(
                        table,
                        transitions,
                        risk,
                    ),
                }
            )
            endpoints[risk] = endpoint

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
    result = {
        "schema": (
            "adaptive-gain-villavicencio-focal-excluded-opportunity-cv-v1"
        ),
        "date": "2026-09-28",
        "status": (
            "retrospective_repair_signal_present"
            if all(
                primary[risk]["all_folds_converged"]
                and primary[risk]["relative_log_loss_reduction"] > 0
                for risk in ("gain", "loss")
            )
            else "retrospective_repair_mixed"
        ),
        "analysis_status": (
            "post_leakage_repair; retrospective contemporaneous opportunity "
            "analysis; not preregistered or causal"
        ),
        "primary_scope": PRIMARY_SCOPE,
        "published_phenological_overlap_used": False,
        "published_aggregate_flower_abundance_used": False,
        "focal_response_excluded_from_opportunity": True,
        "scopes": scopes,
        "ecological_read": (
            "A positive result means that weekly temporal opportunity rebuilt "
            "without the focal dyad response carries reproducible information "
            "about annual link dynamics across held-out response transitions."
        ),
        "claim_ceiling": (
            "Contemporaneous focal-response-excluded opportunity association "
            "only. This is not strict prospective forecasting, a causal "
            "phenology effect, decision equivalence, or routeability."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
