"""Exact binary scope formula for a required structural gap.

Let q>=1 be an integer structural gap that a downstream dynamical regime requires.
For binary unit-cost sensing, define

    h*(q) = min { h>=1 : 2**h - 1 - h >= q }.

The binary productive-tree bound implies that any task with C_F-C_A>=q must
satisfy

    C_A >= h*(q),
    C_F >= h*(q)+q,
    world_count >= h*(q)+q+1,
    query_count >= h*(q)+q,
    |H_min| >= h*(q)+q.

Conversely, the repository's constructive binary tree-to-task theorem attains a
task at this corner: use a binary tree of height h* with h*+q internal nodes,
one physical query per internal node, and the private-pair construction.  The
fixed cost is h*+q; if adaptive cost were below h*, the binary flattening bound
C_F<=2**C_A-1 would contradict the minimality of h*.  Hence C_A=h* exactly.

Thus the componentwise first binary structural corner for gap q is

    n* = h* + q + 1,
    m* = h* + q,
    E* = h* + q.

For a generalized response G=a*Delta_g, q can be supplied by the strict
oscillation threshold in ``structural_oscillation_reachability``.  This module
therefore converts response geometry into a minimum binary information scope.

No novelty is claimed for full-binary-tree counting.  The repository-specific
use is the exact composition with the adaptive/fixed structural gap and the
feedback-phase threshold.
"""

from __future__ import annotations

from dataclasses import dataclass

from .bounded_arity_extremal_bounds import (
    BoundedArityTree,
    _height,
    _internal_count,
    _maximum_tree,
    _tree_task,
    maximum_bounded_arity_tree_internal_nodes,
)
from .core import FiniteTask, adaptive_minimum_resolution, fixed_minimum_resolution
from .productive_frontier import build_productive_frontier
from .structural_oscillation_reachability import (
    maximum_integer_gap_for_stable_response,
    minimum_integer_gap_for_oscillation,
)


def binary_gap_capacity_at_depth(adaptive_depth: int) -> int:
    """Maximum binary structural gap allowed at exact adaptive depth h."""

    if type(adaptive_depth) is not int or adaptive_depth < 1:
        raise ValueError("adaptive_depth must be a positive integer")
    h = adaptive_depth
    return (1 << h) - 1 - h


def minimum_binary_adaptive_depth_for_gap(required_gap: int) -> int:
    """Smallest h with 2**h-1-h >= required_gap."""

    if type(required_gap) is not int or required_gap < 1:
        raise ValueError("required_gap must be a positive integer")
    h = 1
    while binary_gap_capacity_at_depth(h) < required_gap:
        h += 1
    return h


@dataclass(frozen=True)
class BinaryGapScopeThreshold:
    required_structural_gap: int
    minimum_adaptive_depth: int
    minimum_world_count: int
    minimum_query_count: int
    minimum_productive_frontier_edge_count: int
    binary_gap_capacity_at_minimum_depth: int
    scope: str = "componentwise_first_binary_unit_cost_scope_for_required_gap"


def first_binary_scope_for_structural_gap(required_gap: int) -> BinaryGapScopeThreshold:
    """Return the exact componentwise first binary scope capable of gap q."""

    q = int(required_gap)
    if type(required_gap) is not int or q < 1:
        raise ValueError("required_gap must be a positive integer")
    h = minimum_binary_adaptive_depth_for_gap(q)
    fixed = h + q
    return BinaryGapScopeThreshold(
        required_structural_gap=q,
        minimum_adaptive_depth=h,
        minimum_world_count=fixed + 1,
        minimum_query_count=fixed,
        minimum_productive_frontier_edge_count=fixed,
        binary_gap_capacity_at_minimum_depth=binary_gap_capacity_at_depth(h),
    )


def _binary_gap_corner_tree(required_gap: int) -> tuple[BinaryGapScopeThreshold, BoundedArityTree]:
    receipt = first_binary_scope_for_structural_gap(required_gap)
    h = receipt.minimum_adaptive_depth
    n = receipt.minimum_world_count
    m = receipt.minimum_query_count
    tree = _maximum_tree(n, h, 2)
    if _height(tree) != h:
        raise ArithmeticError("binary corner tree did not attain the required height")
    if _internal_count(tree) != m:
        raise ArithmeticError("binary corner tree did not attain the required internal count")
    return receipt, tree


@dataclass(frozen=True)
class BinaryGapCornerAudit:
    required_structural_gap: int
    expected_adaptive_cost: int
    expected_fixed_cost: int
    expected_world_count: int
    expected_query_count: int
    constructed_tree_height: int
    constructed_internal_count: int
    private_pair_count: int
    direct_check_performed: bool
    observed_adaptive_cost: int | None
    observed_fixed_cost: int | None
    observed_frontier_edge_count: int | None
    theorem_holds: bool
    scope: str = "constructive_binary_gap_corner_audit"


def binary_gap_corner_witness(required_gap: int) -> FiniteTask:
    """Construct a solver-sized componentwise first binary task attaining gap q.

    ``FiniteTask`` itself is intentionally capped at 20 queries by the exact
    solver infrastructure.  The structural theorem is not capped; for larger
    corners use ``binary_gap_corner_audit`` with its tree-level checks.
    """

    receipt, tree = _binary_gap_corner_tree(required_gap)
    n = receipt.minimum_world_count
    m = receipt.minimum_query_count
    if m > 20:
        raise ValueError("FiniteTask witness is limited by the exact solver's 20-query cap")
    task, private_count = _tree_task(tree, n, m)
    if private_count != m:
        raise ArithmeticError("binary corner witness lost private-pair obligations")
    return task


def binary_gap_corner_audit(
    required_gap: int,
    *,
    direct_check: bool = True,
) -> BinaryGapCornerAudit:
    """Audit the constructive corner without confusing theorem scope with solver scope."""

    receipt, tree = _binary_gap_corner_tree(required_gap)
    h = receipt.minimum_adaptive_depth
    n = receipt.minimum_world_count
    m = receipt.minimum_query_count

    observed_ca = observed_cf = observed_edges = None
    perform = bool(direct_check and m <= 20)
    if perform:
        task, private_count = _tree_task(tree, n, m)
        if private_count != m:
            raise ArithmeticError("binary corner witness lost private-pair obligations")
        observed_ca = adaptive_minimum_resolution(task).minimum_worst_path_cost
        observed_cf = fixed_minimum_resolution(task).minimum_cost
        observed_edges = len(build_productive_frontier(task).minimal_productive_sets)

    # For large corners we deliberately stop before FiniteTask construction.
    # The private-pair theorem contributes one fixed-mandatory obligation per
    # internal node, so the constructive obligation count is still m.
    structural_checks = (
        _height(tree) == h
        and _internal_count(tree) == m
        and n == m + 1
        and receipt.minimum_productive_frontier_edge_count == m
    )
    direct_agrees = (
        not perform
        or (
            observed_ca == h
            and observed_cf == m
            and observed_cf - observed_ca == required_gap
            and observed_edges == m
        )
    )
    theorem_holds = structural_checks and direct_agrees
    if not theorem_holds:
        raise ArithmeticError("binary gap corner constructive audit failed")

    return BinaryGapCornerAudit(
        required_structural_gap=required_gap,
        expected_adaptive_cost=h,
        expected_fixed_cost=m,
        expected_world_count=n,
        expected_query_count=m,
        constructed_tree_height=_height(tree),
        constructed_internal_count=_internal_count(tree),
        private_pair_count=m,
        direct_check_performed=perform,
        observed_adaptive_cost=observed_ca,
        observed_fixed_cost=observed_cf,
        observed_frontier_edge_count=observed_edges,
        theorem_holds=theorem_holds,
    )


@dataclass(frozen=True)
class BinaryOscillationScopeThreshold:
    evolutionary_persistence: float
    community_memory: float
    gain_per_structural_gap: float
    minimum_oscillatory_gap: int
    maximum_stable_gap: int
    stable_integer_oscillation_possible: bool
    minimum_binary_scope: BinaryGapScopeThreshold | None
    scope: str = "binary_scope_threshold_for_stable_oscillatory_feedback"


def first_binary_scope_for_stable_oscillation(
    *,
    evolutionary_persistence: float,
    community_memory: float,
    gain_per_structural_gap: float,
) -> BinaryOscillationScopeThreshold:
    """Map generalized response geometry to its first stable binary scope.

    If the integer gap ladder jumps directly from nonoscillatory to unstable,
    ``minimum_binary_scope`` is ``None`` because no unit-cost integer structural
    gap can realize stable oscillation under the supplied response geometry.
    """

    q = minimum_integer_gap_for_oscillation(
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
        gain_per_structural_gap=gain_per_structural_gap,
    )
    stable_max = maximum_integer_gap_for_stable_response(
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
        gain_per_structural_gap=gain_per_structural_gap,
    )
    possible = q <= stable_max
    return BinaryOscillationScopeThreshold(
        evolutionary_persistence=float(evolutionary_persistence),
        community_memory=float(community_memory),
        gain_per_structural_gap=float(gain_per_structural_gap),
        minimum_oscillatory_gap=q,
        maximum_stable_gap=stable_max,
        stable_integer_oscillation_possible=possible,
        minimum_binary_scope=first_binary_scope_for_structural_gap(q) if possible else None,
    )


def binary_scope_formula_matches_bounded_arity_ceiling(required_gap: int) -> bool:
    """Audit the formula against the inherited exact binary recurrence.

    Checks that every smaller world count has gap ceiling <q and that the
    declared first world count reaches gap >=q at the formula's adaptive depth.
    Query/frontier lower bounds are algebraic from C_F>=h+q and C_F<=m,E.
    """

    receipt = first_binary_scope_for_structural_gap(required_gap)
    q = receipt.required_structural_gap
    h_star = receipt.minimum_adaptive_depth

    for n in range(2, receipt.minimum_world_count):
        ceiling = max(
            maximum_bounded_arity_tree_internal_nodes(n, h, 2) - h
            for h in range(1, n)
        )
        if ceiling >= q:
            return False

    n_star = receipt.minimum_world_count
    attained_ceiling = (
        maximum_bounded_arity_tree_internal_nodes(n_star, h_star, 2) - h_star
    )
    return attained_ceiling >= q
