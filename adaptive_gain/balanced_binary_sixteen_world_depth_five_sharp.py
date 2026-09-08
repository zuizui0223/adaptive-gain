"""Sharp exact-balanced binary adaptive-depth-five value at n=16.

Let D5(16)=max{C_F : C_A<=5} under globally exact 8/8 binary unit-cost
queries.  The existing (C_A,C_F)=(4,12) witness gives D5(16)>=12.  The sharp
fixed-cost cap is 13.  This module rules out C_F=13.

A minimum 13-query fixed resolver is the exact-balanced cap normal form, up to
world relabelling and outcome complementation.  Any declared query outside that
minimum bundle must be identity-safe; otherwise that query together with 11
members of the minimum bundle would resolve identity and hence every coarser
target partition with only 12 queries.  At n=16 there are exactly three such
external balanced cuts.

For each of their eight subsets, consider every 12-query fixed subfamily.  If a
12-query subfamily has exactly one unresolved world pair, then any target
partition with C_F>=13 must put that pair in different target classes.  Hence
any adaptive resolver must separate every such unique-witness pair.  Exact
Bellman DP shows that separating these mandatory pairs requires depth seven for
all eight external-cut subsets.  Therefore no C_A<=5 task can have C_F=13.

Thus D5(16)=12.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations

from .balanced_binary_depth_four_sharp import (
    _canonical_cap_cuts,
    _identity_safe_external_cuts,
)
from .balanced_binary_sixteen_world_depth_four import (
    audit_exact_balanced_sixteen_world_depth_four,
)


@dataclass(frozen=True)
class SixteenWorldDepthFiveSharpReceipt:
    world_count: int
    adaptive_depth_cap: int
    fixed_cost_cap: int
    safe_external_cut_count: int
    query_counts_by_safe_subset: tuple[int, ...]
    twelve_query_subfamily_counts: tuple[int, ...]
    unique_witness_pair_counts: tuple[int, ...]
    mandatory_pair_adaptive_depths: tuple[int, ...]
    constructive_adaptive_cost: int
    constructive_fixed_cost: int
    sharp_depth_five_value: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_depth_five_sharp_n16"


def _cut_mask(cut: frozenset[int]) -> int:
    return sum(1 << world for world in cut)


def _separator_mask_for_pair(
    pair: tuple[int, int], queries: tuple[frozenset[int], ...]
) -> int:
    left, right = pair
    out = 0
    for query_index, cut in enumerate(queries):
        if (left in cut) != (right in cut):
            out |= 1 << query_index
    return out


def _unique_witness_pairs_for_twelve_query_subfamilies(
    queries: tuple[frozenset[int], ...],
) -> tuple[tuple[int, int], ...]:
    """Pairs that uniquely witness failure of some exactly-12-query bundle."""
    pairs = tuple(combinations(range(16), 2))
    separator_masks = tuple(_separator_mask_for_pair(pair, queries) for pair in pairs)
    omitted_count = len(queries) - 12
    mandatory: set[tuple[int, int]] = set()
    for omitted in combinations(range(len(queries)), omitted_count):
        omitted_mask = sum(1 << index for index in omitted)
        unresolved = tuple(
            pair
            for pair, separating in zip(pairs, separator_masks)
            if separating & ~omitted_mask == 0
        )
        if len(unresolved) == 1:
            mandatory.add(unresolved[0])
    return tuple(sorted(mandatory))


def _minimum_depth_to_separate_pairs(
    queries: tuple[frozenset[int], ...],
    required_pairs: tuple[tuple[int, int], ...],
) -> int:
    full_state = (1 << 16) - 1
    query_masks = tuple(_cut_mask(cut) for cut in queries)

    @lru_cache(maxsize=None)
    def solve(state: int) -> int:
        if all(not (state & (1 << a) and state & (1 << b)) for a, b in required_pairs):
            return 0
        best = 99
        for query_mask in query_masks:
            one = state & query_mask
            zero = state & ~query_mask & full_state
            if not one or not zero:
                continue
            best = min(best, 1 + max(solve(one), solve(zero)))
        return best

    return solve(full_state)


@lru_cache(maxsize=1)
def audit_exact_balanced_sixteen_world_depth_five_sharp() -> SixteenWorldDepthFiveSharpReceipt:
    base = _canonical_cap_cuts(16)
    safe = _identity_safe_external_cuts(16)
    if len(base) != 13 or len(safe) != 3:
        raise ArithmeticError("sixteen-world cap/safe-cut normalization changed")

    query_counts: list[int] = []
    subfamily_counts: list[int] = []
    witness_counts: list[int] = []
    depths: list[int] = []
    for subset_mask in range(8):
        extras = tuple(safe[i] for i in range(3) if subset_mask & (1 << i))
        queries = base + extras
        required = _unique_witness_pairs_for_twelve_query_subfamilies(queries)
        query_counts.append(len(queries))
        subfamily_counts.append(len(tuple(combinations(range(len(queries)), 12))))
        witness_counts.append(len(required))
        depths.append(_minimum_depth_to_separate_pairs(queries, required))

    witness = audit_exact_balanced_sixteen_world_depth_four()
    expected_query_counts = (13, 14, 14, 15, 14, 15, 15, 16)
    expected_subfamilies = (13, 91, 91, 455, 91, 455, 455, 1820)
    expected_witness_counts = (13, 13, 28, 28, 28, 28, 43, 43)
    expected_depths = (7,) * 8
    theorem = (
        tuple(query_counts) == expected_query_counts
        and tuple(subfamily_counts) == expected_subfamilies
        and tuple(witness_counts) == expected_witness_counts
        and tuple(depths) == expected_depths
        and (witness.adaptive_cost, witness.fixed_cost) == (4, 12)
    )
    if not theorem:
        raise ArithmeticError("sixteen-world depth-five sharp audit failed")

    return SixteenWorldDepthFiveSharpReceipt(
        world_count=16,
        adaptive_depth_cap=5,
        fixed_cost_cap=13,
        safe_external_cut_count=3,
        query_counts_by_safe_subset=tuple(query_counts),
        twelve_query_subfamily_counts=tuple(subfamily_counts),
        unique_witness_pair_counts=tuple(witness_counts),
        mandatory_pair_adaptive_depths=tuple(depths),
        constructive_adaptive_cost=witness.adaptive_cost,
        constructive_fixed_cost=witness.fixed_cost,
        sharp_depth_five_value=12,
        theorem_holds=True,
    )
