import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_opportunity_effort_control_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_annual_gain_opportunity_survives_focal_plant_effort_control():
    data = _result()["strict_core_2008_2011"]["gain"]
    inc = data["opportunity_increment_beyond_effort"]
    assert inc["delta_log_loss"] > 0.02
    assert inc["positive_folds"] == "3/3"
    assert inc["classification"] == "reproducible_incremental_information"
    assert (
        data["opportunity_plus_effort"]["log_loss"]
        < data["effort_only"]["log_loss"]
    )


def test_annual_loss_opportunity_is_not_promoted():
    data = _result()["strict_core_2008_2011"]["loss"]
    inc = data["opportunity_increment_beyond_effort"]
    assert inc["delta_log_loss"] > 0
    assert inc["positive_folds"] == "2/3"
    assert inc["classification"] == "positive_but_fold_unstable"


def test_annual_effort_control_keeps_detection_firewall():
    data = _result()
    assert "detection-sensitive" in data["analysis_status"]
    assert "detection-corrected true rewiring" in data["not_established"]
    ceiling = data["claim_ceiling"].lower()
    assert "focal-plant census effort alone" in ceiling
    assert "true ecological rewiring" in ceiling
    assert "routeability" in ceiling
