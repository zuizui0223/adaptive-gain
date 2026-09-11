from __future__ import annotations

from fractions import Fraction
from itertools import product

import pytest

from adaptive_gain.routing_neutral_plateau import (
    expected_attempts_to_first_positive_gain,
    expected_remaining_attempts,
    first_gain_waiting_receipt,
    first_positive_gain_cdf,
    first_positive_gain_pmf,
    harmonic_number,
    lump_transition_row,
    required_gap_first_gain_waiting_receipt,
    touched_count_distribution,
)


def _microstate_lump_transition(k: int, deletions: tuple[int, ...]) -> tuple[Fraction, Fraction]:
    """Return P(stay at m), P(move to m+1) from one microscopic state."""
    m = sum(value > 0 for value in deletions)
    untouched = k - m
    return Fraction(m, k), Fraction(untouched, k)


def test_lump_transition_rows_are_stochastic_and_absorb_at_k() -> None:
    for k in range(2, 8):
        for m in range(k + 1):
            row = lump_transition_row(k, m)
            assert len(row) == k + 1
            assert sum(row, Fraction(0, 1)) == 1
            if m == k:
                assert row[k] == 1
            else:
                assert row[m] == Fraction(m, k)
                assert row[m + 1] == Fraction(k - m, k)


def test_touch_count_is_a_strong_lump_for_all_microstates_through_k4() -> None:
    # A microstate records how many redundant occurrences have already been
    # pruned from each branch, capped at k-1.  Before first gain, the probability
    # of touching a new branch depends only on how many coordinates are nonzero.
    for k in range(2, 5):
        by_m: dict[int, set[tuple[Fraction, Fraction]]] = {}
        for deletions in product(range(k), repeat=k):
            m = sum(value > 0 for value in deletions)
            if m == k:
                continue
            by_m.setdefault(m, set()).add(_microstate_lump_transition(k, deletions))
        for m, rows in by_m.items():
            assert rows == {(Fraction(m, k), Fraction(k - m, k))}


def test_inclusion_exclusion_cdf_matches_exact_lumped_markov_dp() -> None:
    for k in range(2, 7):
        previous = Fraction(0, 1)
        for t in range(0, 3 * k + 8):
            distribution = touched_count_distribution(k, t)
            cdf = first_positive_gain_cdf(k, t)
            assert cdf == distribution[k]
            assert previous <= cdf <= 1
            previous = cdf


def test_pmf_is_cdf_increment_and_zero_before_k() -> None:
    for k in range(2, 7):
        for t in range(0, 3 * k + 8):
            pmf = first_positive_gain_pmf(k, t)
            assert pmf >= 0
            if t < k:
                assert pmf == 0
            if t > 0:
                assert pmf == first_positive_gain_cdf(k, t) - first_positive_gain_cdf(k, t - 1)


def test_harmonic_expectation_solves_first_step_recurrence() -> None:
    for k in range(2, 9):
        assert expected_attempts_to_first_positive_gain(k) == k * harmonic_number(k)
        assert expected_remaining_attempts(k, k) == 0
        for m in range(k):
            e_m = expected_remaining_attempts(k, m)
            e_next = expected_remaining_attempts(k, m + 1)
            stay = Fraction(m, k)
            advance = Fraction(k - m, k)
            assert e_m == 1 + stay * e_m + advance * e_next


def test_earliest_completion_probability_is_k_factorial_over_k_to_k() -> None:
    factorial = 1
    for k in range(2, 9):
        factorial *= k
        assert first_positive_gain_pmf(k, k) == Fraction(factorial, k**k)
        receipt = first_gain_waiting_receipt(k)
        assert receipt.earliest_possible_attempt == k
        assert receipt.earliest_completion_probability == Fraction(factorial, k**k)


def test_canonical_q2_k3_waiting_time_is_eleven_halves() -> None:
    receipt = required_gap_first_gain_waiting_receipt(2)
    assert receipt.branch_count == 3
    assert receipt.static_world_count == 6
    assert receipt.static_query_count == 4
    assert receipt.static_adaptive_depth == 2
    assert receipt.shortest_attempts_to_any_positive_gain == 3
    assert receipt.expected_attempts_to_any_positive_gain == Fraction(11, 2)
    assert receipt.overhead_factor == Fraction(11, 6)


def test_required_gap_family_has_harmonic_stochastic_overhead() -> None:
    for q in range(1, 8):
        receipt = required_gap_first_gain_waiting_receipt(q)
        k = q + 1
        assert receipt.shortest_attempts_to_any_positive_gain == k
        assert receipt.expected_attempts_to_any_positive_gain == k * harmonic_number(k)
        assert receipt.overhead_factor == harmonic_number(k)


def test_validation() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        first_positive_gain_cdf(1, 3)
    with pytest.raises(ValueError, match="nonnegative"):
        first_positive_gain_cdf(3, -1)
    with pytest.raises(ValueError, match=r"\[0,k\]"):
        lump_transition_row(3, 4)
    with pytest.raises(ValueError, match="positive integer"):
        required_gap_first_gain_waiting_receipt(0)
