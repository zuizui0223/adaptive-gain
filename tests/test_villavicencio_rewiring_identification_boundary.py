import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_rewiring_identification_boundary_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_binary_rewiring_remains_unidentified_after_effort_semantics_resolve():
    data = _result()
    assert data["status"] == (
        "binary_rewiring_not_identified_effort_semantics_resolved"
    )
    assert data["sampling_effort"]["semantics"] == (
        "RESOLVED_RAW_5MIN_CENSUS_IDENTITY"
    )
    assert data["response_reconstruction"]["allowed_label"] == (
        "observed-link turnover"
    )
    assert "853 identified ecological rewiring events" in data[
        "response_reconstruction"
    ]["forbidden_label"]


def test_detection_sensitivity_is_material_not_hypothetical():
    data = _result()
    effort = data["binary_turnover_detection_diagnostics"][
        "effort_only_heldout_cv"
    ]["strict_dated_core_2008_2010"]
    assert effort["gain_auc"] > 0.65
    assert effort["loss_auc"] > 0.65

    rare = data["binary_turnover_detection_diagnostics"][
        "matched_effort_rarefaction"
    ]["strict_dated_core_2008_2010"]
    assert rare["gain_mean_original_state_retention"] < 0.65
    assert rare["loss_mean_original_state_retention"] < 0.65


def test_effort_standardized_ecological_increment_is_not_promoted():
    data = _result()["effort_standardized_response"]
    assert data["opportunity_log_loss_improvement"] > 0
    assert data["positive_folds"] == "4/6"
    assert data["classification"] == "not_reproducible_under_frozen_rule"


def test_identification_boundary_blocks_routeability_validation():
    data = _result()
    assert "sampling-effort-corrected ecological rewiring" in data[
        "current_claims"
    ]["not_established"]
    ceiling = data["claim_ceiling"].lower()
    assert "latent link state is not" in ceiling
    assert "not for identifying ecological rewiring" in ceiling
    assert "not be used as empirical validation of routeability" in ceiling
