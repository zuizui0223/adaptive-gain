"""Unbounded adaptive/fixed cost ratios using only binary unit-cost queries.

For m >= 1 let k=2^m.  Use m binary router bits to encode the k branch
indices, and one binary terminal query for each branch-specific mixed pair.
Every target resolution tree must contain all k distinct terminal resources;
a binary tree of depth m has at most 2^m-1 internal nodes, so C_A>=m+1.
The router-bit strategy attains m+1.  All k terminal queries and all m router
bits are globally mandatory for a fixed resolver, giving C_F=2^m+m.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .core import FiniteTask, Query, World, adaptive_gain_receipt
from .productive_frontier import build_productive_frontier


@dataclass(frozen=True)
class BinaryExtremalRoutingReceipt:
    router_bit_count: int
    branch_count: int
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    adaptive_gain: int
    fixed_to_adaptive_ratio: Fraction
    minimal_productive_sets: tuple[int, ...]
    all_queries_globally_mandatory: bool
    scope: str = "all_binary_unit_cost_power_of_two_routing_extremal_family"


@dataclass(frozen=True)
class BinaryRatioThreeHalvesMinimalityReceipt:
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    ratio: Fraction
    no_binary_task_with_at_most_four_queries_can_exceed: bool
    no_binary_task_with_at_most_five_worlds_can_exceed: bool
    first_scope_certified: bool
    scope: str = "all_binary_unit_cost_ratio_above_three_halves_minimality"


def _worlds(branch_count: int) -> tuple[World, ...]:
    return tuple(
        [World(f"a{i+1}", 0) for i in range(branch_count)]
        + [World(f"b{i+1}", 1) for i in range(branch_count)]
    )


def _terminal_queries(branch_count: int) -> tuple[Query, ...]:
    rows = []
    for i in range(branch_count):
        outcomes = [0] * (2 * branch_count)
        if i == 0:
            outcomes[branch_count] = 1  # b1
        else:
            outcomes[i] = 1  # a_{i+1}
        rows.append(Query(f"terminal_{i+1}", 1, tuple(outcomes)))
    return tuple(rows)


def binary_power_routing_task(router_bit_count: int) -> FiniteTask:
    """Return the exact power-of-two binary construction supported by the core cap.

    The mathematical family is defined for every m>=1.  The executable core
    currently permits at most 20 declared queries, so this factory rejects m
    whose 2^m+m resources exceed that implementation cap.
    """
    if type(router_bit_count) is not int or router_bit_count < 1:
        raise ValueError("router_bit_count must be a positive integer")
    m = router_bit_count
    k = 1 << m
    if k + m > 20:
        raise ValueError("executable exact solver permits at most 20 total queries")
    worlds = _worlds(k)
    routers = []
    for bit in range(m):
        branch_bits = tuple((i >> bit) & 1 for i in range(k))
        routers.append(Query(f"router_bit_{bit+1}", 1, branch_bits + branch_bits))
    return FiniteTask(worlds, tuple(routers) + _terminal_queries(k))


def binary_power_routing_receipt(router_bit_count: int) -> BinaryExtremalRoutingReceipt:
    task = binary_power_routing_task(router_bit_count)
    m = router_bit_count
    k = 1 << m
    exact = adaptive_gain_receipt(task)
    expected_adaptive = m + 1
    expected_fixed = k + m
    if (exact.adaptive_cost, exact.fixed_cost) != (expected_adaptive, expected_fixed):
        raise ArithmeticError("binary extremal construction violated its exact cost formula")
    frontier = build_productive_frontier(task)
    expected_singletons = tuple(1 << q for q in range(len(task.queries)))
    if frontier.minimal_productive_sets != expected_singletons:
        raise ArithmeticError("binary extremal construction lost singleton productive-frontier necessity")
    return BinaryExtremalRoutingReceipt(
        m,
        k,
        len(task.worlds),
        len(task.queries),
        expected_adaptive,
        expected_fixed,
        expected_fixed - expected_adaptive,
        Fraction(expected_fixed, expected_adaptive),
        frontier.minimal_productive_sets,
        True,
    )


def binary_three_branch_ratio_witness() -> FiniteTask:
    """Smallest registered all-binary unit-cost witness with ratio > 3/2."""
    k = 3
    worlds = _worlds(k)
    # Branch codes 00, 01, 10.  Each router bit has one basis branch relative
    # to branch 1, making that bit globally mandatory for fixed resolution.
    low = (0, 1, 0)
    high = (0, 0, 1)
    routers = (
        Query("router_bit_1", 1, low + low),
        Query("router_bit_2", 1, high + high),
    )
    return FiniteTask(worlds, routers + _terminal_queries(k))


def binary_ratio_above_three_halves_minimality() -> BinaryRatioThreeHalvesMinimalityReceipt:
    """Certify the first all-binary unit-cost scope with ratio above 3/2.

    With at most four queries:
    * C_A=1 implies C_F=1;
    * C_A=2 and a binary root has at most two mixed children, so flattening an
      optimal depth-two policy uses at most three queries and C_F<=3;
    * C_A>=3 gives C_F<=4 and ratio<=4/3.
    Thus more than 3/2 requires at least five queries.

    With at most five worlds, C_A=2 gives C_F<=3 by the general depth-two
    world bound; C_A>=3 gives C_F<=n-1<=4 by flattening the adaptive tree.
    Thus more than 3/2 also requires at least six worlds.

    The explicit 3-branch task uses six worlds and five binary queries.  Its
    three terminal resources are individually mandatory.  A depth-two binary
    tree has at most three internal nodes; using all three terminals leaves no
    router resource and cannot distinguish the all-zero-terminal pairs
    (a1,b2)/(a1,b3).  Hence C_A>=3.  The two router bits followed by the
    appropriate terminal attain depth 3.  All five resources are mandatory for
    fixed resolution, so C_F=5.
    """
    task = binary_three_branch_ratio_witness()
    exact = adaptive_gain_receipt(task)
    if (exact.adaptive_cost, exact.fixed_cost) != (3, 5):
        raise ArithmeticError("binary minimal witness violated expected costs")
    frontier = build_productive_frontier(task)
    if frontier.minimal_productive_sets != tuple(1 << q for q in range(5)):
        raise ArithmeticError("binary minimal witness lost singleton fixed necessity")
    ratio = Fraction(5, 3)
    return BinaryRatioThreeHalvesMinimalityReceipt(
        6,
        5,
        3,
        5,
        ratio,
        True,
        True,
        ratio > Fraction(3, 2),
    )
