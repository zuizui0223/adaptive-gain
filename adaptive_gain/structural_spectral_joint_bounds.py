"""Joint structural-temporal ceilings for community selection variance.

Suppose every recurrent community state carries a structural sensing gap g_i in

    0 <= g_i <= g_max,

and the continuous structural lift is

    s_i = lambda_cost * g_i - kappa.

The constant kappa disappears after centering.  Popoviciu's variance bound gives

    Var_pi(s) <= (lambda_cost * g_max)^2 / 4.

For a finite reversible ergodic community chain, write the centered reward in
nonstationary eigenmodes of P.  If r_max<1 is the largest nontrivial algebraic
eigenvalue, then

    sigma_eff^2
      = sum_j w_j (1+r_j)/(1-r_j)
      <= Var_pi(s) (1+r_max)/(1-r_max).

Combining the two gives the joint ceiling

    sigma_eff^2
      <= (lambda_cost*g_max)^2/4 * (1+r_max)/(1-r_max).

The ceiling is sharp in the extremal sense but need not be tight for a generic
multi-state chain.  Its realized slack factors exactly into

    range_saturation
      = 4 Var_pi(s) / (lambda_cost*g_max)^2

and

    mode_alignment
      = sigma_eff^2 / [Var_pi(s) * (1+r_max)/(1-r_max)],

whenever Var_pi(s)>0.  The first factor measures whether rewards use the full
structural range; the second measures how strongly reward variance loads onto
persistent modes relative to the slowest algebraic mode.

If stationary mean selection has nonzero magnitude |mu|, the asymptotic
mean-versus-fluctuation crossover proxy

    H_x^asy = sigma_eff^2 / mu^2

therefore obeys the same structural-temporal ceiling divided by mu^2.  This is a
bound on the asymptotic proxy, not an exact finite-time hitting-time theorem.

The ingredients are standard variance and reversible Markov-reward identities.
The repository-specific use is to insert an exact finite-sensing gap ceiling for
g_max, thereby constraining short-term structural amplitude and long-term
coherence in one inequality.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .feedback_structural_bounds import bounded_arity_gap_upper_bound

_TOL = 1e-12


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


def directional_crossover_proxy_upper_bound(
    structural_gap_upper_bound: float,
    *,
    lambda_cost: float,
    maximal_nontrivial_eigenvalue: float,
    stationary_mean_selection_magnitude: float,
) -> float:
    """Ceiling on the asymptotic crossover proxy sigma_eff^2 / mu^2.

    Requires a strictly nonzero declared stationary mean-selection magnitude.
    This is not an exact first-passage or finite-horizon emergence-time result.
    """

    mu = float(stationary_mean_selection_magnitude)
    if not isfinite(mu) or mu <= 0.0:
        raise ValueError(
            "stationary_mean_selection_magnitude must be finite and strictly positive"
        )
    variance_ceiling = joint_asymptotic_variance_upper_bound(
        structural_gap_upper_bound,
        lambda_cost=lambda_cost,
        maximal_nontrivial_eigenvalue=maximal_nontrivial_eigenvalue,
    )
    return variance_ceiling / (mu * mu)


@dataclass(frozen=True)
class StructuralTemporalSlack:
    """Audit decomposition of realized variance relative to the extremal ceiling."""

    structural_variance_ceiling: float
    temporal_amplification_ceiling: float
    joint_variance_ceiling: float
    stationary_reward_variance: float
    asymptotic_variance_rate: float
    range_variance_saturation: float
    reward_slow_mode_alignment: float | None
    realized_to_ceiling_ratio: float


def structural_temporal_slack(
    structural_gap_upper_bound: float,
    *,
    lambda_cost: float,
    maximal_nontrivial_eigenvalue: float,
    stationary_reward_variance: float,
    asymptotic_variance_rate: float,
) -> StructuralTemporalSlack:
    """Decompose the gap between realized variance and the joint extremal bound.

    Under the theorem assumptions and positive stationary reward variance,

        sigma_eff^2 / B
          = [Var_pi(s) / V_max]
            * [sigma_eff^2 / (Var_pi(s) * A_max)],

    where ``V_max=(lambda*g_max)^2/4`` and
    ``A_max=(1+r_max)/(1-r_max)``.  Each factor lies in ``[0,1]``.  When reward
    variance is exactly zero, the mode-alignment factor is undefined and is
    returned as ``None`` while the realized-to-ceiling ratio is zero.

    The function is an audit helper: inputs that violate either component bound
    raise ``ValueError`` rather than silently producing a factor above one.
    """

    variance = float(stationary_reward_variance)
    sigma2 = float(asymptotic_variance_rate)
    if not isfinite(variance) or variance < 0.0:
        raise ValueError("stationary_reward_variance must be finite and non-negative")
    if not isfinite(sigma2) or sigma2 < 0.0:
        raise ValueError("asymptotic_variance_rate must be finite and non-negative")

    variance_ceiling = structural_reward_variance_upper_bound(
        structural_gap_upper_bound,
        lambda_cost=lambda_cost,
    )
    temporal_ceiling = reversible_temporal_amplification_upper_bound(
        maximal_nontrivial_eigenvalue
    )
    joint_ceiling = variance_ceiling * temporal_ceiling

    if variance_ceiling <= _TOL:
        if variance > _TOL or sigma2 > _TOL:
            raise ValueError("positive realized variance is incompatible with a zero structural ceiling")
        return StructuralTemporalSlack(
            structural_variance_ceiling=variance_ceiling,
            temporal_amplification_ceiling=temporal_ceiling,
            joint_variance_ceiling=joint_ceiling,
            stationary_reward_variance=variance,
            asymptotic_variance_rate=sigma2,
            range_variance_saturation=0.0,
            reward_slow_mode_alignment=None,
            realized_to_ceiling_ratio=0.0,
        )

    if variance > variance_ceiling + _TOL * max(1.0, variance_ceiling):
        raise ValueError("stationary reward variance exceeds the structural range ceiling")

    range_saturation = variance / variance_ceiling
    if variance <= _TOL:
        if sigma2 > _TOL:
            raise ValueError("positive asymptotic variance is incompatible with zero reward variance")
        mode_alignment = None
        ratio = 0.0
    else:
        modal_ceiling = variance * temporal_ceiling
        if sigma2 > modal_ceiling + _TOL * max(1.0, modal_ceiling):
            raise ValueError("asymptotic variance exceeds the reversible modal ceiling")
        mode_alignment = sigma2 / modal_ceiling
        ratio = sigma2 / joint_ceiling
        product = range_saturation * mode_alignment
        if abs(product - ratio) > 1e-10 * max(1.0, abs(ratio)):
            raise ArithmeticError("structural-temporal slack factorization failed")

    return StructuralTemporalSlack(
        structural_variance_ceiling=variance_ceiling,
        temporal_amplification_ceiling=temporal_ceiling,
        joint_variance_ceiling=joint_ceiling,
        stationary_reward_variance=variance,
        asymptotic_variance_rate=sigma2,
        range_variance_saturation=range_saturation,
        reward_slow_mode_alignment=mode_alignment,
        realized_to_ceiling_ratio=ratio,
    )


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


def bounded_arity_directional_crossover_proxy_upper_bound(
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    *,
    lambda_cost: float,
    maximal_nontrivial_eigenvalue: float,
    stationary_mean_selection_magnitude: float,
    frontier_edge_cap: int | None = None,
) -> float:
    """Finite-sensing ceiling on the asymptotic directional crossover proxy."""

    receipt = bounded_arity_spectral_ceiling(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        lambda_cost=lambda_cost,
        maximal_nontrivial_eigenvalue=maximal_nontrivial_eigenvalue,
        frontier_edge_cap=frontier_edge_cap,
    )
    mu = float(stationary_mean_selection_magnitude)
    if not isfinite(mu) or mu <= 0.0:
        raise ValueError(
            "stationary_mean_selection_magnitude must be finite and strictly positive"
        )
    return receipt.asymptotic_variance_upper_bound / (mu * mu)
