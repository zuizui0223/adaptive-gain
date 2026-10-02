"""Exact-balanced twins with identical static subset information but different adaptive cost.

The two deterministic tasks in this module share:
- the same 12 represented worlds;
- the same four binary unit-cost query rows;
- exact 6/6 balance for every query;
- the same target multiplicities (8,4);
- the same *named* Shannon information I(T; Q_S) for every one of the 2**4
  query subsets S, under the uniform world prior.

Nevertheless their exact finite costs differ:

    twin A: C_A = C_F = 4
    twin B: C_A = 3, C_F = 4.

Thus the complete static subset-mutual-information set function is sufficient
to recover C_F in this deterministic exact-resolution setting, but is not
sufficient to recover C_A.

The information-profile equality is certified exactly, without floating point,
by representing N*H(T|Q_S) as a formal integer linear combination of log2(p)
over prime p.  Equality of those fingerprints plus equal target multiplicities
implies exact equality of I(T;Q_S).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Hashable, Sequence

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution
from .information import bundle_information_bits, target_entropy_bits


_WORLD_SIGNATURES = (
    (0, 0, 0, 0),
    (0, 0, 0, 1),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 0),
    (0, 1, 1, 1),
    (1, 0, 0, 0),
    (1, 0, 1, 1),
    (1, 1, 0, 0),
    (1, 1, 0, 1),
    (1, 1, 1, 0),
    (1, 1, 1, 1),
)

_TWIN_A_TARGETS = (0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0)
_TWIN_B_TARGETS = (0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0)


def _task(targets: Sequence[Hashable]) -> FiniteTask:
    if len(targets) != len(_WORLD_SIGNATURES):
        raise ValueError("target vector must cover every represented world")
    worlds = tuple(World(f"w{i:02d}", target) for i, target in enumerate(targets))
    queries = tuple(
        Query(
            f"q{j}",
            1,
            tuple(signature[j] for signature in _WORLD_SIGNATURES),
        )
        for j in range(4)
    )
    return FiniteTask(worlds, queries)


def static_information_twin_a_task() -> FiniteTask:
    """Exact-balanced twin with C_A=C_F=4."""
    return _task(_TWIN_A_TARGETS)


def static_information_twin_b_task() -> FiniteTask:
    """Exact-balanced twin with C_A=3 and C_F=4."""
    return _task(_TWIN_B_TARGETS)


def _prime_factorization(n: int) -> dict[int, int]:
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    factors: dict[int, int] = {}
    value = n
    p = 2
    while p * p <= value:
        while value % p == 0:
            factors[p] = factors.get(p, 0) + 1
            value //= p
        p += 1
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def _add_log_integer(coefficients: dict[int, int], multiplier: int, n: int) -> None:
    if n <= 1 or multiplier == 0:
        return
    for prime, exponent in _prime_factorization(n).items():
        coefficients[prime] = coefficients.get(prime, 0) + multiplier * exponent


def joint_entropy_log_fingerprint(
    task: FiniteTask,
    bundle: Sequence[str],
    *,
    include_target: bool = False,
) -> tuple[tuple[int, int], ...]:
    """Exact fingerprint for N*H(Q_bundle) or N*H(T,Q_bundle).

    The common denominator N is the represented-world count under the uniform
    prior.  For observation-cell sizes n_x,

        N H(X) = N log2(N) - sum_x n_x log2(n_x).

    Factoring integers into primes makes equality exact rather than numerical.
    When include_target=True, the target label is prepended to the cue
    signature.  Comparing all cue subsets with and without the target certifies
    equality of the complete Shannon entropy vector over (T,Q_0,...,Q_m).
    """
    lookup = {q.name: q for q in task.queries}
    names = tuple(bundle)
    if len(set(names)) != len(names) or any(name not in lookup for name in names):
        raise ValueError("bundle must contain unique declared query names")

    counts: dict[tuple[Hashable, ...], int] = {}
    for i, world in enumerate(task.worlds):
        signature = tuple(lookup[name].outcomes[i] for name in names)
        if include_target:
            signature = (world.target,) + signature
        counts[signature] = counts.get(signature, 0) + 1

    total = len(task.worlds)
    coefficients: dict[int, int] = {}
    _add_log_integer(coefficients, total, total)
    for count in counts.values():
        _add_log_integer(coefficients, -count, count)
    return tuple(
        sorted(
            (prime, coefficient)
            for prime, coefficient in coefficients.items()
            if coefficient
        )
    )


def conditional_entropy_log_fingerprint(
    task: FiniteTask,
    bundle: Sequence[str],
) -> tuple[tuple[int, int], ...]:
    """Exact fingerprint for N*H(T|Q_bundle) under the uniform world prior.

    For one observation cell with n states and target counts n_t,

        n H(T | cell) = n log2(n) - sum_t n_t log2(n_t).

    Factoring each integer into primes turns the total conditional entropy into
    a formal integer combination of log2(prime).  Equal fingerprints are exact
    entropy equalities, not numerical approximations.
    """
    lookup = {q.name: q for q in task.queries}
    names = tuple(bundle)
    if len(set(names)) != len(names) or any(name not in lookup for name in names):
        raise ValueError("bundle must contain unique declared query names")

    cells: dict[tuple[Hashable, ...], dict[Hashable, int]] = {}
    for i, world in enumerate(task.worlds):
        signature = tuple(lookup[name].outcomes[i] for name in names)
        if signature not in cells:
            cells[signature] = {}
        target_counts = cells[signature]
        target_counts[world.target] = target_counts.get(world.target, 0) + 1

    coefficients: dict[int, int] = {}
    for target_counts in cells.values():
        n = sum(target_counts.values())
        _add_log_integer(coefficients, n, n)
        for count in target_counts.values():
            _add_log_integer(coefficients, -count, count)

    return tuple(sorted((prime, coefficient) for prime, coefficient in coefficients.items() if coefficient))


def _target_multiplicities(task: FiniteTask) -> tuple[int, ...]:
    counts: dict[Hashable, int] = {}
    for world in task.worlds:
        counts[world.target] = counts.get(world.target, 0) + 1
    return tuple(sorted(counts.values(), reverse=True))


def _all_query_subsets(task: FiniteTask) -> tuple[tuple[str, ...], ...]:
    names = tuple(q.name for q in task.queries)
    return tuple(
        tuple(names[j] for j in range(len(names)) if mask & (1 << j))
        for mask in range(1 << len(names))
    )


@dataclass(frozen=True)
class StaticInformationAdaptiveSeparationReceipt:
    world_count: int
    query_count: int
    same_world_names: bool
    same_query_outcome_matrix: bool
    every_query_exactly_balanced: bool
    same_target_multiplicities: bool
    target_multiplicities: tuple[int, ...]
    same_target_entropy: bool
    same_named_subset_information_profile_exactly: bool
    same_full_shannon_entropy_vector_exactly: bool
    subset_information_profile_bits: tuple[tuple[tuple[str, ...], float], ...]
    twin_a_adaptive_cost: int
    twin_a_fixed_cost: int
    twin_b_adaptive_cost: int
    twin_b_fixed_cost: int
    theorem_holds: bool
    scope: str = "exact_balanced_static_information_profile_non_sufficiency_for_adaptive_cost"


def static_information_adaptive_separation_audit() -> StaticInformationAdaptiveSeparationReceipt:
    a = static_information_twin_a_task()
    b = static_information_twin_b_task()

    same_world_names = tuple(w.name for w in a.worlds) == tuple(w.name for w in b.worlds)
    same_query_matrix = all(
        qa.name == qb.name and qa.cost == qb.cost and qa.outcomes == qb.outcomes
        for qa, qb in zip(a.queries, b.queries)
    )
    balanced = all(
        sum(outcome == 0 for outcome in q.outcomes) == len(a.worlds) // 2
        and sum(outcome == 1 for outcome in q.outcomes) == len(a.worlds) // 2
        for q in a.queries
    )

    mult_a = _target_multiplicities(a)
    mult_b = _target_multiplicities(b)
    same_multiplicities = mult_a == mult_b
    same_target_entropy = abs(target_entropy_bits(a) - target_entropy_bits(b)) <= 1e-12

    subsets = _all_query_subsets(a)
    exact_profile_match = all(
        conditional_entropy_log_fingerprint(a, subset)
        == conditional_entropy_log_fingerprint(b, subset)
        for subset in subsets
    )
    full_entropy_vector_match = all(
        joint_entropy_log_fingerprint(a, subset, include_target=include_target)
        == joint_entropy_log_fingerprint(b, subset, include_target=include_target)
        for subset in subsets
        for include_target in (False, True)
    )
    profile = tuple((subset, bundle_information_bits(a, subset)) for subset in subsets)
    numerical_profile_match = all(
        abs(bundle_information_bits(a, subset) - bundle_information_bits(b, subset)) <= 1e-12
        for subset in subsets
    )

    a_ca = adaptive_minimum_resolution(a).minimum_worst_path_cost
    a_cf = fixed_minimum_resolution(a).minimum_cost
    b_ca = adaptive_minimum_resolution(b).minimum_worst_path_cost
    b_cf = fixed_minimum_resolution(b).minimum_cost
    if None in (a_ca, a_cf, b_ca, b_cf):
        raise ArithmeticError("both information twins must be exactly resolvable")

    theorem = (
        same_world_names
        and same_query_matrix
        and balanced
        and same_multiplicities
        and mult_a == (8, 4)
        and same_target_entropy
        and exact_profile_match
        and full_entropy_vector_match
        and numerical_profile_match
        and a_ca == 4
        and a_cf == 4
        and b_ca == 3
        and b_cf == 4
    )
    if not theorem:
        raise ArithmeticError("static-information adaptive-separation audit failed")

    return StaticInformationAdaptiveSeparationReceipt(
        world_count=len(a.worlds),
        query_count=len(a.queries),
        same_world_names=same_world_names,
        same_query_outcome_matrix=same_query_matrix,
        every_query_exactly_balanced=balanced,
        same_target_multiplicities=same_multiplicities,
        target_multiplicities=mult_a,
        same_target_entropy=same_target_entropy,
        same_named_subset_information_profile_exactly=exact_profile_match,
        same_full_shannon_entropy_vector_exactly=full_entropy_vector_match,
        subset_information_profile_bits=profile,
        twin_a_adaptive_cost=a_ca,
        twin_a_fixed_cost=a_cf,
        twin_b_adaptive_cost=b_ca,
        twin_b_fixed_cost=b_cf,
        theorem_holds=theorem,
    )
