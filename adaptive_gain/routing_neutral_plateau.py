"""Exact first-gain waiting law on the neutral routing plateau.

This side-theory module builds on ``local_routing_mutation``.  The ecological
sensing task and branch-program representation stay fixed.  Mutation attempts
choose one of k branch programs uniformly.  If the chosen branch still contains
a target-irrelevant acquisition occurrence, one such occurrence is pruned;
otherwise the attempt is null.

Before the first positive worst-path routing gain appears, only one fact matters:
whether each branch has been pruned at least once.  Therefore the microscopic
routing process strongly lumps to the number m of distinct branches already
touched.  The lumped chain is the classical coupon-collector occupancy chain.

Coupon-collector formulas are established prior art.  Their role here is only to
compose the exact routing plateau from adaptive-gain with an explicit stochastic
mutation-attempt process.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb


def _validate_branch_count(branch_count: int) -> int:
    if type(branch_count) is not int or branch_count < 2:
        raise ValueError("branch_count must be an integer at least 2")
    return branch_count


def _validate_attempts(attempts: int) -> int:
    if type(attempts) is not int or attempts < 0:
        raise ValueError("attempts must be a nonnegative integer")
    return attempts


def harmonic_number(order: int) -> Fraction:
    """Exact harmonic number H_order."""

    if type(order) is not int or order < 1:
        raise ValueError("order must be a positive integer")
    return sum((Fraction(1, j) for j in range(1, order + 1)), Fraction(0, 1))


def lump_transition_row(branch_count: int, touched_branches: int) -> tuple[Fraction, ...]:
    """Exact transition row for m=#branches pruned at least once.

    From m<k, another mutation attempt touches a new branch with probability
    (k-m)/k and an already touched branch with probability m/k.  State k is
    absorbing for the first-gain stopping problem.
    """

    k = _validate_branch_count(branch_count)
    m = touched_branches
    if type(m) is not int or not 0 <= m <= k:
        raise ValueError("touched_branches must be an integer in [0,k]")

    row = [Fraction(0, 1) for _ in range(k + 1)]
    if m == k:
        row[k] = Fraction(1, 1)
    else:
        row[m] = Fraction(m, k)
        row[m + 1] = Fraction(k - m, k)
    return tuple(row)


def touched_count_distribution(branch_count: int, attempts: int) -> tuple[Fraction, ...]:
    """Exact distribution of the lumped occupancy state after t attempts."""

    k = _validate_branch_count(branch_count)
    t = _validate_attempts(attempts)
    distribution = [Fraction(0, 1) for _ in range(k + 1)]
    distribution[0] = Fraction(1, 1)

    for _ in range(t):
        nxt = [Fraction(0, 1) for _ in range(k + 1)]
        for m, mass in enumerate(distribution):
            if not mass:
                continue
            row = lump_transition_row(k, m)
            for target, probability in enumerate(row):
                if probability:
                    nxt[target] += mass * probability
        distribution = nxt

    if sum(distribution, Fraction(0, 1)) != 1:
        raise ArithmeticError("lumped routing mutation distribution lost probability mass")
    return tuple(distribution)


def first_positive_gain_cdf(branch_count: int, attempts: int) -> Fraction:
    """P(T_first <= attempts) by exact inclusion-exclusion.

    First positive worst-path gain occurs exactly when every branch has been
    selected for pruning at least once.  The formula is the classical coupon-
    collector completion probability.
    """

    k = _validate_branch_count(branch_count)
    t = _validate_attempts(attempts)
    total = Fraction(0, 1)
    for omitted in range(k + 1):
        term = Fraction(k - omitted, k) ** t
        coefficient = comb(k, omitted)
        if omitted % 2:
            total -= coefficient * term
        else:
            total += coefficient * term
    if not 0 <= total <= 1:
        raise ArithmeticError("first-gain CDF left [0,1]")
    return total


def first_positive_gain_pmf(branch_count: int, attempts: int) -> Fraction:
    """P(T_first = attempts), with support starting at t=k."""

    k = _validate_branch_count(branch_count)
    t = _validate_attempts(attempts)
    if t == 0:
        return Fraction(0, 1)
    return first_positive_gain_cdf(k, t) - first_positive_gain_cdf(k, t - 1)


def expected_attempts_to_first_positive_gain(branch_count: int) -> Fraction:
    """Exact E[T_first] = k H_k mutation attempts."""

    k = _validate_branch_count(branch_count)
    return k * harmonic_number(k)


def expected_remaining_attempts(branch_count: int, touched_branches: int) -> Fraction:
    """Exact expected remaining attempts from lumped state m.

    E_m = sum_{j=m}^{k-1} k/(k-j), equivalently k H_{k-m}.
    """

    k = _validate_branch_count(branch_count)
    m = touched_branches
    if type(m) is not int or not 0 <= m <= k:
        raise ValueError("touched_branches must be an integer in [0,k]")
    if m == k:
        return Fraction(0, 1)
    return k * harmonic_number(k - m)


@dataclass(frozen=True)
class FirstGainWaitingReceipt:
    branch_count: int
    shortest_elementary_pruning_distance: int
    expected_mutation_attempts: Fraction
    stochastic_overhead_factor: Fraction
    earliest_possible_attempt: int
    earliest_completion_probability: Fraction
    scope: str = "uniform_branch_attempts_neutral_permitting_until_first_positive_gain"


def first_gain_waiting_receipt(branch_count: int) -> FirstGainWaitingReceipt:
    """Compose routing shortest distance with the exact stochastic waiting law."""

    k = _validate_branch_count(branch_count)
    expectation = expected_attempts_to_first_positive_gain(k)
    earliest_probability = first_positive_gain_pmf(k, k)
    expected_earliest = Fraction(1, 1)
    for denominator in range(1, k + 1):
        expected_earliest *= Fraction(denominator, k)
    if earliest_probability != expected_earliest:
        raise ArithmeticError("earliest coupon-completion probability audit failed")

    return FirstGainWaitingReceipt(
        branch_count=k,
        shortest_elementary_pruning_distance=k,
        expected_mutation_attempts=expectation,
        stochastic_overhead_factor=expectation / k,
        earliest_possible_attempt=k,
        earliest_completion_probability=earliest_probability,
    )


@dataclass(frozen=True)
class RequiredGapFirstGainWaitingReceipt:
    required_gap: int
    branch_count: int
    static_world_count: int
    static_query_count: int
    static_adaptive_depth: int
    shortest_attempts_to_any_positive_gain: int
    expected_attempts_to_any_positive_gain: Fraction
    overhead_factor: Fraction


def required_gap_first_gain_waiting_receipt(required_gap: int) -> RequiredGapFirstGainWaitingReceipt:
    """Specialize first-gain waiting to the q-gap query-minimal star family.

    This receipt concerns the waiting time to the *first positive realized gain*,
    not the waiting time to the full target gap q.
    """

    q = required_gap
    if type(q) is not int or q < 1:
        raise ValueError("required_gap must be a positive integer")
    k = q + 1
    waiting = first_gain_waiting_receipt(k)
    return RequiredGapFirstGainWaitingReceipt(
        required_gap=q,
        branch_count=k,
        static_world_count=2 * q + 2,
        static_query_count=q + 2,
        static_adaptive_depth=2,
        shortest_attempts_to_any_positive_gain=k,
        expected_attempts_to_any_positive_gain=waiting.expected_mutation_attempts,
        overhead_factor=waiting.stochastic_overhead_factor,
    )
