from __future__ import annotations

import math

import pytest

from adaptive_gain.ou_moving_optimum_congruence import (
    evots_covariance_formula,
    exogenous_observed_kernel,
    moving_optimum_covariance,
    moving_optimum_mean,
    reciprocal_observed_kernel,
    reciprocal_observed_mean,
    reciprocal_realization,
)


def test_covariance_matches_evots_literal_formula() -> None:
    alpha = 0.73
    v_trait = 0.17
    v_optimum = 0.09
    times = [0.0, 0.2, 0.9, 1.7, 4.3]

    for s in times:
        for t in times:
            assert moving_optimum_covariance(
                s, t, alpha, v_trait, v_optimum
            ) == pytest.approx(
                evots_covariance_formula(s, t, alpha, v_trait, v_optimum),
                rel=1e-12,
                abs=1e-12,
            )


@pytest.mark.parametrize("response_fraction", [0.1, 0.25, 0.5, 0.8, 0.95])
def test_reciprocal_family_preserves_drift_invariants(
    response_fraction: float,
) -> None:
    r = reciprocal_realization(
        alpha=0.8,
        v_trait=0.12,
        v_optimum=0.07,
        anc=1.4,
        theta0=-0.3,
        response_fraction=response_fraction,
    )

    assert r.drift_trace == pytest.approx(0.8)
    assert r.drift_determinant == pytest.approx(0.0, abs=1e-14)
    assert r.reciprocal_product > 0.0
    assert r.trait_response > 0.0
    assert r.latent_response > 0.0


@pytest.mark.parametrize("response_fraction", [0.1, 0.25, 0.5, 0.8, 0.95])
def test_reciprocal_family_has_exact_same_observed_noise_kernel(
    response_fraction: float,
) -> None:
    alpha = 0.8
    v_trait = 0.12
    v_optimum = 0.07
    r = reciprocal_realization(
        alpha=alpha,
        v_trait=v_trait,
        v_optimum=v_optimum,
        anc=1.4,
        theta0=-0.3,
        response_fraction=response_fraction,
    )

    for t in [0.0, 0.03, 0.2, 0.9, 2.1, 5.0]:
        assert reciprocal_observed_kernel(t, r) == pytest.approx(
            exogenous_observed_kernel(t, alpha, v_trait, v_optimum),
            rel=1e-12,
            abs=1e-12,
        )


@pytest.mark.parametrize("response_fraction", [0.1, 0.25, 0.5, 0.8, 0.95])
def test_reciprocal_family_has_exact_same_observed_mean(
    response_fraction: float,
) -> None:
    alpha = 0.8
    anc = 1.4
    theta0 = -0.3
    r = reciprocal_realization(
        alpha=alpha,
        v_trait=0.12,
        v_optimum=0.07,
        anc=anc,
        theta0=theta0,
        response_fraction=response_fraction,
    )

    for t in [0.0, 0.03, 0.2, 0.9, 2.1, 5.0]:
        assert reciprocal_observed_mean(t, r) == pytest.approx(
            moving_optimum_mean(t, anc, theta0, alpha),
            rel=1e-12,
            abs=1e-12,
        )


def test_symmetric_reciprocal_example_is_mutual_tracking() -> None:
    alpha = 1.2
    r = reciprocal_realization(
        alpha=alpha,
        v_trait=0.16,
        v_optimum=0.04,
        anc=0.7,
        theta0=1.1,
        response_fraction=0.5,
    )

    a = alpha / 2.0
    # A = [[a,-a],[-a,a]] means deterministic drift
    # dX/dt = a(Y-X), dY/dt = a(X-Y): reciprocal tracking.
    assert r.A == pytest.approx(((a, -a), (-a, a)))
    assert r.reciprocal_product == pytest.approx(a * a)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"alpha": 0.0, "v_trait": 0.1, "v_optimum": 0.1, "response_fraction": 0.5},
        {"alpha": 1.0, "v_trait": -0.1, "v_optimum": 0.1, "response_fraction": 0.5},
        {"alpha": 1.0, "v_trait": 0.1, "v_optimum": -0.1, "response_fraction": 0.5},
        {"alpha": 1.0, "v_trait": 0.1, "v_optimum": 0.1, "response_fraction": 0.0},
        {"alpha": 1.0, "v_trait": 0.1, "v_optimum": 0.1, "response_fraction": 1.0},
    ],
)
def test_invalid_realization_parameters_fail(kwargs: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        reciprocal_realization(anc=0.0, theta0=0.0, **kwargs)
