"""Finite structural ceilings on generalized-response damped transients.

For restoring generalized feedback under the continuous structural lift,

    G = a_g * Delta_g,
    a_g = (-beta*e)*lambda_cost > 0,

and unit-cost structural gaps are non-negative integers bounded by the inherited
bounded-arity/productive-frontier theorem.

The generalized stable damped phase is

    G_osc < G < G_plus,

where both thresholds depend on evolutionary persistence alpha and community
memory phi.  Gap integrality therefore identifies

* the smallest structural gap entering the damped phase;
* the largest structural gap remaining below the upper stability boundary.

Those integer envelopes give class-wide one-sided ceilings on local oscillation
period and e-folding damping time.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, floor, inf, isfinite, log, nextafter, pi, sqrt

from .feedback_structural_bounds import bounded_arity_gap_upper_bound
from .general_evolutionary_response import general_response_thresholds
from .general_response_structural_bounds import generalized_gain_per_structural_gap


def largest_generalized_stable_integer_gap(
    gap_upper_bound: int,
    gain_per_gap: float,
    upper_stability_gain: float,
) -> int | None:
    """Largest integer gap with a*g<G_plus."""

    if type(gap_upper_bound) is not int or gap_upper_bound < 0:
        raise ValueError("gap_upper_bound must be a non-negative integer")
    a = float(gain_per_gap)
    upper = float(upper_stability_gain)
    if not isfinite(a) or a < 0.0:
        raise ValueError("gain_per_gap must be finite and non-negative")
    if not isfinite(upper) or upper <= 0.0:
        raise ValueError("upper_stability_gain must be finite and positive")
    if gap_upper_bound == 0 or a == 0.0:
        return None
    strict_limit = floor(nextafter(upper / a, -inf))
    candidate = min(gap_upper_bound, strict_limit)
    return candidate if candidate >= 1 else None


def smallest_generalized_damped_integer_gap(
    gap_upper_bound: int,
    gain_per_gap: float,
    oscillation_gain: float,
    upper_stability_gain: float,
) -> int | None:
    """Smallest integer gap with G_osc<a*g<G_plus."""

    if type(gap_upper_bound) is not int or gap_upper_bound < 0:
        raise ValueError("gap_upper_bound must be a non-negative integer")
    a = float(gain_per_gap)
    osc = float(oscillation_gain)
    upper = float(upper_stability_gain)
    if not isfinite(a) or a < 0.0:
        raise ValueError("gain_per_gap must be finite and non-negative")
    if not isfinite(osc) or osc < 0.0:
        raise ValueError("oscillation_gain must be finite and non-negative")
    if not isfinite(upper) or upper <= osc:
        raise ValueError("upper_stability_gain must exceed oscillation_gain")
    if gap_upper_bound == 0 or a == 0.0:
        return None

    maximum_stable = largest_generalized_stable_integer_gap(
        gap_upper_bound,
        a,
        upper,
    )
    if maximum_stable is None:
        return None
    candidate = floor(nextafter(osc / a, inf)) + 1
    candidate = max(1, candidate)
    if candidate > maximum_stable:
        return None
    return candidate


def generalized_damped_damping_time(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> float:
    """Exact e-folding time for a stable generalized damped pair."""

    G = float(generalized_gain)
    thresholds = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    )
    if not thresholds.oscillation_gain < G < thresholds.upper_stability_gain:
        raise ValueError("requires generalized stable damped phase")
    alpha = thresholds.evolutionary_persistence
    phi = thresholds.community_memory
    determinant = alpha * phi + (1.0 - phi) * G
    rho = sqrt(determinant)
    if not 0.0 < rho < 1.0:
        raise ValueError("stable damped spectral radius must lie in (0,1)")
    return -1.0 / log(rho)


def generalized_damped_period(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> float:
    """Exact local period in the generalized stable damped phase."""

    G = float(generalized_gain)
    thresholds = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    )
    if not thresholds.oscillation_gain < G < thresholds.upper_stability_gain:
        raise ValueError("requires generalized stable damped phase")
    alpha = thresholds.evolutionary_persistence
    phi = thresholds.community_memory
    determinant = alpha * phi + (1.0 - phi) * G
    rho = sqrt(determinant)
    cosine = (alpha + phi) / (2.0 * rho)
    cosine = min(1.0, max(-1.0, cosine))
    theta = acos(cosine)
    if theta <= 0.0:
        return inf
    return 2.0 * pi / theta


@dataclass(frozen=True)
class GeneralStructuralTransientCeiling:
    world_count: int
    query_count: int
    adaptive_cost: int
    max_arity: int
    frontier_edge_cap: int | None
    evolutionary_persistence: float
    community_memory: float
    structural_gap_upper_bound: int
    gain_per_integer_gap: float
    oscillation_gain: float
    upper_stability_gain: float
    maximum_stable_gap: int | None
    maximum_stable_gain: float | None
    minimum_damped_gap: int | None
    minimum_damped_gain: float | None
    damped_phase_structurally_possible: bool
    damping_time_upper_bound: float | None
    oscillation_period_upper_bound: float | None
    scope: str = "unit_cost_bounded_arity_general_response_transient_ceiling"


def general_structural_transient_ceiling(
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    *,
    evolutionary_persistence: float,
    community_memory: float,
    lambda_cost: float,
    selection_responsiveness: float,
    ecological_feedback_slope: float,
    frontier_edge_cap: int | None = None,
) -> GeneralStructuralTransientCeiling:
    """Universal local stable-damped time ceilings over a finite sensing scope."""

    gap_bound = bounded_arity_gap_upper_bound(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        frontier_edge_cap=frontier_edge_cap,
    )
    a = generalized_gain_per_structural_gap(
        lambda_cost=lambda_cost,
        selection_responsiveness=selection_responsiveness,
        ecological_feedback_slope=ecological_feedback_slope,
    )
    thresholds = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    )
    g_stable = largest_generalized_stable_integer_gap(
        gap_bound,
        a,
        thresholds.upper_stability_gain,
    )
    g_damped = smallest_generalized_damped_integer_gap(
        gap_bound,
        a,
        thresholds.oscillation_gain,
        thresholds.upper_stability_gain,
    )
    G_stable = a * g_stable if g_stable is not None else None
    G_damped = a * g_damped if g_damped is not None else None

    damping_ceiling = None
    period_ceiling = None
    if g_damped is not None:
        assert G_stable is not None and G_damped is not None
        damping_ceiling = generalized_damped_damping_time(
            G_stable,
            evolutionary_persistence=evolutionary_persistence,
            community_memory=community_memory,
        )
        period_ceiling = generalized_damped_period(
            G_damped,
            evolutionary_persistence=evolutionary_persistence,
            community_memory=community_memory,
        )

    return GeneralStructuralTransientCeiling(
        world_count=world_count,
        query_count=query_count,
        adaptive_cost=adaptive_cost,
        max_arity=max_arity,
        frontier_edge_cap=frontier_edge_cap,
        evolutionary_persistence=float(evolutionary_persistence),
        community_memory=float(community_memory),
        structural_gap_upper_bound=gap_bound,
        gain_per_integer_gap=a,
        oscillation_gain=thresholds.oscillation_gain,
        upper_stability_gain=thresholds.upper_stability_gain,
        maximum_stable_gap=g_stable,
        maximum_stable_gain=G_stable,
        minimum_damped_gap=g_damped,
        minimum_damped_gain=G_damped,
        damped_phase_structurally_possible=(g_damped is not None),
        damping_time_upper_bound=damping_ceiling,
        oscillation_period_upper_bound=period_ceiling,
    )
