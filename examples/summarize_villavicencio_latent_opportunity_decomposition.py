"""Summarize state-versus-detection opportunity decomposition."""

from __future__ import annotations

import argparse
import csv
import json
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
MODELS = (
    "base",
    "detection_only",
    "state_only",
    "state_plus_detection",
)


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("models", type=Path)
    parser.add_argument("posteriors", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows = _read(args.models)
    grouped = {
        (row["transition"], row["model"]): row
        for row in rows
    }
    expected = {
        (transition, model)
        for transition in TRANSITIONS
        for model in MODELS
    }
    if set(grouped) != expected:
        raise SystemExit("latent decomposition model surface incomplete")

    transitions = {}
    state_support_count = 0
    detection_support_count = 0
    strict_state_support_count = 0
    strict_detection_support_count = 0

    for transition in TRANSITIONS:
        item = {}
        for model in MODELS:
            row = grouped[(transition, model)]
            item[model] = {
                "aic": float(row["aic"]),
                "best_nll": float(row["best_nll"]),
                "parameter_count": int(row["parameter_count"]),
                "best_convergence": int(row["best_convergence"]),
                "all_starts_converged": _bool(
                    row["all_starts_converged"]
                ),
                "multi_start_nll_range": float(
                    row["multi_start_nll_range"]
                ),
                "beta_gain": float(row["beta_gain"]),
                "beta_loss": float(row["beta_loss"]),
                "beta_detection": float(row["beta_detection"]),
            }

        base = item["base"]
        detection = item["detection_only"]
        state = item["state_only"]
        both = item["state_plus_detection"]

        # Primary frozen effect rule: this is the rule declared before the
        # opportunity coefficients were inspected. Do not retroactively add
        # optimizer-stability thresholds to redefine this primary result.
        state_supported = (
            both["aic"] <= detection["aic"] - 2
            and both["beta_gain"] > 0
            and both["beta_loss"] < 0
        )
        detection_supported = (
            detection["aic"] <= base["aic"] - 2
            and detection["beta_detection"] > 0
        )

        # Post-result optimizer-reliability sensitivity. This is deliberately
        # reported separately and may only make the interpretation stricter.
        def strict_reliable(model):
            return (
                model["best_convergence"] == 0
                and model["all_starts_converged"]
                and model["multi_start_nll_range"] <= 1e-6
            )

        strict_state_supported = (
            strict_reliable(detection)
            and strict_reliable(both)
            and state_supported
        )
        strict_detection_supported = (
            strict_reliable(base)
            and strict_reliable(detection)
            and detection_supported
        )
        state_support_count += int(state_supported)
        detection_support_count += int(detection_supported)
        strict_state_support_count += int(strict_state_supported)
        strict_detection_support_count += int(strict_detection_supported)

        transitions[transition] = {
            **item,
            "comparisons": {
                "detection_only_delta_aic_vs_base": (
                    detection["aic"] - base["aic"]
                ),
                "state_only_delta_aic_vs_base": (
                    state["aic"] - base["aic"]
                ),
                "both_delta_aic_vs_detection_only": (
                    both["aic"] - detection["aic"]
                ),
                "both_delta_aic_vs_state_only": (
                    both["aic"] - state["aic"]
                ),
                "strict_base_fit_reliable": strict_reliable(base),
                "strict_detection_fit_reliable": strict_reliable(detection),
                "strict_state_fit_reliable": strict_reliable(state),
                "strict_both_fit_reliable": strict_reliable(both),
                "state_component_supported": state_supported,
                "detection_component_supported": detection_supported,
                "strict_state_component_supported": strict_state_supported,
                "strict_detection_component_supported": strict_detection_supported,
            },
        }

    general_state = state_support_count >= 5

    result = {
        "schema": (
            "adaptive-gain-villavicencio-latent-opportunity-decomposition-v1"
        ),
        "date": "2026-09-29",
        "status": (
            "general_latent_state_opportunity_support"
            if general_state
            else "latent_opportunity_state_effect_not_general"
        ),
        "analysis_status": (
            "conditional post-detection-identifiability decomposition; "
            "observational model comparison only"
        ),
        "transition_count": len(TRANSITIONS),
        "state_supported_transition_count": state_support_count,
        "detection_supported_transition_count": detection_support_count,
        "general_state_promotion_rule_met": general_state,
        "post_result_optimizer_reliability_sensitivity": {
            "criterion": "best fit converged, all deterministic starts converged, and multi-start NLL range <= 1e-6",
            "strict_state_supported_transition_count": strict_state_support_count,
            "strict_detection_supported_transition_count": strict_detection_support_count,
            "role": "post-result robustness only; does not redefine the frozen primary rule"
        },
        "transitions": transitions,
        "ecological_read": {
            "state_rule": (
                "A general latent-state opportunity association requires the "
                "state-plus-detection model to beat detection-only by at "
                "least 2 AIC while beta_gain > 0 and beta_loss < 0 in at "
                "least five of six transitions."
            ),
            "detection_rule": (
                "A detection-side association is recorded when detection-only "
                "beats base by at least 2 AIC with beta_detection > 0."
            ),
        },
        "not_established": [
            "causal opportunity effects",
            "the occupancy model as the true ecological process",
            "experimental separation of state and detection",
            "decision-equivalence classes",
            "environmental routeability",
        ],
        "claim_ceiling": (
            "Observational latent-state versus detection decomposition only. "
            "If the five-of-six state rule fails, current opportunity must not "
            "be promoted as a general driver of ecological rewiring even if "
            "some transitions show state-side support."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
