"""Sharp universal fixed-cost cap for exactly-balanced binary queries.

For an even number ``n`` of represented worlds, every binary query in this
module is required to be globally exact 50/50: exactly ``n/2`` worlds return
each outcome.

Let B be a minimum fixed resolver.  Every q in B has a private cross-target
pair: deleting q makes some opposite-target pair indistinguishable, while q
separates it.  Choosing one such pair for every q gives a graph G on the worlds.
Each q crosses exactly its own chosen edge among G, so every edge of G is a
bridge and G is a forest.

Exact balance then forbids a minimum bundle of size n-1, and for n>=6 also
forbids size n-2.  Hence

    C_F <= n-3  (even n>=6).

The bound is sharp.  A three-component private-pair forest with component sizes
(n/2-1, 2, n/2-1), using a star, a single edge, and a star, induces n-3 exact
balanced cuts.  Giving each world a distinct target makes all n-3 queries
fixed-mandatory while the full family resolves.

The small exceptions are sharp as well: cap(2)=1 and cap(4)=2.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import FiniteTask, Query, World, fixed_minimum_resolution


@dataclass(frozen=True)
class ExactBalancedFixedCostCapReceipt:
    world_count: int
    sharp_fixed_cost_cap: int
    witness_query_count: int
    witness_fixed_cost: int
    all_queries_exactly_balanced: bool
    all_registered_private_pairs_unique: bool
    all_registered_private_pairs_cross_target: bool
    theorem_holds: bool
    scope: str = "sharp_exact_balanced_binary_fixed_cost_cap"


def sharp_exact_balanced_binary_fixed_cost_cap(world_count: int) -> int:
    """Maximum possible C_F over exact-50/50 binary tasks on n worlds."""
    if type(world_count) is not int or world_count < 2 or world_count % 2:
        raise ValueError("world_count must be an even integer at least 2")
    if world_count == 2:
        return 1
    if world_count == 4:
        return 2
    return world_count - 3


def _mask_outcomes(world_count: int, one_side: set[int]) -> tuple[int, ...]:
    return tuple(1 if index in one_side else 0 for index in range(world_count))


def _cap_rows_and_private_pairs(
    world_count: int,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, int], ...]]:
    if world_count == 2:
        return ((0, 1),), ((0, 1),)

    if world_count == 4:
        rows = (
            _mask_outcomes(4, {0, 3}),
            _mask_outcomes(4, {0, 1}),
        )
        # q0 uniquely separates (0,1); q1 uniquely separates (1,2).
        return rows, ((0, 1), (1, 2))

    half = world_count // 2
    left = tuple(range(0, half - 1))
    middle = (half - 1, half)
    right = tuple(range(half + 1, world_count))
    if len(left) != half - 1 or len(right) != half - 1:
        raise ArithmeticError("balanced cap construction partition failed")

    rows: list[tuple[int, ...]] = []
    private_pairs: list[tuple[int, int]] = []

    left_center = left[0]
    for leaf in left[1:]:
        one_side = (set(left) - {leaf}) | set(middle)
        rows.append(_mask_outcomes(world_count, one_side))
        private_pairs.append((left_center, leaf))

    # The middle edge is balanced by padding one endpoint with the whole left
    # component.
    rows.append(_mask_outcomes(world_count, set(left) | {middle[0]}))
    private_pairs.append(middle)

    right_center = right[0]
    for leaf in right[1:]:
        one_side = (set(right) - {leaf}) | set(middle)
        rows.append(_mask_outcomes(world_count, one_side))
        private_pairs.append((right_center, leaf))

    expected = world_count - 3
    if len(rows) != expected or len(private_pairs) != expected:
        raise ArithmeticError("balanced cap construction has wrong size")
    return tuple(rows), tuple(private_pairs)


def exact_balanced_binary_fixed_cost_cap_witness(world_count: int) -> FiniteTask:
    """Explicit task attaining the sharp exact-balanced fixed-cost cap."""
    cap = sharp_exact_balanced_binary_fixed_cost_cap(world_count)
    rows, private_pairs = _cap_rows_and_private_pairs(world_count)
    if len(rows) != cap:
        raise ArithmeticError("cap witness query count disagrees with theorem")

    # The cut signatures of the construction are distinct, so identity targets
    # are resolvable by the full bundle.  Using identity targets also makes every
    # registered private pair automatically cross-target.
    worlds = tuple(World(f"w{i}", i) for i in range(world_count))
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    task = FiniteTask(worlds, queries)

    signatures = {
        tuple(query.outcomes[world_index] for query in queries)
        for world_index in range(world_count)
    }
    if len(signatures) != world_count:
        raise ArithmeticError("cap witness does not resolve identity targets")

    for q_index, (left, right) in enumerate(private_pairs):
        separating = [
            index
            for index, query in enumerate(queries)
            if query.outcomes[left] != query.outcomes[right]
        ]
        if separating != [q_index]:
            raise ArithmeticError("registered private pair is not query-unique")
    return task


def exact_balanced_binary_fixed_cost_cap_private_pairs(
    world_count: int,
) -> tuple[tuple[int, int], ...]:
    """Return the registered private-pair forest of the sharp witness."""
    sharp_exact_balanced_binary_fixed_cost_cap(world_count)
    return _cap_rows_and_private_pairs(world_count)[1]


def audit_exact_balanced_binary_fixed_cost_cap(
    world_count: int,
) -> ExactBalancedFixedCostCapReceipt:
    """Directly audit one finite sharp witness against the general fixed solver."""
    task = exact_balanced_binary_fixed_cost_cap_witness(world_count)
    private_pairs = exact_balanced_binary_fixed_cost_cap_private_pairs(world_count)
    cap = sharp_exact_balanced_binary_fixed_cost_cap(world_count)
    fixed = fixed_minimum_resolution(task).minimum_cost
    if fixed is None:
        raise ArithmeticError("sharp cap witness is unresolved")

    half = world_count // 2
    balanced = all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 0 for outcome in query.outcomes) == half
        and sum(outcome == 1 for outcome in query.outcomes) == half
        for query in task.queries
    )
    unique_pairs = len(set(tuple(sorted(pair)) for pair in private_pairs)) == len(private_pairs)
    cross_target = all(task.worlds[a].target != task.worlds[b].target for a, b in private_pairs)
    theorem = (
        len(task.queries) == cap
        and fixed == cap
        and balanced
        and unique_pairs
        and cross_target
    )
    if not theorem:
        raise ArithmeticError("sharp exact-balanced fixed-cost cap audit failed")
    return ExactBalancedFixedCostCapReceipt(
        world_count=world_count,
        sharp_fixed_cost_cap=cap,
        witness_query_count=len(task.queries),
        witness_fixed_cost=fixed,
        all_queries_exactly_balanced=balanced,
        all_registered_private_pairs_unique=unique_pairs,
        all_registered_private_pairs_cross_target=cross_target,
        theorem_holds=True,
    )
