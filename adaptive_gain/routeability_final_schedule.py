"""Compile frozen roster assignments into the final individual trial schedule."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from random import Random
from typing import Iterable

from .routeability_experiment_schedule import (
    ORTHOGONAL_SYMBOL_PROFILES,
    RouteabilityTrial,
    _physical_symbol,
    _revealed_cues,
    _stimuli_by_state,
)
from .routeability_roster_randomization import RouteabilityRosterAssignment


PROFILE_FLIPS = dict(ORTHOGONAL_SYMBOL_PROFILES)


@dataclass(frozen=True)
class FinalRouteabilityTrial:
    individual_id: str
    colony_id: str
    complete_block_id: str
    treatment_cell: str
    architecture: str
    access_mode: str
    budget: int
    counterbalance_profile: str
    block: int
    trial_in_block: int
    trial_index: int
    state: str
    target: object
    q_left_logical: object
    q_route_logical: object
    q_right_logical: object
    q_left_symbol: int
    q_route_symbol: int
    q_right_symbol: int
    terminal_position_swap: bool
    q_left_position: str
    q_right_position: str
    order_swap: bool
    revealed_cues: tuple[str, ...]


def _individual_seed(global_seed: int, assignment: RouteabilityRosterAssignment) -> int:
    payload = (
        f"{global_seed}|{assignment.individual_id}|{assignment.colony_id}|"
        f"{assignment.treatment_cell}|{assignment.counterbalance_profile}"
    ).encode("utf-8")
    return int.from_bytes(sha256(payload).digest()[:8], "big", signed=False)


def compile_assigned_routeability_schedule(
    assignments: Iterable[RouteabilityRosterAssignment],
    *,
    blocks_per_individual: int,
    global_seed: int,
) -> tuple[FinalRouteabilityTrial, ...]:
    """Compile actual randomized individuals into deterministic trial schedules.

    The per-individual RNG seed is derived from the frozen global seed and
    assignment identity, so output is invariant to CSV row order.
    """

    if type(blocks_per_individual) is not int or blocks_per_individual < 1:
        raise ValueError("blocks_per_individual must be a positive integer")
    if type(global_seed) is not int or global_seed < 0:
        raise ValueError("global_seed must be a non-negative integer")

    rows = tuple(assignments)
    if not rows:
        raise ValueError("assignments cannot be empty")

    seen = set()
    for assignment in rows:
        if assignment.individual_id in seen:
            raise ValueError(f"duplicate assigned individual_id: {assignment.individual_id!r}")
        seen.add(assignment.individual_id)
        expected_cell = (
            f"{assignment.architecture}__{assignment.access_mode}__B{assignment.budget}"
        )
        if assignment.treatment_cell != expected_cell:
            raise ValueError(
                f"treatment_cell mismatch for {assignment.individual_id!r}: "
                f"{assignment.treatment_cell!r} != {expected_cell!r}"
            )
        if assignment.counterbalance_profile not in PROFILE_FLIPS:
            raise ValueError(
                f"unknown counterbalance profile: {assignment.counterbalance_profile!r}"
            )

    output: list[FinalRouteabilityTrial] = []
    for assignment in sorted(rows, key=lambda row: row.individual_id):
        stimuli = _stimuli_by_state(assignment.architecture)
        states = tuple(sorted(stimuli))
        if len(states) != 4:
            raise AssertionError("expected exactly four stimulus states")

        rng = Random(_individual_seed(global_seed, assignment))
        flips = PROFILE_FLIPS[assignment.counterbalance_profile]
        trial_index = 0

        for block in range(1, blocks_per_individual + 1):
            block_states = list(states)
            rng.shuffle(block_states)

            position_swaps = [False, False, True, True]
            order_swaps = [False, False, True, True]
            rng.shuffle(position_swaps)
            rng.shuffle(order_swaps)

            for trial_in_block, state in enumerate(block_states, start=1):
                trial_index += 1
                stimulus = stimuli[state]
                position_swap = position_swaps[trial_in_block - 1]
                order_swap = order_swaps[trial_in_block - 1]

                if position_swap:
                    q_left_position, q_right_position = "window_B", "window_A"
                else:
                    q_left_position, q_right_position = "window_A", "window_B"

                revealed = _revealed_cues(
                    access_mode=assignment.access_mode,
                    budget=assignment.budget,
                    q_route=stimulus["q_route"],
                    order_swap=order_swap,
                )

                output.append(
                    FinalRouteabilityTrial(
                        individual_id=assignment.individual_id,
                        colony_id=assignment.colony_id,
                        complete_block_id=assignment.complete_block_id,
                        treatment_cell=assignment.treatment_cell,
                        architecture=assignment.architecture,
                        access_mode=assignment.access_mode,
                        budget=assignment.budget,
                        counterbalance_profile=assignment.counterbalance_profile,
                        block=block,
                        trial_in_block=trial_in_block,
                        trial_index=trial_index,
                        state=state,
                        target=stimulus["target"],
                        q_left_logical=stimulus["q_left"],
                        q_route_logical=stimulus["q_route"],
                        q_right_logical=stimulus["q_right"],
                        q_left_symbol=_physical_symbol(stimulus["q_left"], flips[0]),
                        q_route_symbol=_physical_symbol(stimulus["q_route"], flips[1]),
                        q_right_symbol=_physical_symbol(stimulus["q_right"], flips[2]),
                        terminal_position_swap=position_swap,
                        q_left_position=q_left_position,
                        q_right_position=q_right_position,
                        order_swap=order_swap,
                        revealed_cues=revealed,
                    )
                )

    return tuple(output)


def final_schedule_audit(
    assignments: Iterable[RouteabilityRosterAssignment],
    trials: Iterable[FinalRouteabilityTrial],
) -> dict[str, object]:
    assignments = tuple(assignments)
    trials = tuple(trials)
    by_assignment = {row.individual_id: row for row in assignments}
    by_individual: dict[str, list[FinalRouteabilityTrial]] = {}
    for trial in trials:
        by_individual.setdefault(trial.individual_id, []).append(trial)

    assignment_ids = set(by_assignment)
    trial_ids = set(by_individual)

    identity_match = assignment_ids == trial_ids
    assignment_fidelity = identity_match
    state_balance = True
    side_balance = True
    order_balance = True

    for individual_id, rows in by_individual.items():
        assignment = by_assignment.get(individual_id)
        if assignment is None:
            assignment_fidelity = False
            continue
        assignment_fidelity &= all(
            row.colony_id == assignment.colony_id
            and row.complete_block_id == assignment.complete_block_id
            and row.treatment_cell == assignment.treatment_cell
            and row.architecture == assignment.architecture
            and row.access_mode == assignment.access_mode
            and row.budget == assignment.budget
            and row.counterbalance_profile == assignment.counterbalance_profile
            for row in rows
        )

        state_counts: dict[str, int] = {}
        side_counts = {False: 0, True: 0}
        order_counts = {False: 0, True: 0}
        for row in rows:
            state_counts[row.state] = state_counts.get(row.state, 0) + 1
            side_counts[row.terminal_position_swap] += 1
            order_counts[row.order_swap] += 1

        state_balance &= len(state_counts) == 4 and len(set(state_counts.values())) == 1
        side_balance &= side_counts[False] == side_counts[True]
        order_balance &= order_counts[False] == order_counts[True]

    return {
        "assignment_individual_count": len(assignment_ids),
        "scheduled_individual_count": len(trial_ids),
        "trial_count": len(trials),
        "individual_identity_match": identity_match,
        "assignment_fidelity": assignment_fidelity,
        "individual_state_balance": state_balance,
        "individual_terminal_position_balance": side_balance,
        "individual_order_balance": order_balance,
    }
