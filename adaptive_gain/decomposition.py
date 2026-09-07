"""Exact cost decomposition for a selected optimal adaptive resolution tree.

The key object is the UNION of query identities used anywhere in the adaptive
policy.  Executing that union nonadaptively is always a valid fixed resolving
bundle.  This yields an exact decomposition of branch-exclusive overhead into
realized adaptive gain and a fixed-design bypass discount.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import AdaptiveNode, FiniteTask, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class PolicyCostDecomposition:
    status: str
    adaptive_cost: int | None
    fixed_cost: int | None
    policy_union_cost: int | None
    policy_union_queries: tuple[str, ...]
    branch_exclusive_overhead: int | None
    realized_adaptive_gain: int | None
    fixed_bypass_discount: int | None
    identity_holds: bool
    strict_gain_requires_positive_overhead: bool
    scope: str = "selected_optimal_deterministic_tree_positive_integer_query_costs"


def _policy_union_and_worst_path(task: FiniteTask, node: AdaptiveNode) -> tuple[set[str], int]:
    lookup = {q.name: q.cost for q in task.queries}

    def visit(current: AdaptiveNode, used_on_path: frozenset[str]) -> tuple[set[str], int]:
        if current.query is None:
            return set(), 0
        if current.query not in lookup:
            raise ValueError("policy contains an undeclared query")
        if current.query in used_on_path:
            raise ValueError("policy repeats a query on one path")
        union = {current.query}
        children = []
        for _, child in current.branches:
            child_union, child_cost = visit(child, used_on_path | {current.query})
            union.update(child_union)
            children.append(child_cost)
        if not children:
            raise ValueError("nonterminal policy node must have at least one branch")
        return union, lookup[current.query] + max(children)

    return visit(node, frozenset())


def optimal_policy_cost_decomposition(task: FiniteTask) -> PolicyCostDecomposition:
    """Decompose the selected optimal tree's union cost.

    Let ``U`` be the sum of costs of every distinct query appearing anywhere in
    the selected optimal adaptive tree, ``C_A`` its minimum worst-path cost, and
    ``C_F`` the minimum fixed resolving-bundle cost.  The union of all queries
    in a resolving tree is itself a resolving fixed bundle, so

        C_A <= C_F <= U.

    Therefore

        U - C_A = (C_F - C_A) + (U - C_F).

    The three nonnegative terms are named branch-exclusive overhead, realized
    adaptive gain, and fixed-bypass discount.  Positive branch-exclusive overhead
    is necessary but NOT sufficient for strict adaptive gain: another fixed
    bundle outside the selected tree can bypass the routing query.
    """
    adaptive = adaptive_minimum_resolution(task)
    fixed = fixed_minimum_resolution(task)
    ca, cf = adaptive.minimum_worst_path_cost, fixed.minimum_cost
    if ca is None and cf is None:
        return PolicyCostDecomposition(
            "not_resolvable_by_declared_queries", None, None, None, (), None, None, None,
            True, True,
        )
    if ca is None or cf is None or adaptive.selected_policy is None:
        raise ArithmeticError("fixed/adaptive class containment was violated")
    union_names, policy_worst = _policy_union_and_worst_path(task, adaptive.selected_policy)
    if policy_worst != ca:
        raise ArithmeticError("selected adaptive policy does not attain reported minimum cost")
    order = {q.name: i for i, q in enumerate(task.queries)}
    names = tuple(sorted(union_names, key=order.__getitem__))
    union_cost = sum(task.queries[order[name]].cost for name in names)
    if not ca <= cf <= union_cost:
        raise ArithmeticError("expected C_A <= C_F <= policy union cost")
    overhead = union_cost - ca
    gain = cf - ca
    bypass = union_cost - cf
    identity = overhead == gain + bypass
    if not identity:
        raise ArithmeticError("policy cost decomposition identity failed")
    if gain > 0 and overhead <= 0:
        raise ArithmeticError("strict gain without branch-exclusive overhead")
    return PolicyCostDecomposition(
        "resolved_cost_decomposition",
        ca,
        cf,
        union_cost,
        names,
        overhead,
        gain,
        bypass,
        identity,
        gain == 0 or overhead > 0,
    )
