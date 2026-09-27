"""Colony-blocked individual randomization for the routeability experiment.

Eligible individuals enter this module only after architecture-neutral
familiarization/engagement screening and before any architecture-specific
training or outcome is observed.

The primary rule uses complete 12-cell treatment blocks within colony: every
block assigns one individual to each architecture x access x budget cell.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Hashable, Iterable

from .routeability_experiment_schedule import (
    ACCESS_MODES,
    ARCHITECTURES,
    BUDGETS,
    ORTHOGONAL_SYMBOL_PROFILES,
)

TREATMENT_CELLS = tuple(
    (architecture, access_mode, budget)
    for architecture in ARCHITECTURES
    for access_mode in ACCESS_MODES
    for budget in BUDGETS
)


@dataclass(frozen=True)
class RouteabilityRosterAssignment:
    individual_id: str
    colony_id: str
    complete_block_id: str
    architecture: str
    access_mode: str
    budget: int
    treatment_cell: str
    counterbalance_profile: str


@dataclass(frozen=True)
class RouteabilityRosterRandomizationReceipt:
    individuals_per_cell: int
    treatment_cell_count: int
    complete_block_count: int
    eligible_individual_count: int
    assigned_individual_count: int
    unassigned_individual_count: int
    colony_count: int
    colony_block_capacity: tuple[tuple[str, int], ...]
    assigned_blocks_by_colony: tuple[tuple[str, int], ...]
    treatment_cell_counts: tuple[tuple[str, int], ...]
    profile_counts_by_cell: tuple[
        tuple[str, tuple[tuple[str, int], ...]], ...
    ]
    complete_blocks_valid: bool
    counterbalance_profiles_valid: bool


def _cell_name(
    architecture: str,
    access_mode: str,
    budget: int,
) -> str:
    return f"{architecture}__{access_mode}__B{budget}"


def randomize_roster_complete_colony_blocks(
    roster: Iterable[tuple[Hashable, Hashable]],
    *,
    individuals_per_cell: int,
    seed: int,
) -> tuple[
    tuple[RouteabilityRosterAssignment, ...],
    tuple[tuple[str, str], ...],
    RouteabilityRosterRandomizationReceipt,
]:
    """Assign eligible foragers in complete 12-cell blocks within colony.

    individuals_per_cell equals the total number of complete treatment blocks
    across colonies. It must be a multiple of four so the four frozen cue-symbol
    counterbalance profiles occur equally often in every treatment cell.

    Individuals not needed for complete blocks remain unassigned and are
    returned explicitly. They must not be selected later according to treatment
    performance.
    """

    if type(individuals_per_cell) is not int or individuals_per_cell < 4:
        raise ValueError("individuals_per_cell must be an integer >= 4")
    if individuals_per_cell % len(ORTHOGONAL_SYMBOL_PROFILES) != 0:
        raise ValueError("individuals_per_cell must be a multiple of four")
    if type(seed) is not int or seed < 0:
        raise ValueError("seed must be a non-negative integer")

    by_colony: dict[str, list[str]] = {}
    seen_individuals: set[str] = set()
    for raw_individual, raw_colony in roster:
        individual = str(raw_individual).strip()
        colony = str(raw_colony).strip()
        if not individual or not colony:
            raise ValueError("individual_id and colony_id must be non-empty")
        if individual in seen_individuals:
            raise ValueError(f"duplicate individual_id: {individual!r}")
        seen_individuals.add(individual)
        by_colony.setdefault(colony, []).append(individual)

    if not by_colony:
        raise ValueError("roster is empty")

    block_size = len(TREATMENT_CELLS)
    capacity = {
        colony: len(individuals) // block_size
        for colony, individuals in by_colony.items()
    }
    if sum(capacity.values()) < individuals_per_cell:
        raise ValueError(
            "insufficient complete within-colony block capacity for requested "
            "individuals_per_cell"
        )

    rng = Random(seed)

    assigned_block_counts = {colony: 0 for colony in by_colony}
    block_colonies: list[str] = []
    for _ in range(individuals_per_cell):
        available = [
            colony
            for colony in sorted(by_colony)
            if assigned_block_counts[colony] < capacity[colony]
        ]
        if not available:
            raise AssertionError("complete-block allocation exhausted unexpectedly")
        minimum = min(assigned_block_counts[colony] for colony in available)
        candidates = [
            colony
            for colony in available
            if assigned_block_counts[colony] == minimum
        ]
        colony = rng.choice(candidates)
        assigned_block_counts[colony] += 1
        block_colonies.append(colony)

    shuffled_rosters = {}
    for colony, individuals in by_colony.items():
        values = list(individuals)
        rng.shuffle(values)
        shuffled_rosters[colony] = values

    colony_offsets = {colony: 0 for colony in by_colony}
    assignments: list[RouteabilityRosterAssignment] = []
    blocks_seen: dict[str, list[RouteabilityRosterAssignment]] = {}

    for global_block_index, colony in enumerate(block_colonies, start=1):
        start = colony_offsets[colony]
        stop = start + block_size
        block_individuals = shuffled_rosters[colony][start:stop]
        if len(block_individuals) != block_size:
            raise AssertionError("colony block did not contain 12 individuals")
        colony_offsets[colony] = stop

        cells = list(TREATMENT_CELLS)
        rng.shuffle(cells)
        rng.shuffle(block_individuals)
        profile_name, _ = ORTHOGONAL_SYMBOL_PROFILES[
            (global_block_index - 1) % len(ORTHOGONAL_SYMBOL_PROFILES)
        ]
        block_id = f"block_{global_block_index:04d}"

        block_rows = []
        for individual, (architecture, access_mode, budget) in zip(
            block_individuals,
            cells,
        ):
            row = RouteabilityRosterAssignment(
                individual_id=individual,
                colony_id=colony,
                complete_block_id=block_id,
                architecture=architecture,
                access_mode=access_mode,
                budget=budget,
                treatment_cell=_cell_name(
                    architecture, access_mode, budget
                ),
                counterbalance_profile=profile_name,
            )
            assignments.append(row)
            block_rows.append(row)
        blocks_seen[block_id] = block_rows

    assigned_ids = {row.individual_id for row in assignments}
    unassigned = tuple(
        sorted(
            (
                (individual, colony)
                for colony, individuals in by_colony.items()
                for individual in individuals
                if individual not in assigned_ids
            ),
            key=lambda item: (item[1], item[0]),
        )
    )

    cell_counts = {
        _cell_name(*cell): 0
        for cell in TREATMENT_CELLS
    }
    profile_counts = {
        cell: {
            profile_name: 0
            for profile_name, _ in ORTHOGONAL_SYMBOL_PROFILES
        }
        for cell in cell_counts
    }
    for row in assignments:
        cell_counts[row.treatment_cell] += 1
        profile_counts[row.treatment_cell][row.counterbalance_profile] += 1

    expected_cells = {
        _cell_name(*cell)
        for cell in TREATMENT_CELLS
    }
    complete_blocks_valid = all(
        len(rows) == block_size
        and {row.treatment_cell for row in rows} == expected_cells
        and len({row.colony_id for row in rows}) == 1
        for rows in blocks_seen.values()
    )
    counterbalance_profiles_valid = all(
        len(set(counts.values())) == 1
        for counts in profile_counts.values()
    )

    receipt = RouteabilityRosterRandomizationReceipt(
        individuals_per_cell=individuals_per_cell,
        treatment_cell_count=block_size,
        complete_block_count=len(blocks_seen),
        eligible_individual_count=len(seen_individuals),
        assigned_individual_count=len(assignments),
        unassigned_individual_count=len(unassigned),
        colony_count=len(by_colony),
        colony_block_capacity=tuple(sorted(capacity.items())),
        assigned_blocks_by_colony=tuple(
            sorted(assigned_block_counts.items())
        ),
        treatment_cell_counts=tuple(sorted(cell_counts.items())),
        profile_counts_by_cell=tuple(
            (
                cell,
                tuple(sorted(counts.items())),
            )
            for cell, counts in sorted(profile_counts.items())
        ),
        complete_blocks_valid=complete_blocks_valid,
        counterbalance_profiles_valid=counterbalance_profiles_valid,
    )

    if set(cell_counts.values()) != {individuals_per_cell}:
        raise AssertionError("treatment cells are not exactly balanced")
    if not receipt.complete_blocks_valid:
        raise AssertionError("within-colony complete block invariant failed")
    if not receipt.counterbalance_profiles_valid:
        raise AssertionError("counterbalance profile invariant failed")

    return tuple(assignments), unassigned, receipt
