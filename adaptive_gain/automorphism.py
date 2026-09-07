"""Exact small-task automorphism groups for weighted residual pair-cover incidence.

After stable color refinement, valid query automorphisms must remain inside the
stable query color classes.  This module enumerates those cost/invariant-preserving
permutations exactly, keeps the permutations that preserve the obligation-row
multiset, derives query orbits and a small generator set, and reports the exact
number of distinct labeled incidence forms under the remaining permutation search.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product

from .color_refinement import refine_residual_incidence_colors
from .isomorphism_quotient import ResidualIsomorphismLimitError, ResidualPairCoverInstance


@dataclass(frozen=True)
class ResidualAutomorphismGroupReceipt:
    query_count: int
    stable_query_color_class_sizes: tuple[int, ...]
    allowed_color_preserving_permutations: int
    automorphism_count: int
    distinct_labeled_incidence_forms: int
    query_orbits: tuple[tuple[int, ...], ...]
    generator_permutations: tuple[tuple[int, ...], ...]
    permutations_examined: int
    complete_enumeration: bool
    scope: str = "exact_query_automorphism_group_of_weighted_residual_pair_cover_incidence"


def _groups_from_colors(colors: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    groups: dict[int, list[int]] = {}
    for q, color in enumerate(colors):
        groups.setdefault(color, []).append(q)
    return tuple(tuple(groups[color]) for color in sorted(groups))


def _candidate_mappings(groups: tuple[tuple[int, ...], ...], qn: int):
    families = tuple(tuple(permutations(group)) for group in groups)
    for selected in product(*families):
        mapping = list(range(qn))
        for group, permuted in zip(groups, selected):
            for old, new in zip(group, permuted):
                mapping[old] = new
        yield tuple(mapping)


def _transform_rows(rows: tuple[int, ...], mapping: tuple[int, ...]) -> tuple[int, ...]:
    transformed = []
    for row in rows:
        mask = 0
        for old, new in enumerate(mapping):
            if row & (1 << old):
                mask |= 1 << new
        transformed.append(mask)
    return tuple(sorted(transformed))


def _is_automorphism(instance: ResidualPairCoverInstance, mapping: tuple[int, ...]) -> bool:
    qn = len(instance.query_costs)
    if len(mapping) != qn or set(mapping) != set(range(qn)):
        return False
    if any(
        instance.query_costs[old] != instance.query_costs[new]
        for old, new in enumerate(mapping)
    ):
        return False
    return _transform_rows(instance.separator_rows, mapping) == tuple(
        sorted(instance.separator_rows)
    )


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Return left after right for old->new permutation tuples."""
    return tuple(left[right[i]] for i in range(len(left)))


def _generated_group(
    generators: tuple[tuple[int, ...], ...], qn: int
) -> frozenset[tuple[int, ...]]:
    identity = tuple(range(qn))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            for candidate in (
                _compose(generator, current),
                _compose(current, generator),
            ):
                if candidate not in group:
                    group.add(candidate)
                    frontier.append(candidate)
    return frozenset(group)


def residual_automorphism_group(
    instance: ResidualPairCoverInstance,
    *,
    max_permutations: int = 100_000,
) -> ResidualAutomorphismGroupReceipt:
    """Enumerate the exact query automorphism group of a small residual instance."""
    query_colors, _, refinement = refine_residual_incidence_colors(instance)
    groups = _groups_from_colors(query_colors)
    allowed = refinement.refined_permutation_count
    if allowed > max_permutations:
        raise ResidualIsomorphismLimitError(
            f"exact automorphism enumeration needs {allowed} color-preserving permutations, "
            f"exceeding cap {max_permutations}"
        )

    automorphisms = tuple(
        mapping
        for mapping in _candidate_mappings(groups, len(instance.query_costs))
        if _is_automorphism(instance, mapping)
    )
    if not automorphisms:
        raise ArithmeticError("identity automorphism was lost")
    auto_set = frozenset(automorphisms)
    identity = tuple(range(len(instance.query_costs)))
    if identity not in auto_set:
        raise ArithmeticError("identity automorphism was lost")

    # Greedily build a small exact generator set from the complete group.
    generators: list[tuple[int, ...]] = []
    generated = _generated_group((), len(instance.query_costs))
    for mapping in sorted(auto_set):
        if mapping not in generated:
            generators.append(mapping)
            generated = _generated_group(tuple(generators), len(instance.query_costs))
        if generated == auto_set:
            break
    if generated != auto_set:
        raise ArithmeticError("automorphism generators did not reproduce the complete group")

    unseen = set(range(len(instance.query_costs)))
    orbits = []
    while unseen:
        q = min(unseen)
        orbit = tuple(sorted({mapping[q] for mapping in auto_set}))
        orbits.append(orbit)
        unseen.difference_update(orbit)

    if allowed % len(auto_set):
        raise ArithmeticError("automorphism count does not divide color-preserving labelings")
    receipt = ResidualAutomorphismGroupReceipt(
        len(instance.query_costs),
        refinement.refined_query_color_class_sizes,
        allowed,
        len(auto_set),
        allowed // len(auto_set),
        tuple(orbits),
        tuple(generators),
        allowed,
        True,
    )
    if not verify_residual_automorphism_group(instance, receipt):
        raise ArithmeticError("generated automorphism receipt failed independent verification")
    return receipt


def verify_residual_automorphism_group(
    instance: ResidualPairCoverInstance,
    receipt: ResidualAutomorphismGroupReceipt,
) -> bool:
    """Re-enumerate the bounded candidate group and verify completeness exactly."""
    if not receipt.complete_enumeration or receipt.query_count != len(instance.query_costs):
        return False
    try:
        query_colors, _, refinement = refine_residual_incidence_colors(instance)
    except (ValueError, ArithmeticError):
        return False
    groups = _groups_from_colors(query_colors)
    candidates = tuple(_candidate_mappings(groups, len(instance.query_costs)))
    exact = frozenset(mapping for mapping in candidates if _is_automorphism(instance, mapping))
    generated = _generated_group(receipt.generator_permutations, len(instance.query_costs))
    if generated != exact:
        return False
    if receipt.automorphism_count != len(exact):
        return False
    if receipt.allowed_color_preserving_permutations != refinement.refined_permutation_count:
        return False
    if receipt.permutations_examined != len(candidates):
        return False
    if receipt.allowed_color_preserving_permutations % receipt.automorphism_count:
        return False
    if receipt.distinct_labeled_incidence_forms != (
        receipt.allowed_color_preserving_permutations // receipt.automorphism_count
    ):
        return False
    expected_orbits = []
    unseen = set(range(len(instance.query_costs)))
    while unseen:
        q = min(unseen)
        orbit = tuple(sorted({mapping[q] for mapping in exact}))
        expected_orbits.append(orbit)
        unseen.difference_update(orbit)
    return receipt.query_orbits == tuple(expected_orbits)
