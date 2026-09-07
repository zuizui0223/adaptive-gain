"""Adaptive-safe state-local compression of deterministic query vocabularies.

Full identity-indexed cross-target pair incidence is sufficient for exact
worst-path target resolution, but it need not be used verbatim at every Bellman
state.

Two exact adaptive-safe reductions are implemented here.

1. Continuation equality.  At a current world set A, only target-mixed outcome
   cells can have nonzero continuation value.  Queries with exactly the same
   family of target-mixed cells are interchangeable except for acquisition cost.

2. Refinement dominance.  Restrict each query's cross-target separation mask to
   pairs whose endpoints are both in A.  If q separates every cross-target pair
   separated by r and c(q) <= c(r), then q is target-relevantly at least as
   informative as r.  Every target-mixed q-child lies inside one r-outcome cell,
   so r is constant after q on every unresolved child.  Query r therefore need
   not be considered as a root at A, and it can be removed after q is selected.

These are adaptive-safe compressions.  They are different from fixed
pair-obligation dominance, which can discard information needed to reconstruct
target-mixed children.
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


@dataclass(frozen=True)
class TargetRelevantRefinementDominance:
    dominating_query_index: int
    dominating_query_name: str
    dominating_cost: int
    restricted_separation_mask: int
    dominated_query_indices: tuple[int, ...]
    dominated_query_names: tuple[str, ...]
    scope: str = "state_local_cross_target_separation_refinement_dominance"


@dataclass(frozen=True)
class AdaptiveRefinementCompressionReceipt:
    minimum_worst_path_cost: int | None
    selected_optimal_first_queries: tuple[str, ...]
    search_states: int
    raw_query_candidates_seen: int
    nondominated_queries_evaluated: int
    refinement_dominated_query_occurrences_pruned: int
    no_progress_query_occurrences_skipped: int
    exact_direct_cost: int | None
    cost_agrees_with_direct_solver: bool
    scope: str = "exact_adaptive_bellman_with_cross_target_refinement_dominance"


def _validate_world_mask(task: TargetPairIncidenceTask, world_mask: int) -> None:
    if type(world_mask) is not int or world_mask < 0 or world_mask >= (1 << len(task.targets)):
        raise ValueError("world_mask must be a nonnegative mask over represented worlds")


def _validate_remaining_query_mask(
    task: TargetPairIncidenceTask,
    remaining_query_mask: int | None,
) -> int:
    qn = len(task.query_names)
    if remaining_query_mask is None:
        return (1 << qn) - 1
    if (
        type(remaining_query_mask) is not int
        or remaining_query_mask < 0
        or remaining_query_mask >= (1 << qn)
    ):
        raise ValueError("remaining_query_mask must be a mask over declared queries")
    return remaining_query_mask


def _restricted_separation_mask(
    task: TargetPairIncidenceTask,
    world_mask: int,
    query_index: int,
) -> int:
    active = 0
    for bit, (i, j) in enumerate(task.cross_target_pairs):
        if world_mask & (1 << i) and world_mask & (1 << j):
            active |= 1 << bit
    return task.query_separation_masks[query_index] & active


def target_relevant_query_classes(
    task: TargetPairIncidenceTask,
    *,
    world_mask: int,
    remaining_query_mask: int | None = None,
) -> tuple[TargetRelevantQueryClass, ...]:
    """Group queries by exact target-mixed continuation family at one state.

    Within each family, a minimum-cost query dominates every more expensive
    member.  Equal-cost members are interchangeable for worst-path target
    resolution; the lowest declared query index is a deterministic
    representative.
    """
    _validate_world_mask(task, world_mask)
    remaining_query_mask = _validate_remaining_query_mask(task, remaining_query_mask)

    families: dict[tuple[int, ...], list[int]] = {}
    for q in range(len(task.query_names)):
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
        pruned = tuple(task.query_names[q] for q in members if q != representative)
        rows.append(
            TargetRelevantQueryClass(
                mixed,
                members,
                tuple(task.query_names[q] for q in members),
                minimum_cost,
                representative,
                task.query_names[representative],
                pruned,
            )
        )
    return tuple(
        sorted(
            rows,
            key=lambda row: (
                row.mixed_child_masks,
                row.minimum_cost,
                row.representative_query_index,
            ),
        )
    )


def _dominates(
    task: TargetPairIncidenceTask,
    world_mask: int,
    left: int,
    right: int,
) -> bool:
    """Return whether left safely dominates right at this Bellman state."""
    if left == right or task.query_costs[left] > task.query_costs[right]:
        return False
    left_mask = _restricted_separation_mask(task, world_mask, left)
    right_mask = _restricted_separation_mask(task, world_mask, right)
    if (left_mask | right_mask) != left_mask:
        return False
    # Equal cost and equal target-relevant separation are symmetric.  Keep the
    # lowest index only so the dominance relation is acyclic and deterministic.
    if (
        task.query_costs[left] == task.query_costs[right]
        and left_mask == right_mask
        and left > right
    ):
        return False
    return True


def target_relevant_refinement_dominance(
    task: TargetPairIncidenceTask,
    *,
    world_mask: int,
    remaining_query_mask: int | None = None,
) -> tuple[TargetRelevantRefinementDominance, ...]:
    """Return the nondominated query frontier and what each member safely removes.

    A query q dominates r when q costs no more and its active cross-target
    separation mask is a superset of r's.  Strictly finer equal-cost queries
    dominate coarser ones.  Equal-cost equal-mask queries are tie-broken by index.
    """
    _validate_world_mask(task, world_mask)
    remaining_query_mask = _validate_remaining_query_mask(task, remaining_query_mask)
    available = tuple(
        q for q in range(len(task.query_names))
        if remaining_query_mask & (1 << q)
    )
    frontier = tuple(
        q for q in available
        if not any(_dominates(task, world_mask, other, q) for other in available)
    )
    rows = []
    for q in frontier:
        dominated = tuple(
            r for r in available
            if _dominates(task, world_mask, q, r)
        )
        rows.append(
            TargetRelevantRefinementDominance(
                q,
                task.query_names[q],
                task.query_costs[q],
                _restricted_separation_mask(task, world_mask, q),
                dominated,
                tuple(task.query_names[r] for r in dominated),
            )
        )
    return tuple(sorted(rows, key=lambda row: row.dominating_query_index))


def adaptive_safe_compressed_minimum_resolution(
    task: FiniteTask,
) -> AdaptiveSafeCompressionReceipt:
    """Solve exact target resolution using equality of mixed-child families."""
    incidence = target_pair_incidence_task(task)
    n, qn = len(incidence.targets), len(incidence.query_names)
    root_worlds = (1 << n) - 1
    root_queries = (1 << qn) - 1
    states = raw_seen = representatives = pruned = no_progress = 0

    def target_values(world_mask: int):
        return {
            incidence.targets[i]
            for i in range(n)
            if world_mask & (1 << i)
        }

    @lru_cache(None)
    def search(world_mask: int, remaining_queries: int):
        nonlocal states, raw_seen, representatives, pruned, no_progress
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
            if row.mixed_child_masks == (world_mask,):
                no_progress += len(row.member_query_indices)
                continue

            representatives += 1
            pruned += len(row.member_query_indices) - 1
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
        pruned,
        no_progress,
        direct,
        True,
    )


def adaptive_refinement_compressed_minimum_resolution(
    task: FiniteTask,
) -> AdaptiveRefinementCompressionReceipt:
    """Solve exact target resolution using cross-target refinement dominance."""
    incidence = target_pair_incidence_task(task)
    n, qn = len(incidence.targets), len(incidence.query_names)
    root_worlds = (1 << n) - 1
    root_queries = (1 << qn) - 1
    states = raw_seen = evaluated = pruned = no_progress = 0

    def target_values(world_mask: int):
        return {
            incidence.targets[i]
            for i in range(n)
            if world_mask & (1 << i)
        }

    @lru_cache(None)
    def search(world_mask: int, remaining_queries: int):
        nonlocal states, raw_seen, evaluated, pruned, no_progress
        states += 1
        if len(target_values(world_mask)) <= 1:
            return 0, ()

        available = tuple(
            q for q in range(qn)
            if remaining_queries & (1 << q)
        )
        raw_seen += len(available)
        frontier = target_relevant_refinement_dominance(
            incidence,
            world_mask=world_mask,
            remaining_query_mask=remaining_queries,
        )
        frontier_indices = {row.dominating_query_index for row in frontier}
        pruned += len(available) - len(frontier_indices)
        best: int | None = None
        roots: list[str] = []

        for row in frontier:
            q = row.dominating_query_index
            mixed = _mixed_outcome_components(incidence, world_mask, q)
            if mixed == (world_mask,):
                no_progress += 1
                continue

            evaluated += 1
            remove_mask = 1 << q
            for dominated_query in row.dominated_query_indices:
                remove_mask |= 1 << dominated_query
            next_queries = remaining_queries & ~remove_mask

            child_costs = []
            feasible = True
            for child in mixed:
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
        raise ArithmeticError("adaptive refinement dominance changed the exact adaptive cost")
    return AdaptiveRefinementCompressionReceipt(
        cost,
        roots,
        states,
        raw_seen,
        evaluated,
        pruned,
        no_progress,
        direct,
        True,
    )
