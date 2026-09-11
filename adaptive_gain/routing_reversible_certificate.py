"""Reversible-mutation representation certificate for routing phase claims.

This stacked side-theory module generalizes the representation-dependence line.
A finite genotype representation is declared by

* a gain label g(x) in {0,...,q};
* a neutral mutation-proposal Markov kernel Q;
* a positive neutral stationary measure mu that makes Q reversible;
* a declared start genotype for accessibility questions.

Under the same Moran origin-fixation rule used by routing_origin_fixation and
fitness W(x)=a**g(x), the selected origin-fixation chain has stationary law

    pi(x) proportional to mu(x) * theta**g(x),
    theta = a**(N-1).

Thus stationary phenotype occupancy depends on neutral mutation mass per gain
layer, whereas shortest accessibility depends on the support graph of Q.  The
broad mutation-selection/reversible-chain structure is established prior art;
this module is a declaration/identifiability certificate for the adaptive-gain
extension, not a priority claim.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction

from .routing_origin_fixation import moran_fixation_probability, stationary_tilt


class RepresentationCertificateError(ValueError):
    """Raised when a finite mutation representation violates its declaration."""


@dataclass(frozen=True)
class ReversibleMutationCertificate:
    gains: tuple[int, ...]
    proposal: tuple[tuple[Fraction, ...], ...]
    neutral_measure: tuple[Fraction, ...]
    start_state: int

    @property
    def state_count(self) -> int:
        return len(self.gains)

    @property
    def required_gap(self) -> int:
        return max(self.gains)


def _as_fraction(value: Fraction | int) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value, 1)


def validate_reversible_mutation_certificate(
    certificate: ReversibleMutationCertificate,
) -> ReversibleMutationCertificate:
    n = certificate.state_count
    if n < 2:
        raise RepresentationCertificateError("certificate must contain at least two genotypes")
    if len(certificate.proposal) != n or any(len(row) != n for row in certificate.proposal):
        raise RepresentationCertificateError("proposal must be an n by n matrix")
    if len(certificate.neutral_measure) != n:
        raise RepresentationCertificateError("neutral_measure must contain one weight per genotype")
    if type(certificate.start_state) is not int or not (0 <= certificate.start_state < n):
        raise RepresentationCertificateError("start_state is out of range")

    gains = certificate.gains
    if any(type(g) is not int or g < 0 for g in gains):
        raise RepresentationCertificateError("gain labels must be nonnegative integers")
    q = max(gains)
    if q < 1 or min(gains) != 0:
        raise RepresentationCertificateError("gain labels must include both zero and a positive full phase")
    if set(gains) != set(range(q + 1)):
        raise RepresentationCertificateError("every gain level 0..q must be represented")

    proposal = tuple(tuple(_as_fraction(p) for p in row) for row in certificate.proposal)
    for row in proposal:
        if any(p < 0 for p in row):
            raise RepresentationCertificateError("proposal probabilities must be nonnegative")
        if sum(row, Fraction(0, 1)) != 1:
            raise RepresentationCertificateError("each proposal row must sum to one")

    mu = tuple(_as_fraction(w) for w in certificate.neutral_measure)
    if any(w <= 0 for w in mu):
        raise RepresentationCertificateError("neutral_measure weights must be strictly positive")
    if sum(mu, Fraction(0, 1)) != 1:
        raise RepresentationCertificateError("neutral_measure must sum to one")

    for i in range(n):
        for j in range(n):
            if mu[i] * proposal[i][j] != mu[j] * proposal[j][i]:
                raise RepresentationCertificateError("proposal is not reversible with neutral_measure")

    # Reversibility with positive mu gives symmetric support.  Require one
    # connected neutral mutation component so the stationary law is unique.
    seen = {0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in range(n):
            if j not in seen and (proposal[i][j] > 0 or proposal[j][i] > 0):
                seen.add(j)
                queue.append(j)
    if len(seen) != n:
        raise RepresentationCertificateError("proposal support graph must be connected")

    return ReversibleMutationCertificate(gains, proposal, mu, certificate.start_state)


def neutral_layer_masses(
    certificate: ReversibleMutationCertificate,
) -> tuple[Fraction, ...]:
    cert = validate_reversible_mutation_certificate(certificate)
    q = cert.required_gap
    masses = [Fraction(0, 1) for _ in range(q + 1)]
    for gain, weight in zip(cert.gains, cert.neutral_measure, strict=True):
        masses[gain] += weight
    if sum(masses, Fraction(0, 1)) != 1:
        raise ArithmeticError("neutral layer masses did not sum to one")
    return tuple(masses)


def selected_origin_fixation_transition_row(
    certificate: ReversibleMutationCertificate,
    resident_state: int,
    population_size: int,
    fitness_step: Fraction | int,
) -> tuple[Fraction, ...]:
    cert = validate_reversible_mutation_certificate(certificate)
    n = cert.state_count
    if type(resident_state) is not int or not (0 <= resident_state < n):
        raise ValueError("resident_state is out of range")
    if type(population_size) is not int or population_size < 2:
        raise ValueError("population_size must be an integer at least 2")
    a = _as_fraction(fitness_step)
    if a < 1:
        raise ValueError("fitness_step must be at least one")

    i = resident_state
    row = [Fraction(0, 1) for _ in range(n)]
    gain_i = cert.gains[i]
    for j, proposal_probability in enumerate(cert.proposal[i]):
        if proposal_probability == 0:
            continue
        if j == i:
            row[i] += proposal_probability
            continue
        relative = a ** (cert.gains[j] - gain_i)
        fixation = moran_fixation_probability(relative, population_size)
        row[j] += proposal_probability * fixation
        row[i] += proposal_probability * (1 - fixation)

    if sum(row, Fraction(0, 1)) != 1:
        raise ArithmeticError("selected origin-fixation row lost probability mass")
    return tuple(row)


def selected_stationary_distribution(
    certificate: ReversibleMutationCertificate,
    population_size: int,
    fitness_step: Fraction | int,
) -> tuple[Fraction, ...]:
    cert = validate_reversible_mutation_certificate(certificate)
    theta = stationary_tilt(population_size, fitness_step)
    weights = tuple(
        cert.neutral_measure[i] * theta ** cert.gains[i]
        for i in range(cert.state_count)
    )
    z = sum(weights, Fraction(0, 1))
    return tuple(weight / z for weight in weights)


def selected_stationary_flow(
    certificate: ReversibleMutationCertificate,
    population_size: int,
    fitness_step: Fraction | int,
) -> tuple[Fraction, ...]:
    cert = validate_reversible_mutation_certificate(certificate)
    pi = selected_stationary_distribution(cert, population_size, fitness_step)
    out = [Fraction(0, 1) for _ in range(cert.state_count)]
    for i, mass in enumerate(pi):
        row = selected_origin_fixation_transition_row(cert, i, population_size, fitness_step)
        for j, probability in enumerate(row):
            out[j] += mass * probability
    return tuple(out)


def selected_detailed_balance_holds(
    certificate: ReversibleMutationCertificate,
    population_size: int,
    fitness_step: Fraction | int,
) -> bool:
    cert = validate_reversible_mutation_certificate(certificate)
    pi = selected_stationary_distribution(cert, population_size, fitness_step)
    rows = tuple(
        selected_origin_fixation_transition_row(cert, i, population_size, fitness_step)
        for i in range(cert.state_count)
    )
    for i in range(cert.state_count):
        for j in range(cert.state_count):
            if pi[i] * rows[i][j] != pi[j] * rows[j][i]:
                return False
    return True


def selected_layer_distribution_from_tilt(
    certificate: ReversibleMutationCertificate,
    theta: Fraction | int,
) -> tuple[Fraction, ...]:
    cert = validate_reversible_mutation_certificate(certificate)
    tilt = _as_fraction(theta)
    if tilt <= 0:
        raise ValueError("theta must be positive")
    masses = neutral_layer_masses(cert)
    weights = tuple(masses[r] * tilt**r for r in range(cert.required_gap + 1))
    z = sum(weights, Fraction(0, 1))
    return tuple(weight / z for weight in weights)


def full_phase_modal_inequalities(
    certificate: ReversibleMutationCertificate,
    theta: Fraction | int,
) -> tuple[bool, ...]:
    """Exact inequalities B_q theta^q >= B_r theta^r for r<q."""

    cert = validate_reversible_mutation_certificate(certificate)
    tilt = _as_fraction(theta)
    if tilt <= 0:
        raise ValueError("theta must be positive")
    masses = neutral_layer_masses(cert)
    q = cert.required_gap
    full_weight = masses[q] * tilt**q
    return tuple(full_weight >= masses[r] * tilt**r for r in range(q))


def full_phase_is_modal_from_certificate(
    certificate: ReversibleMutationCertificate,
    theta: Fraction | int,
) -> bool:
    return all(full_phase_modal_inequalities(certificate, theta))


def shortest_support_distance_to_gain(
    certificate: ReversibleMutationCertificate,
    target_gain: int,
) -> int:
    """Shortest support-graph distance from start_state to gain >= target_gain."""

    cert = validate_reversible_mutation_certificate(certificate)
    q = cert.required_gap
    if type(target_gain) is not int or not (0 <= target_gain <= q):
        raise ValueError("target_gain must be an integer in [0,q]")
    start = cert.start_state
    if cert.gains[start] >= target_gain:
        return 0

    seen = {start}
    queue = deque([(start, 0)])
    while queue:
        i, distance = queue.popleft()
        for j in range(cert.state_count):
            if j in seen:
                continue
            if cert.proposal[i][j] == 0 and cert.proposal[j][i] == 0:
                continue
            if cert.gains[j] >= target_gain:
                return distance + 1
            seen.add(j)
            queue.append((j, distance + 1))
    raise ArithmeticError("connected support graph did not reach declared target gain")


@dataclass(frozen=True)
class RepresentationCertificateReceipt:
    required_gap: int
    state_count: int
    neutral_layer_masses: tuple[Fraction, ...]
    shortest_distances: tuple[int, ...]
    full_phase_modal_at_theta: bool
    selected_stationary_verified: bool


def representation_certificate_receipt(
    certificate: ReversibleMutationCertificate,
    population_size: int,
    fitness_step: Fraction | int,
) -> RepresentationCertificateReceipt:
    cert = validate_reversible_mutation_certificate(certificate)
    theta = stationary_tilt(population_size, fitness_step)
    pi = selected_stationary_distribution(cert, population_size, fitness_step)
    flow = selected_stationary_flow(cert, population_size, fitness_step)
    verified = pi == flow and selected_detailed_balance_holds(cert, population_size, fitness_step)
    if not verified:
        raise ArithmeticError("reversible-mutation representation certificate audit failed")
    return RepresentationCertificateReceipt(
        required_gap=cert.required_gap,
        state_count=cert.state_count,
        neutral_layer_masses=neutral_layer_masses(cert),
        shortest_distances=tuple(
            shortest_support_distance_to_gain(cert, r)
            for r in range(cert.required_gap + 1)
        ),
        full_phase_modal_at_theta=full_phase_is_modal_from_certificate(cert, theta),
        selected_stationary_verified=True,
    )
