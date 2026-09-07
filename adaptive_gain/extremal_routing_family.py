"""An explicit unit-cost family with unbounded fixed/adaptive ratio.

For ``k >= 2`` create ``k`` target-mixed branches, each containing one target-0
world ``a_i`` and one target-1 world ``b_i``.  A single k-ary router reports the
branch index.  Terminal query ``q_i`` resolves only branch i.

The terminal outcome codes are chained so that ``a_{i+1}`` and ``b_i`` agree under
every terminal query.  Hence the router is globally mandatory for fixed
resolution, while pair ``(a_i,b_i)`` makes terminal ``q_i`` mandatory.  Therefore

    C_A = 2,
    C_F = k + 1,
    gain = k - 1,
    C_F / C_A = (k + 1) / 2.

The ratio is unbounded as k grows.  The k=2 member is isomorphic to the registered
minimal four-world strict-gain mechanism up to query/world relabeling.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import floor

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution
from .productive_frontier import build_productive_frontier


@dataclass(frozen=True)
class ExtremalRoutingFamilyReceipt:
    branch_count: int
    world_count: int
    query_count: int
    adaptive_cost: int | None
    fixed_cost: int | None
    additive_gain: int | None
    ratio: Fraction | None
    expected_adaptive_cost: int
    expected_fixed_cost: int
    minimal_frontier_edges: tuple[int, ...]
    every_query_frontier_mandatory: bool
    theorem_holds: bool
    scope: str = "unit_cost_k_ary_router_with_chain_terminal_codes"


@dataclass(frozen=True)
class UnitCostRatioThresholdReceipt:
    tested_world_upper_bound: int
    threshold: Fraction
    maximum_possible_ratio_under_bound: Fraction
    ratio_above_threshold_impossible: bool
    minimum_query_count_if_threshold_exceeded: int
    witness_world_count: int
    witness_query_count: int
    witness_ratio: Fraction
    scope: str = "unit_cost_finite_deterministic_world_count_threshold_bound"


def extremal_routing_task(branch_count: int) -> FiniteTask:
    """Return the k-branch star-routing task described in the module theorem."""
    if type(branch_count) is not int or branch_count < 2:
        raise ValueError("branch_count must be an integer at least 2")

    worlds = []
    for i in range(branch_count):
        worlds.append(World(f"a{i}", 0))
        worlds.append(World(f"b{i}", 1))

    # Router outcome is the branch index and is target-blind within a branch.
    router_outcomes = []
    for i in range(branch_count):
        router_outcomes.extend((i, i))
    queries = [Query("router", 1, tuple(router_outcomes))]

    # Code of a_j has ones in coordinates < j.  Code of b_j has ones in
    # coordinates <= j.  Thus q_i differs only within branch i, while
    # code(a_{i+1}) == code(b_i), making the router mandatory between branches.
    for i in range(branch_count):
        outcomes = []
        for j in range(branch_count):
            outcomes.append(int(i < j))   # a_j
            outcomes.append(int(i <= j))  # b_j
        queries.append(Query(f"terminal_{i}", 1, tuple(outcomes)))

    return FiniteTask(tuple(worlds), tuple(queries))


def extremal_routing_family_audit(branch_count: int) -> ExtremalRoutingFamilyReceipt:
    task = extremal_routing_task(branch_count)
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    frontier = build_productive_frontier(task)
    expected_edges = tuple(1 << q for q in range(branch_count + 1))
    actual_edges = tuple(sorted(frontier.minimal_productive_sets))
    ratio = Fraction(fixed, adaptive) if fixed is not None and adaptive not in (None, 0) else None
    gain = fixed - adaptive if fixed is not None and adaptive is not None else None
    theorem_holds = (
        adaptive == 2
        and fixed == branch_count + 1
        and gain == branch_count - 1
        and ratio == Fraction(branch_count + 1, 2)
        and actual_edges == expected_edges
    )
    if not theorem_holds:
        raise ArithmeticError("extremal routing family theorem failed executable audit")
    return ExtremalRoutingFamilyReceipt(
        branch_count,
        len(task.worlds),
        len(task.queries),
        adaptive,
        fixed,
        gain,
        ratio,
        2,
        branch_count + 1,
        actual_edges,
        actual_edges == expected_edges,
        theorem_holds,
    )


def unit_cost_ratio_upper_bound_by_world_count(world_count: int) -> Fraction:
    """Upper-bound C_F/C_A using only represented-world count for unit costs.

    For C_A=1 the ratio is 1.  For C_A=2, the root can have at most
    floor(n/2) mixed child branches, so the flattened selected tree uses at most
    1+floor(n/2) query occurrences/resources.  For C_A>=3, any productive
    resolution tree on n represented worlds has at most n-1 internal nodes, so
    C_F/C_A <= (n-1)/3.  The maximum of those cases gives this bound.
    """
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    ca1 = Fraction(1, 1)
    ca2 = Fraction(1 + floor(world_count / 2), 2)
    ca3plus = Fraction(max(0, world_count - 1), 3)
    return max(ca1, ca2, ca3plus)


def first_unit_cost_ratio_above_three_halves_receipt() -> UnitCostRatioThresholdReceipt:
    """Certify that six worlds/four queries attain the first >3/2 unit-cost scope.

    With at most five worlds the bound above is at most 3/2.  Any ratio above
    3/2 has C_A>=2 and integer C_F, hence C_F>=4 and therefore needs at least four
    declared unit-cost queries.  The k=3 extremal family uses exactly six worlds
    and four queries and has ratio 2.
    """
    threshold = Fraction(3, 2)
    max_five = max(unit_cost_ratio_upper_bound_by_world_count(n) for n in range(2, 6))
    witness = extremal_routing_family_audit(3)
    if witness.ratio is None:
        raise ArithmeticError("missing extremal witness ratio")
    result = UnitCostRatioThresholdReceipt(
        5,
        threshold,
        max_five,
        max_five <= threshold,
        4,
        witness.world_count,
        witness.query_count,
        witness.ratio,
    )
    if not (
        result.ratio_above_threshold_impossible
        and result.witness_world_count == 6
        and result.witness_query_count == 4
        and result.witness_ratio > threshold
    ):
        raise ArithmeticError("unit-cost >3/2 threshold certificate failed")
    return result
