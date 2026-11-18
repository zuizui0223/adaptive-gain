"""Build the frozen nuisance-only routeability procedural-pilot receipt."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from adaptive_gain.routeability_procedural_pilot import (
    FullInformationPilotTrial,
    freeze_response_window,
    pooled_full_information_nuisance_receipt,
)


def _truth(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"{name} must be boolean-like, got {value!r}")


def _pilot_a_latencies(path: Path) -> list[float]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if "terminal_latency_seconds" not in set(reader.fieldnames or ()):
            raise ValueError("Pilot A CSV must contain terminal_latency_seconds")
        out = []
        for row in reader:
            raw = row["terminal_latency_seconds"].strip()
            if raw:
                out.append(float(raw))
        return out


def _pilot_b_trials(path: Path) -> list[FullInformationPilotTrial]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {
            "individual_id",
            "colony_id",
            "correct_within_window",
            "timeout",
            "block",
        }
        fields = set(reader.fieldnames or ())
        if not required <= fields:
            raise ValueError(f"Pilot B CSV must contain {sorted(required)}")
        forbidden = {"architecture", "access_mode", "budget", "H1", "H2"}
        leaked = sorted(fields & forbidden)
        if leaked:
            raise ValueError(
                f"Pilot B nuisance CSV contains forbidden focal columns: {leaked!r}"
            )
        rows = []
        for row in reader:
            colony = row["colony_id"].strip() or None
            rows.append(
                FullInformationPilotTrial(
                    individual_id=row["individual_id"],
                    colony_id=colony,
                    correct_within_window=_truth(
                        row["correct_within_window"], "correct_within_window"
                    ),
                    timeout=_truth(row["timeout"], "timeout"),
                    block=int(row["block"]),
                )
            )
        return rows


def _randomized_ids(path: Path | None):
    if path is None:
        return None
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if "individual_id" not in set(reader.fieldnames or ()):
            raise ValueError("randomized-individual CSV must contain individual_id")
        ids = {row["individual_id"] for row in reader if row["individual_id"]}
    if not ids:
        raise ValueError("randomized-individual CSV contains no IDs")
    return ids


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pilot_a_csv", type=Path)
    parser.add_argument("pilot_b_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--candidate-windows", required=True)
    parser.add_argument("--upper-bound", type=float, required=True)
    parser.add_argument("--randomized-individuals", type=Path)
    args = parser.parse_args()

    candidate_windows = tuple(
        float(value)
        for value in args.candidate_windows.split(",")
        if value.strip()
    )
    selected_window = freeze_response_window(
        _pilot_a_latencies(args.pilot_a_csv),
        candidate_windows=candidate_windows,
        required_coverage=0.95,
        upper_bound=args.upper_bound,
    )

    pooled = pooled_full_information_nuisance_receipt(
        _pilot_b_trials(args.pilot_b_csv),
        randomized_individual_ids=_randomized_ids(args.randomized_individuals),
    )

    result = {
        "schema": "adaptive-gain-routeability-procedural-pilot-bundle-v1",
        "response_window_seconds": selected_window,
        "response_window_rule": "smallest prespecified candidate reaching at least 95 percent coverage",
        "candidate_windows_seconds": candidate_windows,
        "upper_bound_seconds": args.upper_bound,
        "pooled_full_information": pooled,
        "focal_architecture_access_contrast_opened": False,
        "power_bridge_ready": (
            pooled["trial_icc_moment"] is not None
            and pooled["randomized_individual_dropout_fraction"] is not None
        ),
        "claim_ceiling": (
            "Nuisance-only procedural pilot receipt; no H1/H2 or B2 treatment effect is estimated."
        ),
    }
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
