"""Adaptive-safe state-local compression of deterministic query vocabularies.

Full identity-indexed cross-target pair incidence is sufficient for exact
worst-path target resolution, but it need not be used verbatim at every Bellman
state.  For a current world set A, only the target-mixed outcome cells of a query
can have nonzero continuation value.

If two remaining queries induce exactly the same family of target-mixed cells on
A, then each query is constant on every target-mixed child of the other.  Pure
children terminate immediately.  Consequently the queries are interchangeable
for future target resolution except for acquisition cost; one cheapest
representative is sufficient and the entire equivalence class can be removed
from every recursive mixed child after that representative is selected.

This is an adaptive-safe compression.  It is different from fixed pair-obligation
dominance, which can discard information needed to reconstruct target-mixed
children.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .core import FiniteTask, adaptive_minimum_resolution
from .target_pair_incidence import (
    TargetPairIncidenceTask,
    _mixed_outcome_components,
    target_pair_incidence_task,
)


@dataclass(frozen=True)
class TargetRelevantQueryClass:
    mixed_child_masks: tuple[int, ...]
    member_query_indices: tuple[int, ...]
    member_query_names: tuple[str, ...]
    minimum_cost: int
    representative_query_index: int
    representative_query_name: str
    dominated_query_names: tuple[str, ...]
    scope: str = "state_local_equal_target_mixed_continuation_family"


@dataclass(frozen=True)
class AdaptiveSafeCompressionReceipt:
    minimum_worst_path_cost: int | None
    selected_optimal_first_queries: tuple[str, ...]
    search_states: int
    raw_query_candidates_seen: int
    representative_queries_evaluated: int
    dominated_query_occurrences_pruned: int
    no_progress_query_occurrences_skipped: int
    exact_direct_cost: int | None
    cost_agrees_with_direct_solver: bool
    scope: str = "exact_adaptive_bellman_with_target_relevant_query_class_compression"


def _validate_world_mask(task: TargetPairIncidenceTask, world_mask: int) -> None:
    if type(world_mask) is not int or world_mask < 0 or world_mask >= (1 << len(task.targets)):
        raise ValueError("world_mask must be a nonnegative mask over represented worlds")


def target_relevant_query_classes(
    task: TargetPairIncidenceTask,
    *,
    world_mask: int,
    remaining_query_mask: int | None = None,
) -> tuple[TargetRelevantQueryClass, ...]:
    """Group queries by exact target-mixed continuation family at one state.

    Within each family, a minimum-cost query dominates every more expensive
    member.  Equal-cost members are interchangeable for worst-path target
    resolution; the lowest declared query index is used as a deterministic
    representative.
    """
    _validate_world_mask(task, world_mask)
    qn = len(task.query_names)
    if remaining_query_mask is None:
        remaining_query_mask = (1 << qn) - 1
    if (
        type(remaining_query_mask) is not int
        or remaining_query_mask < 0
        or remaining_query_mask >= (1 << qn)
    ):
        raise ValueError("remaining_query_mask must be a mask over declared queries")

    families: dict[tuple[int, ...], list[int]] = {}
    for q in range(qn):
        if not (remaining_query_mask & (1 << q)):
            continue
        mixed = _mixed_outcome_components(task, world_mask, q)
        families.setdefault(mixed, []).append(q)

    rows = []
    for mixed, members_list in families.items():
        members = tuple(sorted(members_list))
        minimum_cost = min(task.query_costs[q] for q in members)
        cheapest = tuple(q for q in members if task.query_costs[q] == minimum_cost)
        representative = min(cheapest)
        dominated = tuple(
            task.query_names[q]
            for q in members
            if q != representative
        )
        rows.append(
            TargetRelevantQueryClass(
                mixed,
                members,
                tuple(task.query_names[q] for q in members),
                minimum_cost,
                representative,
                task.query_names[representative],
                dominated,
            )
        )
    return tuple(sorted(rows, key=lambda row: (row.mixed_child_masks, row.minimum_cost, row.representative_query_index)))


def adaptive_safe_compressed_minimum_resolution(
    task: FiniteTask,
) -> AdaptiveSafeCompressionReceipt:
    """Solve exact target resolution while pruning target-relevant query classes."""
    incidence = target_pair_incidence_task(task)
    n, qn = len(incidence.targets), len(incidence.query_names)
    root_worlds = (1 << n) - 1
    root_queries = (1 << qn) - 1
    states = raw_seen = representatives = dominated = no_progress = 0

    def target_values(world_mask: int):
        return {
            incidence.targets[i]
            for i in range(n)
            if world_mask & (1 << i)
        }

    @lru_cache(None)
    def search(world_mask: int, remaining_queries: int):
        nonlocal states, raw_seen, representatives, dominated, no_progress
        states += 1
        if len(target_values(world_mask)) <= 1:
            return 0, ()

        classes = target_relevant_query_classes(
            incidence,
            world_mask=world_mask,
            remaining_query_mask=remaining_queries,
        )
        raw_seen += sum(len(row.member_query_indices) for row in classes)
        best: int | None = None
        roots: list[str] = []

        for row in classes:
            # One mixed child equal to the full state means the whole state has
            # one target-mixed outcome cell and there are no target-relevant pure
            # exits.  The query makes no target-resolution progress.
            if row.mixed_child_masks == (world_mask,):
                no_progress += len(row.member_query_indices)
                continue

            representatives += 1
            dominated += len(row.member_query_indices) - 1
            q = row.representative_query_index
            group_mask = 0
            for member in row.member_query_indices:
                group_mask |= 1 << member
            next_queries = remaining_queries & ~group_mask

            child_costs = []
            feasible = True
            for child in row.mixed_child_masks:
                child_cost, _ = search(child, next_queries)
                if child_cost is None:
                    feasible = False
                    break
                child_costs.append(child_cost)
            if not feasible:
                continue

            cost = incidence.query_costs[q] + (max(child_costs) if child_costs else 0)
            if best is None or cost < best:
                best = cost
                roots = [incidence.query_names[q]]
            elif cost == best:
                roots.append(incidence.query_names[q])
        return best, tuple(roots)

    cost, roots = search(root_worlds, root_queries)
    direct = adaptive_minimum_resolution(task).minimum_worst_path_cost
    if cost != direct:
        raise ArithmeticError("adaptive-safe query compression changed the exact adaptive cost")
    return AdaptiveSafeCompressionReceipt(
        cost,
        roots,
        states,
        raw_seen,
        representatives,
        dominated,
        no_progress,
        direct,
        True,
    )
