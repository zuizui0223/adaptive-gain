from __future__ import annotations

from collections import deque
from fractions import Fraction

import pytest

from adaptive_gain.downstream_population_nonidentifiability import (
    AccessibilityRepresentation,
    accessibility_nonidentifiability_receipt,
    arbitrary_accessibility_distance_representation,
    canonical_q2_downstream_ceiling_receipt,
    shortest_distance_to_full_phase,
)


def _independent_bfs_distance(rep: AccessibilityRepresentation) -> int:
    queue = deque([(rep.start_state, 0)])
    seen = {rep.start_state}
    while queue:
        state, distance = queue.popleft()
        if rep.gains[state] == rep.required_gap:
            return distance
        for nxt in rep.adjacency[state]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, distance + 1))
    raise AssertionError("full phase was unreachable")


def _independent_connected(rep: AccessibilityRepresentation) -> bool:
    queue = deque([rep.start_state])
    seen = {rep.start_state}
    while queue:
        state = queue.popleft()
        for nxt in rep.adjacency[state]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen) == rep.state_count


def test_arbitrary_distance_construction_realizes_every_small_q_d_pair() -> None:
    for q in range(1, 7):
        for distance in range(1, 10):
            rep = arbitrary_accessibility_distance_representation(q, distance)
            assert set(rep.gains) == set(range(q + 1))
            assert rep.gains[rep.start_state] == 0
            assert rep.gains[rep.full_state] == q
            assert sum(gain == q for gain in rep.gains) == 1
            assert _independent_connected(rep)
            assert _independent_bfs_distance(rep) == distance
            assert shortest_distance_to_full_phase(rep) == distance


def test_receipt_records_exact_declared_distance() -> None:
    receipt = accessibility_nonidentifiability_receipt(4, 13)
    assert receipt.required_gap == 4
    assert receipt.declared_distance == 13
    assert receipt.shortest_full_phase_distance == 13
    assert receipt.represented_gain_levels == (0, 1, 2, 3, 4)
    assert receipt.verified


def test_same_q_supports_arbitrarily_different_accessibility_witnesses() -> None:
    near = accessibility_nonidentifiability_receipt(3, 1)
    far = accessibility_nonidentifiability_receipt(3, 25)
    assert near.required_gap == far.required_gap == 3
    assert near.represented_gain_levels == far.represented_gain_levels == (0, 1, 2, 3)
    assert near.shortest_full_phase_distance == 1
    assert far.shortest_full_phase_distance == 25


def test_canonical_q2_ceiling_composes_access_occupancy_and_time_scale() -> None:
    receipt = canonical_q2_downstream_ceiling_receipt()
    assert receipt.required_gap == 2
    assert receipt.short_access_distance == 1
    assert receipt.long_access_distance == 9

    # Same q=2, same local gain path and same phenotype tilt can make the full
    # phase either a majority or a small minority by changing mutation bias.
    assert receipt.favored_full_stationary_mass == Fraction(7, 10)
    assert receipt.disfavored_full_stationary_mass == Fraction(1, 10)
    assert receipt.fixed_support_distance == 2

    # Holding that support and stationary law fixed, epsilon=1/3 triples the
    # expected proposal-attempt time without changing occupancy.
    assert receipt.timing_scale == Fraction(1, 3)
    assert receipt.timing_inflation == 3
    assert receipt.declaration_ladder == (
        "phenotype gap and fitness schedule",
        "genotype-policy map and mutation support graph",
        "neutral mutation measure or relative proposal bias",
        "absolute proposal or mutation-rate scale",
        "population process connecting mutation and selection",
    )


@pytest.mark.parametrize("q,distance", [(0, 1), (1, 0), (-1, 3), (2, -1)])
def test_invalid_construction_parameters_are_rejected(q: int, distance: int) -> None:
    with pytest.raises(ValueError):
        arbitrary_accessibility_distance_representation(q, distance)
