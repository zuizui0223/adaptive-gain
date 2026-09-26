import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "villavicencio_stage1_predata_gate_v1.json"
SOURCES = ROOT / "validation" / "villavicencio_source_manifest_v1.json"


def test_stage1_gate_freezes_twelve_within_year_transitions():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    design = data["primary_temporal_design"]
    assert design["expected_primary_transition_count"] == 12
    assert design["transitions_per_year"] == ["early_to_mid", "mid_to_late"]
    assert design["year_boundary_transitions"] == "sensitivity_only"


def test_stage1_gate_separates_presence_from_detection():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    policy = data["presence_policy"]
    assert policy["preferred"] == "independent species presence or abundance information"
    assert policy["fallback"] == "positive observed links"
    assert policy["fallback_label"] == "detection_sensitive"
    assert "zero observed degree" in policy["forbidden"]


def test_stage1_gate_forbids_decision_class_proxying():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    assert data["decision_structure_policy"]["stage1_decision_equivalence_inference"] is False
    assert "trait clusters" in data["compatibility_policy"]["forbidden"]
    assert "cannot validate environmental routeability" in data["claim_ceiling"]


def test_source_manifest_keeps_unmaterialized_checksums_null():
    data = json.loads(SOURCES.read_text(encoding="utf-8"))
    assert data["status"] == "source_metadata_verified_raw_bytes_not_frozen"
    assert len(data["sources"]) == 2
    assert all(source["raw_sha256"] is None for source in data["sources"])


def test_source_manifest_records_18_network_response_surface():
    data = json.loads(SOURCES.read_text(encoding="utf-8"))
    response = data["sources"][0]
    assert response["doi"] == "10.5061/dryad.j6q573n9j"
    assert response["declared_network_count"] == 18
    assert "three subseasons per year" in response["declared_temporal_grain"]
