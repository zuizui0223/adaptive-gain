"""Diagnose observed gain/loss direction from the exact detection identity.

For each dyad with an observed binary change, use transition-specific fitted
per-census detection probabilities and the dyad's focal-plant census counts to
compute period-level detection probabilities q_previous and q_current.

Under the persistent-latent-link counterfactual, the exact observation identity
implies P(observed gain)-P(observed loss) = q_current-q_previous.

The resulting score is a mechanistic detection diagnostic, not an independent
ecological predictor and not an estimator of the true fraction of rewiring.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from adaptive_gain.detection_effort_identity import (
    persistent_transition_from_census_effort,
)


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _auc(y, score):
    positives = sum(y)
    negatives = len(y) - positives
    if positives == 0 or negatives == 0:
        return None

    ordered = sorted(zip(score, y), key=lambda item: item[0])
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


def _summary(rows):
    if not rows:
        return {
            "changed_rows": 0,
            "observed_gain": 0,
            "observed_loss": 0,
            "auc_detection_q_difference_gain_over_loss": None,
            "auc_raw_census_difference_gain_over_loss": None,
        }

    y = [int(row["observed_direction"] == "gain") for row in rows]
    q_score = [row["q_difference"] for row in rows]
    census_score = [row["census_difference"] for row in rows]
    gains = [row for row in rows if row["observed_direction"] == "gain"]
    losses = [row for row in rows if row["observed_direction"] == "loss"]

    return {
        "changed_rows": len(rows),
        "observed_gain": len(gains),
        "observed_loss": len(losses),
        "auc_detection_q_difference_gain_over_loss": _auc(y, q_score),
        "auc_raw_census_difference_gain_over_loss": _auc(
            y,
            census_score,
        ),
        "mean_q_difference_observed_gain": (
            sum(row["q_difference"] for row in gains) / len(gains)
            if gains
            else None
        ),
        "mean_q_difference_observed_loss": (
            sum(row["q_difference"] for row in losses) / len(losses)
            if losses
            else None
        ),
        "fraction_gain_with_q_current_gt_previous": (
            sum(row["q_difference"] > 0 for row in gains) / len(gains)
            if gains
            else None
        ),
        "fraction_loss_with_q_current_lt_previous": (
            sum(row["q_difference"] < 0 for row in losses) / len(losses)
            if losses
            else None
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census_rate_table", type=Path)
    parser.add_argument("detection_result", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    table = _read(args.census_rate_table)
    detection = json.loads(
        args.detection_result.read_text(encoding="utf-8")
    )
    transitions = detection["transitions"]

    rows = []
    for row in table:
        previous_present = int(row["previous_success_censuses"]) > 0
        current_present = int(row["current_success_censuses"]) > 0
        if previous_present == current_present:
            continue

        transition = row["transition"]
        fit = transitions[transition]
        params = fit["parameters"]
        identity = persistent_transition_from_census_effort(
            p_previous=float(params["p_previous"]),
            n_previous=int(row["previous_trials"]),
            p_current=float(params["p_current"]),
            n_current=int(row["current_trials"]),
        )

        direct_difference = (
            identity["gain"] - identity["loss"]
        )
        if not math.isclose(
            direct_difference,
            identity["q_current"] - identity["q_previous"],
            rel_tol=0,
            abs_tol=1e-12,
        ):
            raise SystemExit("detection gain-loss identity failed")

        rows.append(
            {
                "transition": transition,
                "identifiability_status": fit[
                    "identifiability_status"
                ],
                "observed_direction": (
                    "gain" if current_present else "loss"
                ),
                "q_previous": identity["q_previous"],
                "q_current": identity["q_current"],
                "q_difference": (
                    identity["q_current"]
                    - identity["q_previous"]
                ),
                "census_difference": (
                    int(row["current_trials"])
                    - int(row["previous_trials"])
                ),
            }
        )

    per_transition = {}
    for transition in transitions:
        selected = [
            row for row in rows if row["transition"] == transition
        ]
        per_transition[transition] = {
            "identifiability_status": transitions[transition][
                "identifiability_status"
            ],
            **_summary(selected),
        }

    identified = [
        row
        for row in rows
        if row["identifiability_status"] == "IDENTIFIED"
    ]

    result = {
        "schema": (
            "adaptive-gain-villavicencio-detection-effort-identity-audit-v1"
        ),
        "date": "2026-09-30",
        "status": "persistent_link_detection_direction_diagnostic_complete",
        "analysis_status": (
            "deterministic post-detection-fit observation-process diagnostic; "
            "not an ecological model and not an independent validation test"
        ),
        "exact_identity": (
            "for a persistent latent link, "
            "P(observed gain)-P(observed loss)=q_current-q_previous"
        ),
        "all_six_transitions": _summary(rows),
        "identified_five_transition_subset": _summary(identified),
        "per_transition": per_transition,
        "interpretation": {
            "allowed": (
                "quantify how changes in period-level detectability alone would "
                "bias the direction of observed binary gain/loss for a persistent "
                "latent interaction"
            ),
            "forbidden": (
                "infer that a specific observed gain/loss is false, estimate the "
                "biological fraction of turnover, or treat fitted q values as "
                "ground-truth detection probabilities"
            ),
        },
        "claim_ceiling": (
            "Mechanistic observation-map diagnostic only. A high AUC means the "
            "direction of observed changes is aligned with period-level "
            "detectability differences under the persistent-link counterfactual; "
            "it does not prove that latent links were actually persistent."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
