"""Balanced-binary unit-cost family with unbounded adaptive advantage.

For routing depth d>=1 let k=2**d.  Start from k mixed target pairs
(a_i,b_i), add one target-0 dummy world, and use:

* d binary routing-bit queries, balanced up to one because the dummy contributes
  one additional zero; and
* k binary terminal queries.  Terminal t_j separates a_j from b_j and is made
  globally balanced by assigning outcome one to both worlds in exactly k/2
  other branches.

Every query therefore has outcome counts (k+1,k) in some order on 2k+1 worlds.
Pair (a_j,b_j) is separated by t_j and by no other query, so every fixed resolver
must contain all k terminal resources: C_F>=k.  Reading all d routing bits and
then the identified branch terminal resolves adaptively in at most d+1 queries:
C_A<=d+1.  Hence

    C_F/C_A >= 2**d/(d+1) -> infinity.

The theorem is an existence/lower-bound result, not a sharp fixed-(n,m) theorem
under balancedness.  Small depths are audited with the repository's exact
solvers; the general construction exceeds the exact solver's 20-query cap.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class BalancedBinaryFamilyReceipt:
    routing_depth: int
    branch_count: int
    world_count: int
    query_count: int
    adaptive_upper_bound: int
    fixed_lower_bound: int
    ratio_lower_bound: Fraction
    all_queries_balanced: bool
    every_terminal_uniquely_mandatory: bool
    direct_adaptive_cost: int | None
    direct_fixed_cost: int | None
    direct_check_performed: bool
    direct_bounds_hold: bool
    theorem_holds: bool
    scope: str = "balanced_binary_unit_cost_unbounded_adaptive_advantage"


def balanced_binary_family_counts(routing_depth: int) -> tuple[int, int, int]:
    if type(routing_depth) is not int or routing_depth < 1:
        raise ValueError("routing_depth must be a positive integer")
    k = 1 << routing_depth
    return k, 2 * k + 1, routing_depth + k


def balanced_binary_ratio_lower_bound(routing_depth: int) -> Fraction:
    k, _, _ = balanced_binary_family_counts(routing_depth)
    return Fraction(k, routing_depth + 1)


def balanced_binary_extremal_task(routing_depth: int) -> FiniteTask:
    """Construct the balanced family when it fits the exact FiniteTask query cap."""
    k, _, query_count = balanced_binary_family_counts(routing_depth)
    if query_count > 20:
        raise ValueError("explicit FiniteTask exceeds the exact solver's 20-query cap")

    worlds = []
    for i in range(k):
        worlds.append(World(f"a{i}", 0))
        worlds.append(World(f"b{i}", 1))
    worlds.append(World("dummy", 0))

    queries = []
    # On the original 2k worlds every routing bit is exactly balanced.  The
    # target-0 dummy gets outcome zero, so counts become k+1 versus k.
    for bit in range(routing_depth):
        outcomes = []
        for i in range(k):
            value = (i >> bit) & 1
            outcomes.extend((value, value))
        outcomes.append(0)
        queries.append(Query(f"route_bit_{bit}", 1, tuple(outcomes)))

    # For terminal j choose the next k/2 cyclic branch indices.  This never
    # includes j.  Those complete pairs contribute k ones; b_j contributes one
    # more; dummy and a_j contribute zero.  Hence terminal counts are k+1/k.
    half = k // 2
    for j in range(k):
        filled = {(j + offset) % k for offset in range(1, half + 1)}
        outcomes = []
        for i in range(k):
            if i == j:
                outcomes.extend((0, 1))
            elif i in filled:
                outcomes.extend((1, 1))
            else:
                outcomes.extend((0, 0))
        outcomes.append(0)
        queries.append(Query(f"terminal_{j}", 1, tuple(outcomes)))

    return FiniteTask(tuple(worlds), tuple(queries))


def _balanced(query: Query) -> bool:
    zeros = sum(outcome == 0 for outcome in query.outcomes)
    ones = sum(outcome == 1 for outcome in query.outcomes)
    return zeros + ones == len(query.outcomes) and abs(zeros - ones) <= 1


def _terminals_uniquely_mandatory(task: FiniteTask, routing_depth: int) -> bool:
    k = 1 << routing_depth
    terminal_start = routing_depth
    for i in range(k):
        a = 2 * i
        b = a + 1
        separators = [
            q_index
            for q_index, query in enumerate(task.queries)
            if query.outcomes[a] != query.outcomes[b]
        ]
        if separators != [terminal_start + i]:
            return False
    return True


def balanced_binary_family_audit(
    routing_depth: int,
    *,
    direct_check: bool = True,
) -> BalancedBinaryFamilyReceipt:
    k, world_count, query_count = balanced_binary_family_counts(routing_depth)
    upper_ca = routing_depth + 1
    lower_cf = k
    direct_ca = direct_cf = None
    all_balanced = mandatory = True
    direct_bounds = True

    if direct_check:
        task = balanced_binary_extremal_task(routing_depth)
        all_balanced = all(_balanced(query) for query in task.queries)
        mandatory = _terminals_uniquely_mandatory(task, routing_depth)
        direct_ca = adaptive_minimum_resolution(task).minimum_worst_path_cost
        direct_cf = fixed_minimum_resolution(task).minimum_cost
        direct_bounds = (
            direct_ca is not None
            and direct_cf is not None
            and direct_ca <= upper_ca
            and direct_cf >= lower_cf
        )

    theorem = (
        world_count == 2 * k + 1
        and query_count == routing_depth + k
        and balanced_binary_ratio_lower_bound(routing_depth) == Fraction(k, routing_depth + 1)
        and (not direct_check or (all_balanced and mandatory and direct_bounds))
    )
    if not theorem:
        raise ArithmeticError("balanced-binary extremal family audit failed")
    return BalancedBinaryFamilyReceipt(
        routing_depth,
        k,
        world_count,
        query_count,
        upper_ca,
        lower_cf,
        Fraction(k, routing_depth + 1),
        all_balanced,
        mandatory,
        direct_ca,
        direct_cf,
        direct_check,
        direct_bounds,
        theorem,
    )
