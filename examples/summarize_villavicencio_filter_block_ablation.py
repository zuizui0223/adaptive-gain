"""Summarize frozen leave-one-block-out temporal CV for conventional filters."""

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
BLOCK_MODELS = {
    "phenology": "drop_phenology",
    "abundance": "drop_abundance",
    "plant_morphology": "drop_plant_morphology",
    "pollinator_morphology": "drop_pollinator_morphology",
}


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _log_loss(rows):
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row["probability"]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _brier(rows):
    return sum(
        (float(row["probability"]) - int(row["outcome"])) ** 2
        for row in rows
    ) / len(rows)


def _classification(delta_pooled, fold_deltas):
    positive_folds = sum(value > 0 for value in fold_deltas.values())
    if delta_pooled > 0 and positive_folds == len(fold_deltas):
        return "reproducible_incremental_information"
    if delta_pooled > 0 and positive_folds > 0:
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
    for row in predictions:
        grouped[
            (
                row["analysis_scope"],
                row["risk_set"],
                row["transition"],
                row["model"],
            )
        ].append(row)

    fold_state = defaultdict(dict)
    for row in folds:
        key = (
            row["analysis_scope"],
            row["risk_set"],
            row["held_out_transition"],
        )
        fold_state[key][row["model"]] = row

    result_scopes = {}
    for scope, expected_fold_count in EXPECTED_FOLDS.items():
        endpoints = {}
        for risk in ("gain", "loss"):
            transitions = sorted(
                {
                    transition
                    for s, r, transition, model in grouped
                    if s == scope and r == risk and model == "full"
                }
            )
            if len(transitions) != expected_fold_count:
                raise SystemExit(
                    f"{scope}/{risk}: expected {expected_fold_count} held-out transitions, "
                    f"found {len(transitions)}"
                )

            full_rows = []
            for transition in transitions:
                full_rows.extend(grouped[(scope, risk, transition, "full")])
            full_log_loss = _log_loss(full_rows)
            full_brier = _brier(full_rows)

            blocks = {}
            for block, drop_model in BLOCK_MODELS.items():
                drop_rows = []
                fold_deltas = {}
                fold_brier_deltas = {}
                for transition in transitions:
                    full_fold = grouped[(scope, risk, transition, "full")]
                    drop_fold = grouped[(scope, risk, transition, drop_model)]
                    if len(full_fold) != len(drop_fold):
                        raise SystemExit(
                            f"{scope}/{risk}/{transition}/{block}: row count mismatch"
                        )
                    drop_rows.extend(drop_fold)
                    fold_deltas[transition] = (
                        _log_loss(drop_fold) - _log_loss(full_fold)
                    )
                    fold_brier_deltas[transition] = (
                        _brier(drop_fold) - _brier(full_fold)
                    )

                drop_log_loss = _log_loss(drop_rows)
                drop_brier = _brier(drop_rows)
                delta_log_loss = drop_log_loss - full_log_loss
                delta_brier = drop_brier - full_brier
                blocks[block] = {
                    "drop_model": drop_model,
                    "n": len(drop_rows),
                    "full_log_loss": full_log_loss,
                    "drop_log_loss": drop_log_loss,
                    "delta_log_loss_drop_minus_full": delta_log_loss,
                    "full_brier": full_brier,
                    "drop_brier": drop_brier,
                    "delta_brier_drop_minus_full": delta_brier,
                    "positive_log_loss_fold_count": sum(
                        value > 0 for value in fold_deltas.values()
                    ),
                    "fold_count": len(fold_deltas),
                    "fold_delta_log_loss": fold_deltas,
                    "fold_delta_brier": fold_brier_deltas,
                    "classification": _classification(delta_log_loss, fold_deltas),
                }

            endpoint_folds = [
                fold_state[(scope, risk, transition)]
                for transition in transitions
            ]
            expected_models = {"full", *BLOCK_MODELS.values()}
            all_models_present = all(
                set(row) == expected_models for row in endpoint_folds
            )
            all_converged = all(
                entry["converged"].strip().lower() == "true"
                for row in endpoint_folds
                for entry in row.values()
            )
            endpoints[risk] = {
                "full_model_n": len(full_rows),
                "full_model_log_loss": full_log_loss,
                "full_model_brier": full_brier,
                "all_models_present": all_models_present,
                "all_folds_converged": all_converged,
                "blocks": blocks,
            }

        result_scopes[scope] = {
            "role": "primary" if scope == PRIMARY_SCOPE else "sensitivity",
            "endpoints": endpoints,
        }

    primary = result_scopes[PRIMARY_SCOPE]["endpoints"]
    result = {
        "schema": "adaptive-gain-villavicencio-filter-block-ablation-v1",
        "analysis_scope": "annual detection-sensitive fallback",
        "primary_scope": PRIMARY_SCOPE,
        "decision_equivalence_inferred": False,
        "blocks_frozen_before_result": list(BLOCK_MODELS),
        "classification_rule": {
            "reproducible_incremental_information": (
                "pooled held-out log-loss worsens when the block is removed and "
                "the same sign occurs in every primary held-out transition"
            ),
            "positive_but_fold_unstable": (
                "pooled held-out log-loss worsens when removed but the sign is "
                "not positive in every held-out transition"
            ),
            "no_reproducible_incremental_information": (
                "pooled held-out log-loss does not worsen when the block is removed"
            ),
        },
        "scopes": result_scopes,
        "primary_summary": {
            risk: {
                block: primary[risk]["blocks"][block]["classification"]
                for block in BLOCK_MODELS
            }
            for risk in ("gain", "loss")
        },
        "claim_ceiling": (
            "This ablation identifies predictive information blocks in held-out "
            "annual link dynamics. It does not identify causal trait effects, "
            "decision-equivalence classes, or routeability."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
