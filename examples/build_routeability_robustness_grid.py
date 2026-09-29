"""Build the frozen final-power robustness config from pilot nuisance data."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from adaptive_gain.routeability_robustness_grid import (
    build_frozen_robustness_scenarios,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("nuisance_receipt_json", type=Path)
    parser.add_argument("planning_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    nuisance = json.loads(
        args.nuisance_receipt_json.read_text(encoding="utf-8")
    )
    planning = json.loads(args.planning_json.read_text(encoding="utf-8"))

    scenarios = build_frozen_robustness_scenarios(
        nuisance,
        candidate_individuals_per_cell=planning[
            "candidate_individuals_per_cell"
        ],
        colony_count=planning["colony_count"],
        simulations_per_scenario=planning["simulations_per_scenario"],
        seed_base=planning["seed_base"],
        alpha_two_sided=planning.get("alpha_two_sided", 0.05),
    )

    ns = sorted(
        {
            row["simulation"]["individuals_per_cell"]
            for row in scenarios
        }
    )
    robustness_ids = sorted({row["robustness_id"] for row in scenarios})
    result = {
        "schema": "adaptive-gain-routeability-frozen-robustness-config-v1",
        "policy_gate": (
            "validation/"
            "routeability_nuisance_robustness_grid_gate_v1.json"
        ),
        "nuisance_receipt_sha256": _sha256(
            args.nuisance_receipt_json
        ),
        "planning_input_sha256": _sha256(args.planning_json),
        "candidate_individuals_per_cell": ns,
        "robustness_ids": robustness_ids,
        "scenario_count_per_N": len(robustness_ids),
        "scenarios": list(scenarios),
        "claim_ceiling": (
            "Frozen planning scenarios only; no operating-characteristic "
            "simulation or final biological N is implied by this file."
        ),
    }
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
