from __future__ import annotations

from collections import deque
from fractions import Fraction

import pytest

from adaptive_gain.routing_origin_fixation import (
    full_phase_is_modal_layer,
    full_phase_modal_tilt_threshold,
    full_phase_stationary_mass_from_tilt,
)
from adaptive_gain.routing_representation_dependence import (
    accessibility_distance_inflation,
    branch_product_distance,
    compressed_chain_transition_row,
    compressed_full_phase_half_mass_holds,
    compressed_full_phase_is_unique_modal,
    compressed_full_phase_mass_from_tilt,
    compressed_gain_chain_distance,
    compressed_half_mass_polynomial,
    compressed_stationary_distribution,
    compressed_stationary_flow,
    modal_threshold_inflation,
    universal_theta_two_witness,
)


def _bfs_product_distance(q: int, target_gain: int) -> int:
    k = q + 1
    start = (0,) * k
    if min(start) >= target_gain:
        return 0
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, d = queue.popleft()
        for i in range(k):
            for direction in (-1, 1):
                value = state[i] + direction
                if not 0 <= value <= q:
                    continue
                nxt = list(state)
                nxt[i] = value
                t = tuple(nxt)
                if t in seen:
                    continue
                if min(t) >= target_gain:
                    return d + 1
                seen.add(t)
                queue.append((t, d + 1))
    raise AssertionError("target gain not reachable")


def test_accessibility_distance_inflation_matches_independent_bfs() -> None:
    for q in range(1, 5):
        for r in range(1, q + 1):
            assert compressed_gain_chain_distance(q, r) == r
            assert branch_product_distance(q, r) == _bfs_product_distance(q, r)
            assert accessibility_distance_inflation(q, r) == q + 1


def test_compressed_origin_fixation_rows_are_stochastic() -> None:
    for q in range(1, 6):
        for r in range(q + 1):
            row = compressed_chain_transition_row(q, r, 4, 2)
            assert sum(row.values(), Fraction(0, 1)) == 1
            assert all(prob >= 0 for prob in row.values())


def test_compressed_stationary_law_is_exactly_invariant() -> None:
    for q in range(1, 7):
        pi = compressed_stationary_distribution(q, 4, 2)
        assert compressed_stationary_flow(q, 4, 2) == pi
        assert sum(pi, Fraction(0, 1)) == 1
        assert all(pi[r + 1] / pi[r] == 8 for r in range(q))


def test_mode_thresholds_separate_for_every_positive_q() -> None:
    for q in range(1, 9):
        assert modal_threshold_inflation(q) == 2 ** (q + 1) - 1
        assert compressed_full_phase_is_unique_modal(q, Fraction(3, 2)) is True
        assert full_phase_is_modal_layer(q, Fraction(3, 2)) is False
        assert full_phase_modal_tilt_threshold(q) == 2 ** (q + 1) - 1


def test_universal_theta_two_witness_reverses_phase_conclusion() -> None:
    for q in range(1, 9):
        receipt = universal_theta_two_witness(q)
        assert receipt.theta == 2
        assert receipt.distance_inflation == q + 1
        assert receipt.product_full_distance == q * (q + 1)
        assert receipt.compressed_full_distance == q
        assert receipt.compressed_full_mass == Fraction(2**q, 2 ** (q + 1) - 1)
        assert receipt.compressed_full_mass > Fraction(1, 2)
        assert receipt.compressed_unique_modal is True
        assert receipt.product_modal is False
        assert receipt.product_modal_threshold == 2 ** (q + 1) - 1


def test_canonical_q2_exact_representation_contrast() -> None:
    q = 2
    receipt = universal_theta_two_witness(q)
    assert receipt.product_full_distance == 6
    assert receipt.compressed_full_distance == 2
    assert receipt.compressed_full_mass == Fraction(4, 7)
    assert receipt.product_full_mass == Fraction(4, 37)
    assert full_phase_stationary_mass_from_tilt(q, 2) == Fraction(4, 37)
    assert full_phase_modal_tilt_threshold(q) == 7


def test_compressed_half_mass_boundary_is_exact_predicate() -> None:
    assert compressed_full_phase_half_mass_holds(1, 1) is True
    assert compressed_full_phase_half_mass_holds(2, Fraction(3, 2)) is False
    assert compressed_full_phase_half_mass_holds(2, 2) is True
    # q=2 boundary solves theta^3-2theta^2+1=(theta-1)(theta^2-theta-1)=0.
    assert compressed_half_mass_polynomial(2, Fraction(3, 2)) < 0
    assert compressed_half_mass_polynomial(2, 2) > 0


def test_same_gain_levels_but_different_stationary_layer_weights() -> None:
    # Same gains {0,1,2} and same theta=2.
    chain = tuple(Fraction(2**r, 1) for r in range(3))
    product = (Fraction(19, 1), Fraction(14, 1), Fraction(4, 1))
    assert chain == (1, 2, 4)
    assert product[2] < max(product)
    assert chain[2] == max(chain)


def test_validation() -> None:
    with pytest.raises(ValueError, match="positive integer"):
        compressed_gain_chain_distance(0, 0)
    with pytest.raises(ValueError, match=r"\[0,q\]"):
        compressed_gain_chain_distance(2, 3)
    with pytest.raises(ValueError, match="undefined"):
        accessibility_distance_inflation(2, 0)
    with pytest.raises(ValueError, match="population_size"):
        compressed_chain_transition_row(2, 0, 1, 2)
    with pytest.raises(ValueError, match="at least one"):
        compressed_chain_transition_row(2, 0, 3, Fraction(1, 2))
    with pytest.raises(ValueError, match="theta must be positive"):
        compressed_full_phase_mass_from_tilt(2, 0)
