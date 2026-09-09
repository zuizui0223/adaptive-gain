"""Feedback-existence identifiability from a local scalar transient.

For the generalized two-state local response layer,

    T = alpha + phi
    D = alpha*phi + (1-phi)*G,

so for any candidate community memory phi < 1,

    G(phi) = (phi**2 - T*phi + D) / (1-phi).

The numerator is exactly the characteristic polynomial of the observed local
Jacobian evaluated at phi.  This gives a sharp qualitative corollary:

* if the observed eigenvalues are real and both lie in [0,1), choosing phi to
  equal either eigenvalue yields G=0 and alpha equal to the other eigenvalue;
  therefore the scalar monotone transient cannot establish feedback existence;
* if the observed eigenvalues are a non-real conjugate pair, the characteristic
  polynomial is strictly positive for every real phi, hence every feasible
  decomposition with phi<1 has G>0; feedback existence is forced, although its
  magnitude remains unidentified without an independent persistence measure.

The algebra itself is elementary.  The repository-specific use is to sharpen
what the generalized nonidentifiability layer says about the interpretation of
stasis versus oscillatory eco-evolutionary transients.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt

_TOL = 1e-12


def discriminant(trace: float, determinant: float) -> float:
    T = float(trace)
    D = float(determinant)
    if not isfinite(T) or not isfinite(D):
        raise ValueError("trace and determinant must be finite")
    return T * T - 4.0 * D


def characteristic_polynomial_at(
    trace: float, determinant: float, phi: float
) -> float:
    T = float(trace)
    D = float(determinant)
    x = float(phi)
    if not all(isfinite(v) for v in (T, D, x)):
        raise ValueError("inputs must be finite")
    return x * x - T * x + D


def compatible_gain(trace: float, determinant: float, phi: float) -> float:
    x = float(phi)
    if not isfinite(x) or x >= 1.0:
        raise ValueError("phi must be finite and less than 1")
    return characteristic_polynomial_at(trace, determinant, x) / (1.0 - x)


def real_eigenvalues(trace: float, determinant: float) -> tuple[float, float]:
    disc = discriminant(trace, determinant)
    if disc < -_TOL:
        raise ValueError("eigenvalues are not real")
    root = sqrt(max(0.0, disc))
    T = float(trace)
    return ((T - root) / 2.0, (T + root) / 2.0)


def has_nonnegative_real_no_feedback_decomposition(
    trace: float, determinant: float
) -> bool:
    """Whether a decomposition with G=0 and alpha,phi in [0,1) exists."""

    disc = discriminant(trace, determinant)
    if disc < -_TOL:
        return False
    r1, r2 = real_eigenvalues(trace, determinant)
    return (-_TOL <= r1 < 1.0 - _TOL) and (-_TOL <= r2 < 1.0 - _TOL)


def no_feedback_decomposition(
    trace: float, determinant: float
) -> tuple[float, float, float]:
    """Return ``(alpha, phi, G=0)`` when the real nonnegative decomposition exists.

    The smaller eigenvalue is used as ``phi`` for deterministic tie-breaking.
    """

    if not has_nonnegative_real_no_feedback_decomposition(trace, determinant):
        raise ValueError("no feasible nonnegative real G=0 decomposition")
    r1, r2 = real_eigenvalues(trace, determinant)
    phi = min(r1, r2)
    alpha = max(r1, r2)
    G = compatible_gain(trace, determinant, phi)
    if abs(G) > 1e-9:
        raise AssertionError("characteristic-root decomposition must have G=0")
    return alpha, phi, 0.0


def oscillatory_transient_forces_positive_feedback(
    trace: float, determinant: float
) -> bool:
    """Whether a non-real eigenpair forces G(phi)>0 for every real phi<1."""

    return discriminant(trace, determinant) < -_TOL


def minimum_compatible_gain_over_unit_memory_interval(
    trace: float, determinant: float
) -> float:
    """Return the infimum of G(phi) over 0 <= phi < 1.

    For an oscillatory transient the infimum is strictly positive.  The minimum
    is attained at the unique stationary point when it lies in [0,1), otherwise
    at phi=0.  The limit phi->1- is +infinity for Schur-stable oscillatory cases.
    """

    T = float(trace)
    D = float(determinant)
    if not isfinite(T) or not isfinite(D):
        raise ValueError("trace and determinant must be finite")
    # d/dphi [(phi^2-T phi+D)/(1-phi)] =
    # [1 - T + D - (1-phi)^2] / (1-phi)^2.
    radicand = 1.0 - T + D
    candidates = [0.0]
    if radicand >= 0.0:
        phi_star = 1.0 - sqrt(radicand)
        if 0.0 <= phi_star < 1.0:
            candidates.append(phi_star)
    return min(compatible_gain(T, D, phi) for phi in candidates)


@dataclass(frozen=True)
class FeedbackExistenceSummary:
    trace: float
    determinant: float
    discriminant: float
    oscillatory: bool
    no_feedback_decomposition_exists: bool
    feedback_existence_forced: bool
    minimum_gain_over_unit_memory: float | None


def summarize_feedback_existence(
    trace: float, determinant: float
) -> FeedbackExistenceSummary:
    disc = discriminant(trace, determinant)
    oscillatory = disc < -_TOL
    zero_exists = has_nonnegative_real_no_feedback_decomposition(trace, determinant)
    minimum = (
        minimum_compatible_gain_over_unit_memory_interval(trace, determinant)
        if oscillatory
        else None
    )
    return FeedbackExistenceSummary(
        trace=float(trace),
        determinant=float(determinant),
        discriminant=disc,
        oscillatory=oscillatory,
        no_feedback_decomposition_exists=zero_exists,
        feedback_existence_forced=oscillatory,
        minimum_gain_over_unit_memory=minimum,
    )
