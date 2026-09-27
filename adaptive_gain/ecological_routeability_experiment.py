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


def ecological_routeability_experiment_contrast() -> ExperimentalRouteabilityContrast:
    routeable = minimal_strict_gain_standard_task()
    control = bypass_matched_control_task()
    routeable_receipt = adaptive_gain_receipt(routeable)
    control_receipt = adaptive_gain_receipt(control)

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
