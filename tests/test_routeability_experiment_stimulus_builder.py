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

    receipt = json.loads(json_path.read_text(encoding="utf-8"))
    assert receipt["exact_minimal_contrast"] is True
    assert receipt["primary_budget"] == 2
    assert receipt["stimulus_row_count"] == 8
    assert receipt["primary_information_interaction"] == 0.25
    contrast = receipt["contrast"]
    assert contrast["routeable_adaptive_cost"] == 2
    assert contrast["routeable_fixed_cost"] == 3
    assert contrast["control_adaptive_cost"] == 2
    assert contrast["control_fixed_cost"] == 2
    assert contrast["routeable_fixed_terminal_accuracy"] == 0.75
    assert contrast["control_fixed_terminal_accuracy"] == 1.0
