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
    cue_target_mapping,
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
            cue_vector = "".join(
                str(row[name])
                for name in ("q_left", "q_route", "q_right")
            )
            rows.append(
                {
                    "architecture": architecture,
                    "cue_vector": cue_vector,
                    **row,
                }
            )

    fields = [
        "architecture",
        "cue_vector",
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

    routeable_mapping = dict(
        cue_target_mapping(minimal_strict_gain_standard_task())
    )
    control_mapping = dict(
        cue_target_mapping(bypass_matched_control_task())
    )
    shared_vectors = sorted(routeable_mapping, key=repr)
    mapping_differences = [
        {
            "cue_vector": "".join(str(value) for value in vector),
            "routeable_target": routeable_mapping[vector],
            "bypass_control_target": control_mapping[vector],
        }
        for vector in shared_vectors
        if routeable_mapping[vector] != control_mapping[vector]
    ]

    receipt = {
        "schema": "adaptive-gain-routeability-experiment-stimuli-v1",
        "state_frequency_primary": "uniform_1_over_4_within_architecture",
        "primary_budget": 2,
        "stimulus_row_count": len(rows),
        "shared_physical_cue_vectors": [
            "".join(str(value) for value in vector)
            for vector in shared_vectors
        ],
        "target_mapping_differences": mapping_differences,
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
