"""Structural upper bounds on endogenous feedback gain.

This module does not introduce a new combinatorial theorem.  It lifts the
repository's existing bounded-arity fixed-cost upper bound into the local
feedback model.

For a unit-cost high-opportunity task with

    n represented worlds,
    m declared queries,
    maximum query arity b,
    adaptive optimum C_A=h,

the parent theorem gives

    C_F <= min(m, F_b(n,h)).

If the low-opportunity comparison state has structural gap zero, then

    Delta_g <= min(m,F_b(n,h)) - h.

At an interior feedback equilibrium,

    L = -eta * lambda_cost * Delta_g * p*(1-p).

Therefore a restoring negative-feedback loop has an immediate structural upper
bound on L.  If that upper bound does not reach an oscillation or instability
threshold, no task in the declared finite scope can reach that local dynamical
phase under the stated lift.

An optional productive-frontier edge-count cap E uses the already-proved
unit-cost fact C_F <= |H_min| <= E.  A frontier-rank cap is intentionally absent:
the parent repository proves that every positive rank cap is extremally
vacuous for the adaptive/fixed ratio because rank-one obligations already attain
the worst case.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .bounded_arity_extremal_bounds import bounded_arity_fixed_cost_bound
from .feedback_loop_gain import oscillation_threshold


def bounded_arity_gap_upper_bound(
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    *,
    frontier_edge_cap: int | None = None,
) -> int:
    """Upper bound on structural gap C_F-C_A at fixed adaptive cost.

    The bound is inherited from the existing tree-union theorem.  When
    ``frontier_edge_cap`` is supplied, the additional unit-cost bound C_F<=E is
    intersected with the tree/query bound.
    """

    h = int(adaptive_cost)
    if type(adaptive_cost) is not int or h <= 0:
        raise ValueError("adaptive_cost must be a positive integer")
    fixed_bound = bounded_arity_fixed_cost_bound(
        world_count,
        query_count,
        h,
        max_arity,
    )
    if frontier_edge_cap is not None:
        if type(frontier_edge_cap) is not int or frontier_edge_cap < 1:
            raise ValueError("frontier_edge_cap must be a positive integer")
        fixed_bound = min(fixed_bound, frontier_edge_cap)
    if fixed_bound < h:
        raise ValueError(
            "declared structural caps cannot support a task with the supplied adaptive_cost"
        )
    return fixed_bound - h


def restoring_loop_gain_upper_bound(
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    *,
    lambda_cost: float,
    feedback_strength: float,
    equilibrium_frequency: float,
    frontier_edge_cap: int | None = None,
) -> float:
    """Upper bound on positive restoring loop gain L for a gap-zero control.

    Requires ``feedback_strength<0`` because the result bounds the restoring
    negative-feedback magnitude.  The structural gap contrast is bounded by the
    high state's maximum possible C_F-C_A in the declared scope.
    """

    lam = float(lambda_cost)
    eta = float(feedback_strength)
    p = float(equilibrium_frequency)
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    if not isfinite(eta) or eta >= 0.0:
        raise ValueError("feedback_strength must be finite and negative")
    if not 0.0 < p < 1.0:
        raise ValueError("equilibrium_frequency must lie strictly inside (0,1)")
    gap_bound = bounded_arity_gap_upper_bound(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        frontier_edge_cap=frontier_edge_cap,
    )
    return (-eta) * lam * gap_bound * p * (1.0 - p)


@dataclass(frozen=True)
class StructuralPhaseExclusion:
    world_count: int
    query_count: int
    adaptive_cost: int
    max_arity: int
    frontier_edge_cap: int | None
    structural_gap_upper_bound: int
    loop_gain_upper_bound: float
    oscillation_threshold: float
    damped_oscillation_possible: bool
    strong_feedback_instability_possible: bool
    scope: str = "unit_cost_bounded_arity_feedback_phase_upper_bound"


def structural_phase_exclusion(
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
) -> StructuralPhaseExclusion:
    """Certify phases that are structurally unreachable under declared caps.

    ``damped_oscillation_possible=False`` is a rigorous exclusion because even
    the structural loop-gain upper bound does not exceed `(1-phi)/4`.

    ``strong_feedback_instability_possible=False`` is likewise a rigorous
    exclusion because the structural upper bound remains below `L=1`.

    A True value means only "not ruled out by this bound"; it is not an
    existence theorem for a task attaining the phase.
    """

    gap_bound = bounded_arity_gap_upper_bound(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        frontier_edge_cap=frontier_edge_cap,
    )
    Lmax = restoring_loop_gain_upper_bound(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        lambda_cost=lambda_cost,
        feedback_strength=feedback_strength,
        equilibrium_frequency=equilibrium_frequency,
        frontier_edge_cap=frontier_edge_cap,
    )
    threshold = oscillation_threshold(community_memory)
    return StructuralPhaseExclusion(
        world_count=world_count,
        query_count=query_count,
        adaptive_cost=adaptive_cost,
        max_arity=max_arity,
        frontier_edge_cap=frontier_edge_cap,
        structural_gap_upper_bound=gap_bound,
        loop_gain_upper_bound=Lmax,
        oscillation_threshold=threshold,
        damped_oscillation_possible=Lmax > threshold,
        strong_feedback_instability_possible=Lmax >= 1.0,
    )
