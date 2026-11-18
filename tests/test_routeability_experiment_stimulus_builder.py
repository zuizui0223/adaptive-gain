import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "examples" / "build_routeability_experiment_stimuli.py"


def test_routeability_stimulus_builder_exports_exact_frozen_surface(tmp_path):
    csv_path = tmp_path / "stimuli.csv"
    json_path = tmp_path / "receipt.json"

    completed = subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            str(csv_path),
            str(json_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 8
    assert sum(row["architecture"] == "routeable" for row in rows) == 4
    assert sum(row["architecture"] == "bypass_control" for row in rows) == 4
    by_architecture = {
        architecture: {
            row["cue_vector"]
            for row in rows
            if row["architecture"] == architecture
        }
        for architecture in ("routeable", "bypass_control")
    }
    assert by_architecture["routeable"] == by_architecture["bypass_control"] == {
        "000", "001", "011", "111"
    }

    receipt = json.loads(json_path.read_text(encoding="utf-8"))
    assert receipt["exact_minimal_contrast"] is True
    assert receipt["primary_budget"] == 2
    assert receipt["stimulus_row_count"] == 8
    assert receipt["primary_information_interaction"] == 0.25
    assert receipt["shared_physical_cue_vectors"] == ["000", "001", "011", "111"]
    assert receipt["target_mapping_differences"] == [
        {
            "cue_vector": "000",
            "routeable_target": 0,
            "bypass_control_target": 1,
        },
        {
            "cue_vector": "001",
            "routeable_target": 1,
            "bypass_control_target": 0,
        },
    ]
    ladder = {
        row["budget"]: row
        for row in receipt["budget_information_ceilings"]
    }
    assert ladder[1]["architecture_by_access_interaction"] == 0.0
    assert ladder[2]["architecture_by_access_interaction"] == 0.25
    assert ladder[3]["architecture_by_access_interaction"] == 0.0
    contrast = receipt["contrast"]
    assert contrast["routeable_adaptive_cost"] == 2
    assert contrast["routeable_fixed_cost"] == 3
    assert contrast["control_adaptive_cost"] == 2
    assert contrast["control_fixed_cost"] == 2
    assert contrast["routeable_fixed_terminal_accuracy"] == 0.75
    assert contrast["control_fixed_terminal_accuracy"] == 1.0
    assert contrast["same_physical_cue_vectors"] is True
    assert contrast["target_relabelled_cue_vector_count"] == 2
