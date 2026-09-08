"""Sharp fixed-query profile for exactly-balanced binary tasks on twelve worlds.

At n=12 the unrestricted binary depth-three extremum reappears inside the exact
50/50 subclass: there is an explicit exact-6/6 witness with

    (C_A, C_F) = (3, 7).

Together with the sharp exact-balanced fixed-cost cap C_F<=9, this yields the
complete profile

    m = 1,2   : 1
    m = 3,4   : 3/2
    m = 5     : 5/3
    m = 6     : 2
    m >= 7    : 7/3.

The seven-query witness also pads by complementary world pairs, proving that
(C_A,C_F)=(3,7) is attainable for every even world count n>=12.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from .balanced_binary_fixed_cost_cap import sharp_exact_balanced_binary_fixed_cost_cap
from .balanced_binary_ten_world_profile import (
    exact_balanced_ten_world_five_query_task,
    exact_balanced_ten_world_six_query_task,
    exact_balanced_ten_world_three_query_task,
)
from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class TwelveWorldSharpProfileReceipt:
    world_count: int
    sharp_profile_prefix: tuple[tuple[int, Fraction], ...]
    all_m_at_least_seven_ratio: Fraction
    fixed_cost_cap: int
    three_query_witness_cost_pair: tuple[int, int]
    five_query_witness_cost_pair: tuple[int, int]
    six_query_witness_cost_pair: tuple[int, int]
    seven_query_witness_cost_pair: tuple[int, int]
    direct_witness_checks_through_m: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_twelve_world_sharp_fixed_m_profile"


def _task_from_rows(targets: tuple[int, ...], rows: tuple[tuple[int, ...], ...]) -> FiniteTask:
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def _append_complementary_world_pair(
    task: FiniteTask,
    zero_target: int,
    one_target: int,
) -> FiniteTask:
    worlds = list(task.worlds)
    worlds.append(World(f"pad_zero_{len(worlds)}", zero_target))
    worlds.append(World(f"pad_one_{len(worlds)}", one_target))
    queries = []
    for query in task.queries:
        queries.append(Query(query.name, query.cost, query.outcomes + (0, 1)))
    return FiniteTask(tuple(worlds), tuple(queries))


def _lift_ten_world_task(task: FiniteTask, zero_target: int, one_target: int) -> FiniteTask:
    if len(task.worlds) != 10:
        raise ValueError("lift expects a ten-world base task")
    return _append_complementary_world_pair(task, zero_target, one_target)


def exact_balanced_twelve_world_three_query_task() -> FiniteTask:
    # In the registered depth-two policy, all-zero routes to target 1 and
    # all-one routes to target 0.
    return _lift_ten_world_task(exact_balanced_ten_world_three_query_task(), 1, 0)


def exact_balanced_twelve_world_five_query_task() -> FiniteTask:
    # Canonical five-query tree leaves: all-zero -> target 0, all-one -> target 5.
    return _lift_ten_world_task(exact_balanced_ten_world_five_query_task(), 0, 5)


def exact_balanced_twelve_world_six_query_task() -> FiniteTask:
    # Canonical six-query tree leaves: all-zero -> target 0, all-one -> target 6.
    return _lift_ten_world_task(exact_balanced_ten_world_six_query_task(), 0, 6)


def exact_balanced_twelve_world_seven_query_task() -> FiniteTask:
    """Exactly-balanced witness with (C_A,C_F)=(3,7)."""
    targets = (0, 0, 1, 1, 2, 3, 4, 5, 4, 7, 6, 7)
    rows = (
        (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1),
        (0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1),
        (0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1),
        (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1),
        (0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1),
        (0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1),
        (0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1),
    )
    return _task_from_rows(targets, rows)


def exact_balanced_depth_three_seven_query_witness(world_count: int) -> FiniteTask:
    """Pad the n=12 (3,7) witness to every even n>=12.

    Each added pair has complementary outcomes on all seven queries.  The
    all-zero member is assigned the target of the all-zero leaf and the all-one
    member the target of the all-one leaf, so the registered complete depth-three
    adaptive policy remains valid.  Original private pairs remain present, so
    C_F stays seven.
    """
    if type(world_count) is not int or world_count < 12 or world_count % 2:
        raise ValueError("world_count must be an even integer at least 12")
    task = exact_balanced_twelve_world_seven_query_task()
    while len(task.worlds) < world_count:
        task = _append_complementary_world_pair(task, 0, 7)
    return task


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


def exact_balanced_twelve_world_sharp_ratio(query_count: int) -> Fraction:
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if query_count <= 2:
        return Fraction(1, 1)
    if query_count <= 4:
        return Fraction(3, 2)
    if query_count == 5:
        return Fraction(5, 3)
    if query_count == 6:
        return Fraction(2, 1)
    return Fraction(7, 3)


def exact_balanced_twelve_world_sharp_witness(query_count: int) -> FiniteTask:
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if query_count <= 2:
        targets = (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1)
        base = _task_from_rows(targets, (targets,))
        return _duplicate_pad(base, query_count)
    if query_count <= 4:
        return _duplicate_pad(exact_balanced_twelve_world_three_query_task(), query_count)
    if query_count == 5:
        return exact_balanced_twelve_world_five_query_task()
    if query_count == 6:
        return exact_balanced_twelve_world_six_query_task()
    return _duplicate_pad(exact_balanced_twelve_world_seven_query_task(), query_count)


def _all_queries_exactly_balanced(task: FiniteTask) -> bool:
    half = len(task.worlds) // 2
    return all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 1 for outcome in query.outcomes) == half
        and sum(outcome == 0 for outcome in query.outcomes) == half
        for query in task.queries
    )


@lru_cache(maxsize=1)
def audit_exact_balanced_twelve_world_sharp_profile() -> TwelveWorldSharpProfileReceipt:
    cap = sharp_exact_balanced_binary_fixed_cost_cap(12)
    if cap != 9:
        raise ArithmeticError("unexpected twelve-world exact-balanced fixed-cost cap")

    three = exact_balanced_twelve_world_three_query_task()
    five = exact_balanced_twelve_world_five_query_task()
    six = exact_balanced_twelve_world_six_query_task()
    seven = exact_balanced_twelve_world_seven_query_task()
    pairs = tuple(
        (
            adaptive_minimum_resolution(task).minimum_worst_path_cost,
            fixed_minimum_resolution(task).minimum_cost,
        )
        for task in (three, five, six, seven)
    )
    if pairs != ((2, 3), (3, 5), (3, 6), (3, 7)):
        raise ArithmeticError("registered twelve-world sharp witnesses changed cost pair")

    direct_through = 9
    for query_count in range(1, direct_through + 1):
        witness = exact_balanced_twelve_world_sharp_witness(query_count)
        if not _all_queries_exactly_balanced(witness):
            raise ArithmeticError("twelve-world sharp witness lost exact 6/6 balance")
        adaptive = adaptive_minimum_resolution(witness).minimum_worst_path_cost
        fixed = fixed_minimum_resolution(witness).minimum_cost
        if adaptive is None or fixed is None:
            raise ArithmeticError("twelve-world sharp witness became unresolved")
        if Fraction(fixed, adaptive) != exact_balanced_twelve_world_sharp_ratio(query_count):
            raise ArithmeticError("twelve-world sharp witness does not attain registered ratio")

    # Upper bounds:
    # * binary depth 1/2/3 flatten to at most 1/3/7 distinct queries;
    # * for adaptive depth >=4, the exact-balanced fixed cap C_F<=9 gives
    #   C_F/C_A<=9/4<7/3.
    theorem = cap == 9 and pairs == ((2, 3), (3, 5), (3, 6), (3, 7))
    if not theorem:
        raise ArithmeticError("twelve-world sharp profile audit failed")

    return TwelveWorldSharpProfileReceipt(
        world_count=12,
        sharp_profile_prefix=(
            (1, Fraction(1, 1)),
            (2, Fraction(1, 1)),
            (3, Fraction(3, 2)),
            (4, Fraction(3, 2)),
            (5, Fraction(5, 3)),
            (6, Fraction(2, 1)),
            (7, Fraction(7, 3)),
        ),
        all_m_at_least_seven_ratio=Fraction(7, 3),
        fixed_cost_cap=cap,
        three_query_witness_cost_pair=(2, 3),
        five_query_witness_cost_pair=(3, 5),
        six_query_witness_cost_pair=(3, 6),
        seven_query_witness_cost_pair=(3, 7),
        direct_witness_checks_through_m=direct_through,
        theorem_holds=True,
    )
