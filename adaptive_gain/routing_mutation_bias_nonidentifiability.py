"""Fixed-support nonidentifiability from unspecified neutral mutation bias.

For a gain chain 0<->1<->...<->q with phenotype fitness tilt theta>0,
any strictly positive target stationary distribution p can be realized by a
reversible neutral mutation kernel on that same path support.  Choose neutral
mass mu_r proportional to p_r * theta^{-r}; then the selected origin-fixation
law pi_r proportional to mu_r * theta^r is exactly p_r.

The construction uses positive reversible edge conductances, so the support graph
is unchanged.  Thus q, phenotype fitness, and even the local mutation support do
not identify stationary phase occupancy without the neutral mutation measure.
This is an identifiability certificate, not a novelty claim for mutation bias or
reversible mutation-selection theory.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from .routing_reversible_certificate import (
    ReversibleMutationCertificate,
    selected_layer_distribution_from_tilt,
    shortest_support_distance_to_gain,
    validate_reversible_mutation_certificate,
)


def _as_fraction(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value, 1)


def normalize_positive_distribution(values: Iterable[Fraction | int]) -> tuple[Fraction, ...]:
    weights = tuple(_as_fraction(value) for value in values)
    if len(weights) < 2:
        raise ValueError("target distribution must contain at least two gain levels")
    if any(weight <= 0 for weight in weights):
        raise ValueError("target distribution weights must be strictly positive")
    total = sum(weights, Fraction(0, 1))
    return tuple(weight / total for weight in weights)


def neutral_measure_for_target_selected_distribution(
    target_distribution: Iterable[Fraction | int],
    theta: Fraction | int,
) -> tuple[Fraction, ...]:
    """Neutral measure mu_r proportional to p_r * theta^{-r}."""

    target = normalize_positive_distribution(target_distribution)
    tilt = _as_fraction(theta)
    if tilt <= 0:
        raise ValueError("theta must be positive")
    raw = tuple(target[r] / (tilt**r) for r in range(len(target)))
    total = sum(raw, Fraction(0, 1))
    return tuple(weight / total for weight in raw)


def reversible_path_certificate_for_target_distribution(
    target_distribution: Iterable[Fraction | int],
    theta: Fraction | int,
    *,
    edge_scale: Fraction | int = Fraction(1, 4),
) -> ReversibleMutationCertificate:
    """Construct a reversible path kernel whose selected law is the target.

    Let c_r = edge_scale * min(mu_r, mu_{r+1}) be the conductance on edge
    r<->r+1.  Then Q_{r,r+1}=c_r/mu_r and Q_{r+1,r}=c_r/mu_{r+1}.
    With 0<edge_scale<=1/2, every row has at most two off-diagonal terms, each at
    most edge_scale, so the diagonal remainder is nonnegative.
    """

    target = normalize_positive_distribution(target_distribution)
    tilt = _as_fraction(theta)
    if tilt <= 0:
        raise ValueError("theta must be positive")
    scale = _as_fraction(edge_scale)
    if not (0 < scale <= Fraction(1, 2)):
        raise ValueError("edge_scale must lie in (0,1/2]")

    mu = neutral_measure_for_target_selected_distribution(target, tilt)
    n = len(target)
    proposal = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for r in range(n - 1):
        conductance = scale * min(mu[r], mu[r + 1])
        proposal[r][r + 1] = conductance / mu[r]
        proposal[r + 1][r] = conductance / mu[r + 1]
    for r in range(n):
        off_diagonal = sum(proposal[r], Fraction(0, 1))
        proposal[r][r] = 1 - off_diagonal

    certificate = ReversibleMutationCertificate(
        gains=tuple(range(n)),
        proposal=tuple(tuple(row) for row in proposal),
        neutral_measure=mu,
        start_state=0,
    )
    certificate = validate_reversible_mutation_certificate(certificate)
    observed = selected_layer_distribution_from_tilt(certificate, tilt)
    if observed != target:
        raise ArithmeticError("constructed reversible path did not reproduce target selected law")
    return certificate


@dataclass(frozen=True)
class FixedSupportNonidentifiabilityReceipt:
    required_gap: int
    theta: Fraction
    target_a: tuple[Fraction, ...]
    target_b: tuple[Fraction, ...]
    neutral_measure_a: tuple[Fraction, ...]
    neutral_measure_b: tuple[Fraction, ...]
    support_distances_a: tuple[int, ...]
    support_distances_b: tuple[int, ...]
    full_mass_a: Fraction
    full_mass_b: Fraction


def fixed_support_nonidentifiability_receipt(
    target_a: Iterable[Fraction | int],
    target_b: Iterable[Fraction | int],
    theta: Fraction | int,
) -> FixedSupportNonidentifiabilityReceipt:
    """Two selected laws with identical gain path support and phenotype tilt."""

    a = normalize_positive_distribution(target_a)
    b = normalize_positive_distribution(target_b)
    if len(a) != len(b):
        raise ValueError("target distributions must have the same gain levels")
    tilt = _as_fraction(theta)
    if tilt <= 0:
        raise ValueError("theta must be positive")

    cert_a = reversible_path_certificate_for_target_distribution(a, tilt)
    cert_b = reversible_path_certificate_for_target_distribution(b, tilt)
    q = len(a) - 1
    distances_a = tuple(shortest_support_distance_to_gain(cert_a, r) for r in range(q + 1))
    distances_b = tuple(shortest_support_distance_to_gain(cert_b, r) for r in range(q + 1))
    expected_distances = tuple(range(q + 1))
    if distances_a != expected_distances or distances_b != expected_distances:
        raise ArithmeticError("path-support distance audit failed")

    return FixedSupportNonidentifiabilityReceipt(
        required_gap=q,
        theta=tilt,
        target_a=a,
        target_b=b,
        neutral_measure_a=cert_a.neutral_measure,
        neutral_measure_b=cert_b.neutral_measure,
        support_distances_a=distances_a,
        support_distances_b=distances_b,
        full_mass_a=a[q],
        full_mass_b=b[q],
    )
