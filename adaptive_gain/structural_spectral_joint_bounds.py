"""Joint structural-temporal ceilings for community selection variance.

Suppose every recurrent community state carries a structural sensing gap g_i in

    0 <= g_i <= g_max,

and the continuous structural lift is

    s_i = lambda_cost * g_i - kappa.

The constant kappa disappears after centering.  Popoviciu's variance bound gives

    Var_pi(s) <= (lambda_cost * g_max)^2 / 4.

For a finite reversible ergodic community chain, write the centered reward in
nonstationary eigenmodes of P.  If r_max<1 is the largest nontrivial eigenvalue,
then

    sigma_eff^2
      = sum_j w_j (1+r_j)/(1-r_j)
      <= Var_pi(s) (1+r_max)/(1-r_max).

Combining the two gives the joint ceiling

    sigma_eff^2
      <= (lambda_cost*g_max)^2/4 * (1+r_max)/(1-r_max).

The ingredients are standard variance and reversible Markov-reward identities.
The repository-specific use is to insert an exact finite-sensing gap ceiling for
g_max, thereby constraining short-term structural amplitude and long-term
coherence in one inequality.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .feedback_structural_bounds import bounded_arity_gap_upper_bound


def structural_reward_variance_upper_bound(
    structural_gap_upper_bound: float,
    *,
    lambda_cost: float = 1.0,
) -> float:
    """Popoviciu ceiling for rewards lifted from 0<=g_i<=g_max."""

    gap = float(structural_gap_upper_bound)
    lam = float(lambda_cost)
    if not isfinite(gap) or gap < 0.0:
        raise ValueError("structural_gap_upper_bound must be finite and non-negative")
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    width = lam * gap
    return (width * width) / 4.0


def reversible_temporal_amplification_upper_bound(
    maximal_nontrivial_eigenvalue: float,
) -> float:
    """Largest reversible Markov-reward multiplier (1+r)/(1-r).

    ``maximal_nontrivial_eigenvalue`` is assumed to be the largest algebraic
    nonstationary eigenvalue of an ergodic reversible transition operator.
    """

    r = float(maximal_nontrivial_eigenvalue)
    if not isfinite(r) or not -1.0 < r < 1.0:
        raise ValueError("maximal_nontrivial_eigenvalue must lie strictly in (-1,1)")
    return (1.0 + r) / (1.0 - r)


def joint_asymptotic_variance_upper_bound(
    structural_gap_upper_bound: float,
    *,
    lambda_cost: float,
    maximal_nontrivial_eigenvalue: float,
) -> float:
    """Joint ceiling on the long-run variance rate of centered selection."""

    instantaneous = structural_reward_variance_upper_bound(
        structural_gap_upper_bound,
        lambda_cost=lambda_cost,
    )
    temporal = reversible_temporal_amplification_upper_bound(
        maximal_nontrivial_eigenvalue
    )
    return instantaneous * temporal


@dataclass(frozen=True)
class BoundedAritySpectralCeiling:
    world_count: int
    query_count: int
    adaptive_cost: int
    max_arity: int
    frontier_edge_cap: int | None
    structural_gap_upper_bound: int
    lambda_cost: float
    maximal_nontrivial_eigenvalue: float
    instantaneous_variance_upper_bound: float
    temporal_amplification_upper_bound: float
    asymptotic_variance_upper_bound: float
    scope: str = "unit_cost_bounded_arity_reversible_spectral_joint_ceiling"


def bounded_arity_spectral_ceiling(
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    *,
    lambda_cost: float,
    maximal_nontrivial_eigenvalue: float,
    frontier_edge_cap: int | None = None,
) -> BoundedAritySpectralCeiling:
    """Lift an inherited finite-sensing gap ceiling into a temporal variance ceiling."""

    gap = bounded_arity_gap_upper_bound(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        frontier_edge_cap=frontier_edge_cap,
    )
    instantaneous = structural_reward_variance_upper_bound(
        gap,
        lambda_cost=lambda_cost,
    )
    temporal = reversible_temporal_amplification_upper_bound(
        maximal_nontrivial_eigenvalue
    )
    total = instantaneous * temporal
    return BoundedAritySpectralCeiling(
        world_count=int(world_count),
        query_count=int(query_count),
        adaptive_cost=int(adaptive_cost),
        max_arity=int(max_arity),
        frontier_edge_cap=frontier_edge_cap,
        structural_gap_upper_bound=gap,
        lambda_cost=float(lambda_cost),
        maximal_nontrivial_eigenvalue=float(maximal_nontrivial_eigenvalue),
        instantaneous_variance_upper_bound=instantaneous,
        temporal_amplification_upper_bound=temporal,
        asymptotic_variance_upper_bound=total,
    )
