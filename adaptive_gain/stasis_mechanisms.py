"""Exact local distinction between cancellation and restoring stasis.

Two mechanisms can both produce little or no long-run net change while having
very different local dynamics.

Cancellation stasis is defined here in the additive weak-selection coordinate

    z[t+1] = z[t] + E * beta[t].

For a periodic selection cycle with zero signed sum, the one-cycle map is the
identity.  Short-term activity can be arbitrarily large, but a perturbation to
z is not repaired: it survives unchanged from cycle to cycle.

Restoring stasis is defined locally around a fixed point of an autonomous
feedback system.  If every eigenvalue of the Jacobian lies strictly inside the
unit disk, perturbations decay asymptotically.  A complex pair gives damped
oscillatory restoring dynamics; non-negative real eigenvalues give a monotone
restoring candidate.

The identity-vs-contraction distinction is standard dynamical-systems algebra.
The repository-specific role is to keep the two stasis mechanisms separate in
the information-structured eco-evolutionary synthesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

_TOL = 1e-12


def _finite_sequence(values: Iterable[float], *, name: str) -> tuple[float, ...]:
    out = tuple(float(x) for x in values)
    if not out:
        raise ValueError(f"{name} must be non-empty")
    if not all(isfinite(x) for x in out):
        raise ValueError(f"{name} must contain only finite values")
    return out


def cancellation_cycle_map(
    state: float,
    selection_cycle: Iterable[float],
    *,
    evolvability: float = 1.0,
) -> float:
    """Apply one complete additive weak-selection cycle to a scalar state."""

    z = float(state)
    if not isfinite(z):
        raise ValueError("state must be finite")
    beta = _finite_sequence(selection_cycle, name="selection_cycle")
    E = float(evolvability)
    if not isfinite(E) or E < 0.0:
        raise ValueError("evolvability must be finite and non-negative")
    return z + E * sum(beta)


@dataclass(frozen=True)
class CancellationStasisSummary:
    period: int
    cycle_sum: float
    activity: float
    retained_change: float
    period_multiplier: float
    neutral: bool


def summarize_cancellation_stasis(
    selection_cycle: Iterable[float],
    *,
    evolvability: float = 1.0,
    tolerance: float = _TOL,
) -> CancellationStasisSummary:
    """Return the exact one-cycle invariants of zero-sum additive selection.

    A cancellation-stasis cycle must have zero signed selection over the period.
    The period map is then the identity and its scalar multiplier is exactly one.
    """

    beta = _finite_sequence(selection_cycle, name="selection_cycle")
    E = float(evolvability)
    tol = abs(float(tolerance))
    if not isfinite(E) or E < 0.0:
        raise ValueError("evolvability must be finite and non-negative")
    if not isfinite(tol):
        raise ValueError("tolerance must be finite")
    cycle_sum = sum(beta)
    if abs(cycle_sum) > tol:
        raise ValueError("cancellation stasis requires a zero-sum selection cycle")
    activity = E * sum(abs(x) for x in beta)
    retained = abs(E * cycle_sum)
    return CancellationStasisSummary(
        period=len(beta),
        cycle_sum=cycle_sum,
        activity=activity,
        retained_change=retained,
        period_multiplier=1.0,
        neutral=True,
    )


@dataclass(frozen=True)
class RestoringStasisSummary:
    eigenvalues: tuple[complex, ...]
    spectral_radius: float
    locally_attractive: bool
    oscillatory: bool
    monotone_candidate: bool


def summarize_restoring_stasis(
    eigenvalues: Iterable[complex],
    *,
    tolerance: float = _TOL,
) -> RestoringStasisSummary:
    """Classify local restoring dynamics from fixed-point eigenvalues."""

    vals = tuple(complex(x) for x in eigenvalues)
    if not vals:
        raise ValueError("eigenvalues must be non-empty")
    if not all(isfinite(v.real) and isfinite(v.imag) for v in vals):
        raise ValueError("eigenvalues must be finite")
    tol = abs(float(tolerance))
    if not isfinite(tol):
        raise ValueError("tolerance must be finite")

    radius = max(abs(v) for v in vals)
    attractive = radius < 1.0 - tol
    oscillatory = any(abs(v.imag) > tol for v in vals)
    monotone = (
        attractive
        and not oscillatory
        and all(v.real >= -tol for v in vals)
    )
    return RestoringStasisSummary(
        eigenvalues=vals,
        spectral_radius=radius,
        locally_attractive=attractive,
        oscillatory=oscillatory,
        monotone_candidate=monotone,
    )
