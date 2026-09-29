import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_rewiring_claim_resolution_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_claim_resolution_rejects_general_rewiring_mechanism():
    data = _result()
    assert data["claim_decisions"]["current_opportunity_drives_latent_link_rewiring"].startswith(
        "NOT_SUPPORTED"
    )
    assert data["claim_decisions"]["routeability_validated"] == "NO"


def test_claim_resolution_preserves_detection_activity_result():
    data = _result()
    assert data["claim_decisions"]["current_opportunity_tracks_current_detectability_activity"].startswith(
        "SUPPORTED"
    )
    assert "4/6" in data["evidence_chain"][5]["result"]


def test_claim_resolution_uses_observed_turnover_language():
    data = _result()
    assert "observed-link turnover" in data["allowed_terms"]
    assert "853 ecological rewiring events" in data["forbidden_terms_without_new_evidence"]


def test_claim_resolution_points_to_direct_mechanism_gate():
    data = _result()
    assert "controlled routeability experiment" in data["next_scientific_gate"]


def test_claim_resolution_records_observation_model_sensitivity():
    data = _result()
    assert data["claim_decisions"]["detection_corrected_true_rewiring_identified"].startswith(
        "NO:"
    )
    level7 = [row for row in data["evidence_chain"] if row["level"] == 7]
    assert len(level7) == 1
    assert "6/6" in level7[0]["result"]
    assert "6/6" in level7[0]["boundary"]
    assert "observation-model dependent" in level7[0]["boundary"]


def test_claim_resolution_has_observational_stop_rule():
    data = _result()
    assert "Stop adding flexible Villavicencio observation models" in data[
        "next_scientific_gate"
    ]
    assert "does not identify binary or detection-corrected ecological rewiring" in data[
        "claim_ceiling"
    ]


def test_claim_resolution_has_one_line_final_status_vector():
    data = _result()
    status = data["final_status_vector"]
    assert status["sampling_effort_semantics"] == (
        "RESOLVED_RAW_5MIN_CENSUS_IDENTITY"
    )
    assert status["binary_observed_link_state"] == (
        "MATERIAL_DETECTION_SENSITIVITY_NOT_LATENT_TRUTH"
    )
    assert status["effort_standardized_interaction_incidence"] == (
        "MIXED_OPPORTUNITY_INCREMENT_4_OF_6"
    )
    assert status["latent_link_state_opportunity_effect"] == (
        "NOT_GENERAL_STATE_SUPPORT_1_OF_6_REQUIRED_5_OF_6"
    )
    assert status["natural_ecological_rewiring"] == "NOT_IDENTIFIED"
    assert status["routeability"] == "NOT_VALIDATED"
    assert "Sampling effort is no longer unresolved" in data["resolution_sentence"]


def test_claim_resolution_integrates_exact_detection_effort_identity():
    data = _result()
    status = data["final_status_vector"]
    assert status["detection_effort_observation_map"] == (
        "EXACT_IDENTITY_WITH_STRONG_DIAGNOSTIC_ALIGNMENT_AUC_0_852"
    )
    decision = data["claim_decisions"][
        "observed_gain_loss_direction_explainable_by_detection_map"
    ]
    assert decision.startswith("SUPPORTED_MECHANISTICALLY")
    level8 = [row for row in data["evidence_chain"] if row["level"] == 8]
    assert len(level8) == 1
    assert "0.852" in level8[0]["result"]
    assert "persistent latent link" in level8[0]["result"]


def test_claim_resolution_freezes_no_more_flexible_observation_models():
    data = _result()
    stop = data["observational_stop_rule"]
    assert stop["status"] == "FROZEN_STOP"
    assert len(stop["trigger"]) >= 5
    assert "Do not add further flexible Villavicencio observation models" in stop[
        "consequence"
    ]
    assert "controlled routeability experiment with an independent decision layer" in stop[
        "allowed_next_evidence"
    ]
