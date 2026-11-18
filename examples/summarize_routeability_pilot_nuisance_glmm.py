"""Combine the pooled Pilot B GLMM fit with the nuisance-only pilot receipt."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def _read_one_csv(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError("nuisance GLMM fit CSV must contain exactly one row")
    return rows[0]


def _truth(value: object) -> bool:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"unrecognized boolean value: {value!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pilot_bundle_json", type=Path)
    parser.add_argument("glmm_fit_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    bundle = json.loads(args.pilot_bundle_json.read_text(encoding="utf-8"))
    if bundle.get("focal_architecture_access_contrast_opened") is not False:
        raise ValueError("pilot bundle does not certify a closed focal contrast")

    pooled = bundle.get("pooled_full_information")
    if not isinstance(pooled, dict):
        raise ValueError("pilot bundle missing pooled_full_information")
    if pooled.get("focal_architecture_contrast_opened") is not False:
        raise ValueError("pooled pilot receipt opened the focal architecture contrast")

    required = {
        "pooled_success_fraction",
        "pooled_timeout_fraction",
        "randomized_individual_dropout_fraction",
        "trials_per_individual",
    }
    missing = sorted(
        key for key in required
        if pooled.get(key) is None
    )
    if missing:
        raise ValueError(
            "pilot bundle missing nuisance values: " + ", ".join(missing)
        )

    fit = _read_one_csv(args.glmm_fit_csv)
    if not _truth(fit["converged"]):
        raise ValueError("nuisance GLMM did not converge")

    values = {
        "pooled_intercept_logit": float(fit["pooled_intercept_logit"]),
        "individual_sd_logit": float(fit["individual_sd_logit"]),
        "colony_sd_logit": float(fit["colony_sd_logit"]),
    }
    if any(not math.isfinite(value) or value < 0 and key.endswith("_sd_logit")
           for key, value in values.items()):
        raise ValueError("invalid nuisance GLMM estimate")

    result = {
        "schema": "adaptive-gain-routeability-pilot-nuisance-glmm-receipt-v1",
        "analysis_role": "pooled B3 nuisance calibration only",
        "focal_architecture_access_contrast_opened": False,
        "pooled_success_fraction": float(pooled["pooled_success_fraction"]),
        "pooled_timeout_fraction": float(pooled["pooled_timeout_fraction"]),
        "randomized_individual_dropout_fraction": float(
            pooled["randomized_individual_dropout_fraction"]
        ),
        "trials_per_individual": int(pooled["trials_per_individual"]),
        **values,
        "colony_count_in_fit": int(fit["colony_count_in_fit"]),
        "individual_count_in_fit": int(fit["individual_count_in_fit"]),
        "trial_count_in_fit": int(fit["trial_count_in_fit"]),
        "singular_fit": _truth(fit["singular"]),
        "claim_ceiling": (
            "Pooled full-information nuisance calibration only; no architecture, "
            "access, B2, H1 or H2 effect is estimated."
        ),
    }
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
