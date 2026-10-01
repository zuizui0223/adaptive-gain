from fractions import Fraction

from adaptive_gain.exact_balanced_routeability_stress_test import (
    exact_balanced_control_stress_task,
    exact_balanced_routeable_stress_task,
    exact_balanced_stress_test_audit,
)


def test_exact_balanced_stress_test_closes_costs_and_accuracy_ceiling():
    receipt = exact_balanced_stress_test_audit()

    assert receipt.theorem_holds
    assert receipt.world_count == 10
    assert receipt.query_count == 6
    assert receipt.all_queries_exactly_balanced
    assert receipt.same_query_matrix
    assert receipt.same_target_multiplicities

    assert receipt.routeable_adaptive_cost == 3
    assert receipt.routeable_fixed_cost == 4
    assert receipt.control_adaptive_cost == 2
    assert receipt.control_fixed_cost == 2

    assert receipt.common_budget == 3
    assert receipt.routeable_contingent_accuracy_ceiling == Fraction(1, 1)
    assert receipt.routeable_best_fixed_accuracy_ceiling == Fraction(4, 5)
    assert receipt.control_contingent_accuracy_ceiling == Fraction(1, 1)
    assert receipt.control_best_fixed_accuracy_ceiling == Fraction(1, 1)
    assert receipt.architecture_access_interaction_ceiling == Fraction(1, 5)


def test_stress_test_changes_target_map_only():
    routeable = exact_balanced_routeable_stress_task()
    control = exact_balanced_control_stress_task()

    assert routeable.queries == control.queries
    assert tuple(w.name for w in routeable.worlds) == tuple(w.name for w in control.worlds)
    assert tuple(w.target for w in routeable.worlds) != tuple(
        w.target for w in control.worlds
    )


def test_all_six_queries_are_exactly_five_five():
    task = exact_balanced_routeable_stress_task()
    for query in task.queries:
        assert sum(outcome == 0 for outcome in query.outcomes) == 5
        assert sum(outcome == 1 for outcome in query.outcomes) == 5


def test_routeable_fixed_three_query_ceiling_is_eighty_percent():
    receipt = exact_balanced_stress_test_audit()
    assert receipt.routeable_best_fixed_bundles
    assert all(len(bundle) == 3 for bundle in receipt.routeable_best_fixed_bundles)
    assert receipt.routeable_best_fixed_accuracy_ceiling == Fraction(4, 5)


def test_control_has_perfect_fixed_three_query_bundle():
    receipt = exact_balanced_stress_test_audit()
    assert receipt.control_best_fixed_bundles
    assert any(
        {"route_bit_0", "route_bit_1"}.issubset(set(bundle))
        for bundle in receipt.control_best_fixed_bundles
    )
    assert receipt.control_best_fixed_accuracy_ceiling == Fraction(1, 1)
