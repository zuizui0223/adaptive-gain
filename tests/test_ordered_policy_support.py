"""Exact on-policy nonidentification and randomized rescue for ordered cue acquisition.

All probabilities are Fraction. The full-path evaluator enumerates target-world
trajectories, all legal cue acquisition trees and terminal target actions,
independently of the production ordered-readout dynamic program.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations, product

import pytest

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.ordered_readout import optimal_ordered_readout_reward

PRIOR = (F(1, 2), F(1, 2))
BASE_ACCURACY = F(3, 4)
COST = F(1, 20)
SECOND_CUES = (1, 2)


def task():
    return FiniteTask(
        (World("target0", 0), World("target1", 1)),
        (Query("context_A", 1, (0, 0)),
         Query("diagnostic_B", 1, (0, 1)),
         Query("diagnostic_C", 1, (0, 1))),
    )


def readout_one(world, history, j, s):
    """Unseen C-after-A response changes with s; all observed A->B paths do not."""
    if j == 0:
        return F(1, 2)
    correct = BASE_ACCURACY
    if j == 2 and len(history) == 1 and history[0][0] == 0:
        correct = s if history[0][1] == 0 else F(3, 2) - s
    return correct if world == 1 else 1 - correct


def kernel(s):
    return lambda w, h, j: readout_one(w, h, j, s)


@lru_cache(None)
def trees(unused, budget):
    result = [None]
    if budget:
        for j in unused:
            after = tuple(x for x in unused if x != j)
            for left, right in product(trees(after, budget - 1), repeat=2):
                result.append((j, left, right))
    return tuple(result)


def fixed_tree(schedule):
    if not schedule:
        return None
    next_node = fixed_tree(schedule[1:])
    return (schedule[0], next_node, next_node)


def exact_policy_score(node, s):
    leaves = {}

    def forward(world, branch, history, mass):
        if branch is None:
            leaves.setdefault(history, [F(0), F(0)])[world] += mass
            return
        j, left, right = branch
        p1 = readout_one(world, history, j, s)
        forward(world, left, history + ((j, 0),), mass * (1-p1))
        forward(world, right, history + ((j, 1),), mass * p1)

    for world in (0, 1):
        forward(world, node, (), PRIOR[world])
    return sum((max(v) for v in leaves.values()), F(0))


def exact_optimum(s, adaptive):
    if adaptive:
        options = trees((0, 1, 2), 2)
    else:
        options = (fixed_tree(schedule) for length in range(3)
                   for schedule in permutations((0, 1, 2), length))
    return max(exact_policy_score(policy, s) for policy in options)


def deployed_distribution(s):
    """Fully labeled population log when the historical policy always buys A->B."""
    rows = {}
    for world in (0, 1):
        for a in (0, 1):
            for b in (0, 1):
                mass = PRIOR[world] * (F(1, 2)) * (
                    readout_one(world, ((0, a),), 1, s) if b
                    else 1-readout_one(world, ((0, a),), 1, s)
                )
                rows[(world, a, b)] = mass
    return rows


def randomized_distribution(s, gamma0, gamma1):
    """Exploratory second-cue assignment: P(J=C | A=a)=gamma_a."""
    assert 0 < gamma0 < 1 and 0 < gamma1 < 1
    rows = {}
    for world in (0, 1):
        for a, gamma in ((0, gamma0), (1, gamma1)):
            for j in SECOND_CUES:
                propensity = gamma if j == 2 else 1-gamma
                for z in (0, 1):
                    p1 = readout_one(world, ((0, a),), j, s)
                    rows[(world, a, j, z)] = PRIOR[world] * F(1, 2) * propensity * (
                        p1 if z else 1-p1
                    )
    assert sum(rows.values(), F(0)) == 1
    return rows


def target_policy(a, s):
    """Best next cue if the two history-stratified cue accuracies are known."""
    return 2 if (s >= BASE_ACCURACY) == (a == 0) else 1


def ipw_value(rows, gamma0, gamma1, s):
    result = F(0)
    for (world, a, j, z), p in rows.items():
        if j == target_policy(a, s):
            gamma = gamma0 if a == 0 else gamma1
            action_probability = gamma if j == 2 else 1-gamma
            result += p * F(z == world) / action_probability
    return result


@pytest.mark.parametrize("s", (F(1, 2), F(3, 5), F(3, 4), F(9, 10), F(1)))
def test_complete_deployed_A_then_B_law_cannot_identify_unseen_C_response(s):
    ref = deployed_distribution(F(3, 4))
    assert deployed_distribution(s) == ref
    assert sum(ref.values(), F(0)) == 1
    for (world, a, b), mass in ref.items():
        assert mass == (F(3, 16) if b == world else F(1, 16))
    for world in (0, 1):
        assert readout_one(world, (), 2, s) == readout_one(world, (), 2, F(3, 4))
    # A history-pooled C-after-A calibration is also identical at 75%.
    assert (s + F(3, 2) - s) / 2 == BASE_ACCURACY


@pytest.mark.parametrize("s", (F(1, 2), F(3, 5), F(3, 4), F(9, 10), F(1)))
def test_exact_sharp_partially_identified_adaptive_premium(s):
    ad = exact_optimum(s, True)
    fixed = exact_optimum(s, False)
    assert fixed == BASE_ACCURACY
    assert ad == BASE_ACCURACY + abs(s-BASE_ACCURACY)/2
    for adaptive, expected in ((True, ad), (False, fixed)):
        actual = optimal_ordered_readout_reward(
            task(), PRIOR, budget=2, response_probability_one=kernel(s), adaptive=adaptive,
        )
        assert actual == pytest.approx(float(expected), abs=1e-12)
    assert ad-fixed-COST == abs(s-BASE_ACCURACY)/2-COST


def test_sharp_identified_set_crosses_controller_maintenance_zero():
    lo = exact_optimum(F(3, 4), True) - exact_optimum(F(3, 4), False) - COST
    hi = exact_optimum(F(1), True) - exact_optimum(F(1), False) - COST
    assert (lo, hi) == (-F(1, 20), F(3, 40))
    assert exact_optimum(F(9, 10), True) == F(33, 40)
    assert exact_optimum(F(9, 10), True)-BASE_ACCURACY-COST == F(1, 40)
    # These bounds are sharp for the explicitly restricted s-family, not an
    # identification claim over all biologically possible sequential kernels.


@pytest.mark.parametrize("s", (F(3, 5), F(3, 4), F(9, 10)))
@pytest.mark.parametrize("gamma0,gamma1", ((F(1, 2), F(1, 2)), (F(1, 4), F(3, 4))))
def test_randomized_second_cue_with_recorded_propensity_identifies_policy_value(s,gamma0,gamma1):
    rows = randomized_distribution(s, gamma0, gamma1)
    assert ipw_value(rows, gamma0, gamma1, s) == exact_optimum(s, True)
    # Disaggregated data identify P(correct | A=a, J=C), including A-branch.
    for a, gamma in ((0,gamma0), (1,gamma1)):
        for j in SECOND_CUES:
            subs = [(world,z,p) for (world,aa,jj,z),p in rows.items() if aa==a and jj==j]
            observed_correct = sum((p for world,z,p in subs if z==world), F(0))
            total = sum((p for _,_,p in subs),F(0))
            expected = ((s if a==0 else F(3,2)-s) if j==2 else BASE_ACCURACY)
            assert observed_correct / total == expected


@pytest.mark.parametrize("s", (F(3, 5), F(3, 4), F(9, 10)))
def test_pooled_randomized_success_can_still_hide_adaptive_premium(s):
    rows = randomized_distribution(s, F(1, 2), F(1, 2))
    assert sum((p for (w,a,j,z),p in rows.items() if z==w),F(0))==BASE_ACCURACY
    for j in SECOND_CUES:
        arm = [(w,z,p) for (w,a,jj,z),p in rows.items() if jj==j]
        assert sum((p for w,z,p in arm if z==w),F(0))/sum((p for _,_,p in arm),F(0)) == BASE_ACCURACY
    # A randomized design can still be wasted if condition-on-context labels
    # are thrown away during aggregation.


def test_deterministic_second_cue_support_failure_is_structural_not_sampling_noise():
    # Under the deployed A->B policy, P(J=C | A=a) = 0, so standard
    # inverse-propensity off-policy evaluation is undefined on that branch.
    s=F(9,10)
    assert target_policy(0,s)==2
    assert target_policy(1,s)==1
    # The deployed schedule A -> B never requests C, while the evaluation
    # policy needs C in context A=0; no reweighting can fill that support gap.
    deployed_actions = {1}
    assert target_policy(0, s) not in deployed_actions
    assert target_policy(1, s) in deployed_actions
