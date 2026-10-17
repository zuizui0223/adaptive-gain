"""Test-first field-plan creation, immutable allocation and independent verification.

All IDs, seeds and presentations are SYNTHETIC. These tests are not data from bees.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from adaptive_gain.pilot_itt import analyze_pilot_itt, read_bee_roster_csv, read_trial_log_csv
from adaptive_gain.pilot_process import read_fixed_cue_plan_csv
from adaptive_gain.pilot_design import (
    BeeInventory, design_pilot, read_inventory_csv, write_pilot_design,
    verify_pilot_design, render_pilot_design, _stimulus_schedule_for_bee,
)

SEED = bytes(range(32)).hex()
OTHER_SEED = bytes(range(32, 64)).hex()


def inventory():
    return tuple(BeeInventory(f"c{col}_bee{i}", f"colony_{col}")
                 for col in (1, 2) for i in range(4))


def test_colony_allocation_and_target_context_balanced_per_bee():
    d = design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED)
    assert len(d.roster) == 8
    assert len(d.presentations) == len(d.trial_template) == 64
    assert len(d.fixed_plans) == 32
    for col in ("colony_1", "colony_2"):
        arms = Counter(b.assigned_access for b in d.roster if b.colony_id == col)
        assert arms == {"contingent": 2, "precommitted": 2}
    by_bee = {b.bee_id: b for b in d.roster}
    by_fixed = {p.trial_id: p for p in d.fixed_plans}
    assert len(by_fixed) == len(d.fixed_plans)
    for bee in by_bee:
        presentation = [p for p in d.presentations if p.bee_id == bee]
        assert [s.slot for s in presentation] == list(range(1, 9))
        assert Counter((s.target, s.context_truth) for s in presentation) == {
            (0, 0): 2, (0, 1): 2, (1, 0): 2, (1, 1): 2
        }
        assert {s.first_cue for s in presentation} == {"A"}
        if by_bee[bee].assigned_access == "precommitted":
            assert Counter((s.target, s.context_truth,
                            by_fixed[s.trial_id].second_cue) for s in presentation) == {
                (target, context, cue): 1 for target in (0, 1)
                for context in (0, 1) for cue in ("B", "C")
            }
        else:
            assert all(s.trial_id not in by_fixed for s in presentation)


def test_deterministic_across_inventory_row_order_and_new_seed_changes_assignments():
    a = render_pilot_design(design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED))
    b = render_pilot_design(design_pilot(reversed(inventory()), slots_per_bee=8, seed_hex=SEED))
    c = render_pilot_design(design_pilot(inventory(), slots_per_bee=8, seed_hex=OTHER_SEED))
    assert a == b
    assert any(a[name] != c[name] for name in ("bee_roster.csv", "stimulus_schedule.csv"))
    assert SEED.encode() not in b"".join(a.values())
    assert OTHER_SEED.encode() not in b"".join(c.values())


def test_marginal_stimuli_generated_independently_of_assigned_arm():
    # Validate domain-separated target/context schedule for every bee against
    # a pure function that receives NO treatment assignment argument.
    d = design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED)
    for b in d.roster:
        expected = _stimulus_schedule_for_bee(b.bee_id, SEED, slots_per_bee=8)
        observed = [(row.target, row.context_truth) for row in d.presentations
                    if row.bee_id == b.bee_id]
        assert observed == expected


def test_trial_template_is_nonobserved_not_artificial_success():
    d = design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED)
    assert all(t.outcome_status == "unobserved" and t.unobserved_reason == "not_yet_run"
               and t.final_action is None and t.delivered_access == "" for t in d.trial_template)
    report = analyze_pilot_itt(d.roster, d.trial_template, planned_trials_per_bee=8)
    assert report.unobserved == 64
    assert report.correct == report.wrong == report.abstain == 0
    assert (report.effect_lower, report.effect_upper) == (-1, 1)
    assert report.exact_randomization_p is None


def test_materialize_verify_and_parse_existing_analysis_csv(tmp_path):
    d = design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED)
    target = tmp_path / "sealed_plan"
    receipt = write_pilot_design(d, target)
    assert receipt["schema"] == "bee_randomized_pilot_design_v1"
    assert receipt["slot_count"] == 64
    assert receipt["slots_per_bee"] == 8
    assert receipt["actual_field_observations"] is False
    assert SEED not in (target / "design_manifest.json").read_text()
    assert verify_pilot_design(d, target) == receipt
    assert read_bee_roster_csv(target / "bee_roster.csv") == d.roster
    assert read_trial_log_csv(target / "bee_trials_template.csv") == d.trial_template
    assert read_fixed_cue_plan_csv(target / "bee_fixed_plans.csv") == d.fixed_plans
    with (target / "stimulus_schedule.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 64
    assert set(rows[0]) == {"trial_id", "bee_id", "slot", "target", "context_truth", "first_cue"}
    assert all(r["target"] in ("0", "1") and r["context_truth"] in ("0", "1") for r in rows)


def test_verified_locked_files_reject_modification_but_trial_copy_can_change(tmp_path):
    d = design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED)
    target = tmp_path / "sealed"
    write_pilot_design(d, target)
    template = target / "bee_trials_template.csv"
    template.write_text(template.read_text() + "# COLLECTED DATA SHOULD GO IN SEPARATE FILE\n")
    assert verify_pilot_design(d, target)["verified"] is True
    schedule = target / "stimulus_schedule.csv"
    changed = schedule.read_text().replace(",0,A\n", ",1,A\n", 1)
    assert changed != schedule.read_text()
    schedule.write_text(changed)
    with pytest.raises(ValueError, match="locked file mismatch"):
        verify_pilot_design(d, target)


def test_manifest_tampering_and_missing_fixed_plan_detected(tmp_path):
    d = design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED)
    target = tmp_path / "sealed"
    write_pilot_design(d, target)
    manifest = target / "design_manifest.json"
    orig = manifest.read_bytes()
    manifest.write_bytes(orig.replace(b'"slot_count": 64', b'"slot_count": 65'))
    with pytest.raises(ValueError, match="manifest mismatch"):
        verify_pilot_design(d, target)
    manifest.write_bytes(orig)
    plans = target / "bee_fixed_plans.csv"
    plans.write_text(plans.read_text().splitlines(keepends=True)[0])
    with pytest.raises(ValueError, match="locked file mismatch"):
        verify_pilot_design(d, target)


def test_no_overwrite_of_existing_output_or_secret_exposure(tmp_path):
    d = design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED)
    folder = tmp_path / "design"
    folder.mkdir()
    (folder / "original").write_text("NEVER REPLACE")
    with pytest.raises(FileExistsError):
        write_pilot_design(d, folder)
    assert (folder / "original").read_text() == "NEVER REPLACE"


@pytest.mark.parametrize("bad_inventory", [
    (BeeInventory("same", "c"), BeeInventory("same", "c")),
    (BeeInventory("", "c"), BeeInventory("other", "c")),
    (BeeInventory("a", ""), BeeInventory("b", "c")),
    (BeeInventory("a", "c"), BeeInventory("b", "c")),
    (BeeInventory("a", "c"), BeeInventory("b", "c"), BeeInventory("c", "c")),
])
def test_bad_bee_inventory_is_rejected(bad_inventory):
    with pytest.raises(ValueError):
        design_pilot(bad_inventory, slots_per_bee=8, seed_hex=SEED)


@pytest.mark.parametrize("slots", (0, -8, 4, 6, 9, 12, 1.0, True))
def test_bad_trial_balance_requirement_rejected(slots):
    with pytest.raises(ValueError, match="multiple of eight"):
        design_pilot(inventory(), slots_per_bee=slots, seed_hex=SEED)


@pytest.mark.parametrize("bad", ("", "1234", "x"*64, "0"*63, "0"*65, "0"*64+" "))
def test_seed_is_exactly_32_bytes_hex(bad):
    with pytest.raises(ValueError, match="seed"):
        design_pilot(inventory(), slots_per_bee=8, seed_hex=bad)


def test_inventory_csv_reader_and_cli_generate_verify_no_seed_printed(tmp_path):
    inv = tmp_path / "inventory.csv"
    inv.write_text("bee_id,colony_id\n" + "".join(f"{b.bee_id},{b.colony_id}\n" for b in inventory()))
    seed_file = tmp_path / "SECRET_DO_NOT_COMMIT.hex"
    seed_file.write_text(SEED + "\n")
    assert read_inventory_csv(inv) == inventory()
    target = tmp_path / "plan"
    prefix = [sys.executable, "-m", "adaptive_gain.pilot_design"]
    args = ["--inventory", str(inv), "--seed-file", str(seed_file),
            "--slots-per-bee", "8", "--outdir", str(target)]
    made = subprocess.run(prefix + ["generate"] + args, check=True, capture_output=True, text=True)
    assert SEED not in made.stdout and SEED not in made.stderr
    assert json.loads(made.stdout)["slot_count"] == 64
    verified = subprocess.run(prefix + ["verify"] + args, check=True, capture_output=True, text=True)
    assert json.loads(verified.stdout)["verified"] is True
    assert SEED not in verified.stdout
    with pytest.raises(FileExistsError):
        write_pilot_design(design_pilot(inventory(),slots_per_bee=8,seed_hex=SEED),target)


def test_bad_inventory_csv_header_rejected(tmp_path):
    p = tmp_path / "input.csv"
    p.write_text("bee_id\nx\n")
    with pytest.raises(ValueError, match="colony_id"):
        read_inventory_csv(p)


def test_generated_plan_roundtrips_into_pilot_process_audit():
    from adaptive_gain.pilot_process import CueEvent, audit_pilot_process
    d = design_pilot(inventory(), slots_per_bee=8, seed_hex=SEED)
    arms = {b.bee_id: b.assigned_access for b in d.roster}
    fixed = {p.trial_id: p.second_cue for p in d.fixed_plans}
    # SYNTHETIC mechanism-diagnostic witness, NOT observed cue reports or bees.
    events = []
    recorded = []
    for p, t in zip(d.presentations, d.trial_template):
        cue = fixed[p.trial_id] if arms[p.bee_id] == "precommitted" else (
            "B" if p.context_truth == 0 else "C"
        )
        events.extend((
            CueEvent(p.trial_id, p.bee_id, 1, "A", p.context_truth, 100),
            CueEvent(p.trial_id, p.bee_id, 2, cue, p.target, 350),
        ))
        recorded.append(replace(t, outcome_status="choice", final_action=p.target,
                                unobserved_reason="", delivered_access=arms[t.bee_id]))
    receipt = audit_pilot_process(d.roster, recorded, events, d.fixed_plans,
                                  planned_trials_per_bee=8, deadline_ms=1000)
    assert receipt.fixed_plan_mismatches == 0
    assert receipt.missing_fixed_plans == 0
    assert receipt.budget_violations == 0
    assert receipt.mechanism_status == "branch_order_observable_not_causal_proof"
    assert receipt.contingent_second_B_rate_A0 == 1.0
    assert receipt.contingent_second_B_rate_A1 == 0.0
    assert receipt.cue_event_rows == 128


def test_seed_generation_excludes_seed_from_stdout_and_refuses_overwrite(tmp_path):
    target = tmp_path / "private_seed.hex"
    cmd = [sys.executable, "-m", "adaptive_gain.pilot_design", "new-seed", "--out", str(target)]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    seed = target.read_text().strip()
    assert len(seed) == 64
    assert seed not in r.stdout and seed not in r.stderr
    assert json.loads(r.stdout)["private_seed_written"] is True
    import os
    if os.name == "posix":
        assert target.stat().st_mode & 0o777 == 0o600
    r2 = subprocess.run(cmd, capture_output=True, text=True)
    assert r2.returncode != 0
    assert target.read_text().strip() == seed


def test_sixteen_slot_balance_is_complete_and_compatible():
    d = design_pilot(inventory(), slots_per_bee=16, seed_hex=SEED)
    byfixed = {x.trial_id:x.second_cue for x in d.fixed_plans}
    arms = {r.bee_id:r.assigned_access for r in d.roster}
    for bee in arms:
        rows = [p for p in d.presentations if p.bee_id == bee]
        assert Counter((p.target,p.context_truth) for p in rows) == {
            (t,a):4 for t in (0,1) for a in (0,1)
        }
        if arms[bee] == "precommitted":
            assert Counter((p.target,p.context_truth,byfixed[p.trial_id]) for p in rows) == {
                (t,a,c):2 for t in (0,1) for a in (0,1) for c in ("B","C")
            }


def test_checked_in_design_validation_receipt_and_example_lock_bytes():
    from hashlib import sha256
    root = Path(__file__).resolve().parents[1]
    r = json.loads((root / "validation/pilot_design_v1.json").read_text())
    assert r["status"] == "synthetic_inventory_and_offline_plan_only_no_real_bee_trials"
    assert r["verification"]["complete_repo_checkout"] is False
    assert r["generator_constraints"]["target_context_assignment_independent"] is True
    d = design_pilot(read_inventory_csv(root / "experiments/templates/pilot_inventory_example.csv"),
                     slots_per_bee=8, seed_hex=SEED)
    rendered = render_pilot_design(d)
    assert r["synthetic_demo"]["locked_csv_sha256"] == {
        key: sha256(rendered[key]).hexdigest()
        for key in ("bee_fixed_plans.csv", "bee_roster.csv", "stimulus_schedule.csv")
    }
    assert r["synthetic_demo"]["seed_sha256_commitment"] == d.seed_commitment
    assert r["synthetic_demo"]["slot_count"] == 64
    for name, fingerprint in r["source_sha256"].items():
        assert sha256((root / name).read_bytes()).hexdigest() == fingerprint
