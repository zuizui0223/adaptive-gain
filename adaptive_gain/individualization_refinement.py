"""Exact individualization-refinement canonicalization for residual pair cover.

Stable color refinement may leave non-singleton query classes.  This module
branches on one canonical non-singleton class, individualizes one query, refines
again, and recurses until every query has a singleton color.  The lexicographic
minimum over all canonical leaves is an exact weighted-incidence canonical form.
"""
from __future__ import annotations

from dataclasses import dataclass

from .isomorphism_quotient import ResidualPairCoverInstance


class IndividualizationRefinementLimitError(RuntimeError):
    """Exact individualization-refinement exceeded a declared search cap."""


@dataclass(frozen=True)
class IndividualizationRefinementSignature:
    signature: tuple
    canonical_query_order: tuple[int, ...]
    search_nodes: int
    canonical_leaves: int
    maximum_depth: int
    scope: str = "exact_individualization_refinement_weighted_residual_pair_cover_canonicalization"


def _validate(instance: ResidualPairCoverInstance) -> None:
    if type(instance.remaining_budget) is not int or instance.remaining_budget < 0:
        raise ValueError("remaining_budget must be a nonnegative integer")
    if any(type(cost) is not int or cost <= 0 for cost in instance.query_costs):
        raise ValueError("query costs must be positive integers")
    limit = 1 << len(instance.query_costs)
    if any(type(row) is not int or row < 0 or row >= limit for row in instance.separator_rows):
        raise ValueError("separator rows must be bitmasks over the declared queries")


def _rank(signatures) -> tuple[int, ...]:
    ranks = {signature: i for i, signature in enumerate(sorted(set(signatures)))}
    return tuple(ranks[signature] for signature in signatures)


def _refine_with_individualization(
    instance: ResidualPairCoverInstance,
    individualized: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    qn = len(instance.query_costs)
    rows = instance.separator_rows
    row_degrees = tuple(row.bit_count() for row in rows)
    marker = {q: i for i, q in enumerate(individualized)}

    base_query = []
    for q in range(qn):
        adjacent_degrees = tuple(
            sorted(row_degrees[p] for p, row in enumerate(rows) if row & (1 << q))
        )
        mark = (1, marker[q]) if q in marker else (0,)
        base_query.append(
            (instance.query_costs[q], len(adjacent_degrees), adjacent_degrees, mark)
        )
    query_colors = _rank(tuple(base_query))
    row_colors = _rank(tuple((degree,) for degree in row_degrees))

    for _ in range(qn + len(rows) + 2):
        new_rows = _rank(
            tuple(
                (
                    row_colors[p],
                    tuple(
                        sorted(
                            query_colors[q]
                            for q in range(qn)
                            if row & (1 << q)
                        )
                    ),
                )
                for p, row in enumerate(rows)
            )
        )
        new_queries = _rank(
            tuple(
                (
                    query_colors[q],
                    instance.query_costs[q],
                    tuple(
                        sorted(
                            new_rows[p]
                            for p, row in enumerate(rows)
                            if row & (1 << q)
                        )
                    ),
                )
                for q in range(qn)
            )
        )
        if new_rows == row_colors and new_queries == query_colors:
            return new_queries, new_rows
        query_colors, row_colors = new_queries, new_rows
    raise ArithmeticError("individualized color refinement failed to stabilize")


def _candidate_signature(
    instance: ResidualPairCoverInstance,
    query_colors: tuple[int, ...],
) -> tuple[tuple, tuple[int, ...]]:
    groups: dict[int, list[int]] = {}
    for q, color in enumerate(query_colors):
        groups.setdefault(color, []).append(q)
    if any(len(group) != 1 for group in groups.values()):
        raise ValueError("canonical leaf requires singleton query colors")
    order = tuple(groups[color][0] for color in sorted(groups))
    position = {old_q: new_q for new_q, old_q in enumerate(order)}
    transformed_rows = []
    for row in instance.separator_rows:
        mask = 0
        for old_q in order:
            if row & (1 << old_q):
                mask |= 1 << position[old_q]
        transformed_rows.append(mask)
    candidate = (
        instance.remaining_budget,
        tuple(instance.query_costs[q] for q in order),
        tuple(sorted(transformed_rows)),
    )
    return candidate, order


def individualization_refined_canonical_signature(
    instance: ResidualPairCoverInstance,
    *,
    max_nodes: int = 100_000,
    max_leaves: int = 100_000,
) -> IndividualizationRefinementSignature:
    """Return the exact canonical signature using individualization-refinement.

    The target cell is chosen deterministically from the stable coloring by
    `(cell_size, color_id)`.  Every query in that cell is individualized in turn,
    so no valid canonical leaf is omitted.  Search caps raise rather than return
    an approximate signature.
    """
    _validate(instance)
    if type(max_nodes) is not int or max_nodes < 1:
        raise ValueError("max_nodes must be a positive integer")
    if type(max_leaves) is not int or max_leaves < 1:
        raise ValueError("max_leaves must be a positive integer")

    nodes = leaves = max_depth = 0
    best_signature = None
    best_order = None

    def search(individualized: tuple[int, ...]) -> None:
        nonlocal nodes, leaves, max_depth, best_signature, best_order
        nodes += 1
        max_depth = max(max_depth, len(individualized))
        if nodes > max_nodes:
            raise IndividualizationRefinementLimitError(
                "individualization-refinement node cap reached"
            )
        query_colors, _ = _refine_with_individualization(instance, individualized)
        groups: dict[int, list[int]] = {}
        for q, color in enumerate(query_colors):
            groups.setdefault(color, []).append(q)
        non_singletons = [
            (len(group), color, tuple(group))
            for color, group in groups.items()
            if len(group) > 1
        ]
        if not non_singletons:
            leaves += 1
            if leaves > max_leaves:
                raise IndividualizationRefinementLimitError(
                    "individualization-refinement leaf cap reached"
                )
            candidate, order = _candidate_signature(instance, query_colors)
            if best_signature is None or candidate < best_signature:
                best_signature, best_order = candidate, order
            return

        _, _, target = min(non_singletons)
        for q in target:
            search(individualized + (q,))

    search(())
    assert best_signature is not None and best_order is not None
    return IndividualizationRefinementSignature(
        best_signature,
        best_order,
        nodes,
        leaves,
        max_depth,
    )
