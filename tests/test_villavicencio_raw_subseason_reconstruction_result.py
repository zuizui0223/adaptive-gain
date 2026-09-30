import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "validation" / "villavicencio_raw_subseason_reconstruction_result_v1.json"


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_raw_subseason_reconstructs_all_documented_periods_and_transitions():
    data = _result()
    assert data["status"] == "raw_18_subseason_response_reconstructed"
    assert data["reconstruction"]["period_count"] == 18
    primary = data["primary_within_year_stage1"]
    assert primary["transition_count"] == 12
    assert primary["eligible_shared_dyad_rows"] == 4581
    assert primary["changed_count"] == 853
    assert primary["gain_count"] == 422
    assert primary["loss_count"] == 431
    assert primary["transitions_with_both_changed_and_unchanged"] == 12


def test_raw_subseason_keeps_date_missingness_visible():
    data = _result()
    rec = data["reconstruction"]
    assert rec["undated_positive_rows"] == 26
    assert rec["undated_positive_visits"] == 45
    assert rec["undated_years"] == [2011]
    assert rec["annual_link_support"]["2011"]["only_undated"] == 7
    for year in ("2006", "2007", "2008", "2009", "2010"):
        assert rec["annual_link_support"][year]["only_undated"] == 0


def test_raw_subseason_records_endpoint_model_boundary():
    data = _result()
    boundary = data["endpoint_model_boundary"]
    assert boundary["degenerate_transition"] == "2006_mid->2006_late"
    assert boundary["degenerate_endpoint"] == "loss"
    assert boundary["counts"] == {"gain": 1, "loss": 0}
    assert "nondegenerate prespecified scope" in boundary["consequence"]


def test_raw_subseason_does_not_claim_rdata_identity_or_routeability():
    data = _result()
    assert data["source"]["published_rdata_bytes_used"] is False
    assert any("byte-for-byte equality" in item for item in data["not_established"])
    ceiling = data["claim_ceiling"].lower()
    assert "exact rdata identity" in ceiling
    assert "routeability" in ceiling


def test_raw_subseason_is_observed_turnover_not_identified_rewiring():
    data = _result()
    followup = data["sampling_effort_followup"]
    assert followup["status"] == (
        "EFFORT_SEMANTICS_RESOLVED_BINARY_DETECTION_MATERIAL"
    )
    assert "not 853 identified ecological rewiring events" in followup["consequence"]
    ceiling = data["claim_ceiling"].lower()
    assert "sampling-effort-corrected rewiring" in ceiling
    assert "binary detection is materially effort-sensitive" in ceiling
