"""Reward/abstention audit; independent exact outcome-enumeration oracle.

Mutations caught: forbidding abstention, giving the nonadaptive comparator a
universal-bundle restriction, ignoring costs, or treating reward as accuracy.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import math

import pytest
from adaptive_gain.core import FiniteTask, Query, World, adaptive_gain_receipt

TARGETS = (0, 1, 1, 0, 0)
VECTORS = {
    "A": ((0, 0, 1, 1, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0)),
    "B": ((1, 0, 0, 0, 0), (0, 0, 0, 1, 0), (1, 1, 1, 1, 0)),
}
PRIORS = (F(1, 5), F(1, 4), F(1, 3), F(1, 2), F(4, 5), F(19, 20))
LOSSES = (F(0), F(1, 2), F(1), F(2), F(299, 100), F(3), F(301, 100), F(4), F(10), F(100))


def task_for(label):
    return FiniteTask(
        tuple(World(f"w{i}", target) for i, target in enumerate(TARGETS)),
        tuple(Query(f"q{j}", 1, vector) for j, vector in enumerate(VECTORS[label])),
    )


def prior_for(t):
    return (t,) + ((1 - t) / 4,) * 4


def solve(task, prior, **kwargs):
    from adaptive_gain.deadline_reward import optimal_deadline_expected_reward
    return optimal_deadline_expected_reward(task, prior, **kwargs)


def exhaustive_outcome_vectors(task, prior, budget, adaptive, allow_abstain):
    """Enumerate attainable (correct, wrong, abstain) masses, not reward DP.

    All operations use Fraction. Terminal choices include both target actions
    even when one is knowingly wrong. No production reward helper is called.
    """
    labels = {w.target for w in task.worlds}

    def terminal(states):
        mass = sum((prior[i] for i in states), F(0))
        vectors = {(F(0), F(0), mass)} if allow_abstain else set()
        for label in labels:
            correct = sum((prior[i] for i in states if task.worlds[i].target == label), F(0))
            vectors.add((correct, mass - correct, F(0)))
        return vectors

    def parts(states, subset):
        groups = {}
        for i in states:
            sig = tuple(task.queries[j].outcomes[i] for j in subset)
            groups.setdefault(sig, []).append(i)
        return tuple(tuple(group) for group in groups.values())

    def combine(options):
        return {
            tuple(sum((row[j] for row in choices), F(0)) for j in range(3))
            for choices in product(*options)
        }

    @lru_cache(None)
    def all_trees(states, unused, remaining):
        vectors = terminal(states)
        for j in unused:
            query = task.queries[j]
            if query.cost > remaining:
                continue
            vectors |= combine(tuple(
                all_trees(group, tuple(k for k in unused if k != j), remaining - query.cost)
                for group in parts(states, (j,))
            ))
        return vectors

    states = tuple(range(len(task.worlds)))
    unused = tuple(range(len(task.queries)))
    if adaptive:
        return all_trees(states, unused, budget)
    vectors = set()
    for size in range(len(unused) + 1):
        for subset in combinations(unused, size):
            if sum(task.queries[j].cost for j in subset) <= budget:
                vectors |= combine(tuple(terminal(group) for group in parts(states, subset)))
    return vectors


@pytest.mark.parametrize("label,expected", [("A", F(1, 6)), ("B", F(1, 3))])
def test_high_error_loss_favors_safe_one_cue_structure(label, expected):
    assert solve(task_for(label), prior_for(F(1, 3)), budget=1, error_cost=4) == pytest.approx(float(expected))


@pytest.mark.parametrize("t", PRIORS)
@pytest.mark.parametrize("label", ("A", "B"))
@pytest.mark.parametrize("adaptive", (False, True))
@pytest.mark.parametrize("allow_abstain", (False, True))
def test_float_solver_matches_fraction_outcome_enumeration(t, label, adaptive, allow_abstain):
    task, prior = task_for(label), prior_for(t)
    for budget in range(4):
        vectors = exhaustive_outcome_vectors(task, prior, budget, adaptive, allow_abstain)
        assert all(sum(row, F(0)) == 1 for row in vectors)
        for loss in LOSSES:
            exact = max(correct - loss * wrong for correct, wrong, _ in vectors)
            actual = solve(task, prior, budget=budget, error_cost=float(loss),
                           adaptive=adaptive, allow_abstain=allow_abstain)
            assert actual == pytest.approx(float(exact), abs=2e-12)


@pytest.mark.parametrize("t", PRIORS)
def test_analytic_one_cue_values_and_exact_loss_ratio_boundary(t):
    q = (1 - t) / 4
    for loss in LOSSES:
        a = q + max(t + (2 - loss) * q, F(0))
        b = t + 2 * q * max(1 - loss, F(0))
        for adaptive in (False, True):
            assert solve(task_for("A"), prior_for(t), budget=1, error_cost=loss, adaptive=adaptive) == pytest.approx(float(a))
            assert solve(task_for("B"), prior_for(t), budget=1, error_cost=loss, adaptive=adaptive) == pytest.approx(float(b))
        if t > F(1, 5):
            assert (a > b) == (loss < 3)
            assert (a == b) == (loss == 3)
            assert (a < b) == (loss > 3)


@pytest.mark.parametrize("t", PRIORS)
def test_two_cue_adaptivity_premium_increases_then_saturates(t):
    q = (1 - t) / 4
    for loss in LOSSES:
        a_ad = solve(task_for("A"), prior_for(t), budget=2, error_cost=loss)
        a_na = solve(task_for("A"), prior_for(t), budget=2, error_cost=loss, adaptive=False)
        b_ad = solve(task_for("B"), prior_for(t), budget=2, error_cost=loss)
        b_na = solve(task_for("B"), prior_for(t), budget=2, error_cost=loss, adaptive=False)
        assert a_ad == pytest.approx(1)
        assert a_ad - a_na == pytest.approx(float(q * min(1 + loss, 2)))
        assert b_ad == pytest.approx(float(t + q + q * max(2 - loss, F(0))))
        assert b_ad == pytest.approx(b_na)
        for budget in (1, 3):
            for label in ("A", "B"):
                assert solve(task_for(label), prior_for(t), budget=budget, error_cost=loss) == pytest.approx(
                    solve(task_for(label), prior_for(t), budget=budget, error_cost=loss, adaptive=False))


@pytest.mark.parametrize("t", PRIORS)
def test_forced_choice_is_affine_accuracy_and_cannot_explain_reversal(t):
    q = (1 - t) / 4
    for loss in LOSSES:
        values = []
        for label, accuracy in (("A", t + 3 * q), ("B", t + 2 * q)):
            value = solve(task_for(label), prior_for(t), budget=1, error_cost=loss, allow_abstain=False)
            assert value == pytest.approx(float((1 + loss) * accuracy - loss))
            values.append(value)
        assert values[0] - values[1] == pytest.approx(float((1 + loss) * q))


def test_reward_units_scale_boundary_and_advantage():
    t = F(1, 3)
    for loss in (0, 3, 4):
        for label in ("A", "B"):
            unscaled = solve(task_for(label), prior_for(t), budget=1, error_cost=loss)
            scaled = solve(task_for(label), prior_for(t), budget=1, correct_reward=2.5, error_cost=2.5 * loss)
            assert scaled == pytest.approx(2.5 * unscaled)


def test_original_task_complexities_are_unchanged():
    assert [(adaptive_gain_receipt(task_for(x)).adaptive_cost,
             adaptive_gain_receipt(task_for(x)).fixed_cost) for x in ("A", "B")] == [(2, 3), (3, 3)]


def test_multiclass_and_unequal_query_costs_against_fraction_oracle():
    task = FiniteTask(
        tuple(World(str(i), target) for i, target in enumerate(("a", "b", "c", "a"))),
        (Query("ternary", 2, (0, 1, 2, 0)), Query("partial", 1, (0, 0, 1, 1)),
         Query("constant", 1, (0, 0, 0, 0))),
    )
    prior = (F(1, 2), F(1, 4), F(1, 8), F(1, 8))
    for budget, adaptive, abstain, loss in product(range(4), (False, True), (False, True), (F(0), F(1), F(5))):
        vectors = exhaustive_outcome_vectors(task, prior, budget, adaptive, abstain)
        value = max(c - loss * e for c, e, _ in vectors)
        assert solve(task, prior, budget=budget, adaptive=adaptive, allow_abstain=abstain, error_cost=loss) == pytest.approx(float(value))


def test_zero_budget_no_queries_and_already_pure():
    task = FiniteTask((World("x", 0), World("y", 1)), ())
    assert solve(task, (0.5, 0.5), budget=0, error_cost=4) == 0
    assert solve(task, (0.5, 0.5), budget=0, error_cost=4, allow_abstain=False) == -1.5
    pure = FiniteTask((World("x", 0),), ())
    assert solve(pure, (1,), budget=0, correct_reward=2, error_cost=1e6) == 2


@pytest.mark.parametrize("kwargs", [
    {"budget": -1}, {"budget": True}, {"budget": 1.0},
    {"correct_reward": 0}, {"correct_reward": -1}, {"correct_reward": math.inf},
    {"error_cost": -1}, {"error_cost": math.nan}, {"error_cost": math.inf},
    {"adaptive": 1}, {"allow_abstain": 1},
])
def test_invalid_parameters_rejected(kwargs):
    options = {"budget": 1}
    options.update(kwargs)
    with pytest.raises(ValueError):
        solve(task_for("A"), prior_for(F(1, 3)), **options)


@pytest.mark.parametrize("prior", [(0.25,) * 4, (0.1,) * 5, (0, 0.25, 0.25, 0.25, 0.25),
                                  (math.nan, 0.2, 0.2, 0.2, 0.2), (-0.2, 0.3, 0.3, 0.3, 0.3)])
def test_invalid_probabilities_rejected(prior):
    with pytest.raises(ValueError):
        solve(task_for("A"), prior, budget=1)
