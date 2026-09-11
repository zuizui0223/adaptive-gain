from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb

import pytest

from adaptive_gain.routing_full_target_mesoscopic import (
    RoutingMesostateLimitError,
    capped_microstate_count,
    capped_progress_histogram,
    earliest_target_completion_probability,
    expected_attempts_to_realized_gain,
    full_target_waiting_receipt,
    histogram_mesostate_count,
    histogram_transition_distribution,
    required_gap_phase_entry_receipt,
)
from adaptive_gain.routing_neutral_plateau import expected_attempts_to_first_positive_gain


def _micro_transition_distribution(k: int, r: int, progress: tuple[int, ...]):
    result: dict[tuple[int, ...], Fraction] = {}
    for branch in range(k):
        nxt = list(progress)
        nxt[branch] = min(r, nxt[branch] + 1)
        hist = capped_progress_histogram(tuple(nxt), r)
        result[hist] = result.get(hist, Fraction(0, 1)) + Fraction(1, k)
    return result


def _micro_expected_attempts(k: int, r: int) -> Fraction:
    @lru_cache(None)
    def expected(progress: tuple[int, ...]) -> Fraction:
        if all(value == r for value in progress):
            return Fraction(0, 1)
        saturated = sum(value == r for value in progress)
        active = k - saturated
        value = Fraction(k, active)
        for branch, count in enumerate(progress):
            if count == r:
                continue
            nxt = list(progress)
            nxt[branch] += 1
            value += Fraction(1, active) * expected(tuple(nxt))
        return value
    return expected((0,) * k)


def _histogram_count_by_enumeration(k: int, r: int) -> int:
    return len({capped_progress_histogram(tuple(p), r) for p in product(range(r + 1), repeat=k)})


def test_histogram_counts_match_microstate_enumeration() -> None:
    for k in range(2, 6):
        for r in range(1, k):
            assert capped_microstate_count(k, r) == (r + 1) ** k
            assert histogram_mesostate_count(k, r) == comb(k + r, r)
            if (r + 1) ** k <= 5000:
                assert _histogram_count_by_enumeration(k, r) == comb(k + r, r)


def test_histogram_is_a_strong_lump_through_small_scopes() -> None:
    for k in range(2, 5):
        for r in range(1, k):
            by_hist: dict[tuple[int, ...], set[tuple[tuple[tuple[int, ...], Fraction], ...]]] = {}
            for progress in product(range(r + 1), repeat=k):
                progress = tuple(progress)
                hist = capped_progress_histogram(progress, r)
                dist = _micro_transition_distribution(k, r, progress)
                signature = tuple(sorted(dist.items()))
                by_hist.setdefault(hist, set()).add(signature)
            for hist, signatures in by_hist.items():
                assert len(signatures) == 1
                observed = dict(next(iter(signatures)))
                assert observed == histogram_transition_distribution(k, r, hist)


def test_mesoscopic_expectation_matches_independent_microstate_dp() -> None:
    for k in range(2, 5):
        for r in range(1, k):
            assert expected_attempts_to_realized_gain(k, r) == _micro_expected_attempts(k, r)


def test_r1_reduces_exactly_to_first_gain_coupon_collector() -> None:
    for k in range(2, 9):
        assert expected_attempts_to_realized_gain(k, 1) == expected_attempts_to_first_positive_gain(k)


def test_earliest_completion_probability_small_exact_values() -> None:
    assert earliest_target_completion_probability(2, 1) == Fraction(1, 2)
    assert earliest_target_completion_probability(3, 1) == Fraction(2, 9)
    assert earliest_target_completion_probability(3, 2) == Fraction(10, 81)


def test_canonical_q2_full_phase_entry_is_347_over_36() -> None:
    receipt = required_gap_phase_entry_receipt(2)
    assert receipt.branch_count == 3
    assert receipt.static_world_count == 6
    assert receipt.static_query_count == 4
    assert receipt.static_adaptive_depth == 2
    assert receipt.shortest_elementary_prunings == 6
    assert receipt.capped_microstate_count == 27
    assert receipt.histogram_mesostate_count == 10
    assert receipt.expected_phase_entry_attempts == Fraction(347, 36)
    assert receipt.stochastic_overhead_factor == Fraction(347, 216)
    assert receipt.earliest_phase_entry_probability == Fraction(10, 81)


def test_expected_attempts_never_beat_shortest_path() -> None:
    for k in range(2, 7):
        for r in range(1, k):
            receipt = full_target_waiting_receipt(k, r)
            assert receipt.shortest_elementary_prunings == k * r
            assert receipt.expected_mutation_attempts >= k * r
            assert receipt.stochastic_overhead_factor >= 1


def test_required_gap_family_exact_values_for_small_q() -> None:
    expected = {
        1: Fraction(3, 1),
        2: Fraction(347, 36),
        3: Fraction(38948987, 1990656),
    }
    for q, value in expected.items():
        receipt = required_gap_phase_entry_receipt(q)
        assert receipt.branch_count == q + 1
        assert receipt.shortest_elementary_prunings == q * (q + 1)
        assert receipt.expected_phase_entry_attempts == value


def test_mesostate_resource_limit_is_explicit() -> None:
    with pytest.raises(RoutingMesostateLimitError, match="mesostates"):
        expected_attempts_to_realized_gain(6, 5, mesostate_limit=100)


def test_validation() -> None:
    with pytest.raises(ValueError, match=r"\[1,k-1\]"):
        expected_attempts_to_realized_gain(3, 0)
    with pytest.raises(ValueError, match="at least two"):
        capped_progress_histogram((0,), 1)
    with pytest.raises(ValueError, match="nonnegative"):
        capped_progress_histogram((0, -1), 1)
    with pytest.raises(ValueError, match="positive integer"):
        required_gap_phase_entry_receipt(0)
