"""Exhaustive validators for tiny binary deterministic task universes.

These scans are finite classification receipts, not empirical frequency claims.
Labeled query names and labeled binary outcomes are counted separately.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Hashable, Sequence

from .core import FiniteTask, Query, World, adaptive_gain_receipt, adaptive_minimum_resolution
from .information import bundle_information_bits


@dataclass(frozen=True)
class BinaryUniverseSummary:
    world_count: int
    query_count: int
    target_multiplicities: tuple[int, ...]
    total_tasks: int
    unresolved_tasks: int
    no_strict_gain_tasks: int
    strict_gain_tasks: int
    cost_pair_counts: tuple[tuple[str, int], ...]
    strict_gain_cost_pairs: tuple[tuple[int, int], ...]
    strict_tasks_all_optimal_roots_zero_direct_information: bool
    scope: str = "all_labeled_binary_query_maps_unit_cost_for_one_fixed_target_assignment"


def enumerate_binary_universe(
    targets: Sequence[Hashable], *, query_count: int = 3, max_tasks: int = 100_000
) -> BinaryUniverseSummary:
    """Enumerate every labeled binary outcome map for ``query_count`` unit queries.

    The target assignment is fixed in the supplied world order.  Relabeling
    worlds, targets, queries, or binary outcomes can create isomorphic tasks that
    are counted separately; this function is a regression/classification tool,
    not a quotient by symmetry.
    """
    target_tuple = tuple(targets)
    if not target_tuple:
        raise ValueError("at least one target-labeled world is required")
    if type(query_count) is not int or query_count < 0:
        raise ValueError("query_count must be a nonnegative integer")
    patterns = tuple(product((0, 1), repeat=len(target_tuple)))
    total_tasks = len(patterns) ** query_count
    if total_tasks > max_tasks:
        raise ValueError("declared exhaustive universe exceeds max_tasks")
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(target_tuple))
    counts: dict[tuple[int | None, int | None], int] = {}
    strict_pairs = set()
    strict = 0
    unresolved = 0
    all_zero = True
    for maps in product(patterns, repeat=query_count):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, tuple(outcomes)) for j, outcomes in enumerate(maps)),
        )
        receipt = adaptive_gain_receipt(task)
        pair = (receipt.adaptive_cost, receipt.fixed_cost)
        counts[pair] = counts.get(pair, 0) + 1
        if receipt.adaptive_cost is None:
            unresolved += 1
        if receipt.strict_adaptive_gain:
            strict += 1
            strict_pairs.add((receipt.adaptive_cost, receipt.fixed_cost))
            roots = adaptive_minimum_resolution(task).optimal_first_queries
            if any(bundle_information_bits(task, (root,)) > 1e-12 for root in roots):
                all_zero = False
    multiplicities: dict[Hashable, int] = {}
    for target in target_tuple:
        multiplicities[target] = multiplicities.get(target, 0) + 1
    def pair_name(pair):
        return f"{pair[0]}:{pair[1]}"
    ordered_counts = tuple(sorted(((pair_name(k), v) for k, v in counts.items())))
    return BinaryUniverseSummary(
        len(target_tuple),
        query_count,
        tuple(sorted(multiplicities.values())),
        total_tasks,
        unresolved,
        total_tasks - strict,
        strict,
        ordered_counts,
        tuple(sorted(strict_pairs)),
        all_zero if strict else True,
    )
