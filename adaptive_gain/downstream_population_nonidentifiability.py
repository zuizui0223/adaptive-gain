"""Downstream population nonidentifiability ceiling for adaptive-gain side theory.

The upstream finite-sensing theorem identifies a required phenotype-level structural gap.
It does not identify genotype accessibility, stationary phase occupancy, or absolute
waiting time.  This module closes the accessibility part with an exact construction
and composes it with the already-established stationary-occupancy and rate-scale
counterexamples.

No novelty is claimed for generic genotype-phenotype representation dependence,
reversible mutation-selection equilibrium, or Markov-chain time rescaling.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction

from .routing_rate_scale_nonidentifiability import (
    rate_scale_nonidentifiability_receipt,
)
from .routing_stationary_nonidentifiability import (
    canonical_q2_mutation_bias_contradiction,
)


@dataclass(frozen=True)
class AccessibilityRepresentation:
    """Finite connected genotype representation with declared gain labels."""

    required_gap: int
    declared_distance: int
    gains: tuple[int, ...]
    adjacency: tuple[tuple[int, ...], ...]
    start_state: int
    full_state: int

    @property
    def state_count(self) -> int:
        return len(self.gains)


def _validate_representation(rep: AccessibilityRepresentation) -> AccessibilityRepresentation:
    if rep.required_gap < 1:
        raise ValueError("required_gap must be at least one")
    if rep.declared_distance < 1:
        raise ValueError("declared_distance must be at least one")
    n = len(rep.gains)
    if n == 0 or len(rep.adjacency) != n:
        raise ValueError("gains and adjacency must define the same nonempty state set")
    if not 0 <= rep.start_state < n or not 0 <= rep.full_state < n:
        raise ValueError("start_state and full_state must be valid indices")
    if rep.gains[rep.start_state] != 0:
        raise ValueError("start_state must have gain zero")
    if rep.gains[rep.full_state] != rep.required_gap:
        raise ValueError("full_state must realize the required gap")
    if set(rep.gains) != set(range(rep.required_gap + 1)):
        raise ValueError("every gain level 0,...,q must be represented")
    for i, neighbors in enumerate(rep.adjacency):
        if len(set(neighbors)) != len(neighbors):
            raise ValueError("adjacency rows must not contain duplicate neighbors")
        for j in neighbors:
            if not 0 <= j < n or j == i:
                raise ValueError("adjacency contains an invalid neighbor")
            if i not in rep.adjacency[j]:
                raise ValueError("adjacency must be undirected")
    return rep


def arbitrary_accessibility_distance_representation(
    required_gap: int,
    distance: int,
) -> AccessibilityRepresentation:
    """Construct the same gain set with shortest full-phase distance exactly D.

    Use a path p_0--...--p_D from the declared start to the unique full-gain
    genotype.  All internal path vertices have gain zero.  For each missing gain
    level 1,...,q-1 attach one leaf to p_0.  Those leaves ensure every phenotype
    gain is represented without creating a shortcut to the full phase.
    """

    q = int(required_gap)
    d = int(distance)
    if q < 1:
        raise ValueError("required_gap must be at least one")
    if d < 1:
        raise ValueError("distance must be at least one")

    path_count = d + 1
    leaf_count = max(0, q - 1)
    n = path_count + leaf_count
    adjacency_sets = [set() for _ in range(n)]

    for i in range(d):
        adjacency_sets[i].add(i + 1)
        adjacency_sets[i + 1].add(i)

    gains = [0 for _ in range(n)]
    gains[d] = q
    for r in range(1, q):
        leaf = path_count + (r - 1)
        gains[leaf] = r
        adjacency_sets[0].add(leaf)
        adjacency_sets[leaf].add(0)

    rep = AccessibilityRepresentation(
        required_gap=q,
        declared_distance=d,
        gains=tuple(gains),
        adjacency=tuple(tuple(sorted(row)) for row in adjacency_sets),
        start_state=0,
        full_state=d,
    )
    return _validate_representation(rep)


def shortest_distance_to_full_phase(rep: AccessibilityRepresentation) -> int:
    """Return exact BFS distance from the declared start to any gain-q state."""

    rep = _validate_representation(rep)
    q = rep.required_gap
    queue: deque[tuple[int, int]] = deque([(rep.start_state, 0)])
    seen = {rep.start_state}
    while queue:
        state, distance = queue.popleft()
        if rep.gains[state] == q:
            return distance
        for nxt in rep.adjacency[state]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, distance + 1))
    raise ArithmeticError("validated representation was unexpectedly disconnected from full phase")


@dataclass(frozen=True)
class AccessibilityNonidentifiabilityReceipt:
    required_gap: int
    declared_distance: int
    state_count: int
    represented_gain_levels: tuple[int, ...]
    shortest_full_phase_distance: int
    verified: bool


def accessibility_nonidentifiability_receipt(
    required_gap: int,
    distance: int,
) -> AccessibilityNonidentifiabilityReceipt:
    rep = arbitrary_accessibility_distance_representation(required_gap, distance)
    observed = shortest_distance_to_full_phase(rep)
    if observed != distance:
        raise ArithmeticError("constructed representation did not realize declared distance")
    levels = tuple(sorted(set(rep.gains)))
    return AccessibilityNonidentifiabilityReceipt(
        required_gap=rep.required_gap,
        declared_distance=rep.declared_distance,
        state_count=rep.state_count,
        represented_gain_levels=levels,
        shortest_full_phase_distance=observed,
        verified=True,
    )


@dataclass(frozen=True)
class CanonicalDownstreamCeilingReceipt:
    required_gap: int
    short_access_distance: int
    long_access_distance: int
    favored_full_stationary_mass: Fraction
    disfavored_full_stationary_mass: Fraction
    fixed_support_distance: int
    timing_scale: Fraction
    timing_inflation: Fraction
    declaration_ladder: tuple[str, ...]


def canonical_q2_downstream_ceiling_receipt() -> CanonicalDownstreamCeilingReceipt:
    """Compose the three exact no-go coordinates for a canonical q=2 audit."""

    short_access = accessibility_nonidentifiability_receipt(2, 1)
    long_access = accessibility_nonidentifiability_receipt(2, 9)
    occupancy = canonical_q2_mutation_bias_contradiction()

    favored = (Fraction(1, 10), Fraction(1, 5), Fraction(7, 10))
    rate = rate_scale_nonidentifiability_receipt(
        favored,
        Fraction(2, 1),
        Fraction(1, 3),
    )

    if occupancy.shortest_full_phase_distance_both != rate.shortest_full_phase_distance:
        raise ArithmeticError("canonical fixed-support distance changed across side-theory layers")

    return CanonicalDownstreamCeilingReceipt(
        required_gap=2,
        short_access_distance=short_access.shortest_full_phase_distance,
        long_access_distance=long_access.shortest_full_phase_distance,
        favored_full_stationary_mass=occupancy.full_favored_mass,
        disfavored_full_stationary_mass=occupancy.full_disfavored_mass,
        fixed_support_distance=rate.shortest_full_phase_distance,
        timing_scale=rate.edge_scale,
        timing_inflation=rate.timing_inflation,
        declaration_ladder=(
            "phenotype gap and fitness schedule",
            "genotype-policy map and mutation support graph",
            "neutral mutation measure or relative proposal bias",
            "absolute proposal or mutation-rate scale",
            "population process connecting mutation and selection",
        ),
    )
