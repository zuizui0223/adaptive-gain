"""Finite-deadline reward with an explicit option to abstain.

Correct classification pays v>0, an incorrect classification pays -L (L>=0),
and abstention pays zero. Query costs consume the hard budget only; there is
no additional acquisition debit. Both policy classes can stop and classify.
The nonadaptive class precommits a budget-feasible query subset; it is NOT
restricted to an all-or-nothing universal resolving bundle.

This is a finite Bayesian decision calculation, not a novel reject rule or
an estimate of organismal fitness. Cues and target labels remain deterministic.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations
import math
from typing import Sequence

from .core import FiniteTask


def optimal_deadline_expected_reward(
    task: FiniteTask,
    world_probabilities: Sequence[float],
    *,
    budget: int,
    correct_reward: float = 1.0,
    error_cost: float = 0.0,
    allow_abstain: bool = True,
    adaptive: bool = True,
) -> float:
    """Maximal E[v*correct - L*wrong] over the declared policy class.

    Terminal decisions use the observed cue history; a mixed branch may guess
    its most probable target or, when allowed, abstain. Adaptive policies may
    choose subsequent queries by their outcomes. Nonadaptive policies acquire
    a subset selected before any outcomes. Both are reoptimized at each budget
    and payoff setting. Computation is combinatorial, with FiniteTask's existing
    twenty-query cap. No controller-maintenance cost is subtracted here.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(adaptive) is not bool or type(allow_abstain) is not bool:
        raise ValueError("adaptive and allow_abstain must be boolean")
    reward, loss = float(correct_reward), float(error_cost)
    if not math.isfinite(reward) or reward <= 0:
        raise ValueError("correct_reward must be finite and positive")
    if not math.isfinite(loss) or loss < 0:
        raise ValueError("error_cost must be finite and nonnegative")
    if len(world_probabilities) != len(task.worlds):
        raise ValueError("one probability required per represented world")
    weights = tuple(float(p) for p in world_probabilities)
    if any(not math.isfinite(p) or p <= 0 for p in weights):
        raise ValueError("world probabilities must be finite and strictly positive")
    if not math.isclose(math.fsum(weights), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("world probabilities must sum to one")

    targets = tuple(world.target for world in task.worlds)
    all_states = tuple(range(len(targets)))
    all_queries = tuple(range(len(task.queries)))

    @lru_cache(None)
    def terminal(states: tuple[int, ...]) -> float:
        labels = {targets[i] for i in states}
        # Sum wrong mass directly: subtracting nearly equal total/correct
        # masses would create spurious penalties on almost-pure branches.
        best = max(
            reward * math.fsum(weights[i] for i in states if targets[i] == label)
            - loss * math.fsum(weights[i] for i in states if targets[i] != label)
            for label in labels
        )
        return max(0.0, best) if allow_abstain else best

    def partition(states: tuple[int, ...], subset: tuple[int, ...]):
        groups: dict[tuple[object, ...], list[int]] = {}
        for i in states:
            signature = tuple(task.queries[j].outcomes[i] for j in subset)
            groups.setdefault(signature, []).append(i)
        return tuple(tuple(group) for group in groups.values())

    if not adaptive:
        best = terminal(all_states)
        for size in range(1, len(all_queries) + 1):
            for subset in combinations(all_queries, size):
                if sum(task.queries[j].cost for j in subset) > budget:
                    continue
                value = math.fsum(terminal(group) for group in partition(all_states, subset))
                best = max(best, value)
        return best

    @lru_cache(None)
    def search(states: tuple[int, ...], unused: tuple[int, ...], remaining: int):
        best = terminal(states)
        for j in unused:
            query = task.queries[j]
            if query.cost > remaining:
                continue
            groups = partition(states, (j,))
            if len(groups) == 1:
                continue
            value = math.fsum(
                search(group, tuple(k for k in unused if k != j), remaining - query.cost)
                for group in groups
            )
            best = max(best, value)
        return best

    return search(all_states, all_queries, budget)
