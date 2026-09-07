"""Explicit unit-cost families with unbounded fixed/adaptive ratio.

Two constructions are registered.

1. ``extremal_routing_task(k)`` uses one k-ary router plus k branch-terminal
   queries and has

       C_A = 2, C_F = k + 1.

2. ``binary_extremal_routing_task(d)`` uses only binary observations.  It has
   ``k=2**d`` target-mixed branches, d binary routing bits, and one terminal query
   per branch.  It has

       C_A = d + 1, C_F = 2**d.

Thus even with binary outcomes and unit acquisition costs the ratio is unbounded.
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
class BinaryExtremalRoutingFamilyReceipt:
    routing_depth: int
    branch_count: int
    world_count: int
    query_count: int
    expected_adaptive_cost: int
    expected_fixed_cost: int
    expected_ratio: Fraction
    lower_bound_values: tuple[int, ...]
    lower_bound_minimum: int
    direct_adaptive_cost: int | None
    direct_fixed_cost: int | None
    direct_check_performed: bool
    direct_check_agrees: bool
    theorem_holds: bool
    scope: str = "binary_unit_cost_branch_index_bits_plus_branch_terminal_queries"


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

    router_outcomes = []
    for i in range(branch_count):
        router_outcomes.extend((i, i))
    queries = [Query("router", 1, tuple(router_outcomes))]

    # Code(a_j) has ones in coordinates < j; code(b_j) has ones in
    # coordinates <= j.  Thus code(a_{i+1}) == code(b_i), making the router
    # mandatory between adjacent branches, while q_i alone resolves branch i.
    for i in range(branch_count):
        outcomes = []
        for j in range(branch_count):
            outcomes.append(int(i < j))
            outcomes.append(int(i <= j))
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


def binary_extremal_routing_task(routing_depth: int) -> FiniteTask:
    """Return a unit-cost unbounded-ratio family using only binary query outcomes."""
    if type(routing_depth) is not int or routing_depth < 1:
        raise ValueError("routing_depth must be a positive integer")
    branch_count = 1 << routing_depth
    worlds = []
    for i in range(branch_count):
        worlds.append(World(f"a{i}", 0))
        worlds.append(World(f"b{i}", 1))

    queries = []
    # Routing bits identify branch index but carry no target information within
    # any branch pair.
    for bit in range(routing_depth):
        outcomes = []
        for i in range(branch_count):
            value = (i >> bit) & 1
            outcomes.extend((value, value))
        queries.append(Query(f"route_bit_{bit}", 1, tuple(outcomes)))

    # terminal_i is 1 only on target-1 world b_i.  Pair (a_i,b_i) is therefore
    # separated by terminal_i and by no other declared query, making all
    # terminals fixed-mandatory.
    for terminal in range(branch_count):
        outcomes = []
        for i in range(branch_count):
            outcomes.extend((0, int(i == terminal)))
        queries.append(Query(f"terminal_{terminal}", 1, tuple(outcomes)))
    return FiniteTask(tuple(worlds), tuple(queries))


def _binary_target0_path_lower_bounds(routing_depth: int) -> tuple[int, ...]:
    # After r independent routing bits, 2**(d-r) branch indices remain compatible
    # with a target-0 world.  Since every terminal returns zero on every target-0
    # world, each compatible target-1 world b_j must be eliminated by its own
    # terminal query.  Hence every target-0 path costs at least r+2**(d-r).
    return tuple(r + (1 << (routing_depth - r)) for r in range(routing_depth + 1))


def binary_extremal_routing_family_audit(
    routing_depth: int,
    *,
    direct_check: bool = True,
) -> BinaryExtremalRoutingFamilyReceipt:
    if type(routing_depth) is not int or routing_depth < 1:
        raise ValueError("routing_depth must be a positive integer")
    branch_count = 1 << routing_depth
    expected_ca = routing_depth + 1
    expected_cf = branch_count
    bounds = _binary_target0_path_lower_bounds(routing_depth)
    lower = min(bounds)
    if lower != expected_ca:
        raise ArithmeticError("binary family target-0 path lower bound was not d+1")

    direct_ca = direct_cf = None
    direct_agrees = True
    if direct_check:
        task = binary_extremal_routing_task(routing_depth)
        direct_ca = adaptive_minimum_resolution(task).minimum_worst_path_cost
        direct_cf = fixed_minimum_resolution(task).minimum_cost
        direct_agrees = direct_ca == expected_ca and direct_cf == expected_cf
        if not direct_agrees:
            raise ArithmeticError("binary extremal family direct solver disagreed with theorem")

    receipt = BinaryExtremalRoutingFamilyReceipt(
        routing_depth,
        branch_count,
        2 * branch_count,
        routing_depth + branch_count,
        expected_ca,
        expected_cf,
        Fraction(expected_cf, expected_ca),
        bounds,
        lower,
        direct_ca,
        direct_cf,
        direct_check,
        direct_agrees,
        lower == expected_ca and (not direct_check or direct_agrees),
    )
    if not receipt.theorem_holds:
        raise ArithmeticError("binary extremal routing family audit failed")
    return receipt


def unit_cost_ratio_upper_bound_by_world_count(world_count: int) -> Fraction:
    """Upper-bound C_F/C_A using only represented-world count for unit costs."""
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    ca1 = Fraction(1, 1)
    ca2 = Fraction(1 + floor(world_count / 2), 2)
    ca3plus = Fraction(max(0, world_count - 1), 3)
    return max(ca1, ca2, ca3plus)


def first_unit_cost_ratio_above_three_halves_receipt() -> UnitCostRatioThresholdReceipt:
    """Certify that six worlds/four queries attain the first >3/2 unit-cost scope."""
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
