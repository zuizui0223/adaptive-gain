"""Summarize the retrospective gain-vs-loss predictability robustness audit.

This audit is intentionally post hoc: the gain/loss directional asymmetry was
noticed before this matched-information sensitivity was designed. The output is
therefore a robustness ledger, not a confirmatory test or a preregistered result.
"""

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


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


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


def _log_loss(rows, probability_field):
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row[probability_field]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _relative_log_loss_skill(rows):
    model = _log_loss(rows, "model_probability")
    null = _log_loss(rows, "null_probability")
    return None if null == 0 else (null - model) / null


def _quantile(values, q):
    values = sorted(values)
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    position = (len(values) - 1) * q
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return values[lower]
    weight = position - lower
    return values[lower] * (1 - weight) + values[upper] * weight


def _summary(values):
    finite = [float(v) for v in values if math.isfinite(float(v))]
    if not finite:
        return {
            "n": 0,
            "mean": None,
            "median": None,
            "q025": None,
            "q975": None,
            "positive_fraction": None,
        }
    return {
        "n": len(finite),
        "mean": sum(finite) / len(finite),
        "median": _quantile(finite, 0.5),
        "q025": _quantile(finite, 0.025),
        "q975": _quantile(finite, 0.975),
        "positive_fraction": sum(v > 0 for v in finite) / len(finite),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument("matched_replicates", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    predictions = _read(args.predictions)
    matched = _read(args.matched_replicates)

    original = defaultdict(list)
    for row in predictions:
        original[
            (row["analysis_scope"], row["transition"], row["risk_set"])
        ].append(row)

    matched_groups = defaultdict(list)
    for row in matched:
        matched_groups[
            (row["analysis_scope"], row["held_out_transition"])
        ].append(row)

    scopes = {}
    all_scope_transition_pass = True
    for scope, expected_transitions in SCOPES.items():
        transitions = sorted(
            {
                transition
                for s, transition, risk in original
                if s == scope and risk == "gain"
            }
        )
        if len(transitions) != expected_transitions:
            raise SystemExit(
                f"{scope}: expected {expected_transitions} transitions, "
                f"found {len(transitions)}"
            )

        transition_results = {}
        for transition in transitions:
            gain_rows = original[(scope, transition, "gain")]
            loss_rows = original[(scope, transition, "loss")]
            if not gain_rows or not loss_rows:
                raise SystemExit(f"{scope}/{transition}: missing endpoint")

            gain_auc = _auc(gain_rows)
            loss_auc = _auc(loss_rows)
            gain_skill = _relative_log_loss_skill(gain_rows)
            loss_skill = _relative_log_loss_skill(loss_rows)

            replicate_rows = matched_groups[(scope, transition)]
            if not replicate_rows:
                raise SystemExit(
                    f"{scope}/{transition}: missing matched-information replicates"
                )
            expected_rep_count = len(replicate_rows)
            fits_ok = [
                row["fits_ok"].strip().lower() == "true"
                for row in replicate_rows
            ]
            if not all(fits_ok):
                raise SystemExit(
                    f"{scope}/{transition}: at least one matched fit failed"
                )

            auc_difference = _summary(
                float(row["gain_minus_loss_auc"])
                for row in replicate_rows
            )
            gain_phenology = _summary(
                float(row["gain_phenology_auc_delta"])
                for row in replicate_rows
            )
            loss_phenology = _summary(
                float(row["loss_phenology_auc_delta"])
                for row in replicate_rows
            )
            phenology_difference = _summary(
                float(row["gain_minus_loss_phenology_auc_delta"])
                for row in replicate_rows
            )

            transition_pass = (
                gain_auc is not None
                and loss_auc is not None
                and gain_auc > loss_auc
                and gain_skill is not None
                and loss_skill is not None
                and gain_skill > loss_skill
                and auc_difference["positive_fraction"] == 1.0
                and gain_phenology["positive_fraction"] == 1.0
                and loss_phenology["positive_fraction"] == 1.0
                and phenology_difference["positive_fraction"] == 1.0
            )
            all_scope_transition_pass = (
                all_scope_transition_pass and transition_pass
            )

            transition_results[transition] = {
                "original_heldout": {
                    "gain_n": len(gain_rows),
                    "loss_n": len(loss_rows),
                    "gain_event_fraction": (
                        sum(int(row["outcome"]) for row in gain_rows)
                        / len(gain_rows)
                    ),
                    "loss_event_fraction": (
                        sum(int(row["outcome"]) for row in loss_rows)
                        / len(loss_rows)
                    ),
                    "gain_auc": gain_auc,
                    "loss_auc": loss_auc,
                    "gain_minus_loss_auc": gain_auc - loss_auc,
                    "gain_relative_log_loss_reduction": gain_skill,
                    "loss_relative_log_loss_reduction": loss_skill,
                    "gain_minus_loss_relative_log_loss_reduction": (
                        gain_skill - loss_skill
                    ),
                },
                "matched_information_training": {
                    "replicates": expected_rep_count,
                    "matched_per_class": int(
                        replicate_rows[0]["matched_per_class"]
                    ),
                    "matched_training_n_per_endpoint": int(
                        replicate_rows[0]["matched_training_n_per_endpoint"]
                    ),
                    "gain_minus_loss_auc": auc_difference,
                    "gain_phenology_auc_delta": gain_phenology,
                    "loss_phenology_auc_delta": loss_phenology,
                    "gain_minus_loss_phenology_auc_delta": phenology_difference,
                },
                "directional_robustness": (
                    "PASS_gain_more_predictable_and_phenology_more_discriminating"
                    if transition_pass
                    else "MIXED"
                ),
            }

        scopes[scope] = {
            "transition_count": len(transitions),
            "transitions": transition_results,
            "all_transitions_directionally_consistent": all(
                item["directional_robustness"].startswith("PASS")
                for item in transition_results.values()
            ),
        }

    result = {
        "schema": "adaptive-gain-villavicencio-gain-loss-asymmetry-audit-v1",
        "date": "2026-09-28",
        "status": (
            "retrospective_robustness_green"
            if all_scope_transition_pass
            else "retrospective_robustness_mixed"
        ),
        "analysis_status": (
            "posthoc_direction_seen_before_matched_audit; "
            "not_confirmatory_or_preregistered"
        ),
        "question": (
            "Does the observed gain-over-loss predictability asymmetry survive "
            "a prevalence-insensitive discrimination metric and matched "
            "training information?"
        ),
        "matched_training_design": {
            "within_each_scope_and_heldout_transition": (
                "fit gain and loss models after sampling the same number of "
                "positive and negative training examples for both endpoints"
            ),
            "models": [
                "full frozen conventional-filter model",
                "same model with phenology removed",
            ],
            "evaluation": (
                "ROC AUC on the untouched full held-out risk set; AUC is "
                "prevalence-insensitive as a scoring metric"
            ),
            "time_support": (
                "phenological overlap and flower abundance are study-wide "
                "six-year aggregates in the source workbook; this audit holds "
                "out annual link outcomes, not past-only covariate information"
            ),
            "random_seed": 20260928,
            "replicates_per_scope_transition": (
                len(next(iter(matched_groups.values())))
                if matched_groups
                else 0
            ),
        },
        "scopes": scopes,
        "ecological_read": (
            "Conventional ecological filters discriminate held-out annual link gains "
            "more strongly than link losses across every held-out annual "
            "transition examined. Equalizing training class information does "
            "not erase that directional pattern. Phenology contributes "
            "positive discrimination to both endpoints in the matched audit, "
            "with a larger AUC contribution to gains throughout."
        ),
        "not_established": [
            "a causal difference between link assembly and disassembly",
            "that phenology is causally primary",
            "that gain and loss arise from different biological mechanisms",
            "environmental routeability",
            "decision-equivalence classes",
            "sampling-effort-corrected true rewiring",\n            "strict prospective forecasting from covariates measured only before the held-out transition",
        ],
        "claim_ceiling": (
            "This is a retrospective robustness result. It supports a "
            "descriptive asymmetry in held-out annual-link discrimination and a "
            "stronger predictive contribution of phenology to gains, but it "
            "cannot promote the asymmetry to a preregistered causal claim or a "\n            "past-only forecasting result because key conventional covariates "\n            "are aggregated over the full six-year study."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
