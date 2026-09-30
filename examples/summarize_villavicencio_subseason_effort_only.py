"""Summarize held-out effort-only discrimination of subseason gain/loss."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


EXPECTED_FOLDS = {
    "strict_dated_core_2008_2010": 6,
    "core_sites_2008_2011": 8,
    "all_2007_2011": 10,
}


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
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
    model_ll = _log_loss(rows, "model_probability")
    null_ll = _log_loss(rows, "null_probability")
    model_brier = _brier(rows, "model_probability")
    null_brier = _brier(rows, "null_probability")
    return {
        "n": len(rows),
        "events": sum(int(row["outcome"]) for row in rows),
        "roc_auc": _auc(rows),
        "model_log_loss": model_ll,
        "null_log_loss": null_ll,
        "relative_log_loss_reduction": (
            None if null_ll == 0 else (null_ll - model_ll) / null_ll
        ),
        "brier_improvement": null_brier - model_brier,
    }


def main() -> None:
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
            )
        ].append(row)

    fold_groups = defaultdict(list)
    for row in folds:
        fold_groups[(row["analysis_scope"], row["risk_set"])].append(row)

    scopes = {}
    for scope, expected in EXPECTED_FOLDS.items():
        endpoints = {}
        for risk in ("gain", "loss"):
            transitions = sorted(
                transition
                for s, r, transition in grouped
                if s == scope and r == risk
            )
            if len(transitions) != expected:
                raise SystemExit(
                    f"{scope}/{risk}: expected {expected} folds, found "
                    f"{len(transitions)}"
                )

            pooled = []
            fold_metrics = {}
            for transition in transitions:
                rows = grouped[(scope, risk, transition)]
                pooled.extend(rows)
                fold_metrics[transition] = _metrics(rows)

            receipts = fold_groups[(scope, risk)]
            all_converged = (
                len(receipts) == expected
                and all(
                    _bool(row["converged"])
                    and int(row["coefficient_count"])
                    == int(row["finite_coefficient_count"])
                    for row in receipts
                )
            )

            endpoint = _metrics(pooled)
            endpoint["folds"] = fold_metrics
            endpoint["all_folds_converged"] = all_converged
            endpoint["positive_log_loss_fold_count"] = sum(
                metric["relative_log_loss_reduction"] > 0
                for metric in fold_metrics.values()
            )
            endpoint["fold_count"] = expected
            endpoints[risk] = endpoint

        scopes[scope] = {"endpoints": endpoints}

    primary = scopes["strict_dated_core_2008_2010"]["endpoints"]
    result = {
        "schema": "adaptive-gain-villavicencio-subseason-effort-only-cv-v1",
        "date": "2026-09-29",
        "status": (
            "effort_only_predictive_signal_material"
            if all(
                primary[risk]["roc_auc"] > 0.5
                and primary[risk]["relative_log_loss_reduction"] > 0
                for risk in ("gain", "loss")
            )
            else "effort_only_signal_mixed"
        ),
        "analysis_status": (
            "post-result detection-bias diagnostic; the predictors are focal-"
            "plant census counts, not ecological mechanism variables"
        ),
        "predictors": [
            "previous-period focal-plant 5-min census count",
            "current-period focal-plant 5-min census count",
        ],
        "scopes": scopes,
        "ecological_read": (
            "If the effort-only model discriminates held-out gain/loss, observed "
            "binary turnover is materially entangled with observation effort. "
            "Because effort is partly endogenous to flowering availability, this "
            "does not imply pure observer bias; it does block identification of "
            "true rewiring from binary zero/nonzero states."
        ),
        "claim_ceiling": (
            "Detection-bias diagnostic only. Do not interpret model skill as an "
            "ecological mechanism or use it to estimate the fraction of true "
            "rewiring events."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
