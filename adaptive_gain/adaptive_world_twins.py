"""Adaptive-safe state-local quotient of target-relevant world twins.

Two worlds of the same target are target-relevant twins at a Bellman state when,
for every remaining query and every currently represented world of a different
target, their cross-target separation bits are identical.

For any remaining query, a target-mixed outcome cell either contains the entire
twin class or none of it.  If two twins are split into different outcome cells,
both cells are target-pure and terminate immediately.  Therefore one representative
per twin class is sufficient for deterministic worst-path target resolution.

The equivalence can become coarser as queries are consumed, so the compressed
solver recomputes the quotient at every Bellman state.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .core import FiniteTask, adaptive_minimum_resolution, fixed_minimum_resolution
from .target_pair_incidence import (
    TargetPairIncidenceTask,
    _mixed_outcome_components,
    target_pair_incidence_task,
)


@dataclass(frozen=True)
class TargetRelevantWorldTwinClass:
    target: object
    member_world_indices: tuple[int, ...]
    member_world_names: tuple[str, ...]
    representative_world_index: int
    representative_world_name: str
    scope: str = "state_local_same_target_cross_target_incidence_twins"


@dataclass(frozen=True)
class StaticWorldTwinQuotientReceipt:
    original_world_count: int
    quotient_world_count: int
    collapsed_world_count: int
    twin_classes: tuple[TargetRelevantWorldTwinClass, ...]
    original_adaptive_cost: int | None
    quotient_adaptive_cost: int | None
    original_fixed_cost: int | None
    quotient_fixed_cost: int | None
    adaptive_cost_preserved: bool
    fixed_cost_preserved: bool
    scope: str = "root_target_relevant_world_twin_quotient"


@dataclass(frozen=True)
class DynamicWorldTwinCompressionReceipt:
    minimum_worst_path_cost: int | None
    selected_optimal_first_queries: tuple[str, ...]
    canonical_search_states: int
    canonicalization_calls: int
    world_occurrences_collapsed: int
    maximum_single_state_collapse: int
    exact_direct_cost: int | None
    cost_agrees_with_direct_solver: bool
    scope: str = "exact_adaptive_bellman_with_dynamic_target_relevant_world_twin_quotient"


def _validate_masks(
    task: TargetPairIncidenceTask,
    world_mask: int,
    remaining_query_mask: int | None,
) -> int:
    n, qn = len(task.targets), len(task.query_names)
    if type(world_mask) is not int or world_mask < 0 or world_mask >= (1 << n):
        raise ValueError("world_mask must be a mask over represented worlds")
    if remaining_query_mask is None:
        return (1 << qn) - 1
    if (
        type(remaining_query_mask) is not int
        or remaining_query_mask < 0
        or remaining_query_mask >= (1 << qn)
    ):
        raise ValueError("remaining_query_mask must be a mask over declared queries")
    return remaining_query_mask


def _pair_lookup(task: TargetPairIncidenceTask) -> dict[tuple[int, int], int]:
    lookup = {}
    for bit, (i, j) in enumerate(task.cross_target_pairs):
        lookup[(i, j)] = bit
        lookup[(j, i)] = bit
    return lookup


def target_relevant_world_twin_classes(
    task: TargetPairIncidenceTask,
    *,
    world_mask: int,
    remaining_query_mask: int | None = None,
) -> tuple[TargetRelevantWorldTwinClass, ...]:
    """Return same-target world classes indistinguishable to all future mixed cells."""
    remaining_query_mask = _validate_masks(task, world_mask, remaining_query_mask)
    pair_lookup = _pair_lookup(task)
    active_worlds = tuple(
        i for i in range(len(task.targets)) if world_mask & (1 << i)
    )
    active_queries = tuple(
        q for q in range(len(task.query_names))
        if remaining_query_mask & (1 << q)
    )

    by_target: dict[object, list[int]] = {}
    for i in active_worlds:
        by_target.setdefault(task.targets[i], []).append(i)

    classes = []
    for target, members in by_target.items():
        opposite = tuple(i for i in active_worlds if task.targets[i] != target)
        signatures: dict[tuple[int, ...], list[int]] = {}
        for i in members:
            signature = []
            for q in active_queries:
                qmask = task.query_separation_masks[q]
                for j in opposite:
                    bit = pair_lookup[(i, j)]
                    signature.append(1 if qmask & (1 << bit) else 0)
            signatures.setdefault(tuple(signature), []).append(i)
        for grouped in signatures.values():
            row = tuple(sorted(grouped))
            representative = min(row)
            classes.append(
                TargetRelevantWorldTwinClass(
                    target,
                    row,
                    tuple(task.world_names[i] for i in row),
                    representative,
                    task.world_names[representative],
                )
            )
    return tuple(
        sorted(classes, key=lambda row: row.representative_world_index)
    )


def target_relevant_world_twin_representative_mask(
    task: TargetPairIncidenceTask,
    *,
    world_mask: int,
    remaining_query_mask: int | None = None,
) -> int:
    classes = target_relevant_world_twin_classes(
        task,
        world_mask=world_mask,
        remaining_query_mask=remaining_query_mask,
    )
    mask = 0
    for row in classes:
        mask |= 1 << row.representative_world_index
    return mask


def static_target_relevant_world_twin_quotient(
    task: FiniteTask,
) -> tuple[FiniteTask, StaticWorldTwinQuotientReceipt]:
    """Collapse root twin classes and independently audit both C_A and C_F."""
    incidence = target_pair_incidence_task(task)
    root_mask = (1 << len(task.worlds)) - 1
    query_mask = (1 << len(task.queries)) - 1
    classes = target_relevant_world_twin_classes(
        incidence,
        world_mask=root_mask,
        remaining_query_mask=query_mask,
    )
    representatives = tuple(row.representative_world_index for row in classes)
    quotient = FiniteTask(
        tuple(task.worlds[i] for i in representatives),
        tuple(
            type(query)(
                query.name,
                query.cost,
                tuple(query.outcomes[i] for i in representatives),
            )
            for query in task.queries
        ),
    )
    original_adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    quotient_adaptive = adaptive_minimum_resolution(quotient).minimum_worst_path_cost
    original_fixed = fixed_minimum_resolution(task).minimum_cost
    quotient_fixed = fixed_minimum_resolution(quotient).minimum_cost
    if original_adaptive != quotient_adaptive or original_fixed != quotient_fixed:
        raise ArithmeticError("target-relevant world twin quotient changed exact costs")
    receipt = StaticWorldTwinQuotientReceipt(
        len(task.worlds),
        len(quotient.worlds),
        len(task.worlds) - len(quotient.worlds),
        classes,
        original_adaptive,
        quotient_adaptive,
        original_fixed,
        quotient_fixed,
        True,
        True,
    )
    return quotient, receipt


def adaptive_world_twin_compressed_minimum_resolution(
    task: FiniteTask,
) -> DynamicWorldTwinCompressionReceipt:
    """Solve exact C_A while re-quotienting same-target world twins at every state."""
    incidence = target_pair_incidence_task(task)
    n, qn = len(task.worlds), len(task.queries)
    root_worlds = (1 << n) - 1
    root_queries = (1 << qn) - 1
    canonicalization_calls = collapsed = maximum_collapse = 0
    states = 0

    def target_values(world_mask: int):
        return {
            incidence.targets[i]
            for i in range(n)
            if world_mask & (1 << i)
        }

    def canonicalize(world_mask: int, remaining_queries: int) -> int:
        nonlocal canonicalization_calls, collapsed, maximum_collapse
        canonicalization_calls += 1
        representative = target_relevant_world_twin_representative_mask(
            incidence,
            world_mask=world_mask,
            remaining_query_mask=remaining_queries,
        )
        reduction = world_mask.bit_count() - representative.bit_count()
        collapsed += reduction
        maximum_collapse = max(maximum_collapse, reduction)
        return representative

    @lru_cache(None)
    def search(canonical_worlds: int, remaining_queries: int):
        nonlocal states
        states += 1
        if len(target_values(canonical_worlds)) <= 1:
            return 0, ()
        best: int | None = None
        roots: list[str] = []
        for q in range(qn):
            bit = 1 << q
            if not (remaining_queries & bit):
                continue
            mixed = _mixed_outcome_components(incidence, canonical_worlds, q)
            if mixed == (canonical_worlds,):
                continue
            next_queries = remaining_queries ^ bit
            child_costs = []
            feasible = True
            for child in mixed:
                child = canonicalize(child, next_queries)
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

    root = canonicalize(root_worlds, root_queries)
    cost, roots = search(root, root_queries)
    direct = adaptive_minimum_resolution(task).minimum_worst_path_cost
    if cost != direct:
        raise ArithmeticError("dynamic target-relevant world twin quotient changed C_A")
    return DynamicWorldTwinCompressionReceipt(
        cost,
        roots,
        states,
        canonicalization_calls,
        collapsed,
        maximum_collapse,
        direct,
        True,
    )
