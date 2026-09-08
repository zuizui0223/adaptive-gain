from fractions import Fraction

from adaptive_gain.balanced_binary_extremal_family import (
    balanced_binary_extremal_task,
    balanced_binary_family_audit,
    balanced_binary_family_counts,
    balanced_binary_ratio_lower_bound,
)


def test_balanced_binary_family_direct_small_depths():
    for depth in (1, 2, 3):
        receipt = balanced_binary_family_audit(depth, direct_check=True)
        k = 1 << depth
        assert receipt.theorem_holds
        assert receipt.branch_count == k
        assert receipt.world_count == 2 * k + 2
        assert receipt.query_count == depth + k
        assert receipt.adaptive_upper_bound == depth + 1
        assert receipt.fixed_lower_bound == k
        assert receipt.ratio_lower_bound == Fraction(k, depth + 1)
        assert receipt.all_queries_balanced
        assert receipt.every_terminal_uniquely_mandatory
        assert receipt.direct_bounds_hold
        assert receipt.direct_adaptive_cost is not None
        assert receipt.direct_adaptive_cost <= depth + 1
        assert receipt.direct_fixed_cost is not None
        assert receipt.direct_fixed_cost >= k


def test_every_explicit_query_is_binary_and_exactly_balanced():
    for depth in (1, 2, 3):
        task = balanced_binary_extremal_task(depth)
        for query in task.queries:
            assert set(query.outcomes) <= {0, 1}
            zeros = sum(outcome == 0 for outcome in query.outcomes)
            ones = sum(outcome == 1 for outcome in query.outcomes)
            assert zeros == ones


def test_balanced_binary_ratio_lower_bound_is_unbounded_analytically():
    depths = (1, 2, 3, 4, 6, 8)
    ratios = [balanced_binary_ratio_lower_bound(depth) for depth in depths]
    assert ratios == [
        Fraction(1, 1),
        Fraction(4, 3),
        Fraction(2, 1),
        Fraction(16, 5),
        Fraction(64, 7),
        Fraction(256, 9),
    ]
    assert ratios == sorted(ratios)


def test_large_family_counts_do_not_require_exact_solver_materialization():
    k, worlds, queries = balanced_binary_family_counts(8)
    assert k == 256
    assert worlds == 514
    assert queries == 264
    assert balanced_binary_ratio_lower_bound(8) == Fraction(256, 9)


def test_explicit_task_fails_closed_above_exact_query_cap():
    try:
        balanced_binary_extremal_task(4)  # 4 + 16 = 20, still allowed
    except ValueError:
        raise AssertionError("depth four should still fit the 20-query FiniteTask cap")
    try:
        balanced_binary_extremal_task(5)  # 5 + 32 > 20
    except ValueError:
        pass
    else:
        raise AssertionError("large explicit balanced family should fail closed above solver cap")
