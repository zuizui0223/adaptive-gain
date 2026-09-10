"""State-independent maintenance cost separates trend from fluctuations.

Let each community state i carry an exact structural gap

    g_i = C_F(i) - C_A(i),

and map it to log-fitness selection

    s_i = lambda_cost * g_i - control_cost.

For a stationary community Markov chain, subtracting one state-independent
control cost shifts the stationary mean selection but leaves centered rewards
unchanged:

    s_i - E_pi[s] = lambda_cost * (g_i - E_pi[g]).

Therefore the complete covariance sequence and the Poisson asymptotic variance
are independent of ``control_cost``.  The critical constitutive cost

    kappa_star = lambda_cost * E_pi[g]

centers long-run selection exactly while preserving all state-dependent
fluctuation geometry.  Near that threshold the general crossover horizon obeys

    H_x ~= sigma_eff^2 / (kappa - kappa_star)^2.

This module makes that algebra executable using the repository's existing exact
finite sensing tasks.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf, isfinite
from typing import Sequence

from .community_markov_selection import (
    stationary_mean_selection,
    structural_rewards_from_tasks,
)
from .community_spectral_timescale import asymptotic_variance_rate
from .core import FiniteTask, adaptive_gain_receipt


def structural_gaps(tasks: Sequence[FiniteTask]) -> tuple[int, ...]:
    """Return exact C_F-C_A for each resolvable community-state task."""

    if not tasks:
        raise ValueError("tasks must be non-empty")
    gaps = []
    for task in tasks:
        receipt = adaptive_gain_receipt(task)
        if receipt.adaptive_cost is None or receipt.fixed_cost is None:
            raise ValueError("all tasks must be resolvable")
        gaps.append(receipt.fixed_cost - receipt.adaptive_cost)
    return tuple(gaps)


def critical_control_cost(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    tasks: Sequence[FiniteTask],
    *,
    lambda_cost: float = 1.0,
) -> float:
    """State-independent control cost that makes stationary mean selection zero."""

    lam = float(lambda_cost)
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    raw = structural_rewards_from_tasks(
        tasks,
        lambda_cost=lam,
        control_cost=0.0,
    )
    return stationary_mean_selection(stationary, transition, raw)


def structural_selection_rewards(
    tasks: Sequence[FiniteTask],
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
) -> tuple[float, ...]:
    """Convenience wrapper returning lambda*(C_F-C_A)-kappa for each state."""

    return structural_rewards_from_tasks(
        tasks,
        lambda_cost=lambda_cost,
        control_cost=control_cost,
    )


def control_invariant_asymptotic_variance(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    tasks: Sequence[FiniteTask],
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
) -> float:
    """Asymptotic variance of structural selection after any common cost shift."""

    rewards = structural_selection_rewards(
        tasks,
        lambda_cost=lambda_cost,
        control_cost=control_cost,
    )
    return asymptotic_variance_rate(stationary, transition, rewards)


def centered_structural_crossover_horizon(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    tasks: Sequence[FiniteTask],
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
) -> float:
    """General long-horizon mean-vs-fluctuation crossover for structural rewards."""

    rewards = structural_selection_rewards(
        tasks,
        lambda_cost=lambda_cost,
        control_cost=control_cost,
    )
    mean = stationary_mean_selection(stationary, transition, rewards)
    if abs(mean) <= 1e-12:
        return inf
    sigma2 = asymptotic_variance_rate(stationary, transition, rewards)
    if sigma2 <= 1e-12:
        return 0.0
    return sigma2 / (mean * mean)


@dataclass(frozen=True)
class StructuralMarkovCenteringSummary:
    state_count: int
    structural_gaps: tuple[int, ...]
    lambda_cost: float
    control_cost: float
    critical_control_cost: float
    stationary_mean_selection: float
    asymptotic_variance_rate: float
    crossover_horizon: float
    variance_invariance_error: float


def summarize_structural_centering(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    tasks: Sequence[FiniteTask],
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
) -> StructuralMarkovCenteringSummary:
    if not tasks:
        raise ValueError("tasks must be non-empty")
    lam = float(lambda_cost)
    kappa = float(control_cost)
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    if not isfinite(kappa) or kappa < 0.0:
        raise ValueError("control_cost must be finite and non-negative")

    raw = structural_selection_rewards(tasks, lambda_cost=lam, control_cost=0.0)
    shifted = structural_selection_rewards(tasks, lambda_cost=lam, control_cost=kappa)
    critical = stationary_mean_selection(stationary, transition, raw)
    mean = stationary_mean_selection(stationary, transition, shifted)
    sigma_raw = asymptotic_variance_rate(stationary, transition, raw)
    sigma_shifted = asymptotic_variance_rate(stationary, transition, shifted)
    error = abs(sigma_raw - sigma_shifted)
    if error > 1e-8:
        raise ArithmeticError("state-independent control cost changed centered asymptotic variance")
    crossover = inf if abs(mean) <= 1e-12 else (sigma_shifted / (mean * mean) if sigma_shifted > 1e-12 else 0.0)
    return StructuralMarkovCenteringSummary(
        state_count=len(tasks),
        structural_gaps=structural_gaps(tasks),
        lambda_cost=lam,
        control_cost=kappa,
        critical_control_cost=critical,
        stationary_mean_selection=mean,
        asymptotic_variance_rate=sigma_shifted,
        crossover_horizon=crossover,
        variance_invariance_error=error,
    )
