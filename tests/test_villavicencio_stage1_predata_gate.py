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


def test_source_manifest_records_partial_verified_materialization():
    data = json.loads(SOURCES.read_text(encoding="utf-8"))
    assert data["status"] == "trait_bytes_verified_response_metadata_only"
    assert len(data["sources"]) == 2
    response, traits = data["sources"]
    assert response["raw_sha256"] is None
    assert traits["raw_sha256"] == traits["target_file"]["published_digest"]
    assert traits["materialization"]["dryad_digest_match"] is True


def test_source_manifest_records_18_network_response_surface():
    data = json.loads(SOURCES.read_text(encoding="utf-8"))
    response = data["sources"][0]
    assert response["doi"] == "10.5061/dryad.j6q573n9j"
    assert response["declared_network_count"] == 18
    assert "three subseasons per year" in response["declared_temporal_grain"]


def test_source_manifest_freezes_published_file_identity():
    data = json.loads(SOURCES.read_text(encoding="utf-8"))
    response, traits = data["sources"]

    assert response["dryad_version_id"] == 57785
    assert response["target_file"]["file_id"] == 268444
    assert response["target_file"]["digest_type"] == "sha-256"
    assert len(response["target_file"]["published_digest"]) == 64

    assert traits["dryad_version_id"] == 87009
    assert traits["target_file"]["file_id"] == 449108
    assert traits["target_file"]["digest_type"] == "sha-256"
    assert len(traits["target_file"]["published_digest"]) == 64


def test_source_manifest_pins_trait_mirror_without_trusting_name_alone():
    data = json.loads(SOURCES.read_text(encoding="utf-8"))
    traits = data["sources"][1]
    mirror = traits["public_mirror_candidate"]
    assert mirror["repository"] == "Ecological-Complexity-Lab/emln_package"
    assert len(mirror["commit"]) == 40
    assert mirror["size_bytes"] == traits["target_file"]["size_bytes"]
    assert mirror["status"] == "pinned_pending_dryad_sha256_verification"
    assert "published Dryad digest" in mirror["admission_rule"]


def test_stage1_gate_records_green_annual_response_estimability():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    annual = data["annual_detection_sensitive_fallback"]
    assert data["status"] == "annual_repaired_opportunity_green_primary_subseason_blocked"
    assert annual["transition_count"] == 5
    assert annual["shared_dyad_rows"] == 7620
    assert annual["changed_count"] == 1134
    assert annual["unchanged_count"] == 6486
    assert annual["transitions_with_both_outcomes"] == 5
    assert annual["join_unmatched_plants"] == 0
    assert annual["join_unmatched_pollinators"] == 0
    assert annual["gate"] == "PASS_response_estimability"
    assert data["stage1_success_gate_status"]["conventional_filter_join"] == "PASS_NUMERIC_SURFACE"
    assert data["stage1_success_gate_status"]["focal_excluded_opportunity_repair"] == "PASS_CURRENT_STATE_OPPORTUNITY"
