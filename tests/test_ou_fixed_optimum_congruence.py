from __future__ import annotations

import pytest

from adaptive_gain.adaptation_halflife_identifiability import (
    direct_trait_half_life,
    ou_half_life,
)
from adaptive_gain.ou_fixed_optimum_congruence import (
    fixed_optimum_covariance,
    fixed_optimum_mean,
    fixed_optimum_observed_kernel,
    fixed_optimum_variance,
    paleots_fixed_ou_covariance,
    reciprocal_fixed_optimum_realization,
)
from adaptive_gain.ou_moving_optimum_congruence import (
    moving_optimum_covariance,
    reciprocal_observed_kernel,
    reciprocal_observed_mean,
)


def test_fixed_covariance_matches_literal_paleots_joint_ou() -> None:
    alpha = 0.73
    vstep = 0.17
    times = [0.0, 0.2, 0.9, 1.7, 4.3]
    for s in times:
        for t in times:
            exact = fixed_optimum_covariance(s, t, alpha, vstep)
            assert exact == pytest.approx(
                paleots_fixed_ou_covariance(s, t, alpha, vstep),
                rel=1e-12,
                abs=1e-12,
            )
            assert exact == pytest.approx(
                moving_optimum_covariance(s, t, alpha, vstep, 0.0),
                rel=1e-12,
                abs=1e-12,
            )


def test_fixed_variance_is_covariance_diagonal() -> None:
    for t in [0.0, 0.1, 1.0, 5.0]:
        assert fixed_optimum_covariance(t, t, 0.8, 0.12) == pytest.approx(
            fixed_optimum_variance(t, 0.8, 0.12)
        )


@pytest.mark.parametrize("q", [0.1, 0.25, 0.5, 0.8, 0.95])
def test_reciprocal_fixed_ou_preserves_observed_mean_and_kernel(q: float) -> None:
    alpha = 0.8
    vstep = 0.12
    anc = 1.4
    theta = -0.3
    r = reciprocal_fixed_optimum_realization(
        alpha=alpha,
        vstep=vstep,
        anc=anc,
        theta=theta,
        response_fraction=q,
    )

    assert r.trait_response == pytest.approx(q * alpha)
    assert r.latent_response == pytest.approx((1.0 - q) * alpha)
    assert r.drift_trace == pytest.approx(alpha)
    assert r.drift_determinant == pytest.approx(0.0, abs=1e-14)
    assert r.reciprocal_product > 0.0
    assert r.S[1][1] == pytest.approx(0.0)

    for t in [0.0, 0.03, 0.2, 0.9, 2.1, 5.0]:
        assert reciprocal_observed_mean(t, r) == pytest.approx(
            fixed_optimum_mean(t, anc, theta, alpha),
            rel=1e-12,
            abs=1e-12,
        )
        assert reciprocal_observed_kernel(t, r) == pytest.approx(
            fixed_optimum_observed_kernel(t, alpha, vstep),
            rel=1e-12,
            abs=1e-12,
        )


def test_fixed_ou_semantic_boundary_observed_vs_direct_half_life() -> None:
    alpha = 0.8
    observed = ou_half_life(alpha)
    assert observed == pytest.approx(ou_half_life(alpha))

    for q in [0.8, 0.5, 0.25, 0.1]:
        direct = direct_trait_half_life(alpha, q)
        assert direct == pytest.approx(observed / q)
        assert direct > observed


def test_invalid_fixed_ou_arguments_fail() -> None:
    with pytest.raises(ValueError):
        fixed_optimum_variance(1.0, 0.0, 0.1)
    with pytest.raises(ValueError):
        fixed_optimum_variance(1.0, 1.0, -0.1)
    with pytest.raises(ValueError):
        paleots_fixed_ou_covariance(-1.0, 1.0, 1.0, 0.1)
