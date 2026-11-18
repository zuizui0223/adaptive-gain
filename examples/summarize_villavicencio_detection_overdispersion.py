"""Summarize beta-binomial detection-overdispersion stress test."""

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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fits", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows = _read(args.fits)
    by_transition = {row["transition"]: row for row in rows}
    if set(by_transition) != set(TRANSITIONS):
        raise SystemExit("overdispersion transition set mismatch")

    transitions = {}
    preferred = 0
    boundary = 0

    for transition in TRANSITIONS:
        row = by_transition[transition]
        pref = _bool(row["beta_binomial_preferred"])
        bound = _bool(row["any_state_transition_boundary"])
        preferred += int(pref)
        boundary += int(bound)

        transitions[transition] = {
            "binomial_aic": float(row["binomial_aic"]),
            "beta_binomial_aic": float(row["beta_binomial_aic"]),
            "delta_aic_beta_minus_binomial": float(
                row["delta_aic_beta_minus_binomial"]
            ),
            "beta_binomial_preferred": pref,
            "all_starts_converged": _bool(
                row["all_starts_converged"]
            ),
            "multi_start_nll_range": float(
                row["multi_start_nll_range"]
            ),
            "parameters": {
                key: float(row[key])
                for key in (
                    "psi",
                    "gamma",
                    "epsilon",
                    "p_previous",
                    "p_current",
                    "kappa_previous",
                    "kappa_current",
                )
            },
            "gamma_logit_at_boundary": _bool(
                row["gamma_logit_at_boundary"]
            ),
            "epsilon_logit_at_boundary": _bool(
                row["epsilon_logit_at_boundary"]
            ),
            "any_state_transition_boundary": bound,
        }

    model_sensitive = preferred >= 5 and boundary >= 3

    result = {
        "schema": (
            "adaptive-gain-villavicencio-detection-overdispersion-result-v1"
        ),
        "date": "2026-09-29",
        "status": (
            "latent_transition_inference_model_sensitive"
            if model_sensitive
            else "overdispersion_stress_not_decisive"
        ),
        "analysis_status": (
            "post-identifiability observation-model robustness stress test; "
            "not a latent ecological effect analysis"
        ),
        "transition_count": len(TRANSITIONS),
        "beta_binomial_preferred_transition_count": preferred,
        "state_transition_boundary_count": boundary,
        "model_sensitivity_rule": (
            "flag model sensitivity when beta-binomial AIC is at least 2 "
            "better in >=5/6 transitions and gamma/epsilon hits the frozen "
            "state-transition logit boundary in >=3/6 transitions"
        ),
        "transitions": transitions,
        "ecological_read": {
            "supported": (
                "The stress test asks whether the apparent latent transition "
                "rates survive extra-binomial heterogeneity in repeated "
                "interaction detections."
            ),
            "consequence_if_sensitive": (
                "A model-sensitive result means simple-binomial latent gain/"
                "loss estimates are not robust enough to restore an ecological "
                "rewiring claim."
            ),
        },
        "not_established": [
            "the beta-binomial model as the true detection process",
            "true latent rewiring rates",
            "causal opportunity effects",
            "decision-equivalence classes",
            "environmental routeability",
        ],
        "claim_ceiling": (
            "Observation-model sensitivity only. If the frozen sensitivity "
            "rule fires, detection-corrected rewiring remains model-dependent "
            "and must not be promoted as an identified ecological response."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
