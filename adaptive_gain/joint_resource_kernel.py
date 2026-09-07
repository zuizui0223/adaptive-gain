"""Joint-safe preprocessing that preserves both adaptive and fixed costs.

The adaptive-only kernels may use state-local reductions that intentionally do
not preserve fixed-bundle resource reuse.  This module instead applies only two
global reductions that are safe for BOTH C_A and C_F.

1. Same-target world twins.  Two worlds of the same target are twins when every
   remaining query has the same separation/nonseparation relation from each of
   them to every remaining opposite-target world.  One representative suffices:
   the fixed pair obligations are duplicates and the adaptive mixed continuation
   cannot distinguish the twins in a target-relevant way.

2. Global query refinement dominance.  Query q dominates r when c(q)<=c(r) and
   q separates every remaining cross-target world pair that r separates.  Any
   fixed bundle using r can replace it by q.  On every adaptive branch the same
   inclusion remains true after restriction to the branch world set, so r is
   never needed after q and can be removed globally.

The two reductions are iterated because removing worlds can create query
refinement, while removing queries can create new world twins.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class JointResourceKernelReceipt:
    reduced_task: FiniteTask
    kept_world_names: tuple[str, ...]
    removed_world_names: tuple[str, ...]
    kept_query_names: tuple[str, ...]
    removed_query_names: tuple[str, ...]
    iterations: int
    original_adaptive_cost: int | None
    reduced_adaptive_cost: int | None
    original_fixed_cost: int | None
    reduced_fixed_cost: int | None
    adaptive_cost_agrees: bool
    fixed_cost_agrees: bool
    exact_costs_agree: bool
    scope: str = "global_same_target_world_twins_and_query_refinement_preserving_CA_CF"


def _cross_target_pairs(task: FiniteTask) -> tuple[tuple[int, int], ...]:
    return tuple(
        (i, j)
        for i, j in combinations(range(len(task.worlds)), 2)
        if task.worlds[i].target != task.worlds[j].target
    )


def _query_mask(task: FiniteTask, query_index: int) -> int:
    mask = 0
    query = task.queries[query_index]
    for bit, (i, j) in enumerate(_cross_target_pairs(task)):
        if query.outcomes[i] != query.outcomes[j]:
            mask |= 1 << bit
    return mask


def _world_twin_classes(task: FiniteTask) -> tuple[tuple[int, ...], ...]:
    """Return maximal same-target classes with identical cross-target relations."""
    signatures: dict[tuple[object, tuple[tuple[bool, ...], ...]], list[int]] = {}
    for i, world in enumerate(task.worlds):
        opposite = tuple(
            j for j, other in enumerate(task.worlds)
            if other.target != world.target
        )
        per_query = tuple(
            tuple(query.outcomes[i] != query.outcomes[j] for j in opposite)
            for query in task.queries
        )
        signatures.setdefault((world.target, per_query), []).append(i)
    return tuple(tuple(indices) for _, indices in sorted(signatures.items(), key=lambda item: min(item[1])))


def _collapse_world_twins(task: FiniteTask) -> tuple[FiniteTask, tuple[str, ...]]:
    classes = _world_twin_classes(task)
    keep = tuple(group[0] for group in classes)
    removed = tuple(
        task.worlds[i].name
        for group in classes for i in group[1:]
    )
    if not removed:
        return task, ()
    worlds = tuple(task.worlds[i] for i in keep)
    queries = tuple(
        Query(query.name, query.cost, tuple(query.outcomes[i] for i in keep))
        for query in task.queries
    )
    return FiniteTask(worlds, queries), removed


def _dominates_query(task: FiniteTask, left: int, right: int) -> bool:
    if left == right:
        return False
    q, r = task.queries[left], task.queries[right]
    if q.cost > r.cost:
        return False
    left_mask = _query_mask(task, left)
    right_mask = _query_mask(task, right)
    if (left_mask | right_mask) != left_mask:
        return False
    # Equal-cost/equal-effect queries are interchangeable.  Keep the lower index
    # so dominance is deterministic and acyclic.
    if q.cost == r.cost and left_mask == right_mask and left > right:
        return False
    return True


def _remove_dominated_queries(task: FiniteTask) -> tuple[FiniteTask, tuple[str, ...]]:
    dominated = tuple(
        r for r in range(len(task.queries))
        if any(_dominates_query(task, q, r) for q in range(len(task.queries)))
    )
    if not dominated:
        return task, ()
    drop = set(dominated)
    removed = tuple(task.queries[q].name for q in dominated)
    queries = tuple(query for q, query in enumerate(task.queries) if q not in drop)
    return FiniteTask(task.worlds, queries), removed


def joint_resource_kernel(task: FiniteTask, *, max_iterations: int = 100) -> JointResourceKernelReceipt:
    """Iterate the joint-safe world/query reductions to a fixed point."""
    if not isinstance(task, FiniteTask):
        raise ValueError("task must be a FiniteTask")
    if type(max_iterations) is not int or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")

    current = task
    removed_worlds: list[str] = []
    removed_queries: list[str] = []
    iterations = 0
    while True:
        iterations += 1
        if iterations > max_iterations:
            raise RuntimeError("joint resource kernel did not reach a fixed point within max_iterations")
        changed = False

        current, world_rows = _collapse_world_twins(current)
        if world_rows:
            removed_worlds.extend(world_rows)
            changed = True

        current, query_rows = _remove_dominated_queries(current)
        if query_rows:
            removed_queries.extend(query_rows)
            changed = True

        if not changed:
            break

    original_adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    reduced_adaptive = adaptive_minimum_resolution(current).minimum_worst_path_cost
    original_fixed = fixed_minimum_resolution(task).minimum_cost
    reduced_fixed = fixed_minimum_resolution(current).minimum_cost
    if original_adaptive != reduced_adaptive or original_fixed != reduced_fixed:
        raise ArithmeticError("joint resource kernel changed an exact resolution cost")

    return JointResourceKernelReceipt(
        current,
        tuple(world.name for world in current.worlds),
        tuple(removed_worlds),
        tuple(query.name for query in current.queries),
        tuple(removed_queries),
        iterations,
        original_adaptive,
        reduced_adaptive,
        original_fixed,
        reduced_fixed,
        True,
        True,
        True,
    )
