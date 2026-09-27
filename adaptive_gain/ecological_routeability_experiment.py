"""Exact four-state experimental contrast for ecological routeability.

The routeable and bypass-control tasks share:

- four represented states;
- balanced 2+2 target classes;
- three unit-cost binary cues;
- the same per-cue outcome multiplicities: 1/3, 2/2, and 3/1.

They differ in structure. The routeable task has C_A=2 and C_F=3, whereas
the bypass control has C_A=C_F=2. This makes the pair suitable as a minimal
stimulus-design target when ecological cues can be acquired separately.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
from math import log2
from typing import Mapping, Sequence

from .core import FiniteTask, Query, World, adaptive_gain_receipt
from .minimal_normal_form import minimal_strict_gain_standard_task


@dataclass(frozen=True)
class ExperimentalRouteabilityContrast:
    routeable_adaptive_cost: int | None
    routeable_fixed_cost: int | None
    control_adaptive_cost: int | None
    control_fixed_cost: int | None
    same_world_count: bool
    same_target_multiplicities: bool
    same_query_outcome_multiplicities: bool
    routeable_strict_gain: bool
    control_strict_gain: bool
    routeable_fixed_terminal_accuracy: float
    control_fixed_terminal_accuracy: float
    routeable_adaptive_accuracy: float
    control_adaptive_accuracy: float
    same_pairwise_information_signatures: bool
    routeable_terminal_pair_target_information_bits: float
    control_terminal_pair_target_information_bits: float
    routeable_context_given_terminals_information_bits: float
    control_context_given_terminals_information_bits: float

    @property
    def exact_minimal_contrast(self) -> bool:
        return (
            self.routeable_adaptive_cost == 2
            and self.routeable_fixed_cost == 3
            and self.control_adaptive_cost == 2
            and self.control_fixed_cost == 2
            and self.same_world_count
            and self.same_target_multiplicities
            and self.same_query_outcome_multiplicities
            and self.routeable_strict_gain
            and not self.control_strict_gain
            and self.routeable_fixed_terminal_accuracy == 0.75
            and self.control_fixed_terminal_accuracy == 1.0
            and self.routeable_adaptive_accuracy == 1.0
            and self.control_adaptive_accuracy == 1.0
            and self.same_pairwise_information_signatures
            and self.routeable_terminal_pair_target_information_bits == 0.5
            and self.control_terminal_pair_target_information_bits == 1.0
            and self.routeable_context_given_terminals_information_bits == 0.5
            and self.control_context_given_terminals_information_bits == 0.0
        )


def bypass_matched_control_task() -> FiniteTask:
    """Return a no-gain control matched on cue outcome multiplicities.

    With targets (0,0,1,1), the cue maps have 1, 2, and 3 positive outcomes,
    exactly matching the minimal strict-gain standard task. The task is
    globally resolvable by the two terminal cues, so the balanced route cue is
    bypassable and C_A=C_F=2.
    """

    worlds = (
        World("w0", 0),
        World("w1", 0),
        World("w2", 1),
        World("w3", 1),
    )
    return FiniteTask(
        worlds,
        (
            Query("q_left", 1, (0, 0, 0, 1)),
            Query("q_route", 1, (0, 1, 0, 1)),
            Query("q_right", 1, (1, 1, 0, 1)),
        ),
    )


def _target_multiplicities(task: FiniteTask) -> tuple[int, ...]:
    counts: dict[object, int] = {}
    for world in task.worlds:
        counts[world.target] = counts.get(world.target, 0) + 1
    return tuple(sorted(counts.values()))


def _query_outcome_multiplicities(task: FiniteTask) -> tuple[tuple[int, ...], ...]:
    rows = []
    for query in task.queries:
        counts: dict[object, int] = {}
        for outcome in query.outcomes:
            counts[outcome] = counts.get(outcome, 0) + 1
        rows.append(tuple(sorted(counts.values())))
    return tuple(rows)



def uniform_target_accuracy_for_query_bundle(
    task: FiniteTask,
    query_names: tuple[str, ...],
) -> float:
    """Bayes-optimal target accuracy under a uniform distribution of states.

    The observer sees only the named cue outcomes. Within each unresolved
    outcome pattern, the best possible classifier predicts the majority target.
    """

    lookup = {query.name: query for query in task.queries}
    missing = [name for name in query_names if name not in lookup]
    if missing:
        raise ValueError(f"unknown query names: {missing!r}")

    pattern_targets: dict[tuple[object, ...], dict[object, int]] = {}
    for i, world in enumerate(task.worlds):
        pattern = tuple(lookup[name].outcomes[i] for name in query_names)
        counts = pattern_targets.setdefault(pattern, {})
        counts[world.target] = counts.get(world.target, 0) + 1

    correct = sum(max(counts.values()) for counts in pattern_targets.values())
    return correct / len(task.worlds)


def uniform_target_accuracy_for_context_policy(
    task: FiniteTask,
    *,
    context_query: str = "q_route",
    branch_queries: Mapping[object, str] | None = None,
) -> float:
    """Bayes-optimal accuracy after one context cue and one routed terminal cue.

    The default policy is q_route=0 -> q_right and q_route=1 -> q_left.
    The same physical policy is used for both experimental architectures.
    """

    if branch_queries is None:
        branch_queries = {0: "q_right", 1: "q_left"}

    lookup = {query.name: query for query in task.queries}
    if context_query not in lookup:
        raise ValueError(f"unknown context query: {context_query!r}")
    missing = [
        query_name
        for query_name in branch_queries.values()
        if query_name not in lookup
    ]
    if missing:
        raise ValueError(f"unknown branch query names: {missing!r}")

    context = lookup[context_query]
    pattern_targets: dict[tuple[object, object], dict[object, int]] = {}
    for i, world in enumerate(task.worlds):
        context_outcome = context.outcomes[i]
        if context_outcome not in branch_queries:
            raise ValueError(
                f"no branch query frozen for context outcome {context_outcome!r}"
            )
        terminal = lookup[branch_queries[context_outcome]]
        pattern = (context_outcome, terminal.outcomes[i])
        counts = pattern_targets.setdefault(pattern, {})
        counts[world.target] = counts.get(world.target, 0) + 1

    correct = sum(max(counts.values()) for counts in pattern_targets.values())
    return correct / len(task.worlds)

def _uniform_entropy(values: Sequence[object]) -> float:
    """Shannon entropy in bits under the uniform distribution over rows."""

    if not values:
        raise ValueError("entropy requires at least one value")
    counts = Counter(values)
    n = len(values)
    return -sum(
        (count / n) * log2(count / n)
        for count in counts.values()
    )


def uniform_target_information_for_query_bundle(
    task: FiniteTask,
    query_names: tuple[str, ...],
) -> float:
    """Mutual information I(target; query bundle) in bits under uniform states."""

    lookup = {query.name: query for query in task.queries}
    missing = [name for name in query_names if name not in lookup]
    if missing:
        raise ValueError(f"unknown query names: {missing!r}")

    target = tuple(world.target for world in task.worlds)
    bundle = tuple(
        tuple(lookup[name].outcomes[i] for name in query_names)
        for i in range(len(task.worlds))
    )
    joint = tuple(zip(target, bundle))
    return _uniform_entropy(target) + _uniform_entropy(bundle) - _uniform_entropy(joint)


def uniform_target_conditional_information_for_query(
    task: FiniteTask,
    query_name: str,
    *,
    given_query_names: tuple[str, ...],
) -> float:
    """Conditional mutual information I(target; query | given bundle) in bits."""

    lookup = {query.name: query for query in task.queries}
    names = (query_name,) + given_query_names
    missing = [name for name in names if name not in lookup]
    if missing:
        raise ValueError(f"unknown query names: {missing!r}")

    target = tuple(world.target for world in task.worlds)
    query = tuple(lookup[query_name].outcomes)
    given = tuple(
        tuple(lookup[name].outcomes[i] for name in given_query_names)
        for i in range(len(task.worlds))
    )
    target_given = tuple(zip(target, given))
    query_given = tuple(zip(query, given))
    joint = tuple(zip(target, query, given))
    return (
        _uniform_entropy(target_given)
        + _uniform_entropy(query_given)
        - _uniform_entropy(given)
        - _uniform_entropy(joint)
    )

def _binary_unlabeled_pair_signature(
    left: Sequence[object],
    right: Sequence[object],
) -> tuple[int, int, int, int]:
    """Canonical 2x2 contingency counts up to independent binary relabeling.

    Equal signatures imply equal pairwise mutual information and equal
    binary association strength for any statistic invariant to independent
    relabeling of the two binary outcomes.
    """

    if len(left) != len(right):
        raise ValueError("paired variables must have the same length")
    if set(left) - {0, 1} or set(right) - {0, 1}:
        raise ValueError("pairwise information signature requires binary 0/1 values")

    candidates: list[tuple[int, int, int, int]] = []
    for flip_left, flip_right in product((False, True), repeat=2):
        counts = {(a, b): 0 for a in (0, 1) for b in (0, 1)}
        for raw_left, raw_right in zip(left, right):
            a = 1 - raw_left if flip_left else raw_left
            b = 1 - raw_right if flip_right else raw_right
            counts[(a, b)] += 1
        candidates.append(
            (
                counts[(0, 0)],
                counts[(0, 1)],
                counts[(1, 0)],
                counts[(1, 1)],
            )
        )
    return min(candidates)


def pairwise_information_signature(
    task: FiniteTask,
) -> tuple[tuple[str, str, tuple[int, int, int, int]], ...]:
    """Return the named pairwise binary-information surface of a task.

    Target and cue values are reduced pair-by-pair to canonical unlabeled
    2x2 contingency counts. This is stronger than comparing pairwise mutual
    information numerically while treating arbitrary binary cue symbols as
    labels rather than ecological content.
    """

    variables: list[tuple[str, tuple[object, ...]]] = [
        ("target", tuple(world.target for world in task.worlds))
    ]
    variables.extend(
        (query.name, tuple(query.outcomes))
        for query in task.queries
    )

    rows = []
    for (left_name, left), (right_name, right) in combinations(variables, 2):
        rows.append(
            (
                left_name,
                right_name,
                _binary_unlabeled_pair_signature(left, right),
            )
        )
    return tuple(rows)

def ecological_routeability_experiment_contrast() -> ExperimentalRouteabilityContrast:
    routeable = minimal_strict_gain_standard_task()
    control = bypass_matched_control_task()
    routeable_receipt = adaptive_gain_receipt(routeable)
    control_receipt = adaptive_gain_receipt(control)

    routeable_fixed_terminal_accuracy = uniform_target_accuracy_for_query_bundle(
        routeable, ("q_left", "q_right")
    )
    control_fixed_terminal_accuracy = uniform_target_accuracy_for_query_bundle(
        control, ("q_left", "q_right")
    )
    routeable_adaptive_accuracy = uniform_target_accuracy_for_context_policy(
        routeable
    )
    control_adaptive_accuracy = uniform_target_accuracy_for_context_policy(
        control
    )
    same_pairwise_information_signatures = (
        pairwise_information_signature(routeable)
        == pairwise_information_signature(control)
    )
    routeable_terminal_pair_target_information_bits = (
        uniform_target_information_for_query_bundle(
            routeable, ("q_left", "q_right")
        )
    )
    control_terminal_pair_target_information_bits = (
        uniform_target_information_for_query_bundle(
            control, ("q_left", "q_right")
        )
    )
    routeable_context_given_terminals_information_bits = (
        uniform_target_conditional_information_for_query(
            routeable,
            "q_route",
            given_query_names=("q_left", "q_right"),
        )
    )
    control_context_given_terminals_information_bits = (
        uniform_target_conditional_information_for_query(
            control,
            "q_route",
            given_query_names=("q_left", "q_right"),
        )
    )

    return ExperimentalRouteabilityContrast(
        routeable_adaptive_cost=routeable_receipt.adaptive_cost,
        routeable_fixed_cost=routeable_receipt.fixed_cost,
        control_adaptive_cost=control_receipt.adaptive_cost,
        control_fixed_cost=control_receipt.fixed_cost,
        same_world_count=len(routeable.worlds) == len(control.worlds),
        same_target_multiplicities=(
            _target_multiplicities(routeable) == _target_multiplicities(control)
        ),
        same_query_outcome_multiplicities=(
            _query_outcome_multiplicities(routeable)
            == _query_outcome_multiplicities(control)
        ),
        routeable_strict_gain=routeable_receipt.strict_adaptive_gain,
        control_strict_gain=control_receipt.strict_adaptive_gain,
        routeable_fixed_terminal_accuracy=routeable_fixed_terminal_accuracy,
        control_fixed_terminal_accuracy=control_fixed_terminal_accuracy,
        routeable_adaptive_accuracy=routeable_adaptive_accuracy,
        control_adaptive_accuracy=control_adaptive_accuracy,
        same_pairwise_information_signatures=same_pairwise_information_signatures,
        routeable_terminal_pair_target_information_bits=(
            routeable_terminal_pair_target_information_bits
        ),
        control_terminal_pair_target_information_bits=(
            control_terminal_pair_target_information_bits
        ),
        routeable_context_given_terminals_information_bits=(
            routeable_context_given_terminals_information_bits
        ),
        control_context_given_terminals_information_bits=(
            control_context_given_terminals_information_bits
        ),
    )



@dataclass(frozen=True)
class BudgetInformationCeiling:
    budget: int
    routeable_adaptive_policy: float
    routeable_fixed_policy: float
    control_adaptive_policy: float
    control_fixed_policy: float

    @property
    def architecture_by_access_interaction(self) -> float:
        return (
            self.routeable_adaptive_policy
            - self.routeable_fixed_policy
            - (
                self.control_adaptive_policy
                - self.control_fixed_policy
            )
        )


def routeability_budget_information_ceilings() -> tuple[BudgetInformationCeiling, ...]:
    """Exact uniform-state ceilings for the preregistered B=1,2,3 ladder.

    B=1 compares the first observation of the adaptive policy (q_route) with
    one terminal cue from the fixed policy (q_left; q_right gives the same
    accuracy in both architectures). B=2 is the focal routeability window.
    B=3 supplies all three cues to both access arms.
    """

    routeable = minimal_strict_gain_standard_task()
    control = bypass_matched_control_task()

    b1_route_adaptive = uniform_target_accuracy_for_query_bundle(
        routeable, ("q_route",)
    )
    b1_route_fixed = uniform_target_accuracy_for_query_bundle(
        routeable, ("q_left",)
    )
    b1_control_adaptive = uniform_target_accuracy_for_query_bundle(
        control, ("q_route",)
    )
    b1_control_fixed = uniform_target_accuracy_for_query_bundle(
        control, ("q_left",)
    )

    contrast = ecological_routeability_experiment_contrast()

    return (
        BudgetInformationCeiling(
            budget=1,
            routeable_adaptive_policy=b1_route_adaptive,
            routeable_fixed_policy=b1_route_fixed,
            control_adaptive_policy=b1_control_adaptive,
            control_fixed_policy=b1_control_fixed,
        ),
        BudgetInformationCeiling(
            budget=2,
            routeable_adaptive_policy=contrast.routeable_adaptive_accuracy,
            routeable_fixed_policy=contrast.routeable_fixed_terminal_accuracy,
            control_adaptive_policy=contrast.control_adaptive_accuracy,
            control_fixed_policy=contrast.control_fixed_terminal_accuracy,
        ),
        BudgetInformationCeiling(
            budget=3,
            routeable_adaptive_policy=1.0,
            routeable_fixed_policy=1.0,
            control_adaptive_policy=1.0,
            control_fixed_policy=1.0,
        ),
    )

def experimental_stimulus_table(task: FiniteTask) -> tuple[dict[str, object], ...]:
    """Return a deterministic table for translating a task into physical stimuli."""

    rows = []
    for i, world in enumerate(task.worlds):
        row: dict[str, object] = {
            "state": world.name,
            "target": world.target,
        }
        for query in task.queries:
            row[query.name] = query.outcomes[i]
        rows.append(row)
    return tuple(rows)
