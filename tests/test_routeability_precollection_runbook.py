import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "manuscript" / "ROUTEABILITY_PRECOLLECTION_RUNBOOK_V1.md"
GATE = ROOT / "validation" / "routeability_precollection_runbook_gate_v1.json"


def test_runbook_sequence_is_frozen():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    assert data["status"] == "ordered_operational_handoff_frozen"
    assert data["authoritative_sequence"][0] == "candidate_material_set"
    assert data["authoritative_sequence"][-1] == "begin_confirmatory_collection"
    assert data["resolved_before_real_input"]["SESOI_H1"] == 0.10
    assert data["resolved_before_real_input"]["SESOI_H2"] == 0.10
    assert data["resolved_before_real_input"]["robustness_scenarios_per_N"] == 12
    assert data["resolved_before_real_input"]["minimum_simulations_per_scenario"] >= 1000


def test_runbook_keeps_pilot_and_power_firewalls():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    firewalls = " ".join(data["firewalls"]).lower()
    assert "no b2 or h1/h2" in firewalls
    assert "0.25" in firewalls
    assert "mechanically selected" in firewalls
    assert "preregistration" in firewalls


def test_runbook_points_to_real_next_action():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    assert "material-pretest" in data["current_blocker"]
    assert "architecture-neutral material qualification" in data["next_action"]


def test_runbook_markdown_has_all_hard_gates():
    text = RUNBOOK.read_text(encoding="utf-8")
    for phrase in (
        "Gate 2 — architecture-neutral material pretest",
        "Gate 3 — Pilot A",
        "Gate 4 — Pilot B",
        "Gate 7 — run final GLMM operating characteristics",
        "Gate 8 — select N mechanically",
        "Gate 11 — finalize preregistration",
        "Gate 12 — confirmatory collection may begin",
        "Do not hand-select N.",
    ):
        assert phrase in text
