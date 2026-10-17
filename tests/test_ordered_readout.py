"""Independent exact checks for cue-order-dependent observational kernels.

The oracle explicitly enumerates all acquisition trees and integrates over
latent states and ordered observation histories using Fraction arithmetic.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations, product
import math

import pytest

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.ordered_readout import optimal_ordered_readout_reward


def task():
    return FiniteTask(
        (World('negative', 0), World('positive', 1)),
        (
            Query('context', 1, (0, 0)),
            Query('cue_B', 1, (0, 1)),
            Query('cue_C', 1, (0, 1)),
        ),
    )


PRIOR = (F(1, 2), F(1, 2))


def readout_one(world, history, cue, *, reactive, primed_accuracy=F(1)):
    """Literal rational experimental channel, independent from production DP."""
    if cue == 0:
        return F(1, 2)
    if reactive and len(history) == 1 and history[0][0] == 0:
        context_bit = history[0][1]
        primed_cue = 1 if context_bit == 0 else 2
        accuracy = primed_accuracy if cue == primed_cue else F(3, 2) - primed_accuracy
        return accuracy if world == 1 else 1 - accuracy
    return F(3, 4) if world == 1 else F(1, 4)


def kernel(reactive, primed_accuracy=F(1)):
    return lambda world, history, cue: readout_one(
        world, history, cue, reactive=reactive, primed_accuracy=primed_accuracy
    )


@lru_cache(None)
def trees(unused, budget):
    result = [None]
    if budget:
        for j in unused:
            rest = tuple(k for k in unused if k != j)
            children = trees(rest, budget - 1)
            result.extend((j, left, right) for left, right in product(children, repeat=2))
    return tuple(result)


def fixed_tree(sequence):
    if not sequence:
        return None
    child = fixed_tree(sequence[1:])
    return (sequence[0], child, child)


def independent_exact_score(policy, *, reactive, error_cost, primed_accuracy=F(1)):
    """Forward-enumerate paths of a fixed policy, then optimize leaf actions."""
    cells = {}

    def run(world, node, history, mass):
        if node is None:
            group = cells.setdefault(history, [F(0), F(0)])
            group[world] += mass
            return
        j, left, right = node
        p1 = readout_one(world, history, j, reactive=reactive, primed_accuracy=primed_accuracy)
        run(world, left, history + ((j, 0),), mass * (1 - p1))
        run(world, right, history + ((j, 1),), mass * p1)

    for world in range(2):
        run(world, policy, (), PRIOR[world])

    return sum((max(F(0), x - error_cost * y, y - error_cost * x)
                for x, y in cells.values()), F(0))


def exhaustive_value(*, reactive, budget, adaptive, error_cost, primed_accuracy=F(1)):
    if adaptive:
        options = trees((0, 1, 2), budget)
    else:
        options = (fixed_tree(seq) for k in range(budget + 1)
                   for seq in permutations((0, 1, 2), k))
    return max(independent_exact_score(t, reactive=reactive, error_cost=error_cost,
                                       primed_accuracy=primed_accuracy)
               for t in options)


@pytest.mark.parametrize('reactive', (False, True))
@pytest.mark.parametrize('L', (F(0), F(1), F(2), F(3), F(4)))
@pytest.mark.parametrize('budget', (0, 1, 2))
@pytest.mark.parametrize('adaptive', (False, True))
def test_production_matches_independent_fraction_policy_tree_oracle(reactive, L, budget, adaptive):
    want = exhaustive_value(reactive=reactive, budget=budget,
                            adaptive=adaptive, error_cost=L)
    got = optimal_ordered_readout_reward(task(), PRIOR, budget=budget,
                                         response_probability_one=kernel(reactive),
                                         error_cost=L, adaptive=adaptive)
    assert got == pytest.approx(float(want), abs=2e-12)


@pytest.mark.parametrize('L,stable,reactive_fixed', [
    (0, F(3, 4), F(3, 4)),
    (1, F(1, 2), F(1, 2)),
    (2, F(7, 16), F(1, 2)),
    (3, F(3, 8), F(1, 2)),
    (4, F(5, 16), F(1, 2)),
])
def test_static_vs_order_reactive_repayment_is_not_identified_by_passive_calibration(L, stable, reactive_fixed):
    static_a = exhaustive_value(reactive=False, budget=2, adaptive=True, error_cost=F(L))
    static_f = exhaustive_value(reactive=False, budget=2, adaptive=False, error_cost=F(L))
    reactive_a = exhaustive_value(reactive=True, budget=2, adaptive=True, error_cost=F(L))
    reactive_f = exhaustive_value(reactive=True, budget=2, adaptive=False, error_cost=F(L))
    assert static_a == static_f == stable
    assert reactive_a == 1
    assert reactive_f == reactive_fixed
    if L == 0:
        assert reactive_a - reactive_f == F(1, 4)
    if L == 3:
        assert reactive_a - reactive_f == F(1, 2)


def test_all_first_cue_and_passive_joint_calibrations_identical():
    # Cue 0 is target-independent; cues 1 and 2 individually have 75% accuracy.
    for w in (0, 1):
        for j in (0, 1, 2):
            assert readout_one(w, (), j, reactive=False) == readout_one(w, (), j, reactive=True)
        # Passive simultaneous calibration is a *different* intervention:
        # neither cue is read after actively acquiring the other. We define
        # its readout law as two independent first-position cue reports.
        for a in range(3):
            for b in range(a + 1, 3):
                def passive_pair_law(reactive):
                    pa = readout_one(w, (), a, reactive=reactive)
                    pb = readout_one(w, (), b, reactive=reactive)
                    return {
                        (z, t): (pa if z else 1 - pa) * (pb if t else 1 - pb)
                        for z, t in product((0, 1), repeat=2)
                    }
                stable = passive_pair_law(False)
                reactive = passive_pair_law(True)
                assert stable == reactive
                assert sum(stable.values(), F(0)) == 1


def test_serial_position_marginal_accuracy_same_but_history_conditional_kernel_differs():
    # For every fixed two-cue order, the second cue's marginal accuracy is
    # identical; only conditioning on the preceding perceived context reveals
    # whether the second cue was primed or degraded.
    for a, b in permutations((0, 1, 2), 2):
        for w in (0, 1):
            def second_accuracy(reactive):
                return sum(
                    (p1 if z else 1 - p1)
                    * (readout_one(w, ((a, z),), b, reactive=reactive) if w
                       else 1 - readout_one(w, ((a, z),), b, reactive=reactive))
                    for z in (0, 1)
                    for p1 in (readout_one(w, (), a, reactive=reactive),)
                )
            assert second_accuracy(False) == second_accuracy(True)
    assert readout_one(1, ((0, 0),), 1, reactive=False) == F(3, 4)
    assert readout_one(1, ((0, 0),), 1, reactive=True) == 1
    assert readout_one(1, ((0, 1),), 1, reactive=False) == F(3, 4)
    assert readout_one(1, ((0, 1),), 1, reactive=True) == F(1, 2)


def test_no_advantage_before_second_query_and_context_not_target_informative():
    for w in (0, 1):
        assert readout_one(w, (), 0, reactive=True) == F(1, 2)
    for L in (0, 3):
        a = exhaustive_value(reactive=True, budget=1, adaptive=True, error_cost=F(L))
        f = exhaustive_value(reactive=True, budget=1, adaptive=False, error_cost=F(L))
        assert a == f


@pytest.mark.parametrize('kwargs', (
    {'budget': -1}, {'budget': True}, {'budget': 1.0},
    {'correct_reward': 0}, {'error_cost': -1}, {'error_cost': math.nan},
    {'adaptive': 1},
))
def test_invalid_inputs_rejected(kwargs):
    args = {'budget': 2, 'response_probability_one': kernel(False)}
    args.update(kwargs)
    with pytest.raises(ValueError):
        optimal_ordered_readout_reward(task(), PRIOR, **args)


def test_invalid_kernel_probabilities_rejected():
    with pytest.raises(ValueError, match='probability'):
        optimal_ordered_readout_reward(task(), PRIOR, budget=2,
                                         response_probability_one=lambda w,h,j: 2.0)


@pytest.mark.parametrize('L,expected_adaptive,expected_fixed', [
    (0, F(9, 10), F(3, 4)),
    (1, F(4, 5), F(1, 2)),
    (2, F(7, 10), F(7, 16)),
    (3, F(3, 5), F(3, 8)),
    (4, F(1, 2), F(5, 16)),
    (8, F(1, 10), F(1, 16)),
    (9, F(0), F(0)),
])
def test_full_support_history_effect_changes_reward_without_perfect_readouts(L, expected_adaptive, expected_fixed):
    # On acquiring context 0, the right next cue becomes 90% accurate while
    # the other one is 60% accurate; both errors remain strictly positive.
    high = F(9, 10)
    for adaptive, want in ((True, expected_adaptive), (False, expected_fixed)):
        exact = exhaustive_value(reactive=True, budget=2, adaptive=adaptive,
                                 error_cost=F(L), primed_accuracy=high)
        assert exact == want
        got = optimal_ordered_readout_reward(
            task(), PRIOR, budget=2, response_probability_one=kernel(True, high),
            error_cost=L, adaptive=adaptive,
        )
        assert got == pytest.approx(float(want), abs=2e-12)
    # Independent static 75% cue accuracy is unchanged in this comparison.
    assert readout_one(1, (), 1, reactive=False) == F(3, 4)
    assert readout_one(1, (), 1, reactive=True, primed_accuracy=high) == F(3, 4)
