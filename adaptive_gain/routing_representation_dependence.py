"""Exact representation dependence for routing phase accessibility.

This side-theory module compares two genotype encodings of the same phenotype
levels g=0,...,q with the same fitness schedule W(g)=a**g.

1. branch-product encoding: x in {0,...,q}^{q+1}, g(x)=min_i x_i;
2. compressed gain-chain encoding: genotype r in {0,...,q}, g(r)=r.

The generic fact that genotype-phenotype representation affects evolution is
established prior art.  The purpose here is narrower: quantify exactly how the
same required-gap coordinate q produces different mutation distances and
stationary phase occupancy under two declared encodings.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .local_routing_mutation import minimum_local_prunings_for_gain
from .routing_origin_fixation import (
    full_phase_is_modal_layer,
    full_phase_modal_tilt_threshold,
    full_phase_stationary_mass_from_tilt,
    moran_fixation_probability,
    stationary_tilt,
)


def _validate_q(required_gap: int) -> int:
    if type(required_gap) is not int or required_gap < 1:
        raise ValueError("required_gap must be a positive integer")
    return required_gap


def _validate_gain(required_gap: int, realized_gain: int) -> tuple[int, int]:
    q = _validate_q(required_gap)
    r = realized_gain
    if type(r) is not int or not (0 <= r <= q):
        raise ValueError("realized_gain must be an integer in [0,q]")
    return q, r


def _as_positive_fraction(value: Fraction | int, name: str) -> Fraction:
    result = value if isinstance(value, Fraction) else Fraction(value, 1)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def compressed_gain_chain_distance(required_gap: int, realized_gain: int) -> int:
    """Shortest +/-1 gain-coordinate mutation distance from 0 to r."""

    _, r = _validate_gain(required_gap, realized_gain)
    return r


def branch_product_distance(required_gap: int, realized_gain: int) -> int:
    """Shortest one-coordinate routing distance from zero progress to gain r."""

    q, r = _validate_gain(required_gap, realized_gain)
    return minimum_local_prunings_for_gain(q + 1, r)


def accessibility_distance_inflation(required_gap: int, realized_gain: int) -> Fraction:
    """Exact branch-product / compressed distance ratio for r>=1."""

    q, r = _validate_gain(required_gap, realized_gain)
    if r == 0:
        raise ValueError("distance inflation is undefined at realized_gain=0")
    ratio = Fraction(branch_product_distance(q, r), compressed_gain_chain_distance(q, r))
    expected = Fraction(q + 1, 1)
    if ratio != expected:
        raise ArithmeticError("representation distance ratio changed unexpectedly")
    return ratio


def compressed_chain_transition_row(
    required_gap: int,
    resident_gain: int,
    population_size: int,
    fitness_step: Fraction | int,
) -> dict[int, Fraction]:
    """Exact origin-fixation row for the compressed gain-chain encoding.

    A +/-1 direction is proposed with probability 1/2. Boundary-invalid proposals
    and failed fixations contribute to the resident self-loop.
    """

    q, r = _validate_gain(required_gap, resident_gain)
    if type(population_size) is not int or population_size < 2:
        raise ValueError("population_size must be an integer at least 2")
    a = _as_positive_fraction(fitness_step, "fitness_step")
    if a < 1:
        raise ValueError("fitness_step must be at least one")

    proposal = Fraction(1, 2)
    row: dict[int, Fraction] = {r: Fraction(0, 1)}
    for direction in (-1, 1):
        mutant = r + direction
        if not 0 <= mutant <= q:
            row[r] += proposal
            continue
        relative = a ** (mutant - r)
        fixation = moran_fixation_probability(relative, population_size)
        row[mutant] = row.get(mutant, Fraction(0, 1)) + proposal * fixation
        row[r] += proposal * (1 - fixation)

    if sum(row.values(), Fraction(0, 1)) != 1:
        raise ArithmeticError("compressed chain transition row lost probability mass")
    return row


def compressed_stationary_distribution(
    required_gap: int,
    population_size: int,
    fitness_step: Fraction | int,
) -> tuple[Fraction, ...]:
    """Exact stationary law pi(r) proportional to theta**r."""

    q = _validate_q(required_gap)
    theta = stationary_tilt(population_size, fitness_step)
    weights = tuple(theta**r for r in range(q + 1))
    z = sum(weights, Fraction(0, 1))
    return tuple(weight / z for weight in weights)


def compressed_stationary_flow(
    required_gap: int,
    population_size: int,
    fitness_step: Fraction | int,
) -> tuple[Fraction, ...]:
    """Multiply the proposed compressed stationary law by its transition matrix."""

    q = _validate_q(required_gap)
    pi = compressed_stationary_distribution(q, population_size, fitness_step)
    out = [Fraction(0, 1) for _ in range(q + 1)]
    for r, mass in enumerate(pi):
        for target, probability in compressed_chain_transition_row(
            q, r, population_size, fitness_step
        ).items():
            out[target] += mass * probability
    return tuple(out)


def compressed_full_phase_mass_from_tilt(
    required_gap: int,
    theta: Fraction | int,
) -> Fraction:
    q = _validate_q(required_gap)
    tilt = _as_positive_fraction(theta, "theta")
    numerator = tilt**q
    denominator = sum((tilt**r for r in range(q + 1)), Fraction(0, 1))
    return numerator / denominator


def compressed_full_phase_is_modal(required_gap: int, theta: Fraction | int) -> bool:
    _validate_q(required_gap)
    tilt = _as_positive_fraction(theta, "theta")
    return tilt >= 1


def compressed_full_phase_is_unique_modal(required_gap: int, theta: Fraction | int) -> bool:
    _validate_q(required_gap)
    tilt = _as_positive_fraction(theta, "theta")
    return tilt > 1


def compressed_full_phase_half_mass_holds(
    required_gap: int,
    theta: Fraction | int,
) -> bool:
    return compressed_full_phase_mass_from_tilt(required_gap, theta) >= Fraction(1, 2)


def compressed_half_mass_polynomial(required_gap: int, theta: Fraction | int) -> Fraction:
    """Polynomial whose nontrivial zero gives the half-mass boundary for theta>1.

    For theta != 1, full mass=1/2 is equivalent to
        theta^(q+1) - 2 theta^q + 1 = 0.
    The direct mass predicate should be used at theta=1.
    """

    q = _validate_q(required_gap)
    tilt = _as_positive_fraction(theta, "theta")
    return tilt ** (q + 1) - 2 * tilt**q + 1


def compressed_modal_tilt_threshold(required_gap: int) -> int:
    _validate_q(required_gap)
    return 1


def modal_threshold_inflation(required_gap: int) -> int:
    q = _validate_q(required_gap)
    return full_phase_modal_tilt_threshold(q) // compressed_modal_tilt_threshold(q)


@dataclass(frozen=True)
class UniversalThetaTwoRepresentationWitness:
    required_gap: int
    branch_count: int
    theta: int
    compressed_full_distance: int
    product_full_distance: int
    distance_inflation: int
    compressed_full_mass: Fraction
    product_full_mass: Fraction
    compressed_unique_modal: bool
    product_modal: bool
    product_modal_threshold: int


def universal_theta_two_witness(required_gap: int) -> UniversalThetaTwoRepresentationWitness:
    """Exact all-q contradiction witness at the same phenotype fitness tilt theta=2."""

    q = _validate_q(required_gap)
    theta = 2
    compressed_mass = compressed_full_phase_mass_from_tilt(q, theta)
    expected_compressed_mass = Fraction(2**q, 2 ** (q + 1) - 1)
    if compressed_mass != expected_compressed_mass or compressed_mass <= Fraction(1, 2):
        raise ArithmeticError("compressed theta=2 majority identity failed")

    product_modal = full_phase_is_modal_layer(q, theta)
    product_threshold = full_phase_modal_tilt_threshold(q)
    if product_modal or not theta < product_threshold:
        raise ArithmeticError("branch-product theta=2 nonmodal witness failed")

    product_distance = branch_product_distance(q, q)
    compressed_distance = compressed_gain_chain_distance(q, q)
    if product_distance != (q + 1) * compressed_distance:
        raise ArithmeticError("full-gain representation distance comparison failed")

    return UniversalThetaTwoRepresentationWitness(
        required_gap=q,
        branch_count=q + 1,
        theta=theta,
        compressed_full_distance=compressed_distance,
        product_full_distance=product_distance,
        distance_inflation=q + 1,
        compressed_full_mass=compressed_mass,
        product_full_mass=full_phase_stationary_mass_from_tilt(q, theta),
        compressed_unique_modal=True,
        product_modal=False,
        product_modal_threshold=product_threshold,
    )
