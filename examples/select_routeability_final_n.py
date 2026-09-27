"""Select the final balanced routeability sample size from a frozen power surface."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from adaptive_gain.routeability_final_n_selection import (
    FinalNRule,
    receipt_as_dict,
    select_final_individuals_per_cell,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("power_surface_csv", type=Path)
    parser.add_argument("rule_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    rule_payload = json.loads(args.rule_json.read_text(encoding="utf-8"))
    rule = FinalNRule(
        minimum_fit_success_fraction=float(
            rule_payload["minimum_fit_success_fraction"]
        ),
        minimum_h1_directional_rejection_fraction=float(
            rule_payload["minimum_h1_directional_rejection_fraction"]
        ),
        minimum_h2_hierarchical_pass_fraction=float(
            rule_payload["minimum_h2_hierarchical_pass_fraction"]
        ),
        minimum_scenarios_per_n=int(
            rule_payload.get("minimum_scenarios_per_n", 2)
        ),
        minimum_simulations_per_scenario=int(
            rule_payload.get("minimum_simulations_per_scenario", 1000)
        ),
        counterbalance_multiple=int(
            rule_payload.get("counterbalance_multiple", 4)
        ),
    ).validated()

    receipt = select_final_individuals_per_cell(
        args.power_surface_csv,
        rule,
    )
    result = receipt_as_dict(receipt)
    result.update(
        {
            "power_surface_sha256": hashlib.sha256(
                args.power_surface_csv.read_bytes()
            ).hexdigest(),
            "rule_sha256": hashlib.sha256(
                args.rule_json.read_bytes()
            ).hexdigest(),
            "power_surface_reference": str(args.power_surface_csv),
            "rule_reference": str(args.rule_json),
            "claim_ceiling": (
                "Final N is selected mechanically from the frozen operating-"
                "characteristic surface and frozen thresholds. This receipt "
                "does not create pilot, ethics, apparatus, or preregistration approval."
            ),
        }
    )
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
