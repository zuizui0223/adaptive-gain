from fractions import Fraction

from adaptive_gain.binary_unit_cost_extremal_bounds import (
    binary_tree_fixed_cost_bound,
    sharp_binary_unit_cost_ratio,
    sharp_binary_unit_cost_ratio_receipt,
    threshold_path_task,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution


def test_threshold_path_exact_costs_for_small_world_counts():
    for n in range(2, 11):
        task = threshold_path_task(n)
        ca = adaptive_minimum_resolution(task).minimum_worst_path_cost
        cf = fixed_minimum_resolution(task).minimum_cost
        assert ca == (n - 1).bit_length()
        assert cf == n - 1


def test_binary_tree_union_bound_special_cases():
    assert binary_tree_fixed_cost_bound(100, 100, 1) == 1
    assert binary_tree_fixed_cost_bound(100, 100, 2) == 3
    assert binary_tree_fixed_cost_bound(100, 100, 3) == 7
    assert binary_tree_fixed_cost_bound(6, 5, 3) == 5
    assert binary_tree_fixed_cost_bound(6, 4, 3) == 4


def test_sharp_binary_formula_known_values():
    expected = {
        (2, 1): Fraction(1, 1),
        (4, 3): Fraction(3, 2),
        (4, 10): Fraction(3, 2),
        (5, 10): Fraction(3, 2),
        (6, 4): Fraction(3, 2),
        (6, 5): Fraction(5, 3),
        (7, 6): Fraction(2, 1),
        (8, 7): Fraction(7, 3),
        (10, 7): Fraction(7, 3),
        (10, 9): Fraction(7, 3),
        (11, 10): Fraction(5, 2),
    }
    for key, value in expected.items():
        assert sharp_binary_unit_cost_ratio(*key) == value


def test_sharp_binary_witnesses_attain_bound_on_small_grid():
    for n in range(2, 11):
        for m in range(1, 9):
            receipt = sharp_binary_unit_cost_ratio_receipt(n, m)
            assert receipt.upper_bound_attained
            assert receipt.witness_ratio == sharp_binary_unit_cost_ratio(n, m)


def test_first_binary_scope_above_three_halves():
    for n in range(2, 6):
        for m in range(1, 10):
            assert sharp_binary_unit_cost_ratio(n, m) <= Fraction(3, 2)
    for m in range(1, 5):
        for n in range(2, 12):
            assert sharp_binary_unit_cost_ratio(n, m) <= Fraction(3, 2)
    assert sharp_binary_unit_cost_ratio(6, 5) == Fraction(5, 3)
