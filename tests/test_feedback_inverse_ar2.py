import pytest

from adaptive_gain.feedback_inverse_diagnostics import (
    infer_feedback_from_ar2_coefficients,
    infer_feedback_from_eigenvalues,
)


def _coefficients(phi: float, loop_gain: float) -> tuple[float, float]:
    trace = 1.0 + phi
    determinant = phi + (1.0 - phi) * loop_gain
    return trace, -determinant


def test_repo_native_ar2_coefficients_recover_memory_and_loop_gain():
    # Repo-native damped example: phi=0.8, L=0.125.
    a1, a2 = _coefficients(0.8, 0.125)
    assert a1 == pytest.approx(1.8)
    assert a2 == pytest.approx(-0.825)
    inferred = infer_feedback_from_ar2_coefficients(a1, a2)
    assert inferred.community_memory == pytest.approx(0.8)
    assert inferred.loop_gain == pytest.approx(0.125)
    assert inferred.trace == pytest.approx(1.8)
    assert inferred.determinant == pytest.approx(0.825)
    assert inferred.reconstruction == "phenotype_logit_ar2"


def test_ar2_round_trip_across_feedback_parameter_grid():
    for phi in (0.0, 0.1, 0.5, 0.8, 0.95):
        for loop_gain in (-0.25, 0.0, 0.1, 0.5, 0.9, 1.25):
            a1, a2 = _coefficients(phi, loop_gain)
            inferred = infer_feedback_from_ar2_coefficients(a1, a2)
            assert inferred.community_memory == pytest.approx(phi, abs=2e-12)
            assert inferred.loop_gain == pytest.approx(loop_gain, abs=2e-12)


def test_ar2_and_eigenvalue_inversions_agree():
    phi = 0.6
    loop_gain = 0.4
    trace = 1.0 + phi
    determinant = phi + (1.0 - phi) * loop_gain
    discriminant = trace * trace - 4.0 * determinant
    root = complex(discriminant) ** 0.5
    eig1 = (trace + root) / 2.0
    eig2 = (trace - root) / 2.0

    from_ar2 = infer_feedback_from_ar2_coefficients(trace, -determinant)
    from_eigenvalues = infer_feedback_from_eigenvalues(eig1, eig2)
    assert from_ar2.community_memory == pytest.approx(from_eigenvalues.community_memory)
    assert from_ar2.loop_gain == pytest.approx(from_eigenvalues.loop_gain)


def test_ar2_inversion_does_not_require_damped_phase():
    # The trace/determinant inverse is a local algebraic diagnostic and also
    # works in nonoscillatory or unstable regimes when the model assumptions hold.
    nonosc = infer_feedback_from_ar2_coefficients(*_coefficients(0.2, 0.05))
    unstable = infer_feedback_from_ar2_coefficients(*_coefficients(0.5, 1.2))
    assert nonosc.community_memory == pytest.approx(0.2)
    assert nonosc.loop_gain == pytest.approx(0.05)
    assert unstable.community_memory == pytest.approx(0.5)
    assert unstable.loop_gain == pytest.approx(1.2)


def test_trace_implying_phi_one_is_not_identifiable_in_this_parameterization():
    with pytest.raises(ValueError):
        infer_feedback_from_ar2_coefficients(2.0, -1.0)


def test_negative_community_memory_is_outside_current_feedback_scope():
    # a1<1 implies phi<0, whereas the endogenous feedback branch explicitly
    # restricts community memory to 0<=phi<1.
    with pytest.raises(ValueError):
        infer_feedback_from_ar2_coefficients(0.9, -0.5)


def test_nonfinite_ar2_coefficients_raise():
    with pytest.raises(ValueError):
        infer_feedback_from_ar2_coefficients(float("nan"), -0.5)
    with pytest.raises(ValueError):
        infer_feedback_from_ar2_coefficients(1.5, float("inf"))
