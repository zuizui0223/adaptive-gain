import pytest

from adaptive_gain.feedback_empirical_factorization import (
    evolutionary_response,
    infer_feedback_strength_from_loop_gain,
    infer_lambda_from_selection_and_structural_gap,
    infer_selection_contrast_from_loop_gain,
    reconstructed_loop_gain,
)


def test_repo_native_loop_gain_recovers_selection_contrast_without_lambda():
    # Parent repo-native centered witness: eta=-0.5, p*=0.5, Delta_s=1 -> L=0.125.
    result = infer_selection_contrast_from_loop_gain(
        0.125,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    )
    assert result.evolutionary_response == pytest.approx(0.25)
    assert result.inferred_selection_contrast == pytest.approx(1.0)


def test_selection_contrast_and_feedback_strength_inversions_are_reciprocal():
    for eta, contrast, p in (
        (-0.2, 0.5, 0.3),
        (-0.8, 1.7, 0.5),
        (-1.2, 0.3, 0.8),
    ):
        L = reconstructed_loop_gain(
            feedback_strength=eta,
            selection_contrast=contrast,
            equilibrium_frequency=p,
        )
        recovered_s = infer_selection_contrast_from_loop_gain(
            L,
            feedback_strength=eta,
            equilibrium_frequency=p,
        )
        recovered_eta = infer_feedback_strength_from_loop_gain(
            L,
            selection_contrast=contrast,
            equilibrium_frequency=p,
        )
        assert recovered_s.inferred_selection_contrast == pytest.approx(contrast)
        assert recovered_eta.inferred_feedback_strength == pytest.approx(eta)


def test_structural_gap_then_calibrates_lambda_downstream():
    # If natural-history finite-task reconstruction independently gives Delta_g=1,
    # the recovered Delta_s=1 calibrates lambda=1 rather than assuming it upstream.
    selection = infer_selection_contrast_from_loop_gain(
        0.125,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    ).inferred_selection_contrast
    scaling = infer_lambda_from_selection_and_structural_gap(selection, 1.0)
    assert scaling.inferred_lambda_cost == pytest.approx(1.0)


def test_lambda_calibration_exposes_inconsistent_structural_gap_scale():
    # Same measured selection contrast with a proposed gap 2 requires lambda=0.5.
    scaling = infer_lambda_from_selection_and_structural_gap(1.0, 2.0)
    assert scaling.inferred_lambda_cost == pytest.approx(0.5)


def test_response_is_maximal_at_intermediate_frequency():
    assert evolutionary_response(0.5) == pytest.approx(0.25)
    assert evolutionary_response(0.2) < evolutionary_response(0.5)
    assert evolutionary_response(0.8) == pytest.approx(evolutionary_response(0.2))


def test_invalid_empirical_factorizations_raise():
    with pytest.raises(ValueError):
        evolutionary_response(0.0)
    with pytest.raises(ValueError):
        infer_selection_contrast_from_loop_gain(
            0.1,
            feedback_strength=0.1,
            equilibrium_frequency=0.5,
        )
    with pytest.raises(ValueError):
        infer_feedback_strength_from_loop_gain(
            0.1,
            selection_contrast=0.0,
            equilibrium_frequency=0.5,
        )
    with pytest.raises(ValueError):
        infer_lambda_from_selection_and_structural_gap(1.0, 0.0)
