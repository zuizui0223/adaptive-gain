"""Summarize effort-standardized Villavicencio census-rate CV."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


TRANSITIONS = (
    "2008_early->2008_mid",
    "2008_mid->2008_late",
    "2009_early->2009_mid",
    "2009_mid->2009_late",
    "2010_early->2010_mid",
    "2010_mid->2010_late",
)
MODELS = ("history_only", "history_plus_opportunity")


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _metrics(rows):
    loss = 0.0
    brier_num = 0.0
    total_trials = 0
    total_successes = 0

    for row in rows:
        successes = int(row["successes"])
        trials = int(row["trials"])
        p = min(max(float(row["probability"]), 1e-8), 1 - 1e-8)
        failures = trials - successes
        loss -= successes * math.log(p) + failures * math.log(1 - p)
        observed_rate = successes / trials
        brier_num += trials * (p - observed_rate) ** 2
        total_trials += trials
        total_successes += successes

    return {
        "dyad_transition_rows": len(rows),
        "dyad_census_trials": total_trials,
        "positive_censuses": total_successes,
        "observed_positive_census_fraction": (
            total_successes / total_trials
        ),
        "per_census_log_loss": loss / total_trials,
        "trial_weighted_brier": brier_num / total_trials,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("table_summary", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("folds", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    table_summary = json.loads(
        args.table_summary.read_text(encoding="utf-8")
    )
    predictions = _read(args.predictions)
    folds = _read(args.folds)

    grouped = defaultdict(list)
    for row in predictions:
        grouped[(row["transition"], row["model"])].append(row)

    fold_state = defaultdict(dict)
    for row in folds:
        fold_state[row["held_out_transition"]][row["model"]] = row

    pooled = {model: [] for model in MODELS}
    transition_results = {}

    for transition in TRANSITIONS:
        metrics = {}
        for model in MODELS:
            rows = grouped[(transition, model)]
            if not rows:
                raise SystemExit(
                    f"{transition}/{model}: no predictions"
                )
            pooled[model].extend(rows)
            metrics[model] = _metrics(rows)

            receipt = fold_state[transition].get(model)
            if receipt is None:
                raise SystemExit(
                    f"{transition}/{model}: missing fold receipt"
                )
            if not (
                _bool(receipt["converged"])
                and int(receipt["coefficient_count"])
                == int(receipt["finite_coefficient_count"])
            ):
                raise SystemExit(
                    f"{transition}/{model}: model convergence failure"
                )

        improvement = (
            metrics["history_only"]["per_census_log_loss"]
            - metrics["history_plus_opportunity"][
                "per_census_log_loss"
            ]
        )
        brier_improvement = (
            metrics["history_only"]["trial_weighted_brier"]
            - metrics["history_plus_opportunity"][
                "trial_weighted_brier"
            ]
        )
        transition_results[transition] = {
            "history_only": metrics["history_only"],
            "history_plus_opportunity": (
                metrics["history_plus_opportunity"]
            ),
            "opportunity_increment": {
                "per_census_log_loss_improvement": improvement,
                "trial_weighted_brier_improvement": (
                    brier_improvement
                ),
            },
        }

    pooled_metrics = {
        model: _metrics(rows)
        for model, rows in pooled.items()
    }
    pooled_logloss_improvement = (
        pooled_metrics["history_only"]["per_census_log_loss"]
        - pooled_metrics["history_plus_opportunity"][
            "per_census_log_loss"
        ]
    )
    pooled_brier_improvement = (
        pooled_metrics["history_only"]["trial_weighted_brier"]
        - pooled_metrics["history_plus_opportunity"][
            "trial_weighted_brier"
        ]
    )
    positive_folds = sum(
        transition_results[t]["opportunity_increment"][
            "per_census_log_loss_improvement"
        ]
        > 0
        for t in TRANSITIONS
    )

    reproducible = (
        pooled_logloss_improvement > 0
        and positive_folds == len(TRANSITIONS)
    )

    result = {
        "schema": (
            "adaptive-gain-villavicencio-census-rate-cv-v1"
        ),
        "date": "2026-09-29",
        "status": (
            "effort_standardized_opportunity_increment_reproducible"
            if reproducible
            else "effort_standardized_opportunity_increment_mixed"
        ),
        "analysis_status": (
            "post-effort-audit ecological association using a binomial "
            "5-min-census incidence response; not ecological rewiring"
        ),
        "primary_scope": "strict_dated_core_2008_2010",
        "table_audit": table_summary,
        "pooled": {
            "history_only": pooled_metrics["history_only"],
            "history_plus_opportunity": (
                pooled_metrics["history_plus_opportunity"]
            ),
            "opportunity_increment": {
                "per_census_log_loss_improvement": (
                    pooled_logloss_improvement
                ),
                "trial_weighted_brier_improvement": (
                    pooled_brier_improvement
                ),
                "positive_log_loss_folds": (
                    f"{positive_folds}/{len(TRANSITIONS)}"
                ),
                "classification": (
                    "reproducible_incremental_information"
                    if reproducible
                    else "not_reproducible_under_frozen_rule"
                ),
            },
        },
        "transitions": transition_results,
        "ecological_read": (
            "The response is standardized by observed focal-plant census "
            "effort. A positive frozen result means focal-response-excluded "
            "current site-week opportunity improves held-out prediction of "
            "per-census interaction incidence beyond the previous-period "
            "interaction rate."
        ),
        "not_established": [
            "latent true link occupancy",
            "ecological rewiring",
            "causal effect of opportunity",
            "sampling-process-independent mechanism",
            "independent dyad-census replicates",
            "strict prospective forecasting",
            "decision-equivalence classes",
            "environmental routeability",
        ],
        "claim_ceiling": (
            "Effort-standardized observed interaction-incidence association "
            "only. The binomial denominator removes unequal focal-plant "
            "census count from the response scale, but the analysis does not "
            "identify latent links, true rewiring, causality, or routeability."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
