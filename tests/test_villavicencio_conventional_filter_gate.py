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
    assert model["primary_scope"] == "strict_core_2008_2011"
    scopes = model["transition_scopes"]
    assert scopes["strict_core_2008_2011"]["transitions"] == [
        "2008->2009",
        "2009->2010",
        "2010->2011",
    ]
    assert scopes["near_core_2007_2011"]["role"] == "sampling-effort sensitivity"
    assert scopes["all_annual_2006_2011"]["role"] == "broad sensitivity"
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


def test_sampling_effort_audit_controls_annual_scope():
    path = ROOT / "validation" / "villavicencio_sampling_effort_audit_v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    consequence = data["consequence"]
    assert data["status"] == "external_methods_frozen_before_formal_filter_cv_result"
    assert consequence["primary_filter_cv_scope"]["name"] == "strict_core_2008_2011"
    assert consequence["primary_filter_cv_scope"]["transitions"] == [
        "2008->2009",
        "2009->2010",
        "2010->2011",
    ]
    assert "two additional" in data["documented_sampling"]["extra_sites_2006"]
    assert data["freeze_boundary"]["formal_cv_result_seen_before_scope_freeze"] is False


def test_conventional_filter_gate_blocks_interaction_derived_matching_leakage():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    policy = data["anti_leakage"]
    assert "independently measured raw morphology" in policy["policy"]
    assert "do not import interaction-derived trait-matching scores" in policy["policy"]
    assert "circular" in policy["reason"]
