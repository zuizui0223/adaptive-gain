"""Summarize post-result annual link-frequency threshold sensitivity."""

from __future__ import annotations
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

THRESHOLDS = (2, 3)
TRANSITIONS = ("2008->2009", "2009->2010", "2010->2011")


def _read(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _log_loss(rows, field):
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row[field]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _brier(rows, field):
    return sum(
        (float(row[field]) - int(row["outcome"])) ** 2
        for row in rows
    ) / len(rows)


def _auc(rows):
    y = [int(row["outcome"]) for row in rows]
    p = [float(row["model_probability"]) for row in rows]
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
    model_ll = _log_loss(rows, "model_probability")
    null_ll = _log_loss(rows, "null_probability")
    model_brier = _brier(rows, "model_probability")
    null_brier = _brier(rows, "null_probability")
    return {
        "n": len(rows),
        "events": sum(int(row["outcome"]) for row in rows),
        "roc_auc": _auc(rows),
        "relative_log_loss_reduction": (
            (null_ll - model_ll) / null_ll if null_ll else None
        ),
        "brier_improvement": null_brier - model_brier,
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
                int(row["threshold"]),
                row["risk_set"],
                row["transition"],
            )
        ].append(row)
    receipts = defaultdict(list)
    for row in folds:
        receipts[(int(row["threshold"]), row["risk_set"])].append(row)

    thresholds = {}
    for threshold in THRESHOLDS:
        endpoints = {}
        for risk in ("gain", "loss"):
            pooled = []
            fold_metrics = {}
            for transition in TRANSITIONS:
                rows = grouped[(threshold, risk, transition)]
                if not rows:
                    raise SystemExit(
                        f"{threshold}/{risk}/{transition}: missing predictions"
                    )
                pooled.extend(rows)
                fold_metrics[transition] = _metrics(rows)

            state = receipts[(threshold, risk)]
            if len(state) != len(TRANSITIONS):
                raise SystemExit(
                    f"{threshold}/{risk}: incorrect fold receipt count"
                )
            if not all(
                _bool(row["converged"])
                and int(row["finite_coefficient_count"])
                == int(row["coefficient_count"])
                for row in state
            ):
                raise SystemExit(
                    f"{threshold}/{risk}: model convergence failure"
                )

            endpoint = _metrics(pooled)
            endpoint["folds"] = fold_metrics
            endpoint["positive_log_loss_folds"] = sum(
                fold["relative_log_loss_reduction"] > 0
                for fold in fold_metrics.values()
            )
            endpoints[risk] = endpoint
        thresholds[str(threshold)] = endpoints

    green = all(
        thresholds[str(threshold)][risk]["roc_auc"] > 0.5
        and thresholds[str(threshold)][risk]["relative_log_loss_reduction"] > 0
        and thresholds[str(threshold)][risk]["positive_log_loss_folds"] == 3
        for threshold in THRESHOLDS
        for risk in ("gain", "loss")
    )

    result = {
        "schema": (
            "adaptive-gain-villavicencio-link-frequency-threshold-audit-v1"
        ),
        "date": "2026-09-29",
        "status": (
            "retrospective_threshold_robustness_green"
            if green
            else "retrospective_threshold_robustness_mixed"
        ),
        "analysis_status": (
            "post-result >=2 and >=3 visit threshold sensitivity; "
            "not confirmatory"
        ),
        "scope": "strict_core_2008_2011",
        "thresholds": thresholds,
        "ecological_read": (
            "If green, the repaired current-state opportunity association "
            "persists after singleton links and, separately, links with fewer "
            "than three observed visits are prevented from defining a positive "
            "annual link state."
        ),
        "claim_ceiling": (
            "Frequency-threshold robustness only. This is not a detection "
            "model, true-absence analysis, causal test, decision-equivalence "
            "test, or routeability test."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
