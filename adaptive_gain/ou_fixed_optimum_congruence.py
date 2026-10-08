"""Exact reciprocal-state corollary for the paleoTS fixed-optimum OU likelihood.

The joint fixed-optimum OU likelihood in ``paleoTS::logL.joint.OU`` uses

    E[X_t] = theta + (anc-theta) exp(-alpha t)

and, before sampling error is added,

    Cov(X_s, X_t)
      = exp(-alpha |t-s|) * min(V(s), V(t)),
    V(t) = vstep/(2 alpha) * (1-exp(-2 alpha t)).

This is exactly the ``v_optimum=0`` boundary of the moving-optimum observation
law already handled by ``ou_moving_optimum_congruence``.  Therefore the same
latent-coordinate transform yields a continuum of reciprocal two-state
realizations with an identical observed trait process.

Important semantic boundary: the conventional OU half-life log(2)/alpha remains
the relaxation half-life of the *observed mean*.  What is non-unique is the
one-way mechanistic attribution of alpha to the direct X<-latent attraction.
Inside the reciprocal family the direct attraction is a=q*alpha, so a direct
coupling half-life is log(2)/a = H_OU/q, while the observable relaxation rate is
still alpha=a+d.
"""

from __future__ import annotations

from math import exp, sqrt

from .ou_moving_optimum_congruence import (
    ReciprocalMovingOptimumRealization,
    reciprocal_realization,
)


def _positive(name: str, value: float) -> float:
    x = float(value)
    if x <= 0.0:
        raise ValueError(f"{name} must be positive")
    return x


def _nonnegative(name: str, value: float) -> float:
    x = float(value)
    if x < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return x


def fixed_optimum_mean(t: float, anc: float, theta: float, alpha: float) -> float:
    """Mean of the paleoTS joint fixed-optimum OU process."""

    rate = _positive("alpha", alpha)
    time = _nonnegative("t", t)
    return float(theta) + (float(anc) - float(theta)) * exp(-rate * time)


def fixed_optimum_variance(t: float, alpha: float, vstep: float) -> float:
    """Process variance V(t) used by paleoTS before sampling error."""

    rate = _positive("alpha", alpha)
    variance_rate = _nonnegative("vstep", vstep)
    time = _nonnegative("t", t)
    return variance_rate * (1.0 - exp(-2.0 * rate * time)) / (2.0 * rate)


def paleots_fixed_ou_covariance(
    s: float,
    t: float,
    alpha: float,
    vstep: float,
) -> float:
    """Literal covariance contract of ``paleoTS::logL.joint.OU``."""

    rate = _positive("alpha", alpha)
    s0 = _nonnegative("s", s)
    t0 = _nonnegative("t", t)
    vs = fixed_optimum_variance(s0, rate, vstep)
    vt = fixed_optimum_variance(t0, rate, vstep)
    return exp(-rate * abs(t0 - s0)) * min(vs, vt)


def fixed_optimum_covariance(
    s: float,
    t: float,
    alpha: float,
    vstep: float,
) -> float:
    """Equivalent closed form exposing the OUBM ``v_optimum=0`` boundary."""

    rate = _positive("alpha", alpha)
    variance_rate = _nonnegative("vstep", vstep)
    s0 = _nonnegative("s", s)
    t0 = _nonnegative("t", t)
    m = min(s0, t0)
    h = abs(t0 - s0)
    return variance_rate * (
        exp(-rate * h) - exp(-rate * (h + 2.0 * m))
    ) / (2.0 * rate)


def fixed_optimum_observed_kernel(
    t: float,
    alpha: float,
    vstep: float,
) -> tuple[float, float]:
    """Noise impulse-response vector after embedding the fixed optimum as dTheta=0."""

    rate = _positive("alpha", alpha)
    variance_rate = _nonnegative("vstep", vstep)
    time = _nonnegative("t", t)
    return sqrt(variance_rate) * exp(-rate * time), 0.0


def reciprocal_fixed_optimum_realization(
    *,
    alpha: float,
    vstep: float,
    anc: float,
    theta: float,
    response_fraction: float = 0.5,
) -> ReciprocalMovingOptimumRealization:
    """Construct an exact reciprocal realization of the paleoTS fixed-OU law."""

    return reciprocal_realization(
        alpha=alpha,
        v_trait=vstep,
        v_optimum=0.0,
        anc=anc,
        theta0=theta,
        response_fraction=response_fraction,
    )
