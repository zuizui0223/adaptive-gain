from fractions import Fraction

from adaptive_gain.balanced_binary_ten_world_profile import (
    audit_exact_balanced_ten_world_sharp_profile,
    audit_ten_world_no_depth_three_fixed_seven,
    exact_balanced_ten_world_five_query_task,
    exact_balanced_ten_world_sharp_ratio,
    exact_balanced_ten_world_sharp_witness,
    exact_balanced_ten_world_six_query_task,
    exact_balanced_ten_world_three_query_task,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution


def _pair(task):
    return (
        adaptive_minimum_resolution(task).minimum_worst_path_cost,
        fixed_minimum_resolution(task).minimum_cost,
    )


def _balanced(task):
    return all(
        set(query.outcomes) <= {0, 1}
        and sum(value == 0 for value in query.outcomes) == 5
        and sum(value == 1 for value in query.outcomes) == 5
        for query in task.queries
    )


def test_registered_ten_world_witnesses_have_expected_cost_pairs():
    three = exact_balanced_ten_world_three_query_task()
    five = exact_balanced_ten_world_five_query_task()
    six = exact_balanced_ten_world_six_query_task()
    assert _pair(three) == (2, 3)
    assert _pair(five) == (3, 5)
    assert _pair(six) == (3, 6)
    assert _balanced(three)
    assert _balanced(five)
    assert _balanced(six)


def test_depth_three_fixed_seven_is_impossible_under_exact_balance():
    receipt = audit_ten_world_no_depth_three_fixed_seven()
    assert receipt.left_half_states == 2944
    assert receipt.right_half_states == 2944
    assert receipt.complementary_balance_pairs == 0
    assert not receipt.depth_three_fixed_seven_possible
    assert receipt.theorem_holds


def test_ten_world_sharp_profile_formula():
    expected = {
        1: Fraction(1, 1),
        2: Fraction(1, 1),
        3: Fraction(3, 2),
        4: Fraction(3, 2),
        5: Fraction(5, 3),
        6: Fraction(2, 1),
        7: Fraction(2, 1),
        8: Fraction(2, 1),
        9: Fraction(2, 1),
        12: Fraction(2, 1),
    }
    for query_count, ratio in expected.items():
        assert exact_balanced_ten_world_sharp_ratio(query_count) == ratio


def test_explicit_witnesses_attain_profile_through_nine_queries():
    for query_count in range(1, 10):
        task = exact_balanced_ten_world_sharp_witness(query_count)
        adaptive, fixed = _pair(task)
        assert adaptive is not None
        assert fixed is not None
        assert _balanced(task)
        assert Fraction(fixed, adaptive) == exact_balanced_ten_world_sharp_ratio(query_count)


def test_ten_world_profile_audit_closes_all_declared_query_counts():
    receipt = audit_exact_balanced_ten_world_sharp_profile()
    assert receipt.world_count == 10
    assert receipt.fixed_cost_cap == 7
    assert receipt.three_query_witness_cost_pair == (2, 3)
    assert receipt.five_query_witness_cost_pair == (3, 5)
    assert receipt.six_query_witness_cost_pair == (3, 6)
    assert receipt.sharp_profile_prefix == (
        (1, Fraction(1, 1)),
        (2, Fraction(1, 1)),
        (3, Fraction(3, 2)),
        (4, Fraction(3, 2)),
        (5, Fraction(5, 3)),
        (6, Fraction(2, 1)),
    )
    assert receipt.all_m_at_least_six_ratio == Fraction(2, 1)
    assert receipt.obstruction_left_states == 2944
    assert receipt.obstruction_right_states == 2944
    assert receipt.theorem_holds
