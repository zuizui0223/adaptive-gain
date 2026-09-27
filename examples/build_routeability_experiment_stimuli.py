"""Export the frozen minimal routeability experiment as machine-readable stimuli.

Outputs:
- CSV with the four routeable and four bypass-control stimulus states;
- JSON receipt with exact costs, matching checks and two-cue information ceilings.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

from adaptive_gain.ecological_routeability_experiment import (
    bypass_matched_control_task,
    ecological_routeability_experiment_contrast,
    experimental_stimulus_table,
    routeability_budget_information_ceilings,
)
from adaptive_gain.minimal_normal_form import minimal_strict_gain_standard_task


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stimulus_csv", type=Path)
    parser.add_argument("receipt_json", type=Path)
    args = parser.parse_args()

    rows = []
    for architecture, task in (
        ("routeable", minimal_strict_gain_standard_task()),
        ("bypass_control", bypass_matched_control_task()),
    ):
        for row in experimental_stimulus_table(task):
            rows.append({"architecture": architecture, **row})

    fields = [
        "architecture",
        "state",
        "target",
        "q_left",
        "q_route",
        "q_right",
    ]
    with args.stimulus_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    contrast = ecological_routeability_experiment_contrast()
    receipt = {
        "schema": "adaptive-gain-routeability-experiment-stimuli-v1",
        "state_frequency_primary": "uniform_1_over_4_within_architecture",
        "primary_budget": 2,
        "stimulus_row_count": len(rows),
        "contrast": asdict(contrast),
        "exact_minimal_contrast": contrast.exact_minimal_contrast,
        "primary_information_interaction": (
            contrast.routeable_adaptive_accuracy
            - contrast.routeable_fixed_terminal_accuracy
            - (
                contrast.control_adaptive_accuracy
                - contrast.control_fixed_terminal_accuracy
            )
        ),
        "budget_information_ceilings": [
            {
                **asdict(row),
                "architecture_by_access_interaction": (
                    row.architecture_by_access_interaction
                ),
            }
            for row in routeability_budget_information_ceilings()
        ],
        "claim_ceiling": (
            "Accuracy values are information ceilings under uniform states, "
            "not required behavioral effect sizes."
        ),
    }
    args.receipt_json.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
