"""Exact observation-law congruence for the evoTS moving-optimum OU model.

The evoTS OUBM model can be written as

    dX = alpha (Theta - X) dt + sqrt(v_trait) dW1
    dTheta = sqrt(v_opt) dW2,

with deterministic initial state ``(X0, Theta0) = (anc, theta0)``.
Only ``X`` is observed.

This module constructs a continuum of reciprocal two-state systems with the
*same observed X process*.  For any 0 < q < 1, let

    a = q * alpha
    d = (1-q) * alpha

and define

    dX = a (Y - X) dt + sqrt(v_trait) dW1
    dY = d (X - Y) dt
         - (d/a) sqrt(v_trait) dW1
         + (alpha/a) sqrt(v_opt) dW2.

The latent initial condition is chosen so that the deterministic mean of X
matches the evoTS model exactly.  The first-row stochastic convolution kernel
is also identical, hence the complete finite-dimensional Gaussian law of X is
identical for arbitrary observation times.  Adding the same independent
sampling-error variances therefore leaves the evoTS multivariate-normal
likelihood unchanged.

The result is a mechanistic-attribution statement, not a claim that generic OU
non-identifiability is new.  It targets the specific exogenous-moving-optimum
interpretation used by evoTS.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, sqrt


def _require_nonnegative(name: str, value: float) -> float:
    x = float(value)
    if x < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return x


def _require_positive(name: str, value: float) -> float:
    x = float(value)
    if x <= 0.0:
        raise ValueError(f"{name} must be positive")
    return x


def moving_optimum_mean(t: float, anc: float, theta0: float, alpha: float) -> float:
    """Mean used by evoTS ``ou.M`` for the moving-optimum OU model."""

    rate = _require_positive("alpha", alpha)
    time = _require_nonnegative("t", t)
    return float(theta0) + (float(anc) - float(theta0)) * exp(-rate * time)


def moving_optimum_covariance(
    s: float,
    t: float,
    alpha: float,
    v_trait: float,
    v_optimum: float,
) -> float:
    """Process covariance of the evoTS OUBM latent trait means.

    This is algebraically the same covariance used in
    ``evoTS::logL.joint.OU.BM`` before sampling-error variances are added to the
    diagonal.  The expression below is written without division by ``min(s,t)``
    so the time-zero case is explicit and numerically safe.
    """

    rate = _require_positive("alpha", alpha)
    vt = _require_nonnegative("v_trait", v_trait)
    vo = _require_nonnegative("v_optimum", v_optimum)
    s0 = _require_nonnegative("s", s)
    t0 = _require_nonnegative("t", t)

    m = min(s0, t0)
    if m == 0.0:
        return 0.0
    h = abs(s0 - t0)
    eh = exp(-rate * h)
    em = exp(-rate * m)
    e2m_h = exp(-rate * (h + 2.0 * m))

    trait = vt * (eh - e2m_h) / (2.0 * rate)
    optimum = vo * (
        m
        - (1.0 + eh) * (1.0 - em) / rate
        + (eh - e2m_h) / (2.0 * rate)
    )
    return trait + optimum


def evots_covariance_formula(
    s: float,
    t: float,
    alpha: float,
    v_trait: float,
    v_optimum: float,
) -> float:
    """Literal algebraic form used in evoTS ``logL.joint.OU.BM``.

    This helper exists only to regression-test the simplified covariance above.
    """

    rate = _require_positive("alpha", alpha)
    vt = _require_nonnegative("v_trait", v_trait)
    vo = _require_nonnegative("v_optimum", v_optimum)
    s0 = _require_nonnegative("s", s)
    t0 = _require_nonnegative("t", t)
    m = min(s0, t0)
    if m == 0.0:
        return 0.0
    h = abs(s0 - t0)
    eh = exp(-rate * h)
    return (
        ((vo + vt) / (2.0 * rate))
        * (1.0 - exp(-2.0 * rate * m))
        * eh
        + vo
        * m
        * (
            1.0
            - (1.0 + eh) * (1.0 - exp(-rate * m)) / (rate * m)
        )
    )


@dataclass(frozen=True)
class ReciprocalMovingOptimumRealization:
    """A reciprocal latent-state realization congruent with evoTS OUBM."""

    alpha: float
    trait_response: float
    latent_response: float
    v_trait: float
    v_optimum: float
    anc: float
    theta0: float
    hidden_initial: float
    A: tuple[tuple[float, float], tuple[float, float]]
    S: tuple[tuple[float, float], tuple[float, float]]

    @property
    def drift_trace(self) -> float:
        return self.A[0][0] + self.A[1][1]

    @property
    def drift_determinant(self) -> float:
        return self.A[0][0] * self.A[1][1] - self.A[0][1] * self.A[1][0]

    @property
    def reciprocal_product(self) -> float:
        return self.A[0][1] * self.A[1][0]


def reciprocal_realization(
    *,
    alpha: float,
    v_trait: float,
    v_optimum: float,
    anc: float,
    theta0: float,
    response_fraction: float = 0.5,
) -> ReciprocalMovingOptimumRealization:
    """Construct an exact reciprocal realization of an evoTS OUBM law.

    ``response_fraction=q`` partitions the evoTS apparent return rate ``alpha``
    into a direct trait response ``a=q*alpha`` and a reciprocal latent response
    ``d=(1-q)*alpha``.  Every ``q`` strictly between zero and one gives a
    distinct system with non-zero two-way coupling but the same observed trait
    process.
    """

    rate = _require_positive("alpha", alpha)
    vt = _require_nonnegative("v_trait", v_trait)
    vo = _require_nonnegative("v_optimum", v_optimum)
    q = float(response_fraction)
    if not 0.0 < q < 1.0:
        raise ValueError("response_fraction must lie strictly between 0 and 1")

    a = q * rate
    d = (1.0 - q) * rate
    sx = sqrt(vt)
    so = sqrt(vo)

    # Tracking-form drift:
    #   dX = a(Y-X)dt + ...
    #   dY = d(X-Y)dt + ...
    A = ((a, -a), (-d, d))

    # This diffusion makes the first-coordinate impulse-response vector exactly
    # [sqrt(v_trait)e^{-alpha t}, sqrt(v_optimum)(1-e^{-alpha t})].
    S = ((sx, 0.0), (-(d / a) * sx, (rate / a) * so))

    # For A^2 = alpha A, the deterministic trajectory converges along the
    # neutral common mode.  Choose Y0 so the observed X mean converges to theta0.
    hidden_initial = (rate * float(theta0) - d * float(anc)) / a

    return ReciprocalMovingOptimumRealization(
        alpha=rate,
        trait_response=a,
        latent_response=d,
        v_trait=vt,
        v_optimum=vo,
        anc=float(anc),
        theta0=float(theta0),
        hidden_initial=hidden_initial,
        A=A,
        S=S,
    )


def reciprocal_observed_mean(
    t: float, realization: ReciprocalMovingOptimumRealization
) -> float:
    """Observed X mean under the reciprocal realization."""

    time = _require_nonnegative("t", t)
    rate = realization.alpha
    a = realization.trait_response
    qtime = (1.0 - exp(-rate * time)) / rate
    row0 = (1.0 - a * qtime, a * qtime)
    return row0[0] * realization.anc + row0[1] * realization.hidden_initial


def exogenous_observed_kernel(
    t: float, alpha: float, v_trait: float, v_optimum: float
) -> tuple[float, float]:
    """Noise impulse-response vector for the evoTS exogenous OUBM model."""

    rate = _require_positive("alpha", alpha)
    vt = _require_nonnegative("v_trait", v_trait)
    vo = _require_nonnegative("v_optimum", v_optimum)
    time = _require_nonnegative("t", t)
    decay = exp(-rate * time)
    return sqrt(vt) * decay, sqrt(vo) * (1.0 - decay)


def reciprocal_observed_kernel(
    t: float, realization: ReciprocalMovingOptimumRealization
) -> tuple[float, float]:
    """Noise impulse-response vector for X under the reciprocal realization."""

    time = _require_nonnegative("t", t)
    rate = realization.alpha
    a = realization.trait_response
    qtime = (1.0 - exp(-rate * time)) / rate

    # First row of exp(-A t) because A^2 = alpha A.
    left = 1.0 - a * qtime
    right = a * qtime
    s00, s01 = realization.S[0]
    s10, s11 = realization.S[1]
    return left * s00 + right * s10, left * s01 + right * s11
