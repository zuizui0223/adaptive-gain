"""Sharp fixed-query profile for exactly-balanced binary tasks on ten worlds.

For n=10, every declared query is binary and globally exact 5/5 balanced.
The sharp ratio is

    m = 1,2   : 1
    m = 3,4   : 3/2
    m = 5     : 5/3
    m >= 6    : 2

The only non-generic obstruction is at adaptive depth three.  The universal
binary flattening bound allows C_F=7 at C_A=3, while the exact-balanced fixed
cost cap also allows C_F=7 in principle.  This module proves that the two
requirements cannot coexist at n=10.

If C_A=3 and C_F=7, an optimal binary tree must be the complete depth-three
tree with seven distinct query labels.  Exact balance at the root puts exactly
five represented worlds in each root half.  Each half therefore has four
nonempty terminal leaves and one duplicated leaf.  Fixed minimality gives a
private cross-target Hamming edge for each query.  In the left half this forces
one cross-leaf edge in each of q1,q3,q4; in the right half, one in each of
q2,q5,q6.  Exhaustively enumerating the possible five-world half-configurations
produces 2,944 distinct six-coordinate count vectors per side, and no left
vector has a right complement summing coordinatewise to five.  Hence globally
5/5 balance is impossible before the root private-pair condition is even used.

Explicit ten-world witnesses attain (C_A,C_F)=(2,3), (3,5), and (3,6).
Duplicate balanced physical query labels pad the declared m without changing
resolution costs.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product

from .balanced_binary_fixed_cost_cap import sharp_exact_balanced_binary_fixed_cost_cap
from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class TenWorldDepthThreeSevenQueryObstructionReceipt:
    left_half_states: int
    right_half_states: int
    complementary_balance_pairs: int
    depth_three_fixed_seven_possible: bool
    theorem_holds: bool
    scope: str = "exact_balanced_binary_ten_world_no_CA3_CF7"


@dataclass(frozen=True)
class TenWorldSharpProfileReceipt:
    world_count: int
    sharp_profile_prefix: tuple[tuple[int, Fraction], ...]
    all_m_at_least_six_ratio: Fraction
    fixed_cost_cap: int
    three_query_witness_cost_pair: tuple[int, int]
    five_query_witness_cost_pair: tuple[int, int]
    six_query_witness_cost_pair: tuple[int, int]
    obstruction_left_states: int
    obstruction_right_states: int
    direct_witness_checks_through_m: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_ten_world_sharp_fixed_m_profile"


def _duplicate_pad(task: FiniteTask, query_count: int) -> FiniteTask:
    if query_count < len(task.queries):
        raise ValueError("query_count cannot be smaller than the base witness")
    if query_count > 20:
        raise ValueError("explicit FiniteTask witness is limited by the 20-query exact-solver cap")
    queries = list(task.queries)
    pad_index = 0
    while len(queries) < query_count:
        source = task.queries[pad_index % len(task.queries)]
        queries.append(Query(f"pad_{pad_index}_{source.name}", 1, source.outcomes))
        pad_index += 1
    return FiniteTask(task.worlds, tuple(queries))


def _task_from_rows(targets: tuple[int, ...], rows: tuple[tuple[int, ...], ...]) -> FiniteTask:
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def exact_balanced_ten_world_three_query_task() -> FiniteTask:
    """Exactly-balanced witness with (C_A,C_F)=(2,3)."""
    targets = (0, 0, 1, 1, 1, 0, 0, 0, 1, 0)
    rows = (
        (0, 0, 0, 0, 1, 1, 1, 1, 0, 1),
        (1, 1, 1, 0, 1, 0, 0, 0, 0, 1),
        (1, 1, 0, 1, 0, 1, 0, 0, 0, 1),
    )
    return _task_from_rows(targets, rows)


def exact_balanced_ten_world_five_query_task() -> FiniteTask:
    """Exactly-balanced witness with (C_A,C_F)=(3,5)."""
    targets = (0, 1, 1, 2, 2, 5, 5, 3, 4, 5)
    rows = (
        (0, 0, 0, 0, 0, 1, 1, 1, 1, 1),
        (0, 0, 0, 1, 1, 0, 0, 1, 1, 1),
        (0, 0, 1, 0, 1, 1, 1, 0, 0, 1),
        (0, 1, 1, 0, 1, 1, 1, 0, 0, 0),
        (1, 1, 0, 0, 0, 0, 1, 0, 1, 1),
    )
    return _task_from_rows(targets, rows)


def exact_balanced_ten_world_six_query_task() -> FiniteTask:
    """Exactly-balanced witness with (C_A,C_F)=(3,6)."""
    targets = (0, 1, 3, 2, 3, 4, 5, 6, 6, 6)
    rows = (
        (0, 0, 0, 0, 0, 1, 1, 1, 1, 1),
        (0, 0, 1, 1, 1, 0, 0, 0, 1, 1),
        (0, 0, 0, 1, 1, 0, 0, 1, 1, 1),
        (0, 1, 0, 1, 1, 0, 0, 0, 1, 1),
        (1, 1, 1, 0, 1, 0, 0, 0, 0, 1),
        (0, 0, 0, 1, 1, 0, 1, 0, 1, 1),
    )
    return _task_from_rows(targets, rows)


def _patterns() -> tuple[tuple[int, ...], ...]:
    return tuple(product((0, 1), repeat=6))


def _left_leaf(pattern: tuple[int, ...]) -> tuple[int, int]:
    q1, _q2, q3, q4, _q5, _q6 = pattern
    return q1, q3 if q1 == 0 else q4


def _right_leaf(pattern: tuple[int, ...]) -> tuple[int, int]:
    _q1, q2, _q3, _q4, q5, q6 = pattern
    return q2, q5 if q2 == 0 else q6


def _cross_leaf_edges(side: str, dimension: int) -> tuple[tuple[int, int], ...]:
    patterns = _patterns()
    lookup = {pattern: index for index, pattern in enumerate(patterns)}
    leaf = _left_leaf if side == "left" else _right_leaf
    edges = []
    for index, pattern in enumerate(patterns):
        if pattern[dimension] != 0:
            continue
        other = list(pattern)
        other[dimension] = 1
        other_index = lookup[tuple(other)]
        if leaf(pattern) != leaf(patterns[other_index]):
            edges.append((index, other_index))
    return tuple(edges)


@lru_cache(maxsize=2)
def _half_count_vectors(side: str) -> frozenset[tuple[int, ...]]:
    """Enumerate every five-world half compatible with the three private edges.

    Coordinates are q1..q6 after fixing the root outcome.  The local required
    private-edge dimensions are q1,q3,q4 on the left and q2,q5,q6 on the right.
    Selecting one witness edge for each required dimension is complete because
    any C_F=7 minimum bundle supplies at least one such edge.  The two terminal
    sibling edges already cover all four local leaves, so their endpoint union
    has size at least four.  With only five worlds per root half, the union of
    all three selected edges can therefore have size only four or five.
    """
    if side == "left":
        dimensions = (0, 2, 3)
        leaf = _left_leaf
    elif side == "right":
        dimensions = (1, 4, 5)
        leaf = _right_leaf
    else:
        raise ValueError("side must be 'left' or 'right'")

    patterns = _patterns()
    edge_lists = tuple(_cross_leaf_edges(side, dimension) for dimension in dimensions)
    states: set[tuple[int, ...]] = set()

    for first in edge_lists[0]:
        for second in edge_lists[1]:
            for third in edge_lists[2]:
                support = set(first + second + third)
                if len(support) > 5:
                    continue
                if len({leaf(patterns[index]) for index in support}) != 4:
                    continue

                base = [
                    sum(patterns[index][coordinate] for index in support)
                    for coordinate in range(6)
                ]
                if len(support) == 5:
                    states.add(tuple(base))
                    continue

                if len(support) != 4:
                    raise ArithmeticError("unexpected private-edge support size")

                # One additional represented world remains.  It may duplicate
                # an existing six-bit signature or introduce a new one.
                for extra in patterns:
                    states.add(tuple(base[i] + extra[i] for i in range(6)))

    return frozenset(states)


@lru_cache(maxsize=1)
def audit_ten_world_no_depth_three_fixed_seven() -> TenWorldDepthThreeSevenQueryObstructionReceipt:
    left = _half_count_vectors("left")
    right = _half_count_vectors("right")
    complements = sum(
        tuple(5 - value for value in left_vector) in right
        for left_vector in left
    )
    theorem = len(left) == 2944 and len(right) == 2944 and complements == 0
    if not theorem:
        raise ArithmeticError("ten-world depth-three/fixed-seven obstruction audit failed")
    return TenWorldDepthThreeSevenQueryObstructionReceipt(
        left_half_states=len(left),
        right_half_states=len(right),
        complementary_balance_pairs=complements,
        depth_three_fixed_seven_possible=False,
        theorem_holds=True,
    )


def exact_balanced_ten_world_sharp_ratio(query_count: int) -> Fraction:
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if query_count <= 2:
        return Fraction(1, 1)
    if query_count <= 4:
        return Fraction(3, 2)
    if query_count == 5:
        return Fraction(5, 3)
    return Fraction(2, 1)


def exact_balanced_ten_world_sharp_witness(query_count: int) -> FiniteTask:
    """Return an explicit witness attaining the sharp ratio for 1<=m<=20."""
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if query_count <= 2:
        targets = (0, 0, 0, 0, 0, 1, 1, 1, 1, 1)
        base = _task_from_rows(targets, (targets,))
        return _duplicate_pad(base, query_count)
    if query_count <= 4:
        return _duplicate_pad(exact_balanced_ten_world_three_query_task(), query_count)
    if query_count == 5:
        return exact_balanced_ten_world_five_query_task()
    return _duplicate_pad(exact_balanced_ten_world_six_query_task(), query_count)


def _all_queries_exactly_balanced(task: FiniteTask) -> bool:
    return all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 1 for outcome in query.outcomes) == 5
        for query in task.queries
    )


@lru_cache(maxsize=1)
def audit_exact_balanced_ten_world_sharp_profile() -> TenWorldSharpProfileReceipt:
    obstruction = audit_ten_world_no_depth_three_fixed_seven()
    cap = sharp_exact_balanced_binary_fixed_cost_cap(10)
    if cap != 7:
        raise ArithmeticError("unexpected ten-world exact-balanced fixed-cost cap")

    three = exact_balanced_ten_world_three_query_task()
    five = exact_balanced_ten_world_five_query_task()
    six = exact_balanced_ten_world_six_query_task()
    three_pair = (
        adaptive_minimum_resolution(three).minimum_worst_path_cost,
        fixed_minimum_resolution(three).minimum_cost,
    )
    five_pair = (
        adaptive_minimum_resolution(five).minimum_worst_path_cost,
        fixed_minimum_resolution(five).minimum_cost,
    )
    six_pair = (
        adaptive_minimum_resolution(six).minimum_worst_path_cost,
        fixed_minimum_resolution(six).minimum_cost,
    )
    if three_pair != (2, 3) or five_pair != (3, 5) or six_pair != (3, 6):
        raise ArithmeticError("registered ten-world sharp witnesses changed cost pair")

    direct_through = 9
    for query_count in range(1, direct_through + 1):
        witness = exact_balanced_ten_world_sharp_witness(query_count)
        if not _all_queries_exactly_balanced(witness):
            raise ArithmeticError("ten-world sharp witness lost exact 5/5 balance")
        adaptive = adaptive_minimum_resolution(witness).minimum_worst_path_cost
        fixed = fixed_minimum_resolution(witness).minimum_cost
        if adaptive is None or fixed is None:
            raise ArithmeticError("ten-world sharp witness became unresolved")
        if Fraction(fixed, adaptive) != exact_balanced_ten_world_sharp_ratio(query_count):
            raise ArithmeticError("ten-world sharp witness does not attain registered ratio")

    # Upper bounds:
    # * m<=2: trivial adaptive/fixed comparison gives ratio <=1.
    # * m=3,4: any binary depth-two tree flattens to <=3 queries, so <=3/2.
    # * m=5: C_A<=2 gives <=3/2; C_A>=3 gives C_F/C_A<=5/3.
    # * m>=6: C_A<=2 gives <=3/2.  At C_A=3, the complete-tree
    #   obstruction excludes C_F=7, so C_F<=6 and the ratio is <=2.
    #   At C_A>=4, the sharp exact-balanced fixed-cost cap C_F<=7 gives
    #   C_F/C_A<=7/4<2.
    theorem = (
        obstruction.theorem_holds
        and cap == 7
        and three_pair == (2, 3)
        and five_pair == (3, 5)
        and six_pair == (3, 6)
    )
    if not theorem:
        raise ArithmeticError("ten-world sharp profile audit failed")

    return TenWorldSharpProfileReceipt(
        world_count=10,
        sharp_profile_prefix=(
            (1, Fraction(1, 1)),
            (2, Fraction(1, 1)),
            (3, Fraction(3, 2)),
            (4, Fraction(3, 2)),
            (5, Fraction(5, 3)),
            (6, Fraction(2, 1)),
        ),
        all_m_at_least_six_ratio=Fraction(2, 1),
        fixed_cost_cap=cap,
        three_query_witness_cost_pair=(2, 3),
        five_query_witness_cost_pair=(3, 5),
        six_query_witness_cost_pair=(3, 6),
        obstruction_left_states=obstruction.left_half_states,
        obstruction_right_states=obstruction.right_half_states,
        direct_witness_checks_through_m=direct_through,
        theorem_holds=True,
    )
