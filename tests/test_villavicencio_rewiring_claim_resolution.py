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
