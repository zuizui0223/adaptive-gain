"""Exact automorphism-orbit pruning for individualization-refinement.

The complete residual query automorphism group is certified first.  At an
individualization node, only automorphisms that fix every already individualized
query pointwise remain valid.  Queries in the same orbit of this stabilizer inside
the selected color cell lead to isomorphic child searches, so one representative
per orbit is sufficient.
"""
from __future__ import annotations

from dataclasses import dataclass

from .automorphism import _generated_group, residual_automorphism_group
from .individualization_refinement import (
    IndividualizationRefinementLimitError,
    _candidate_signature,
    _refine_with_individualization,
)
from .isomorphism_quotient import ResidualPairCoverInstance


@dataclass(frozen=True)
class OrbitPrunedIndividualizationSignature:
    signature: tuple
    canonical_query_order: tuple[int, ...]
    root_automorphism_count: int
    search_nodes: int
    canonical_leaves: int
    orbit_pruned_branches: int
    maximum_depth: int
    scope: str = "exact_individualization_refinement_with_certified_automorphism_stabilizer_orbit_pruning"


def _validate(instance: ResidualPairCoverInstance) -> None:
    if type(instance.remaining_budget) is not int or instance.remaining_budget < 0:
        raise ValueError("remaining_budget must be a nonnegative integer")
    if any(type(cost) is not int or cost <= 0 for cost in instance.query_costs):
        raise ValueError("query costs must be positive integers")
    limit = 1 << len(instance.query_costs)
    if any(type(row) is not int or row < 0 or row >= limit for row in instance.separator_rows):
        raise ValueError("separator rows must be bitmasks over the declared queries")


def orbit_pruned_individualization_canonical_signature(
    instance: ResidualPairCoverInstance,
    *,
    max_automorphism_permutations: int = 100_000,
    max_nodes: int = 100_000,
    max_leaves: int = 100_000,
) -> OrbitPrunedIndividualizationSignature:
    """Return an exact canonical form with certified stabilizer-orbit pruning."""
    _validate(instance)
    if type(max_nodes) is not int or max_nodes < 1:
        raise ValueError("max_nodes must be a positive integer")
    if type(max_leaves) is not int or max_leaves < 1:
        raise ValueError("max_leaves must be a positive integer")

    automorphism_receipt = residual_automorphism_group(
        instance,
        max_permutations=max_automorphism_permutations,
    )
    full_group = _generated_group(
        automorphism_receipt.generator_permutations,
        len(instance.query_costs),
    )
    if len(full_group) != automorphism_receipt.automorphism_count:
        raise ArithmeticError("certified automorphism generators changed group size")

    nodes = leaves = pruned = max_depth = 0
    best_signature = None
    best_order = None

    def search(individualized: tuple[int, ...]) -> None:
        nonlocal nodes, leaves, pruned, max_depth, best_signature, best_order
        nodes += 1
        max_depth = max(max_depth, len(individualized))
        if nodes > max_nodes:
            raise IndividualizationRefinementLimitError(
                "orbit-pruned individualization node cap reached"
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
                    "orbit-pruned individualization leaf cap reached"
                )
            candidate, order = _candidate_signature(instance, query_colors)
            if best_signature is None or candidate < best_signature:
                best_signature, best_order = candidate, order
            return

        _, _, target = min(non_singletons)
        target_set = set(target)
        stabilizer = tuple(
            mapping
            for mapping in full_group
            if all(mapping[q] == q for q in individualized)
        )
        if not stabilizer:
            raise ArithmeticError("identity disappeared from automorphism stabilizer")

        unseen = set(target)
        representatives = []
        while unseen:
            seed = min(unseen)
            orbit = {mapping[seed] for mapping in stabilizer}
            if not orbit <= target_set:
                raise ArithmeticError(
                    "certified stabilizer moved a query outside its refined target cell"
                )
            representatives.append(min(orbit))
            unseen.difference_update(orbit)
        pruned += len(target) - len(representatives)
        for q in tuple(sorted(representatives)):
            search(individualized + (q,))

    search(())
    assert best_signature is not None and best_order is not None
    return OrbitPrunedIndividualizationSignature(
        best_signature,
        best_order,
        automorphism_receipt.automorphism_count,
        nodes,
        leaves,
        pruned,
        max_depth,
    )
