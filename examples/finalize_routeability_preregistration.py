"""Finalize the routeability preregistration only after all blockers are resolved."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from adaptive_gain.routeability_experiment_power import RouteabilitySESoi

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "manuscript" / "ROUTEABILITY_PREREGISTRATION_TEMPLATE_V1.md"

REQUIRED_FIELDS = (
    "preregistration_version",
    "species",
    "study_site",
    "ethics_approval",
    "planned_start_date",
    "individuals_per_cell",
    "colony_count",
    "trials_per_individual",
    "power_surface_reference",
    "h1_sesoi",
    "h2_sesoi",
    "sesoi_provenance",
    "apparatus_description",
    "cue_alphabet_description",
    "nominal_cue_duration_seconds",
    "cue_duration_tolerance_seconds",
    "response_window_seconds",
    "pilot_receipt_reference",
    "familiarization_protocol",
    "training_dose",
    "randomization_seed",
    "colony_allocation_rule",
    "exclusion_rules",
    "final_n_decision_rule",
    "frozen_precollection_commit",
    "final_schedule_reference",
    "final_stimulus_reference",
)

FORBIDDEN_PENDING_MARKERS = (
    "pending",
    "tbd",
    "to be determined",
    "not yet",
    "placeholder",
    "unknown",
)


def _nonempty(value, name: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{name} must be non-empty")
    return text


def _positive_int(value, name: str) -> int:
    out = int(value)
    if out < 1 or float(value) != out:
        raise ValueError(f"{name} must be a positive integer")
    return out


def _positive_float(value, name: str, *, allow_zero: bool = False) -> float:
    out = float(value)
    if allow_zero:
        valid = out >= 0
    else:
        valid = out > 0
    if not valid:
        relation = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{name} must be {relation}")
    return out


def _reject_pending_marker(value, name: str) -> str:
    text = _nonempty(value, name)
    lower = text.lower()
    if any(marker in lower for marker in FORBIDDEN_PENDING_MARKERS):
        raise ValueError(f"{name} still contains a pending placeholder")
    return text


def validate_finalization_payload(payload: dict) -> dict[str, str]:
    missing = [name for name in REQUIRED_FIELDS if name not in payload]
    if missing:
        raise ValueError(
            "preregistration finalization payload missing fields: "
            + ", ".join(missing)
        )

    individuals_per_cell = _positive_int(
        payload["individuals_per_cell"], "individuals_per_cell"
    )
    if individuals_per_cell % 4 != 0:
        raise ValueError(
            "individuals_per_cell must be a multiple of four for frozen cue-symbol counterbalancing"
        )
    colony_count = _positive_int(payload["colony_count"], "colony_count")
    trials_per_individual = _positive_int(
        payload["trials_per_individual"], "trials_per_individual"
    )
    randomization_seed = int(payload["randomization_seed"])
    if randomization_seed < 0:
        raise ValueError("randomization_seed must be non-negative")

    response_window = _positive_float(
        payload["response_window_seconds"], "response_window_seconds"
    )
    cue_duration = _positive_float(
        payload["nominal_cue_duration_seconds"],
        "nominal_cue_duration_seconds",
    )
    cue_tolerance = _positive_float(
        payload["cue_duration_tolerance_seconds"],
        "cue_duration_tolerance_seconds",
        allow_zero=True,
    )

    sesoi = RouteabilitySESoi(
        h1_probability_interaction=float(payload["h1_sesoi"]),
        h2_probability_localization=float(payload["h2_sesoi"]),
        provenance=str(payload["sesoi_provenance"]),
    ).validated()

    commit = _nonempty(
        payload["frozen_precollection_commit"],
        "frozen_precollection_commit",
    )
    if re.fullmatch(r"[0-9a-fA-F]{40}", commit) is None:
        raise ValueError(
            "frozen_precollection_commit must be a full 40-character Git SHA"
        )

    text_fields = (
        "preregistration_version",
        "species",
        "study_site",
        "ethics_approval",
        "planned_start_date",
        "power_surface_reference",
        "apparatus_description",
        "cue_alphabet_description",
        "pilot_receipt_reference",
        "familiarization_protocol",
        "training_dose",
        "colony_allocation_rule",
        "exclusion_rules",
        "final_n_decision_rule",
        "final_schedule_reference",
        "final_stimulus_reference",
    )
    clean = {
        name: _reject_pending_marker(payload[name], name)
        for name in text_fields
    }

    replacements = {
        **clean,
        "individuals_per_cell": str(individuals_per_cell),
        "total_randomized_individuals": str(12 * individuals_per_cell),
        "colony_count": str(colony_count),
        "trials_per_individual": str(trials_per_individual),
        "h1_sesoi": str(sesoi.h1_probability_interaction),
        "h2_sesoi": str(sesoi.h2_probability_localization),
        "sesoi_provenance": sesoi.provenance,
        "nominal_cue_duration_seconds": str(cue_duration),
        "cue_duration_tolerance_seconds": str(cue_tolerance),
        "response_window_seconds": str(response_window),
        "randomization_seed": str(randomization_seed),
        "frozen_precollection_commit": commit.lower(),
    }
    return replacements


def finalize_preregistration(payload: dict) -> str:
    replacements = validate_finalization_payload(payload)
    text = TEMPLATE.read_text(encoding="utf-8")
    for name, value in replacements.items():
        text = text.replace("{{" + name + "}}", value)

    remaining = sorted(set(re.findall(r"\{\{([a-zA-Z0-9_]+)\}\}", text)))
    if remaining:
        raise ValueError(
            "unresolved preregistration placeholders remain: "
            + ", ".join(remaining)
        )

    text = text.replace(
        "Status: **TEMPLATE ONLY — NOT YET PREREGISTERABLE**",
        "Status: **FINALIZED PRE-COLLECTION PREREGISTRATION CANDIDATE**",
        1,
    )
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_md", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    finalized = finalize_preregistration(payload)
    args.output_md.write_text(finalized, encoding="utf-8")


if __name__ == "__main__":
    main()
