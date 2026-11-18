import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_focal_excluded_opportunity_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_repaired_opportunity_surface_breaks_response_support_nesting():
    data = _result()
    support = data["support_repair"]
    assert data["response_integrity"][
        "raw_figshare_vs_stage1_response_mismatch_count"
    ] == 0
    assert support["opportunity_support_nested_in_ever_linked"] is False
    assert support["opportunity_positive_never_linked_count"] > 0
    assert 0 < support["probability_ever_linked_given_opportunity_positive"] < 1


def test_current_opportunity_has_primary_proper_score_skill():
    data = _result()
    primary = data["primary_scope"]
    for risk in ("gain", "loss"):
        current = primary[risk]["current_full"]
        assert current["relative_log_loss_reduction"] > 0
        assert current["brier_improvement"] > 0
        assert current["roc_auc"] > 0.5
        assert current["all_primary_folds_positive_log_loss_skill"] is True


def test_current_state_outperforms_one_year_lagged_control():
    data = _result()
    primary = data["primary_scope"]
    for risk in ("gain", "loss"):
        contrast = primary[risk]["current_minus_lagged"]
        assert contrast["relative_log_loss_skill_difference"] > 0
        assert contrast["auc_difference"] > 0
        assert contrast["current_better_log_loss_skill_folds"] == "3/3"

    assert primary["gain"]["lagged_full"]["roc_auc"] < 0.55
    assert primary["loss"]["lagged_full"]["relative_log_loss_reduction"] < 0


def test_pairwise_overlap_is_not_promoted_to_main_mechanism():
    data = _result()
    for risk in ("gain", "loss"):
        overlap = data["primary_scope"][risk][
            "current_pairwise_overlap_increment"
        ]
        assert overlap["delta_log_loss_drop_minus_full"] > 0
        assert overlap["positive_log_loss_folds"] == "3/3"
        assert "fold_unstable" in overlap["broader_sensitivity"]
        assert "small" in overlap["interpretation"].lower()


def test_supersession_and_claim_ceiling_are_explicit():
    data = _result()
    assert data["supersession"]["published_overlap_gain_filter_claim_valid"] is False
    ceiling = data["claim_ceiling"].lower()
    for forbidden in (
        "does not establish causality",
        "strict forecasting",
        "pair-specific matching",
        "decision equivalence",
        "routeability",
    ):
        assert forbidden in ceiling
