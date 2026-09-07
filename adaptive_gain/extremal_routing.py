"""Extremal depth-two routing families for finite deterministic adaptive gain.

For every integer k >= 2 this module constructs a unit-cost task with 2k worlds
and k+1 queries:

* one k-valued router whose outcome i leaves exactly the mixed pair (a_i,b_i);
* k branch-specific binary terminal queries, one for each mixed pair.

The adaptive policy pays 2 on every path.  The productive-frontier hypergraph
contains one singleton edge for every physical query, so every fixed resolver
must buy all k+1 queries.  Hence

    C_A = 2,
    C_F = k+1,
    C_F / C_A = (k+1)/2.

The ratio is therefore unbounded when deterministic query arity may grow.
This is a structural finite result, not an empirical prevalence claim.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .core import FiniteTask, Query, World, adaptive_gain_receipt
from .productive_frontier import build_productive_frontier


@dataclass(frozen=True)
class ExtremalRoutingReceipt:
    branch_count: int
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    adaptive_gain: int
    fixed_to_adaptive_ratio: Fraction
    minimal_productive_sets: tuple[int, ...]
    singleton_frontier_query_names: tuple[str, ...]
    depth_two_world_bound: int
    saturates_depth_two_world_bound: bool
    scope: str = "unit_cost_deterministic_k_branch_depth_two_extremal_routing_family"


@dataclass(frozen=True)
class RatioThreeHalvesMinimalityReceipt:
    witness_branch_count: int
    witness_world_count: int
    witness_query_count: int
    witness_adaptive_cost: int
    witness_fixed_cost: int
    witness_ratio: Fraction
    no_task_with_at_most_three_queries_can_exceed: bool
    no_task_with_at_most_five_worlds_can_exceed: bool
    first_scope_certified: bool
    scope: str = "unit_cost_finite_deterministic_ratio_above_three_halves_minimality"


def depth_two_fixed_cost_world_bound(world_count: int) -> int:
    """Upper bound C_F <= 1+floor(n/2) whenever a unit-cost task has C_A=2.

    Choose an optimal depth-two policy.  Every unresolved root outcome cell
    contains at least two represented worlds with different targets, so there
    are at most floor(n/2) unresolved children.  Flattening the root query plus
    one second query per unresolved child is a valid fixed bundle.
    """
    if type(world_count) is not int or world_count < 1:
        raise ValueError("world_count must be a positive integer")
    return 1 + world_count // 2


def k_branch_routing_task(branch_count: int) -> FiniteTask:
    """Return the exact 2k-world, k+1-query extremal routing construction."""
    if type(branch_count) is not int or branch_count < 2:
        raise ValueError("branch_count must be an integer at least 2")
    k = branch_count
    worlds = tuple(
        [World(f"a{i+1}", 0) for i in range(k)]
        + [World(f"b{i+1}", 1) for i in range(k)]
    )

    # Router outcome i is shared by a_i and b_i, creating k mixed branches.
    router_outcomes = tuple(range(k)) + tuple(range(k))
    queries = [Query("router", 1, router_outcomes)]

    # q1 marks b1.  For i>=2, qi marks a_i.  This orientation makes the
    # cross-target pair (a1,b2) all-zero on every terminal query, so the router
    # itself is globally mandatory in every fixed resolving bundle.
    for i in range(k):
        outcomes = [0] * (2 * k)
        if i == 0:
            outcomes[k] = 1  # b1
        else:
            outcomes[i] = 1  # a_{i+1}
        queries.append(Query(f"terminal_{i+1}", 1, tuple(outcomes)))
    return FiniteTask(worlds, tuple(queries))


def extremal_routing_receipt(branch_count: int) -> ExtremalRoutingReceipt:
    task = k_branch_routing_task(branch_count)
    gain = adaptive_gain_receipt(task)
    if gain.adaptive_cost is None or gain.fixed_cost is None:
        raise ArithmeticError("extremal routing construction unexpectedly became unresolved")
    k = branch_count
    expected_adaptive = 2
    expected_fixed = k + 1
    if (gain.adaptive_cost, gain.fixed_cost) != (expected_adaptive, expected_fixed):
        raise ArithmeticError("extremal routing construction violated its exact cost formula")

    frontier = build_productive_frontier(task)
    expected_singletons = tuple(1 << q for q in range(len(task.queries)))
    if frontier.minimal_productive_sets != expected_singletons:
        raise ArithmeticError("extremal routing productive frontier lost singleton necessity")
    singleton_names = tuple(task.queries[mask.bit_length() - 1].name for mask in expected_singletons)
    bound = depth_two_fixed_cost_world_bound(len(task.worlds))
    return ExtremalRoutingReceipt(
        k,
        len(task.worlds),
        len(task.queries),
        gain.adaptive_cost,
        gain.fixed_cost,
        gain.fixed_cost - gain.adaptive_cost,
        Fraction(gain.fixed_cost, gain.adaptive_cost),
        frontier.minimal_productive_sets,
        singleton_names,
        bound,
        gain.fixed_cost == bound,
    )


def ratio_above_three_halves_minimality() -> RatioThreeHalvesMinimalityReceipt:
    """Certify the first possible unit-cost scope with C_F/C_A > 3/2.

    Query-count lower bound: with at most three unit-cost queries, C_F<=3.  If
    C_A=1 then C_F=1; otherwise C_A>=2, so C_F/C_A<=3/2.

    World-count lower bound for n<=5:
    * C_A=1 implies C_F=1;
    * C_A=2 implies C_F<=1+floor(n/2)<=3 by the depth-two bound;
    * C_A>=3: flatten an optimal adaptive tree.  A productive decision tree on
      n represented worlds has at most n-1 internal nodes, hence its union uses
      at most n-1 distinct unit-cost queries.  Thus C_F<=n-1<=4 and
      C_F/C_A<=4/3.

    The k=3 construction has six worlds, four queries, C_A=2 and C_F=4, so the
    two lower bounds are simultaneously attained.
    """
    witness = extremal_routing_receipt(3)
    ratio = witness.fixed_to_adaptive_ratio
    return RatioThreeHalvesMinimalityReceipt(
        3,
        witness.world_count,
        witness.query_count,
        witness.adaptive_cost,
        witness.fixed_cost,
        ratio,
        True,
        True,
        witness.world_count == 6 and witness.query_count == 4 and ratio > Fraction(3, 2),
    )
