"""Finite-population origin-fixation selection on routing genotypes.

This side-theory module declares a monomorphic strong-selection/weak-mutation
(origin-fixation) process on the exact routing genotype space built in the local
routing side line.  It does not modify the frozen submission.

For required gap q, there are k=q+1 routing branches and a genotype is a vector
x in {0,...,q}^k of branch-local pruning progress.  Its realized routing gain is

    g(x) = min_i x_i.

A local mutation changes one coordinate by +/-1.  Mutation proposals are
symmetric; invalid boundary directions are null proposals.  A proposed mutant
then fixes according to the classical well-mixed Moran fixation probability.
Fitness is multiplicative per realized gain level,

    W(x) = a**g(x),

where a>=1 is the fitness multiplier for one unit of realized routing gain.

With population size N, the origin-fixation chain is reversible and has exact
stationary genotype weights proportional to

    a**((N-1)*g(x)).

The broad Boltzmann/free-fitness structure is established prior art.  The module
uses it only to expose the exact gain-layer multiplicities induced by the
required-gap routing family.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import prod
from typing import Iterable

from ._exact_rational import as_exact_fraction


RoutingGenotype = tuple[int, ...]


class RoutingStationaryStateLimitError(RuntimeError):
    """Raised when exact genotype enumeration exceeds a declared state cap."""


def _validate_q(required_gap: int) -> int:
    q = required_gap
    if type(q) is not int or q < 1:
        raise ValueError("required_gap must be a positive integer")
    return q


def _validate_population_size(population_size: int) -> int:
    n = population_size
    if type(n) is not int or n < 2:
        raise ValueError("population_size must be an integer at least 2")
    return n


def _as_fraction(value: Fraction | int) -> Fraction:
    result = as_exact_fraction(value, name="fitness_step")
    if result < 1:
        raise ValueError("fitness_step must be at least one in this directional-selection model")
    return result


def routing_branch_count(required_gap: int) -> int:
    return _validate_q(required_gap) + 1


def routing_genotype_count(required_gap: int) -> int:
    q = _validate_q(required_gap)
    k = q + 1
    return (q + 1) ** k


def routing_genotypes(required_gap: int) -> Iterable[RoutingGenotype]:
    q = _validate_q(required_gap)
    k = q + 1
    return product(range(q + 1), repeat=k)


def validate_routing_genotype(required_gap: int, genotype: RoutingGenotype) -> RoutingGenotype:
    q = _validate_q(required_gap)
    k = q + 1
    if len(genotype) != k:
        raise ValueError("routing genotype must contain q+1 branch coordinates")
    if any(type(value) is not int or not (0 <= value <= q) for value in genotype):
        raise ValueError("routing progress coordinates must be integers in [0,q]")
    return genotype


def routing_realized_gain(required_gap: int, genotype: RoutingGenotype) -> int:
    validate_routing_genotype(required_gap, genotype)
    return min(genotype)


def routing_fitness(
    required_gap: int,
    genotype: RoutingGenotype,
    fitness_step: Fraction | int,
) -> Fraction:
    a = _as_fraction(fitness_step)
    return a ** routing_realized_gain(required_gap, genotype)


def moran_fixation_probability(
    relative_fitness: Fraction | int,
    population_size: int,
) -> Fraction:
    """Fixation probability of one mutant in a well-mixed Moran population.

    For relative mutant fitness R,

        rho(R) = (1-R^-1)/(1-R^-N)

    with neutral limit 1/N.  The algebraically equivalent form used below stays
    exact for Fraction inputs and for both R>1 and 0<R<1.
    """

    n = _validate_population_size(population_size)
    r = as_exact_fraction(relative_fitness, name="relative_fitness")
    if r <= 0:
        raise ValueError("relative_fitness must be positive")
    if r == 1:
        return Fraction(1, n)
    return Fraction(r - 1, 1) * (r ** (n - 1)) / (r**n - 1)


def moran_fixation_ratio(
    relative_fitness: Fraction | int,
    population_size: int,
) -> Fraction:
    """Exact rho(R)/rho(1/R) = R^(N-1)."""

    n = _validate_population_size(population_size)
    r = as_exact_fraction(relative_fitness, name="relative_fitness")
    if r <= 0:
        raise ValueError("relative_fitness must be positive")
    forward = moran_fixation_probability(r, n)
    reverse = moran_fixation_probability(1 / r, n)
    ratio = forward / reverse
    expected = r ** (n - 1)
    if ratio != expected:
        raise ArithmeticError("Moran fixation-ratio identity failed")
    return ratio


def origin_fixation_transition_row(
    required_gap: int,
    genotype: RoutingGenotype,
    population_size: int,
    fitness_step: Fraction | int,
) -> dict[RoutingGenotype, Fraction]:
    """Exact one-substitution-attempt transition row.

    One of 2k coordinate/direction proposals is chosen uniformly.  Invalid
    boundary proposals and failed fixation events contribute to the resident
    self-loop.  Every valid off-diagonal mutation proposal is symmetric with its
    reverse proposal.
    """

    q = _validate_q(required_gap)
    n = _validate_population_size(population_size)
    a = _as_fraction(fitness_step)
    x = validate_routing_genotype(q, genotype)
    k = q + 1
    proposal = Fraction(1, 2 * k)
    row: dict[RoutingGenotype, Fraction] = {x: Fraction(0, 1)}
    fitness_x = routing_fitness(q, x, a)

    for coordinate in range(k):
        for direction in (-1, 1):
            value = x[coordinate] + direction
            if not 0 <= value <= q:
                row[x] += proposal
                continue
            mutant = list(x)
            mutant[coordinate] = value
            y = tuple(mutant)
            relative = routing_fitness(q, y, a) / fitness_x
            fixation = moran_fixation_probability(relative, n)
            row[y] = row.get(y, Fraction(0, 1)) + proposal * fixation
            row[x] += proposal * (1 - fixation)

    if sum(row.values(), Fraction(0, 1)) != 1:
        raise ArithmeticError("origin-fixation transition row lost probability mass")
    return row


def stationary_tilt(population_size: int, fitness_step: Fraction | int) -> Fraction:
    n = _validate_population_size(population_size)
    a = _as_fraction(fitness_step)
    return a ** (n - 1)


def gain_layer_degeneracy(required_gap: int, realized_gain: int) -> int:
    """Number of routing genotypes with exact realized gain r."""

    q = _validate_q(required_gap)
    r = realized_gain
    if type(r) is not int or not (0 <= r <= q):
        raise ValueError("realized_gain must be an integer in [0,q]")
    k = q + 1
    return (q - r + 1) ** k - (q - r) ** k


def gain_layer_degeneracies(required_gap: int) -> tuple[int, ...]:
    q = _validate_q(required_gap)
    result = tuple(gain_layer_degeneracy(q, r) for r in range(q + 1))
    if sum(result) != routing_genotype_count(q):
        raise ArithmeticError("gain-layer degeneracies did not partition genotype space")
    return result


def stationary_layer_weights(
    required_gap: int,
    population_size: int,
    fitness_step: Fraction | int,
) -> tuple[int | Fraction, ...]:
    q = _validate_q(required_gap)
    theta = stationary_tilt(population_size, fitness_step)
    return tuple(gain_layer_degeneracy(q, r) * theta**r for r in range(q + 1))


def stationary_layer_distribution(
    required_gap: int,
    population_size: int,
    fitness_step: Fraction | int,
) -> tuple[Fraction, ...]:
    weights = tuple(Fraction(weight) for weight in stationary_layer_weights(required_gap, population_size, fitness_step))
    z = sum(weights, Fraction(0, 1))
    return tuple(weight / z for weight in weights)


def stationary_genotype_distribution(
    required_gap: int,
    population_size: int,
    fitness_step: Fraction | int,
    *,
    state_limit: int = 10_000,
) -> dict[RoutingGenotype, Fraction]:
    """Exact stationary genotype law pi(x) proportional to theta^g(x)."""

    q = _validate_q(required_gap)
    if type(state_limit) is not int or state_limit < 1:
        raise ValueError("state_limit must be a positive integer")
    count = routing_genotype_count(q)
    if count > state_limit:
        raise RoutingStationaryStateLimitError(
            f"exact stationary enumeration has {count} routing genotypes; declared limit is {state_limit}"
        )
    theta = stationary_tilt(population_size, fitness_step)
    weights = {x: theta ** routing_realized_gain(q, x) for x in routing_genotypes(q)}
    z = sum(weights.values(), Fraction(0, 1))
    return {x: weight / z for x, weight in weights.items()}


def detailed_balance_holds(
    required_gap: int,
    population_size: int,
    fitness_step: Fraction | int,
    *,
    state_limit: int = 10_000,
) -> bool:
    """Exact edgewise detailed-balance audit for small declared state spaces."""

    q = _validate_q(required_gap)
    pi = stationary_genotype_distribution(q, population_size, fitness_step, state_limit=state_limit)
    for x, pi_x in pi.items():
        row = origin_fixation_transition_row(q, x, population_size, fitness_step)
        for y, p_xy in row.items():
            if x == y or p_xy == 0:
                continue
            p_yx = origin_fixation_transition_row(q, y, population_size, fitness_step).get(x, Fraction(0, 1))
            if pi_x * p_xy != pi[y] * p_yx:
                return False
    return True


def stationary_flow_distribution(
    required_gap: int,
    population_size: int,
    fitness_step: Fraction | int,
    *,
    state_limit: int = 10_000,
) -> dict[RoutingGenotype, Fraction]:
    """Multiply the exact proposed stationary law by P once: pi P."""

    q = _validate_q(required_gap)
    pi = stationary_genotype_distribution(q, population_size, fitness_step, state_limit=state_limit)
    out = {x: Fraction(0, 1) for x in pi}
    for x, mass in pi.items():
        for y, probability in origin_fixation_transition_row(q, x, population_size, fitness_step).items():
            out[y] += mass * probability
    return out


def full_phase_modal_tilt_threshold(required_gap: int) -> int:
    """Sharp stationary tilt theta at which the full-gain layer becomes modal."""

    q = _validate_q(required_gap)
    k = q + 1
    return 2**k - 1


def steps_below_full_layer_degeneracy(required_gap: int, steps_below: int) -> int:
    q = _validate_q(required_gap)
    s = steps_below
    if type(s) is not int or not (0 <= s <= q):
        raise ValueError("steps_below must be an integer in [0,q]")
    k = q + 1
    return (s + 1) ** k - s**k


def degeneracy_chain_bound_holds(required_gap: int, steps_below: int) -> bool:
    """Check A_s <= (2^k-1)^s, sharp at s=1.

    A_s counts nested chains of s nonempty subsets of k branch labels; dropping
    the nesting constraint gives at most (2^k-1)^s arbitrary nonempty-subset
    sequences.
    """

    q = _validate_q(required_gap)
    s = steps_below
    if type(s) is not int or not (1 <= s <= q):
        raise ValueError("steps_below must be an integer in [1,q]")
    k = q + 1
    a_s = steps_below_full_layer_degeneracy(q, s)
    bound = (2**k - 1) ** s
    return a_s <= bound


def full_phase_is_modal_layer(required_gap: int, theta: Fraction | int) -> bool:
    q = _validate_q(required_gap)
    tilt = as_exact_fraction(theta, name="theta")
    if tilt <= 0:
        raise ValueError("theta must be positive")
    weights = tuple(Fraction(gain_layer_degeneracy(q, r)) * tilt**r for r in range(q + 1))
    return weights[q] == max(weights)


def full_phase_stationary_mass_from_tilt(required_gap: int, theta: Fraction | int) -> Fraction:
    q = _validate_q(required_gap)
    tilt = as_exact_fraction(theta, name="theta")
    if tilt <= 0:
        raise ValueError("theta must be positive")
    weights = tuple(Fraction(gain_layer_degeneracy(q, r)) * tilt**r for r in range(q + 1))
    return weights[q] / sum(weights, Fraction(0, 1))


def full_phase_half_mass_bounds(required_gap: int) -> tuple[int, int]:
    """Necessary and sufficient-easy tilt bounds for pi(full)>=1/2.

    A=2^k-1 is necessary because the q-1 layer alone has mass ratio A/theta.
    theta>=2A is sufficient because every layer s steps below full has degeneracy
    at most A^s, so the total lower-layer/full ratio is bounded by a geometric
    series with ratio <=1/2.
    """

    a = full_phase_modal_tilt_threshold(required_gap)
    return a, 2 * a


def minimum_population_size_for_modal_full_phase(
    required_gap: int,
    fitness_step: Fraction | int,
) -> int | None:
    """Smallest N>=2 with a^(N-1) >= 2^(q+1)-1; None when a=1."""

    q = _validate_q(required_gap)
    a = _as_fraction(fitness_step)
    if a == 1:
        return None
    target = full_phase_modal_tilt_threshold(q)
    n = 2
    while a ** (n - 1) < target:
        n += 1
    return n


@dataclass(frozen=True)
class OriginFixationSelectionReceipt:
    required_gap: int
    branch_count: int
    population_size: int
    fitness_step: Fraction
    stationary_tilt: Fraction
    genotype_count: int
    layer_degeneracies: tuple[int, ...]
    modal_tilt_threshold: int
    full_phase_is_modal: bool
    full_phase_stationary_mass: Fraction
    half_mass_necessary_tilt: int
    half_mass_sufficient_tilt: int
    detailed_balance_verified: bool | None
    scope: str = "well_mixed_moran_origin_fixation_symmetric_local_routing_mutation"


def origin_fixation_selection_receipt(
    required_gap: int,
    population_size: int,
    fitness_step: Fraction | int,
    *,
    verify_detailed_balance: bool = True,
    state_limit: int = 10_000,
) -> OriginFixationSelectionReceipt:
    q = _validate_q(required_gap)
    n = _validate_population_size(population_size)
    a = _as_fraction(fitness_step)
    theta = stationary_tilt(n, a)
    necessary, sufficient = full_phase_half_mass_bounds(q)
    verified: bool | None = None
    if verify_detailed_balance:
        verified = detailed_balance_holds(q, n, a, state_limit=state_limit)
        if not verified:
            raise ArithmeticError("origin-fixation detailed-balance audit failed")
        pi = stationary_genotype_distribution(q, n, a, state_limit=state_limit)
        if stationary_flow_distribution(q, n, a, state_limit=state_limit) != pi:
            raise ArithmeticError("stationary genotype law failed exact pi P = pi audit")

    return OriginFixationSelectionReceipt(
        required_gap=q,
        branch_count=q + 1,
        population_size=n,
        fitness_step=a,
        stationary_tilt=theta,
        genotype_count=routing_genotype_count(q),
        layer_degeneracies=gain_layer_degeneracies(q),
        modal_tilt_threshold=full_phase_modal_tilt_threshold(q),
        full_phase_is_modal=full_phase_is_modal_layer(q, theta),
        full_phase_stationary_mass=full_phase_stationary_mass_from_tilt(q, theta),
        half_mass_necessary_tilt=necessary,
        half_mass_sufficient_tilt=sufficient,
        detailed_balance_verified=verified,
    )
