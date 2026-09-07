"""Exact two-sided adaptive Bellman kernel.

This solver combines the two adaptive-safe state-local reductions already proved
separately:

- world side: collapse same-target future-incidence twins to one representative;
- query side: keep only the target-relevant cross-target refinement frontier.

At every recursive state the world quotient is recomputed after the consumed and
refinement-dominated queries have been removed.  The result is then audited
against the original direct Bellman solver.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .adaptive_safe_compression import target_relevant_refinement_dominance
from .adaptive_world_twins import target_relevant_world_twin_representative_mask
from .core import FiniteTask, adaptive_minimum_resolution
from .target_pair_incidence import _mixed_outcome_components, target_pair_incidence_task


@dataclass(frozen=True)
class AdaptiveTwoSidedKernelReceipt:
    minimum_worst_path_cost: int | None
    selected_optimal_first_queries: tuple[str, ...]
    canonical_search_states: int
    world_canonicalization_calls: int
    world_occurrences_collapsed: int
    maximum_single_state_world_collapse: int
    raw_query_candidates_seen: int
    nondominated_query_occurrences_evaluated: int
    refinement_dominated_query_occurrences_pruned: int
    no_progress_query_occurrences_skipped: int
    exact_direct_cost: int | None
    cost_agrees_with_direct_solver: bool
    scope: str = "exact_adaptive_bellman_two_sided_world_twin_and_query_refinement_kernel"


def adaptive_two_sided_kernel_minimum_resolution(
    task: FiniteTask,
) -> AdaptiveTwoSidedKernelReceipt:
    """Return exact C_A after composing world-twin and query-refinement reductions."""
    incidence = target_pair_incidence_task(task)
    n, qn = len(task.worlds), len(task.queries)
    root_worlds = (1 << n) - 1
    root_queries = (1 << qn) - 1

    states = 0
    world_calls = world_collapsed = max_world_collapse = 0
    raw_queries = evaluated = query_pruned = no_progress = 0

    def target_values(world_mask: int):
        return {
            incidence.targets[i]
            for i in range(n)
            if world_mask & (1 << i)
        }

    def canonicalize_worlds(world_mask: int, remaining_queries: int) -> int:
        nonlocal world_calls, world_collapsed, max_world_collapse
        world_calls += 1
        representative = target_relevant_world_twin_representative_mask(
            incidence,
            world_mask=world_mask,
            remaining_query_mask=remaining_queries,
        )
        reduction = world_mask.bit_count() - representative.bit_count()
        world_collapsed += reduction
        max_world_collapse = max(max_world_collapse, reduction)
        return representative

    @lru_cache(None)
    def search(canonical_worlds: int, remaining_queries: int):
        nonlocal states, raw_queries, evaluated, query_pruned, no_progress
        states += 1
        if len(target_values(canonical_worlds)) <= 1:
            return 0, ()

        available = tuple(
            q for q in range(qn)
            if remaining_queries & (1 << q)
        )
        raw_queries += len(available)
        frontier = target_relevant_refinement_dominance(
            incidence,
            world_mask=canonical_worlds,
            remaining_query_mask=remaining_queries,
        )
        query_pruned += len(available) - len(frontier)

        best: int | None = None
        roots: list[str] = []
        for row in frontier:
            q = row.dominating_query_index
            mixed = _mixed_outcome_components(incidence, canonical_worlds, q)
            if mixed == (canonical_worlds,):
                no_progress += 1
                continue

            evaluated += 1
            remove_mask = 1 << q
            for dominated in row.dominated_query_indices:
                remove_mask |= 1 << dominated
            next_queries = remaining_queries & ~remove_mask

            child_costs = []
            feasible = True
            for child in mixed:
                child = canonicalize_worlds(child, next_queries)
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

    root = canonicalize_worlds(root_worlds, root_queries)
    cost, roots = search(root, root_queries)
    direct = adaptive_minimum_resolution(task).minimum_worst_path_cost
    if cost != direct:
        raise ArithmeticError("adaptive two-sided kernel changed the exact adaptive cost")
    return AdaptiveTwoSidedKernelReceipt(
        cost,
        roots,
        states,
        world_calls,
        world_collapsed,
        max_world_collapse,
        raw_queries,
        evaluated,
        query_pruned,
        no_progress,
        direct,
        True,
    )
