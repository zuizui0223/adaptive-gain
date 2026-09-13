import json
from pathlib import Path

import pytest

from adaptive_gain.nonlinear_feedback_reachability import (
    canonical_binary_lipschitz_no_go_receipt,
    maximum_feedback_gain_under_lipschitz_lift,
    minimum_integer_gap_contrast_for_oscillation_under_lipschitz_lift,
    minimum_integer_gap_for_oscillation_under_lipschitz_lift,
    oscillation_is_ruled_out_under_lipschitz_lift,
)


RECEIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "validation"
    / "nonlinear_lipschitz_no_go_v2.json"
)


def test_linear_special_case_is_recovered_as_lipschitz_ceiling():
    # B=1/2 and L=1/4 reproduce the existing a=B*L=1/8 example.
    kwargs = dict(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        feedback_per_selection=0.5,
        max_selection_gain_per_gap=0.25,
    )
    assert minimum_integer_gap_contrast_for_oscillation_under_lipschitz_lift(
        **kwargs
    ) == 2
    # Backward-compatible function now explicitly returns the same contrast.
    assert minimum_integer_gap_for_oscillation_under_lipschitz_lift(**kwargs) == 2
    assert maximum_feedback_gain_under_lipschitz_lift(
        1,
        feedback_per_selection=0.5,
        max_selection_gain_per_gap=0.25,
    ) == pytest.approx(0.125)


def test_strict_boundary_is_excluded_for_between_state_contrast():
    # alpha=1, phi=.2 gives G_osc=.2. B=.4 and L=.25 give B*L=.1,
    # so contrast 2 reaches at most the boundary and contrast >=3 is necessary.
    assert minimum_integer_gap_contrast_for_oscillation_under_lipschitz_lift(
        evolutionary_persistence=1.0,
        community_memory=0.2,
        feedback_per_selection=0.4,
        max_selection_gain_per_gap=0.25,
    ) == 3
    assert oscillation_is_ruled_out_under_lipschitz_lift(
        2,
        evolutionary_persistence=1.0,
        community_memory=0.2,
        feedback_per_selection=0.4,
        max_selection_gain_per_gap=0.25,
    )


def test_crossing_necessary_contrast_bound_does_not_assert_sufficiency():
    assert not oscillation_is_ruled_out_under_lipschitz_lift(
        2,
        evolutionary_persistence=1.0,
        community_memory=0.5,
        feedback_per_selection=0.5,
        max_selection_gain_per_gap=0.25,
    )


def test_canonical_binary_smaller_scopes_bound_every_state_and_the_contrast():
    receipt = canonical_binary_lipschitz_no_go_receipt()
    assert receipt.theorem_holds
    assert receipt.linear_special_case_matches_existing_a
    assert receipt.effective_gain_ceiling_per_gap_contrast == pytest.approx(0.125)
    assert receipt.oscillation_gain == pytest.approx(0.125)
    assert receipt.necessary_integer_gap_contrast == 2

    assert receipt.binary_five_world_state_gap_ceiling == 1
    assert receipt.binary_four_query_state_gap_ceiling == 1
    assert receipt.binary_four_frontier_edge_state_gap_ceiling == 1
    assert receipt.binary_five_world_contrast_ceiling == 1
    assert receipt.binary_four_query_contrast_ceiling == 1
    assert receipt.binary_four_frontier_edge_contrast_ceiling == 1

    assert receipt.five_world_scope_ruled_out
    assert receipt.four_query_scope_ruled_out
    assert receipt.four_frontier_edge_scope_ruled_out
    assert receipt.constructive_low_state_gap == 0
    assert receipt.constructive_high_state_gap == 2


def test_machine_readable_receipt_matches_executable_theorem():
    stored = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    receipt = canonical_binary_lipschitz_no_go_receipt()

    assert stored["status"] == "validated_theorem_receipt"
    assert stored["theorem"]["sufficiency_claimed"] is False
    assert stored["theorem"]["state_gap"] == "g_i=C_F(i)-C_A(i)>=0"
    assert stored["theorem"]["between_state_contrast"] == "Delta_g=g_high-g_low>=0"

    geometry = stored["canonical_geometry"]
    assert geometry["alpha"] == receipt.evolutionary_persistence
    assert geometry["phi"] == receipt.community_memory
    assert geometry["G_osc"] == pytest.approx(receipt.oscillation_gain)
    assert geometry["feedback_per_selection_B"] == receipt.feedback_per_selection
    assert geometry["max_selection_gain_per_gap_L"] == receipt.max_selection_gain_per_gap
    assert geometry["B_times_L"] == pytest.approx(
        receipt.effective_gain_ceiling_per_gap_contrast
    )
    assert geometry["necessary_integer_gap_contrast"] == (
        receipt.necessary_integer_gap_contrast
    )

    exclusions = stored["binary_extremal_exclusions"]
    assert exclusions["world_count_at_most_5"]["state_gap_ceiling"] == (
        receipt.binary_five_world_state_gap_ceiling
    )
    assert exclusions["world_count_at_most_5"]["contrast_ceiling"] == (
        receipt.binary_five_world_contrast_ceiling
    )
    assert exclusions["query_count_at_most_4"]["state_gap_ceiling"] == (
        receipt.binary_four_query_state_gap_ceiling
    )
    assert exclusions["productive_frontier_edges_at_most_4"]["state_gap_ceiling"] == (
        receipt.binary_four_frontier_edge_state_gap_ceiling
    )
    assert exclusions["world_count_at_most_5"]["oscillation_ruled_out"]
    assert exclusions["query_count_at_most_4"]["oscillation_ruled_out"]
    assert exclusions["productive_frontier_edges_at_most_4"][
        "oscillation_ruled_out"
    ]

    constructive = stored["linear_special_case"]
    assert constructive["low_state_gap"] == receipt.constructive_low_state_gap
    assert constructive["high_state_gap"] == receipt.constructive_high_state_gap
    assert constructive["between_state_contrast"] == 2


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        maximum_feedback_gain_under_lipschitz_lift(
            -1,
            feedback_per_selection=1.0,
            max_selection_gain_per_gap=1.0,
        )
    with pytest.raises(ValueError):
        minimum_integer_gap_contrast_for_oscillation_under_lipschitz_lift(
            evolutionary_persistence=1.0,
            community_memory=0.5,
            feedback_per_selection=0.0,
            max_selection_gain_per_gap=1.0,
        )
    with pytest.raises(ValueError):
        minimum_integer_gap_contrast_for_oscillation_under_lipschitz_lift(
            evolutionary_persistence=1.0,
            community_memory=0.5,
            feedback_per_selection=1.0,
            max_selection_gain_per_gap=float("inf"),
        )
