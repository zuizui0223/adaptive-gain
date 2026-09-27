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

from dataclasses import dataclass

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
        routeable_adaptive_accuracy=1.0 if routeable_receipt.adaptive_cost == 2 else 0.0,
        control_adaptive_accuracy=1.0 if control_receipt.adaptive_cost <= 2 else 0.0,
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
