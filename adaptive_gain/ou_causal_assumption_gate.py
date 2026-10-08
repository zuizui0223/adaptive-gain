"""Causal attribution gate for a partially observed moving-optimum OU model.

The evoTS OUBM observation law has two latent innovation channels with observed
impulse-response kernel

    h_E(t) = [sqrt(v_trait) exp(-alpha t),
              sqrt(v_optimum) (1-exp(-alpha t))].

A reciprocal two-state realization can reproduce this law exactly, but doing so
requires instantaneous innovation covariance between the observed trait and the
latent coordinate whenever the trait has non-zero process variance.

This module makes that assumption boundary executable.  The result is not a
claim that state-space similarity is new mathematics; it isolates which
biological assumption, rather than the scalar trait data, selects a causal
interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose


@dataclass(frozen=True)
class GaugeTransform:
    """Output-preserving linear transformation of the hidden coordinate.

    We use T = [[1, 0], [t, u]] with u != 0, so the observed coordinate is
    unchanged exactly: X' = X.
    """

    alpha: float
    v_trait: float
    v_optimum: float
    t: float
    u: float
    A: tuple[tuple[float, float], tuple[float, float]]
    Q: tuple[tuple[float, float], tuple[float, float]]

    @property
    def reverse_coupling(self) -> float:
        return self.A[1][0]

    @property
    def forward_coupling(self) -> float:
        return self.A[0][1]

    @property
    def reciprocal(self) -> bool:
        return (not isclose(self.forward_coupling, 0.0, abs_tol=1e-12)) and (
            not isclose(self.reverse_coupling, 0.0, abs_tol=1e-12)
        )

    @property
    def innovation_covariance(self) -> float:
        return self.Q[0][1]


def output_preserving_gauge(
    *,
    alpha: float,
    v_trait: float,
    v_optimum: float,
    t: float,
    u: float,
) -> GaugeTransform:
    """Transform evoTS OUBM while leaving the observed trait path unchanged.

    The source drift matrix in ``dZ = -A Z dt + S dW`` form is

        A0 = [[alpha, -alpha], [0, 0]],

    with process covariance ``Q0=diag(v_trait, v_optimum)``.  Under
    ``T=[[1,0],[t,u]]``, the transformed state has

        A' = T A0 T^{-1}
        Q' = T Q0 T^T.

    The first state coordinate is unchanged, so this is an exact observation-law
    equivalence, including non-stationary finite-time distributions.
    """

    rate = float(alpha)
    vx = float(v_trait)
    vo = float(v_optimum)
    tt = float(t)
    uu = float(u)
    if rate <= 0.0:
        raise ValueError("alpha must be positive")
    if vx < 0.0 or vo < 0.0:
        raise ValueError("process variances must be non-negative")
    if uu == 0.0:
        raise ValueError("u must be non-zero")

    A = (
        (rate * (tt + uu) / uu, -rate / uu),
        (rate * tt * (tt + uu) / uu, -rate * tt / uu),
    )
    Q = (
        (vx, tt * vx),
        (tt * vx, tt * tt * vx + uu * uu * vo),
    )
    return GaugeTransform(
        alpha=rate,
        v_trait=vx,
        v_optimum=vo,
        t=tt,
        u=uu,
        A=A,
        Q=Q,
    )


def reciprocal_gauge_requires_shared_innovation(
    *, v_trait: float, t: float, u: float, tol: float = 1e-12
) -> bool:
    """Whether a reciprocal gauge necessarily has cross-innovation covariance.

    For positive trait process variance, any output-preserving similarity that
    creates a non-zero reverse coupling has ``t != 0`` and therefore
    ``Q12=t*v_trait != 0``.
    """

    vx = float(v_trait)
    tt = float(t)
    uu = float(u)
    if vx <= 0.0:
        raise ValueError("v_trait must be positive for this implication")
    if uu == 0.0:
        raise ValueError("u must be non-zero")
    reverse_nonzero = abs(tt * (tt + uu)) > tol
    if not reverse_nonzero:
        return False
    return abs(tt * vx) > tol


def independent_innovation_equivalence_forces_one_way(
    *,
    alpha: float,
    v_trait: float,
    q_trait: float,
    a11: float,
    a12: float,
    a21: float,
    a22: float,
    q_latent: float,
    tol: float = 1e-9,
) -> bool:
    """Check the zero-mode no-go implication for independent innovations.

    Consider any two-state model with deterministic initial state, drift trace
    ``alpha`` and determinant zero, diagonal process covariance
    ``diag(q_trait, q_latent)``, and observed first coordinate.  If its complete
    observed covariance kernel equals evoTS OUBM with ``v_trait>0``, coefficient
    matching in the finite-time impulse-response inner product forces

        q_trait = v_trait,
        a11 = alpha,
        a22 = 0,
        a12*a21 = 0.

    Thus if the hidden state affects X (a12 != 0), the reverse coupling a21
    must vanish.  This function verifies the algebraic implication for a
    candidate parameter set satisfying the prerequisite invariant equations.
    """

    rate = float(alpha)
    vx = float(v_trait)
    if rate <= 0.0 or vx <= 0.0:
        raise ValueError("alpha and v_trait must be positive")
    qt = float(q_trait)
    ql = float(q_latent)
    if qt < 0.0 or ql < 0.0:
        raise ValueError("innovation variances must be non-negative")

    trace_ok = abs((float(a11) + float(a22)) - rate) <= tol
    det_ok = abs(float(a11) * float(a22) - float(a12) * float(a21)) <= tol
    observed_short_time_ok = abs(qt - vx) <= tol
    observed_linear_coefficient_ok = abs(qt * float(a11) - vx * rate) <= tol
    prerequisites = (
        trace_ok
        and det_ok
        and observed_short_time_ok
        and observed_linear_coefficient_ok
    )
    if not prerequisites:
        return False

    return (
        abs(float(a11) - rate) <= tol
        and abs(float(a22)) <= tol
        and abs(float(a12) * float(a21)) <= tol
    )
