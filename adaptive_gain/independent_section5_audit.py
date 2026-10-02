"""Independent audit of manuscript Section 5.

This module intentionally does NOT import the repository's finite-task solver,
information helpers, or static-information witness implementation.  It rebuilds
the Section-5 tasks from literal matrices and verifies:

1. complete Shannon entropy-vector equivalence for the one-copy twins;
2. exact fixed costs C_F=(4,4);
3. exact adaptive worst-case costs C_A=(4,3);
4. the two-copy product gives C_F=(8,8), C_A=(8,6);
5. the two-copy complete Shannon entropy vectors remain exactly matched.

Entropy equality is certified as an integer coefficient vector over log2(prime)
rather than by floating-point comparison.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from dataclasses import dataclass


WORLD_SIGNATURES = (
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

TARGET_A = (0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0)
TARGET_B = (0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0)


def _prime_factors(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("n must be positive")
    out: dict[int, int] = {}
    p = 2
    value = n
    while p * p <= value:
        while value % p == 0:
            out[p] = out.get(p, 0) + 1
            value //= p
        p += 1
    if value > 1:
        out[value] = out.get(value, 0) + 1
    return out


def _add_log(coeff: dict[int, int], multiplier: int, n: int) -> None:
    if n <= 1 or multiplier == 0:
        return
    for p, e in _prime_factors(n).items():
        coeff[p] = coeff.get(p, 0) + multiplier * e


def entropy_fingerprint(values: tuple[object, ...]) -> tuple[tuple[int, int], ...]:
    """Exact fingerprint for N*H(X) under the uniform empirical distribution."""
    counts = Counter(values)
    n = len(values)
    coeff: dict[int, int] = {}
    _add_log(coeff, n, n)
    for count in counts.values():
        _add_log(coeff, -count, count)
    return tuple(sorted((p, c) for p, c in coeff.items() if c))


def _joint_values(
    targets: tuple[object, ...],
    queries: tuple[tuple[int, ...], ...],
    subset: tuple[int, ...],
    include_target: bool,
) -> tuple[object, ...]:
    rows = []
    for i in range(len(targets)):
        cue = tuple(queries[j][i] for j in subset)
        rows.append((targets[i],) + cue if include_target else cue)
    return tuple(rows)


def _all_entropy_fingerprints(
    targets: tuple[object, ...],
    queries: tuple[tuple[int, ...], ...],
) -> tuple[tuple[tuple[int, ...], bool, tuple[tuple[int, int], ...]], ...]:
    out = []
    m = len(queries)
    for r in range(m + 1):
        for subset in combinations(range(m), r):
            for include_target in (False, True):
                out.append(
                    (
                        subset,
                        include_target,
                        entropy_fingerprint(
                            _joint_values(targets, queries, subset, include_target)
                        ),
                    )
                )
    return tuple(out)


def _resolves(
    targets: tuple[object, ...],
    queries: tuple[tuple[int, ...], ...],
    subset: tuple[int, ...],
) -> bool:
    seen: dict[tuple[int, ...], object] = {}
    for i, target in enumerate(targets):
        signature = tuple(queries[j][i] for j in subset)
        previous = seen.get(signature, target)
        if signature in seen and previous != target:
            return False
        seen[signature] = target
    return True


def fixed_cost(
    targets: tuple[object, ...],
    queries: tuple[tuple[int, ...], ...],
) -> int:
    m = len(queries)
    for r in range(m + 1):
        for subset in combinations(range(m), r):
            if _resolves(targets, queries, subset):
                return r
    raise AssertionError("task is not fixed-resolvable")


def adaptive_cost(
    targets: tuple[object, ...],
    queries: tuple[tuple[int, ...], ...],
) -> int:
    """Independent exact minimax decision-tree solver for unit-cost queries."""
    n = len(targets)
    m = len(queries)
    root_mask = (1 << n) - 1
    all_queries = (1 << m) - 1

    @lru_cache(None)
    def solve(mask: int, remaining: int) -> int:
        present = [i for i in range(n) if mask & (1 << i)]
        if len({targets[i] for i in present}) <= 1:
            return 0

        best: int | None = None
        for q in range(m):
            bit = 1 << q
            if not remaining & bit:
                continue
            children: dict[int, int] = {}
            for i in present:
                outcome = queries[q][i]
                children[outcome] = children.get(outcome, 0) | (1 << i)
            if len(children) <= 1:
                continue
            candidate = 1 + max(
                solve(child, remaining ^ bit) for child in children.values()
            )
            if best is None or candidate < best:
                best = candidate
        if best is None:
            raise AssertionError("adaptive task became unresolvable")
        return best

    return solve(root_mask, all_queries)


def one_copy_task(targets: tuple[int, ...]):
    queries = tuple(
        tuple(row[j] for row in WORLD_SIGNATURES)
        for j in range(4)
    )
    return tuple(targets), queries


def two_copy_task(targets: tuple[int, ...]):
    world_pairs = tuple(product(range(12), repeat=2))
    compound_targets = tuple((targets[i], targets[j]) for i, j in world_pairs)
    queries = []
    for coordinate in range(2):
        for q in range(4):
            queries.append(
                tuple(
                    WORLD_SIGNATURES[pair[coordinate]][q]
                    for pair in world_pairs
                )
            )
    return compound_targets, tuple(queries)


@dataclass(frozen=True)
class IndependentSection5Audit:
    one_copy_entropy_vector_match: bool
    one_copy_fixed_costs: tuple[int, int]
    one_copy_adaptive_costs: tuple[int, int]
    two_copy_entropy_vector_match: bool
    two_copy_fixed_costs: tuple[int, int]
    two_copy_adaptive_costs: tuple[int, int]
    one_copy_worlds: int
    two_copy_worlds: int
    theorem_holds: bool


def run_independent_section5_audit() -> IndependentSection5Audit:
    a_t, q = one_copy_task(TARGET_A)
    b_t, q_b = one_copy_task(TARGET_B)
    assert q == q_b

    entropy_one = (
        _all_entropy_fingerprints(a_t, q)
        == _all_entropy_fingerprints(b_t, q_b)
    )
    cf_one = (fixed_cost(a_t, q), fixed_cost(b_t, q_b))
    ca_one = (adaptive_cost(a_t, q), adaptive_cost(b_t, q_b))

    a2_t, q2 = two_copy_task(TARGET_A)
    b2_t, q2_b = two_copy_task(TARGET_B)
    assert q2 == q2_b

    entropy_two = (
        _all_entropy_fingerprints(a2_t, q2)
        == _all_entropy_fingerprints(b2_t, q2_b)
    )
    cf_two = (fixed_cost(a2_t, q2), fixed_cost(b2_t, q2_b))
    ca_two = (adaptive_cost(a2_t, q2), adaptive_cost(b2_t, q2_b))

    holds = (
        entropy_one
        and cf_one == (4, 4)
        and ca_one == (4, 3)
        and entropy_two
        and cf_two == (8, 8)
        and ca_two == (8, 6)
    )
    if not holds:
        raise AssertionError("independent Section-5 audit failed")

    return IndependentSection5Audit(
        one_copy_entropy_vector_match=entropy_one,
        one_copy_fixed_costs=cf_one,
        one_copy_adaptive_costs=ca_one,
        two_copy_entropy_vector_match=entropy_two,
        two_copy_fixed_costs=cf_two,
        two_copy_adaptive_costs=ca_two,
        one_copy_worlds=len(a_t),
        two_copy_worlds=len(a2_t),
        theorem_holds=holds,
    )
