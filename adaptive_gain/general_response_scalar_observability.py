"""Observability gate for recovering local trace and determinant from one series.

Every scalar coordinate of the local two-dimensional generalized response system
satisfies

    x[t+2] = T*x[t+1] - D*x[t].

Four consecutive noiseless observations give two linear equations for ``T`` and
``D``.  Their determinant is

    R = x0*x2 - x1^2.

When ``R != 0`` the invariants are uniquely recovered as

    T = (x0*x3 - x1*x2) / R,
    D = (x1*x3 - x2^2) / R.

When ``R=0`` the four points do not identify both invariants.  A canonical
example is a single visible eigenmode ``x_t=c*r^t``.  Thus a long trajectory is
not enough by itself: the perturbation and observation must expose both local
modes.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class ScalarInvariantEstimate:
    trace: float
    determinant: float
    visibility_determinant: float
    normalized_visibility_margin: float


def _values(*items: float) -> tuple[float, ...]:
    out = tuple(float(x) for x in items)
    if not all(isfinite(x) for x in out):
        raise ValueError("observations must be finite")
    return out


def scalar_mode_visibility_determinant(x0: float, x1: float, x2: float) -> float:
    """Return ``R=x0*x2-x1^2`` for the local scalar recurrence."""

    a, b, c = _values(x0, x1, x2)
    return a * c - b * b


def identify_trace_determinant_from_four_points(
    x0: float,
    x1: float,
    x2: float,
    x3: float,
    *,
    relative_tolerance: float = 1e-12,
) -> ScalarInvariantEstimate:
    """Recover ``(T,D)`` when the observed scalar trajectory exposes two modes.

    ``relative_tolerance`` is only a numerical singularity guard.  This helper is
    deterministic and does not provide a statistical uncertainty interval.
    """

    a, b, c, d = _values(x0, x1, x2, x3)
    tol = float(relative_tolerance)
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("relative_tolerance must be finite and non-negative")

    R = a * c - b * b
    scale = max(
        1.0,
        abs(a * c),
        abs(b * b),
        abs(a * d),
        abs(b * c),
        abs(b * d),
        abs(c * c),
    )
    margin = abs(R) / scale
    if margin <= tol:
        raise ValueError(
            "scalar trajectory does not expose two independent local modes at the requested tolerance"
        )

    trace = (a * d - b * c) / R
    determinant = (b * d - c * c) / R
    return ScalarInvariantEstimate(
        trace=trace,
        determinant=determinant,
        visibility_determinant=R,
        normalized_visibility_margin=margin,
    )


def two_real_mode_visibility_determinant(
    coefficient_1: float,
    coefficient_2: float,
    eigenvalue_1: float,
    eigenvalue_2: float,
) -> float:
    """Closed form for ``x_t=c1*r1^t+c2*r2^t``.

    The first Hankel determinant is

        R = c1*c2*(r1-r2)^2.

    It vanishes when either mode is absent or the two eigenvalues coincide.
    """

    c1, c2, r1, r2 = _values(
        coefficient_1,
        coefficient_2,
        eigenvalue_1,
        eigenvalue_2,
    )
    return c1 * c2 * (r1 - r2) ** 2
