"""Combinatorial size bounds for pair-obligation antichain kernels.

After exact pair-obligation dominance, no remaining cross-target pair has a
separator set that strictly contains another remaining pair's separator set.
Ignoring duplicate signatures, the residual separator signatures therefore form
an antichain of nonempty subsets of the remaining query vocabulary.

By Sperner's theorem, an antichain of subsets of an m-element set has size at
most binom(m, floor(m/2)). This module provides a checkable receipt for that
bound. It does not prove that a caller's residual state came from the exact
kernelizer; it verifies only the supplied/task-derived signature structure.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import comb

from .core import FiniteTask


@dataclass(frozen=True)
class AntichainKernelBoundReceipt:
    query_count: int
    raw_cross_target_pair_count: int
    distinct_nonempty_separator_signatures: int
    minimal_separator_antichain_size: int
    sperner_upper_bound: int
    antichain_bound_holds: bool
    strict_reduction_from_raw_pairs: int
    canonical_signatures: tuple[int, ...]
    scope: str = "distinct_minimal_cross_target_separator_signatures_on_declared_query_vocabulary"


def _separator_masks(task: FiniteTask) -> tuple[int, ...]:
    masks = []
    for i, j in combinations(range(len(task.worlds)), 2):
        if task.worlds[i].target == task.worlds[j].target:
            continue
        mask = 0
        for q, query in enumerate(task.queries):
            if query.outcomes[i] != query.outcomes[j]:
                mask |= 1 << q
        masks.append(mask)
    return tuple(masks)


def minimal_separator_antichain(signatures: tuple[int, ...]) -> tuple[int, ...]:
    """Remove duplicate and inclusion-dominated separator obligations.

    A pair with separator set E is redundant when another pair has separator set
    H with H subset E: every fixed bundle that covers H necessarily covers E.
    Therefore only inclusion-minimal nonempty separator signatures are needed.
    Empty signatures are kept separately by callers as an immediate
    unseparability witness and are not members of the nonempty antichain.
    """
    unique = sorted({mask for mask in signatures if mask != 0})
    minimal = []
    for mask in unique:
        if any(other != mask and (other & ~mask) == 0 for other in unique):
            continue
        minimal.append(mask)
    return tuple(minimal)


def is_inclusion_antichain(signatures: tuple[int, ...]) -> bool:
    """Check pairwise incomparability of distinct nonempty subset masks."""
    if any(mask == 0 for mask in signatures) or len(set(signatures)) != len(signatures):
        return False
    for i, left in enumerate(signatures):
        for right in signatures[i + 1:]:
            if (left & ~right) == 0 or (right & ~left) == 0:
                return False
    return True


def task_pair_antichain_bound(task: FiniteTask) -> AntichainKernelBoundReceipt:
    """Audit the root cross-target pair obligations against Sperner's bound.

    This applies only pair-obligation dominance at the declared root vocabulary;
    budget-dependent query deletion, forcing, and query dominance can make later
    residual kernels smaller still.
    """
    masks = _separator_masks(task)
    distinct_nonempty = len({mask for mask in masks if mask != 0})
    minimal = minimal_separator_antichain(masks)
    m = len(task.queries)
    sperner = comb(m, m // 2) if m else 1
    antichain = is_inclusion_antichain(minimal) if minimal else True
    holds = antichain and len(minimal) <= sperner
    if not holds:
        raise ArithmeticError("minimal separator signatures violated Sperner antichain bound")
    return AntichainKernelBoundReceipt(
        m,
        len(masks),
        distinct_nonempty,
        len(minimal),
        sperner,
        True,
        len(masks) - len(minimal),
        minimal,
    )
