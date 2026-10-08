"""Sharp scalable expected-value limits under fixed binary-target prevalence."""
import math

import pytest

from adaptive_gain.bounded_arity_extremal_bounds import (
    ternary_target_balance_expected_witness,
    finite_expected_ceiling_witness,
    two_shallow_leaf_expected_value_witness,
    finite_target_prevalence_ternary_witness,
)
from adaptive_gain.core import fixed_minimum_resolution
from adaptive_gain.policy_fitness import discounted_fitness_optimal_policy
from adaptive_gain.target_prevalence_capacity import (
    finite_ternary_capacity_premium_prevalence_interval,
    finite_ternary_only_prevalence_interval,
    exponential_target_prevalence_expected_capacity,
    exponential_minimum_expected_arity_with_target_prevalence,
    minimum_expected_cue_arity_with_target_prevalence,
    target_prevalence_expected_capacity,
    finite_target_prevalence_expected_capacity,
    finite_minimum_expected_cue_arity_with_target_prevalence,
)


def _balanced_target_world_probabilities(task, rare_mass=0.01):
    """Exactly half of probability on each target, all represented worlds positive."""
    assert task.worlds[0].target != task.worlds[1].target
    probs = [0.5 - rare_mass / 2.0, 0.5 - rare_mass / 2.0]
    for target in (task.worlds[0].target, task.worlds[1].target):
        assert any(w.target == target for w in task.worlds[2:])
    for world in task.worlds[2:]:
        within_target = sum(w.target == world.target for w in task.worlds[2:])
        probs.append((rare_mass / 2.0) / within_target)

    assert len(probs) == len(task.worlds)
    assert sum(probs) == pytest.approx(1.0)
    assert all(p > 0 for p in probs)
    for target in (task.worlds[0].target, task.worlds[1].target):
        assert sum(
            p for p, world in zip(probs, task.worlds) if world.target == target
        ) == pytest.approx(0.5)
    return probs


def test_balanced_target_prevalence_restores_arity_gap():
    mu = 0.3
    binary = exponential_target_prevalence_expected_capacity(
        0.5,
        closure_rate=mu,
        resolution_value=1.0,
        max_arity=2,
    )
    ternary = exponential_target_prevalence_expected_capacity(
        0.5,
        closure_rate=mu,
        resolution_value=1.0,
        max_arity=3,
    )
    u1 = math.exp(-mu)
    u2 = math.exp(-2 * mu)
    assert binary.binary_ceiling == pytest.approx((u1 + u2) / 2)
    assert binary.selected_arity_ceiling == pytest.approx(0.6448149283888872)
    assert ternary.selected_arity_ceiling == pytest.approx(u1)
    assert ternary.selected_arity_ceiling > binary.selected_arity_ceiling


def test_exact_minimum_arity_with_balanced_target_and_strict_cost():
    kwargs = dict(closure_rate=0.3, resolution_value=1.0)
    assert exponential_minimum_expected_arity_with_target_prevalence(
        0.62, 0.5, **kwargs
    ) == 2
    assert exponential_minimum_expected_arity_with_target_prevalence(
        0.68, 0.5, **kwargs
    ) == 3
    assert exponential_minimum_expected_arity_with_target_prevalence(
        math.exp(-0.3), 0.5, **kwargs
    ) is None

    at_binary = (math.exp(-0.3) + math.exp(-0.6)) / 2
    assert exponential_minimum_expected_arity_with_target_prevalence(
        at_binary, 0.5, **kwargs
    ) == 3


def test_skewed_target_prevalence_can_make_binary_sufficient():
    mu = 0.3
    balanced = exponential_target_prevalence_expected_capacity(
        0.5, closure_rate=mu, max_arity=2
    )
    skewed = exponential_target_prevalence_expected_capacity(
        0.9, closure_rate=mu, max_arity=2
    )
    assert skewed.binary_ceiling > balanced.binary_ceiling
    assert exponential_minimum_expected_arity_with_target_prevalence(
        0.68, 0.9, closure_rate=mu
    ) == 2


def test_ternary_private_pair_witness_is_exact_and_target_marginal_can_be_balanced():
    task = ternary_target_balance_expected_witness(rare_depth=3)
    assert len(task.worlds) == 10
    assert len(task.queries) == 8
    assert len(set(task.queries[0].outcomes)) == 3
    assert all(len(set(q.outcomes)) <= 3 for q in task.queries)
    assert fixed_minimum_resolution(task).minimum_cost == 8
    _balanced_target_world_probabilities(task)


def test_finite_ternary_witness_pays_cost_impossible_for_any_balanced_binary_task():
    mu, rare_mass, cost = 0.3, 0.01, 0.68
    depth = 4
    task = ternary_target_balance_expected_witness(rare_depth=depth)
    _balanced_target_world_probabilities(task, rare_mass=rare_mass)
    assert len(task.worlds) == 18
    assert len(task.queries) == 16

    # Explicit root-then-rare-subtree policy has depth 1 in both pure classes,
    # and depth (1+depth) in the rare branch. Every query is fixed mandatory
    # by the private-pair construction audited by the witness factory.
    expected_ternary = (
        (1.0 - rare_mass) * math.exp(-mu)
        + rare_mass * math.exp(-mu * (depth + 1))
    )
    ternary_advantage = expected_ternary - math.exp(-mu * len(task.queries))
    binary_global_bound = (
        math.exp(-mu) + math.exp(-2.0 * mu)
    ) / 2.0
    assert binary_global_bound < cost
    assert ternary_advantage > cost


def test_binary_root_cannot_offer_two_pure_target_outcomes_and_a_mixed_one():
    # A binary root may resolve the majority target after one step and the
    # minority after two. The rare branch preserves a large fixed burden.
    task = two_shallow_leaf_expected_value_witness(rare_depth=3)
    assert len(set(task.queries[0].outcomes)) == 2
    _balanced_target_world_probabilities(task)
    fixed = fixed_minimum_resolution(task)
    assert fixed.minimum_cost == len(task.queries)


def test_capacity_value_monotonicity_and_probability_validation():
    with pytest.raises(ValueError):
        target_prevalence_expected_capacity(
            0.0, value_at_one=1.0, value_at_two=0.5,
            limiting_value=0.0, max_arity=2
        )
    with pytest.raises(ValueError):
        target_prevalence_expected_capacity(
            0.5, value_at_one=0.2, value_at_two=0.5,
            limiting_value=0.0, max_arity=2
        )
    with pytest.raises(ValueError):
        target_prevalence_expected_capacity(
            0.5, value_at_one=1.0, value_at_two=0.5,
            limiting_value=0.0, max_arity=1
        )


def test_general_monotone_capacity_inverts_expected_arity():
    assert minimum_expected_cue_arity_with_target_prevalence(
        0.7, 0.5,
        value_at_one=1.0,
        value_at_two=0.5,
        limiting_value=0.0,
    ) == 2
    assert minimum_expected_cue_arity_with_target_prevalence(
        0.8, 0.5,
        value_at_one=1.0,
        value_at_two=0.5,
        limiting_value=0.0,
    ) == 3
    assert minimum_expected_cue_arity_with_target_prevalence(
        1.0, 0.5,
        value_at_one=1.0,
        value_at_two=0.5,
        limiting_value=0.0,
    ) is None



def test_four_world_two_query_minimal_target_balanced_arity_separation():
    mu, cost = 0.3, 0.14
    task = ternary_target_balance_expected_witness(rare_depth=1)

    assert len(task.worlds) == 4
    assert len(task.queries) == 2
    assert len(set(task.queries[0].outcomes)) == 3
    assert fixed_minimum_resolution(task).minimum_cost == 2

    probs = [0.45, 0.45, 0.05, 0.05]
    for target in (task.worlds[0].target, task.worlds[1].target):
        assert sum(
            p for p, world in zip(probs, task.worlds)
            if world.target == target
        ) == pytest.approx(0.5)

    policy = discounted_fitness_optimal_policy(
        task,
        probs,
        discount_rate=mu,
    )
    fixed_value = math.exp(-2.0 * mu)
    advantage = policy.expected_discounted_completion_value - fixed_value

    explicit = 0.9 * (math.exp(-mu) - math.exp(-2.0 * mu))
    binary_global_upper = 0.5 * (math.exp(-mu) - math.exp(-2.0 * mu))

    assert advantage >= explicit - 1e-12
    assert binary_global_upper < cost < explicit


def test_binary_four_world_two_query_witness_respects_class_balance():
    task = finite_expected_ceiling_witness(4, 2)
    assert all(len(set(q.outcomes)) <= 2 for q in task.queries)
    assert fixed_minimum_resolution(task).minimum_cost == 2

    # The first world and the padded fourth world share the root-pure
    # target; leaf 2 is a rare same-target world in the mixed branch.
    labels = [w.target for w in task.worlds]
    assert labels[0] == labels[2] == labels[3]
    assert labels[1] != labels[0]
    probs = [0.4, 0.5, 0.05, 0.05]
    assert sum(p for p, y in zip(probs, labels) if y == labels[0]) == pytest.approx(0.5)

    value = discounted_fitness_optimal_policy(task, probs, discount_rate=0.3)
    gain = value.expected_discounted_completion_value - math.exp(-0.6)
    assert gain <= 0.5 * (math.exp(-0.3) - math.exp(-0.6)) + 1e-12



def test_sharp_finite_target_prevalence_frontier_binary_vs_ternary():
    value = lambda c: math.exp(-0.3 * c)
    binary = finite_target_prevalence_expected_capacity(
        10, 9, 0.5, max_arity=2, completion_value=value
    )
    ternary = finite_target_prevalence_expected_capacity(
        10, 9, 0.5, max_arity=3, completion_value=value
    )
    binary_exact = (
        0.5 * (math.exp(-0.3) + math.exp(-0.6))
        - math.exp(-2.7)
    )
    ternary_exact = math.exp(-0.3) - math.exp(-2.4)

    assert binary.expected_value_supremum == pytest.approx(binary_exact)
    assert binary_exact == pytest.approx(0.5776094156481224)
    assert ternary.expected_value_supremum == pytest.approx(ternary_exact)
    assert ternary_exact == pytest.approx(0.6501002673923054)
    assert binary.expected_value_supremum < 0.62
    assert ternary.expected_value_supremum > 0.62
    assert finite_minimum_expected_cue_arity_with_target_prevalence(
        10, 9, 0.5, 0.62, completion_value=value
    ) == 3


def test_finite_prevalence_frontier_can_prefer_binary_structure_even_with_ternary_available():
    value = lambda c: math.exp(-0.3 * c)
    receipt = finite_target_prevalence_expected_capacity(
        4, 3, 0.9, max_arity=3, completion_value=value
    )
    assert receipt.binary_supr > receipt.two_target_pure_root_supr
    assert receipt.expected_value_supremum == pytest.approx(receipt.binary_supr)
    assert receipt.maximizing_root_pattern == (
        "one_target_pure_root_outcome_plus_rare_mixed"
    )


def test_finite_ternary_private_pair_builder_attains_all_small_cost_budgets():
    for n in range(4, 9):
        for m in range(2, 7):
            task = finite_target_prevalence_ternary_witness(n, m)
            assert len(task.worlds) == n
            assert len(task.queries) == m
            assert all(len(set(q.outcomes)) <= 3 for q in task.queries)
            assert len(set(task.queries[0].outcomes)) == 3
            assert task.worlds[0].target != task.worlds[1].target
            assert {w.target for w in task.worlds[2:]} == {
                task.worlds[0].target, task.worlds[1].target
            }
            assert fixed_minimum_resolution(task).minimum_cost == min(m, n - 2)


def test_finite_balanced_ternary_witness_beats_binary_impossibility_at_same_nm():
    mu = 0.3
    k = 0.62
    task = finite_target_prevalence_ternary_witness(10, 9)
    assert fixed_minimum_resolution(task).minimum_cost == 8
    probabilities = _balanced_target_world_probabilities(
        task, rare_mass=0.02
    )

    # Even the declared tree's conservative worst rare-branch bound suffices.
    # All frequent worlds finish at depth one; rare worlds take at most 8.
    conservative = (
        0.98 * math.exp(-mu)
        + 0.02 * math.exp(-mu * 8)
        - math.exp(-mu * 8)
    )
    binary_upper = finite_target_prevalence_expected_capacity(
        10, 9, 0.5,
        max_arity=2,
        completion_value=lambda t: math.exp(-mu * t)
    ).expected_value_supremum
    assert binary_upper < k < conservative

    policy = discounted_fitness_optimal_policy(
        task, probabilities, discount_rate=mu
    )
    actual = policy.expected_discounted_completion_value - math.exp(-mu * 8)
    assert actual >= conservative - 1e-12
    assert actual > k


def test_finite_target_prevalence_edge_cases():
    value = lambda c: math.exp(-0.3 * c)
    for b in (2,3,4):
        assert finite_target_prevalence_expected_capacity(
            5, 1, 0.5, max_arity=b, completion_value=value
        ).expected_value_supremum == pytest.approx(0.0)
    n3binary = finite_target_prevalence_expected_capacity(
        3, 2, 0.5, max_arity=2, completion_value=value
    )
    n3ternary = finite_target_prevalence_expected_capacity(
        3, 2, 0.5, max_arity=3, completion_value=value
    )
    assert n3binary.expected_value_supremum == pytest.approx(
        n3ternary.expected_value_supremum
    )



def test_independent_exhaustive_four_world_two_query_target_balance():
    """Exhaust every 4-world two-query table independently of repo solvers.

    The supremum over positive world frequencies with a 50:50 binary-target
    marginal is approached by concentrating probability 0.5 on one world of
    each target. Because expected value is linear in those probabilities for
    each fixed policy, it suffices to inspect these extreme pairs.
    """
    from itertools import combinations, product

    mu = 0.3
    u1 = math.exp(-mu)
    u2 = math.exp(-2 * mu)

    def resolves(queries, labels):
        signatures = {}
        for i in range(4):
            signature = tuple(q[i] for q in queries)
            if signature in signatures and signatures[signature] != labels[i]:
                return False
            signatures[signature] = labels[i]
        return True

    results = {}
    for arity in (2, 3):
        patterns = [
            q for q in product(range(arity), repeat=4)
            if len(set(q)) > 1
        ]
        best = float("-inf")
        considered = 0

        for qa, qb in combinations(patterns, 2):
            if qa == qb:
                continue
            for labels in product((0, 1), repeat=4):
                if len(set(labels)) != 2 or not resolves((qa, qb), labels):
                    continue
                fixed_cost = (
                    1 if resolves((qa,), labels) or resolves((qb,), labels)
                    else 2
                )
                for root in (qa, qb):
                    pure_at_root = {}
                    for outcome in set(root):
                        cell = [i for i in range(4) if root[i] == outcome]
                        pure_at_root[outcome] = len({
                            labels[i] for i in cell
                        }) == 1
                    for a in range(4):
                        if labels[a] != 0:
                            continue
                        for b in range(4):
                            if labels[b] != 1:
                                continue
                            p1 = 0.5 * int(pure_at_root[root[a]]) + (
                                0.5 * int(pure_at_root[root[b]])
                            )
                            value = (
                                p1 * u1 + (1.0 - p1) * u2
                                - math.exp(-mu * fixed_cost)
                            )
                            best = max(best, value)
                            considered += 1

        results[arity] = (best, considered)

    binary_theory = finite_target_prevalence_expected_capacity(
        4, 2, 0.5, max_arity=2,
        completion_value=lambda t: math.exp(-mu * t)
    ).expected_value_supremum
    ternary_theory = finite_target_prevalence_expected_capacity(
        4, 2, 0.5, max_arity=3,
        completion_value=lambda t: math.exp(-mu * t)
    ).expected_value_supremum

    assert results[2][1] > 0
    assert results[3][1] > results[2][1]
    assert results[2][0] == pytest.approx(binary_theory, abs=1e-12)
    assert results[3][0] == pytest.approx(ternary_theory, abs=1e-12)



def test_finite_prevalence_arity_transition_window_exact_canonical():
    mu, cost = 0.3, 0.62
    val = lambda c: math.exp(-mu * c)
    receipt = finite_ternary_only_prevalence_interval(
        10, 9, cost, completion_value=val
    )
    assert receipt.target_one_probability_interval is not None
    lo, hi = receipt.target_one_probability_interval
    assert lo == pytest.approx(0.2792232779781706)
    assert hi == pytest.approx(0.7207767220218294)
    assert receipt.majority_target_probability_max == pytest.approx(hi)
    assert lo == pytest.approx(1.0 - hi)

    for p in (0.5, 0.6, 0.7, 0.72, lo, hi):
        binary = finite_target_prevalence_expected_capacity(
            10, 9, p, max_arity=2, completion_value=val
        )
        ternary = finite_target_prevalence_expected_capacity(
            10, 9, p, max_arity=3, completion_value=val
        )
        assert binary.expected_value_supremum <= cost + 1e-12
        assert ternary.expected_value_supremum > cost

    for p in (0.25, 0.73, 0.8, 0.9):
        binary = finite_target_prevalence_expected_capacity(
            10, 9, p, max_arity=2, completion_value=val
        )
        assert binary.expected_value_supremum > cost


def test_finite_prevalence_arity_transition_absent_if_binary_already_pays():
    val = lambda c: math.exp(-0.3 * c)
    receipt = finite_ternary_only_prevalence_interval(
        10, 9, 0.55, completion_value=val
    )
    assert receipt.target_one_probability_interval is None


def test_finite_prevalence_arity_transition_absent_if_ternary_cannot_pay():
    val = lambda c: math.exp(-0.3 * c)
    receipt = finite_ternary_only_prevalence_interval(
        10, 9, 0.66, completion_value=val
    )
    assert receipt.target_one_probability_interval is None


def test_finite_prevalence_arity_transition_empty_for_small_scope():
    val = lambda c: math.exp(-0.3 * c)
    receipt = finite_ternary_only_prevalence_interval(
        3, 2, 0.05, completion_value=val
    )
    assert receipt.target_one_probability_interval is None


def test_finite_prevalence_arity_transition_at_balance_boundary():
    val = lambda c: math.exp(-0.3 * c)
    binary = finite_target_prevalence_expected_capacity(
        10, 9, 0.5, max_arity=2, completion_value=val
    )
    receipt = finite_ternary_only_prevalence_interval(
        10, 9, binary.expected_value_supremum, completion_value=val
    )
    assert receipt.target_one_probability_interval == pytest.approx((0.5, 0.5))



def test_ternary_class_capacity_premium_shrinks_with_extra_overhead():
    val = lambda c: math.exp(-0.3 * c)
    free = finite_ternary_capacity_premium_prevalence_interval(
        10, 9, 0.0, completion_value=val
    )
    costly = finite_ternary_capacity_premium_prevalence_interval(
        10, 9, 0.05, completion_value=val
    )

    assert free.ternary_minus_binary_positive_interval == pytest.approx(
        (0.12245642825298209, 0.8775435717470179)
    )
    assert costly.ternary_minus_binary_positive_interval == pytest.approx(
        (0.38286416430728654, 0.6171358356927135)
    )
    assert costly.maximal_capacity_premium_at_balance == pytest.approx(
        0.0724908517441829
    )

    for p in (0.50, 0.60):
        b2 = finite_target_prevalence_expected_capacity(
            10, 9, p, max_arity=2, completion_value=val
        )
        b3 = finite_target_prevalence_expected_capacity(
            10, 9, p, max_arity=3, completion_value=val
        )
        assert b3.expected_value_supremum - b2.expected_value_supremum > 0.05

    for p in (0.35, 0.65, 0.85):
        b2 = finite_target_prevalence_expected_capacity(
            10, 9, p, max_arity=2, completion_value=val
        )
        b3 = finite_target_prevalence_expected_capacity(
            10, 9, p, max_arity=3, completion_value=val
        )
        assert b3.expected_value_supremum - b2.expected_value_supremum < 0.05


def test_ternary_capacity_advantage_vanishes_if_its_extra_cost_too_high():
    val = lambda c: math.exp(-0.3 * c)
    receipt = finite_ternary_capacity_premium_prevalence_interval(
        10, 9, 0.08, completion_value=val
    )
    assert receipt.ternary_minus_binary_positive_interval is None


def test_ternary_class_capacity_premium_not_available_in_tiny_tasks():
    val = lambda c: math.exp(-0.3 * c)
    receipt = finite_ternary_capacity_premium_prevalence_interval(
        3, 2, 0.0, completion_value=val
    )
    assert receipt.ternary_minus_binary_positive_interval is None


def test_ternary_capacity_premium_rejects_negative_overhead():
    with pytest.raises(ValueError):
        finite_ternary_capacity_premium_prevalence_interval(
            10, 9, -0.001,
            completion_value=lambda c: math.exp(-0.3*c),
        )



def test_free_ternary_capacity_can_dominate_all_nonextreme_prevalences():
    # When m <= n-2, both arity classes can have the same fixed burden M.
    # With no extra ternary cost, the three-outcome class then strictly
    # improves on binary for every target prevalence p in (0,1).
    val = lambda c: math.exp(-0.3 * c)
    receipt = finite_ternary_capacity_premium_prevalence_interval(
        10, 6, 0.0, completion_value=val
    )
    assert receipt.ternary_minus_binary_positive_interval == pytest.approx(
        (0.0, 1.0)
    )

    for p in (0.001, 0.20, 0.5, 0.8, 0.999):
        binary = finite_target_prevalence_expected_capacity(
            10, 6, p, max_arity=2, completion_value=val
        )
        ternary = finite_target_prevalence_expected_capacity(
            10, 6, p, max_arity=3, completion_value=val
        )
        assert ternary.expected_value_supremum > binary.expected_value_supremum
