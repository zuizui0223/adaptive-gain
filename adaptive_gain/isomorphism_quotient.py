"""Exact isomorphism quotient for small residual target-pair cover states.

The bounded fixed-cover continuation problem depends only on:

- the remaining integer budget;
- the costs of the available queries; and
- the bipartite incidence between still-uncovered target-pair obligations and
  those available queries.

World names, pair order, and query names are not part of that continuation
problem.  This module canonicalizes the weighted incidence structure under row
permutation and cost-preserving query permutation, then uses the canonical code
to share infeasible residual states across label-different but isomorphic search
histories.

Canonicalization is exact but factorial in unresolved query symmetries.  A hard
permutation cap raises rather than silently falling back to an unverified
quotient.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product
from math import factorial

from .core import FiniteTask, adaptive_minimum_resolution, bundle_resolves


class ResidualIsomorphismLimitError(RuntimeError):
    """Exact cost-preserving canonicalization exceeded its declared cap."""


@dataclass(frozen=True)
class ResidualPairCoverInstance:
    query_costs: tuple[int, ...]
    separator_rows: tuple[int, ...]
    remaining_budget: int


@dataclass(frozen=True)
class CanonicalResidualCoverSignature:
    signature: tuple
    canonical_query_order: tuple[int, ...]
    query_color_class_sizes: tuple[int, ...]
    permutations_examined: int
    scope: str = "exact_cost_preserving_query_permutation_and_obligation_row_permutation"


@dataclass(frozen=True)
class ResidualIsomorphismWitness:
    left: ResidualPairCoverInstance
    right: ResidualPairCoverInstance
    left_to_right_query: tuple[int, ...]
    scope: str = "explicit_weighted_pair_cover_incidence_isomorphism"


@dataclass(frozen=True)
class IsomorphismQuotientFixedBudgetDecision:
    budget: int
    fixed_resolver_exists_within_budget: bool
    feasible_bundle: tuple[str, ...] | None
    branch_state_occurrences: int
    exact_residual_state_count: int
    isomorphism_class_count: int
    isomorphism_merge_count: int
    infeasible_isomorphism_cache_hits: int
    canonicalization_calls: int
    canonical_permutations_examined: int
    first_merge_witness: ResidualIsomorphismWitness | None
    complete_search: bool
    scope: str = "exact_kernelized_fixed_cover_decision_with_small_state_isomorphism_quotient"


@dataclass(frozen=True)
class IsomorphismQuotientAdaptiveGainAudit:
    adaptive_cost: int | None
    tested_fixed_budget: int | None
    strict_adaptive_gain: bool
    decision: IsomorphismQuotientFixedBudgetDecision | None
    interpretation: str


def _validate_instance(instance: ResidualPairCoverInstance) -> None:
    if type(instance.remaining_budget) is not int or instance.remaining_budget < 0:
        raise ValueError("remaining_budget must be a nonnegative integer")
    if any(type(cost) is not int or cost <= 0 for cost in instance.query_costs):
        raise ValueError("query costs must be positive integers")
    limit = 1 << len(instance.query_costs)
    for row in instance.separator_rows:
        if type(row) is not int or row < 0 or row >= limit:
            raise ValueError("separator rows must be nonnegative bitmasks over the declared queries")


def canonical_residual_pair_cover_signature(
    instance: ResidualPairCoverInstance,
    *,
    max_permutations: int = 100_000,
) -> CanonicalResidualCoverSignature:
    """Return an exact canonical code for a small weighted pair-cover instance.

    Obligation rows are unlabeled and therefore sorted.  Query columns may be
    permuted only when structural invariants and acquisition cost agree.  The
    invariants merely reduce the enumeration: every true weighted-incidence
    isomorphism preserves them, so restricting to those color classes does not
    remove a valid isomorphism.
    """
    _validate_instance(instance)
    if type(max_permutations) is not int or max_permutations < 1:
        raise ValueError("max_permutations must be a positive integer")

    qn = len(instance.query_costs)
    rows = instance.separator_rows
    row_degrees = tuple(row.bit_count() for row in rows)

    colors: dict[tuple, list[int]] = {}
    for q in range(qn):
        covered_row_degrees = tuple(
            sorted(row_degrees[p] for p, row in enumerate(rows) if row & (1 << q))
        )
        color = (
            instance.query_costs[q],
            len(covered_row_degrees),
            covered_row_degrees,
        )
        colors.setdefault(color, []).append(q)

    groups = tuple(tuple(colors[color]) for color in sorted(colors))
    permutation_count = 1
    for group in groups:
        permutation_count *= factorial(len(group))
    if permutation_count > max_permutations:
        raise ResidualIsomorphismLimitError(
            f"exact residual canonicalization needs {permutation_count} query permutations, "
            f"exceeding cap {max_permutations}"
        )

    best_signature = None
    best_order: tuple[int, ...] | None = None
    examined = 0
    permutation_families = tuple(tuple(permutations(group)) for group in groups)
    for selected in product(*permutation_families):
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

    # product over an empty family yields one empty order, so this also covers
    # zero-query states.
    assert best_signature is not None and best_order is not None
    return CanonicalResidualCoverSignature(
        best_signature,
        best_order,
        tuple(len(group) for group in groups),
        examined,
    )


def residual_pair_cover_isomorphism_witness(
    left: ResidualPairCoverInstance,
    right: ResidualPairCoverInstance,
    *,
    max_permutations: int = 100_000,
) -> ResidualIsomorphismWitness | None:
    """Construct an explicit query bijection when two residual states are isomorphic."""
    left_c = canonical_residual_pair_cover_signature(
        left, max_permutations=max_permutations
    )
    right_c = canonical_residual_pair_cover_signature(
        right, max_permutations=max_permutations
    )
    if left_c.signature != right_c.signature:
        return None
    if len(left.query_costs) != len(right.query_costs):
        return None
    mapping = [-1] * len(left.query_costs)
    for left_q, right_q in zip(
        left_c.canonical_query_order, right_c.canonical_query_order
    ):
        mapping[left_q] = right_q
    witness = ResidualIsomorphismWitness(left, right, tuple(mapping))
    if not verify_residual_pair_cover_isomorphism(witness):
        raise ArithmeticError("canonical signatures matched but explicit isomorphism failed")
    return witness


def verify_residual_pair_cover_isomorphism(
    witness: ResidualIsomorphismWitness,
) -> bool:
    """Check an isomorphism witness without trusting canonicalization internals."""
    try:
        _validate_instance(witness.left)
        _validate_instance(witness.right)
    except ValueError:
        return False
    left, right = witness.left, witness.right
    if left.remaining_budget != right.remaining_budget:
        return False
    if len(left.query_costs) != len(right.query_costs):
        return False
    qn = len(left.query_costs)
    mapping = witness.left_to_right_query
    if len(mapping) != qn or set(mapping) != set(range(qn)):
        return False
    for left_q, right_q in enumerate(mapping):
        if left.query_costs[left_q] != right.query_costs[right_q]:
            return False

    transformed = []
    for row in left.separator_rows:
        mask = 0
        for left_q, right_q in enumerate(mapping):
            if row & (1 << left_q):
                mask |= 1 << right_q
        transformed.append(mask)
    return tuple(sorted(transformed)) == tuple(sorted(right.separator_rows))


def _rows(task: FiniteTask):
    rows = []
    for i, j in combinations(range(len(task.worlds)), 2):
        if task.worlds[i].target == task.worlds[j].target:
            continue
        separators = 0
        for q, query in enumerate(task.queries):
            if query.outcomes[i] != query.outcomes[j]:
                separators |= 1 << q
        rows.append((i, j, separators))
    return tuple(rows)


def _cover_masks(task: FiniteTask, rows):
    masks = []
    for q in range(len(task.queries)):
        mask = 0
        for p, (_, _, separators) in enumerate(rows):
            if separators & (1 << q):
                mask |= 1 << p
        masks.append(mask)
    return tuple(masks)


def _local_instance(rows, costs, uncovered: int, available: int, remaining: int):
    active_queries = tuple(q for q in range(len(costs)) if available & (1 << q))
    position = {q: local for local, q in enumerate(active_queries)}
    local_rows = []
    for p, (_, _, separators) in enumerate(rows):
        if not (uncovered & (1 << p)):
            continue
        local_mask = 0
        for q in active_queries:
            if separators & (1 << q):
                local_mask |= 1 << position[q]
        local_rows.append(local_mask)
    return (
        ResidualPairCoverInstance(
            tuple(costs[q] for q in active_queries),
            tuple(local_rows),
            remaining,
        ),
        active_queries,
    )


def isomorphic_fixed_budget_cover_decision(
    task: FiniteTask,
    *,
    budget: int,
    max_classes: int = 200_000,
    max_permutations: int = 100_000,
) -> IsomorphismQuotientFixedBudgetDecision:
    """Exact bounded fixed-cover decision with kernelization and isomorphic sharing.

    Only *infeasible* canonical classes are reused across differently labeled
    residual states.  Feasible states are solved in their current query labels so
    a constructive fixed bundle can always be returned without transporting a
    cached witness through an isomorphism.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(max_classes) is not int or max_classes < 1:
        raise ValueError("max_classes must be a positive integer")

    rows = _rows(task)
    if not rows:
        return IsomorphismQuotientFixedBudgetDecision(
            budget, True, (), 0, 0, 0, 0, 0, 0, 0, None, True
        )
    if any(separators == 0 for _, _, separators in rows):
        return IsomorphismQuotientFixedBudgetDecision(
            budget, False, None, 0, 0, 0, 0, 0, 0, 0, None, True
        )

    qn = len(task.queries)
    costs = tuple(query.cost for query in task.queries)
    covers = _cover_masks(task, rows)
    full_uncovered = (1 << len(rows)) - 1
    full_available = (1 << qn) - 1

    infeasible_classes: dict[tuple, ResidualPairCoverInstance] = {}
    exact_states: set[tuple[int, int, int]] = set()
    iso_classes: set[tuple] = set()
    occurrences = 0
    cache_hits = 0
    canonical_calls = 0
    permutations_examined = 0
    first_witness: ResidualIsomorphismWitness | None = None

    def reduce_state(uncovered: int, available: int, remaining: int):
        forced: list[str] = []
        while True:
            changed = False

            remove_queries = []
            for q in range(qn):
                if available & (1 << q) and (
                    costs[q] > remaining or not (covers[q] & uncovered)
                ):
                    remove_queries.append(q)
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
                easy_sep = separator_sets[easy]
                for hard in active_pairs:
                    if easy == hard:
                        continue
                    hard_sep = separator_sets[hard]
                    if hard_sep & ~easy_sep:
                        continue
                    if hard_sep != easy_sep or hard < easy:
                        dominated_pairs.add(easy)
                        break
            if dominated_pairs:
                for p in dominated_pairs:
                    uncovered &= ~(1 << p)
                continue

            active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]
            unique_q = None
            for p in active_pairs:
                separator_mask = rows[p][2] & available
                separators = tuple(q for q in range(qn) if separator_mask & (1 << q))
                if not separators:
                    return "infeasible", uncovered, available, remaining, tuple(forced)
                if len(separators) == 1:
                    unique_q = separators[0]
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
        nonlocal occurrences, cache_hits, canonical_calls, permutations_examined, first_witness
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
        canonical = canonical_residual_pair_cover_signature(
            instance, max_permutations=max_permutations
        )
        canonical_calls += 1
        permutations_examined += canonical.permutations_examined
        signature = canonical.signature
        iso_classes.add(signature)
        if len(iso_classes) > max_classes:
            raise ResidualIsomorphismLimitError(
                "isomorphism quotient exceeded its declared canonical-class cap"
            )

        representative = infeasible_classes.get(signature)
        if representative is not None:
            cache_hits += 1
            if first_witness is None and representative != instance:
                witness = residual_pair_cover_isomorphism_witness(
                    representative,
                    instance,
                    max_permutations=max_permutations,
                )
                if witness is None:
                    raise ArithmeticError("canonical cache hit lacked an explicit isomorphism")
                first_witness = witness
            return False, None

        active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]

        def candidates(p: int):
            separator_mask = rows[p][2] & available
            return tuple(q for q in range(qn) if separator_mask & (1 << q))

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
            raise ArithmeticError("isomorphism-quotient solver repeated a query")
        if sum(lookup[name] for name in bundle) > budget or not bundle_resolves(task, bundle):
            raise ArithmeticError("isomorphism-quotient solver returned an invalid fixed bundle")

    exact_count = len(exact_states)
    iso_count = len(iso_classes)
    if iso_count > exact_count:
        raise ArithmeticError("isomorphism quotient created more classes than exact residual states")
    if first_witness is not None and not verify_residual_pair_cover_isomorphism(first_witness):
        raise ArithmeticError("stored residual isomorphism witness failed independent verification")
    return IsomorphismQuotientFixedBudgetDecision(
        budget,
        exists,
        bundle,
        occurrences,
        exact_count,
        iso_count,
        exact_count - iso_count,
        cache_hits,
        canonical_calls,
        permutations_examined,
        first_witness,
        True,
    )


def selected_policy_isomorphism_quotient_gain_audit(
    task: FiniteTask,
    *,
    max_classes: int = 200_000,
    max_permutations: int = 100_000,
) -> IsomorphismQuotientAdaptiveGainAudit:
    adaptive = adaptive_minimum_resolution(task)
    ca = adaptive.minimum_worst_path_cost
    if ca is None:
        return IsomorphismQuotientAdaptiveGainAudit(
            None, None, False, None, "no resolving adaptive policy"
        )
    decision = isomorphic_fixed_budget_cover_decision(
        task,
        budget=ca,
        max_classes=max_classes,
        max_permutations=max_permutations,
    )
    strict = not decision.fixed_resolver_exists_within_budget
    return IsomorphismQuotientAdaptiveGainAudit(
        ca,
        ca,
        strict,
        decision,
        (
            f"isomorphism-quotient exact decision proves no fixed resolver of cost <= {ca}"
            if strict
            else f"isomorphism-quotient exact decision found a fixed resolver of cost <= {ca}"
        ),
    )
