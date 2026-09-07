from itertools import product

from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    fixed_budget_cover_decision,
    kernelized_fixed_budget_cover_decision,
    selected_policy_kernelized_gain_audit,
)
from adaptive_gain.witnesses import routing_bypass_control


def _kernel_compression_control():
    # Registered synthetic strict-gain benchmark discovered by seeded search.
    # Exact costs are C_A=3,C_F=4.  The unkernelized bounded-cover proof visits
    # 13 states at B=3; forced selection + dominance closes the kernelized
    # decision at the root without a genuine branch state.
    worlds = tuple(World(f"w{i}", 0 if i < 4 else 1) for i in range(8))
    maps = (
        (1, 1, 0, 1, 0, 1, 0, 1),
        (1, 1, 1, 0, 1, 1, 0, 0),
        (1, 1, 0, 1, 0, 1, 1, 1),
        (0, 0, 0, 0, 0, 0, 1, 1),
        (1, 1, 1, 0, 1, 1, 0, 0),
        (1, 0, 0, 0, 0, 0, 1, 1),
        (1, 0, 1, 1, 0, 1, 0, 0),
        (1, 1, 0, 0, 1, 0, 0, 0),
    )
    costs = (1, 1, 1, 1, 1, 1, 2, 1)
    return FiniteTask(
        worlds,
        tuple(Query(f"q{i}", cost, row) for i, (cost, row) in enumerate(zip(costs, maps))),
    )


def test_kernelization_preserves_strict_gain_decision_on_compression_control():
    task = _kernel_compression_control()
    exact = adaptive_gain_receipt(task)
    assert (exact.adaptive_cost, exact.fixed_cost) == (3, 4)

    baseline = fixed_budget_cover_decision(task, budget=3)
    kernel = kernelized_fixed_budget_cover_decision(task, budget=3)
    assert not baseline.fixed_resolver_exists_within_budget
    assert not kernel.fixed_resolver_exists_within_budget
    assert baseline.states_visited == 13
    assert kernel.kernel_calls == 1
    assert kernel.canonical_branch_states == 0
    assert kernel.forced_query_selections == 3
    assert kernel.dominated_query_removals == 3
    assert kernel.inactive_or_unaffordable_query_removals == 2
    assert selected_policy_kernelized_gain_audit(task).strict_adaptive_gain


def test_dominance_replaces_a_more_expensive_identical_separator():
    task = FiniteTask(
        (World("a", 0), World("b", 1)),
        (
            Query("expensive", 2, (0, 1)),
            Query("cheap", 1, (0, 1)),
        ),
    )
    result = kernelized_fixed_budget_cover_decision(task, budget=1)
    assert result.fixed_resolver_exists_within_budget
    assert result.feasible_bundle == ("cheap",)
    assert result.forced_query_selections == 1


def test_dominance_removes_equal_cost_strict_cover_subset():
    task = FiniteTask(
        (World("a", 0), World("b", 0), World("c", 1)),
        (
            Query("subset", 1, (0, 1, 1)),
            Query("superset", 1, (0, 0, 1)),
            Query("other", 1, (1, 0, 1)),
        ),
    )
    # subset covers only (a,c); superset covers both cross-target pairs.
    result = kernelized_fixed_budget_cover_decision(task, budget=1)
    assert result.fixed_resolver_exists_within_budget
    assert result.feasible_bundle == ("superset",)
    assert result.dominated_query_removals >= 1


def test_kernelized_solver_constructively_refuses_false_gain_on_bypass_control():
    task = routing_bypass_control()
    result = kernelized_fixed_budget_cover_decision(task, budget=2)
    assert result.fixed_resolver_exists_within_budget
    assert result.feasible_bundle is not None
    assert not selected_policy_kernelized_gain_audit(task).strict_adaptive_gain


def test_kernelized_decision_matches_exact_cost_class_on_complete_minimal_universe():
    targets = (0, 0, 1, 1)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    patterns = tuple(product((0, 1), repeat=4))
    strict = kernel_strict = false_positive = false_negative = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, outcomes) for j, outcomes in enumerate(maps)),
        )
        exact = adaptive_gain_receipt(task)
        actual = exact.strict_adaptive_gain
        predicted = False
        if exact.adaptive_cost is not None:
            predicted = not kernelized_fixed_budget_cover_decision(
                task, budget=exact.adaptive_cost
            ).fixed_resolver_exists_within_budget
        strict += int(actual)
        kernel_strict += int(predicted)
        false_positive += int(predicted and not actual)
        false_negative += int(actual and not predicted)
    assert strict == 192
    assert kernel_strict == 192
    assert false_positive == 0
    assert false_negative == 0
