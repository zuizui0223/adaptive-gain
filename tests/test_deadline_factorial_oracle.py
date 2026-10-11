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
    optimal_nonadaptive_deadline_mass,
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


def test_same_skew_prior_flips_topology_rank_between_certainty_and_guessing():
    prior = (0.5, 0.125, 0.125, 0.125, 0.125)
    easy = task_for_topology("routeable")
    sequential = task_for_topology("sequential")
    certified = (
        optimal_timely_resolution_mass(easy, prior, budget=1),
        optimal_timely_resolution_mass(sequential, prior, budget=1),
    )
    correct = (
        optimal_deadline_correct_choice_mass(easy, prior, budget=1),
        optimal_deadline_correct_choice_mass(sequential, prior, budget=1),
    )
    assert certified == pytest.approx((0.125, 0.5), abs=1e-12)
    assert correct == pytest.approx((0.875, 0.75), abs=1e-12)
    assert certified[0] < certified[1]  # B certifies more worlds in one cue.
    assert correct[0] > correct[1]  # A is more accurate when guesses are allowed.


@pytest.mark.parametrize(
    ("name", "certified", "guessed"),
    (
        ("routeable", (0.0, 0.2, 0.6, 1.0), (0.6, 0.8, 0.8, 1.0)),
        ("sequential", (0.0, 0.2, 0.4, 1.0), (0.6, 0.6, 0.8, 1.0)),
    ),
)
def test_fair_nonadaptive_partial_query_baseline_uniform(name, certified, guessed):
    task = task_for_topology(name)
    assert tuple(
        optimal_nonadaptive_deadline_mass(task, UNIFORM, budget=b)
        for b in range(4)
    ) == pytest.approx(certified, abs=1e-12)
    assert tuple(
        optimal_nonadaptive_deadline_mass(task, UNIFORM, budget=b, allow_guess=True)
        for b in range(4)
    ) == pytest.approx(guessed, abs=1e-12)


@pytest.mark.parametrize("name", ("routeable", "sequential"))
@pytest.mark.parametrize(
    "prior", (UNIFORM, (0.5, 0.125, 0.125, 0.125, 0.125))
)
def test_adaptive_information_policy_dominates_budget_matched_nonadaptive(name, prior):
    task = task_for_topology(name)
    for b in range(4):
        assert optimal_timely_resolution_mass(task, prior, budget=b) + 1e-12 >= (
            optimal_nonadaptive_deadline_mass(task, prior, budget=b)
        )
        assert optimal_deadline_correct_choice_mass(task, prior, budget=b) + 1e-12 >= (
            optimal_nonadaptive_deadline_mass(task, prior, budget=b, allow_guess=True)
        )


def test_contingent_advantage_not_artifact_of_forcing_fixed_full_bundle():
    a = task_for_topology("routeable")
    b = task_for_topology("sequential")
    # At two queries, A has a conditional advantage against a fair partial
    # nonadaptive query plan; B does not.
    cert_advantage = (
        optimal_timely_resolution_mass(a, UNIFORM, budget=2)
        - optimal_nonadaptive_deadline_mass(a, UNIFORM, budget=2),
        optimal_timely_resolution_mass(b, UNIFORM, budget=2)
        - optimal_nonadaptive_deadline_mass(b, UNIFORM, budget=2),
    )
    accuracy_advantage = (
        optimal_deadline_correct_choice_mass(a, UNIFORM, budget=2)
        - optimal_nonadaptive_deadline_mass(a, UNIFORM, budget=2, allow_guess=True),
        optimal_deadline_correct_choice_mass(b, UNIFORM, budget=2)
        - optimal_nonadaptive_deadline_mass(b, UNIFORM, budget=2, allow_guess=True),
    )
    assert cert_advantage == pytest.approx((0.4, 0.0), abs=1e-12)
    assert accuracy_advantage == pytest.approx((0.2, 0.0), abs=1e-12)


@pytest.mark.parametrize("t", (0.21, 0.25, 1.0 / 3.0, 0.5, 0.75, 0.95))
def test_strict_endpoint_rank_reversal_over_open_encounter_family(t):
    # The one-cue ranking flip is an objective effect, not an adaptive-control
    # effect: with only one cue, contingent and fixed-subset access coincide.
    q = (1.0 - t) / 4.0
    prior = (t, q, q, q, q)
    a = task_for_topology("routeable")
    b = task_for_topology("sequential")
    certain_a = optimal_timely_resolution_mass(a, prior, budget=1)
    certain_b = optimal_timely_resolution_mass(b, prior, budget=1)
    guess_a = optimal_deadline_correct_choice_mass(a, prior, budget=1)
    guess_b = optimal_deadline_correct_choice_mass(b, prior, budget=1)
    assert certain_a == pytest.approx(q)
    assert certain_b == pytest.approx(t)
    assert guess_a == pytest.approx(t + 3*q)
    assert guess_b == pytest.approx(t + 2*q)
    assert certain_b - certain_a == pytest.approx((5*t-1)/4)
    assert guess_a - guess_b == pytest.approx((1-t)/4)
    assert certain_b > certain_a
    assert guess_a > guess_b
    for task in (a, b):
        for guessing, adaptive in (
            (False, optimal_timely_resolution_mass),
            (True, optimal_deadline_correct_choice_mass),
        ):
            assert adaptive(task, prior, budget=1) == pytest.approx(
                optimal_nonadaptive_deadline_mass(
                    task, prior, budget=1, allow_guess=guessing
                ),
                abs=1e-12,
            )


@pytest.mark.parametrize("t", (0.21, 0.25, 1.0 / 3.0, 0.5, 0.75, 0.95))
def test_true_two_query_adaptivity_premium_over_same_encounter_family(t):
    q = (1-t)/4
    prior = (t,q,q,q,q)
    a=task_for_topology("routeable")
    b=task_for_topology("sequential")
    a_cert=optimal_timely_resolution_mass(a,prior,budget=2)
    af_cert=optimal_nonadaptive_deadline_mass(a,prior,budget=2)
    a_guess=optimal_deadline_correct_choice_mass(a,prior,budget=2)
    af_guess=optimal_nonadaptive_deadline_mass(a,prior,budget=2,allow_guess=True)
    b_cert=optimal_timely_resolution_mass(b,prior,budget=2)
    bf_cert=optimal_nonadaptive_deadline_mass(b,prior,budget=2)
    b_guess=optimal_deadline_correct_choice_mass(b,prior,budget=2)
    bf_guess=optimal_nonadaptive_deadline_mass(b,prior,budget=2,allow_guess=True)
    assert a_cert==pytest.approx(1)
    assert af_cert==pytest.approx(t+2*q)
    assert a_cert-af_cert==pytest.approx(2*q)
    assert a_guess==pytest.approx(1)
    assert af_guess==pytest.approx(t+3*q)
    assert a_guess-af_guess==pytest.approx(q)
    assert b_cert==pytest.approx(bf_cert)
    assert b_guess==pytest.approx(bf_guess)


def test_maximin_prior_within_declared_one_parameter_family():
    # For 1/5<t<1, the two strict reversal margins are t-q and q.
    # Their minimum is maximized where t-q=q => t=1/3.
    t=1/3
    q=(1-t)/4
    gap_cert=t-q
    gap_guess=q
    assert gap_cert==pytest.approx(1/6)
    assert gap_guess==pytest.approx(1/6)
    for other_t in (0.21,0.25,0.3,0.4,0.5,0.7,0.9):
        other_q=(1-other_t)/4
        assert min(other_t-other_q,other_q)<min(gap_cert,gap_guess)
