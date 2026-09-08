from adaptive_gain.bounded_arity_extremal_bounds import sharp_bounded_arity_unit_cost_ratio
from adaptive_gain.global_once_policy_semantics import (
    GlobalOnceSearchLimitError,
    global_label_once_adaptive_minimum_resolution,
    global_once_containment_counterexample_audit,
    global_once_containment_counterexample_task,
    sharp_global_once_unit_cost_ratio,
    sharp_global_once_unit_cost_ratio_receipt,
)


def test_global_label_once_can_exclude_a_feasible_fixed_bundle():
    receipt = global_once_containment_counterexample_audit()
    assert receipt.standard_adaptive_cost == 2
    assert receipt.fixed_cost == 2
    assert receipt.global_once_adaptive_cost is None
    assert receipt.fixed_bundle_exists
    assert not receipt.global_once_tree_exists
    assert receipt.ordinary_containment_holds
    assert receipt.global_once_containment_fails


def test_counterexample_exact_solver_has_no_global_once_plan():
    task = global_once_containment_counterexample_task()
    receipt = global_label_once_adaptive_minimum_resolution(task)
    assert receipt.minimum_worst_path_cost is None
    assert receipt.selected_policy is None
    assert receipt.globally_used_queries == ()


def test_global_once_extremal_ratio_matches_bounded_arity_on_small_grid():
    for n in range(2, 7):
        for m in range(1, 6):
            for b in (2, 3):
                expected = sharp_bounded_arity_unit_cost_ratio(n, m, b)
                assert sharp_global_once_unit_cost_ratio(n, m, b) == expected
                receipt = sharp_global_once_unit_cost_ratio_receipt(
                    n, m, b, direct_check=True
                )
                assert receipt.theorem_holds
                assert receipt.witness_uses_each_query_once_globally
                assert receipt.witness_ratio == expected


def test_exact_solver_fails_closed_above_declared_query_cap():
    task = global_once_containment_counterexample_task()
    try:
        global_label_once_adaptive_minimum_resolution(task, max_queries=1)
    except GlobalOnceSearchLimitError:
        pass
    else:
        raise AssertionError("global-once solver must fail closed above its query cap")
