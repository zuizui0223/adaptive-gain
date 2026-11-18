import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_current_opportunity_axis_audit_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_axis_audit_remains_explicitly_post_result():
    data = _result()
    assert "post-result" in data["analysis_status"]
    assert "hypothesis-generating" in data["analysis_status"]
    assert "not confirmatory" in data["analysis_status"]


def test_primary_gain_is_more_pollinator_activity_weighted():
    data = _result()["strict_core_2008_2011"]["gain"]
    plant = data["plant_availability_increment"]
    pollinator = data["pollinator_activity_increment"]
    contrast = data["axis_contrast"]

    assert plant["delta_log_loss"] > 0
    assert pollinator["delta_log_loss"] > plant["delta_log_loss"]
    assert plant["positive_folds"] == "3/3"
    assert pollinator["positive_folds"] == "3/3"
    assert contrast["pollinator_minus_plant"] > 0
    assert contrast["positive_folds"] == "3/3"


def test_primary_loss_is_more_plant_availability_weighted():
    data = _result()["strict_core_2008_2011"]["loss"]
    plant = data["plant_availability_increment"]
    pollinator = data["pollinator_activity_increment"]
    contrast = data["axis_contrast"]

    assert pollinator["delta_log_loss"] > 0
    assert plant["delta_log_loss"] > pollinator["delta_log_loss"]
    assert plant["positive_folds"] == "3/3"
    assert pollinator["positive_folds"] == "3/3"
    assert contrast["plant_minus_pollinator"] > 0
    assert contrast["positive_folds"] == "3/3"


def test_near_core_preserves_axis_direction_but_all_annual_records_exception():
    data = _result()
    near = data["near_core_2007_2011"]
    broad = data["all_annual_2006_2011"]

    assert near["gain"]["axis_direction_positive_folds"] == "4/4"
    assert near["loss"]["axis_direction_positive_folds"] == "4/4"
    assert broad["gain"]["axis_direction_positive_folds"] == "5/5"
    assert broad["loss"]["axis_direction_positive_folds"] == "4/5"
    assert broad["loss"]["exception"] == "2006->2007"
    assert "sampling-effort sensitivity" in broad["loss"]["exception_context"]


def test_axis_audit_claim_ceiling_blocks_causal_and_routeability_promotion():
    data = _result()
    ceiling = data["claim_ceiling"].lower()
    assert "causal" in ceiling
    assert "routeability" in ceiling
    assert "independent replication" in ceiling
