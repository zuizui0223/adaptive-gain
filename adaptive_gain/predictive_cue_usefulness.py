"""General predictive cue-usefulness calculations for contingent sensing.

This module separates the temporal routing result from the special symmetric
binary parameter ``rho``.  A current context ``i`` has prior mass ``pi[i]`` and
induces a distribution ``K[i][j]`` over which downstream specialist ``j`` will
be useful at the later sensing step.

For a fair binary target and a branch-diagnostic specialist abstraction, the
best fixed and contingent accuracies are

    A_F = 1/2 + 1/2 max_j sum_i pi_i K_ij
    A_A = 1/2 + 1/2 sum_i pi_i max_j K_ij

so the contingent routing gain is one half of the Jensen gap of ``max``.

For two future branches this also gives the exact arbitrary-transition-kernel
extension of the repository's original q_left/q_right normal form.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Iterable, Sequence


_TOL = 1e-12


def _as_prob_vector(values: Iterable[float], *, name: str) -> tuple[float, ...]:
    out = tuple(float(x) for x in values)
    if not out:
        raise ValueError(f"{name} must be non-empty")
    if any(x < -_TOL or x > 1.0 + _TOL for x in out):
        raise ValueError(f"{name} entries must lie in [0, 1]")
    if not isclose(sum(out), 1.0, abs_tol=_TOL, rel_tol=0.0):
        raise ValueError(f"{name} must sum to 1")
    return out


def _as_kernel(rows: Iterable[Iterable[float]]) -> tuple[tuple[float, ...], ...]:
    kernel = tuple(tuple(float(x) for x in row) for row in rows)
    if not kernel:
        raise ValueError("kernel must contain at least one current-context row")
    width = len(kernel[0])
    if width == 0:
        raise ValueError("kernel rows must be non-empty")
    for row in kernel:
        if len(row) != width:
            raise ValueError("kernel must be rectangular")
        if any(x < -_TOL or x > 1.0 + _TOL for x in row):
            raise ValueError("kernel entries must lie in [0, 1]")
        if not isclose(sum(row), 1.0, abs_tol=_TOL, rel_tol=0.0):
            raise ValueError("each kernel row must sum to 1")
    return kernel


def validate_model(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> tuple[tuple[float, ...], tuple[tuple[float, ...], ...]]:
    """Validate and canonicalize a current-context prior and transition kernel."""

    pi = _as_prob_vector(prior, name="prior")
    K = _as_kernel(kernel)
    if len(pi) != len(K):
        raise ValueError("prior length must equal the number of kernel rows")
    return pi, K


def future_specialist_marginal(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> tuple[float, ...]:
    """Return the marginal probability that each future specialist is useful."""

    pi, K = validate_model(prior, kernel)
    m = len(K[0])
    return tuple(sum(pi[i] * K[i][j] for i in range(len(pi))) for j in range(m))


def optimal_fixed_specialist(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> int:
    """Return the smallest-index Bayes-optimal fixed specialist."""

    marginal = future_specialist_marginal(prior, kernel)
    return max(range(len(marginal)), key=lambda j: (marginal[j], -j))


def optimal_adaptive_policy(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> tuple[int, ...]:
    """Return the smallest-index row-wise optimal specialist for each context."""

    _, K = validate_model(prior, kernel)
    return tuple(max(range(len(row)), key=lambda j: (row[j], -j)) for row in K)


def best_fixed_usefulness_probability(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> float:
    """Probability that the best single fixed specialist matches the future branch."""

    return max(future_specialist_marginal(prior, kernel))


def best_adaptive_usefulness_probability(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> float:
    """Probability that a context-contingent specialist matches the future branch."""

    pi, K = validate_model(prior, kernel)
    return sum(pi[i] * max(K[i]) for i in range(len(pi)))


def fixed_accuracy(prior: Sequence[float], kernel: Sequence[Sequence[float]]) -> float:
    """Best fixed target accuracy in the branch-diagnostic two-step model."""

    return 0.5 + 0.5 * best_fixed_usefulness_probability(prior, kernel)


def adaptive_accuracy(prior: Sequence[float], kernel: Sequence[Sequence[float]]) -> float:
    """Best contingent target accuracy in the branch-diagnostic two-step model."""

    return 0.5 + 0.5 * best_adaptive_usefulness_probability(prior, kernel)


def routing_gain(prior: Sequence[float], kernel: Sequence[Sequence[float]]) -> float:
    """Exact contingent-minus-fixed accuracy gain.

    This is one half of the Jensen gap

        E[max_j K(j|C0)] - max_j E[K(j|C0)].
    """

    return adaptive_accuracy(prior, kernel) - fixed_accuracy(prior, kernel)


def common_optimal_specialists(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> tuple[int, ...]:
    """Specialists that are row-wise optimal for every positive-prior context.

    The routing gain is zero exactly when this tuple is non-empty.
    """

    pi, K = validate_model(prior, kernel)
    positive_rows = [K[i] for i, mass in enumerate(pi) if mass > _TOL]
    if not positive_rows:
        raise ValueError("prior must place positive mass somewhere")
    common = set(range(len(K[0])))
    for row in positive_rows:
        row_max = max(row)
        common &= {j for j, value in enumerate(row) if isclose(value, row_max, abs_tol=_TOL, rel_tol=0.0)}
    return tuple(sorted(common))


def has_strict_routing_gain(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> bool:
    """Whether current context changes which future specialist should be used."""

    return not common_optimal_specialists(prior, kernel)


def binary_signed_advantages(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> tuple[float, ...]:
    """Return d_i = K(0|i)-K(1|i) for a two-specialist kernel."""

    _, K = validate_model(prior, kernel)
    if len(K[0]) != 2:
        raise ValueError("binary_signed_advantages requires exactly two specialists")
    return tuple(row[0] - row[1] for row in K)


def binary_jensen_gap_formula(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> float:
    """Binary closed form: 1/4(E|d| - |E d|)."""

    pi, K = validate_model(prior, kernel)
    if len(K[0]) != 2:
        raise ValueError("binary_jensen_gap_formula requires exactly two specialists")
    d = tuple(row[0] - row[1] for row in K)
    return 0.25 * (sum(pi[i] * abs(d[i]) for i in range(len(pi))) - abs(sum(pi[i] * d[i] for i in range(len(pi)))))


def symmetric_binary_gain(rho: float) -> float:
    """Recover |2*rho-1|/4 from the symmetric two-context kernel."""

    rho = float(rho)
    if rho < 0.0 or rho > 1.0:
        raise ValueError("rho must lie in [0, 1]")
    prior = (0.5, 0.5)
    kernel = ((rho, 1.0 - rho), (1.0 - rho, rho))
    return routing_gain(prior, kernel)


@dataclass(frozen=True)
class PredictiveRoutingSummary:
    fixed_accuracy: float
    adaptive_accuracy: float
    gain: float
    future_marginal: tuple[float, ...]
    fixed_specialist: int
    adaptive_policy: tuple[int, ...]
    common_optima: tuple[int, ...]


def summarize(
    prior: Sequence[float], kernel: Sequence[Sequence[float]]
) -> PredictiveRoutingSummary:
    """Collect the main theorem quantities for auditing and examples."""

    return PredictiveRoutingSummary(
        fixed_accuracy=fixed_accuracy(prior, kernel),
        adaptive_accuracy=adaptive_accuracy(prior, kernel),
        gain=routing_gain(prior, kernel),
        future_marginal=future_specialist_marginal(prior, kernel),
        fixed_specialist=optimal_fixed_specialist(prior, kernel),
        adaptive_policy=optimal_adaptive_policy(prior, kernel),
        common_optima=common_optimal_specialists(prior, kernel),
    )
