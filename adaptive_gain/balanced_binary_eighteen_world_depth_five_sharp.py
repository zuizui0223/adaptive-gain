"""Sharp exact-balanced binary adaptive-depth-five value at n=18.

The fixed-cost cap is 15.  A cap-15 minimum resolver has the canonical
star--edge--star normal form, and every outside query must be one of the three
identity-safe balanced cuts.  Across all eight safe-cut subsets, the unique
witness pairs forced by the exactly-14-query subfamilies require adaptive depth
eight, so C_F=15 is impossible at depth five.

An explicit fourteen-query exact-9/9 family has a private-pair forest of type
(1,3,7,7).  Every query owns a query-unique cross-target private pair and an
explicit decision tree separates the resulting target classes in depth five.
Thus its exact cost pair is (C_A,C_F)=(5,14), and D5(18)=14.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations

from .balanced_binary_depth_four_sharp import (
    _canonical_cap_cuts,
    _identity_safe_external_cuts,
)
from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


_WITNESS_ONE_SIDES = (
    (0, 2, 4, 5, 6, 7, 8, 9, 10),
    (0, 3, 4, 5, 6, 7, 8, 9, 10),
    (0, 1, 2, 3, 4, 7, 8, 9, 10),
    (0, 6, 11, 12, 13, 14, 15, 16, 17),
    (0, 1, 2, 3, 4, 5, 6, 9, 10),
    (0, 1, 2, 3, 4, 5, 6, 7, 8),
    (0, 8, 11, 12, 13, 14, 15, 16, 17),
    (0, 10, 11, 12, 13, 14, 15, 16, 17),
    (0, 1, 2, 3, 11, 14, 15, 16, 17),
    (0, 4, 5, 6, 7, 8, 9, 10, 13),
    (0, 1, 2, 3, 11, 12, 13, 16, 17),
    (0, 1, 2, 3, 11, 12, 13, 14, 15),
    (0, 4, 5, 6, 7, 8, 9, 10, 15),
    (0, 4, 5, 6, 7, 8, 9, 10, 17),
)

_WITNESS_PRIVATE_PAIRS = (
    (2, 1),
    (1, 3),
    (5, 4),
    (5, 6),
    (4, 7),
    (4, 9),
    (7, 8),
    (9, 10),
    (12, 11),
    (12, 13),
    (11, 14),
    (11, 16),
    (14, 15),
    (16, 17),
)

_WITNESS_TARGETS = (0, 8, 0, 7, 0, 6, 5, 4, 3, 2, 1, 8, 14, 13, 12, 11, 10, 9)


@dataclass(frozen=True)
class EighteenWorldDepthFiveSharpReceipt:
    world_count: int
    adaptive_depth_cap: int
    fixed_cost_cap: int
    safe_external_cut_count: int
    fourteen_query_subfamily_counts: tuple[int, ...]
    cap_unique_witness_pair_counts: tuple[int, ...]
    cap_mandatory_pair_adaptive_depths: tuple[int, ...]
    witness_query_count: int
    witness_adaptive_cost: int
    witness_fixed_cost: int
    witness_component_sizes: tuple[int, ...]
    all_witness_queries_exactly_balanced: bool
    all_witness_private_pairs_unique: bool
    all_witness_private_pairs_cross_target: bool
    sharp_depth_five_value: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_depth_five_sharp_n18"


def exact_balanced_eighteen_world_fourteen_query_depth_five_task() -> FiniteTask:
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(_WITNESS_TARGETS))
    rows = tuple(
        tuple(1 if world in side else 0 for world in range(18))
        for side in _WITNESS_ONE_SIDES
    )
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def eighteen_world_fourteen_query_depth_five_private_pairs() -> tuple[tuple[int, int], ...]:
    return _WITNESS_PRIVATE_PAIRS


def eighteen_world_depth_five_policy() -> tuple:
    """Explicit policy; nodes are (query, one-branch, zero-branch)."""
    leaf = lambda *worlds: ("leaf", tuple(worlds))
    return (
        0,
        (
            2,
            (
                4,
                (5, leaf(0, 2, 4), (7, leaf(10), leaf(9))),
                (6, leaf(8), leaf(7)),
            ),
            (3, leaf(6), leaf(5)),
        ),
        (
            8,
            (
                10,
                (11, (1, leaf(3), leaf(1, 11)), (13, leaf(17), leaf(16))),
                (12, leaf(15), leaf(14)),
            ),
            (9, leaf(13), leaf(12)),
        ),
    )


def _policy_resolves(task: FiniteTask, policy: tuple) -> tuple[bool, int]:
    max_depth = 0
    def walk(node: tuple, active: tuple[int, ...], depth: int) -> bool:
        nonlocal max_depth
        if node[0] == "leaf":
            max_depth = max(max_depth, depth)
            return len({task.worlds[i].target for i in active}) <= 1
        query_index, one_node, zero_node = node
        query = task.queries[query_index]
        one = tuple(i for i in active if query.outcomes[i] == 1)
        zero = tuple(i for i in active if query.outcomes[i] == 0)
        if not one or not zero:
            return False
        return walk(one_node, one, depth + 1) and walk(zero_node, zero, depth + 1)
    return walk(policy, tuple(range(18)), 0), max_depth


def _separator_mask(pair: tuple[int, int], queries: tuple[frozenset[int], ...]) -> int:
    left, right = pair
    out = 0
    for query_index, cut in enumerate(queries):
        if (left in cut) != (right in cut):
            out |= 1 << query_index
    return out


def _unique_witness_pairs_for_fourteen_query_subfamilies(
    queries: tuple[frozenset[int], ...],
) -> tuple[tuple[int, int], ...]:
    pairs = tuple(combinations(range(18), 2))
    separator_masks = tuple(_separator_mask(pair, queries) for pair in pairs)
    omitted_count = len(queries) - 14
    mandatory: set[tuple[int, int]] = set()
    for omitted in combinations(range(len(queries)), omitted_count):
        omitted_mask = sum(1 << index for index in omitted)
        unresolved = tuple(
            pair for pair, separating in zip(pairs, separator_masks)
            if separating & ~omitted_mask == 0
        )
        if len(unresolved) == 1:
            mandatory.add(unresolved[0])
    return tuple(sorted(mandatory))


def _minimum_depth_to_separate_pairs(
    queries: tuple[frozenset[int], ...], required_pairs: tuple[tuple[int, int], ...]
) -> int:
    full_state = (1 << 18) - 1
    query_masks = tuple(sum(1 << world for world in cut) for cut in queries)
    @lru_cache(maxsize=None)
    def solve(state: int) -> int:
        if all(not (state & (1 << a) and state & (1 << b)) for a, b in required_pairs):
            return 0
        best = 99
        for query_mask in query_masks:
            one = state & query_mask
            zero = state & ~query_mask & full_state
            if one and zero:
                best = min(best, 1 + max(solve(one), solve(zero)))
        return best
    return solve(full_state)


@lru_cache(maxsize=1)
def audit_exact_balanced_eighteen_world_depth_five_sharp() -> EighteenWorldDepthFiveSharpReceipt:
    base = _canonical_cap_cuts(18)
    safe = _identity_safe_external_cuts(18)
    if len(base) != 15 or len(safe) != 3:
        raise ArithmeticError("eighteen-world cap/safe-cut normalization changed")

    subfamily_counts: list[int] = []
    witness_counts: list[int] = []
    cap_depths: list[int] = []
    for subset_mask in range(8):
        extras = tuple(safe[i] for i in range(3) if subset_mask & (1 << i))
        queries = base + extras
        required = _unique_witness_pairs_for_fourteen_query_subfamilies(queries)
        subfamily_counts.append(len(tuple(combinations(range(len(queries)), 14))))
        witness_counts.append(len(required))
        cap_depths.append(_minimum_depth_to_separate_pairs(queries, required))

    task = exact_balanced_eighteen_world_fourteen_query_depth_five_task()
    private_pairs = eighteen_world_fourteen_query_depth_five_private_pairs()
    balanced = all(
        sum(x == 0 for x in query.outcomes) == 9
        and sum(x == 1 for x in query.outcomes) == 9
        for query in task.queries
    )
    unique = True
    cross_target = True
    for query_index, (left, right) in enumerate(private_pairs):
        separating = tuple(
            index for index, query in enumerate(task.queries)
            if query.outcomes[left] != query.outcomes[right]
        )
        unique = unique and separating == (query_index,)
        cross_target = cross_target and task.worlds[left].target != task.worlds[right].target

    policy_ok, policy_depth = _policy_resolves(task, eighteen_world_depth_five_policy())
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost

    expected_subfamilies = (15, 120, 120, 680, 120, 680, 680, 3060)
    expected_witness_counts = (15, 15, 36, 36, 36, 36, 57, 57)
    expected_cap_depths = (8,) * 8
    theorem = (
        tuple(subfamily_counts) == expected_subfamilies
        and tuple(witness_counts) == expected_witness_counts
        and tuple(cap_depths) == expected_cap_depths
        and balanced and unique and cross_target and policy_ok and policy_depth == 5
        and adaptive == 5 and fixed == 14
    )
    if not theorem:
        raise ArithmeticError("eighteen-world depth-five sharp audit failed")

    return EighteenWorldDepthFiveSharpReceipt(
        world_count=18,
        adaptive_depth_cap=5,
        fixed_cost_cap=15,
        safe_external_cut_count=3,
        fourteen_query_subfamily_counts=tuple(subfamily_counts),
        cap_unique_witness_pair_counts=tuple(witness_counts),
        cap_mandatory_pair_adaptive_depths=tuple(cap_depths),
        witness_query_count=14,
        witness_adaptive_cost=adaptive,
        witness_fixed_cost=fixed,
        witness_component_sizes=(1, 3, 7, 7),
        all_witness_queries_exactly_balanced=balanced,
        all_witness_private_pairs_unique=unique,
        all_witness_private_pairs_cross_target=cross_target,
        sharp_depth_five_value=14,
        theorem_holds=True,
    )
