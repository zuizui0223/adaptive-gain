"""Exact classification for the 5-world / 2+3-target / 3-query scope.

This is the smallest declared scope in the repository where strict adaptive gain
can be irreducible with respect to deleting one world from the larger target
class.  Exhaustive enumeration of all 32^3 labeled binary query maps shows five
strict symmetry classes.  Four contain at least one strict balanced four-world
deletion; one class, with canonical separator signature ``(7, 28, 42)``, does
not.  The irreducible class has 288 labeled tasks and one symmetry orbit.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

from .core import FiniteTask, Query, World, adaptive_gain_receipt


FIVE_WORLD_STRICT_SIGNATURES: dict[tuple[int, int, int], str] = {
    (7, 9, 49): "two_strict_balanced_deletions_type_a",
    (7, 14, 54): "two_strict_balanced_deletions_type_b",
    (7, 27, 42): "one_strict_balanced_deletion_type_a",
    (14, 21, 45): "one_strict_balanced_deletion_type_b",
    (7, 28, 42): "irreducible_five_world_core",
}
FIVE_WORLD_IRREDUCIBLE_STRICT_GAIN_SIGNATURE = (7, 28, 42)


@dataclass(frozen=True)
class FiveWorldNormalFormReceipt:
    canonical_separator_signature: tuple[int, int, int]
    strict_class: str | None
    matches_declared_strict_normal_form: bool
    strict_balanced_four_world_deletion_count: int
    irreducible_against_majority_world_deletion: bool
    matches_unique_irreducible_normal_form: bool
    adaptive_cost: int | None
    fixed_cost: int | None
    exact_strict_gain: bool
    exact_irreducible_strict_gain: bool
    strict_classification_agrees_with_exact_solver: bool
    irreducible_classification_agrees_with_exact_solver: bool
    scope: str = "five_world_two_plus_three_target_three_binary_unit_cost_queries"


@dataclass(frozen=True)
class FiveWorldUniverseSummary:
    total_tasks: int
    unresolved_tasks: int
    cost_pair_counts: tuple[tuple[str, int], ...]
    strict_gain_tasks: int
    strict_signature_counts: tuple[tuple[tuple[int, int, int], int], ...]
    strict_class_counts: tuple[tuple[str, int], ...]
    strict_deletion_count_distribution: tuple[tuple[int, int], ...]
    irreducible_strict_gain_tasks: int
    irreducible_signature_counts: tuple[tuple[tuple[int, int, int], int], ...]
    irreducible_symmetry_orbit_count: int
    strict_gain_cost_pairs: tuple[tuple[int, int], ...]
    maximum_strict_cost_ratio: Fraction | None
    strict_classification_disagreement_count: int
    irreducible_classification_disagreement_count: int
    scope: str = "complete_labeled_five_world_two_plus_three_target_three_binary_unit_cost_query_universe"


def _target_blocks(task: FiniteTask) -> tuple[tuple[int, ...], tuple[int, ...]]:
    blocks: dict[object, list[int]] = {}
    for i, world in enumerate(task.worlds):
        blocks.setdefault(world.target, []).append(i)
    sizes = sorted(len(indices) for indices in blocks.values())
    if sizes != [2, 3]:
        raise ValueError("target multiplicities must be exactly 2+3")
    small = next(tuple(indices) for indices in blocks.values() if len(indices) == 2)
    large = next(tuple(indices) for indices in blocks.values() if len(indices) == 3)
    return small, large


def _validate_five_world_scope(task: FiniteTask) -> None:
    if len(task.worlds) != 5 or len(task.queries) != 3:
        raise ValueError("five-world normal form requires exactly five worlds and three queries")
    _target_blocks(task)
    if any(query.cost != 1 for query in task.queries):
        raise ValueError("five-world normal form requires unit query costs")
    if any(len(set(query.outcomes)) > 2 for query in task.queries):
        raise ValueError("five-world normal form requires binary-or-constant outcomes")


def _separator_mask_on_canonical_order(outcomes: tuple[object, ...]) -> int:
    # Canonical positions 0,1 are the size-2 target class; 2,3,4 are size-3.
    cross_pairs = ((0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4))
    mask = 0
    for bit, (i, j) in enumerate(cross_pairs):
        if outcomes[i] != outcomes[j]:
            mask |= 1 << bit
    return mask


def canonical_five_world_separator_signature(task: FiniteTask) -> tuple[int, int, int]:
    """Quotient within-target world permutations and query order exactly.

    Independent binary outcome flips need no explicit enumeration because pair
    separation depends only on equality versus inequality of outcomes.
    """
    _validate_five_world_scope(task)
    small, large = _target_blocks(task)
    representatives = []
    for small_order in permutations(small):
        for large_order in permutations(large):
            order = small_order + large_order
            masks = []
            for query in task.queries:
                transformed = tuple(query.outcomes[i] for i in order)
                masks.append(_separator_mask_on_canonical_order(transformed))
            representatives.append(tuple(sorted(masks)))
    return min(representatives)


def _strict_balanced_four_world_deletion_count(task: FiniteTask) -> int:
    """Count majority-class world deletions that retain strict adaptive gain."""
    _validate_five_world_scope(task)
    _, large = _target_blocks(task)
    count = 0
    for omitted in large:
        keep = tuple(i for i in range(5) if i != omitted)
        subtask = FiniteTask(
            tuple(task.worlds[i] for i in keep),
            tuple(
                Query(query.name, query.cost, tuple(query.outcomes[i] for i in keep))
                for query in task.queries
            ),
        )
        count += int(adaptive_gain_receipt(subtask).strict_adaptive_gain)
    return count


def five_world_irreducible_standard_task() -> FiniteTask:
    """One representative of the unique irreducible five-world strict-gain orbit."""
    worlds = (
        World("a0", 0), World("a1", 0),
        World("b0", 1), World("b1", 1), World("b2", 1),
    )
    return FiniteTask(
        worlds,
        (
            Query("q_terminal_a", 1, (0, 1, 1, 1, 1)),
            Query("q_route_left", 1, (0, 1, 0, 0, 1)),
            Query("q_route_right", 1, (0, 1, 0, 1, 0)),
        ),
    )


def five_world_normal_form_receipt(task: FiniteTask) -> FiveWorldNormalFormReceipt:
    signature = canonical_five_world_separator_signature(task)
    strict_class = FIVE_WORLD_STRICT_SIGNATURES.get(signature)
    predicted_strict = strict_class is not None
    deletion_count = _strict_balanced_four_world_deletion_count(task)
    exact = adaptive_gain_receipt(task)
    exact_irreducible = exact.strict_adaptive_gain and deletion_count == 0
    predicted_irreducible = signature == FIVE_WORLD_IRREDUCIBLE_STRICT_GAIN_SIGNATURE
    return FiveWorldNormalFormReceipt(
        signature,
        strict_class,
        predicted_strict,
        deletion_count,
        deletion_count == 0,
        predicted_irreducible,
        exact.adaptive_cost,
        exact.fixed_cost,
        exact.strict_adaptive_gain,
        exact_irreducible,
        predicted_strict == exact.strict_adaptive_gain,
        predicted_irreducible == exact_irreducible,
    )


def five_world_irreducible_raw_symmetry_orbit_size() -> int:
    """Count labeled binary query triples in the standard form's declared orbit."""
    task = five_world_irreducible_standard_task()
    small, large = _target_blocks(task)
    raw = set()
    maps = tuple(query.outcomes for query in task.queries)
    for small_order in permutations(small):
        for large_order in permutations(large):
            order = small_order + large_order
            world_relabelled = tuple(tuple(q[i] for i in order) for q in maps)
            for query_order in permutations(range(3)):
                ordered = tuple(world_relabelled[q] for q in query_order)
                for flips in product((0, 1), repeat=3):
                    raw.add(
                        tuple(
                            tuple(1 - value for value in outcomes) if flip else outcomes
                            for outcomes, flip in zip(ordered, flips)
                        )
                    )
    return len(raw)


def enumerate_two_plus_three_three_query_universe(
    *, max_tasks: int = 32_768
) -> FiveWorldUniverseSummary:
    """Enumerate all 32^3 labeled binary query maps in the declared scope."""
    patterns = tuple(product((0, 1), repeat=5))
    total = len(patterns) ** 3
    if total > max_tasks:
        raise ValueError("declared exhaustive universe exceeds max_tasks")
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1), World("w4", 1),
    )
    cost_counts: dict[tuple[int | None, int | None], int] = {}
    strict_signature_counts: dict[tuple[int, int, int], int] = {}
    strict_class_counts: dict[str, int] = {}
    deletion_counts: dict[int, int] = {}
    irreducible_signature_counts: dict[tuple[int, int, int], int] = {}
    strict_pairs: set[tuple[int, int]] = set()
    strict = unresolved = irreducible = 0
    strict_disagreements = irreducible_disagreements = 0
    max_ratio: Fraction | None = None

    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{q}", 1, outcomes) for q, outcomes in enumerate(maps)),
        )
        exact = adaptive_gain_receipt(task)
        pair = (exact.adaptive_cost, exact.fixed_cost)
        cost_counts[pair] = cost_counts.get(pair, 0) + 1
        if exact.adaptive_cost is None:
            unresolved += 1

        signature = canonical_five_world_separator_signature(task)
        strict_class = FIVE_WORLD_STRICT_SIGNATURES.get(signature)
        predicted_strict = strict_class is not None
        strict_disagreements += int(predicted_strict != exact.strict_adaptive_gain)

        if not exact.strict_adaptive_gain:
            # A non-strict task cannot be an irreducible strict task.
            irreducible_disagreements += int(
                signature == FIVE_WORLD_IRREDUCIBLE_STRICT_GAIN_SIGNATURE
            )
            continue

        strict += 1
        assert exact.adaptive_cost is not None and exact.fixed_cost is not None
        assert strict_class is not None
        strict_pairs.add((exact.adaptive_cost, exact.fixed_cost))
        ratio = Fraction(exact.fixed_cost, exact.adaptive_cost)
        max_ratio = ratio if max_ratio is None or ratio > max_ratio else max_ratio
        strict_signature_counts[signature] = strict_signature_counts.get(signature, 0) + 1
        strict_class_counts[strict_class] = strict_class_counts.get(strict_class, 0) + 1

        deletions = _strict_balanced_four_world_deletion_count(task)
        deletion_counts[deletions] = deletion_counts.get(deletions, 0) + 1
        exact_irreducible = deletions == 0
        predicted_irreducible = signature == FIVE_WORLD_IRREDUCIBLE_STRICT_GAIN_SIGNATURE
        irreducible_disagreements += int(predicted_irreducible != exact_irreducible)
        if exact_irreducible:
            irreducible += 1
            irreducible_signature_counts[signature] = (
                irreducible_signature_counts.get(signature, 0) + 1
            )

    def pair_name(pair):
        return f"{pair[0]}:{pair[1]}"

    return FiveWorldUniverseSummary(
        total,
        unresolved,
        tuple(sorted((pair_name(pair), count) for pair, count in cost_counts.items())),
        strict,
        tuple(sorted(strict_signature_counts.items())),
        tuple(sorted(strict_class_counts.items())),
        tuple(sorted(deletion_counts.items())),
        irreducible,
        tuple(sorted(irreducible_signature_counts.items())),
        len(irreducible_signature_counts),
        tuple(sorted(strict_pairs)),
        max_ratio,
        strict_disagreements,
        irreducible_disagreements,
    )
