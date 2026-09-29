import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "validation" / "villavicencio_census_rate_result_v1.json"


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_census_rate_response_is_effort_standardized_and_focal_excluded():
    data = _result()
    assert data["status"] == "effort_standardized_opportunity_increment_mixed"
    assert data["primary_scope"]["transition_count"] == 6
    assert data["primary_scope"]["dyad_census_trials"] == 24684
    assert data["candidate_surface"]["focal_response_excluded_from_candidate_surface"] is True
    assert data["candidate_surface"]["focal_response_excluded_from_opportunity"] is True


def test_census_rate_opportunity_increment_is_small_and_fold_mixed():
    data = _result()["opportunity_increment"]
    assert data["per_census_log_loss_improvement"] > 0
    assert data["trial_weighted_brier_improvement"] > 0
    assert data["positive_log_loss_folds"] == "4/6"
    assert data["classification"] == "not_reproducible_under_frozen_rule"
    values = list(data["fold_log_loss_improvement"].values())
    assert sum(value > 0 for value in values) == 4
    assert sum(value < 0 for value in values) == 2


def test_census_rate_result_blocks_rewiring_promotion():
    data = _result()
    assert "ecological rewiring" in data["not_established"]
    assert "not reproducibly positive" in data["ecological_read"]["not_supported"]
    ceiling = data["claim_ceiling"].lower()
    assert "fold-mixed" in ceiling
    assert "rewiring" in ceiling
    assert "routeability" in ceiling
