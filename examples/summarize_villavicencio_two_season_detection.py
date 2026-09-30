"""Summarize frozen two-season detection identifiability diagnostics."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


TRANSITIONS = (
    "2008_early->2008_mid",
    "2008_mid->2008_late",
    "2009_early->2009_mid",
    "2009_mid->2009_late",
    "2010_early->2010_mid",
    "2010_mid->2010_late",
)


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _float(row, key):
    value = row.get(key, "")
    if value is None or str(value).strip() in {"", "NA", "NaN", "nan"}:
        return None
    return float(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fits", type=Path)
    parser.add_argument("posteriors", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    fits = _read(args.fits)
    posteriors = _read(args.posteriors)

    by_transition = {row["transition"]: row for row in fits}
    if set(by_transition) != set(TRANSITIONS):
        raise SystemExit("fit transition set disagrees with frozen gate")

    transitions = {}
    identified_count = 0
    total_observed_gain = 0
    total_observed_loss = 0
    total_expected_gain = 0.0
    total_expected_loss = 0.0

    for transition in TRANSITIONS:
        row = by_transition[transition]
        status = row["identifiability_status"]
        identified_count += int(status == "IDENTIFIED")

        observed_gain = int(row["observed_gain_count"])
        observed_loss = int(row["observed_loss_count"])
        expected_gain = float(row["expected_latent_gain"])
        expected_loss = float(row["expected_latent_loss"])

        total_observed_gain += observed_gain
        total_observed_loss += observed_loss
        total_expected_gain += expected_gain
        total_expected_loss += expected_loss

        transitions[transition] = {
            "n_rows": int(row["n_rows"]),
            "identifiability_status": status,
            "optimizer": {
                "optim_result_count": int(row["optim_result_count"]),
                "best_start_index": int(row["best_start_index"]),
                "best_nll": float(row["best_nll"]),
                "multi_start_nll_range": float(
                    row["multi_start_nll_range"]
                ),
                "best_convergence": int(row["best_convergence"]),
                "all_starts_converged": _bool(
                    row["all_starts_converged"]
                ),
            },
            "curvature": {
                "hessian_positive_definite": _bool(
                    row["hessian_positive_definite"]
                ),
                "min_hessian_eigenvalue": _float(
                    row, "min_hessian_eigenvalue"
                ),
                "hessian_condition_number": _float(
                    row, "hessian_condition_number"
                ),
                "finite_logit_standard_errors": _bool(
                    row["finite_logit_standard_errors"]
                ),
            },
            "parameters": {
                name: float(row[name])
                for name in (
                    "psi",
                    "gamma",
                    "epsilon",
                    "p_previous",
                    "p_current",
                )
            },
            "posterior_expected_states": {
                "stable_absent": float(
                    row["expected_latent_stable_absent"]
                ),
                "gain": expected_gain,
                "loss": expected_loss,
                "stable_present": float(
                    row["expected_latent_stable_present"]
                ),
            },
            "observed_binary_changes": {
                "gain": observed_gain,
                "loss": observed_loss,
            },
            "mean_posterior_true_transition_among_observed": {
                "gain": _float(
                    row,
                    "mean_true_gain_posterior_among_observed_gains",
                ),
                "loss": _float(
                    row,
                    "mean_true_loss_posterior_among_observed_losses",
                ),
            },
        }

    promotion_allowed = identified_count >= 5

    result = {
        "schema": (
            "adaptive-gain-villavicencio-two-season-detection-result-v1"
        ),
        "date": "2026-09-29",
        "status": (
            "latent_link_detection_identified_enough_for_sensitivity"
            if promotion_allowed
            else "latent_link_rewiring_not_identified_under_simple_detection_model"
        ),
        "analysis_status": (
            "post-effort-audit latent-state identifiability diagnostic; "
            "no opportunity effect fitted"
        ),
        "primary_scope": "strict_dated_core_2008_2010",
        "transition_count": len(TRANSITIONS),
        "identified_transition_count": identified_count,
        "required_identified_transition_count": 5,
        "promotion_to_latent_opportunity_model_allowed": promotion_allowed,
        "transitions": transitions,
        "aggregate_descriptive": {
            "observed_binary_gain_count": total_observed_gain,
            "observed_binary_loss_count": total_observed_loss,
            "sum_expected_latent_gain": total_expected_gain,
            "sum_expected_latent_loss": total_expected_loss,
            "note": (
                "Expected latent counts are model-based posterior sums and "
                "must not be read as observed ecological events."
            ),
        },
        "ecological_read": {
            "supported": (
                "Repeated 5-min censuses were used to ask whether latent "
                "interaction states can be separated from non-detection under "
                "a simple two-season occupancy model."
            ),
            "consequence_if_failed": (
                "If fewer than five transitions pass the frozen gate, the "
                "data do not identify a defensible detection-corrected "
                "rewiring response under this model; binary observed-link "
                "turnover remains the honest response label."
            ),
        },
        "not_established": [
            "the simple occupancy model is the true ecological process",
            "true ecological rewiring",
            "causal opportunity effects",
            "decision-equivalence classes",
            "environmental routeability",
        ],
        "claim_ceiling": (
            "Latent-state identifiability diagnostic only. A failed gate "
            "blocks detection-corrected rewiring promotion rather than being "
            "repaired by changing the model after seeing the result."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
