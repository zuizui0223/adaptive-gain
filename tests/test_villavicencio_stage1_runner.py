import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "examples" / "villavicencio_stage1_from_csv.py"


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def test_stage1_runner_emits_machine_readable_receipt(tmp_path):
    interactions = tmp_path / "interactions.csv"
    transitions = tmp_path / "transitions.csv"
    output = tmp_path / "result.json"
    dyads = tmp_path / "dyads.csv"

    _write(
        interactions,
        "period,plant,pollinator,weight\n"
        "early,p1,q1,1\n"
        "early,p2,q2,1\n"
        "mid,p1,q2,1\n"
        "mid,p2,q1,1\n",
    )
    _write(
        transitions,
        "previous_period,current_period,role\n"
        "early,mid,primary\n",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            str(interactions),
            str(transitions),
            "--output",
            str(output),
            "--dyad-output",
            str(dyads),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["decision_equivalence_inferred"] is False
    assert result["primary_transition_count"] == 1
    assert result["primary_external_presence_count"] == 0
    receipt = result["transitions"][0]["receipt"]
    assert receipt["shared_species_rewiring_count"] == 4
    assert receipt["species_turnover_link_count"] == 0
    assert receipt["exact_partition"] is True

    with dyads.open(newline="", encoding="utf-8") as handle:
        dyad_rows = list(csv.DictReader(handle))
    assert len(dyad_rows) == 4
    assert {row["direction"] for row in dyad_rows} == {"gain", "loss"}


def test_stage1_runner_rejects_unverified_presence_by_default(tmp_path):
    interactions = tmp_path / "interactions.csv"
    transitions = tmp_path / "transitions.csv"
    presence = tmp_path / "presence.csv"

    _write(
        interactions,
        "period,plant,pollinator,weight\n"
        "early,p1,q1,1\n"
        "mid,p1,q2,1\n",
    )
    _write(
        transitions,
        "previous_period,current_period,role\n"
        "early,mid,primary\n",
    )
    _write(
        presence,
        "period,guild,species,basis\n"
        "early,plant,p1,matrix_axis_not_verified_presence\n"
        "early,pollinator,q1,matrix_axis_not_verified_presence\n"
        "early,pollinator,q2,matrix_axis_not_verified_presence\n"
        "mid,plant,p1,matrix_axis_not_verified_presence\n"
        "mid,pollinator,q1,matrix_axis_not_verified_presence\n"
        "mid,pollinator,q2,matrix_axis_not_verified_presence\n",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            str(interactions),
            str(transitions),
            "--presence",
            str(presence),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "presence basis is not independently verified" in completed.stderr


def test_stage1_runner_accepts_verified_presence(tmp_path):
    interactions = tmp_path / "interactions.csv"
    transitions = tmp_path / "transitions.csv"
    presence = tmp_path / "presence.csv"
    output = tmp_path / "result.json"

    _write(
        interactions,
        "period,plant,pollinator,weight\n"
        "early,p1,q1,1\n"
        "mid,p1,q2,1\n",
    )
    _write(
        transitions,
        "previous_period,current_period,role\n"
        "early,mid,primary\n",
    )
    _write(
        presence,
        "period,guild,species,basis\n"
        "early,plant,p1,independent_occurrence\n"
        "early,pollinator,q1,independent_occurrence\n"
        "early,pollinator,q2,independent_occurrence\n"
        "mid,plant,p1,independent_occurrence\n"
        "mid,pollinator,q1,independent_occurrence\n"
        "mid,pollinator,q2,independent_occurrence\n",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            str(interactions),
            str(transitions),
            "--presence",
            str(presence),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["primary_external_presence_count"] == 1
    receipt = result["transitions"][0]["receipt"]
    assert receipt["shared_species_rewiring_count"] == 2
    assert receipt["species_turnover_link_count"] == 0
    assert receipt["presence_basis"] == "externally_supplied_presence"
