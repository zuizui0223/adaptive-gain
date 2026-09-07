"""Local productive-frontier certificates for absence of external shortcut.

Let H be the productive frontier and S the selected adaptive policy union.  For
an outside resource q, suppose there is a replacement set R_q subseteq S with
cost(R_q) <= cost(q) that hits every frontier edge containing q.  Replacing each
outside member of any global hitting set by its R_q preserves edge coverage and
does not increase cost.  If every outside resource has such a replacement, then
C_F=C_U and the external shortcut discount is zero.

This is a sufficient certificate, not a necessary characterization.  It can be
strictly stronger than pairwise query dominance because R_q may contain several
inside resources.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import AdaptiveNode, FiniteTask, adaptive_minimum_resolution
from .productive_frontier import ProductiveFrontierCertificate, build_productive_frontier


class FrontierReplacementLimitError(RuntimeError):
    """Declared replacement-subset search cap was exceeded."""


@dataclass(frozen=True, order=True)
class OutsideResourceReplacement:
    outside_query: str
    replacement_queries: tuple[str, ...]
    outside_cost: int
    replacement_cost: int
    covered_frontier_edge_count: int


@dataclass(frozen=True)
class FrontierNoExternalShortcutCertificate:
    policy_union_queries: tuple[str, ...]
    replacements: tuple[OutsideResourceReplacement, ...]
    certified: bool
    subsets_examined: int
    complete_search: bool
    scope: str = "set_valued_inside_replacement_certificate_for_zero_external_shortcut"


def _mask(names: tuple[str, ...], query_names: tuple[str, ...]) -> int:
    lookup = {name: i for i, name in enumerate(query_names)}
    if len(set(names)) != len(names) or any(name not in lookup for name in names):
        raise ValueError("query names must be unique and declared")
    result = 0
    for name in names:
        result |= 1 << lookup[name]
    return result


def _names(mask: int, query_names: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(name for q, name in enumerate(query_names) if mask & (1 << q))


def _cost(mask: int, costs: tuple[int, ...]) -> int:
    return sum(cost for q, cost in enumerate(costs) if mask & (1 << q))


def frontier_replacement_certificate(
    frontier: ProductiveFrontierCertificate,
    policy_union_queries: tuple[str, ...],
    *,
    max_subsets_per_outside_query: int = 1_000_000,
) -> FrontierNoExternalShortcutCertificate:
    """Search exact inside replacements for each outside frontier resource."""
    if not isinstance(frontier, ProductiveFrontierCertificate) or frontier.complete is not True:
        raise ValueError("frontier must be a complete ProductiveFrontierCertificate")
    if type(max_subsets_per_outside_query) is not int or max_subsets_per_outside_query < 1:
        raise ValueError("max_subsets_per_outside_query must be a positive integer")
    qn = len(frontier.query_names)
    union_mask = _mask(policy_union_queries, frontier.query_names)
    inside_indices = tuple(q for q in range(qn) if union_mask & (1 << q))
    subset_count = 1 << len(inside_indices)
    if subset_count > max_subsets_per_outside_query:
        raise FrontierReplacementLimitError(
            f"inside replacement search needs {subset_count} subsets per outside query, "
            f"exceeding cap {max_subsets_per_outside_query}"
        )

    inside_masks = []
    for local in range(subset_count):
        mask = 0
        for bit, q in enumerate(inside_indices):
            if local & (1 << bit):
                mask |= 1 << q
        inside_masks.append(mask)
    inside_masks.sort(key=lambda mask: (_cost(mask, frontier.query_costs), mask.bit_count(), mask))

    replacements = []
    examined = 0
    certified = True
    for q in range(qn):
        bit = 1 << q
        if union_mask & bit:
            continue
        target_edges = tuple(edge for edge in frontier.minimal_productive_sets if edge & bit)
        outside_cost = frontier.query_costs[q]
        chosen = None
        for candidate in inside_masks:
            examined += 1
            candidate_cost = _cost(candidate, frontier.query_costs)
            if candidate_cost > outside_cost:
                break
            if all(candidate & edge for edge in target_edges):
                chosen = candidate
                break
        if chosen is None:
            certified = False
            continue
        replacements.append(
            OutsideResourceReplacement(
                frontier.query_names[q],
                _names(chosen, frontier.query_names),
                outside_cost,
                _cost(chosen, frontier.query_costs),
                len(target_edges),
            )
        )

    result = FrontierNoExternalShortcutCertificate(
        policy_union_queries,
        tuple(replacements),
        certified,
        examined,
        True,
    )
    if certified and not verify_frontier_replacement_certificate(frontier, result):
        raise ArithmeticError("generated frontier replacement certificate failed verification")
    return result


def verify_frontier_replacement_certificate(
    frontier: ProductiveFrontierCertificate,
    certificate: FrontierNoExternalShortcutCertificate,
) -> bool:
    """Verify stored replacements directly from frontier incidence and costs."""
    try:
        if not isinstance(frontier, ProductiveFrontierCertificate) or frontier.complete is not True:
            return False
        if not isinstance(certificate, FrontierNoExternalShortcutCertificate):
            return False
        if certificate.complete_search is not True or certificate.certified is not True:
            return False
        union_mask = _mask(certificate.policy_union_queries, frontier.query_names)
        lookup = {name: i for i, name in enumerate(frontier.query_names)}
        outside = tuple(
            frontier.query_names[q]
            for q in range(len(frontier.query_names))
            if not (union_mask & (1 << q))
        )
        if tuple(row.outside_query for row in certificate.replacements) != outside:
            return False
        for row in certificate.replacements:
            q = lookup[row.outside_query]
            bit = 1 << q
            replacement_mask = _mask(row.replacement_queries, frontier.query_names)
            if replacement_mask & ~union_mask:
                return False
            actual_cost = _cost(replacement_mask, frontier.query_costs)
            if row.outside_cost != frontier.query_costs[q]:
                return False
            if row.replacement_cost != actual_cost or actual_cost > row.outside_cost:
                return False
            target_edges = tuple(edge for edge in frontier.minimal_productive_sets if edge & bit)
            if row.covered_frontier_edge_count != len(target_edges):
                return False
            if not all(replacement_mask & edge for edge in target_edges):
                return False
        return True
    except (AttributeError, TypeError, ValueError, KeyError, IndexError):
        return False


def _selected_policy_union(task: FiniteTask, node: AdaptiveNode | None) -> tuple[str, ...]:
    if node is None:
        return ()
    order = {query.name: i for i, query in enumerate(task.queries)}

    def visit(current: AdaptiveNode, used: frozenset[str]) -> set[str]:
        if current.query is None:
            return set()
        if current.query not in order or current.query in used:
            raise ValueError("selected policy contains an invalid or repeated query")
        union = {current.query}
        for _, child in current.branches:
            union.update(visit(child, used | {current.query}))
        return union

    return tuple(sorted(visit(node, frozenset()), key=order.__getitem__))


def selected_policy_no_external_shortcut_certificate(
    task: FiniteTask,
    *,
    max_subsets_per_outside_query: int = 1_000_000,
) -> FrontierNoExternalShortcutCertificate:
    adaptive = adaptive_minimum_resolution(task)
    if adaptive.minimum_worst_path_cost is None or adaptive.selected_policy is None:
        raise ValueError("task must have a selected resolving adaptive policy")
    union = _selected_policy_union(task, adaptive.selected_policy)
    frontier = build_productive_frontier(task)
    return frontier_replacement_certificate(
        frontier,
        union,
        max_subsets_per_outside_query=max_subsets_per_outside_query,
    )
