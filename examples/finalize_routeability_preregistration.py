"""Finalize the routeability preregistration only after all blockers are resolved."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from adaptive_gain.ecological_routeability_experiment import (
    bypass_matched_control_task,
    experimental_stimulus_table,
)
from adaptive_gain.minimal_normal_form import minimal_strict_gain_standard_task
from adaptive_gain.routeability_experiment_power import RouteabilitySESoi
from adaptive_gain.routeability_final_n_selection import (
    FinalNRule,
    select_final_individuals_per_cell,
)
from adaptive_gain.routeability_robustness_grid import (
    BASELINE_PROFILE_NAMES,
    NUISANCE_PROFILES,
)
from adaptive_gain.routeability_material_pretest import (
    qualify_material_pretest,
)

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "manuscript" / "ROUTEABILITY_PREREGISTRATION_TEMPLATE_V1.md"
SESOI_GATE = ROOT / "validation" / "routeability_sesoi_gate_v1.json"
FINAL_N_THRESHOLD_RULE = (
    ROOT / "validation" / "routeability_final_n_threshold_rule_v1.json"
)

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
    "final_n_rule_reference",
    "final_n_rule_sha256",
    "final_n_receipt_reference",
    "final_n_receipt_sha256",
    "h1_sesoi",
    "h2_sesoi",
    "sesoi_provenance",
    "apparatus_description",
    "cue_alphabet_description",
    "material_pretest_log_reference",
    "material_pretest_log_sha256",
    "material_spec_reference",
    "material_spec_sha256",
    "material_pretest_receipt_reference",
    "material_pretest_receipt_sha256",
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



def _read_csv(path: Path, name: str) -> list[dict[str, str]]:
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))
    except Exception as exc:
        raise ValueError(f"{name} is not valid UTF-8 CSV") from exc



def _validate_power_surface_csv(
    path: Path,
    *,
    individuals_per_cell: int,
    trials_per_individual: int,
    colony_count: int,
    h1_sesoi: float,
    h2_sesoi: float,
    sesoi_provenance: str,
) -> None:
    rows = _read_csv(path, "power_surface_reference")
    required = {
        "scenario_id",
        "robustness_id",
        "simulations",
        "individuals_per_cell",
        "trials_per_individual",
        "colony_count",
        "colony_block_counts",
        "individual_sd_logit",
        "colony_sd_logit",
        "dropout_fraction",
        "timeout_fraction",
        "sesoi_provenance",
        "fit_success_fraction",
        "h1_directional_rejection_fraction",
        "h2_hierarchical_pass_fraction",
        "expected_h1_delta_b2",
        "expected_h2_localization",
    }
    if len(rows) < 2 or not required <= set(rows[0]):
        raise ValueError(
            "final power surface must contain at least two scenario rows and all frozen design/operating-characteristic columns"
        )
    ids = [row["scenario_id"] for row in rows]
    if any(not value.strip() for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("final power surface scenario_id values must be unique and non-empty")

    expected_robustness_ids = {
        f"{baseline}__{nuisance}"
        for baseline in BASELINE_PROFILE_NAMES
        for nuisance in NUISANCE_PROFILES
    }
    robustness_by_n: dict[int, set[str]] = {}
    for row in rows:
        n_value = int(row["individuals_per_cell"])
        robustness_by_n.setdefault(n_value, set()).add(
            row["robustness_id"].strip()
        )
    for n_value, observed_ids in robustness_by_n.items():
        if observed_ids != expected_robustness_ids:
            missing = sorted(expected_robustness_ids - observed_ids)
            extra = sorted(observed_ids - expected_robustness_ids)
            raise ValueError(
                "final power surface must use the exact frozen 12 robustness_id "
                f"values at every candidate N; N={n_value}, "
                f"missing={missing!r}, extra={extra!r}"
            )

    matching_final_n = False
    for row in rows:
        n = int(row["individuals_per_cell"])
        if n < 4 or n % 4 != 0:
            raise ValueError(
                "final power surface contains individuals_per_cell incompatible with four-profile counterbalancing"
            )
        row_colony_count = int(row["colony_count"])
        try:
            block_counts = tuple(
                int(value)
                for value in row["colony_block_counts"].split(";")
                if value != ""
            )
        except ValueError as exc:
            raise ValueError(
                "final power surface colony_block_counts must be semicolon-separated positive integers"
            ) from exc
        if (
            len(block_counts) != row_colony_count
            or any(value < 1 for value in block_counts)
            or sum(block_counts) != n
        ):
            raise ValueError(
                "final power surface colony_block_counts must contain one positive count per colony and sum to individuals_per_cell"
            )
        for field in (
            "fit_success_fraction",
            "h1_directional_rejection_fraction",
            "h2_hierarchical_pass_fraction",
        ):
            value = float(row[field])
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"final power surface {field} must lie in [0,1]"
                )
        if (
            n == individuals_per_cell
            and int(row["trials_per_individual"]) == trials_per_individual
            and int(row["colony_count"]) == colony_count
            and row["sesoi_provenance"] == sesoi_provenance
            and abs(float(row["expected_h1_delta_b2"]) - h1_sesoi) <= 1e-12
            and abs(float(row["expected_h2_localization"]) - h2_sesoi) <= 1e-12
        ):
            matching_final_n = True

    if not matching_final_n:
        raise ValueError(
            "final power surface contains no scenario matching the preregistered final N, trials, colony count and H1/H2 SESOI/provenance"
        )


def _validate_stimulus_csv(path: Path) -> None:
    rows = _read_csv(path, "final_stimulus_reference")
    required = {
        "architecture",
        "state",
        "target",
        "q_left",
        "q_route",
        "q_right",
    }
    if len(rows) != 8 or not required <= set(rows[0]):
        raise ValueError(
            "final stimulus artifact must contain exactly the frozen 8-row logical stimulus surface"
        )

    observed = {}
    for row in rows:
        key = (row["architecture"], row["state"])
        if key in observed:
            raise ValueError("final stimulus artifact contains duplicate architecture/state rows")
        observed[key] = (
            int(row["target"]),
            int(row["q_left"]),
            int(row["q_route"]),
            int(row["q_right"]),
        )

    expected = {}
    for architecture, task in (
        ("routeable", minimal_strict_gain_standard_task()),
        ("bypass_control", bypass_matched_control_task()),
    ):
        for row in experimental_stimulus_table(task):
            expected[(architecture, str(row["state"]))] = (
                int(row["target"]),
                int(row["q_left"]),
                int(row["q_route"]),
                int(row["q_right"]),
            )

    if observed != expected:
        raise ValueError(
            "final stimulus artifact does not match the exact frozen routeable/bypass logical stimulus mapping"
        )

def _validate_assignment_csv(
    path: Path,
    *,
    individuals_per_cell: int,
) -> dict[str, dict[str, str]]:
    rows = _read_csv(path, "final_assignment_reference")
    required = {
        "individual_id",
        "colony_id",
        "complete_block_id",
        "architecture",
        "access_mode",
        "budget",
        "treatment_cell",
        "counterbalance_profile",
    }
    if not rows or not required <= set(rows[0]):
        raise ValueError(
            "final assignment CSV is empty or missing required columns"
        )

    by_id: dict[str, dict[str, str]] = {}
    cell_counts: dict[str, int] = {}
    profile_counts: dict[str, dict[str, int]] = {}
    for row in rows:
        individual = row["individual_id"].strip()
        if not individual or individual in by_id:
            raise ValueError(
                "final assignment CSV contains empty or duplicate individual_id"
            )
        by_id[individual] = row

        expected_cell = (
            f"{row['architecture']}__{row['access_mode']}__B{int(row['budget'])}"
        )
        if row["treatment_cell"] != expected_cell:
            raise ValueError(
                f"final assignment treatment_cell mismatch for {individual!r}"
            )
        cell_counts[expected_cell] = cell_counts.get(expected_cell, 0) + 1
        profiles = profile_counts.setdefault(expected_cell, {})
        profile = row["counterbalance_profile"]
        profiles[profile] = profiles.get(profile, 0) + 1

    if len(cell_counts) != 12 or set(cell_counts.values()) != {
        individuals_per_cell
    }:
        raise ValueError(
            "final assignment CSV does not contain 12 exactly balanced treatment cells"
        )

    expected_profiles = {"cb0", "cb1", "cb2", "cb3"}
    for cell, counts in profile_counts.items():
        if set(counts) != expected_profiles or len(set(counts.values())) != 1:
            raise ValueError(
                f"final assignment counterbalance profiles are not balanced in {cell}"
            )

    if len(by_id) != 12 * individuals_per_cell:
        raise ValueError(
            "final assignment individual count disagrees with 12-cell final N"
        )
    return by_id


def _validate_schedule_csv(
    path: Path,
    assignments: dict[str, dict[str, str]],
    *,
    trials_per_individual: int,
) -> None:
    rows = _read_csv(path, "final_schedule_reference")
    required = {
        "individual_id",
        "colony_id",
        "complete_block_id",
        "treatment_cell",
        "architecture",
        "access_mode",
        "budget",
        "counterbalance_profile",
        "trial_index",
        "state",
        "revealed_cues",
    }
    if not rows or not required <= set(rows[0]):
        raise ValueError(
            "final schedule CSV is empty or missing required columns"
        )

    counts = {individual: 0 for individual in assignments}
    seen_trial_keys = set()
    for row in rows:
        individual = row["individual_id"]
        assignment = assignments.get(individual)
        if assignment is None:
            raise ValueError(
                f"final schedule contains unassigned individual {individual!r}"
            )
        key = (individual, row["trial_index"])
        if key in seen_trial_keys:
            raise ValueError("final schedule contains duplicate individual/trial key")
        seen_trial_keys.add(key)
        counts[individual] += 1

        for field in (
            "colony_id",
            "complete_block_id",
            "treatment_cell",
            "architecture",
            "access_mode",
            "budget",
            "counterbalance_profile",
        ):
            if str(row[field]) != str(assignment[field]):
                raise ValueError(
                    f"final schedule assignment mismatch for {individual!r}: {field}"
                )

    if set(counts.values()) != {trials_per_individual}:
        raise ValueError(
            "final schedule does not contain exactly trials_per_individual for every randomized individual"
        )

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

    frozen_sesoi_gate = _read_json(
        SESOI_GATE,
        "routeability_sesoi_gate_v1.json",
    )
    frozen_power = frozen_sesoi_gate["power_interface"]
    frozen_h1 = float(frozen_power["h1_sesoi"])
    frozen_h2 = float(frozen_power["h2_sesoi"])
    frozen_provenance = str(frozen_power["sesoi_provenance"])
    if (
        abs(sesoi.h1_probability_interaction - frozen_h1) > 1e-12
        or abs(sesoi.h2_probability_localization - frozen_h2) > 1e-12
        or sesoi.provenance != frozen_provenance
    ):
        raise ValueError(
            "preregistration SESOI must exactly match the frozen "
            "routeability_sesoi_gate_v1.json values/provenance: "
            f"H1={frozen_h1}, H2={frozen_h2}, "
            f"provenance={frozen_provenance!r}"
        )

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
        "final_n_rule_reference",
        "final_n_receipt_reference",
        "apparatus_description",
        "cue_alphabet_description",
        "material_pretest_log_reference",
        "material_spec_reference",
        "material_pretest_receipt_reference",
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
        "material_pretest_log_sha256",
        "material_spec_sha256",
        "material_pretest_receipt_sha256",
        "pilot_receipt_sha256",
        "power_surface_sha256",
        "final_n_rule_sha256",
        "final_n_receipt_sha256",
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
        ("material_pretest_log_reference", "material_pretest_log_sha256"),
        ("material_spec_reference", "material_spec_sha256"),
        ("material_pretest_receipt_reference", "material_pretest_receipt_sha256"),
        ("pilot_receipt_reference", "pilot_receipt_sha256"),
        ("power_surface_reference", "power_surface_sha256"),
        ("final_n_rule_reference", "final_n_rule_sha256"),
        ("final_n_receipt_reference", "final_n_receipt_sha256"),
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

    material_rows = _read_csv(
        verified["material_pretest_log_reference"],
        "material_pretest_log_reference",
    )
    material_spec = _read_json(
        verified["material_spec_reference"],
        "material_spec_reference",
    )
    recomputed_material_receipt = qualify_material_pretest(
        material_rows,
        material_spec=material_spec,
        trial_log_sha256=hashes["material_pretest_log_sha256"],
        material_spec_sha256=hashes["material_spec_sha256"],
    )
    material_receipt = _read_json(
        verified["material_pretest_receipt_reference"],
        "material_pretest_receipt_reference",
    )
    if material_receipt != recomputed_material_receipt:
        raise ValueError(
            "material pretest receipt disagrees with independent recomputation"
        )
    if (
        material_receipt.get("status") != "PASS_material_set_qualified"
        or material_receipt.get("qualified") is not True
    ):
        raise ValueError(
            "material pretest receipt does not certify a qualified material set"
        )

    _validate_power_surface_csv(
        verified["power_surface_reference"],
        individuals_per_cell=individuals_per_cell,
        trials_per_individual=trials_per_individual,
        colony_count=colony_count,
        h1_sesoi=sesoi.h1_probability_interaction,
        h2_sesoi=sesoi.h2_probability_localization,
        sesoi_provenance=sesoi.provenance,
    )
    final_n_rule_payload = _read_json(
        verified["final_n_rule_reference"],
        "final_n_rule_reference",
    )
    frozen_final_n_rule = _read_json(
        FINAL_N_THRESHOLD_RULE,
        "routeability_final_n_threshold_rule_v1.json",
    )
    frozen_rule_fields = (
        "minimum_fit_success_fraction",
        "minimum_h1_directional_rejection_fraction",
        "minimum_h2_hierarchical_pass_fraction",
        "minimum_scenarios_per_n",
        "minimum_simulations_per_scenario",
        "counterbalance_multiple",
    )
    for field in frozen_rule_fields:
        if final_n_rule_payload.get(field) != frozen_final_n_rule.get(field):
            raise ValueError(
                "final-N threshold rule must exactly match the frozen "
                "routeability_final_n_threshold_rule_v1.json; "
                f"field {field!r} differs"
            )
    final_n_rule = FinalNRule(
        minimum_fit_success_fraction=float(
            final_n_rule_payload["minimum_fit_success_fraction"]
        ),
        minimum_h1_directional_rejection_fraction=float(
            final_n_rule_payload[
                "minimum_h1_directional_rejection_fraction"
            ]
        ),
        minimum_h2_hierarchical_pass_fraction=float(
            final_n_rule_payload[
                "minimum_h2_hierarchical_pass_fraction"
            ]
        ),
        minimum_scenarios_per_n=int(
            final_n_rule_payload.get("minimum_scenarios_per_n", 2)
        ),
        minimum_simulations_per_scenario=int(
            final_n_rule_payload.get(
                "minimum_simulations_per_scenario", 1000
            )
        ),
        counterbalance_multiple=int(
            final_n_rule_payload.get("counterbalance_multiple", 4)
        ),
    ).validated()
    recomputed_final_n = select_final_individuals_per_cell(
        verified["power_surface_reference"],
        final_n_rule,
    )

    final_n_receipt = _read_json(
        verified["final_n_receipt_reference"],
        "final_n_receipt_reference",
    )
    if final_n_receipt.get("schema") != (
        "adaptive-gain-routeability-final-n-selection-v1"
    ):
        raise ValueError("unexpected final-N receipt schema")
    if final_n_receipt.get("power_surface_sha256") != hashes[
        "power_surface_sha256"
    ]:
        raise ValueError("final-N receipt power-surface hash mismatch")
    if final_n_receipt.get("rule_sha256") != hashes["final_n_rule_sha256"]:
        raise ValueError("final-N receipt rule hash mismatch")
    if int(final_n_receipt.get("selected_individuals_per_cell")) != (
        recomputed_final_n.selected_individuals_per_cell
    ):
        raise ValueError(
            "final-N receipt selected N disagrees with independent selector recomputation"
        )
    if individuals_per_cell != recomputed_final_n.selected_individuals_per_cell:
        raise ValueError(
            "individuals_per_cell does not equal the mechanically selected final N"
        )
    if int(final_n_receipt.get("total_randomized_individuals")) != (
        12 * individuals_per_cell
    ):
        raise ValueError("final-N receipt total randomized N mismatch")

    _validate_stimulus_csv(
        verified["final_stimulus_reference"],
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

    assignments = _validate_assignment_csv(
        verified["final_assignment_reference"],
        individuals_per_cell=individuals_per_cell,
    )
    _validate_schedule_csv(
        verified["final_schedule_reference"],
        assignments,
        trials_per_individual=trials_per_individual,
    )

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
    if int(randomization_core.get("colony_count")) != colony_count:
        raise ValueError("colony_count disagrees with randomization receipt")
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
