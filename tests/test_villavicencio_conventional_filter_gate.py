import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "villavicencio_conventional_filter_gate_v1.json"
RESULT = ROOT / "validation" / "villavicencio_annual_stage1_fallback_result_v1.json"


def test_conventional_filter_gate_is_effect_blind():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    assert data["status"] == "effect_blind_model_specification_frozen"
    timing = data["freeze_timing"]
    assert "response event counts" in timing["inspected_before_freeze"]
    assert "covariate-response correlations" in timing["not_inspected_before_freeze"]
    assert "model skill" in timing["not_inspected_before_freeze"]
    assert "decision-structure effects" in timing["not_inspected_before_freeze"]


def test_conventional_filter_gate_separates_gain_and_loss_risk_sets():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    gain = data["endpoints"]["gain"]
    loss = data["endpoints"]["loss"]
    assert (gain["n"], gain["events"], gain["nonevents"]) == (6632, 648, 5984)
    assert (loss["n"], loss["events"], loss["nonevents"]) == (988, 486, 502)
    assert data["endpoints"]["pooled_change"]["status"] == "descriptive_only"


def test_conventional_filter_gate_freezes_predictors_and_temporal_cv():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    names = [row["name"] for row in data["frozen_predictors"]]
    assert names == [
        "phenological_overlap",
        "flower_abundance",
        "corolla_length",
        "corolla_aperture",
        "height_mean",
        "body_length",
        "proboscis_length",
        "proboscis_width",
        "body_width",
        "body_thickness",
    ]
    model = data["model_family"]
    assert model["type"] == "separate binomial logistic models for gain and loss"
    assert "leave-one-transition-out" in model["transition_handling"]
    assert model["null_model"] == "training-fold event prevalence"
    assert model["primary_comparison"] == "conventional-filter model versus null on held-out transitions"


def test_conventional_filter_gate_freezes_complete_case_surface():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    completeness = data["completeness"]
    assert completeness["shared_dyad_rows"] == 7620
    assert completeness["complete_case_rows_all_frozen_predictors"] == 7186
    assert completeness["primary_missingness_policy"].startswith("complete case")
    assert completeness["no_response_dependent_imputation"] is True


def test_annual_result_keeps_claim_ceiling():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    assert data["status"] == "green_detection_sensitive_response_estimability"
    assert data["design"]["decision_equivalence_inferred"] is False
    assert data["design"]["primary_18_subseason_design_replaced"] is False
    assert data["interpretation"]["gate"] == "PASS for response estimability"
    assert "routeability" in data["claim_ceiling"]


def test_conventional_filter_claim_firewall():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    firewall = " ".join(data["claim_firewall"]).lower()
    assert "do not infer decision-equivalence classes" in firewall
    assert "do not tune predictor definitions" in firewall
    assert "do not promote annual fallback" in firewall
    assert "do not interpret predictive improvement as a causal effect" in firewall
