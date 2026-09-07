"""Antichain bounds for reduced state-resource fixed-failure rows.

A row is a pair (U,P) of disjoint query subsets.  The reduction order is
componentwise inclusion:

    (U1,P1) <= (U2,P2) iff U1 subseteq U2 and P1 subseteq P2.

After dominance reduction the retained rows form an antichain in the q-fold
product of the three-element poset {0 < U, 0 < P}.  A rank-k row chooses k query
coordinates and assigns U/P to each, so rank size is C(q,k) 2^k.

A uniformly random maximal chain gives each rank-k row probability
1 / (C(q,k) 2^k).  Since an antichain intersects a chain at most once,

    sum_r 1/(C(q,k_r) 2^k_r) <= 1.

Therefore the reduced row count is at most max_k C(q,k) 2^k.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb

from .core import FiniteTask
from .state_resource_incidence import (
    StateResourceIncidenceRow,
    build_state_resource_incidence,
)


@dataclass(frozen=True)
class StateResourceAntichainBoundReceipt:
    query_count: int
    rank_sizes: tuple[int, ...]
    maximizing_ranks: tuple[int, ...]
    maximum_antichain_bound: int
    scope: str = "lym_bound_for_componentwise_state_resource_failure_row_antichain"


@dataclass(frozen=True)
class StateResourceKernelBoundReceipt:
    query_count: int
    raw_row_count: int
    reduced_row_count: int
    maximum_antichain_bound: int
    lym_weight_numerator: int
    lym_weight_denominator: int
    reduced_rows_form_antichain: bool
    bound_holds: bool
    scope: str = "task_state_resource_reduced_row_antichain_bound_audit"


def state_resource_antichain_bound(query_count: int) -> StateResourceAntichainBoundReceipt:
    if type(query_count) is not int or query_count < 0:
        raise ValueError("query_count must be a nonnegative integer")
    ranks = tuple(comb(query_count, k) * (2 ** k) for k in range(query_count + 1))
    maximum = max(ranks, default=1)
    maximizing = tuple(k for k, size in enumerate(ranks) if size == maximum)
    return StateResourceAntichainBoundReceipt(
        query_count,
        ranks,
        maximizing,
        maximum,
    )


def _row_rank(row: StateResourceIncidenceRow) -> int:
    return (row.unavailable_queries | row.productive_queries).bit_count()


def state_resource_lym_weight(
    rows: tuple[StateResourceIncidenceRow, ...],
    query_count: int,
) -> Fraction:
    receipt = state_resource_antichain_bound(query_count)
    total = Fraction(0, 1)
    for row in rows:
        rank = _row_rank(row)
        if rank > query_count:
            raise ValueError("row rank exceeds declared query count")
        total += Fraction(1, receipt.rank_sizes[rank])
    return total


def rows_form_state_resource_antichain(
    rows: tuple[StateResourceIncidenceRow, ...],
) -> bool:
    for i, left in enumerate(rows):
        for j, right in enumerate(rows):
            if i == j:
                continue
            if (
                left.unavailable_queries & ~right.unavailable_queries == 0
                and left.productive_queries & ~right.productive_queries == 0
            ):
                return False
    return True


def task_state_resource_kernel_bound(task: FiniteTask) -> StateResourceKernelBoundReceipt:
    certificate = build_state_resource_incidence(task)
    qn = len(task.queries)
    bound = state_resource_antichain_bound(qn)
    antichain = rows_form_state_resource_antichain(certificate.reduced_rows)
    weight = state_resource_lym_weight(certificate.reduced_rows, qn)
    holds = (
        antichain
        and weight <= 1
        and len(certificate.reduced_rows) <= bound.maximum_antichain_bound
    )
    return StateResourceKernelBoundReceipt(
        qn,
        len(certificate.rows),
        len(certificate.reduced_rows),
        bound.maximum_antichain_bound,
        weight.numerator,
        weight.denominator,
        antichain,
        holds,
    )
