"""Sharp scalable expected-value limits under fixed binary-target prevalence."""
import math

import pytest

from adaptive_gain.bounded_arity_extremal_bounds import (
    ternary_target_balance_expected_witness,
    two_shallow_leaf_expected_value_witness,
)
from adaptive_gain.core import fixed_minimum_resolution
from adaptive_gain.target_prevalence_capacity import (
    exponential_target_prevalence_expected_capacity,
    exponential_minimum_expected_arity_with_target_prevalence,
    minimum_expected_cue_arity_with_target_prevalence,
    target_prevalence_expected_capacity,
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
