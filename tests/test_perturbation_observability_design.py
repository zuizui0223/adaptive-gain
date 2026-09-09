import math

import pytest

from adaptive_gain.perturbation_observability_design import (
    best_independent_candidate_design,
    best_observation_candidate,
    best_perturbation_candidate,
    brute_force_candidate_design,
    factorized_visibility,
    hankel_visibility,
    normalized_hankel_visibility,
    normalized_observation_visibility,
    normalized_perturbation_visibility,
    observation_visibility_factor,
    perturbation_visibility_factor,
    scalar_trajectory_first_three,
    summarize_visibility_design,
    symmetric_max_hankel_visibility,
    symmetric_max_single_side_visibility,
    symmetric_single_side_visibility,
)


def test_hankel_visibility_factorizes_exactly():
    cases = (
        (((0.9, 0.2), (-0.1, 0.5)), (1.0, -0.3), (0.2, 1.1)),
        (((0.8, 0.0), (0.0, 0.4)), (1.0, 1.0), (1.0, -2.0)),
        (((0.4, -0.6), (0.7, 0.2)), (-0.5, 0.9), (1.4, 0.3)),
    )
    for J, c, v in cases:
        assert hankel_visibility(J, c, v) == pytest.approx(
            factorized_visibility(J, c, v)
        )


def test_observation_blindness_can_kill_visibility_even_with_mixed_perturbation():
    J = ((0.9, 0.0), (0.0, 0.4))
    c = (1.0, 0.0)
    v = (1.0, 1.0)
    assert observation_visibility_factor(J, c) == pytest.approx(0.0)
    assert perturbation_visibility_factor(J, v) != pytest.approx(0.0)
    assert hankel_visibility(J, c, v) == pytest.approx(0.0)


def test_eigenmode_aligned_perturbation_kills_visibility():
    J = ((0.9, 0.0), (0.0, 0.4))
    c = (1.0, 1.0)
    v = (1.0, 0.0)
    assert observation_visibility_factor(J, c) != pytest.approx(0.0)
    assert perturbation_visibility_factor(J, v) == pytest.approx(0.0)
    assert hankel_visibility(J, c, v) == pytest.approx(0.0)


def test_equal_mode_mixture_is_optimal_for_symmetric_diagonal_system():
    r1, r2 = 0.9, 0.4
    x = 1.0 / math.sqrt(2.0)
    c = (x, x)
    v = (x, -x)
    J = ((r1, 0.0), (0.0, r2))

    side = abs(r1 - r2) / 2.0
    assert normalized_observation_visibility(J, c) == pytest.approx(side)
    assert normalized_perturbation_visibility(J, v) == pytest.approx(side)
    assert normalized_hankel_visibility(J, c, v) == pytest.approx(side * side)
    assert symmetric_max_single_side_visibility(r1, r2) == pytest.approx(side)
    assert symmetric_max_hankel_visibility(r1, r2) == pytest.approx(side * side)


def test_symmetric_single_side_formula_matches_direct_angles():
    r1, r2 = 0.8, -0.1
    J = ((r1, 0.0), (0.0, r2))
    for theta in (0.0, 0.2, 0.7, 1.1, math.pi / 4):
        c = (math.cos(theta), math.sin(theta))
        assert normalized_observation_visibility(J, c) == pytest.approx(
            symmetric_single_side_visibility(r1, r2, *c)
        )


def test_normalized_visibility_is_scale_invariant():
    J = ((0.7, 0.3), (-0.2, 0.5))
    c = (0.4, 1.2)
    v = (-0.9, 0.6)
    base = normalized_hankel_visibility(J, c, v)
    assert normalized_hankel_visibility(J, (4.0 * c[0], 4.0 * c[1]), v) == pytest.approx(base)
    assert normalized_hankel_visibility(J, c, (-3.0 * v[0], -3.0 * v[1])) == pytest.approx(base)


def test_summary_identifies_which_side_closes_the_gate():
    J = ((0.9, 0.0), (0.0, 0.4))

    observation_blind = summarize_visibility_design(J, (1.0, 0.0), (1.0, 1.0))
    assert not observation_blind.scalar_modes_visible
    assert not observation_blind.observation_side_visible
    assert observation_blind.perturbation_side_visible

    perturbation_blind = summarize_visibility_design(J, (1.0, 1.0), (1.0, 0.0))
    assert not perturbation_blind.scalar_modes_visible
    assert perturbation_blind.observation_side_visible
    assert not perturbation_blind.perturbation_side_visible

    visible = summarize_visibility_design(J, (1.0, 1.0), (1.0, -1.0))
    assert visible.scalar_modes_visible
    assert visible.observation_side_visible
    assert visible.perturbation_side_visible


def test_scalar_trajectory_matches_expected_diagonal_mixture():
    J = ((0.9, 0.0), (0.0, 0.4))
    c = (1.0, 1.0)
    v = (2.0, -1.0)
    x0, x1, x2 = scalar_trajectory_first_three(J, c, v)
    assert x0 == pytest.approx(1.0)
    assert x1 == pytest.approx(2.0 * 0.9 - 0.4)
    assert x2 == pytest.approx(2.0 * 0.9**2 - 0.4**2)


def test_repeated_eigenvalues_remove_symmetric_visibility():
    assert symmetric_max_single_side_visibility(0.5, 0.5) == pytest.approx(0.0)
    assert symmetric_max_hankel_visibility(0.5, 0.5) == pytest.approx(0.0)


def test_independent_candidate_design_factorizes_into_separate_argmaxes():
    J = ((0.9, 0.0), (0.0, 0.4))
    observations = ((1.0, 0.0), (1.0, 0.2), (1.0, 1.0))
    perturbations = ((1.0, 0.0), (1.0, 0.1), (1.0, -1.0))

    oi, os = best_observation_candidate(J, observations)
    pi, ps = best_perturbation_candidate(J, perturbations)
    separate = best_independent_candidate_design(J, observations, perturbations)
    brute = brute_force_candidate_design(J, observations, perturbations)

    assert separate.observation_index == oi
    assert separate.perturbation_index == pi
    assert separate.observation_score == pytest.approx(os)
    assert separate.perturbation_score == pytest.approx(ps)
    assert separate.joint_score == pytest.approx(os * ps)
    assert separate.joint_score == pytest.approx(brute.joint_score)
    assert separate.observation_index == brute.observation_index
    assert separate.perturbation_index == brute.perturbation_index


def test_candidate_selector_prefers_mixed_modes_over_blind_candidates():
    J = ((0.9, 0.0), (0.0, 0.4))
    observations = ((1.0, 0.0), (0.0, 1.0), (1.0, 1.0))
    perturbations = ((1.0, 0.0), (0.0, 1.0), (1.0, -1.0))
    best = best_independent_candidate_design(J, observations, perturbations)
    assert best.observation_index == 2
    assert best.perturbation_index == 2
    assert best.joint_score > 0.0


def test_candidate_selector_tie_breaks_to_smallest_index():
    J = ((0.9, 0.0), (0.0, 0.4))
    observations = ((1.0, 1.0), (-1.0, -1.0))
    perturbations = ((1.0, -1.0), (-1.0, 1.0))
    best = best_independent_candidate_design(J, observations, perturbations)
    assert best.observation_index == 0
    assert best.perturbation_index == 0


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        normalized_observation_visibility(((1.0, 0.0), (0.0, 1.0)), (0.0, 0.0))
    with pytest.raises(ValueError):
        normalized_perturbation_visibility(((1.0, 0.0), (0.0, 1.0)), (0.0, 0.0))
    with pytest.raises(ValueError):
        symmetric_single_side_visibility(1.0, 0.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        hankel_visibility(((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)), (1.0, 0.0), (1.0, 0.0))
    with pytest.raises(ValueError):
        best_observation_candidate(((1.0, 0.0), (0.0, 1.0)), ())
    with pytest.raises(ValueError):
        best_perturbation_candidate(((1.0, 0.0), (0.0, 1.0)), ())
