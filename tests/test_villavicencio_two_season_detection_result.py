import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_two_season_detection_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_detection_model_passes_five_of_six_gate_only():
    data = _result()
    primary = data["primary_scope"]
    assert data["status"] == (
        "latent_link_detection_identified_enough_for_sensitivity"
    )
    assert primary["identified_transition_count"] == 5
    assert primary["required_identified_transition_count"] == 5
    assert primary["promotion_to_latent_opportunity_model_allowed"] is True
    assert (
        primary["weak_or_nonidentified_transition"]["transition"]
        == "2009_early->2009_mid"
    )


def test_per_census_detection_is_low():
    data = _result()["detection_parameter_range"]
    assert data["p_previous_max"] < 0.2
    assert data["p_current_max"] < 0.2
    assert data["p_previous_min"] > 0.01
    assert data["p_current_min"] > 0.01


def test_observed_binary_changes_are_not_latent_truth():
    data = _result()["aggregate_descriptive"]
    assert data["candidate_surface_observed_binary_gain_count"] == 196
    assert data["candidate_surface_observed_binary_loss_count"] == 253
    assert data["sum_expected_latent_gain"] > 250
    assert data["sum_expected_latent_loss"] < 230
    assert (
        data["weighted_mean_posterior_true_gain_probability_among_observed_gains"]
        < 0.6
    )
    assert (
        data["weighted_mean_posterior_true_loss_probability_among_observed_losses"]
        < 0.5
    )


def test_detection_result_keeps_model_sensitivity_ceiling():
    data = _result()
    assert "true ecological rewiring as an observed fact" in data["not_established"]
    ceiling = data["claim_ceiling"].lower()
    assert "sensitivity" in ceiling
    assert "observed ecological rewiring" in ceiling
