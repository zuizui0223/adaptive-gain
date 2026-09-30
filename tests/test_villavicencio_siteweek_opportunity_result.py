import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "validation" / "villavicencio_siteweek_opportunity_audit_result_v1.json"


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_siteweek_primary_signal_is_green_for_both_endpoints():
    data = _result()
    assert data["status"] == "retrospective_spatiotemporal_robustness_green"
    primary = data["strict_core_2008_2011"]
    for risk in ("gain", "loss"):
        endpoint = primary[risk]
        assert endpoint["roc_auc"] > 0.5
        assert endpoint["relative_log_loss_reduction"] > 0
        assert endpoint["brier_improvement"] > 0
        assert endpoint["positive_log_loss_folds"] == "3/3"


def test_siteweek_binary_formation_contrast_is_preserved():
    data = _result()
    formation = data["strict_core_2008_2011"]["gain"]["binary_siteweek_opportunity"]
    assert formation["positive_event_rate"] > formation["zero_event_rate"]
    assert formation["rate_ratio"] > 4


def test_siteweek_broad_exception_is_2006_transition():
    data = _result()["sensitivities"]["all_annual_2006_2011"]
    assert data["gain_positive_folds"] == "4/5"
    assert data["loss_positive_folds"] == "4/5"
    assert data["exception"] == "2006->2007"


def test_siteweek_claim_ceiling_blocks_causal_routeability_promotion():
    data = _result()
    assert "post-result" in data["analysis_status"]
    ceiling = data["claim_ceiling"].lower()
    for phrase in ("causality", "sampling-effort independence", "strict forecasting", "decision equivalence", "routeability"):
        assert phrase in ceiling
