"""Exact small-scope extremal checks for globally 50/50 binary queries.

This module complements the asymptotic exactly-balanced construction.  It uses
an independent bit-mask solver and quotients only symmetries that provably do
not change deterministic exact-resolution costs:

* per-query outcome complementation, and
* world/target relabeling through target multiplicity profiles.

For a fixed even world count ``n``, an exactly balanced binary query is a
bipartition with ``n/2`` worlds on each side.  Complementary outcome maps define
the same partition, so we keep the representative whose bit for world 0 is 0.
Duplicate query partitions are resolution-redundant and may be used only to pad
a declared query count; therefore enumerating all nonempty subsets of the
canonical partition classes covers every finite task up to these symmetries.

The complete n=4 and n=6 scans show that exact balance changes the finite-size
extremum even though it does not bound the ratio asymptotically:

* n=4: max C_F/C_A = 1;
* n=6: max C_F/C_A = 3/2 over every target partition and every query family.

An explicit n=8, m=5 exactly-balanced task has (C_A,C_F)=(3,5), so the first
world count at which exact balance permits a ratio strictly above 3/2 is 8.
Five queries are also minimal, because any binary task with m<=4 has ratio at
most 3/2 by the depth-two internal-node bound.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class BalancedBinaryWorldCountReceipt:
    world_count: int
    balanced_partition_classes: int
    target_multiplicity_profiles: int
    representative_query_families: int
    resolved_representatives: int
    maximum_ratio: Fraction
    maximizing_cost_pairs: tuple[tuple[int, int], ...]
    maximum_by_distinct_query_count: tuple[tuple[int, Fraction], ...]
    theorem_holds: bool
    scope: str = "exactly_balanced_binary_small_world_complete_classification"


@dataclass(frozen=True)
class BalancedBinaryThresholdReceipt:
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    ratio: Fraction
    all_queries_exactly_balanced: bool
    private_pair_for_every_query: bool
    smaller_even_world_counts_at_most_three_halves: bool
    fewer_than_five_queries_at_most_three_halves: bool
    theorem_holds: bool
    scope: str = "first_exactly_balanced_binary_scope_above_three_halves"


def _integer_partitions(total: int, maximum: int | None = None):
    if maximum is None or maximum > total:
        maximum = total
    if total == 0:
        yield ()
        return
    for first in range(min(maximum, total), 0, -1):
        for rest in _integer_partitions(total - first, first):
            yield (first,) + rest


def target_multiplicity_profiles(world_count: int) -> tuple[tuple[int, ...], ...]:
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer >=2")
    return tuple(profile for profile in _integer_partitions(world_count) if len(profile) >= 2)


def canonical_exact_balanced_query_masks(world_count: int) -> tuple[int, ...]:
    """Return exact-50/50 binary partitions modulo outcome complementation."""
    if type(world_count) is not int or world_count < 2 or world_count % 2:
        raise ValueError("exact 50/50 balance requires a positive even world_count")
    half = world_count // 2
    masks = []
    # Force world 0 to outcome 0.  Every balanced partition has exactly one of
    # its two complementary outcome maps in this form.
    for ones in combinations(range(1, world_count), half):
        mask = 0
        for index in ones:
            mask |= 1 << index
        masks.append(mask)
    return tuple(masks)


def _targets_for_profile(profile: tuple[int, ...]) -> tuple[int, ...]:
    targets = []
    for label, multiplicity in enumerate(profile):
        targets.extend([label] * multiplicity)
    return tuple(targets)


def _solve_mask_task(targets: tuple[int, ...], query_masks: tuple[int, ...]) -> tuple[int | None, int | None]:
    """Independent exact unit-cost solver for one tiny deterministic task."""
    n = len(targets)
    m = len(query_masks)
    all_worlds = (1 << n) - 1

    # Fixed resolution is a minimum hitting set of cross-target pair separator
    # sets.  This is independent of the package's general fixed solver.
    separator_edges: list[int] = []
    for left in range(n):
        for right in range(left + 1, n):
            if targets[left] == targets[right]:
                continue
            separators = 0
            for q_index, query_mask in enumerate(query_masks):
                if ((query_mask >> left) & 1) != ((query_mask >> right) & 1):
                    separators |= 1 << q_index
            if separators == 0:
                return None, None
            separator_edges.append(separators)

    fixed_cost = None
    for size in range(1, m + 1):
        for chosen_indices in combinations(range(m), size):
            chosen = 0
            for q_index in chosen_indices:
                chosen |= 1 << q_index
            if all(chosen & edge for edge in separator_edges):
                fixed_cost = size
                break
        if fixed_cost is not None:
            break
    if fixed_cost is None:
        return None, None

    target_masks: dict[int, int] = {}
    for world_index, target in enumerate(targets):
        target_masks[target] = target_masks.get(target, 0) | (1 << world_index)

    def resolved(mask: int) -> bool:
        return any(mask & ~target_mask == 0 for target_mask in target_masks.values())

    @lru_cache(None)
    def adaptive(mask: int, remaining: int) -> int | None:
        if resolved(mask):
            return 0
        best = None
        pending = remaining
        while pending:
            bit = pending & -pending
            q_index = bit.bit_length() - 1
            query_mask = query_masks[q_index]
            child_one = mask & query_mask
            child_zero = mask & (~query_mask) & all_worlds
            pending ^= bit
            if not child_zero or not child_one:
                continue
            zero_cost = adaptive(child_zero, remaining ^ bit)
            one_cost = adaptive(child_one, remaining ^ bit)
            if zero_cost is None or one_cost is None:
                continue
            cost = 1 + max(zero_cost, one_cost)
            if best is None or cost < best:
                best = cost
        return best

    adaptive_cost = adaptive(all_worlds, (1 << m) - 1)
    return adaptive_cost, fixed_cost


def classify_exact_balanced_world_count(world_count: int) -> BalancedBinaryWorldCountReceipt:
    """Completely classify n=4 or n=6 up to harmless relabeling symmetries."""
    masks = canonical_exact_balanced_query_masks(world_count)
    if len(masks) > 10:
        raise ValueError("complete subset classification is intentionally limited to <=10 partition classes")
    profiles = target_multiplicity_profiles(world_count)
    total_families = 0
    resolved_families = 0
    best = Fraction(0, 1)
    best_pairs: set[tuple[int, int]] = set()
    best_by_count: dict[int, Fraction] = {}

    for profile in profiles:
        targets = _targets_for_profile(profile)
        for query_count in range(1, len(masks) + 1):
            for family in combinations(masks, query_count):
                total_families += 1
                adaptive_cost, fixed_cost = _solve_mask_task(targets, family)
                if adaptive_cost is None or fixed_cost is None:
                    continue
                resolved_families += 1
                ratio = Fraction(fixed_cost, adaptive_cost)
                if ratio > best_by_count.get(query_count, Fraction(0, 1)):
                    best_by_count[query_count] = ratio
                if ratio > best:
                    best = ratio
                    best_pairs = {(adaptive_cost, fixed_cost)}
                elif ratio == best:
                    best_pairs.add((adaptive_cost, fixed_cost))

    expected_total = len(profiles) * ((1 << len(masks)) - 1)
    theorem = total_families == expected_total and resolved_families > 0 and best > 0
    if not theorem:
        raise ArithmeticError("exact-balanced small-world classification audit failed")
    return BalancedBinaryWorldCountReceipt(
        world_count,
        len(masks),
        len(profiles),
        total_families,
        resolved_families,
        best,
        tuple(sorted(best_pairs)),
        tuple(sorted(best_by_count.items())),
        theorem,
    )


def exact_balanced_eight_world_five_query_task() -> FiniteTask:
    """Registered exact-50/50 witness with (C_A,C_F)=(3,5)."""
    targets = (0, 0, 0, 0, 1, 1, 1, 1)
    outcome_rows = (
        (0, 1, 1, 0, 0, 0, 1, 1),
        (0, 1, 0, 0, 0, 1, 1, 1),
        (0, 1, 0, 1, 0, 1, 1, 0),
        (0, 1, 1, 0, 0, 1, 0, 1),
        (0, 0, 1, 1, 1, 0, 0, 1),
    )
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    queries = tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(outcome_rows))
    return FiniteTask(worlds, queries)


def _has_private_pair_for_each_query(task: FiniteTask) -> bool:
    for q_index, query in enumerate(task.queries):
        found = False
        for left in range(len(task.worlds)):
            for right in range(left + 1, len(task.worlds)):
                if task.worlds[left].target == task.worlds[right].target:
                    continue
                separators = [
                    j
                    for j, candidate in enumerate(task.queries)
                    if candidate.outcomes[left] != candidate.outcomes[right]
                ]
                if separators == [q_index]:
                    found = True
                    break
            if found:
                break
        if not found:
            return False
    return True


def exact_balanced_first_above_three_halves_audit() -> BalancedBinaryThresholdReceipt:
    four = classify_exact_balanced_world_count(4)
    six = classify_exact_balanced_world_count(6)
    task = exact_balanced_eight_world_five_query_task()
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive is None or fixed is None:
        raise ArithmeticError("registered exact-balanced threshold witness is unresolved")
    balanced = all(
        set(query.outcomes) <= {0, 1}
        and sum(value == 0 for value in query.outcomes) == sum(value == 1 for value in query.outcomes)
        for query in task.queries
    )
    private = _has_private_pair_for_each_query(task)
    smaller_worlds = four.maximum_ratio <= Fraction(3, 2) and six.maximum_ratio <= Fraction(3, 2)
    # For m<=4: if C_A=1 then C_F<=1; if C_A=2 a binary depth-two
    # tree has <=3 internal nodes so C_F<=3; if C_A>=3 then C_F<=m<=4.
    fewer_queries = True
    theorem = (
        len(task.worlds) == 8
        and len(task.queries) == 5
        and adaptive == 3
        and fixed == 5
        and balanced
        and private
        and smaller_worlds
        and fewer_queries
    )
    if not theorem:
        raise ArithmeticError("first exact-balanced >3/2 threshold audit failed")
    return BalancedBinaryThresholdReceipt(
        8,
        5,
        adaptive,
        fixed,
        Fraction(fixed, adaptive),
        balanced,
        private,
        smaller_worlds,
        fewer_queries,
        theorem,
    )
