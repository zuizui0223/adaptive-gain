"""Machine qualification for routeability physical cue materials.

The physical-cue feasibility gate requires an architecture-neutral material
pretest before confirmatory allocation. This module converts the raw scored
choice log plus an exact material-specification JSON into a hash-addressed
qualification receipt.

It does not choose colours, patterns, species, or apparatus dimensions. It
only enforces the already frozen admission rule:
- q_route, q_left, q_right each reach at least 80% correct in their last
  20 scored choices;
- the best-minus-worst final-20 accuracy is at most 0.10;
- all rows are architecture-neutral;
- no confirmatory-roster individual appears in the material pretest.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable, Mapping


CUE_IDENTITIES = ("q_route", "q_left", "q_right")
MIN_FINAL_CHOICES = 20
MIN_FINAL20_ACCURACY = 0.80
MAX_FINAL20_ACCURACY_SPREAD = 0.10


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bool(value: object, name: str) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"{name} must be boolean-like")


def _positive_int(value: object, name: str) -> int:
    out = int(value)
    if out < 1 or float(value) != out:
        raise ValueError(f"{name} must be a positive integer")
    return out


def _binary(value: object, name: str) -> int:
    out = int(value)
    if out not in (0, 1) or float(value) != out:
        raise ValueError(f"{name} must be 0/1")
    return out


def qualify_material_pretest(
    rows: Iterable[Mapping[str, object]],
    *,
    material_spec: Mapping[str, object],
    trial_log_sha256: str,
    material_spec_sha256: str,
) -> dict[str, object]:
    rows = list(rows)
    if not rows:
        raise ValueError("material pretest log is empty")

    material_set_id = str(material_spec.get("material_set_id", "")).strip()
    if not material_set_id:
        raise ValueError("material spec must contain non-empty material_set_id")

    expected_roles = material_spec.get("cue_roles")
    if not isinstance(expected_roles, Mapping):
        raise ValueError("material spec must contain cue_roles mapping")
    if set(expected_roles) != set(CUE_IDENTITIES):
        raise ValueError(
            "material spec cue_roles must contain exactly q_route, q_left, q_right"
        )

    grouped: dict[str, list[dict[str, object]]] = {
        cue: [] for cue in CUE_IDENTITIES
    }
    seen_indices: set[tuple[str, int]] = set()

    for row_index, row in enumerate(rows, start=1):
        row_material = str(row.get("material_set_id", "")).strip()
        if row_material != material_set_id:
            raise ValueError(
                f"row {row_index}: material_set_id does not match material spec"
            )

        cue = str(row.get("cue_identity", "")).strip()
        if cue not in grouped:
            raise ValueError(
                f"row {row_index}: unexpected cue_identity {cue!r}"
            )

        sequence_index = _positive_int(
            row.get("sequence_index"),
            f"row {row_index} sequence_index",
        )
        key = (cue, sequence_index)
        if key in seen_indices:
            raise ValueError(
                f"duplicate sequence_index {sequence_index} for {cue}"
            )
        seen_indices.add(key)

        correct = _binary(
            row.get("correct"),
            f"row {row_index} correct",
        )
        if not _bool(
            row.get("architecture_neutral"),
            f"row {row_index} architecture_neutral",
        ):
            raise ValueError(
                "all material-pretest rows must be architecture-neutral"
            )
        if _bool(
            row.get("confirmatory_roster_member"),
            f"row {row_index} confirmatory_roster_member",
        ):
            raise ValueError(
                "confirmatory-roster individuals are forbidden in material pretest"
            )

        individual_id = str(row.get("individual_id", "")).strip()
        if not individual_id:
            raise ValueError(
                f"row {row_index}: individual_id must be non-empty"
            )

        grouped[cue].append(
            {
                "sequence_index": sequence_index,
                "correct": correct,
                "individual_id": individual_id,
            }
        )

    cue_results: dict[str, dict[str, object]] = {}
    for cue in CUE_IDENTITIES:
        cue_rows = sorted(
            grouped[cue],
            key=lambda row: int(row["sequence_index"]),
        )
        if len(cue_rows) < MIN_FINAL_CHOICES:
            raise ValueError(
                f"{cue}: requires at least {MIN_FINAL_CHOICES} scored choices"
            )

        final20 = cue_rows[-MIN_FINAL_CHOICES:]
        final20_correct = sum(int(row["correct"]) for row in final20)
        accuracy = final20_correct / MIN_FINAL_CHOICES
        cue_results[cue] = {
            "scored_choice_count": len(cue_rows),
            "individual_count": len(
                {str(row["individual_id"]) for row in cue_rows}
            ),
            "final20_correct": final20_correct,
            "final20_accuracy": accuracy,
            "meets_accuracy_criterion": (
                accuracy >= MIN_FINAL20_ACCURACY
            ),
        }

    accuracies = [
        float(cue_results[cue]["final20_accuracy"])
        for cue in CUE_IDENTITIES
    ]
    spread = max(accuracies) - min(accuracies)
    all_accuracy_pass = all(
        bool(cue_results[cue]["meets_accuracy_criterion"])
        for cue in CUE_IDENTITIES
    )
    salience_pass = (
        spread <= MAX_FINAL20_ACCURACY_SPREAD + 1e-12
    )
    qualified = all_accuracy_pass and salience_pass

    return {
        "schema": "adaptive-gain-routeability-material-pretest-receipt-v1",
        "material_set_id": material_set_id,
        "trial_log_sha256": str(trial_log_sha256),
        "material_spec_sha256": str(material_spec_sha256),
        "architecture_neutral_only": True,
        "confirmatory_roster_members_present": False,
        "criteria": {
            "minimum_scored_choices_per_cue": MIN_FINAL_CHOICES,
            "minimum_final20_accuracy": MIN_FINAL20_ACCURACY,
            "maximum_final20_accuracy_spread": (
                MAX_FINAL20_ACCURACY_SPREAD
            ),
        },
        "cue_results": cue_results,
        "final20_accuracy_spread": spread,
        "all_cues_meet_accuracy": all_accuracy_pass,
        "salience_balance_pass": salience_pass,
        "qualified": qualified,
        "status": (
            "PASS_material_set_qualified"
            if qualified
            else "FAIL_material_set_not_qualified"
        ),
        "promotion_rule": (
            "Only PASS_material_set_qualified may be hash-locked into the "
            "confirmatory stimulus/schedule chain. A failed set must be "
            "redesigned and retested architecture-neutrally before allocation."
        ),
        "claim_ceiling": (
            "This receipt qualifies cue learnability and gross salience balance "
            "only. It is not evidence for routeability, treatment effects, final "
            "sample size, or confirmatory animal performance."
        ),
    }
