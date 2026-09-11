"""Stationary phase nonidentifiability under fixed local gain-path support.

This stacked side-theory module sharpens the reversible representation
certificate.  It fixes all of the following:

* required gap q;
* one genotype for each gain level 0,...,q;
* the local path support 0 <-> 1 <-> ... <-> q;
* the phenotype fitness tilt theta.

Even after those declarations, neutral mutation bias can realize any strictly
positive rational selected stationary distribution.  The result is an
identifiability/no-go statement for the adaptive-gain extension.  Mutation bias
and reversible mutation-selection equilibria are established prior art.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .routing_reversible_certificate import (
    ReversibleMutationCertificate,
    selected_layer_distribution_from_tilt,
    selected_stationary_distribution,
    shortest_support_distance_to_gain,
    validate_reversible_mutation_certificate,
)


def _as_fraction(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value, 1)


def _validate_target_distribution(
    target_distribution: tuple[Fraction | int, ...],
) -> tuple[Fraction, ...]:
    if len(target_distribution) < 2:
        raise ValueError("target_distribution must contain at least two gain levels")
    target = tuple(_as_fraction(value) for value in target_distribution)
    if any(value <= 0 for value in target):
        raise ValueError("target_distribution entries must be strictly positive")
    if sum(target, Fraction(0, 1)) != 1:
        raise ValueError("target_distribution must sum exactly to one")
    return target


def _validate_theta(theta: Fraction | int) -> Fraction:
    tilt = _as_fraction(theta)
    if tilt < 1:
        raise ValueError("theta must be at least one")
    return tilt


def neutral_measure_for_target_stationary_distribution(
    target_distribution: tuple[Fraction | int, ...],
    theta: Fraction | int,
) -> tuple[Fraction, ...]:
    """Return normalized mu_r proportional to p_r * theta**(-r)."""

    target = _validate_target_distribution(target_distribution)
    tilt = _validate_theta(theta)
    raw = tuple(target[r] / tilt**r for r in range(len(target)))
    z = sum(raw, Fraction(0, 1))
    return tuple(value / z for value in raw)


def gain_path_certificate_for_target_stationary_distribution(
    target_distribution: tuple[Fraction | int, ...],
    theta: Fraction | int,
    *,
    edge_scale: Fraction | int = Fraction(1, 2),
) -> ReversibleMutationCertificate:
    """Construct a reversible local gain-path kernel selecting exactly target p.

    With neutral measure mu, put on every adjacent pair r,r+1

        Q[r,r+1] = eps * mu[r+1],
        Q[r+1,r] = eps * mu[r].

    Remaining probability is assigned to the diagonal.  eps<=1 guarantees
    nonnegative diagonals because the sum of neighboring neutral masses is at
    most one.  Strictly positive p gives strictly positive adjacent transitions,
    so the support is exactly the connected gain path.
    """

    target = _validate_target_distribution(target_distribution)
    tilt = _validate_theta(theta)
    eps = _as_fraction(edge_scale)
    if not 0 < eps <= 1:
        raise ValueError("edge_scale must lie in (0,1]")

    mu = neutral_measure_for_target_stationary_distribution(target, tilt)
    n = len(target)
    rows = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]

    for r in range(n - 1):
        rows[r][r + 1] = eps * mu[r + 1]
        rows[r + 1][r] = eps * mu[r]

    for r in range(n):
        off_diagonal = sum(rows[r], Fraction(0, 1))
        rows[r][r] = 1 - off_diagonal
        if rows[r][r] < 0:
            raise ArithmeticError("constructed gain-path proposal had a negative self-loop")

    certificate = ReversibleMutationCertificate(
        gains=tuple(range(n)),
        proposal=tuple(tuple(row) for row in rows),
        neutral_measure=mu,
        start_state=0,
    )
    cert = validate_reversible_mutation_certificate(certificate)

    observed = selected_layer_distribution_from_tilt(cert, tilt)
    if observed != target:
        raise ArithmeticError("constructed certificate did not recover target stationary distribution")
    return cert


def gain_path_support_is_exact(certificate: ReversibleMutationCertificate) -> bool:
    """Whether positive off-diagonal support is exactly adjacent gain levels."""

    cert = validate_reversible_mutation_certificate(certificate)
    n = cert.state_count
    if cert.gains != tuple(range(n)):
        return False
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            positive = cert.proposal[i][j] > 0
            if positive != (abs(i - j) == 1):
                return False
    return True


@dataclass(frozen=True)
class StationaryNonidentifiabilityReceipt:
    required_gap: int
    theta: Fraction
    target_distribution: tuple[Fraction, ...]
    neutral_measure: tuple[Fraction, ...]
    shortest_full_phase_distance: int
    support_is_local_gain_path: bool
    exact_selected_stationary_verified: bool


def stationary_nonidentifiability_receipt(
    target_distribution: tuple[Fraction | int, ...],
    theta: Fraction | int,
) -> StationaryNonidentifiabilityReceipt:
    target = _validate_target_distribution(target_distribution)
    tilt = _validate_theta(theta)
    cert = gain_path_certificate_for_target_stationary_distribution(target, tilt)

    # N=2 and per-gain fitness multiplier a=theta give selected tilt exactly theta.
    selected = selected_stationary_distribution(cert, population_size=2, fitness_step=tilt)
    support_ok = gain_path_support_is_exact(cert)
    distance = shortest_support_distance_to_gain(cert, len(target) - 1)
    verified = selected == target and support_ok and distance == len(target) - 1
    if not verified:
        raise ArithmeticError("stationary nonidentifiability construction audit failed")

    return StationaryNonidentifiabilityReceipt(
        required_gap=len(target) - 1,
        theta=tilt,
        target_distribution=target,
        neutral_measure=cert.neutral_measure,
        shortest_full_phase_distance=distance,
        support_is_local_gain_path=True,
        exact_selected_stationary_verified=True,
    )


@dataclass(frozen=True)
class CanonicalQ2MutationBiasContradiction:
    theta: Fraction
    full_favored_distribution: tuple[Fraction, ...]
    full_disfavored_distribution: tuple[Fraction, ...]
    full_favored_mass: Fraction
    full_disfavored_mass: Fraction
    shortest_full_phase_distance_both: int


def canonical_q2_mutation_bias_contradiction() -> CanonicalQ2MutationBiasContradiction:
    """Same q=2, path support and theta=2; opposite full-phase conclusions."""

    theta = Fraction(2, 1)
    favored = (Fraction(1, 10), Fraction(1, 5), Fraction(7, 10))
    disfavored = (Fraction(7, 10), Fraction(1, 5), Fraction(1, 10))
    favored_receipt = stationary_nonidentifiability_receipt(favored, theta)
    disfavored_receipt = stationary_nonidentifiability_receipt(disfavored, theta)

    if favored_receipt.shortest_full_phase_distance != 2 or disfavored_receipt.shortest_full_phase_distance != 2:
        raise ArithmeticError("canonical gain-path distances changed unexpectedly")
    if not favored[2] > Fraction(1, 2):
        raise ArithmeticError("favored witness did not make full phase a majority")
    if not disfavored[2] < max(disfavored[:2]):
        raise ArithmeticError("disfavored witness did not make full phase nonmodal")

    return CanonicalQ2MutationBiasContradiction(
        theta=theta,
        full_favored_distribution=favored,
        full_disfavored_distribution=disfavored,
        full_favored_mass=favored[2],
        full_disfavored_mass=disfavored[2],
        shortest_full_phase_distance_both=2,
    )
