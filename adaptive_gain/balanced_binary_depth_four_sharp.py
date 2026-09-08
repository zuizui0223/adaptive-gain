"""Sharp exact-balanced binary depth-four values at n=12 and n=14.

Let D4(n)=max{C_F : C_A<=4} for unit-cost binary queries that are globally
exact 50/50 on n represented worlds.  The constructive frontier already gives
D4(12)>=8 and D4(14)>=10.  This module closes the one-query gaps.

If C_F=n-3, choose a minimum fixed resolver B.  The sharp fixed-cost-cap
normal form gives a three-component private-pair forest with component sizes
(n/2-1,2,n/2-1); exact balance then forces the canonical star--edge--star
query matrix, up to world relabelling and outcome complementation.

Any declared query outside B must remain safe after refining targets all the
way to identity targets: otherwise B plus that one query would contain an
(n-4)-query identity resolver and hence an (n-4)-query resolver for the
original targets, contradicting C_F=n-3.  Exhausting all balanced cuts leaves
only three safe external cuts at n=12 and again only three at n=14.

For every one of the 2^3 subsets of those safe cuts, we exhaust every leaf
partition reachable by a depth-at-most-four policy.  A hypothetical original
target partition can be replaced by the policy's leaf partition: leaves refine
targets, B resolves identity and hence the leaf partition, and every registered
private edge must still cross leaves.  We then test whether any reachable leaf
partition retains fixed minimum n-3.  None does.

Therefore D4(12)=8 and D4(14)=10.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations

from .balanced_binary_depth_four_frontier import (
    exact_balanced_fourteen_world_ten_query_depth_four_task,
    exact_balanced_twelve_world_eight_query_depth_four_task,
)
from .balanced_binary_fixed_cost_cap import (
    exact_balanced_binary_fixed_cost_cap_private_pairs,
    exact_balanced_binary_fixed_cost_cap_witness,
)
from .core import adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class DepthFourSharpSizeReceipt:
    world_count: int
    fixed_cost_cap: int
    safe_external_cut_count: int
    reachable_partition_counts_by_safe_subset: tuple[int, ...]
    cap_retaining_partition_counts_by_safe_subset: tuple[int, ...]
    constructive_adaptive_cost: int
    constructive_fixed_cost: int
    sharp_depth_four_value: int
    theorem_holds: bool


@dataclass(frozen=True)
class DepthFourSharpReceipt:
    twelve_world: DepthFourSharpSizeReceipt
    fourteen_world: DepthFourSharpSizeReceipt
    theorem_holds: bool
    scope: str = "exact_balanced_binary_depth_four_sharp_n12_n14"


def _canon_cut(cut: frozenset[int], world_count: int) -> frozenset[int]:
    full = frozenset(range(world_count))
    comp = full - cut
    return min(cut, comp, key=lambda side: tuple(sorted(side)))


def _canonical_cap_cuts(world_count: int) -> tuple[frozenset[int], ...]:
    task = exact_balanced_binary_fixed_cost_cap_witness(world_count)
    return tuple(
        _canon_cut(
            frozenset(i for i, outcome in enumerate(query.outcomes) if outcome == 1),
            world_count,
        )
        for query in task.queries
    )


def _balanced_cut_universe(world_count: int) -> tuple[frozenset[int], ...]:
    half = world_count // 2
    # Quotient outcome complementation by requiring world 0 on the chosen side.
    return tuple(frozenset(c) for c in combinations(range(world_count), half) if 0 in c)


def _world_pairs(world_count: int) -> tuple[tuple[int, int], ...]:
    return tuple(combinations(range(world_count), 2))


def _separator_mask(
    cut: frozenset[int],
    pairs: tuple[tuple[int, int], ...],
) -> int:
    mask = 0
    for index, (left, right) in enumerate(pairs):
        if (left in cut) != (right in cut):
            mask |= 1 << index
    return mask


def _identity_safe_external_cuts(world_count: int) -> tuple[frozenset[int], ...]:
    """Cuts that do not lower the canonical identity fixed minimum n-3."""
    cap_cuts = _canonical_cap_cuts(world_count)
    cap = world_count - 3
    pairs = _world_pairs(world_count)
    full_pair_mask = (1 << len(pairs)) - 1
    base_masks = tuple(_separator_mask(cut, pairs) for cut in cap_cuts)
    base_set = set(cap_cuts)

    # The base bundle has identity fixed minimum cap: every query owns a
    # registered Hamming-1 private pair.
    if len(cap_cuts) != cap:
        raise ArithmeticError("canonical cap bundle has wrong size")
    for omitted in range(cap):
        union = 0
        for index, mask in enumerate(base_masks):
            if index != omitted:
                union |= mask
        if union == full_pair_mask:
            raise ArithmeticError("canonical cap query unexpectedly redundant for identity")

    safe: list[frozenset[int]] = []
    for raw_cut in _balanced_cut_universe(world_count):
        cut = _canon_cut(raw_cut, world_count)
        if cut in base_set:
            continue
        external_mask = _separator_mask(cut, pairs)

        # If fixed cost falls below cap, pad a smaller resolver to cap-1.
        # Since B alone needs cap queries, every cap-1 resolver in B+{r}
        # must contain r and omit exactly two members of B.
        lowers = False
        for first, second in combinations(range(cap), 2):
            union = external_mask
            for index, mask in enumerate(base_masks):
                if index != first and index != second:
                    union |= mask
            if union == full_pair_mask:
                lowers = True
                break
        if not lowers:
            safe.append(cut)
    return tuple(sorted(set(safe), key=lambda side: tuple(sorted(side))))


def _reachable_leaf_partitions(
    world_count: int,
    queries: tuple[frozenset[int], ...],
    depth: int = 4,
) -> frozenset[tuple[int, ...]]:
    full_state = (1 << world_count) - 1
    query_masks = tuple(sum(1 << i for i in cut) for cut in queries)

    @lru_cache(maxsize=None)
    def rec(state: int, remaining: int) -> frozenset[tuple[int, ...]]:
        out: set[tuple[int, ...]] = {(state,)}
        if remaining == 0 or state & (state - 1) == 0:
            return frozenset(out)
        for query_mask in query_masks:
            left = state & query_mask
            right = state & (~query_mask) & full_state
            if not left or not right:
                continue
            for left_partition in rec(left, remaining - 1):
                for right_partition in rec(right, remaining - 1):
                    out.add(tuple(sorted(left_partition + right_partition)))
        return frozenset(out)

    return rec(full_state, depth)


def _block_map(partition: tuple[int, ...], world_count: int) -> tuple[int, ...]:
    blocks = [-1] * world_count
    for block_index, block_mask in enumerate(partition):
        for world in range(world_count):
            if block_mask & (1 << world):
                blocks[world] = block_index
    if any(block < 0 for block in blocks):
        raise ArithmeticError("partition does not cover all worlds")
    return tuple(blocks)


def _cap_retaining_partition_count(
    world_count: int,
    queries: tuple[frozenset[int], ...],
    partitions: frozenset[tuple[int, ...]],
) -> int:
    """Count depth-four leaf partitions whose fixed minimum stays n-3."""
    cap = world_count - 3
    private_pairs = exact_balanced_binary_fixed_cost_cap_private_pairs(world_count)
    world_pairs = _world_pairs(world_count)

    separator_masks: dict[tuple[int, int], int] = {}
    for pair in world_pairs:
        mask = 0
        for query_index, cut in enumerate(queries):
            if (pair[0] in cut) != (pair[1] in cut):
                mask |= 1 << query_index
        separator_masks[pair] = mask

    # To decide whether fixed cost is <=cap-1, it suffices to test all
    # exactly-(cap-1)-query subsets (smaller resolvers can be padded).
    omit_count = len(queries) - (cap - 1)
    omission_unresolved_pairs: list[tuple[tuple[int, int], ...]] = []
    for omitted_indices in combinations(range(len(queries)), omit_count):
        omitted_mask = sum(1 << index for index in omitted_indices)
        unresolved = tuple(
            pair
            for pair, separating in separator_masks.items()
            if separating & ~omitted_mask == 0
        )
        omission_unresolved_pairs.append(unresolved)

    retaining = 0
    for partition in partitions:
        blocks = _block_map(partition, world_count)

        # In the normalized cap bundle, each registered private edge is
        # cross-target.  A policy leaf partition refines targets, so every one
        # of those edges must cross leaves as well.
        if any(blocks[left] == blocks[right] for left, right in private_pairs):
            continue

        fixed_is_cap = True
        for unresolved_pairs in omission_unresolved_pairs:
            # The kept cap-1 queries resolve the leaf partition iff every pair
            # they fail to separate lies inside a single leaf block.
            if not any(blocks[left] != blocks[right] for left, right in unresolved_pairs):
                fixed_is_cap = False
                break
        if fixed_is_cap:
            retaining += 1
    return retaining


@lru_cache(maxsize=None)
def _audit_size(world_count: int) -> DepthFourSharpSizeReceipt:
    if world_count not in (12, 14):
        raise ValueError("sharp depth-four audit is registered only for n=12 and n=14")

    base = _canonical_cap_cuts(world_count)
    safe = _identity_safe_external_cuts(world_count)
    if len(safe) != 3:
        raise ArithmeticError("identity-safe external-cut count changed")

    reachable_counts: list[int] = []
    retaining_counts: list[int] = []
    for subset_mask in range(1 << len(safe)):
        extras = tuple(safe[i] for i in range(len(safe)) if subset_mask & (1 << i))
        query_family = base + extras
        partitions = _reachable_leaf_partitions(world_count, query_family, depth=4)
        reachable_counts.append(len(partitions))
        retaining_counts.append(
            _cap_retaining_partition_count(world_count, query_family, partitions)
        )

    if any(retaining_counts):
        raise ArithmeticError("found a depth-four leaf partition retaining the n-3 cap")

    witness = (
        exact_balanced_twelve_world_eight_query_depth_four_task()
        if world_count == 12
        else exact_balanced_fourteen_world_ten_query_depth_four_task()
    )
    adaptive = adaptive_minimum_resolution(witness).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(witness).minimum_cost
    expected_fixed = world_count - 4
    theorem = adaptive == 4 and fixed == expected_fixed and not any(retaining_counts)
    if not theorem:
        raise ArithmeticError("sharp depth-four finite-size audit failed")

    return DepthFourSharpSizeReceipt(
        world_count=world_count,
        fixed_cost_cap=world_count - 3,
        safe_external_cut_count=len(safe),
        reachable_partition_counts_by_safe_subset=tuple(reachable_counts),
        cap_retaining_partition_counts_by_safe_subset=tuple(retaining_counts),
        constructive_adaptive_cost=adaptive,
        constructive_fixed_cost=fixed,
        sharp_depth_four_value=expected_fixed,
        theorem_holds=True,
    )


@lru_cache(maxsize=1)
def audit_exact_balanced_depth_four_sharp() -> DepthFourSharpReceipt:
    twelve = _audit_size(12)
    fourteen = _audit_size(14)
    theorem = (
        twelve.sharp_depth_four_value == 8
        and fourteen.sharp_depth_four_value == 10
        and twelve.theorem_holds
        and fourteen.theorem_holds
    )
    if not theorem:
        raise ArithmeticError("combined depth-four sharp audit failed")
    return DepthFourSharpReceipt(
        twelve_world=twelve,
        fourteen_world=fourteen,
        theorem_holds=True,
    )
