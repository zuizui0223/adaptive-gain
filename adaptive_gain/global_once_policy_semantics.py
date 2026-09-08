"""Exact audit of a globally label-unique adaptive-tree syntax.

The repository's ordinary adaptive tree already uses a query at most once along
any realized history.  The same physical query name may nevertheless appear in
several mutually exclusive counterfactual branches.  That is not repeated
acquisition on one run.

This module studies a *different* syntactic restriction: every physical query
name may label at most one node in the entire policy tree.  We call this
``global-label-once``.  It is intentionally not treated as the default resource
semantics because it can exclude a fixed bundle from the adaptive policy class.

Two exact facts are registered:

1. Pointwise class containment can fail: a task can have C_A=C_F=2 under the
   ordinary semantics while no global-label-once resolving tree exists.
2. As an extremal problem over tasks that *are* global-label-once resolvable,
   the sharp unit-cost fixed/adaptive ratio at fixed (n,m,b) is unchanged.  The
   bounded-arity sharp witness already assigns one distinct physical query to
   every internal tree node.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from fractions import Fraction

from .bounded_arity_extremal_bounds import (
    sharp_bounded_arity_unit_cost_ratio,
    sharp_bounded_arity_unit_cost_witness,
)
from .core import (
    AdaptiveNode,
    FiniteTask,
    Query,
    World,
    adaptive_minimum_resolution,
    fixed_minimum_resolution,
)


class GlobalOnceSearchLimitError(RuntimeError):
    """The exact global-label-once option search exceeded a declared cap."""


@dataclass(frozen=True)
class GlobalOnceAdaptiveReceipt:
    minimum_worst_path_cost: int | None
    selected_policy: AdaptiveNode | None
    globally_used_queries: tuple[str, ...]
    target_already_identified: bool
    searched_world_states: int
    generated_options: int
    scope: str = "finite_deterministic_global_query_label_unique_policy_tree"


@dataclass(frozen=True)
class GlobalOnceContainmentCounterexampleReceipt:
    standard_adaptive_cost: int | None
    fixed_cost: int | None
    global_once_adaptive_cost: int | None
    fixed_bundle_exists: bool
    global_once_tree_exists: bool
    ordinary_containment_holds: bool
    global_once_containment_fails: bool
    scope: str = "global_label_once_is_syntactic_not_operational_resource_constraint"


@dataclass(frozen=True)
class GlobalOnceExtremalReceipt:
    world_count: int
    query_count: int
    max_arity: int
    sharp_ratio: Fraction
    witness_global_once_cost: int | None
    witness_fixed_cost: int | None
    witness_ratio: Fraction | None
    witness_uses_each_query_once_globally: bool
    theorem_holds: bool
    scope: str = "sharp_unit_cost_ratio_among_global_label_once_resolvable_tasks"


def _indices(mask: int, n: int) -> tuple[int, ...]:
    return tuple(i for i in range(n) if mask & (1 << i))


def _pure(task: FiniteTask, mask: int) -> bool:
    return len({task.worlds[i].target for i in _indices(mask, len(task.worlds))}) <= 1


def _partition(task: FiniteTask, mask: int, query_index: int) -> tuple[tuple[object, int], ...]:
    groups: dict[object, int] = {}
    query = task.queries[query_index]
    for i in _indices(mask, len(task.worlds)):
        outcome = query.outcomes[i]
        groups[outcome] = groups.get(outcome, 0) | (1 << i)
    return tuple(sorted(groups.items(), key=lambda item: repr(item[0])))


def global_label_once_adaptive_minimum_resolution(
    task: FiniteTask,
    *,
    max_queries: int = 10,
    max_generated_options: int = 200_000,
) -> GlobalOnceAdaptiveReceipt:
    """Exact minimum worst-path cost with each query label used once in the whole tree.

    A subtree option records the complete set of query identities used anywhere
    in that subtree.  Options selected for distinct unresolved child branches
    must have disjoint query sets.  This is the counterfactual coupling absent
    from the ordinary Bellman recursion.
    """
    if not isinstance(task, FiniteTask):
        raise ValueError("task must be a FiniteTask")
    if type(max_queries) is not int or max_queries < 0:
        raise ValueError("max_queries must be a nonnegative integer")
    if type(max_generated_options) is not int or max_generated_options < 1:
        raise ValueError("max_generated_options must be a positive integer")
    qn = len(task.queries)
    if qn > max_queries:
        raise GlobalOnceSearchLimitError(
            f"global-label-once exact solver capped at {max_queries} queries"
        )

    generated = 0
    states = 0
    n = len(task.worlds)

    # map used_query_mask -> (minimum worst-path cost, representative policy)
    @lru_cache(None)
    def options(mask: int) -> tuple[tuple[int, int, AdaptiveNode], ...]:
        nonlocal generated, states
        states += 1
        support = tuple(task.worlds[i].name for i in _indices(mask, n))
        targets = {task.worlds[i].target for i in _indices(mask, n)}
        if len(targets) <= 1:
            target = next(iter(targets)) if targets else None
            return ((0, 0, AdaptiveNode(None, (), support, target)),)

        best: dict[int, tuple[int, AdaptiveNode]] = {}
        for q_index, query in enumerate(task.queries):
            qbit = 1 << q_index
            groups = _partition(task, mask, q_index)
            if len(groups) <= 1:
                continue

            # (union mask) -> (max child path cost, branch nodes)
            combined: dict[int, tuple[int, tuple[tuple[object, AdaptiveNode], ...]]] = {
                0: (0, ())
            }
            feasible = True
            for outcome, child_mask in groups:
                child_options = options(child_mask)
                usable = [row for row in child_options if not (row[0] & qbit)]
                if not usable:
                    feasible = False
                    break
                nxt: dict[int, tuple[int, tuple[tuple[object, AdaptiveNode], ...]]] = {}
                for used_so_far, (worst_so_far, branches_so_far) in combined.items():
                    for child_used, child_cost, child_node in usable:
                        if used_so_far & child_used:
                            continue
                        union = used_so_far | child_used
                        worst = max(worst_so_far, child_cost)
                        branches = branches_so_far + ((outcome, child_node),)
                        old = nxt.get(union)
                        if old is None or worst < old[0]:
                            nxt[union] = (worst, branches)
                combined = nxt
                if not combined:
                    feasible = False
                    break
                generated += len(combined)
                if generated > max_generated_options:
                    raise GlobalOnceSearchLimitError(
                        "global-label-once option cap exceeded"
                    )
            if not feasible:
                continue

            for child_union, (child_worst, branches) in combined.items():
                if child_union & qbit:
                    continue
                used = child_union | qbit
                cost = query.cost + child_worst
                node = AdaptiveNode(query.name, branches, support, None)
                old = best.get(used)
                if old is None or cost < old[0]:
                    best[used] = (cost, node)
        rows = tuple((used, cost, node) for used, (cost, node) in sorted(best.items()))
        generated += len(rows)
        if generated > max_generated_options:
            raise GlobalOnceSearchLimitError("global-label-once option cap exceeded")
        return rows

    root_mask = (1 << n) - 1
    root_options = options(root_mask)
    if not root_options:
        return GlobalOnceAdaptiveReceipt(
            None,
            None,
            (),
            len({world.target for world in task.worlds}) <= 1,
            states,
            generated,
        )
    used, cost, node = min(root_options, key=lambda row: (row[1], row[0]))
    names = tuple(task.queries[i].name for i in range(qn) if used & (1 << i))
    return GlobalOnceAdaptiveReceipt(
        cost,
        node,
        names,
        len({world.target for world in task.worlds}) <= 1,
        states,
        generated,
    )


def global_once_containment_counterexample_task() -> FiniteTask:
    """Two-query task where ordinary/fixed cost is 2 but global-label-once is infeasible."""
    worlds = (
        World("a0", 0),
        World("b0", 1),
        World("a1", 0),
        World("b1", 1),
    )
    # route leaves two target-mixed branch pairs.
    route = Query("route", 1, (0, 0, 1, 1))
    # assay resolves either branch locally, but with reversed target coding, so
    # it is not a direct global target resolver.
    assay = Query("assay", 1, (0, 1, 1, 0))
    return FiniteTask(worlds, (route, assay))


def global_once_containment_counterexample_audit() -> GlobalOnceContainmentCounterexampleReceipt:
    task = global_once_containment_counterexample_task()
    ordinary = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    global_once = global_label_once_adaptive_minimum_resolution(task).minimum_worst_path_cost
    receipt = GlobalOnceContainmentCounterexampleReceipt(
        ordinary,
        fixed,
        global_once,
        fixed is not None,
        global_once is not None,
        ordinary is not None and fixed is not None and ordinary <= fixed,
        fixed is not None and global_once is None,
    )
    if not (
        receipt.standard_adaptive_cost == 2
        and receipt.fixed_cost == 2
        and receipt.global_once_adaptive_cost is None
        and receipt.global_once_containment_fails
    ):
        raise ArithmeticError("global-label-once containment counterexample failed audit")
    return receipt


def _query_labels_unique_in_tree(node: AdaptiveNode | None) -> bool:
    if node is None:
        return True
    seen: set[str] = set()
    def walk(current: AdaptiveNode) -> bool:
        if current.query is None:
            return True
        if current.query in seen:
            return False
        seen.add(current.query)
        return all(walk(child) for _, child in current.branches)
    return walk(node)


def sharp_global_once_unit_cost_ratio(
    world_count: int,
    query_count: int,
    max_arity: int,
) -> Fraction:
    """Sharp C_F/C_G among tasks resolvable by a global-label-once policy."""
    return sharp_bounded_arity_unit_cost_ratio(world_count, query_count, max_arity)


def sharp_global_once_unit_cost_ratio_receipt(
    world_count: int,
    query_count: int,
    max_arity: int,
    *,
    direct_check: bool = True,
) -> GlobalOnceExtremalReceipt:
    expected = sharp_global_once_unit_cost_ratio(world_count, query_count, max_arity)
    task = sharp_bounded_arity_unit_cost_witness(world_count, query_count, max_arity)
    ordinary = adaptive_minimum_resolution(task)
    fixed = fixed_minimum_resolution(task).minimum_cost
    unique = _query_labels_unique_in_tree(ordinary.selected_policy)

    global_cost = ordinary.minimum_worst_path_cost if unique else None
    if direct_check and len(task.queries) <= 9:
        exact_global = global_label_once_adaptive_minimum_resolution(
            task, max_queries=9
        ).minimum_worst_path_cost
        if exact_global != global_cost:
            raise ArithmeticError("global-label-once direct solver disagreed with sharp witness")
        global_cost = exact_global

    ratio = Fraction(fixed, global_cost) if fixed is not None and global_cost not in (None, 0) else None
    theorem = unique and ratio == expected
    if not theorem:
        raise ArithmeticError("global-label-once extremal witness failed theorem audit")
    return GlobalOnceExtremalReceipt(
        world_count,
        query_count,
        max_arity,
        expected,
        global_cost,
        fixed,
        ratio,
        unique,
        theorem,
    )
