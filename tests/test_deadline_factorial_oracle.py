"""Independent tree enumeration: certified identification versus lucky guessing.

This oracle enumerates possible policy subtrees (all outcomes and all terminal
stop decisions) and scores them at their leaves. It deliberately does not call
the production dynamic-programming solver.
"""

from itertools import product

import pytest

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.deadline_factorial import (
    optimal_deadline_correct_choice_mass,
    optimal_timely_resolution_mass,
)
TARGETS = (0, 1, 1, 0, 0)
UNIFORM = (0.2,) * 5


def task_for_topology(name):
    if name == "routeable":
        vectors = ((0, 0, 1, 1, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0))
    elif name == "sequential":
        vectors = ((1, 0, 0, 0, 0), (0, 0, 0, 1, 0), (1, 1, 1, 1, 0))
    else:
        raise ValueError(name)
    return FiniteTask(
        tuple(World(f"world_{i}", target) for i, target in enumerate(TARGETS)),
        tuple(Query(f"q_{j}", 1, vec) for j, vec in enumerate(vectors)),
    )


def exhaustive_policy_leaf_scores(task, prior, *, budget, guessing):
    states = frozenset(range(len(task.worlds)))

    def all_scores(remaining_worlds, unused_queries, remaining_budget):
        mass_by_target = {}
        for i in remaining_worlds:
            t = task.worlds[i].target
            mass_by_target[t] = mass_by_target.get(t, 0.0) + prior[i]
        if guessing:
            score_if_stop = max(mass_by_target.values())
        else:
            score_if_stop = sum(mass_by_target.values()) if len(mass_by_target) == 1 else 0.0

        scores = {round(score_if_stop, 12)}
        for j in unused_queries:
            q = task.queries[j]
            if q.cost > remaining_budget:
                continue
            parts = {}
            for i in remaining_worlds:
                parts.setdefault(q.outcomes[i], set()).add(i)
            if len(parts) < 2:
                continue
            children = [
                all_scores(
                    frozenset(members),
                    frozenset(k for k in unused_queries if k != j),
                    remaining_budget - q.cost,
                )
                for members in parts.values()
            ]
            for child_combo in product(*children):
                scores.add(round(sum(child_combo), 12))
        return scores

    return all_scores(states, frozenset(range(len(task.queries))), budget)


@pytest.mark.parametrize("name", ("routeable", "sequential"))
@pytest.mark.parametrize(
    "prior",
    (
        UNIFORM,
        (0.5, 0.125, 0.125, 0.125, 0.125),
    ),
)
@pytest.mark.parametrize("budget", (0, 1, 2, 3))
def test_two_endpoints_equal_independent_policy_enumeration(name, prior, budget):
    task = task_for_topology(name)
    for guessing, solver in (
        (False, optimal_timely_resolution_mass),
        (True, optimal_deadline_correct_choice_mass),
    ):
        independent = max(exhaustive_policy_leaf_scores(
            task, prior, budget=budget, guessing=guessing
        ))
        assert solver(task, prior, budget=budget) == pytest.approx(independent, abs=1e-11)


@pytest.mark.parametrize(
    ("name", "profile"),
    (
        ("routeable", (0.6, 0.8, 1.0, 1.0)),
        ("sequential", (0.6, 0.6, 0.8, 1.0)),
    ),
)
def test_balanced_prior_best_guess_profiles(name, profile):
    task = task_for_topology(name)
    assert tuple(
        optimal_deadline_correct_choice_mass(task, UNIFORM, budget=b)
        for b in range(4)
    ) == pytest.approx(profile, abs=1e-12)


def test_even_at_zero_budget_majority_guess_beats_certified_resolution():
    task = task_for_topology("routeable")
    assert sum(TARGETS) == 2
    assert optimal_timely_resolution_mass(task, UNIFORM, budget=0) == 0.0
    assert optimal_deadline_correct_choice_mass(task, UNIFORM, budget=0) == pytest.approx(0.6)


def test_costly_query_and_invalid_prior():
    task = task_for_topology("routeable")
    expensive = FiniteTask(
        task.worlds,
        tuple(Query(q.name, q.cost * 2, q.outcomes) for q in task.queries),
    )
    assert optimal_deadline_correct_choice_mass(expensive, UNIFORM, budget=1) == pytest.approx(0.6)
    for bad in ((0.25,) * 4, (0.1,) * 5, (0.2, 0.2, 0.2, 0.2, 0)):
        with pytest.raises(ValueError):
            optimal_deadline_correct_choice_mass(task, bad, budget=1)
    with pytest.raises(ValueError):
        optimal_deadline_correct_choice_mass(task, UNIFORM, budget=-1)
