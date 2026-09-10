import pytest

from adaptive_gain.general_evolutionary_response import (
    damped_damping_time,
    general_response_jacobian,
    general_response_thresholds,
    generalized_loop_gain,
    generalized_structural_loop_gain,
    summarize_general_response,
    upper_boundary_critical_slowing_approximation,
)


def test_original_haploid_logit_model_is_exact_special_case():
    # Parent model: Delta_s=1, eta=-0.5, p*=0.5, phi=0.8.
    # In z=logit(p) coordinates, alpha=beta=1 and
    # e=dq_target/dz=eta*p*(1-p)=-0.125.
    summary = summarize_general_response(
        evolutionary_persistence=1.0,
        selection_responsiveness=1.0,
        selection_contrast=1.0,
        ecological_feedback_slope=-0.125,
        community_memory=0.8,
    )
    assert summary.loop_gain == pytest.approx(0.125)
    assert summary.trace == pytest.approx(1.8)
    assert summary.determinant == pytest.approx(0.825)
    assert summary.locally_stable
    assert summary.oscillatory
    assert summary.regime == "stable_damped_oscillation"

    thresholds = general_response_thresholds(1.0, 0.8)
    assert thresholds.lower_stability_gain == pytest.approx(0.0)
    assert thresholds.upper_stability_gain == pytest.approx(1.0)
    assert thresholds.oscillation_gain == pytest.approx(0.05)


def test_general_jacobian_matches_definition():
    J = general_response_jacobian(
        evolutionary_persistence=0.7,
        selection_responsiveness=0.4,
        selection_contrast=2.0,
        ecological_feedback_slope=-0.3,
        community_memory=0.6,
    )
    assert J[0] == pytest.approx((0.7, 0.8))
    assert J[1] == pytest.approx((-0.12, 0.6))


def test_intrinsic_evolutionary_damping_can_buffer_weak_positive_feedback():
    # e>0 gives G<0 (positive ecological feedback), but alpha<1 supplies
    # intrinsic damping.  Stability only fails once G reaches alpha-1.
    stable = summarize_general_response(
        evolutionary_persistence=0.7,
        selection_responsiveness=1.0,
        selection_contrast=1.0,
        ecological_feedback_slope=0.1,  # G=-0.1
        community_memory=0.5,
    )
    assert stable.loop_gain == pytest.approx(-0.1)
    assert general_response_thresholds(0.7, 0.5).lower_stability_gain == pytest.approx(-0.3)
    assert stable.locally_stable
    assert stable.regime == "stable_nonoscillatory"

    unstable = summarize_general_response(
        evolutionary_persistence=0.7,
        selection_responsiveness=1.0,
        selection_contrast=1.0,
        ecological_feedback_slope=0.4,  # G=-0.4 < alpha-1
        community_memory=0.5,
    )
    assert not unstable.locally_stable
    assert unstable.regime == "lower_boundary_or_nonrestoring_instability"


def test_restoring_gain_crosses_nonoscillatory_damped_and_upper_instability():
    alpha = 0.8
    phi = 0.5
    thresholds = general_response_thresholds(alpha, phi)
    assert thresholds.lower_stability_gain == pytest.approx(-0.2)
    assert thresholds.upper_stability_gain == pytest.approx(1.2)
    assert thresholds.oscillation_gain == pytest.approx(0.045)

    nonosc = summarize_general_response(
        evolutionary_persistence=alpha,
        selection_responsiveness=1.0,
        selection_contrast=1.0,
        ecological_feedback_slope=-0.02,  # G=.02
        community_memory=phi,
    )
    damped = summarize_general_response(
        evolutionary_persistence=alpha,
        selection_responsiveness=1.0,
        selection_contrast=1.0,
        ecological_feedback_slope=-0.5,  # G=.5
        community_memory=phi,
    )
    unstable = summarize_general_response(
        evolutionary_persistence=alpha,
        selection_responsiveness=1.0,
        selection_contrast=1.0,
        ecological_feedback_slope=-1.3,  # G=1.3 > upper
        community_memory=phi,
    )
    assert nonosc.regime == "stable_nonoscillatory"
    assert damped.regime == "stable_damped_oscillation"
    assert unstable.regime == "upper_oscillatory_instability"


def test_structural_gap_maps_into_generalized_gain():
    # Delta_s=lambda*Delta_g, then G=-beta*Delta_s*e.
    G = generalized_structural_loop_gain(
        3.0,
        lambda_cost=0.5,
        selection_responsiveness=0.4,
        ecological_feedback_slope=-0.25,
    )
    assert G == pytest.approx(0.15)


def test_upper_boundary_has_unit_circle_and_generalized_critical_period():
    alpha = 0.6
    phi = 0.7
    thresholds = general_response_thresholds(alpha, phi)
    G = thresholds.upper_stability_gain
    # At the upper boundary D=1 and trace=alpha+phi.
    summary = summarize_general_response(
        evolutionary_persistence=alpha,
        selection_responsiveness=1.0,
        selection_contrast=1.0,
        ecological_feedback_slope=-G,
        community_memory=phi,
    )
    assert summary.determinant == pytest.approx(1.0)
    assert max(abs(z) for z in summary.eigenvalues) == pytest.approx(1.0)
    assert thresholds.upper_boundary_period > 2.0


def test_generalized_critical_slowing_near_upper_boundary():
    alpha = 0.6
    phi = 0.8
    upper = general_response_thresholds(alpha, phi).upper_stability_gain
    for distance in (1e-2, 1e-3, 1e-4):
        G = upper - distance
        exact = damped_damping_time(
            G,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
        approx = upper_boundary_critical_slowing_approximation(
            G,
            evolutionary_persistence=alpha,
            community_memory=phi,
        )
        assert exact / approx == pytest.approx(1.0, rel=2e-2)


def test_generalized_loop_gain_sign_and_validation():
    assert generalized_loop_gain(
        selection_responsiveness=2.0,
        selection_contrast=0.5,
        ecological_feedback_slope=-0.3,
    ) == pytest.approx(0.3)
    assert generalized_loop_gain(
        selection_responsiveness=2.0,
        selection_contrast=0.5,
        ecological_feedback_slope=0.3,
    ) == pytest.approx(-0.3)

    with pytest.raises(ValueError):
        general_response_thresholds(1.1, 0.5)
    with pytest.raises(ValueError):
        generalized_loop_gain(
            selection_responsiveness=-1.0,
            selection_contrast=1.0,
            ecological_feedback_slope=-0.2,
        )
