from fractions import Fraction
from math import comb

from adaptive_gain.balanced_binary_eight_world_profile import (
    audit_eight_world_balanced_cut_cap,
    audit_exact_balanced_eight_world_sharp_profile,
    exact_balanced_eight_world_sharp_ratio,
    exact_balanced_eight_world_sharp_witness,
    exact_balanced_eight_world_three_query_task,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution


def test_eight_world_irredundant_balanced_cut_cap_is_five():
    receipt = audit_eight_world_balanced_cut_cap()
    assert receipt.theorem_holds
    assert receipt.world_count == 8
    assert receipt.balanced_cut_classes == 35
    assert receipt.six_cut_families_checked == comb(35, 6) == 1_623_160
    assert not receipt.any_irredundant_six_cut_family
    assert receipt.registered_five_cut_witness_irredundant
    assert receipt.maximum_irredundant_family_size == 5
    assert receipt.universal_fixed_cost_upper_bound == 5


def test_three_query_exact_balanced_witness_has_three_over_two_ratio():
    task = exact_balanced_eight_world_three_query_task()
    for query in task.queries:
        assert set(query.outcomes) <= {0, 1}
        assert sum(value == 0 for value in query.outcomes) == 4
        assert sum(value == 1 for value in query.outcomes) == 4
    assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 2
    assert fixed_minimum_resolution(task).minimum_cost == 3


def test_exact_balanced_eight_world_sharp_formula():
    expected = {
        1: Fraction(1, 1),
        2: Fraction(1, 1),
        3: Fraction(3, 2),
        4: Fraction(3, 2),
        5: Fraction(5, 3),
        6: Fraction(5, 3),
        7: Fraction(5, 3),
        8: Fraction(5, 3),
        20: Fraction(5, 3),
        100: Fraction(5, 3),
    }
    for query_count, ratio in expected.items():
        assert exact_balanced_eight_world_sharp_ratio(query_count) == ratio


def test_direct_sharp_witnesses_through_eight_queries():
    for query_count in range(1, 9):
        task = exact_balanced_eight_world_sharp_witness(query_count)
        assert len(task.queries) == query_count
        for query in task.queries:
            assert sum(value == 0 for value in query.outcomes) == 4
            assert sum(value == 1 for value in query.outcomes) == 4
        adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
        fixed = fixed_minimum_resolution(task).minimum_cost
        assert adaptive is not None and fixed is not None
        assert Fraction(fixed, adaptive) == exact_balanced_eight_world_sharp_ratio(query_count)


def test_eight_world_sharp_profile_audit_closes_all_declared_m():
    receipt = audit_exact_balanced_eight_world_sharp_profile()
    assert receipt.theorem_holds
    assert receipt.world_count == 8
    assert receipt.sharp_profile_prefix == (
        (1, Fraction(1, 1)),
        (2, Fraction(1, 1)),
        (3, Fraction(3, 2)),
        (4, Fraction(3, 2)),
        (5, Fraction(5, 3)),
    )
    assert receipt.all_m_at_least_five_ratio == Fraction(5, 3)
    assert receipt.fixed_cost_cap == 5
    assert receipt.three_query_witness_cost_pair == (2, 3)
    assert receipt.five_query_witness_cost_pair == (3, 5)
