import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "examples" / "build_routeability_procedural_pilot_receipt.py"


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def test_procedural_pilot_exporter_builds_power_bridge_ready_receipt(tmp_path):
    pilot_a = tmp_path / "pilot_a.csv"
    pilot_b = tmp_path / "pilot_b.csv"
    randomized = tmp_path / "randomized.csv"
    output = tmp_path / "receipt.json"

    _write(
        pilot_a,
        "terminal_latency_seconds\n"
        + "1.0\n" * 19
        + "4.0\n",
    )
    _write(
        pilot_b,
        "individual_id,colony_id,correct_within_window,timeout,block\n"
        "i1,c1,1,0,1\n"
        "i1,c1,1,0,2\n"
        "i2,c1,0,0,1\n"
        "i2,c1,0,0,2\n"
        "i3,c2,1,0,1\n"
        "i3,c2,0,0,2\n",
    )
    _write(
        randomized,
        "individual_id\n"
        "i1\n"
        "i2\n"
        "i3\n"
        "i4\n",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            str(pilot_a),
            str(pilot_b),
            str(output),
            "--candidate-windows",
            "1,2,3,4",
            "--upper-bound",
            "4",
            "--randomized-individuals",
            str(randomized),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["response_window_seconds"] == 1.0
    assert result["power_bridge_ready"] is True
    pooled = result["pooled_full_information"]
    assert pooled["randomized_individual_dropout_fraction"] == 0.25
    assert pooled["trial_icc_moment"] is not None
    assert result["focal_architecture_access_contrast_opened"] is False


def test_procedural_pilot_exporter_rejects_focal_columns(tmp_path):
    pilot_a = tmp_path / "pilot_a.csv"
    pilot_b = tmp_path / "pilot_b.csv"
    output = tmp_path / "receipt.json"
    _write(pilot_a, "terminal_latency_seconds\n1\n1\n")
    _write(
        pilot_b,
        "individual_id,colony_id,correct_within_window,timeout,block,architecture\n"
        "i1,c1,1,0,1,routeable\n",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(EXPORTER),
            str(pilot_a),
            str(pilot_b),
            str(output),
            "--candidate-windows",
            "1,2",
            "--upper-bound",
            "2",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "forbidden focal columns" in completed.stderr
