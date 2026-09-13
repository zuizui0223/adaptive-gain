import pytest

from adaptive_gain.nonlinear_feedback_reachability import (
    canonical_binary_lipschitz_no_go_receipt,
    maximum_feedback_gain_under_lipschitz_lift,
    minimum_integer_gap_for_oscillation_under_lipschitz_lift,
    oscillation_is_ruled_out_under_lipschitz_lift,
)


def test_linear_special_case_is_recovered_as_lipschitz_ceiling():
    # B=1/2 and L=1/4 reproduce the existing a=B*L=1/8 example.
    assert minimum_integer_gap_for_oscillation_under_lipschitz_lift(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        feedback_per_selection=0.5,
        max_selection_gain_per_gap=0.25,
    ) == 2
    assert maximum_feedback_gain_under_lipschitz_lift(
        1,
        feedback_per_selection=0.5,
        max_selection_gain_per_gap=0.25,
    ) == pytest.approx(0.125)


def test_strict_boundary_is_excluded_for_nonlinear_class():
    # alpha=1, phi=.2 gives G_osc=.2.  B=.4 and L=.25 give B*L=.1,
    # so gap=2 can reach at most the boundary and gap>=3 is necessary.
    assert minimum_integer_gap_for_oscillation_under_lipschitz_lift(
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


def test_crossing_necessary_bound_does_not_assert_sufficiency():
    # With the canonical geometry, a gap ceiling of 2 is no longer ruled out by
    # the Lipschitz theorem because its maximum permitted gain exceeds G_osc.
    # The function intentionally returns only whether oscillation is impossible.
    assert not oscillation_is_ruled_out_under_lipschitz_lift(
        2,
        evolutionary_persistence=1.0,
        community_memory=0.5,
        feedback_per_selection=0.5,
        max_selection_gain_per_gap=0.25,
    )


def test_canonical_binary_smaller_scopes_are_ruled_out_without_linear_lift():
    receipt = canonical_binary_lipschitz_no_go_receipt()
    assert receipt.theorem_holds
    assert receipt.linear_special_case_matches_existing_a
    assert receipt.effective_gain_ceiling_per_gap == pytest.approx(0.125)
    assert receipt.oscillation_gain == pytest.approx(0.125)
    assert receipt.necessary_integer_gap == 2
    assert receipt.binary_five_world_gap_ceiling == 1
    assert receipt.binary_four_query_gap_ceiling == 1
    assert receipt.binary_four_frontier_edge_gap_ceiling == 1
    assert receipt.five_world_scope_ruled_out
    assert receipt.four_query_scope_ruled_out
    assert receipt.four_frontier_edge_scope_ruled_out


def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError):
        maximum_feedback_gain_under_lipschitz_lift(
            -1,
            feedback_per_selection=1.0,
            max_selection_gain_per_gap=1.0,
        )
    with pytest.raises(ValueError):
        minimum_integer_gap_for_oscillation_under_lipschitz_lift(
            evolutionary_persistence=1.0,
            community_memory=0.5,
            feedback_per_selection=0.0,
            max_selection_gain_per_gap=1.0,
        )
    with pytest.raises(ValueError):
        minimum_integer_gap_for_oscillation_under_lipschitz_lift(
            evolutionary_persistence=1.0,
            community_memory=0.5,
            feedback_per_selection=1.0,
            max_selection_gain_per_gap=float("inf"),
        )
