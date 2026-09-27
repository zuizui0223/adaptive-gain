"""Finalize the routeability preregistration only after all blockers are resolved."""

from __future__ import annotations

import argparse
import hashlib
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
    "power_surface_sha256",
    "h1_sesoi",
    "h2_sesoi",
    "sesoi_provenance",
    "apparatus_description",
    "cue_alphabet_description",
    "nominal_cue_duration_seconds",
    "cue_duration_tolerance_seconds",
    "response_window_seconds",
    "pilot_receipt_reference",
    "pilot_receipt_sha256",
    "familiarization_protocol",
    "training_dose",
    "randomization_seed",
    "colony_allocation_rule",
    "exclusion_rules",
    "final_n_decision_rule",
    "frozen_precollection_commit",
    "randomization_receipt_reference",
    "randomization_receipt_sha256",
    "final_assignment_reference",
    "final_assignment_sha256",
    "final_schedule_receipt_reference",
    "final_schedule_receipt_sha256",
    "final_schedule_reference",
    "final_schedule_sha256",
    "final_stimulus_reference",
    "final_stimulus_sha256",
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
    valid = out >= 0 if allow_zero else out > 0
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


def _sha256(value, name: str) -> str:
    text = _nonempty(value, name).lower()
    if re.fullmatch(r"[0-9a-f]{64}", text) is None:
        raise ValueError(f"{name} must be a 64-character SHA-256 hex digest")
    return text


def _artifact_path(
    reference: str,
    expected_sha256: str,
    *,
    artifact_root: Path,
    name: str,
) -> Path:
    rel = Path(reference)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"{name} must be a relative path within artifact-root")

    root = artifact_root.resolve()
    path = (root / rel).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"{name} escapes artifact-root")
    if not path.is_file():
        raise ValueError(f"{name} does not exist: {reference}")

    observed = hashlib.sha256(path.read_bytes()).hexdigest()
    if observed != expected_sha256:
        raise ValueError(
            f"{name} SHA-256 mismatch: observed {observed}, expected {expected_sha256}"
        )
    return path


def _read_json(path: Path, name: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"{name} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain a JSON object")
    return value


def validate_finalization_payload(
    payload: dict,
    *,
    artifact_root: Path = ROOT,
) -> dict[str, str]:
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
        "randomization_receipt_reference",
        "final_assignment_reference",
        "final_schedule_receipt_reference",
        "final_schedule_reference",
        "final_stimulus_reference",
    )
    clean = {
        name: _reject_pending_marker(payload[name], name)
        for name in text_fields
    }

    if "fixture" in clean["power_surface_reference"].lower():
        raise ValueError(
            "power_surface_reference cannot point to a software fixture"
        )

    hash_fields = (
        "pilot_receipt_sha256",
        "power_surface_sha256",
        "randomization_receipt_sha256",
        "final_assignment_sha256",
        "final_schedule_receipt_sha256",
        "final_schedule_sha256",
        "final_stimulus_sha256",
    )
    hashes = {
        name: _sha256(payload[name], name)
        for name in hash_fields
    }

    artifact_pairs = (
        ("pilot_receipt_reference", "pilot_receipt_sha256"),
        ("power_surface_reference", "power_surface_sha256"),
        ("randomization_receipt_reference", "randomization_receipt_sha256"),
        ("final_assignment_reference", "final_assignment_sha256"),
        ("final_schedule_receipt_reference", "final_schedule_receipt_sha256"),
        ("final_schedule_reference", "final_schedule_sha256"),
        ("final_stimulus_reference", "final_stimulus_sha256"),
    )
    verified = {}
    for ref_field, hash_field in artifact_pairs:
        verified[ref_field] = _artifact_path(
            clean[ref_field],
            hashes[hash_field],
            artifact_root=artifact_root,
            name=ref_field,
        )

    pilot = _read_json(
        verified["pilot_receipt_reference"],
        "pilot_receipt_reference",
    )
    if pilot.get("schema") != "adaptive-gain-routeability-procedural-pilot-bundle-v1":
        raise ValueError("unexpected pilot receipt schema")
    if pilot.get("focal_architecture_access_contrast_opened") is not False:
        raise ValueError("pilot receipt does not certify focal contrast blindness")
    if float(pilot.get("response_window_seconds")) != response_window:
        raise ValueError("response_window_seconds disagrees with pilot receipt")

    randomization = _read_json(
        verified["randomization_receipt_reference"],
        "randomization_receipt_reference",
    )
    if randomization.get("schema") != "adaptive-gain-routeability-roster-randomization-v1":
        raise ValueError("unexpected randomization receipt schema")
    if randomization.get("assignments_sha256") != hashes["final_assignment_sha256"]:
        raise ValueError(
            "randomization receipt assignment hash disagrees with final_assignment_sha256"
        )
    if int(randomization.get("randomization_seed")) != randomization_seed:
        raise ValueError("randomization_seed disagrees with randomization receipt")

    randomization_core = randomization.get("receipt")
    if not isinstance(randomization_core, dict):
        raise ValueError("randomization receipt missing nested receipt")
    if int(randomization_core.get("individuals_per_cell")) != individuals_per_cell:
        raise ValueError(
            "individuals_per_cell disagrees with randomization receipt"
        )
    if int(randomization_core.get("assigned_individual_count")) != (
        12 * individuals_per_cell
    ):
        raise ValueError(
            "randomization assigned-individual count disagrees with 12-cell final N"
        )
    if not randomization_core.get("complete_blocks_valid"):
        raise ValueError("randomization receipt does not certify complete colony blocks")
    if not randomization_core.get("counterbalance_profiles_valid"):
        raise ValueError("randomization receipt does not certify counterbalance profiles")

    schedule_receipt = _read_json(
        verified["final_schedule_receipt_reference"],
        "final_schedule_receipt_reference",
    )
    if schedule_receipt.get("schema") != (
        "adaptive-gain-routeability-final-trial-schedule-v1"
    ):
        raise ValueError("unexpected final schedule receipt schema")
    if schedule_receipt.get("assignments_sha256") != hashes["final_assignment_sha256"]:
        raise ValueError("final schedule receipt assignment hash mismatch")
    if schedule_receipt.get("randomization_receipt_sha256") != hashes[
        "randomization_receipt_sha256"
    ]:
        raise ValueError("final schedule receipt randomization-receipt hash mismatch")
    if schedule_receipt.get("schedule_sha256") != hashes["final_schedule_sha256"]:
        raise ValueError("final schedule receipt schedule hash mismatch")
    if int(schedule_receipt.get("blocks_per_individual")) * 4 != trials_per_individual:
        raise ValueError(
            "trials_per_individual disagrees with final schedule receipt"
        )

    audit = schedule_receipt.get("audit")
    if not isinstance(audit, dict):
        raise ValueError("final schedule receipt missing audit")
    for field in (
        "individual_identity_match",
        "assignment_fidelity",
        "individual_state_balance",
        "individual_terminal_position_balance",
        "individual_order_balance",
    ):
        if audit.get(field) is not True:
            raise ValueError(f"final schedule audit failed: {field}")
    if int(audit.get("scheduled_individual_count")) != 12 * individuals_per_cell:
        raise ValueError(
            "final schedule individual count disagrees with randomized final N"
        )
    if int(audit.get("trial_count")) != (
        12 * individuals_per_cell * trials_per_individual
    ):
        raise ValueError(
            "final schedule trial count disagrees with N x trials_per_individual"
        )

    replacements = {
        **hashes,
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


def finalize_preregistration(
    payload: dict,
    *,
    artifact_root: Path = ROOT,
) -> str:
    replacements = validate_finalization_payload(
        payload,
        artifact_root=artifact_root,
    )
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
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=ROOT,
        help="Root directory containing all hash-frozen preregistration artifacts.",
    )
    args = parser.parse_args()

    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    finalized = finalize_preregistration(
        payload,
        artifact_root=args.artifact_root,
    )
    args.output_md.write_text(finalized, encoding="utf-8")


if __name__ == "__main__":
    main()
