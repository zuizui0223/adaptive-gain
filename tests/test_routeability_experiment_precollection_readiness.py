import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "validation" / "routeability_experiment_precollection_readiness_v1.json"


def _ledger():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def test_precollection_readiness_marks_design_gates_green_but_power_blocked():
    data = _ledger()
    assert data["status"] == "design_complete_pilot_and_final_power_pending"
    assert data["frozen_v5_unchanged"] is True
    by_item = {row["item"]: row for row in data["gates"]}
    assert by_item["exact routeable versus bypass contrast"]["status"] == "PASS"
    assert by_item["generic randomization/counterbalance schedule mechanics"]["status"] == "PASS"
    assert by_item["eligible-roster treatment randomization"]["status"] == "PASS_CODE_ONLY"
    assert by_item["roster-to-final trial schedule linkage"]["status"] == "PASS_CODE_ONLY"
    assert by_item["confirmatory estimands and multiplicity"]["status"] == "PASS"
    assert by_item["external H1/H2 SESOI"]["status"] == "PASS_FROZEN"
    assert by_item["final GLMM operating-characteristic simulation"]["status"] == "BLOCKED_INPUTS_CODE_READY"
    assert by_item["definitive biological sample size"]["status"] == "BLOCKED"


def test_precollection_readiness_keeps_operational_and_human_blocks_explicit():
    data = _ledger()
    by_item = {row["item"]: row for row in data["gates"]}
    assert by_item["species/husbandry/apparatus implementation"]["status"] == "BLOCKED_OPERATIONAL"
    assert by_item["ethics and regulatory approval"]["status"] == "BLOCKED_HUMAN"
    assert by_item["confirmatory preregistration package"]["status"] == "TEMPLATE_READY_FINALIZATION_BLOCKED"


def test_precollection_readiness_points_to_pilot_as_next_biological_action():
    data = _ledger()
    assert "Pilot A" in data["next_biological_action"]
    assert "Pilot B" in data["next_biological_action"]
    assert "GLMM operating-characteristic simulator" in data["next_machine_action"]
    assert "does not mean animal work" in data["claim_ceiling"]
