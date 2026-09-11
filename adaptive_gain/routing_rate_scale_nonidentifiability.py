"""Absolute mutation/proposal-rate scale nonidentifiability.

This stacked side-theory module builds on the fixed-support stationary
nonidentifiability construction.  Holding required gap, gain map, support graph,
neutral mutation measure and selected stationary distribution fixed, a common
proposal-rate scale epsilon changes waiting times without changing stationary
proportions or shortest support distance.

For the selected origin-fixation transition matrix,

    P_epsilon = (1-epsilon) I + epsilon P_1.

Hence expected hitting times in proposal attempts scale exactly as 1/epsilon.
This is standard Markov-chain laziness/time-change mathematics and is used only
as an identifiability boundary for the adaptive-gain downstream extension.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .routing_reversible_certificate import (
    selected_origin_fixation_transition_row,
    selected_stationary_distribution,
    shortest_support_distance_to_gain,
)
from .routing_stationary_nonidentifiability import (
    gain_path_certificate_for_target_stationary_distribution,
)


def _as_fraction(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value, 1)


def _validate_scale(edge_scale: Fraction | int) -> Fraction:
    eps = _as_fraction(edge_scale)
    if not 0 < eps <= 1:
        raise ValueError("edge_scale must lie in (0,1]")
    return eps


def selected_transition_matrix(
    target_distribution: tuple[Fraction | int, ...],
    theta: Fraction | int,
    *,
    edge_scale: Fraction | int,
) -> tuple[tuple[Fraction, ...], ...]:
    """Exact selected origin-fixation matrix at one proposal scale.

    N=2 and fitness_step=theta are used so the selected tilt is exactly theta.
    """

    eps = _validate_scale(edge_scale)
    tilt = _as_fraction(theta)
    cert = gain_path_certificate_for_target_stationary_distribution(
        target_distribution,
        tilt,
        edge_scale=eps,
    )
    return tuple(
        selected_origin_fixation_transition_row(
            cert,
            resident_state=i,
            population_size=2,
            fitness_step=tilt,
        )
        for i in range(cert.state_count)
    )


def lazy_scaled_matrix_identity_holds(
    target_distribution: tuple[Fraction | int, ...],
    theta: Fraction | int,
    edge_scale: Fraction | int,
) -> bool:
    """Check P_eps=(1-eps)I+eps P_1 exactly."""

    eps = _validate_scale(edge_scale)
    p_eps = selected_transition_matrix(
        target_distribution,
        theta,
        edge_scale=eps,
    )
    p_one = selected_transition_matrix(
        target_distribution,
        theta,
        edge_scale=1,
    )
    n = len(p_one)
    for i in range(n):
        for j in range(n):
            expected = eps * p_one[i][j]
            if i == j:
                expected += 1 - eps
            if p_eps[i][j] != expected:
                return False
    return True


def _solve_fraction_linear_system(
    matrix: list[list[Fraction]],
    rhs: list[Fraction],
) -> tuple[Fraction, ...]:
    """Exact Gauss-Jordan solve for a nonsingular square Fraction system."""

    n = len(matrix)
    if n == 0 or len(rhs) != n or any(len(row) != n for row in matrix):
        raise ValueError("linear system must be nonempty and square")
    aug = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if aug[row][col] != 0), None)
        if pivot is None:
            raise ArithmeticError("hitting-time linear system was singular")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor == 0:
                continue
            aug[row] = [
                aug[row][j] - factor * aug[col][j]
                for j in range(n + 1)
            ]
    return tuple(aug[i][n] for i in range(n))


def expected_full_phase_hitting_attempts(
    target_distribution: tuple[Fraction | int, ...],
    theta: Fraction | int,
    *,
    edge_scale: Fraction | int,
) -> Fraction:
    """Expected proposal attempts from gain 0 to the full gain state."""

    p = selected_transition_matrix(
        target_distribution,
        theta,
        edge_scale=edge_scale,
    )
    n = len(p)
    transient = n - 1
    matrix = [
        [
            (Fraction(1, 1) if i == j else Fraction(0, 1)) - p[i][j]
            for j in range(transient)
        ]
        for i in range(transient)
    ]
    rhs = [Fraction(1, 1) for _ in range(transient)]
    solution = _solve_fraction_linear_system(matrix, rhs)
    return solution[0]


@dataclass(frozen=True)
class RateScaleNonidentifiabilityReceipt:
    required_gap: int
    theta: Fraction
    edge_scale: Fraction
    shortest_full_phase_distance: int
    stationary_distribution: tuple[Fraction, ...]
    baseline_expected_attempts: Fraction
    scaled_expected_attempts: Fraction
    timing_inflation: Fraction
    lazy_matrix_identity_verified: bool


def rate_scale_nonidentifiability_receipt(
    target_distribution: tuple[Fraction | int, ...],
    theta: Fraction | int,
    edge_scale: Fraction | int,
) -> RateScaleNonidentifiabilityReceipt:
    eps = _validate_scale(edge_scale)
    tilt = _as_fraction(theta)
    cert = gain_path_certificate_for_target_stationary_distribution(
        target_distribution,
        tilt,
        edge_scale=eps,
    )
    baseline = expected_full_phase_hitting_attempts(
        target_distribution,
        tilt,
        edge_scale=1,
    )
    scaled = expected_full_phase_hitting_attempts(
        target_distribution,
        tilt,
        edge_scale=eps,
    )
    if scaled != baseline / eps:
        raise ArithmeticError("expected hitting time did not scale as 1/edge_scale")
    identity = lazy_scaled_matrix_identity_holds(
        target_distribution,
        tilt,
        eps,
    )
    if not identity:
        raise ArithmeticError("selected transition matrix did not obey lazy scaling identity")

    stationary = selected_stationary_distribution(
        cert,
        population_size=2,
        fitness_step=tilt,
    )
    distance = shortest_support_distance_to_gain(cert, cert.required_gap)
    return RateScaleNonidentifiabilityReceipt(
        required_gap=cert.required_gap,
        theta=tilt,
        edge_scale=eps,
        shortest_full_phase_distance=distance,
        stationary_distribution=stationary,
        baseline_expected_attempts=baseline,
        scaled_expected_attempts=scaled,
        timing_inflation=Fraction(1, 1) / eps,
        lazy_matrix_identity_verified=True,
    )
