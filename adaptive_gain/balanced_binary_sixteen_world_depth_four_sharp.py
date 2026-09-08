"""Sharp exact-balanced binary depth-four value at n=16.

The generic fixed-cost cap gives D4(16)<=13.  The identity-safe-cut reduction
from the n=12/n=14 sharp audit leaves exactly three possible external balanced
cuts outside a normalized 13-query cap bundle.  Exhausting all eight subsets
of those cuts and every depth-at-most-four leaf partition finds no partition
retaining fixed minimum 13.  The explicit twelve-query witness therefore gives
D4(16)=12.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .balanced_binary_depth_four_sharp import (
    _canonical_cap_cuts,
    _cap_retaining_partition_count,
    _identity_safe_external_cuts,
    _reachable_leaf_partitions,
)
from .balanced_binary_sixteen_world_depth_four import (
    audit_exact_balanced_sixteen_world_depth_four,
)


@dataclass(frozen=True)
class SixteenWorldDepthFourSharpReceipt:
    world_count: int
    fixed_cost_cap: int
    safe_external_cut_count: int
    reachable_partition_counts_by_safe_subset: tuple[int, ...]
    cap_retaining_partition_counts_by_safe_subset: tuple[int, ...]
    constructive_adaptive_cost: int
    constructive_fixed_cost: int
    sharp_depth_four_value: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_depth_four_sharp_n16"


@lru_cache(maxsize=1)
def audit_exact_balanced_sixteen_world_depth_four_sharp() -> SixteenWorldDepthFourSharpReceipt:
    world_count = 16
    base = _canonical_cap_cuts(world_count)
    safe = _identity_safe_external_cuts(world_count)
    if len(base) != 13 or len(safe) != 3:
        raise ArithmeticError("sixteen-world cap normalization changed")

    reachable_counts: list[int] = []
    retaining_counts: list[int] = []
    for subset_mask in range(1 << len(safe)):
        extras = tuple(safe[i] for i in range(len(safe)) if subset_mask & (1 << i))
        queries = base + extras
        partitions = _reachable_leaf_partitions(world_count, queries, depth=4)
        reachable_counts.append(len(partitions))
        retaining_counts.append(
            _cap_retaining_partition_count(world_count, queries, partitions)
        )

    if any(retaining_counts):
        raise ArithmeticError("found a sixteen-world depth-four partition retaining cap 13")

    witness = audit_exact_balanced_sixteen_world_depth_four()
    theorem = (
        witness.adaptive_cost == 4
        and witness.fixed_cost == 12
        and tuple(reachable_counts)
        == (81188, 105064, 133669, 171496, 133669, 171496, 219882, 279840)
        and tuple(retaining_counts) == (0,) * 8
    )
    if not theorem:
        raise ArithmeticError("sixteen-world sharp depth-four audit failed")

    return SixteenWorldDepthFourSharpReceipt(
        world_count=16,
        fixed_cost_cap=13,
        safe_external_cut_count=3,
        reachable_partition_counts_by_safe_subset=tuple(reachable_counts),
        cap_retaining_partition_counts_by_safe_subset=tuple(retaining_counts),
        constructive_adaptive_cost=witness.adaptive_cost,
        constructive_fixed_cost=witness.fixed_cost,
        sharp_depth_four_value=12,
        theorem_holds=True,
    )
