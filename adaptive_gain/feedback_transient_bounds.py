"""Finite-structure upper bounds on stable eco-evolutionary transient times.

This module combines two already-established ingredients:

1. the bounded-arity structural gap upper bound on ``C_F-C_A``;
2. the endogenous feedback phase formulas in which

       L = a * Delta_g,
       a = (-eta) * lambda_cost * p_star * (1-p_star) > 0.

For unit-cost tasks the structural gap is an integer.  Hence a finite sensing
scope not only bounds the largest loop gain; it also bounds the largest *stable*
integer gap satisfying ``L<1`` and the smallest integer gap entering the damped
phase ``L>(1-phi)/4``.

These integer envelopes give rigorous one-sided ceilings on

* the e-folding damping time of any stable damped transient;
* the oscillation period of any stable damped transient.

A finite ceiling is an upper bound for every realizable task in the declared
scope.  It is not an existence claim that a task attaining the envelope exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, floor, inf, isfinite, nextafter, pi, sqrt

from .feedback_loop_gain import (
    damping_time_from_loop_gain,
    oscillation_threshold,
)
from .feedback_structural_bounds import bounded_arity_gap_upper_bound


def restoring_gain_per_gap(
    *,
    lambda_cost: float,
    feedback_strength: float,
    equilibrium_frequency: float,
) -> float:
    """Return ``a=(-eta)*lambda*p*(1-p)`` for a restoring feedback loop."""

    lam = float(lambda_cost)
    eta = float(feedback_strength)
    p = float(equilibrium_frequency)
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    if not isfinite(eta) or eta >= 0.0:
        raise ValueError("feedback_strength must be finite and negative")
    if not 0.0 < p < 1.0:
        raise ValueError("equilibrium_frequency must lie strictly inside (0,1)")
    return (-eta) * lam * p * (1.0 - p)


def largest_stable_integer_gap(gap_upper_bound: int, gain_per_gap: float) -> int | None:
    """Largest integer gap ``g`` with ``1<=g<=G`` and ``a*g<1``.

    ``nextafter`` makes the strict stability boundary robust when ``1/a`` is
    itself an integer.
    """

    if type(gap_upper_bound) is not int or gap_upper_bound < 0:
        raise ValueError("gap_upper_bound must be a non-negative integer")
    a = float(gain_per_gap)
    if not isfinite(a) or a < 0.0:
        raise ValueError("gain_per_gap must be finite and non-negative")
    if gap_upper_bound == 0 or a == 0.0:
        return None
    strict_limit = floor(nextafter(1.0 / a, -inf))
    candidate = min(gap_upper_bound, strict_limit)
    return candidate if candidate >= 1 else None


def smallest_damped_integer_gap(
    gap_upper_bound: int,
    gain_per_gap: float,
    community_memory: float,
) -> int | None:
    """Smallest stable integer gap entering the damped-oscillatory phase."""

    if type(gap_upper_bound) is not int or gap_upper_bound < 0:
        raise ValueError("gap_upper_bound must be a non-negative integer")
    a = float(gain_per_gap)
    if not isfinite(a) or a < 0.0:
        raise ValueError("gain_per_gap must be finite and non-negative")
    if gap_upper_bound == 0 or a == 0.0:
        return None
    maximum_stable = largest_stable_integer_gap(gap_upper_bound, a)
    if maximum_stable is None:
        return None
    threshold = oscillation_threshold(community_memory)
    # Strictly require a*g > threshold.  Nudging upward protects an exact
    # integer ratio threshold/a from being classified as damped at equality.
    candidate = floor(nextafter(threshold / a, inf)) + 1
    candidate = max(1, candidate)
    if candidate > maximum_stable:
        return None
    return candidate


def damped_period_from_loop_gain(loop_gain: float, community_memory: float) -> float:
    """Exact local period for a stable damped loop-gain pair ``(L,phi)``."""

    L = float(loop_gain)
    phi = float(community_memory)
    threshold = oscillation_threshold(phi)
    if not threshold < L < 1.0:
        raise ValueError("requires stable damped phase: (1-phi)/4 < L < 1")
    determinant = phi + (1.0 - phi) * L
    rho = sqrt(determinant)
    cosine = (1.0 + phi) / (2.0 * rho)
    # Roundoff may put a theoretically valid cosine a few ulps outside [-1,1].
    cosine = min(1.0, max(-1.0, cosine))
    theta = acos(cosine)
    return 2.0 * pi / theta


@dataclass(frozen=True)
class StructuralTransientCeiling:
    world_count: int
    query_count: int
    adaptive_cost: int
    max_arity: int
    frontier_edge_cap: int | None
    structural_gap_upper_bound: int
    gain_per_integer_gap: float
    community_memory: float
    oscillation_threshold: float
    maximum_stable_gap: int | None
    maximum_stable_loop_gain: float | None
    minimum_damped_gap: int | None
    minimum_damped_loop_gain: float | None
    damped_phase_structurally_possible: bool
    damping_time_upper_bound: float | None
    oscillation_period_upper_bound: float | None
    scope: str = "unit_cost_bounded_arity_feedback_transient_time_ceiling"


def structural_transient_ceiling(
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    *,
    lambda_cost: float,
    feedback_strength: float,
    equilibrium_frequency: float,
    community_memory: float,
    frontier_edge_cap: int | None = None,
) -> StructuralTransientCeiling:
    """Bound stable damped transient times from finite sensing constraints.

    The result uses only the inherited structural gap upper bound and the fact
    that a unit-cost gap is integer.  If no stable damped integer gap is allowed,
    both time ceilings are ``None`` and the phase is rigorously excluded.

    If the phase is allowed, ``damping_time_upper_bound`` is evaluated at the
    largest stable integer gap because damping time increases monotonically with
    ``L``.  ``oscillation_period_upper_bound`` is evaluated at the smallest
    damped integer gap because period decreases monotonically with ``L`` inside
    the damped phase.
    """

    gap_bound = bounded_arity_gap_upper_bound(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        frontier_edge_cap=frontier_edge_cap,
    )
    a = restoring_gain_per_gap(
        lambda_cost=lambda_cost,
        feedback_strength=feedback_strength,
        equilibrium_frequency=equilibrium_frequency,
    )
    threshold = oscillation_threshold(community_memory)
    g_stable = largest_stable_integer_gap(gap_bound, a)
    L_stable = a * g_stable if g_stable is not None else None
    g_damped = smallest_damped_integer_gap(gap_bound, a, community_memory)
    L_damped = a * g_damped if g_damped is not None else None

    damped_possible = g_damped is not None
    damping_ceiling = None
    period_ceiling = None
    if damped_possible:
        assert L_stable is not None and L_damped is not None
        damping_ceiling = damping_time_from_loop_gain(L_stable, community_memory)
        period_ceiling = damped_period_from_loop_gain(L_damped, community_memory)

    return StructuralTransientCeiling(
        world_count=world_count,
        query_count=query_count,
        adaptive_cost=adaptive_cost,
        max_arity=max_arity,
        frontier_edge_cap=frontier_edge_cap,
        structural_gap_upper_bound=gap_bound,
        gain_per_integer_gap=a,
        community_memory=float(community_memory),
        oscillation_threshold=threshold,
        maximum_stable_gap=g_stable,
        maximum_stable_loop_gain=L_stable,
        minimum_damped_gap=g_damped,
        minimum_damped_loop_gain=L_damped,
        damped_phase_structurally_possible=damped_possible,
        damping_time_upper_bound=damping_ceiling,
        oscillation_period_upper_bound=period_ceiling,
    )
