import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "manuscript" / "ROUTEABILITY_PREREGISTRATION_TEMPLATE_V1.md"
GATE = ROOT / "validation" / "routeability_preregistration_gate_v1.json"
FINALIZER = ROOT / "examples" / "finalize_routeability_preregistration.py"


def _payload():
    return {
        "preregistration_version": "v1-final-test-fixture",
        "species": "Bombus testus",
        "study_site": "Test laboratory",
        "ethics_approval": "TEST-APPROVAL-001",
        "planned_start_date": "2099-01-01",
        "individuals_per_cell": 20,
        "colony_count": 4,
        "trials_per_individual": 12,
        "power_surface_reference": "validation/final_power_surface.csv",
        "power_surface_sha256": "a" * 64,
        "h1_sesoi": 0.12,
        "h2_sesoi": 0.10,
        "sesoi_provenance": "practical_decision_threshold",
        "apparatus_description": "Three-window artificial-flower apparatus",
        "cue_alphabet_description": "Counterbalanced binary visual symbols",
        "nominal_cue_duration_seconds": 1.0,
        "cue_duration_tolerance_seconds": 0.1,
        "response_window_seconds": 3.0,
        "pilot_receipt_reference": "validation/pilot_receipt.json",
        "pilot_receipt_sha256": "b" * 64,
        "familiarization_protocol": "Architecture-neutral familiarization",
        "training_dose": "4 full-information blocks",
        "randomization_seed": 20260927,
        "colony_allocation_rule": "Complete 12-cell treatment blocks within colony",
        "exclusion_rules": "Apparatus failure or identity loss only",
        "final_n_decision_rule": "Smallest robust-grid N meeting frozen H1/H2 criterion",
        "frozen_precollection_commit": "1" * 40,
        "final_schedule_reference": "validation/final_schedule.csv",
        "final_schedule_sha256": "c" * 64,
        "final_stimulus_reference": "validation/final_stimuli.csv",
        "final_stimulus_sha256": "d" * 64,
    }


def test_preregistration_template_is_explicitly_blocked():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "TEMPLATE ONLY — NOT YET PREREGISTERABLE" in text
    assert "{{individuals_per_cell}}" in text
    assert "{{response_window_seconds}}" in text
    assert "{{ethics_approval}}" in text


def test_preregistration_gate_requires_pilot_power_and_human_inputs():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    assert data["status"] == (
        "template_ready_finalization_blocked_on_pilot_power_and_operational_inputs"
    )
    required = data["required_before_finalization"]
    assert "procedural pilot response window frozen" in required
    assert "final GLMM operating-characteristic robustness surface completed" in required
    assert "ethics/regulatory approval recorded" in required
    assert data["current_output_status"] == "no final preregistration generated"


def test_finalizer_generates_complete_candidate_from_full_payload(tmp_path):
    input_json = tmp_path / "input.json"
    output_md = tmp_path / "final.md"
    input_json.write_text(json.dumps(_payload()), encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(FINALIZER), str(input_json), str(output_md)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr

    text = output_md.read_text(encoding="utf-8")
    assert "FINALIZED PRE-COLLECTION PREREGISTRATION CANDIDATE" in text
    assert "{{" not in text
    assert "individuals per cell: 20" in text
    assert "total randomized individuals: 240" in text
    assert "H1 probability-scale SESOI: 0.12" in text
    assert "TEST-APPROVAL-001" in text
    assert "`" + "a" * 64 + "`" in text
    assert "`" + "b" * 64 + "`" in text


def test_finalizer_rejects_missing_or_pending_human_fields(tmp_path):
    missing = _payload()
    del missing["ethics_approval"]
    input_json = tmp_path / "missing.json"
    output_md = tmp_path / "final.md"
    input_json.write_text(json.dumps(missing), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(FINALIZER), str(input_json), str(output_md)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "missing fields" in completed.stderr

    pending = _payload()
    pending["ethics_approval"] = "PENDING"
    input_json.write_text(json.dumps(pending), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(FINALIZER), str(input_json), str(output_md)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "pending placeholder" in completed.stderr


def test_finalizer_rejects_theory_ceiling_and_unbalanced_cell_n(tmp_path):
    bad = _payload()
    bad["sesoi_provenance"] = "theoretical_information_ceiling"
    input_json = tmp_path / "bad.json"
    output_md = tmp_path / "final.md"
    input_json.write_text(json.dumps(bad), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(FINALIZER), str(input_json), str(output_md)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "forbidden SESOI provenance" in completed.stderr

    bad = _payload()
    bad["individuals_per_cell"] = 18
    input_json.write_text(json.dumps(bad), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(FINALIZER), str(input_json), str(output_md)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "multiple of four" in completed.stderr


def test_finalizer_rejects_unhashed_or_fixture_power_inputs(tmp_path):
    bad = _payload()
    bad["power_surface_sha256"] = "not-a-hash"
    input_json = tmp_path / "bad.json"
    output_md = tmp_path / "final.md"
    input_json.write_text(json.dumps(bad), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(FINALIZER), str(input_json), str(output_md)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "64-character SHA-256" in completed.stderr

    bad = _payload()
    bad["power_surface_reference"] = "artifact/software_fixture_summary.csv"
    input_json.write_text(json.dumps(bad), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(FINALIZER), str(input_json), str(output_md)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    assert "cannot point to a software fixture" in completed.stderr
