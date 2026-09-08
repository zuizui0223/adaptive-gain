import pytest

from adaptive_gain.feedback_inverse_sensitivity import (
    ar2_finite_error_bound,
    ar2_inverse_sensitivity,
    exact_ar2_perturbation,
    structural_gap_error_bound,
)


def test_first_order_sensitivity_has_expected_memory_singularity():
    low_memory = ar2_inverse_sensitivity(0.2, 0.4)
    high_memory = ar2_inverse_sensitivity(0.9, 0.4)
    assert low_memory.d_phi_d_a1 == pytest.approx(1.0)
    assert low_memory.d_phi_d_a2 == pytest.approx(0.0)
    assert low_memory.d_L_d_a2 == pytest.approx(-1.25)
    assert high_memory.d_L_d_a2 == pytest.approx(-10.0)
    assert abs(high_memory.d_L_d_a1) > abs(low_memory.d_L_d_a1)


def test_exact_perturbation_identity_matches_direct_ar2_reinversion():
    phi = 0.8
    L = 0.125
    e1 = 0.002
    e2 = -0.003
    delta_phi, delta_L = exact_ar2_perturbation(
        phi,
        L,
        lag1_error=e1,
        lag2_error=e2,
    )

    a1 = 1.0 + phi
    determinant = phi + (1.0 - phi) * L
    a2 = -determinant
    phi_hat = (a1 + e1) - 1.0
    L_hat = (-(a2 + e2) - phi_hat) / (1.0 - phi_hat)

    assert delta_phi == pytest.approx(phi_hat - phi)
    assert delta_L == pytest.approx(L_hat - L)


def test_finite_error_bound_contains_all_corner_perturbations():
    phi = 0.8
    L = 0.125
    E1 = 0.01
    E2 = 0.02
    bound = ar2_finite_error_bound(
        phi,
        L,
        lag1_error_bound=E1,
        lag2_error_bound=E2,
    )
    assert bound.community_memory_error_bound == pytest.approx(E1)
    assert bound.loop_gain_error_bound == pytest.approx(
        (abs(1.0 - L) * E1 + E2) / (1.0 - phi - E1)
    )

    for e1 in (-E1, E1):
        for e2 in (-E2, E2):
            delta_phi, delta_L = exact_ar2_perturbation(
                phi,
                L,
                lag1_error=e1,
                lag2_error=e2,
            )
            assert abs(delta_phi) <= bound.community_memory_error_bound + 1e-15
            assert abs(delta_L) <= bound.loop_gain_error_bound + 1e-15


def test_same_coefficient_errors_are_amplified_by_high_memory():
    low = ar2_finite_error_bound(
        0.2,
        0.5,
        lag1_error_bound=0.005,
        lag2_error_bound=0.005,
    )
    high = ar2_finite_error_bound(
        0.95,
        0.5,
        lag1_error_bound=0.005,
        lag2_error_bound=0.005,
    )
    assert high.loop_gain_error_bound > 10.0 * low.loop_gain_error_bound


def test_loop_gain_uncertainty_propagates_to_structural_gap():
    # Repo-native scale is (-eta)*lambda*p*(1-p)=1/8.
    gap_error = structural_gap_error_bound(
        0.01,
        lambda_cost=1.0,
        feedback_strength=-0.5,
        equilibrium_frequency=0.5,
    )
    assert gap_error == pytest.approx(0.08)


def test_error_bound_rejects_crossing_phi_one_singularity():
    with pytest.raises(ValueError):
        ar2_finite_error_bound(
            0.99,
            0.5,
            lag1_error_bound=0.02,
            lag2_error_bound=0.001,
        )
    with pytest.raises(ValueError):
        exact_ar2_perturbation(
            0.99,
            0.5,
            lag1_error=0.02,
            lag2_error=0.0,
        )


def test_invalid_structural_scaling_raises():
    with pytest.raises(ValueError):
        structural_gap_error_bound(
            0.01,
            lambda_cost=1.0,
            feedback_strength=0.1,
            equilibrium_frequency=0.5,
        )
