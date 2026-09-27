import pytest

from adaptive_gain.routeability_experiment_power import (
    RouteabilityPilotNuisance,
    RouteabilitySESoi,
    conservative_routeability_planning_receipt,
    pilot_nuisance_from_procedural_receipt,
)


def _nuisance():
    return RouteabilityPilotNuisance(
        trial_icc=0.20,
        randomized_individual_dropout=0.10,
        full_information_success=0.90,
        timeout_fraction=0.05,
        source="architecture_neutral_procedural_pilot",
    )


def _sesoi():
    return RouteabilitySESoi(
        h1_probability_interaction=0.15,
        h2_probability_localization=0.15,
        provenance="external_biological_criterion",
    )


def test_planning_receipt_uses_external_sesoi_and_counterbalance_rounding():
    receipt = conservative_routeability_planning_receipt(
        _nuisance(),
        _sesoi(),
        trials_per_individual=12,
    )

    assert receipt.h2_complete_individuals_per_cell >= receipt.h1_complete_individuals_per_cell
    assert receipt.required_complete_individuals_per_cell == receipt.h2_complete_individuals_per_cell
    assert receipt.randomized_individuals_per_cell >= receipt.required_complete_individuals_per_cell
    assert receipt.randomized_individuals_per_cell % 4 == 0
    assert receipt.randomized_total_individuals == 12 * receipt.randomized_individuals_per_cell
    assert receipt.repeated_trial_design_effect == pytest.approx(3.2)
    assert "final GLMM simulation still required" in receipt.method


def test_more_trial_correlation_never_reduces_required_complete_n():
    low = conservative_routeability_planning_receipt(
        RouteabilityPilotNuisance(
            trial_icc=0.05,
            randomized_individual_dropout=0.0,
            full_information_success=0.9,
            timeout_fraction=0.02,
            source="architecture_neutral_procedural_pilot",
        ),
        _sesoi(),
        trials_per_individual=12,
    )
    high = conservative_routeability_planning_receipt(
        RouteabilityPilotNuisance(
            trial_icc=0.40,
            randomized_individual_dropout=0.0,
            full_information_success=0.9,
            timeout_fraction=0.02,
            source="architecture_neutral_procedural_pilot",
        ),
        _sesoi(),
        trials_per_individual=12,
    )
    assert high.required_complete_individuals_per_cell >= low.required_complete_individuals_per_cell


def test_dropout_inflates_randomized_not_complete_target():
    no_dropout = conservative_routeability_planning_receipt(
        RouteabilityPilotNuisance(
            trial_icc=0.2,
            randomized_individual_dropout=0.0,
            full_information_success=0.9,
            timeout_fraction=0.05,
            source="architecture_neutral_procedural_pilot",
        ),
        _sesoi(),
        trials_per_individual=12,
    )
    dropout = conservative_routeability_planning_receipt(
        _nuisance(),
        _sesoi(),
        trials_per_individual=12,
    )
    assert dropout.required_complete_individuals_per_cell == no_dropout.required_complete_individuals_per_cell
    assert dropout.randomized_individuals_per_cell >= no_dropout.randomized_individuals_per_cell


@pytest.mark.parametrize(
    "provenance",
    [
        "theoretical_information_ceiling",
        "focal_confirmatory_pilot",
        "posthoc_observed_interaction",
    ],
)
def test_forbidden_effect_provenance_is_rejected(provenance):
    sesoi = RouteabilitySESoi(
        h1_probability_interaction=0.15,
        h2_probability_localization=0.15,
        provenance=provenance,
    )
    with pytest.raises(ValueError):
        conservative_routeability_planning_receipt(
            _nuisance(), sesoi, trials_per_individual=12
        )


def test_opened_focal_pilot_is_rejected_as_nuisance_source():
    nuisance = RouteabilityPilotNuisance(
        trial_icc=0.2,
        randomized_individual_dropout=0.1,
        full_information_success=0.9,
        timeout_fraction=0.05,
        source="pilot_after_unblinding",
        focal_architecture_access_contrast_opened=True,
    )
    with pytest.raises(ValueError):
        conservative_routeability_planning_receipt(
            nuisance, _sesoi(), trials_per_individual=12
        )


def test_smaller_external_sesoi_requires_more_individuals():
    large = conservative_routeability_planning_receipt(
        _nuisance(),
        RouteabilitySESoi(0.20, 0.20, "practical_decision_threshold"),
        trials_per_individual=12,
    )
    small = conservative_routeability_planning_receipt(
        _nuisance(),
        RouteabilitySESoi(0.10, 0.10, "practical_decision_threshold"),
        trials_per_individual=12,
    )
    assert small.required_complete_individuals_per_cell > large.required_complete_individuals_per_cell


def test_power_nuisance_can_be_built_directly_from_frozen_procedural_receipt():
    receipt = {
        "focal_architecture_contrast_opened": False,
        "trial_icc_moment": 0.2,
        "randomized_individual_dropout_fraction": 0.1,
        "pooled_success_fraction": 0.9,
        "pooled_timeout_fraction": 0.05,
    }
    nuisance = pilot_nuisance_from_procedural_receipt(receipt)

    assert nuisance.trial_icc == 0.2
    assert nuisance.randomized_individual_dropout == 0.1
    assert nuisance.full_information_success == 0.9
    assert nuisance.timeout_fraction == 0.05
    assert nuisance.focal_architecture_access_contrast_opened is False


def test_power_nuisance_bridge_rejects_missing_icc_or_opened_focal_contrast():
    incomplete = {
        "focal_architecture_contrast_opened": False,
        "trial_icc_moment": None,
        "randomized_individual_dropout_fraction": 0.1,
        "pooled_success_fraction": 0.9,
        "pooled_timeout_fraction": 0.05,
    }
    with pytest.raises(ValueError, match="trial_icc_moment"):
        pilot_nuisance_from_procedural_receipt(incomplete)

    opened = {
        "focal_architecture_contrast_opened": True,
        "trial_icc_moment": 0.2,
        "randomized_individual_dropout_fraction": 0.1,
        "pooled_success_fraction": 0.9,
        "pooled_timeout_fraction": 0.05,
    }
    with pytest.raises(ValueError, match="must certify"):
        pilot_nuisance_from_procedural_receipt(opened)
