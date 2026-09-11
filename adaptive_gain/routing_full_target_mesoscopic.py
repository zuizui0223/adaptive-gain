"""Exact mesoscopic occupancy dynamics to a full realized routing-gain target.

This stacked side-theory module extends ``routing_neutral_plateau`` from the
first positive routing gain to an arbitrary target realized gain r.  Under the
uniform branch-attempt process, gain r is reached once every branch has received
at least r effective pruning hits.  Capping each branch's progress at r gives a
classical multiple-copy coupon-collector process.

The microscopic state is a k-vector of capped branch hit counts.  Exchangeability
strongly lumps that process to an occupancy histogram n_j: the number of branches
with capped progress j, j=0,...,r.  The finite histogram chain is exact; no
diffusion approximation is used.

Multiple-coupon collection and occupancy chains are established prior art.  Their
role here is only to compose the routing-accessibility geometry with a declared
stochastic mutation-attempt process.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import comb, factorial

from .local_routing_mutation import minimum_local_prunings_for_gain
from .routing_neutral_plateau import expected_attempts_to_first_positive_gain


class RoutingMesostateLimitError(RuntimeError):
    """Raised when exact histogram recursion exceeds the declared state cap."""


def _validate_k_r(branch_count: int, required_gain: int) -> tuple[int, int]:
    k = branch_count
    r = required_gain
    if type(k) is not int or k < 2:
        raise ValueError("branch_count must be an integer at least 2")
    if type(r) is not int or not (1 <= r <= k - 1):
        raise ValueError("required_gain must be an integer in [1,k-1]")
    return k, r


def capped_progress_histogram(
    progress: tuple[int, ...],
    required_gain: int,
) -> tuple[int, ...]:
    """Map branch-level pruning counts to the exact occupancy histogram."""

    if type(required_gain) is not int or required_gain < 1:
        raise ValueError("required_gain must be a positive integer")
    if len(progress) < 2:
        raise ValueError("progress must contain at least two branches")
    r = required_gain
    histogram = [0] * (r + 1)
    for value in progress:
        if type(value) is not int or value < 0:
            raise ValueError("branch progress values must be nonnegative integers")
        histogram[min(value, r)] += 1
    return tuple(histogram)


def histogram_mesostate_count(branch_count: int, required_gain: int) -> int:
    """Number of occupancy histograms: C(k+r,r)."""

    k, r = _validate_k_r(branch_count, required_gain)
    return comb(k + r, r)


def capped_microstate_count(branch_count: int, required_gain: int) -> int:
    """Number of capped branch-progress microstates: (r+1)^k."""

    k, r = _validate_k_r(branch_count, required_gain)
    return (r + 1) ** k


def _validate_histogram(
    branch_count: int,
    required_gain: int,
    histogram: tuple[int, ...],
) -> tuple[int, int]:
    k, r = _validate_k_r(branch_count, required_gain)
    if len(histogram) != r + 1:
        raise ValueError("histogram must contain one bin for each capped progress level 0..r")
    if any(type(count) is not int or count < 0 for count in histogram):
        raise ValueError("histogram counts must be nonnegative integers")
    if sum(histogram) != k:
        raise ValueError("histogram counts must sum to branch_count")
    return k, r


def histogram_transition_distribution(
    branch_count: int,
    required_gain: int,
    histogram: tuple[int, ...],
) -> dict[tuple[int, ...], Fraction]:
    """Exact one-attempt transition distribution on the mesoscopic histogram.

    A branch at capped level j<r advances to j+1 when selected.  A branch already
    at level r produces a null attempt and leaves the histogram unchanged.
    """

    k, r = _validate_histogram(branch_count, required_gain, histogram)
    result: dict[tuple[int, ...], Fraction] = {}

    saturated = histogram[r]
    if saturated:
        result[histogram] = Fraction(saturated, k)

    for level in range(r):
        count = histogram[level]
        if not count:
            continue
        nxt = list(histogram)
        nxt[level] -= 1
        nxt[level + 1] += 1
        state = tuple(nxt)
        result[state] = result.get(state, Fraction(0, 1)) + Fraction(count, k)

    if sum(result.values(), Fraction(0, 1)) != 1:
        raise ArithmeticError("histogram transition probabilities did not sum to one")
    return result


def expected_attempts_to_realized_gain(
    branch_count: int,
    required_gain: int,
    *,
    mesostate_limit: int = 50_000,
) -> Fraction:
    """Exact expected mutation attempts from the full program to gain r.

    The histogram chain has C(k+r,r) possible states.  Self-loops occur only from
    proposals to already saturated branches.  Removing that self-loop yields an
    acyclic recurrence because every effective transition increases total capped
    progress by one.
    """

    k, r = _validate_k_r(branch_count, required_gain)
    if type(mesostate_limit) is not int or mesostate_limit < 1:
        raise ValueError("mesostate_limit must be a positive integer")
    states = histogram_mesostate_count(k, r)
    if states > mesostate_limit:
        raise RoutingMesostateLimitError(
            f"exact histogram recursion has {states} possible mesostates; "
            f"declared limit is {mesostate_limit}"
        )

    @lru_cache(None)
    def expected(histogram: tuple[int, ...]) -> Fraction:
        saturated = histogram[r]
        if saturated == k:
            return Fraction(0, 1)

        active = k - saturated
        # First-step equation:
        # E = 1 + (saturated/k)E + sum_{j<r}(n_j/k)E(next_j).
        # Solving the self-loop gives the recurrence below.
        value = Fraction(k, active)
        for level in range(r):
            count = histogram[level]
            if not count:
                continue
            nxt = list(histogram)
            nxt[level] -= 1
            nxt[level + 1] += 1
            value += Fraction(count, active) * expected(tuple(nxt))
        return value

    start = (k,) + (0,) * r
    return expected(start)


def earliest_target_completion_probability(branch_count: int, required_gain: int) -> Fraction:
    """Probability of reaching gain r in the minimum k*r attempts.

    Earliest completion requires exactly r selections of every one of the k
    branches.  The favorable branch-label sequences are the multinomial
    interleavings counted by (kr)!/(r!)^k.
    """

    k, r = _validate_k_r(branch_count, required_gain)
    attempts = k * r
    favorable = factorial(attempts) // (factorial(r) ** k)
    return Fraction(favorable, k**attempts)


@dataclass(frozen=True)
class FullTargetWaitingReceipt:
    branch_count: int
    required_gain: int
    shortest_elementary_prunings: int
    capped_microstate_count: int
    histogram_mesostate_count: int
    expected_mutation_attempts: Fraction
    stochastic_overhead_factor: Fraction
    earliest_completion_probability: Fraction
    scope: str = "uniform_branch_attempts_multiple_coupon_routing_target"


def full_target_waiting_receipt(
    branch_count: int,
    required_gain: int,
    *,
    mesostate_limit: int = 50_000,
) -> FullTargetWaitingReceipt:
    """Exact deterministic/stochastic accessibility summary for gain r."""

    k, r = _validate_k_r(branch_count, required_gain)
    shortest = minimum_local_prunings_for_gain(k, r)
    expectation = expected_attempts_to_realized_gain(
        k,
        r,
        mesostate_limit=mesostate_limit,
    )
    if expectation < shortest:
        raise ArithmeticError("expected attempt count fell below deterministic shortest distance")
    if r == 1 and expectation != expected_attempts_to_first_positive_gain(k):
        raise ArithmeticError("r=1 histogram chain disagreed with first-gain coupon collector")

    return FullTargetWaitingReceipt(
        branch_count=k,
        required_gain=r,
        shortest_elementary_prunings=shortest,
        capped_microstate_count=capped_microstate_count(k, r),
        histogram_mesostate_count=histogram_mesostate_count(k, r),
        expected_mutation_attempts=expectation,
        stochastic_overhead_factor=expectation / shortest,
        earliest_completion_probability=earliest_target_completion_probability(k, r),
    )


@dataclass(frozen=True)
class RequiredGapPhaseEntryReceipt:
    required_gap: int
    branch_count: int
    static_world_count: int
    static_query_count: int
    static_adaptive_depth: int
    shortest_elementary_prunings: int
    capped_microstate_count: int
    histogram_mesostate_count: int
    expected_phase_entry_attempts: Fraction
    stochastic_overhead_factor: Fraction
    earliest_phase_entry_probability: Fraction


def required_gap_phase_entry_receipt(
    required_gap: int,
    *,
    mesostate_limit: int = 50_000,
) -> RequiredGapPhaseEntryReceipt:
    """Compose the q-gap star task with full realized-gain waiting dynamics.

    For the query-minimal star family, k=q+1 and the full required task gap is
    realized only after every branch has been pruned q times.
    """

    q = required_gap
    if type(q) is not int or q < 1:
        raise ValueError("required_gap must be a positive integer")
    k = q + 1
    waiting = full_target_waiting_receipt(
        k,
        q,
        mesostate_limit=mesostate_limit,
    )
    return RequiredGapPhaseEntryReceipt(
        required_gap=q,
        branch_count=k,
        static_world_count=2 * q + 2,
        static_query_count=q + 2,
        static_adaptive_depth=2,
        shortest_elementary_prunings=waiting.shortest_elementary_prunings,
        capped_microstate_count=waiting.capped_microstate_count,
        histogram_mesostate_count=waiting.histogram_mesostate_count,
        expected_phase_entry_attempts=waiting.expected_mutation_attempts,
        stochastic_overhead_factor=waiting.stochastic_overhead_factor,
        earliest_phase_entry_probability=waiting.earliest_completion_probability,
    )
