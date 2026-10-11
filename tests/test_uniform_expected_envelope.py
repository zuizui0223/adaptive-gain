import math

import pytest

from adaptive_gain.core import FiniteTask, Query, World, fixed_minimum_resolution
from adaptive_gain.bounded_arity_extremal_bounds import BoundedArityTree, _tree_task
from adaptive_gain.policy_fitness import discounted_fitness_optimal_policy
from adaptive_gain.uniform_expected_envelope import (
    _binary_leaf_depth_profiles,
    exact_uniform_expected_envelope,
    exact_uniform_expected_witness,
)


def exponential(mu):
    return lambda c: math.exp(-mu * c)


def test_canonical_uniform_envelope_is_sharp_and_below_frequency_floor_bound():
    receipt = exact_uniform_expected_envelope(10, 9, exponential(0.3))
    assert receipt.optimal_fixed_cost == 6
    assert receipt.duplicate_world_count == 3
    assert receipt.optimal_leaf_depths == (1, 3, 3, 4, 4, 4, 4)
    assert receipt.evaluated_depth_profiles == 115
    assert receipt.optimal_expected_gain == pytest.approx(0.3328200167641013)
    assert receipt.optimal_expected_gain < 0.5008067818130457
    assert receipt.optimal_expected_gain < math.exp(-0.3) - math.exp(-2.7)


def test_explicit_uniform_witness_attains_combinatorial_envelope():
    mu = 0.3
    receipt = exact_uniform_expected_envelope(10, 9, exponential(mu))
    task = exact_uniform_expected_witness(receipt)
    fixed = fixed_minimum_resolution(task)
    assert fixed.minimum_cost == receipt.optimal_fixed_cost
    assert len(task.worlds) == 10
    assert len(task.queries) == 9
    assert all(len(set(q.outcomes)) <= 2 for q in task.queries)

    probabilities = (0.1,) * 10
    selected = discounted_fitness_optimal_policy(
        task, probabilities, discount_rate=mu
    )
    assert selected.selected_policy is not None
    realized = (
        selected.expected_discounted_completion_value
        - math.exp(-mu * fixed.minimum_cost)
    )
    assert realized == pytest.approx(receipt.optimal_expected_gain, abs=1e-11)


def test_one_world_per_terminal_restriction_reduces_the_maximum():
    mu = 0.3
    allowed = exact_uniform_expected_envelope(10, 9, exponential(mu))
    restricted = exact_uniform_expected_envelope(
        10, 9, exponential(mu), one_world_per_terminal=True
    )
    assert restricted.duplicate_world_count == 0
    assert restricted.optimal_fixed_cost == 9
    assert restricted.optimal_leaf_depths == (3, 3, 3, 3, 3, 3, 4, 4, 4, 4)
    assert restricted.optimal_expected_gain == pytest.approx(0.29721396786949056)
    assert allowed.optimal_expected_gain - restricted.optimal_expected_gain == pytest.approx(
        0.03560604889461072
    )


@pytest.mark.parametrize(
    ("mu", "fixed"),
    [(0.1, 9), (0.2, 9), (0.3, 6), (0.5, 4), (1.0, 3)],
)
def test_ecological_urgency_reranks_optimal_structural_burden(mu, fixed):
    receipt = exact_uniform_expected_envelope(10, 9, exponential(mu))
    assert receipt.optimal_fixed_cost == fixed


def test_independent_witness_receipts_across_small_binary_world_budgets():
    for n in range(2, 9):
        receipt = exact_uniform_expected_envelope(n, n - 1, exponential(0.4))
        task = exact_uniform_expected_witness(receipt)
        assert fixed_minimum_resolution(task).minimum_cost == receipt.optimal_fixed_cost
        assert len(task.worlds) == n
        assert len(task.queries) == n - 1
        assert all(len(set(q.outcomes)) <= 2 for q in task.queries)


def test_monotone_step_and_linear_values_supported():
    for value in (
        lambda c: -c,
        lambda c: 1.0 if c <= 2 else 0.0,
        lambda c: 1.0 / (1.0 + c),
    ):
        receipt = exact_uniform_expected_envelope(6, 5, value)
        task = exact_uniform_expected_witness(receipt)
        assert fixed_minimum_resolution(task).minimum_cost == receipt.optimal_fixed_cost
        assert receipt.optimal_expected_gain >= -1e-12


def test_scope_rejects_underspecified_query_budget_and_nonmonotone_value():
    with pytest.raises(ValueError, match="query_count"):
        exact_uniform_expected_envelope(10, 8, exponential(0.3))
    with pytest.raises(ValueError, match="nonincreasing"):
        exact_uniform_expected_envelope(5, 4, lambda c: c)
    with pytest.raises(ValueError, match="between 2 and 14"):
        exact_uniform_expected_envelope(15, 14, exponential(0.3))


def test_depth_profile_recursion_includes_all_full_binary_tree_shapes_for_n4():
    # Four leaves permit the balanced shape (2,2,2,2) and the caterpillar
    # shape (1,2,3,3), up to ordering/mirroring of leaves.
    assert set(_binary_leaf_depth_profiles(4)) == {
        (2, 2, 2, 2),
        (1, 2, 3, 3),
    }



def test_uniform_world_and_balanced_target_prevalence_still_allow_large_gain():
    # A concrete eight-terminal private-pair tree with target counts 3:5.
    # Two target-0 exact twins of its one-step world make ten equiprobable
    # represented worlds and exactly balanced target prevalence 5:5.
    shape = (
        None,
        (
            (None, (None, None)),
            (((None, None), None), None),
        ),
    )

    def make_tree(shape):
        if shape is None:
            return BoundedArityTree()
        return BoundedArityTree(tuple(make_tree(x) for x in shape))

    base, mandatory = _tree_task(make_tree(shape), 8, 7)
    assert mandatory == 7
    assert sum(w.target == 0 for w in base.worlds) == 3
    assert sum(w.target == 1 for w in base.worlds) == 5

    worlds = list(base.worlds) + [
        World("same_easy_world_1", base.worlds[0].target),
        World("same_easy_world_2", base.worlds[0].target),
    ]
    queries = [
        Query(
            q.name, q.cost,
            q.outcomes + (q.outcomes[0], q.outcomes[0]),
        )
        for q in base.queries
    ]
    task = FiniteTask(tuple(worlds), tuple(queries))
    assert len(task.worlds) == 10
    assert sum(w.target == 0 for w in task.worlds) == 5
    assert sum(w.target == 1 for w in task.worlds) == 5

    fixed = fixed_minimum_resolution(task)
    assert fixed.minimum_cost == 7

    mu = 0.3
    selected = discounted_fitness_optimal_policy(
        task, (0.1,) * 10, discount_rate=mu
    )
    assert selected.selected_policy is not None
    realized_gain = (
        selected.expected_discounted_completion_value
        - math.exp(-mu * fixed.minimum_cost)
    )

    # This is an explicit lower bound, NOT an assertion of global sharpness
    # over all balanced-target finite information architectures.
    assert realized_gain >= 0.3160872655029999 - 1e-12
    assert realized_gain <= 0.3328200167641013 + 1e-12
