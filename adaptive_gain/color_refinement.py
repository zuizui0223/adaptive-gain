"""Exact bipartite color refinement for residual pair-cover canonicalization.

Color refinement is used only to split query permutation classes before the final
exact enumeration.  The canonical signature is still the lexicographic minimum
over every permutation remaining inside the refined classes, so refinement never
replaces the exact isomorphism test with a heuristic.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from math import factorial

from .core import FiniteTask, adaptive_minimum_resolution, bundle_resolves
from .isomorphism_quotient import (
    ResidualIsomorphismLimitError,
    ResidualIsomorphismWitness,
    ResidualPairCoverInstance,
    _cover_masks,
    _local_instance,
    _rows,
    verify_residual_pair_cover_isomorphism,
)


@dataclass(frozen=True)
class BipartiteColorRefinementReceipt:
    initial_query_color_class_sizes: tuple[int, ...]
    refined_query_color_class_sizes: tuple[int, ...]
    refined_row_color_class_sizes: tuple[int, ...]
    initial_permutation_count: int
    refined_permutation_count: int
    refinement_rounds: int
    stable: bool
    scope: str = "exact_isomorphism_invariant_bipartite_color_refinement"


@dataclass(frozen=True)
class RefinedCanonicalResidualCoverSignature:
    signature: tuple
    canonical_query_order: tuple[int, ...]
    query_color_class_sizes: tuple[int, ...]
    permutations_examined: int
    permutations_before_refinement: int
    refinement_rounds: int
    scope: str = "exact_refined_cost_preserving_residual_pair_cover_canonicalization"


@dataclass(frozen=True)
class RefinedIsomorphismQuotientFixedBudgetDecision:
    budget: int
    fixed_resolver_exists_within_budget: bool
    feasible_bundle: tuple[str, ...] | None
    branch_state_occurrences: int
    exact_residual_state_count: int
    isomorphism_class_count: int
    isomorphism_merge_count: int
    infeasible_isomorphism_cache_hits: int
    canonicalization_calls: int
    canonical_permutations_before_refinement: int
    canonical_permutations_examined: int
    first_merge_witness: ResidualIsomorphismWitness | None
    complete_search: bool
    scope: str = "exact_kernelized_fixed_cover_decision_with_color_refined_isomorphism_quotient"


@dataclass(frozen=True)
class RefinedIsomorphismQuotientAdaptiveGainAudit:
    adaptive_cost: int | None
    tested_fixed_budget: int | None
    strict_adaptive_gain: bool
    decision: RefinedIsomorphismQuotientFixedBudgetDecision | None
    interpretation: str


def _validate_instance(instance: ResidualPairCoverInstance) -> None:
    if type(instance.remaining_budget) is not int or instance.remaining_budget < 0:
        raise ValueError("remaining_budget must be a nonnegative integer")
    if any(type(cost) is not int or cost <= 0 for cost in instance.query_costs):
        raise ValueError("query costs must be positive integers")
    limit = 1 << len(instance.query_costs)
    if any(type(row) is not int or row < 0 or row >= limit for row in instance.separator_rows):
        raise ValueError("separator rows must be nonnegative bitmasks over the declared queries")


def _rank_colors(signatures) -> tuple[int, ...]:
    unique = {signature: rank for rank, signature in enumerate(sorted(set(signatures)))}
    return tuple(unique[signature] for signature in signatures)


def _class_sizes(colors: tuple[int, ...]) -> tuple[int, ...]:
    counts: dict[int, int] = {}
    for color in colors:
        counts[color] = counts.get(color, 0) + 1
    return tuple(counts[color] for color in sorted(counts))


def _permutation_count(class_sizes: tuple[int, ...]) -> int:
    value = 1
    for size in class_sizes:
        value *= factorial(size)
    return value


def refine_residual_incidence_colors(
    instance: ResidualPairCoverInstance,
) -> tuple[tuple[int, ...], tuple[int, ...], BipartiteColorRefinementReceipt]:
    """Refine query/obligation colors to the coarsest stable equitable partition.

    Initial query colors reproduce the invariant used by the original exact
    canonicalizer: acquisition cost plus the multiset of adjacent row degrees.
    Initial row colors use row degree.  Each round then refines rows by the
    multiset of neighboring query colors and queries by the multiset of updated
    row colors.  Previous colors are included, so partitions can only split.
    """
    _validate_instance(instance)
    qn = len(instance.query_costs)
    rows = instance.separator_rows
    rn = len(rows)
    row_degrees = tuple(row.bit_count() for row in rows)

    query_signatures = []
    for q in range(qn):
        adjacent_degrees = tuple(
            sorted(row_degrees[p] for p, row in enumerate(rows) if row & (1 << q))
        )
        query_signatures.append(
            (instance.query_costs[q], len(adjacent_degrees), adjacent_degrees)
        )
    query_colors = _rank_colors(tuple(query_signatures))
    initial_query_colors = query_colors
    row_colors = _rank_colors(tuple((degree,) for degree in row_degrees))

    max_rounds = qn + rn + 2
    rounds = 0
    stable = False
    while rounds < max_rounds:
        rounds += 1
        new_row_colors = _rank_colors(
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
        new_query_colors = _rank_colors(
            tuple(
                (
                    query_colors[q],
                    instance.query_costs[q],
                    tuple(
                        sorted(
                            new_row_colors[p]
                            for p, row in enumerate(rows)
                            if row & (1 << q)
                        )
                    ),
                )
                for q in range(qn)
            )
        )
        if new_query_colors == query_colors and new_row_colors == row_colors:
            stable = True
            query_colors, row_colors = new_query_colors, new_row_colors
            break
        query_colors, row_colors = new_query_colors, new_row_colors

    if not stable:
        raise ArithmeticError("bipartite color refinement failed to reach a fixed point")

    initial_sizes = _class_sizes(initial_query_colors)
    refined_sizes = _class_sizes(query_colors)
    row_sizes = _class_sizes(row_colors)
    receipt = BipartiteColorRefinementReceipt(
        initial_sizes,
        refined_sizes,
        row_sizes,
        _permutation_count(initial_sizes),
        _permutation_count(refined_sizes),
        rounds,
        True,
    )
    if receipt.refined_permutation_count > receipt.initial_permutation_count:
        raise ArithmeticError("color refinement enlarged the exact permutation search")
    return query_colors, row_colors, receipt


def refined_canonical_residual_pair_cover_signature(
    instance: ResidualPairCoverInstance,
    *,
    max_permutations: int = 100_000,
) -> RefinedCanonicalResidualCoverSignature:
    """Exact residual canonicalization after safe color refinement."""
    if type(max_permutations) is not int or max_permutations < 1:
        raise ValueError("max_permutations must be a positive integer")
    query_colors, _, refinement = refine_residual_incidence_colors(instance)
    groups_dict: dict[int, list[int]] = {}
    for q, color in enumerate(query_colors):
        groups_dict.setdefault(color, []).append(q)
    groups = tuple(tuple(groups_dict[color]) for color in sorted(groups_dict))

    if refinement.refined_permutation_count > max_permutations:
        raise ResidualIsomorphismLimitError(
            f"exact refined canonicalization needs {refinement.refined_permutation_count} query permutations, "
            f"exceeding cap {max_permutations}"
        )

    rows = instance.separator_rows
    best_signature = None
    best_order: tuple[int, ...] | None = None
    examined = 0
    families = tuple(tuple(permutations(group)) for group in groups)
    for selected in product(*families):
        order = tuple(q for group_order in selected for q in group_order)
        position = {old_q: new_q for new_q, old_q in enumerate(order)}
        transformed_rows = []
        for row in rows:
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
        examined += 1
        if best_signature is None or candidate < best_signature:
            best_signature = candidate
            best_order = order

    assert best_signature is not None and best_order is not None
    if examined != refinement.refined_permutation_count:
        raise ArithmeticError("refined canonicalizer did not enumerate its declared class product")
    return RefinedCanonicalResidualCoverSignature(
        best_signature,
        best_order,
        refinement.refined_query_color_class_sizes,
        examined,
        refinement.initial_permutation_count,
        refinement.refinement_rounds,
    )


def refined_residual_pair_cover_isomorphism_witness(
    left: ResidualPairCoverInstance,
    right: ResidualPairCoverInstance,
    *,
    max_permutations: int = 100_000,
) -> ResidualIsomorphismWitness | None:
    left_c = refined_canonical_residual_pair_cover_signature(
        left, max_permutations=max_permutations
    )
    right_c = refined_canonical_residual_pair_cover_signature(
        right, max_permutations=max_permutations
    )
    if left_c.signature != right_c.signature or len(left.query_costs) != len(right.query_costs):
        return None
    mapping = [-1] * len(left.query_costs)
    for left_q, right_q in zip(left_c.canonical_query_order, right_c.canonical_query_order):
        mapping[left_q] = right_q
    witness = ResidualIsomorphismWitness(left, right, tuple(mapping))
    if not verify_residual_pair_cover_isomorphism(witness):
        raise ArithmeticError("refined canonical signatures matched but explicit isomorphism failed")
    return witness


def refined_isomorphic_fixed_budget_cover_decision(
    task: FiniteTask,
    *,
    budget: int,
    max_classes: int = 200_000,
    max_permutations: int = 100_000,
) -> RefinedIsomorphismQuotientFixedBudgetDecision:
    """Exact kernelized fixed-cover decision using refined isomorphism classes."""
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(max_classes) is not int or max_classes < 1:
        raise ValueError("max_classes must be a positive integer")

    rows = _rows(task)
    if not rows:
        return RefinedIsomorphismQuotientFixedBudgetDecision(
            budget, True, (), 0, 0, 0, 0, 0, 0, 0, 0, None, True
        )
    if any(separators == 0 for _, _, separators in rows):
        return RefinedIsomorphismQuotientFixedBudgetDecision(
            budget, False, None, 0, 0, 0, 0, 0, 0, 0, 0, None, True
        )

    qn = len(task.queries)
    costs = tuple(query.cost for query in task.queries)
    covers = _cover_masks(task, rows)
    full_uncovered = (1 << len(rows)) - 1
    full_available = (1 << qn) - 1

    infeasible_classes: dict[tuple, ResidualPairCoverInstance] = {}
    exact_states: set[tuple[int, int, int]] = set()
    iso_classes: set[tuple] = set()
    occurrences = cache_hits = canonical_calls = 0
    permutations_before = permutations_examined = 0
    first_witness: ResidualIsomorphismWitness | None = None

    def reduce_state(uncovered: int, available: int, remaining: int):
        forced: list[str] = []
        while True:
            changed = False
            remove_queries = [
                q for q in range(qn)
                if available & (1 << q)
                and (costs[q] > remaining or not (covers[q] & uncovered))
            ]
            if remove_queries:
                for q in remove_queries:
                    available &= ~(1 << q)
                changed = True
            if uncovered == 0:
                return "resolved", uncovered, available, remaining, tuple(forced)

            active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]
            separator_sets = {p: rows[p][2] & available for p in active_pairs}
            if any(mask == 0 for mask in separator_sets.values()):
                return "infeasible", uncovered, available, remaining, tuple(forced)

            dominated_pairs: set[int] = set()
            for easy in active_pairs:
                for hard in active_pairs:
                    if easy == hard:
                        continue
                    easy_sep, hard_sep = separator_sets[easy], separator_sets[hard]
                    if not (hard_sep & ~easy_sep) and (hard_sep != easy_sep or hard < easy):
                        dominated_pairs.add(easy)
                        break
            if dominated_pairs:
                for p in dominated_pairs:
                    uncovered &= ~(1 << p)
                continue

            active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]
            unique_q = None
            for p in active_pairs:
                sep = rows[p][2] & available
                choices = tuple(q for q in range(qn) if sep & (1 << q))
                if not choices:
                    return "infeasible", uncovered, available, remaining, tuple(forced)
                if len(choices) == 1:
                    unique_q = choices[0]
                    break
            if unique_q is not None:
                q = unique_q
                forced.append(task.queries[q].name)
                uncovered &= ~covers[q]
                available &= ~(1 << q)
                remaining -= costs[q]
                continue

            available_queries = [q for q in range(qn) if available & (1 << q)]
            dominated_queries: set[int] = set()
            for q in available_queries:
                q_cover = covers[q] & uncovered
                for r in available_queries:
                    if q == r:
                        continue
                    r_cover = covers[r] & uncovered
                    if q_cover & ~r_cover or costs[r] > costs[q]:
                        continue
                    if costs[r] < costs[q] or r_cover != q_cover or r < q:
                        dominated_queries.add(q)
                        break
            if dominated_queries:
                for q in dominated_queries:
                    available &= ~(1 << q)
                changed = True
            if not changed:
                return "branch", uncovered, available, remaining, tuple(forced)

    def solve(uncovered: int, available: int, remaining: int):
        nonlocal occurrences, cache_hits, canonical_calls
        nonlocal permutations_before, permutations_examined, first_witness
        status, uncovered, available, remaining, forced = reduce_state(
            uncovered, available, remaining
        )
        if status == "resolved":
            return True, forced
        if status == "infeasible":
            return False, None

        occurrences += 1
        exact_states.add((uncovered, available, remaining))
        instance, _ = _local_instance(rows, costs, uncovered, available, remaining)
        canonical = refined_canonical_residual_pair_cover_signature(
            instance, max_permutations=max_permutations
        )
        canonical_calls += 1
        permutations_before += canonical.permutations_before_refinement
        permutations_examined += canonical.permutations_examined
        signature = canonical.signature
        iso_classes.add(signature)
        if len(iso_classes) > max_classes:
            raise ResidualIsomorphismLimitError(
                "refined isomorphism quotient exceeded its canonical-class cap"
            )

        representative = infeasible_classes.get(signature)
        if representative is not None:
            cache_hits += 1
            if first_witness is None and representative != instance:
                witness = refined_residual_pair_cover_isomorphism_witness(
                    representative, instance, max_permutations=max_permutations
                )
                if witness is None:
                    raise ArithmeticError("refined canonical cache hit lacked explicit isomorphism")
                first_witness = witness
            return False, None

        active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]
        def candidates(p: int):
            sep = rows[p][2] & available
            return tuple(q for q in range(qn) if sep & (1 << q))
        chosen = min(active_pairs, key=lambda p: (len(candidates(p)), p))
        for q in candidates(chosen):
            ok, child_bundle = solve(
                uncovered & ~covers[q],
                available & ~(1 << q),
                remaining - costs[q],
            )
            if ok:
                assert child_bundle is not None
                return True, forced + (task.queries[q].name,) + child_bundle
        infeasible_classes[signature] = instance
        return False, None

    exists, bundle = solve(full_uncovered, full_available, budget)
    if exists:
        assert bundle is not None
        lookup = {query.name: query.cost for query in task.queries}
        if len(set(bundle)) != len(bundle):
            raise ArithmeticError("refined isomorphism solver repeated a query")
        if sum(lookup[name] for name in bundle) > budget or not bundle_resolves(task, bundle):
            raise ArithmeticError("refined isomorphism solver returned invalid fixed bundle")

    exact_count, iso_count = len(exact_states), len(iso_classes)
    if iso_count > exact_count:
        raise ArithmeticError("refined isomorphism quotient created more classes than exact states")
    if first_witness is not None and not verify_residual_pair_cover_isomorphism(first_witness):
        raise ArithmeticError("stored refined isomorphism witness failed verification")
    return RefinedIsomorphismQuotientFixedBudgetDecision(
        budget, exists, bundle, occurrences, exact_count, iso_count,
        exact_count - iso_count, cache_hits, canonical_calls,
        permutations_before, permutations_examined, first_witness, True,
    )


def selected_policy_refined_isomorphism_gain_audit(
    task: FiniteTask,
    *,
    max_classes: int = 200_000,
    max_permutations: int = 100_000,
) -> RefinedIsomorphismQuotientAdaptiveGainAudit:
    adaptive = adaptive_minimum_resolution(task)
    ca = adaptive.minimum_worst_path_cost
    if ca is None:
        return RefinedIsomorphismQuotientAdaptiveGainAudit(
            None, None, False, None, "no resolving adaptive policy"
        )
    decision = refined_isomorphic_fixed_budget_cover_decision(
        task, budget=ca, max_classes=max_classes, max_permutations=max_permutations
    )
    strict = not decision.fixed_resolver_exists_within_budget
    return RefinedIsomorphismQuotientAdaptiveGainAudit(
        ca, ca, strict, decision,
        (
            f"color-refined exact quotient proves no fixed resolver of cost <= {ca}"
            if strict
            else f"color-refined exact quotient found a fixed resolver of cost <= {ca}"
        ),
    )
