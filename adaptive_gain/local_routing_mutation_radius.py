"""Coordinated edit-radius thresholds for the local routing-pruning model.

This is a side-model extension of local_routing_mutation.py. A radius-rho
mutation may bundle at most rho of the elementary branch-pruning edits into one
mutation event. The task, cues and target remain fixed.

The results are elementary consequences of the declared L1 edit geometry and are
used only to make the small-jump/accessibility distinction explicit.
"""
from __future__ import annotations

from dataclasses import dataclass

from .local_routing_mutation import (
    RoutingPruningState,
    initial_full_program_state,
    minimum_local_prunings_for_gain,
)


def _validate_radius(edit_radius: int) -> int:
    if type(edit_radius) is not int or edit_radius < 1:
        raise ValueError("edit_radius must be a positive integer")
    return edit_radius


def minimum_one_step_edit_radius_for_gain(branch_count: int, required_gain: int) -> int:
    """Exact L1 edit radius needed to realize gain r in one mutation from full."""

    return minimum_local_prunings_for_gain(branch_count, required_gain)


def one_step_gain_reachable(
    branch_count: int,
    required_gain: int,
    edit_radius: int,
) -> bool:
    """Whether one coordinated deletion mutation can reach realized gain r."""

    rho = _validate_radius(edit_radius)
    return rho >= minimum_one_step_edit_radius_for_gain(branch_count, required_gain)


def minimum_radius_for_first_strict_gain(branch_count: int) -> int:
    """Exact one-mutation radius at which the full program gets a beneficial neighbor."""

    return minimum_one_step_edit_radius_for_gain(branch_count, 1)


def balanced_strict_improvement_path(
    branch_count: int,
    required_gain: int,
    edit_radius: int,
) -> tuple[RoutingPruningState, ...]:
    """Construct a strictly gain-increasing path when rho>=k.

    Each step prunes one occurrence from every branch, using exactly k elementary
    edits. Hence gain rises by one per mutation event until required_gain is met.
    """

    k = branch_count
    r = required_gain
    rho = _validate_radius(edit_radius)
    # Reuse validation of k and r.
    minimum_local_prunings_for_gain(k, r)
    if r == 0:
        return (initial_full_program_state(k),)
    if rho < k:
        raise ValueError("edit_radius is too small for any first strict gain from the full program")

    return tuple(
        RoutingPruningState(k, (k - gain,) * k)
        for gain in range(0, r + 1)
    )


def strict_improvement_path_exists(
    branch_count: int,
    required_gain: int,
    edit_radius: int,
) -> bool:
    """Existence of a monotone path whose every mutation strictly raises gain."""

    k = branch_count
    r = required_gain
    rho = _validate_radius(edit_radius)
    minimum_local_prunings_for_gain(k, r)
    return r == 0 or rho >= k


@dataclass(frozen=True)
class RoutingMutationRadiusReceipt:
    branch_count: int
    required_gain: int
    first_strict_gain_radius: int
    direct_target_radius: int
    unit_edit_strictly_trapped: bool
    balanced_strict_path_radius: int
    balanced_strict_path_steps: int


def routing_mutation_radius_receipt(
    branch_count: int,
    required_gain: int,
) -> RoutingMutationRadiusReceipt:
    """Summarize the two exact radius thresholds for a declared target gain."""

    k = branch_count
    r = required_gain
    minimum_local_prunings_for_gain(k, r)
    first = k if r > 0 else 0
    direct = k * r
    if r > 0:
        path = balanced_strict_improvement_path(k, r, k)
        if len(path) - 1 != r:
            raise ArithmeticError("balanced strict-improvement construction failed")
        for before, after in zip(path, path[1:]):
            if after.realized_structural_gain != before.realized_structural_gain + 1:
                raise ArithmeticError("balanced path did not raise gain by exactly one")
            elementary_edits = sum(
                a - b
                for a, b in zip(
                    before.branch_lengths,
                    after.branch_lengths,
                    strict=True,
                )
            )
            if elementary_edits != k:
                raise ArithmeticError("balanced path event did not use exactly k elementary edits")
    return RoutingMutationRadiusReceipt(
        branch_count=k,
        required_gain=r,
        first_strict_gain_radius=first,
        direct_target_radius=direct,
        unit_edit_strictly_trapped=(r > 0 and k > 1),
        balanced_strict_path_radius=(k if r > 0 else 0),
        balanced_strict_path_steps=r,
    )
