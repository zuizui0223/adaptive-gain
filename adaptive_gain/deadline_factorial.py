"""Deadline-conditioned exact value of contingent target resolution.

Scope: finite deterministic queries with integral acquisition costs, exact target
identification and a declared strictly-positive state distribution. A branch
counts as timely success only when every remaining state has the same target.
Lucky guesses, query error, reward variation, and interaction detection are not
part of the reported mass. Policies may re-optimize for each declared budget.
"""

from __future__ import annotations

from functools import lru_cache
import math
from typing import Sequence

from .core import FiniteTask


def optimal_timely_resolution_mass(
    task: FiniteTask,
    world_probabilities: Sequence[float],
    *,
    budget: int,
) -> float:
    """Return maximal probability of CERTAIN correct resolution by budget.

    Query choice and early stopping may depend on previous query outcomes.
    Unresolved branches at deadline contribute zero, even when a guess would
    happen to be correct. The result is an attainable decision-policy envelope,
    not the performance expected of an untrained or resource-limited organism.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if len(world_probabilities) != len(task.worlds):
        raise ValueError("one probability required per represented world")
    weights = tuple(float(p) for p in world_probabilities)
    if any(not math.isfinite(p) or p <= 0 for p in weights):
        raise ValueError("world probabilities must be finite and strictly positive")
    if not math.isclose(sum(weights), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("world probabilities must sum to one")

    world_count = len(task.worlds)
    full_world_mask = (1 << world_count) - 1
    full_query_mask = (1 << len(task.queries)) - 1
    targets = tuple(world.target for world in task.worlds)

    @lru_cache(maxsize=None)
    def recurse(world_mask: int, query_mask: int, remaining: int) -> float:
        current = tuple(i for i in range(world_count) if world_mask & (1 << i))
        if len({targets[i] for i in current}) == 1:
            return sum(weights[i] for i in current)

        best = 0.0
        for q_index, query in enumerate(task.queries):
            bit = 1 << q_index
            if not (query_mask & bit) or query.cost > remaining:
                continue
            partition: dict[object, int] = {}
            for i in current:
                outcome = query.outcomes[i]
                partition[outcome] = partition.get(outcome, 0) | (1 << i)
            if len(partition) <= 1:
                continue

            score = sum(
                recurse(sub_mask, query_mask ^ bit, remaining - query.cost)
                for sub_mask in partition.values()
            )
            if score > best:
                best = score
        return best

    return recurse(full_world_mask, full_query_mask, budget)


def optimal_deadline_correct_choice_mass(
    task: FiniteTask,
    world_probabilities: Sequence[float],
    *,
    budget: int,
) -> float:
    """Bayes-optimal correct *choice* with deadline-limited deterministic cues.

    Unlike certain-resolution mass, unresolved branches may end with a
    best-guess target. Therefore nonzero success is possible at budget zero.
    This is a best-achievable ideal decision policy, not an observed rate.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if len(world_probabilities) != len(task.worlds):
        raise ValueError("one probability required per represented world")
    weights = tuple(float(p) for p in world_probabilities)
    if any(not math.isfinite(p) or p <= 0 for p in weights):
        raise ValueError("world probabilities must be finite and strictly positive")
    if not math.isclose(sum(weights), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("world probabilities must sum to one")

    n_worlds = len(task.worlds)
    targets = tuple(w.target for w in task.worlds)

    @lru_cache(maxsize=None)
    def recurse(world_mask: int, query_mask: int, remaining: int) -> float:
        current = tuple(i for i in range(n_worlds) if world_mask & (1 << i))
        target_labels = {targets[i] for i in current}
        # A terminal guess receives weight only from worlds matching it.
        best = max(
            sum(weights[i] for i in current if targets[i] == target)
            for target in target_labels
        )
        for j, q in enumerate(task.queries):
            bit = 1 << j
            if not (query_mask & bit) or q.cost > remaining:
                continue
            parts: dict[object, int] = {}
            for i in current:
                outcome = q.outcomes[i]
                parts[outcome] = parts.get(outcome, 0) | (1 << i)
            if len(parts) <= 1:
                continue
            candidate = sum(
                recurse(submask, query_mask ^ bit, remaining - q.cost)
                for submask in parts.values()
            )
            best = max(best, candidate)
        return best

    return recurse((1 << n_worlds) - 1, (1 << len(task.queries)) - 1, budget)


def optimal_nonadaptive_deadline_mass(
    task: FiniteTask,
    world_probabilities: Sequence[float],
    *,
    budget: int,
    allow_guess: bool = False,
) -> float:
    """Best budget-limited PRECOMMITTED query subset with no conditional choice.

    Unlike the all-or-nothing universal resolving bundle (cost C_F), this
    comparator may use an incomplete fixed subset and report only its
    identifiable states, or make the Bayesian best guess. It is the fair
    deadline-matched nonadaptive policy class: no outcome-contingent
    next-query selection, but no artificially forbidden early decisions.
    """
    from itertools import combinations

    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(allow_guess) is not bool:
        raise ValueError("allow_guess must be boolean")
    if len(world_probabilities) != len(task.worlds):
        raise ValueError("one probability required per represented world")
    weights = tuple(float(p) for p in world_probabilities)
    if any(not math.isfinite(p) or p <= 0 for p in weights):
        raise ValueError("world probabilities must be finite and strictly positive")
    if not math.isclose(sum(weights), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("world probabilities must sum to one")

    targets = tuple(w.target for w in task.worlds)
    best = 0.0
    for size in range(len(task.queries) + 1):
        for subset in combinations(range(len(task.queries)), size):
            if sum(task.queries[j].cost for j in subset) > budget:
                continue
            outcomes: dict[tuple[object, ...], list[int]] = {}
            for i in range(len(task.worlds)):
                signature = tuple(task.queries[j].outcomes[i] for j in subset)
                outcomes.setdefault(signature, []).append(i)
            score = 0.0
            for group in outcomes.values():
                if allow_guess:
                    score += max(
                        sum(weights[i] for i in group if targets[i] == target)
                        for target in {targets[i] for i in group}
                    )
                elif len({targets[i] for i in group}) == 1:
                    score += sum(weights[i] for i in group)
            best = max(best, score)
    return best
