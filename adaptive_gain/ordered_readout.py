"""Finite target-choice reward for order-/history-dependent binary cue readouts.

For each latent ecological world w and ordered observed history h, the supplied
kernel gives P(next response=1 | w, h, next cue). The kernel is not inferred
from static simultaneous cue marginals. It must be specified independently.
The true world/target stays fixed during each encounter; queries are used once,
consume a hard acquisition budget, and carry no further utility debit. Correct
choices pay v>0, errors -L>=-infinity, and abstention zero.

Nonadaptive access precommits an ORDERED list of affordable cues. It may make
any posterior-based target decision (or abstain) after reading that list. The
order is part of the comparator because the channel can respond to previous
acquisition. No biological fitness, learning dynamics or causal effect is fit.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import permutations, product
import math
from typing import Callable, Sequence

from .core import FiniteTask

ReadoutKernel = Callable[[int, tuple[tuple[int, int], ...], int], float]


def optimal_ordered_readout_reward(
    task: FiniteTask,
    world_probabilities: Sequence[float],
    *,
    budget: int,
    response_probability_one: ReadoutKernel,
    correct_reward: float = 1.0,
    error_cost: float = 0.0,
    adaptive: bool = True,
) -> float:
    """Optimize reward with adaptive query choice or a precommitted cue order.

    The response model may depend on the previously observed cue identities,
    outcomes, and order. The same model is supplied to both policy classes.
    The policy sees only perceived outcomes, never latent worlds. The kernel
    must be pure/stationary within an encounter and is queried as necessary.
    Intended as a small exact-state calculation, not a model of real insects.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError('budget must be a nonnegative integer')
    if type(adaptive) is not bool:
        raise ValueError('adaptive must be boolean')
    if not callable(response_probability_one):
        raise ValueError('response_probability_one must be callable')
    if len(task.queries) > 8:
        raise ValueError('ordered-readout solver permits at most eight cues')
    if len(world_probabilities) != len(task.worlds):
        raise ValueError('one prior probability per represented world required')
    weights = tuple(float(x) for x in world_probabilities)
    if any(not math.isfinite(x) or x <= 0 for x in weights) or not math.isclose(
        math.fsum(weights), 1., rel_tol=0., abs_tol=1e-9
    ):
        raise ValueError('world probabilities must be finite positive and sum to one')
    v, loss = float(correct_reward), float(error_cost)
    if not math.isfinite(v) or v <= 0:
        raise ValueError('correct_reward must be finite and positive')
    if not math.isfinite(loss) or loss < 0:
        raise ValueError('error_cost must be finite and nonnegative')

    targets = tuple(w.target for w in task.worlds)
    classes = frozenset(targets)
    all_queries = tuple(range(len(task.queries)))

    @lru_cache(maxsize=None)
    def posterior_unnormalized(history: tuple[tuple[int, int], ...]) -> tuple[float, ...]:
        mass = list(weights)
        for step, (j, z) in enumerate(history):
            prefix = history[:step]
            for world in range(len(weights)):
                p1 = float(response_probability_one(world, prefix, j))
                if not math.isfinite(p1) or not 0 <= p1 <= 1:
                    raise ValueError('response probability must be in [0,1] and finite')
                likelihood = p1 if z else (1 - p1)
                revised = mass[world] * likelihood
                if mass[world] > 0 and likelihood > 0 and revised == 0:
                    raise ArithmeticError('likelihood underflow; use exact arithmetic')
                mass[world] = revised
        return tuple(mass)

    @lru_cache(maxsize=None)
    def terminal(history: tuple[tuple[int, int], ...]) -> float:
        m = posterior_unnormalized(history)
        total = math.fsum(m)
        if not total:
            return 0.0
        return max(0.0, max(
            v * math.fsum(x for x, t in zip(m, targets) if t == target)
            - loss * math.fsum(x for x, t in zip(m, targets) if t != target)
            for target in classes
        ))

    if not adaptive:
        best = terminal(())
        for k in range(1, len(all_queries) + 1):
            for schedule in permutations(all_queries, k):
                if sum(task.queries[j].cost for j in schedule) > budget:
                    continue
                gain = math.fsum(
                    terminal(tuple(zip(schedule, outcomes)))
                    for outcomes in product((0, 1), repeat=k)
                )
                best = max(best, gain)
        return best

    @lru_cache(maxsize=None)
    def search(history: tuple[tuple[int, int], ...], unused: tuple[int, ...], remaining: int) -> float:
        best = terminal(history)
        for j in unused:
            cost = task.queries[j].cost
            if cost > remaining:
                continue
            rest = tuple(k for k in unused if k != j)
            value = math.fsum(
                search(history + ((j, z),), rest, remaining - cost)
                for z in (0, 1)
            )
            best = max(best, value)
        return best

    return search((), all_queries, budget)
