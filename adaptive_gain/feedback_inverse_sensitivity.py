"""Sensitivity bounds for the phenotype-only AR(2) feedback inverse.

The local phenotype-logit recurrence is

    x[t+2] = a1*x[t+1] + a2*x[t],

with

    a1 = 1 + phi,
    a2 = -[phi + (1-phi)L].

Suppose fitted coefficients are perturbed by

    a1_hat = a1 + e1,
    a2_hat = a2 + e2.

The inverse formulas give an exact perturbation identity

    phi_hat - phi = e1,

    L_hat - L
      = -[(1-L)e1 + e2] / [1-phi-e1].

Therefore, if ``|e1|<=E1<1-phi`` and ``|e2|<=E2``, then

    |L_hat-L|
      <= [|1-L| E1 + E2] / [1-phi-E1].

This is a deterministic coefficient-error bound, not a statistical confidence
interval.  It makes explicit that the inverse becomes ill-conditioned as
``phi -> 1``.  If the nonstructural scaling

    A = (-eta)*lambda*p_star*(1-p_star)

is treated as known, the corresponding structural-gap error is the loop-gain
error divided by ``A``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class AR2InverseSensitivity:
    community_memory: float
    loop_gain: float
    d_phi_d_a1: float
    d_phi_d_a2: float
    d_L_d_a1: float
    d_L_d_a2: float
    memory_denominator: float


@dataclass(frozen=True)
class AR2FiniteErrorBound:
    community_memory: float
    loop_gain: float
    lag1_error_bound: float
    lag2_error_bound: float
    community_memory_error_bound: float
    loop_gain_error_bound: float
    denominator_margin: float


def _validate_phi_L(phi: float, loop_gain: float) -> tuple[float, float]:
    p = float(phi)
    L = float(loop_gain)
    if not isfinite(p) or not 0.0 <= p < 1.0:
        raise ValueError("community_memory must be finite and lie in [0,1)")
    if not isfinite(L):
        raise ValueError("loop_gain must be finite")
    return p, L


def ar2_inverse_sensitivity(
    community_memory: float,
    loop_gain: float,
) -> AR2InverseSensitivity:
    """Return the exact first-order Jacobian of ``(phi,L)`` with respect to AR(2) coefficients."""

    phi, L = _validate_phi_L(community_memory, loop_gain)
    margin = 1.0 - phi
    return AR2InverseSensitivity(
        community_memory=phi,
        loop_gain=L,
        d_phi_d_a1=1.0,
        d_phi_d_a2=0.0,
        d_L_d_a1=-(1.0 - L) / margin,
        d_L_d_a2=-1.0 / margin,
        memory_denominator=margin,
    )


def exact_ar2_perturbation(
    community_memory: float,
    loop_gain: float,
    *,
    lag1_error: float,
    lag2_error: float,
) -> tuple[float, float]:
    """Return exact ``(phi_hat-phi, L_hat-L)`` for AR(2) coefficient perturbations."""

    phi, L = _validate_phi_L(community_memory, loop_gain)
    e1 = float(lag1_error)
    e2 = float(lag2_error)
    if not isfinite(e1) or not isfinite(e2):
        raise ValueError("coefficient perturbations must be finite")
    denominator = 1.0 - phi - e1
    if denominator <= 0.0:
        raise ValueError("lag1 perturbation crosses the phi=1 singular boundary")
    return (
        e1,
        -((1.0 - L) * e1 + e2) / denominator,
    )


def ar2_finite_error_bound(
    community_memory: float,
    loop_gain: float,
    *,
    lag1_error_bound: float,
    lag2_error_bound: float,
) -> AR2FiniteErrorBound:
    """Deterministic worst-case inverse bound from coefficient-error envelopes."""

    phi, L = _validate_phi_L(community_memory, loop_gain)
    E1 = float(lag1_error_bound)
    E2 = float(lag2_error_bound)
    if not isfinite(E1) or E1 < 0.0:
        raise ValueError("lag1_error_bound must be finite and non-negative")
    if not isfinite(E2) or E2 < 0.0:
        raise ValueError("lag2_error_bound must be finite and non-negative")
    margin = 1.0 - phi - E1
    if margin <= 0.0:
        raise ValueError("lag1_error_bound reaches or crosses the phi=1 singular boundary")
    loop_bound = (abs(1.0 - L) * E1 + E2) / margin
    return AR2FiniteErrorBound(
        community_memory=phi,
        loop_gain=L,
        lag1_error_bound=E1,
        lag2_error_bound=E2,
        community_memory_error_bound=E1,
        loop_gain_error_bound=loop_bound,
        denominator_margin=margin,
    )


def structural_gap_error_bound(
    loop_gain_error_bound: float,
    *,
    lambda_cost: float,
    feedback_strength: float,
    equilibrium_frequency: float,
) -> float:
    """Propagate a loop-gain error bound to ``Delta_g`` when nonstructural factors are fixed."""

    E = float(loop_gain_error_bound)
    lam = float(lambda_cost)
    eta = float(feedback_strength)
    p = float(equilibrium_frequency)
    if not isfinite(E) or E < 0.0:
        raise ValueError("loop_gain_error_bound must be finite and non-negative")
    if not isfinite(lam) or lam <= 0.0:
        raise ValueError("lambda_cost must be finite and positive")
    if not isfinite(eta) or eta >= 0.0:
        raise ValueError("feedback_strength must be finite and negative")
    if not 0.0 < p < 1.0:
        raise ValueError("equilibrium_frequency must lie strictly inside (0,1)")
    scale = (-eta) * lam * p * (1.0 - p)
    return E / scale
