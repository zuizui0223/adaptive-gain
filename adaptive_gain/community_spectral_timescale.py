"""Long-timescale coefficients for finite community Markov selection.

For a stationary finite-state Markov chain with transition matrix P,
stationary distribution pi, and state-specific selection reward s, write

    mu = E_pi[s],
    c  = s - mu.

When the Poisson equation

    (I - P + Pi) h = c

is nonsingular (Pi has every row equal to pi), the long-run variance rate of
cumulative centered selection is

    sigma_eff^2 = 2 <c,h>_pi - <c,c>_pi.

Equivalently, when the stationary covariance series is summable,

    sigma_eff^2 = gamma(0) + 2 sum_{k>=1} gamma(k).

This gives two cross-timescale quantities used by the evolutionary branch:

* if mu=0, expected absolute selection activity grows as H*a while RMS net
  selection grows as sqrt(H)*sigma_eff, so the RMS retained fraction is
  asymptotically (sigma_eff/a) H^{-1/2};
* if mu!=0, the directional mean H*mu overtakes the fluctuation SD near
  H_x ~= sigma_eff^2 / mu^2.

For a reversible chain with centered reward expanded in orthogonal eigenmodes,
this same coefficient is

    sigma_eff^2 = sum_r w_r * (1+lambda_r)/(1-lambda_r),

where w_r is the reward variance carried by mode r.  Thus slow community modes
matter only to the extent that structural selection projects onto them.

The probability identities are standard Markov-reward theory.  Their role here
is to connect the repository's state-specific adaptive/fixed structural rewards
to a general finite-community evolutionary timescale.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf, isfinite, sqrt
from typing import Sequence

from .community_markov_selection import (
    stationary_mean_absolute_selection,
    stationary_mean_selection,
)

_TOL = 1e-10


def _validate_basic(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    rewards: Sequence[float],
) -> tuple[tuple[float, ...], tuple[tuple[float, ...], ...], tuple[float, ...]]:
    pi = tuple(float(x) for x in stationary)
    P = tuple(tuple(float(x) for x in row) for row in transition)
    s = tuple(float(x) for x in rewards)
    n = len(pi)
    if n == 0:
        raise ValueError("stationary distribution must be non-empty")
    if len(P) != n or any(len(row) != n for row in P):
        raise ValueError("transition matrix must be square and match stationary length")
    if len(s) != n:
        raise ValueError("reward vector must match stationary length")
    if any(not isfinite(x) or x < -_TOL or x > 1.0 + _TOL for x in pi):
        raise ValueError("stationary probabilities must lie in [0,1]")
    if abs(sum(pi) - 1.0) > _TOL:
        raise ValueError("stationary probabilities must sum to one")
    for row in P:
        if any(not isfinite(x) or x < -_TOL or x > 1.0 + _TOL for x in row):
            raise ValueError("transition probabilities must lie in [0,1]")
        if abs(sum(row) - 1.0) > _TOL:
            raise ValueError("every transition row must sum to one")
    if any(not isfinite(x) for x in s):
        raise ValueError("selection rewards must be finite")
    for j in range(n):
        incoming = sum(pi[i] * P[i][j] for i in range(n))
        if abs(incoming - pi[j]) > _TOL:
            raise ValueError("supplied stationary distribution is not stationary for transition matrix")
    return pi, P, s


def _solve_linear_system(
    matrix: Sequence[Sequence[float]], rhs: Sequence[float]
) -> tuple[float, ...]:
    """Solve Ax=b by partial-pivot Gaussian elimination.

    The state spaces used in this repository are small.  Keeping this solver
    local avoids adding a numerical linear-algebra dependency solely for the
    Poisson equation.
    """

    A = [list(map(float, row)) for row in matrix]
    b = list(map(float, rhs))
    n = len(A)
    if n == 0 or len(b) != n or any(len(row) != n for row in A):
        raise ValueError("linear system must be non-empty and square")

    scale = max((abs(x) for row in A for x in row), default=1.0)
    pivot_tol = max(1e-14, 1e-12 * scale)

    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(A[r][col]))
        if abs(A[pivot][col]) <= pivot_tol:
            raise ValueError(
                "Poisson system is singular or numerically unresolved; "
                "the supplied chain may have multiple closed classes"
            )
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            b[col], b[pivot] = b[pivot], b[col]

        pivot_value = A[col][col]
        for j in range(col, n):
            A[col][j] /= pivot_value
        b[col] /= pivot_value

        for row in range(n):
            if row == col:
                continue
            factor = A[row][col]
            if abs(factor) <= pivot_tol:
                continue
            for j in range(col, n):
                A[row][j] -= factor * A[col][j]
            b[row] -= factor * b[col]

    return tuple(b)


def centered_rewards(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    rewards: Sequence[float],
) -> tuple[float, ...]:
    pi, P, s = _validate_basic(stationary, transition, rewards)
    mu = stationary_mean_selection(pi, P, s)
    return tuple(x - mu for x in s)


def poisson_solution(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    rewards: Sequence[float],
) -> tuple[float, ...]:
    """Solve (I-P+Pi)h = s-E_pi[s]."""

    pi, P, s = _validate_basic(stationary, transition, rewards)
    n = len(pi)
    mu = sum(pi[i] * s[i] for i in range(n))
    c = tuple(s[i] - mu for i in range(n))
    matrix = tuple(
        tuple(
            (1.0 if i == j else 0.0) - P[i][j] + pi[j]
            for j in range(n)
        )
        for i in range(n)
    )
    h = _solve_linear_system(matrix, c)
    residual = max(
        abs(
            sum(matrix[i][j] * h[j] for j in range(n)) - c[i]
        )
        for i in range(n)
    )
    if residual > 1e-8:
        raise ArithmeticError("Poisson equation residual exceeded tolerance")
    return h


def asymptotic_variance_rate(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    rewards: Sequence[float],
) -> float:
    """Long-run variance per generation of cumulative centered selection."""

    pi, P, s = _validate_basic(stationary, transition, rewards)
    mu = sum(pi[i] * s[i] for i in range(len(pi)))
    c = tuple(x - mu for x in s)
    h = poisson_solution(pi, P, s)
    inner_ch = sum(pi[i] * c[i] * h[i] for i in range(len(pi)))
    variance = sum(pi[i] * c[i] * c[i] for i in range(len(pi)))
    value = 2.0 * inner_ch - variance
    if value < 0.0 and abs(value) < 1e-8:
        value = 0.0
    if value < 0.0:
        raise ArithmeticError("Poisson formula produced negative asymptotic variance")
    return value


def zero_mean_retention_prefactor(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    rewards: Sequence[float],
) -> float:
    """Coefficient K in RMS retention ~= K / sqrt(H), requiring mean selection zero."""

    pi, P, s = _validate_basic(stationary, transition, rewards)
    mu = stationary_mean_selection(pi, P, s)
    if abs(mu) > 1e-9:
        raise ValueError("zero_mean_retention_prefactor requires stationary mean selection zero")
    activity = stationary_mean_absolute_selection(pi, P, s)
    if activity <= _TOL:
        return 0.0
    return sqrt(asymptotic_variance_rate(pi, P, s)) / activity


def directional_crossover_horizon(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    rewards: Sequence[float],
) -> float:
    """Asymptotic H where |H*mu| ~= sqrt(H*sigma_eff^2)."""

    pi, P, s = _validate_basic(stationary, transition, rewards)
    mu = stationary_mean_selection(pi, P, s)
    if abs(mu) <= _TOL:
        return inf
    sigma2 = asymptotic_variance_rate(pi, P, s)
    if sigma2 <= _TOL:
        return 0.0
    return sigma2 / (mu * mu)


@dataclass(frozen=True)
class CommunitySpectralTimescaleSummary:
    state_count: int
    stationary_mean_selection: float
    stationary_mean_absolute_selection: float
    asymptotic_variance_rate: float
    zero_mean_retention_prefactor: float | None
    directional_crossover_horizon: float
    poisson_solution: tuple[float, ...]


def summarize_community_timescale(
    stationary: Sequence[float],
    transition: Sequence[Sequence[float]],
    rewards: Sequence[float],
) -> CommunitySpectralTimescaleSummary:
    pi, P, s = _validate_basic(stationary, transition, rewards)
    mu = stationary_mean_selection(pi, P, s)
    activity = stationary_mean_absolute_selection(pi, P, s)
    sigma2 = asymptotic_variance_rate(pi, P, s)
    prefactor = None
    if abs(mu) <= 1e-9:
        prefactor = sqrt(sigma2) / activity if activity > _TOL else 0.0
    crossover = inf if abs(mu) <= _TOL else (sigma2 / (mu * mu) if sigma2 > _TOL else 0.0)
    return CommunitySpectralTimescaleSummary(
        state_count=len(pi),
        stationary_mean_selection=mu,
        stationary_mean_absolute_selection=activity,
        asymptotic_variance_rate=sigma2,
        zero_mean_retention_prefactor=prefactor,
        directional_crossover_horizon=crossover,
        poisson_solution=poisson_solution(pi, P, s),
    )
