import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_annual_stage1_fallback_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_annual_fallback_is_historical_detection_sensitive_surface():
    data = _result()
    assert data["status"] == "green_detection_sensitive_response_estimability"
    assert data["design"]["detection_sensitive"] is True
    assert data["current_resolution"]["sampling_effort_semantics"] == (
        "RESOLVED_RAW_5MIN_CENSUS_IDENTITY"
    )
    assert data["current_resolution"]["natural_rewiring_status"] == (
        "NOT_IDENTIFIED"
    )


def test_legacy_rewiring_fields_are_explicitly_observed_turnover_only():
    data = _result()["transition_field_semantics"]
    assert "legacy field name" in data["rewiring_count"]
    assert "not identified ecological rewiring" in data["rewiring_count"]
    assert "observed binary change fraction" in data[
        "rewiring_opportunity_rate"
    ]


def test_annual_fallback_points_to_final_claim_resolution_and_stop_rule():
    data = _result()
    assert data["supersession"]["ecological_interpretation_superseded_by"] == (
        "validation/villavicencio_rewiring_claim_resolution_v1.json"
    )
    assert data["next_gate"].startswith("OBSERVATIONAL_STOP_RULE_REACHED")
    ceiling = data["claim_ceiling"].lower()
    assert "observed-link turnover" in ceiling
    assert "true rewiring" in ceiling
    assert "routeability" in ceiling
