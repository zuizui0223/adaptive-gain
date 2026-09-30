"""Build a conservative sample-size screening receipt from frozen pilot inputs."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from adaptive_gain.routeability_experiment_power import (
    RouteabilityPilotNuisance,
    RouteabilitySESoi,
    conservative_routeability_planning_receipt,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    nuisance = RouteabilityPilotNuisance(**payload["pilot_nuisance"])
    sesoi = RouteabilitySESoi(**payload["sesoi"])
    settings = payload["planning"]

    receipt = conservative_routeability_planning_receipt(
        nuisance,
        sesoi,
        trials_per_individual=int(settings["trials_per_individual"]),
        alpha_two_sided=float(settings.get("alpha_two_sided", 0.05)),
        target_power=float(settings.get("target_power", 0.80)),
        counterbalance_multiple=int(settings.get("counterbalance_multiple", 4)),
    )

    output = {
        "schema": "adaptive-gain-routeability-power-screening-receipt-v1",
        "pilot_nuisance": asdict(nuisance),
        "sesoi": asdict(sesoi),
        "planning": settings,
        "receipt": asdict(receipt),
        "final_sample_size_frozen": False,
        "next_gate": (
            "final GLMM simulation with colony allocation and frozen nuisance inputs"
        ),
    }
    args.output_json.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
