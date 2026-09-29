import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "validation" / "villavicencio_subseason_effort_audit_result_v1.json"


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_effort_semantics_are_resolved_without_hiding_2010_discrepancy():
    data = _result()
    assert data["status"] == (
        "effort_semantics_resolved_binary_detection_materially_sensitive"
    )
    annual = data["effort_semantics"]["annual_raw_vs_published"]
    for year in ("2006", "2007", "2008", "2009", "2011"):
        assert annual[year]["difference"] == 0
    assert annual["2010"] == {"raw": 463, "published": 460, "difference": 3}


def test_subseason_detection_completeness_is_incomplete():
    data = _result()["trait_subset_detection_completeness"]
    assert data["minimum_observed_fraction"] < 0.32
    assert data["maximum_observed_fraction"] < 0.66


def test_effort_change_strongly_tracks_observed_gain_loss_direction():
    data = _result()["effort_alignment_with_observed_direction"]
    assert data["strict_dated_core_2008_2010_auc_gain_over_loss"] > 0.8
    assert data["core_sites_2008_2011_auc_gain_over_loss"] > 0.8
    assert data["all_2006_2011_auc_gain_over_loss"] > 0.8


def test_effort_only_models_have_material_heldout_skill():
    data = _result()["effort_only_heldout_cv"]["strict_dated_core_2008_2010"]
    assert data["gain"]["roc_auc"] > 0.65
    assert data["loss"]["roc_auc"] > 0.65
    assert data["gain"]["relative_log_loss_reduction"] > 0
    assert data["loss"]["relative_log_loss_reduction"] > 0


def test_matched_effort_rarefaction_does_not_support_raw_state_identity():
    data = _result()["matched_effort_rarefaction"]["strict_dated_core_2008_2010"]
    assert data["gain"]["mean_same_state_probability"] < 0.65
    assert data["loss"]["mean_same_state_probability"] < 0.65
    assert data["stable_present"]["mean_same_state_probability"] < 0.7


def test_effort_audit_claim_ceiling_uses_observed_turnover_language():
    data = _result()
    assert "observed-link turnover" in data["ecological_interpretation"]["consequence"]
    ceiling = data["claim_ceiling"].lower()
    assert "observed link-state turnover" in ceiling or "observed-link turnover" in ceiling
    assert "ecological rewiring" in ceiling
