import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "manuscript" / "ROUTEABILITY_PREREGISTRATION_TEMPLATE_V1.md"
GATE = ROOT / "validation" / "routeability_preregistration_gate_v1.json"
FINALIZER = ROOT / "examples" / "finalize_routeability_preregistration.py"
STIMULUS_BUILDER = ROOT / "examples" / "build_routeability_experiment_stimuli.py"
RANDOMIZER = ROOT / "examples" / "randomize_routeability_roster.py"
SCHEDULE_COMPILER = ROOT / "examples" / "compile_routeability_final_schedule.py"
FINAL_N_SELECTOR = ROOT / "examples" / "select_routeability_final_n.py"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_finalizer(tmp_path: Path, payload: dict):
    input_json = tmp_path / "input.json"
    output_md = tmp_path / "final.md"
    input_json.write_text(json.dumps(payload), encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            str(FINALIZER),
            str(input_json),
            str(output_md),
            "--artifact-root",
            str(tmp_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed, output_md


def _prepare_artifacts(tmp_path: Path) -> dict:
    roster = tmp_path / "roster.csv"
    assignments = tmp_path / "assignments.csv"
    unassigned = tmp_path / "unassigned.csv"
    randomization = tmp_path / "randomization.json"
    schedule = tmp_path / "schedule.csv"
    schedule_receipt = tmp_path / "schedule_receipt.json"
    pilot = tmp_path / "pilot.json"
    power = tmp_path / "final_power_surface.csv"
    final_n_rule = tmp_path / "final_n_rule.json"
    final_n_receipt = tmp_path / "final_n_receipt.json"
    stimuli = tmp_path / "final_stimuli.csv"

    with roster.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["individual_id", "colony_id"])
        for colony in range(1, 5):
            for index in range(1, 13):
                writer.writerow([f"c{colony}_i{index:03d}", f"c{colony}"])

    randomized = subprocess.run(
        [
            sys.executable,
            str(RANDOMIZER),
            str(roster),
            str(assignments),
            str(unassigned),
            str(randomization),
            "--individuals-per-cell",
            "4",
            "--seed",
            "20260927",
            "--eligibility-rule",
            "architecture-neutral apparatus engagement completed",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert randomized.returncode == 0, randomized.stderr

    compiled = subprocess.run(
        [
            sys.executable,
            str(SCHEDULE_COMPILER),
            str(assignments),
            str(randomization),
            str(schedule),
            str(schedule_receipt),
            "--blocks-per-individual",
            "2",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert compiled.returncode == 0, compiled.stderr

    pilot.write_text(
        json.dumps(
            {
                "schema": "adaptive-gain-routeability-procedural-pilot-bundle-v1",
                "response_window_seconds": 3.0,
                "focal_architecture_access_contrast_opened": False,
            }
        ),
        encoding="utf-8",
    )
    power.write_text(
        "scenario_id,robustness_id,simulations,individuals_per_cell,trials_per_individual,"
        "colony_count,colony_block_counts,individual_sd_logit,colony_sd_logit,dropout_fraction,"
        "timeout_fraction,alpha_two_sided,sesoi_provenance,"
        "p_KF_B1,p_KC_B1,p_RF_B1,p_RC_B1,"
        "p_KF_B2,p_KC_B2,p_RF_B2,p_RC_B2,"
        "p_KF_B3,p_KC_B3,p_RF_B3,p_RC_B3,"
        "fit_success_fraction,h1_directional_rejection_fraction,"
        "h2_hierarchical_pass_fraction,expected_h1_delta_b2,expected_h2_localization\n"
        "n4_robust_a,a,1000,4,8,4,1;1;1;1,0.5,0.2,0.10,0.05,0.05,"
        "practical_decision_threshold_frozen_2026-09-29,"
        "0.50,0.51,0.50,0.53,0.60,0.62,0.58,0.72,0.70,0.71,0.70,0.73,"
        "0.99,0.82,0.80,0.10,0.10\n"
        "n4_robust_b,b,1000,4,8,4,1;1;1;1,0.8,0.3,0.15,0.08,0.05,"
        "practical_decision_threshold_frozen_2026-09-29,"
        "0.45,0.46,0.45,0.48,0.55,0.57,0.53,0.67,0.65,0.66,0.65,0.68,"
        "0.97,0.83,0.81,0.10,0.10\n"
        "n8_robust_a,a,1000,8,8,4,2;2;2;2,0.5,0.2,0.10,0.05,0.05,"
        "practical_decision_threshold_frozen_2026-09-29,"
        "0.50,0.51,0.50,0.53,0.60,0.62,0.58,0.72,0.70,0.71,0.70,0.73,"
        "0.99,0.90,0.87,0.10,0.10\n"
        "n8_robust_b,b,1000,8,8,4,2;2;2;2,0.8,0.3,0.15,0.08,0.05,"
        "practical_decision_threshold_frozen_2026-09-29,"
        "0.45,0.46,0.45,0.48,0.55,0.57,0.53,0.67,0.65,0.66,0.65,0.68,"
        "0.98,0.88,0.85,0.10,0.10\n",
        encoding="utf-8",
    )
    final_n_rule.write_text(
        json.dumps(
            {
                "minimum_fit_success_fraction": 0.95,
                "minimum_h1_directional_rejection_fraction": 0.80,
                "minimum_h2_hierarchical_pass_fraction": 0.80,
                "minimum_scenarios_per_n": 2,
                "minimum_simulations_per_scenario": 1000,
                "counterbalance_multiple": 4,
            }
        ),
        encoding="utf-8",
    )
    selected_n = subprocess.run(
        [
            sys.executable,
            str(FINAL_N_SELECTOR),
            str(power),
            str(final_n_rule),
            str(final_n_receipt),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert selected_n.returncode == 0, selected_n.stderr

    stimulus_receipt = tmp_path / "stimulus_receipt.json"
    built_stimuli = subprocess.run(
        [
            sys.executable,
            str(STIMULUS_BUILDER),
            str(stimuli),
            str(stimulus_receipt),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert built_stimuli.returncode == 0, built_stimuli.stderr

    return {
        "preregistration_version": "v1-final-test-fixture",
        "species": "Bombus testus",
        "study_site": "Test laboratory",
        "ethics_approval": "TEST-APPROVAL-001",
        "planned_start_date": "2099-01-01",
        "individuals_per_cell": 4,
        "colony_count": 4,
        "trials_per_individual": 8,
        "power_surface_reference": power.name,
        "power_surface_sha256": _sha(power),
        "final_n_rule_reference": final_n_rule.name,
        "final_n_rule_sha256": _sha(final_n_rule),
        "final_n_receipt_reference": final_n_receipt.name,
        "final_n_receipt_sha256": _sha(final_n_receipt),
        "h1_sesoi": 0.10,
        "h2_sesoi": 0.10,
        "sesoi_provenance": "practical_decision_threshold_frozen_2026-09-29",
        "apparatus_description": "Three-window artificial-flower apparatus",
        "cue_alphabet_description": "Counterbalanced binary visual symbols",
        "nominal_cue_duration_seconds": 1.0,
        "cue_duration_tolerance_seconds": 0.1,
        "response_window_seconds": 3.0,
        "pilot_receipt_reference": pilot.name,
        "pilot_receipt_sha256": _sha(pilot),
        "familiarization_protocol": "Architecture-neutral familiarization",
        "training_dose": "4 full-information blocks",
        "randomization_seed": 20260927,
        "colony_allocation_rule": "Complete 12-cell treatment blocks within colony",
        "exclusion_rules": "Apparatus failure or identity loss only",
        "final_n_decision_rule": "Smallest robust-grid N meeting frozen H1/H2 criterion",
        "frozen_precollection_commit": "1" * 40,
        "randomization_receipt_reference": randomization.name,
        "randomization_receipt_sha256": _sha(randomization),
        "final_assignment_reference": assignments.name,
        "final_assignment_sha256": _sha(assignments),
        "final_schedule_receipt_reference": schedule_receipt.name,
        "final_schedule_receipt_sha256": _sha(schedule_receipt),
        "final_schedule_reference": schedule.name,
        "final_schedule_sha256": _sha(schedule),
        "final_stimulus_reference": stimuli.name,
        "final_stimulus_sha256": _sha(stimuli),
    }


def test_preregistration_template_is_explicitly_blocked():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "TEMPLATE ONLY — NOT YET PREREGISTERABLE" in text
    assert "{{individuals_per_cell}}" in text
    assert "{{response_window_seconds}}" in text
    assert "{{ethics_approval}}" in text
    assert "{{randomization_receipt_sha256}}" in text
    assert "{{final_assignment_sha256}}" in text
    assert "{{final_schedule_receipt_sha256}}" in text
    assert "{{final_n_rule_sha256}}" in text
    assert "{{final_n_receipt_sha256}}" in text
    assert "primary confirmatory H1/H2 experiment uses guided contingent presentation" in text
    assert "Autonomous terminal-window routing is a separate mechanistic follow-up" in text


def test_preregistration_gate_requires_pilot_power_and_human_inputs():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    assert data["status"] == (
        "template_ready_finalization_blocked_on_pilot_power_and_operational_inputs"
    )
    required = data["required_before_finalization"]
    assert "procedural pilot response window frozen" in required
    assert "final GLMM operating-characteristic robustness surface completed" in required
    assert "ethics/regulatory approval recorded" in required
    assert "final schedule is compiled from the hash-matching randomized assignment artifact" in required
    assert data["current_output_status"] == "no final preregistration generated"


def test_finalizer_generates_complete_candidate_from_real_artifact_chain(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    completed, output_md = _run_finalizer(tmp_path, payload)
    assert completed.returncode == 0, completed.stderr

    text = output_md.read_text(encoding="utf-8")
    assert "FINALIZED PRE-COLLECTION PREREGISTRATION CANDIDATE" in text
    assert "{{" not in text
    assert "individuals per cell: 4" in text
    assert "total randomized individuals: 48" in text
    assert "H1 probability-scale SESOI: 0.1" in text
    assert "TEST-APPROVAL-001" in text
    assert payload["randomization_receipt_sha256"] in text
    assert payload["final_assignment_sha256"] in text
    assert payload["final_schedule_receipt_sha256"] in text


def test_finalizer_rejects_missing_or_pending_human_fields(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    missing = dict(payload)
    del missing["ethics_approval"]
    completed, _ = _run_finalizer(tmp_path, missing)
    assert completed.returncode != 0
    assert "missing fields" in completed.stderr

    pending = dict(payload)
    pending["ethics_approval"] = "PENDING"
    completed, _ = _run_finalizer(tmp_path, pending)
    assert completed.returncode != 0
    assert "pending placeholder" in completed.stderr


def test_finalizer_rejects_sesoi_drift_from_frozen_gate(tmp_path):
    payload = _prepare_artifacts(tmp_path)

    bad = dict(payload)
    bad["h1_sesoi"] = 0.11
    completed, _ = _run_finalizer(tmp_path, bad)
    assert completed.returncode != 0
    assert "must exactly match the frozen" in completed.stderr

    bad = dict(payload)
    bad["sesoi_provenance"] = "practical_decision_threshold"
    completed, _ = _run_finalizer(tmp_path, bad)
    assert completed.returncode != 0
    assert "must exactly match the frozen" in completed.stderr


def test_finalizer_rejects_theory_ceiling_and_unbalanced_cell_n(tmp_path):
    payload = _prepare_artifacts(tmp_path)

    bad = dict(payload)
    bad["sesoi_provenance"] = "theoretical_information_ceiling"
    completed, _ = _run_finalizer(tmp_path, bad)
    assert completed.returncode != 0
    assert "forbidden SESOI provenance" in completed.stderr

    bad = dict(payload)
    bad["individuals_per_cell"] = 18
    completed, _ = _run_finalizer(tmp_path, bad)
    assert completed.returncode != 0
    assert "multiple of four" in completed.stderr


def test_finalizer_rejects_unhashed_or_fixture_power_inputs(tmp_path):
    payload = _prepare_artifacts(tmp_path)

    bad = dict(payload)
    bad["power_surface_sha256"] = "not-a-hash"
    completed, _ = _run_finalizer(tmp_path, bad)
    assert completed.returncode != 0
    assert "64-character SHA-256" in completed.stderr

    bad = dict(payload)
    bad["power_surface_reference"] = "artifact/software_fixture_summary.csv"
    completed, _ = _run_finalizer(tmp_path, bad)
    assert completed.returncode != 0
    assert "cannot point to a software fixture" in completed.stderr


def test_finalizer_rejects_tampered_artifact_bytes(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    schedule = tmp_path / payload["final_schedule_reference"]
    schedule.write_text(
        schedule.read_text(encoding="utf-8") + "\n",
        encoding="utf-8",
    )
    completed, _ = _run_finalizer(tmp_path, payload)
    assert completed.returncode != 0
    assert "final_schedule_reference SHA-256 mismatch" in completed.stderr


def test_finalizer_rejects_rehashed_but_broken_assignment_chain(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    randomization_path = tmp_path / payload["randomization_receipt_reference"]
    randomization = json.loads(randomization_path.read_text(encoding="utf-8"))
    randomization["assignments_sha256"] = "0" * 64
    randomization_path.write_text(
        json.dumps(randomization, indent=2) + "\n",
        encoding="utf-8",
    )
    payload["randomization_receipt_sha256"] = _sha(randomization_path)

    completed, _ = _run_finalizer(tmp_path, payload)
    assert completed.returncode != 0
    assert "assignment hash disagrees" in completed.stderr


def test_finalizer_rejects_schedule_assignment_fidelity_break(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    schedule_path = tmp_path / payload["final_schedule_reference"]
    rows = list(
        csv.DictReader(schedule_path.open(newline="", encoding="utf-8"))
    )
    rows[0]["colony_id"] = "tampered_colony"
    fields = list(rows[0])
    with schedule_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    new_schedule_sha = _sha(schedule_path)
    payload["final_schedule_sha256"] = new_schedule_sha

    receipt_path = tmp_path / payload["final_schedule_receipt_reference"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["schedule_sha256"] = new_schedule_sha
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    payload["final_schedule_receipt_sha256"] = _sha(receipt_path)

    completed, _ = _run_finalizer(tmp_path, payload)
    assert completed.returncode != 0
    assert "final schedule assignment mismatch" in completed.stderr


def test_finalizer_rejects_power_surface_changed_after_final_n_selection(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    power = tmp_path / payload["power_surface_reference"]
    text = power.read_text(encoding="utf-8")
    text = text.replace(",0.99,0.82,0.80,0.12,0.10", ",0.98,0.82,0.80,0.12,0.10", 1)
    power.write_text(text, encoding="utf-8")
    payload["power_surface_sha256"] = _sha(power)

    completed, _ = _run_finalizer(tmp_path, payload)
    assert completed.returncode != 0
    assert "final-N receipt power-surface hash mismatch" in completed.stderr


def test_finalizer_rejects_rehashed_but_wrong_logical_stimulus_mapping(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    stimuli = tmp_path / payload["final_stimulus_reference"]
    rows = list(csv.DictReader(stimuli.open(newline="", encoding="utf-8")))
    rows[0]["target"] = "1" if rows[0]["target"] == "0" else "0"
    fields = list(rows[0])
    with stimuli.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    payload["final_stimulus_sha256"] = _sha(stimuli)

    completed, _ = _run_finalizer(tmp_path, payload)
    assert completed.returncode != 0
    assert "does not match the exact frozen" in completed.stderr


def test_finalizer_independently_recomputes_selected_final_n(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    receipt_path = tmp_path / payload["final_n_receipt_reference"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["selected_individuals_per_cell"] = 8
    receipt["total_randomized_individuals"] = 96
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    payload["final_n_receipt_sha256"] = _sha(receipt_path)

    completed, _ = _run_finalizer(tmp_path, payload)
    assert completed.returncode != 0
    assert "selected N disagrees with independent selector recomputation" in completed.stderr


def test_finalizer_rejects_changed_final_n_rule_after_selection(tmp_path):
    payload = _prepare_artifacts(tmp_path)
    rule_path = tmp_path / payload["final_n_rule_reference"]
    rule = json.loads(rule_path.read_text(encoding="utf-8"))
    rule["minimum_h2_hierarchical_pass_fraction"] = 0.79
    rule_path.write_text(
        json.dumps(rule, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    payload["final_n_rule_sha256"] = _sha(rule_path)

    completed, _ = _run_finalizer(tmp_path, payload)
    assert completed.returncode != 0
    assert "final-N receipt rule hash mismatch" in completed.stderr
