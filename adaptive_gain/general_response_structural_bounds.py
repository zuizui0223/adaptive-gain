"""Structural phase exclusions for the generalized evolutionary-response model.

This module combines the parent's exact unit-cost bounded-arity gap ceiling with
the generalized local response thresholds.

For a high-opportunity task with C_A=h and a gap-zero comparison state,

    Delta_g <= Ggap_max = min(m,F_b(n,h)) - h,

optionally intersected with a productive-frontier edge cap E.

Under the continuous structural lift and restoring ecological feedback ``e<0``,

    generalized_gain = (-beta*e)*lambda_cost*Delta_g.

Hence finite sensing structure bounds the largest possible generalized gain.  If
the bound cannot reach the damped-oscillation threshold or the upper stability
boundary, those phases are impossible for every task in the declared structural
scope.

The combinatorial bound and local response thresholds are both inherited; this
module only composes them.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .feedback_structural_bounds import bounded_arity_gap_upper_bound
from .general_evolutionary_response import general_response_thresholds


@dataclass(frozen=True)
class GeneralStructuralPhaseExclusion:
    world_count: int
    query_count: int
    adaptive_cost: int
    max_arity: int
    frontier_edge_cap: int | None
    structural_gap_upper_bound: int
    generalized_gain_per_gap: float
    generalized_gain_upper_bound: float
    lower_stability_gain: float
    oscillation_gain: float
    upper_stability_gain: float
    damped_oscillation_possible: bool
    upper_instability_possible: bool
    scope: str = "unit_cost_bounded_arity_general_response_phase_upper_bound"


def generalized_gain_per_structural_gap(
    *,
    lambda_cost: float,
    selection_responsiveness: float,
    ecological_feedback_slope: float,
) -> float:
    """Return a=(-beta*e)*lambda for restoring e<0."""

    lam = float(lambda_cost)
    beta = float(selection_responsiveness)
    e = float(ecological_feedback_slope)
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    if not isfinite(beta) or beta < 0.0:
        raise ValueError("selection_responsiveness must be finite and non-negative")
    if not isfinite(e) or e >= 0.0:
        raise ValueError("ecological_feedback_slope must be finite and negative")
    return (-beta * e) * lam


def generalized_structural_gain_upper_bound(
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    *,
    lambda_cost: float,
    selection_responsiveness: float,
    ecological_feedback_slope: float,
    frontier_edge_cap: int | None = None,
) -> float:
    """Maximum generalized restoring gain allowed by inherited structural bounds."""

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
    return a * gap_bound


def general_structural_phase_exclusion(
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
) -> GeneralStructuralPhaseExclusion:
    """Certify generalized damped/upper-instability phases as unreachable.

    A ``False`` possible flag is a rigorous one-sided exclusion under the stated
    finite unit-cost structural scope and local response parameters.  ``True``
    means only that the inherited upper bound does not exclude the phase.
    """

    gap_bound = bounded_arity_gap_upper_bound(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        frontier_edge_cap=frontier_edge_cap,
    )
    per_gap = generalized_gain_per_structural_gap(
        lambda_cost=lambda_cost,
        selection_responsiveness=selection_responsiveness,
        ecological_feedback_slope=ecological_feedback_slope,
    )
    gain_bound = per_gap * gap_bound
    thresholds = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    )
    return GeneralStructuralPhaseExclusion(
        world_count=world_count,
        query_count=query_count,
        adaptive_cost=adaptive_cost,
        max_arity=max_arity,
        frontier_edge_cap=frontier_edge_cap,
        structural_gap_upper_bound=gap_bound,
        generalized_gain_per_gap=per_gap,
        generalized_gain_upper_bound=gain_bound,
        lower_stability_gain=thresholds.lower_stability_gain,
        oscillation_gain=thresholds.oscillation_gain,
        upper_stability_gain=thresholds.upper_stability_gain,
        damped_oscillation_possible=gain_bound > thresholds.oscillation_gain,
        upper_instability_possible=gain_bound >= thresholds.upper_stability_gain,
    )
