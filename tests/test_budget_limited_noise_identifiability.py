"""Exact two-query sufficiency and task-aligned pairwise-error counterexamples.

Independent Fraction oracle uses full latent-world x error-response table,
enumerates all feasible acquisition trees and all terminal target/abstain
decisions. The production solver is cross-checked only after exact enumeration.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product

import pytest
from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.joint_bitflip_reward import optimal_joint_bitflip_reward

TARGETS = (0, 1, 1, 0, 0)
CUES = {
    "A": ((0, 0, 1, 1, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0)),
    "B": ((1, 0, 0, 0, 0), (0, 0, 0, 1, 0), (1, 1, 1, 1, 0)),
}
PRIOR = (F(1, 3),) + (F(1, 6),) * 4
E = F(1, 10)
H = F(9, 200)
TRIPLE = F(1, 50)
LOSS = F(4)
COST = F(1, 10)


def finite_task(name="A"):
    return FiniteTask(
        tuple(World(f"w{i}", y) for i, y in enumerate(TARGETS)),
        tuple(Query(f"q{j}", 1, bits) for j, bits in enumerate(CUES[name])),
    )


def error_law(h01, h02, h12, triple):
    """All eight cell probabilities from first, second and third moments."""
    pair = {(0, 1): h01, (0, 2): h02, (1, 2): h12}
    out = {}
    for e in product((0, 1), repeat=3):
        ones = tuple(j for j, x in enumerate(e) if x)
        if len(ones) == 3:
            mass = triple
        elif len(ones) == 2:
            mass = pair[ones] - triple
        elif len(ones) == 1:
            j = ones[0]
            mass = E - sum(pair[tuple(sorted((j, k)))]
                           for k in range(3) if k != j) + triple
        else:
            mass = 1 - 3 * E + sum(pair.values()) - triple
        assert mass >= 0, (e, mass)
        out[e] = mass
    assert sum(out.values(), F(0)) == 1
    return out


def moment_profile(law):
    marginal = tuple(sum((p for e, p in law.items() if e[j]), F(0))
                     for j in range(3))
    paired = tuple(sum((p for e, p in law.items() if e[j] and e[k]), F(0))
                   for j, k in ((0, 1), (0, 2), (1, 2)))
    histogram = tuple(sum((p for e, p in law.items() if sum(e) == k), F(0))
                      for k in range(4))
    return marginal, paired, histogram


@lru_cache(None)
def policy_trees(unused, remaining):
    result = [None]
    if remaining:
        for j in unused:
            rest = tuple(k for k in unused if k != j)
            child = policy_trees(rest, remaining - 1)
            result.extend((j, left, right) for left, right in product(child, repeat=2))
    return tuple(result)


def observed_leaf(tree, observed):
    path = []
    while tree is not None:
        j, left, right = tree
        bit = observed[j]
        path.append((j, bit))
        tree = right if bit else left
    return tuple(path)


def exact_rows(name, law):
    cues = CUES[name]
    rows = []
    for i, target in enumerate(TARGETS):
        for flips, probability in law.items():
            if probability:
                observed = tuple(cues[j][i] ^ flips[j] for j in range(3))
                rows.append((target, observed, PRIOR[i] * probability))
    assert sum((mass for _, _, mass in rows), F(0)) == 1
    return rows


def score_partition(rows, assign, loss):
    by_observation = {}
    for target, observed, mass in rows:
        cell = by_observation.setdefault(assign(observed), [F(0), F(0)])
        cell[target] += mass
    return sum((max(F(0), a - loss*b, b - loss*a)
                for a, b in by_observation.values()), F(0))


def exact_oracle(name, law, loss, budget, adaptive):
    rows = exact_rows(name, law)
    if adaptive:
        return max(
            score_partition(rows, lambda obs, t=t: observed_leaf(t, obs), loss)
            for t in policy_trees((0, 1, 2), budget)
        )
    return max(
        score_partition(rows, lambda obs, sub=sub: tuple(obs[j] for j in sub), loss)
        for k in range(min(3, budget) + 1)
        for sub in combinations((0, 1, 2), k)
    )


def input_laws():
    # Mean pair correlation and error-count histogram match exactly;
    # pair (root,right) and (left,right) exchange their error associations.
    x = error_law(F(1, 25), F(7, 100), F(1, 40), TRIPLE)
    y = error_law(F(1, 25), F(1, 40), F(7, 100), TRIPLE)
    return x, y


def test_same_single_accuracy_average_pair_corr_and_error_count_histogram():
    x, y = input_laws()
    mx, px, hx = moment_profile(x)
    my, py, hy = moment_profile(y)
    assert x != y and px != py
    assert mx == my == (E, E, E)
    assert sum(px, F(0))/3 == sum(py, F(0))/3 == H
    assert px[0] == py[0] == F(1, 25)
    assert hx == hy == (F(163, 200), F(9, 100), F(3, 40), F(1, 50))
    cx = tuple((h - E*E)/(E*(1-E)) for h in px)
    cy = tuple((h - E*E)/(E*(1-E)) for h in py)
    assert cx == (F(1, 3), F(2, 3), F(1, 6))
    assert cy == (F(1, 3), F(1, 6), F(2, 3))
    assert sum(cx, F(0))/3 == sum(cy, F(0))/3 == F(7, 18)


def test_same_aggregate_correlations_different_controller_viability():
    x, y = input_laws()
    for law, expected_a, expected_f, expected_gain in (
        (x, F(8, 15), F(7, 20), F(11, 60)),
        (y, F(13, 30), F(7, 20), F(1, 12)),
    ):
        a = exact_oracle("A", law, LOSS, 2, True)
        f = exact_oracle("A", law, LOSS, 2, False)
        assert (a, f, a - f) == (expected_a, expected_f, expected_gain)
        assert optimal_joint_bitflip_reward(
            finite_task(), PRIOR, budget=2, error_pattern_probabilities=law,
            error_cost=LOSS
        ) == pytest.approx(float(a), abs=1e-12)
        assert optimal_joint_bitflip_reward(
            finite_task(), PRIOR, budget=2, error_pattern_probabilities=law,
            error_cost=LOSS, adaptive=False
        ) == pytest.approx(float(f), abs=1e-12)
    assert F(11, 60) - COST == F(1, 12) > 0
    assert F(1, 12) - COST == -F(1, 60) < 0


@pytest.mark.parametrize("name", ("A", "B"))
@pytest.mark.parametrize("loss", (0, 1, 4, 20))
@pytest.mark.parametrize("adaptive", (False, True))
def test_triple_only_changes_are_invisible_at_budget_two(name, loss, adaptive):
    laws = [error_law(H, H, H, a) for a in (F(0), F(1, 50), H)]
    profiles = [moment_profile(law) for law in laws]
    assert all(prof[:2] == profiles[0][:2] for prof in profiles)
    assert len({prof[2] for prof in profiles}) == 3
    values = [exact_oracle(name, law, F(loss), 2, adaptive) for law in laws]
    assert values[0] == values[1] == values[2]
    for law, value in zip(laws, values):
        result = optimal_joint_bitflip_reward(
            finite_task(name), PRIOR, budget=2,
            error_pattern_probabilities=law, error_cost=loss, adaptive=adaptive
        )
        assert result == pytest.approx(float(value), abs=1e-12)


def test_triple_dep_changes_value_when_three_queries_are_affordable():
    sparse = error_law(H, H, H, F(0))
    clustered = error_law(H, H, H, H)
    full = [exact_oracle("A", law, LOSS, 3, False)
            for law in (sparse, clustered)]
    assert full == [F(517, 600), F(49, 100)]
    for law, value in zip((sparse, clustered), full):
        for adaptive in (False, True):
            result = optimal_joint_bitflip_reward(
                finite_task(), PRIOR, budget=3,
                error_pattern_probabilities=law, error_cost=LOSS,
                adaptive=adaptive
            )
            assert result == pytest.approx(float(value), abs=1e-12)


def test_aggregate_pair_failure_is_not_caused_by_third_order_noise():
    x, y = input_laws()
    assert x[(1, 1, 1)] == y[(1, 1, 1)] == TRIPLE
    for law in (x, y):
        _, pair, counts = moment_profile(law)
        assert pair[0] == F(1, 25)
        assert counts[3] == TRIPLE
