import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "routeability_roster_randomization_gate_v1.json"


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_roster_gate_freezes_complete_within_colony_blocks():
    data = _gate()
    assert data["status"] == "algorithm_frozen_actual_eligible_roster_pending"
    assert data["blocking"]["treatment_cell_count"] == 12
    assert "within a single colony" in data["blocking"]["rule"]
    assert "one individual to every architecture x access x budget cell" in data[
        "blocking"
    ]["rule"]


def test_roster_gate_blocks_outcome_dependent_eligibility_and_replacement():
    data = _gate()
    forbidden_inputs = data["eligible_roster"]["forbidden_inputs"]
    assert "architecture-specific training accuracy" in forbidden_inputs
    assert "test accuracy or behavioral outcome" in forbidden_inputs
    assert "H1/H2 or other focal-effect information" in forbidden_inputs

    forbidden = data["forbidden"]
    assert any("replacement individuals" in item for item in forbidden)
    assert any("unassigned eligible individuals" in item for item in forbidden)


def test_roster_gate_requires_hash_seed_and_pretraining_freeze():
    data = _gate()
    assert "SHA-256" in data["eligible_roster"]["hash_rule"]
    assert "before assignments are generated" in data["timing"]["randomization_seed"]
    required = data["finalization"]["required_before_confirmatory_collection"]
    assert "eligible roster and colony IDs frozen" in required
    assert "randomization seed frozen" in required
    assert any("before architecture-specific training" in item for item in required)


def test_roster_gate_keeps_colony_in_hierarchical_analysis():
    data = _gate()
    assert "does not make colony a negligible biological source" in data["claim_ceiling"]
    assert "hierarchical factor" in data["claim_ceiling"]
