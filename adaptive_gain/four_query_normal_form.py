"""Exact finite classification for the 4-world / 4-binary-query balanced scope.

This extends the unique 3-query strict-gain normal form by one labeled unit-cost
binary query and asks whether any genuinely new irreducible strict-gain structure
appears. Exhaustive enumeration shows that it does not: every strict 4-query task
contains a strict 3-query deletion and belongs to one of three one-query extension
orbits.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

from .core import FiniteTask, Query, World, adaptive_gain_receipt
from .minimal_normal_form import (
    MINIMAL_STRICT_GAIN_SIGNATURE,
    canonical_minimal_separator_signature,
)


FOUR_QUERY_STRICT_EXTENSION_SIGNATURES = {
    (0, 3, 5, 9): "null_query_extension",
    (3, 3, 5, 9): "duplicate_terminal_extension",
    (3, 5, 9, 9): "duplicate_routing_extension",
}


@dataclass(frozen=True)
class FourQueryNormalFormReceipt:
    canonical_separator_signature: tuple[int, int, int, int]
    extension_class: str | None
    matches_strict_extension_normal_form: bool
    strict_three_query_deletion_count: int
    adaptive_cost: int | None
    fixed_cost: int | None
    exact_strict_gain: bool
    classification_agrees_with_exact_solver: bool
    scope: str = "four_world_two_plus_two_target_four_binary_unit_cost_queries"


@dataclass(frozen=True)
class FourQueryUniverseSummary:
    total_tasks: int
    unresolved_tasks: int
    cost_pair_counts: tuple[tuple[str, int], ...]
    strict_gain_tasks: int
    strict_extension_class_counts: tuple[tuple[str, int], ...]
    strict_deletion_count_distribution: tuple[tuple[int, int], ...]
    all_strict_tasks_have_minimal_strict_deletion: bool
    strict_gain_cost_pairs: tuple[tuple[int, int], ...]
    maximum_strict_cost_ratio: Fraction | None
    classification_disagreement_count: int
    scope: str = "complete_labeled_four_world_balanced_four_binary_unit_cost_query_universe"


def _validate_four_query_scope(task: FiniteTask) -> None:
    if len(task.worlds) != 4 or len(task.queries) != 4:
        raise ValueError("four-query normal form requires exactly four worlds and four queries")
    multiplicities: dict[object, int] = {}
    for world in task.worlds:
        multiplicities[world.target] = multiplicities.get(world.target, 0) + 1
    if sorted(multiplicities.values()) != [2, 2]:
        raise ValueError("target multiplicities must be exactly 2+2")
    if any(query.cost != 1 for query in task.queries):
        raise ValueError("four-query normal form requires unit query costs")
    if any(len(set(query.outcomes)) > 2 for query in task.queries):
        raise ValueError("four-query normal form requires binary-or-constant outcomes")


def _world_symmetries(task: FiniteTask):
    targets = tuple(world.target for world in task.worlds)
    return tuple(
        p
        for p in permutations(range(4))
        if all(
            (targets[i] == targets[j]) == (targets[p[i]] == targets[p[j]])
            for i in range(4)
            for j in range(4)
        )
    )


def _separator_mask(outcomes) -> int:
    cross_pairs = ((0, 2), (0, 3), (1, 2), (1, 3))
    mask = 0
    for bit, (i, j) in enumerate(cross_pairs):
        if outcomes[i] != outcomes[j]:
            mask |= 1 << bit
    return mask


def canonical_four_query_separator_signature(
    task: FiniteTask,
) -> tuple[int, int, int, int]:
    """Quotient target-equivalence-preserving world permutations and query order."""
    _validate_four_query_scope(task)
    representatives = []
    for permutation in _world_symmetries(task):
        masks = []
        for query in task.queries:
            transformed = tuple(query.outcomes[permutation[i]] for i in range(4))
            masks.append(_separator_mask(transformed))
        representatives.append(tuple(sorted(masks)))
    return min(representatives)


def _strict_three_query_deletion_count(task: FiniteTask) -> int:
    count = 0
    for omitted in range(4):
        subtask = FiniteTask(
            task.worlds,
            tuple(query for q, query in enumerate(task.queries) if q != omitted),
        )
        if canonical_minimal_separator_signature(subtask) == MINIMAL_STRICT_GAIN_SIGNATURE:
            count += 1
    return count


def four_query_normal_form_receipt(task: FiniteTask) -> FourQueryNormalFormReceipt:
    signature = canonical_four_query_separator_signature(task)
    extension = FOUR_QUERY_STRICT_EXTENSION_SIGNATURES.get(signature)
    predicted = extension is not None
    deletion_count = _strict_three_query_deletion_count(task)
    exact = adaptive_gain_receipt(task)
    return FourQueryNormalFormReceipt(
        signature,
        extension,
        predicted,
        deletion_count,
        exact.adaptive_cost,
        exact.fixed_cost,
        exact.strict_adaptive_gain,
        predicted == exact.strict_adaptive_gain,
    )


def enumerate_balanced_four_query_universe(
    *, max_tasks: int = 65_536
) -> FourQueryUniverseSummary:
    """Enumerate all 16^4 labeled binary query maps in the declared scope."""
    patterns = tuple(product((0, 1), repeat=4))
    total = len(patterns) ** 4
    if total > max_tasks:
        raise ValueError("declared exhaustive universe exceeds max_tasks")
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    cost_counts: dict[tuple[int | None, int | None], int] = {}
    extension_counts: dict[str, int] = {}
    deletion_counts: dict[int, int] = {}
    strict_pairs: set[tuple[int, int]] = set()
    strict = unresolved = disagreements = 0
    all_reducible = True
    max_ratio: Fraction | None = None

    for maps in product(patterns, repeat=4):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{q}", 1, outcomes) for q, outcomes in enumerate(maps)),
        )
        exact = adaptive_gain_receipt(task)
        pair = (exact.adaptive_cost, exact.fixed_cost)
        cost_counts[pair] = cost_counts.get(pair, 0) + 1
        if exact.adaptive_cost is None:
            unresolved += 1

        signature = canonical_four_query_separator_signature(task)
        extension = FOUR_QUERY_STRICT_EXTENSION_SIGNATURES.get(signature)
        predicted = extension is not None
        disagreements += int(predicted != exact.strict_adaptive_gain)
        if not exact.strict_adaptive_gain:
            continue

        strict += 1
        assert exact.adaptive_cost is not None and exact.fixed_cost is not None
        assert extension is not None
        strict_pairs.add((exact.adaptive_cost, exact.fixed_cost))
        ratio = Fraction(exact.fixed_cost, exact.adaptive_cost)
        max_ratio = ratio if max_ratio is None or ratio > max_ratio else max_ratio
        extension_counts[extension] = extension_counts.get(extension, 0) + 1
        deletions = _strict_three_query_deletion_count(task)
        deletion_counts[deletions] = deletion_counts.get(deletions, 0) + 1
        all_reducible = all_reducible and deletions > 0

    def pair_name(pair):
        return f"{pair[0]}:{pair[1]}"

    return FourQueryUniverseSummary(
        total,
        unresolved,
        tuple(sorted((pair_name(pair), count) for pair, count in cost_counts.items())),
        strict,
        tuple(sorted(extension_counts.items())),
        tuple(sorted(deletion_counts.items())),
        all_reducible,
        tuple(sorted(strict_pairs)),
        max_ratio,
        disagreements,
    )
