"""Deterministic schedule construction for the direct routeability experiment.

The schedule keeps architecture, access mode, and budget between individuals.
Within individuals it balances the four ecological states, physical terminal
positions, and state-independent fixed-cue order. Binary cue symbols are
counterbalanced across individuals with a four-profile orthogonal design.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .ecological_routeability_experiment import (
    bypass_matched_control_task,
    experimental_stimulus_table,
)
from .minimal_normal_form import minimal_strict_gain_standard_task

ARCHITECTURES = ("routeable", "bypass_control")
ACCESS_MODES = ("contingent", "fixed")
BUDGETS = (1, 2, 3)

# Across these four profiles, every cue outcome symbol is flipped in half of
# individuals and every pair of cue-flip bits realizes all four combinations.
ORTHOGONAL_SYMBOL_PROFILES = (
    ("cb0", (0, 0, 0)),
    ("cb1", (0, 1, 1)),
    ("cb2", (1, 0, 1)),
    ("cb3", (1, 1, 0)),
)


@dataclass(frozen=True)
class RouteabilityTrial:
    individual_id: str
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


def _task(architecture: str):
    if architecture == "routeable":
        return minimal_strict_gain_standard_task()
    if architecture == "bypass_control":
        return bypass_matched_control_task()
    raise ValueError(f"unknown architecture: {architecture!r}")


def _stimuli_by_state(architecture: str) -> dict[str, dict[str, object]]:
    return {
        str(row["state"]): row
        for row in experimental_stimulus_table(_task(architecture))
    }


def _physical_symbol(logical: object, flip: int) -> int:
    if logical not in (0, 1):
        raise ValueError("schedule builder requires binary 0/1 cue outcomes")
    return int(logical) ^ int(flip)


def _revealed_cues(
    *,
    access_mode: str,
    budget: int,
    q_route: object,
    order_swap: bool,
) -> tuple[str, ...]:
    if budget not in BUDGETS:
        raise ValueError(f"budget must be one of {BUDGETS!r}")
    if access_mode not in ACCESS_MODES:
        raise ValueError(f"unknown access mode: {access_mode!r}")

    if budget == 1:
        if access_mode == "contingent":
            return ("q_route",)
        return ("q_right",) if order_swap else ("q_left",)

    if budget == 2:
        if access_mode == "contingent":
            if q_route == 0:
                return ("q_route", "q_right")
            if q_route == 1:
                return ("q_route", "q_left")
            raise ValueError("q_route must be binary")
        return (
            ("q_right", "q_left")
            if order_swap
            else ("q_left", "q_right")
        )

    # At B=3 both access arms receive the same complete information surface.
    # Only terminal presentation order is counterbalanced.
    return (
        ("q_route", "q_right", "q_left")
        if order_swap
        else ("q_route", "q_left", "q_right")
    )


def build_between_subject_routeability_schedule(
    *,
    individuals_per_cell: int,
    blocks_per_individual: int,
    seed: int,
) -> tuple[RouteabilityTrial, ...]:
    """Build a balanced 2x2x3 between-subject experimental schedule.

    Each block contains each of the four states exactly once. Symbol mapping
    is fixed within an individual but orthogonally counterbalanced across
    individuals within every treatment cell. Terminal position and
    state-independent fixed-cue order are balanced within every four-trial
    block.
    """

    if type(individuals_per_cell) is not int or individuals_per_cell < 4:
        raise ValueError("individuals_per_cell must be an integer >= 4")
    if individuals_per_cell % len(ORTHOGONAL_SYMBOL_PROFILES) != 0:
        raise ValueError("individuals_per_cell must be a multiple of 4")
    if type(blocks_per_individual) is not int or blocks_per_individual < 1:
        raise ValueError("blocks_per_individual must be a positive integer")
    if type(seed) is not int:
        raise ValueError("seed must be an integer")

    rng = Random(seed)
    out: list[RouteabilityTrial] = []

    for architecture in ARCHITECTURES:
        stimuli = _stimuli_by_state(architecture)
        states = tuple(sorted(stimuli))
        if len(states) != 4:
            raise AssertionError("expected exactly four stimulus states")

        for access_mode in ACCESS_MODES:
            for budget in BUDGETS:
                cell = f"{architecture}__{access_mode}__B{budget}"
                for individual_index in range(individuals_per_cell):
                    profile_name, flips = ORTHOGONAL_SYMBOL_PROFILES[
                        individual_index % len(ORTHOGONAL_SYMBOL_PROFILES)
                    ]
                    individual_id = f"{cell}__i{individual_index + 1:03d}"
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
                            row = stimuli[state]
                            position_swap = position_swaps[trial_in_block - 1]
                            order_swap = order_swaps[trial_in_block - 1]

                            if position_swap:
                                q_left_position, q_right_position = "window_B", "window_A"
                            else:
                                q_left_position, q_right_position = "window_A", "window_B"

                            revealed = _revealed_cues(
                                access_mode=access_mode,
                                budget=budget,
                                q_route=row["q_route"],
                                order_swap=order_swap,
                            )

                            out.append(
                                RouteabilityTrial(
                                    individual_id=individual_id,
                                    treatment_cell=cell,
                                    architecture=architecture,
                                    access_mode=access_mode,
                                    budget=budget,
                                    counterbalance_profile=profile_name,
                                    block=block,
                                    trial_in_block=trial_in_block,
                                    trial_index=trial_index,
                                    state=state,
                                    target=row["target"],
                                    q_left_logical=row["q_left"],
                                    q_route_logical=row["q_route"],
                                    q_right_logical=row["q_right"],
                                    q_left_symbol=_physical_symbol(row["q_left"], flips[0]),
                                    q_route_symbol=_physical_symbol(row["q_route"], flips[1]),
                                    q_right_symbol=_physical_symbol(row["q_right"], flips[2]),
                                    terminal_position_swap=position_swap,
                                    q_left_position=q_left_position,
                                    q_right_position=q_right_position,
                                    order_swap=order_swap,
                                    revealed_cues=revealed,
                                )
                            )

    return tuple(out)


def schedule_balance_audit(
    trials: tuple[RouteabilityTrial, ...],
) -> dict[str, object]:
    """Return deterministic balance checks for a generated schedule."""

    by_individual: dict[str, list[RouteabilityTrial]] = {}
    by_cell_individuals: dict[str, set[str]] = {}
    for trial in trials:
        by_individual.setdefault(trial.individual_id, []).append(trial)
        by_cell_individuals.setdefault(trial.treatment_cell, set()).add(
            trial.individual_id
        )

    individual_state_balance = True
    individual_position_balance = True
    individual_order_balance = True
    single_cell_per_individual = True
    for rows in by_individual.values():
        state_counts: dict[str, int] = {}
        position_counts = {False: 0, True: 0}
        order_counts = {False: 0, True: 0}
        cells = {row.treatment_cell for row in rows}
        single_cell_per_individual &= len(cells) == 1
        for row in rows:
            state_counts[row.state] = state_counts.get(row.state, 0) + 1
            position_counts[row.terminal_position_swap] += 1
            order_counts[row.order_swap] += 1
        individual_state_balance &= len(set(state_counts.values())) == 1
        individual_position_balance &= position_counts[False] == position_counts[True]
        individual_order_balance &= order_counts[False] == order_counts[True]

    cell_sizes = {cell: len(ids) for cell, ids in by_cell_individuals.items()}
    symbol_profiles_balanced = True
    for cell, ids in by_cell_individuals.items():
        counts = {name: 0 for name, _ in ORTHOGONAL_SYMBOL_PROFILES}
        for individual_id in ids:
            rows = by_individual[individual_id]
            counts[rows[0].counterbalance_profile] += 1
        symbol_profiles_balanced &= len(set(counts.values())) == 1

    return {
        "trial_count": len(trials),
        "individual_count": len(by_individual),
        "treatment_cell_count": len(by_cell_individuals),
        "cell_sizes": cell_sizes,
        "single_cell_per_individual": single_cell_per_individual,
        "individual_state_balance": individual_state_balance,
        "individual_terminal_position_balance": individual_position_balance,
        "individual_order_balance": individual_order_balance,
        "symbol_profiles_balanced_within_cells": symbol_profiles_balanced,
    }
