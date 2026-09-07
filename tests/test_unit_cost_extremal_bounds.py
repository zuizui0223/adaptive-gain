from functools import lru_cache
from fractions import Fraction

from adaptive_gain.unit_cost_extremal_bounds import (
    maximum_productive_tree_internal_nodes,
    sharp_unit_cost_ratio,
    sharp_unit_cost_ratio_receipt,
    unit_cost_fixed_cost_bound,
)


@lru_cache(None)
def _bruteforce_tree_internal_max(leaves: int, depth: int) -> int:
    """Independent recurrence over root-child leaf partitions."""
    if leaves <= 1 or depth == 0:
        return 0
    if depth == 1:
        return 1

    # Integer compositions into at least two positive child leaf counts.
    best = 1

    def visit(remaining: int, parts: tuple[int, ...]) -> None:
        nonlocal best
        if remaining == 0:
            if len(parts) >= 2:
                value = 1 + sum(
                    _bruteforce_tree_internal_max(part, depth - 1)
                    for part in parts
                    if part >= 2
                )
                best = max(best, value)
            return
        for size in range(1, remaining + 1):
            visit(remaining - size, parts + (size,))

    visit(leaves, ())
    return best


def test_closed_form_tree_union_bound_matches_independent_recurrence():
    for n in range(1, 11):
        for h in range(0, 6):
            assert maximum_productive_tree_internal_nodes(n, h) == _bruteforce_tree_internal_max(n, h)


def test_tree_union_bound_special_cases():
    assert maximum_productive_tree_internal_nodes(10, 1) == 1
    assert maximum_productive_tree_internal_nodes(10, 2) == 6
    assert maximum_productive_tree_internal_nodes(10, 3) == 8
    assert maximum_productive_tree_internal_nodes(10, 4) == 9
    assert unit_cost_fixed_cost_bound(10, 99, 2) == 6
    assert unit_cost_fixed_cost_bound(10, 4, 2) == 4


def test_sharp_fixed_world_query_ratio_formula():
    expected = {
        (2, 1): Fraction(1, 1),
        (3, 7): Fraction(1, 1),
        (4, 3): Fraction(3, 2),
        (5, 99): Fraction(3, 2),
        (6, 4): Fraction(2, 1),
        (10, 4): Fraction(2, 1),
        (10, 6): Fraction(3, 1),
        (10, 99): Fraction(3, 1),
    }
    for key, value in expected.items():
        assert sharp_unit_cost_ratio(*key) == value


def test_sharp_ratio_witnesses_attain_bound_on_small_grid():
    for n in range(2, 11):
        for m in range(1, 8):
            receipt = sharp_unit_cost_ratio_receipt(n, m)
            assert receipt.upper_bound_attained
            assert receipt.witness_world_count == n
            assert receipt.witness_query_count == m
            assert receipt.witness_ratio == sharp_unit_cost_ratio(n, m)


def test_known_minimal_ratio_above_three_halves_is_immediate_corollary():
    for n in range(2, 6):
        for m in range(1, 8):
            assert sharp_unit_cost_ratio(n, m) <= Fraction(3, 2)
    for m in range(1, 4):
        for n in range(2, 12):
            assert sharp_unit_cost_ratio(n, m) <= Fraction(3, 2)
    assert sharp_unit_cost_ratio(6, 4) == Fraction(2, 1)
