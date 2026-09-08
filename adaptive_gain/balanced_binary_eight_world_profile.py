"""Sharp fixed-query profile for exactly-balanced binary tasks on eight worlds.

The key finite combinatorial object is an irredundant family of balanced cuts.
If a minimum fixed resolver contains ``k`` queries, then deleting any one query
must make some opposite-target world pair unresolved.  That pair is separated
by the deleted query and by no other query in the bundle.  Hence the bundle is
an irredundant family of balanced bipartitions.

For eight worlds there are 35 balanced bipartitions modulo outcome
complementation.  Exhaustively checking all C(35, 6)=1,623,160 six-cut families
shows that none is irredundant, while the registered five-query witness is
irredundant.  Therefore every exactly-balanced eight-world task has C_F <= 5.

Together with the binary depth-two flattening bound and explicit witnesses this
closes the sharp ratio for every declared query count m>=1:

    m = 1,2   : 1
    m = 3,4   : 3/2
    m >= 5    : 5/3

Duplicate physical query labels with identical balanced outcomes can pad a
witness to any larger declared m without changing either optimum.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb

from .balanced_binary_small_scope import (
    canonical_exact_balanced_query_masks,
    exact_balanced_eight_world_five_query_task,
)
from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class EightWorldBalancedCutCapReceipt:
    world_count: int
    balanced_cut_classes: int
    six_cut_families_checked: int
    any_irredundant_six_cut_family: bool
    registered_five_cut_witness_irredundant: bool
    maximum_irredundant_family_size: int
    universal_fixed_cost_upper_bound: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_eight_world_irredundant_cut_cap"


@dataclass(frozen=True)
class EightWorldSharpProfileReceipt:
    world_count: int
    sharp_profile_prefix: tuple[tuple[int, Fraction], ...]
    all_m_at_least_five_ratio: Fraction
    fixed_cost_cap: int
    three_query_witness_cost_pair: tuple[int, int]
    five_query_witness_cost_pair: tuple[int, int]
    direct_witness_checks_through_m: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_eight_world_sharp_fixed_m_profile"


def _pair_order(world_count: int) -> tuple[tuple[int, int], ...]:
    return tuple(combinations(range(world_count), 2))


def _separated_pair_mask(query_mask: int, world_count: int) -> int:
    pair_mask = 0
    for pair_index, (left, right) in enumerate(_pair_order(world_count)):
        if ((query_mask >> left) & 1) != ((query_mask >> right) & 1):
            pair_mask |= 1 << pair_index
    return pair_mask


def _is_irredundant_separator_family(separator_masks: tuple[int, ...]) -> bool:
    """Every member must own at least one pair not separated by the others."""
    size = len(separator_masks)
    prefix = [0] * (size + 1)
    suffix = [0] * (size + 1)
    for index, separator_mask in enumerate(separator_masks):
        prefix[index + 1] = prefix[index] | separator_mask
    for index in range(size - 1, -1, -1):
        suffix[index] = suffix[index + 1] | separator_masks[index]
    return all(
        separator_masks[index] & ~(prefix[index] | suffix[index + 1])
        for index in range(size)
    )


def _query_mask(query: Query) -> int:
    mask = 0
    for world_index, outcome in enumerate(query.outcomes):
        if outcome == 1:
            mask |= 1 << world_index
        elif outcome != 0:
            raise ValueError("registered balanced-binary witnesses must use outcomes 0/1")
    return mask


@lru_cache(maxsize=1)
def audit_eight_world_balanced_cut_cap() -> EightWorldBalancedCutCapReceipt:
    """Exhaustively certify that no irredundant six balanced cuts exist."""
    world_count = 8
    cuts = canonical_exact_balanced_query_masks(world_count)
    if len(cuts) != 35:
        raise ArithmeticError("unexpected eight-world balanced-cut class count")
    separator_masks = tuple(_separated_pair_mask(mask, world_count) for mask in cuts)

    witness = exact_balanced_eight_world_five_query_task()
    witness_separator_masks = tuple(
        _separated_pair_mask(_query_mask(query), world_count)
        for query in witness.queries
    )
    five_irredundant = _is_irredundant_separator_family(witness_separator_masks)

    checked = 0
    six_exists = False
    for indices in combinations(range(len(cuts)), 6):
        checked += 1
        family = tuple(separator_masks[index] for index in indices)
        if _is_irredundant_separator_family(family):
            six_exists = True
            break

    expected = comb(35, 6)
    theorem = (
        checked == expected
        and not six_exists
        and five_irredundant
    )
    if not theorem:
        raise ArithmeticError("eight-world irredundant balanced-cut cap audit failed")
    return EightWorldBalancedCutCapReceipt(
        world_count=8,
        balanced_cut_classes=35,
        six_cut_families_checked=checked,
        any_irredundant_six_cut_family=six_exists,
        registered_five_cut_witness_irredundant=five_irredundant,
        maximum_irredundant_family_size=5,
        universal_fixed_cost_upper_bound=5,
        theorem_holds=True,
    )


def exact_balanced_eight_world_three_query_task() -> FiniteTask:
    """Exactly-balanced witness with (C_A,C_F)=(2,3)."""
    targets = (0, 0, 1, 1, 1, 0, 0, 0)
    outcome_rows = (
        (0, 0, 0, 0, 1, 1, 1, 1),
        (1, 1, 1, 0, 1, 0, 0, 0),
        (1, 1, 0, 1, 0, 1, 0, 0),
    )
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    queries = tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(outcome_rows))
    return FiniteTask(worlds, queries)


def exact_balanced_eight_world_sharp_ratio(query_count: int) -> Fraction:
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if query_count <= 2:
        return Fraction(1, 1)
    if query_count <= 4:
        return Fraction(3, 2)
    return Fraction(5, 3)


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


def exact_balanced_eight_world_sharp_witness(query_count: int) -> FiniteTask:
    """Return an explicit witness attaining the sharp ratio for 1<=m<=20."""
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if query_count <= 2:
        targets = (0, 0, 0, 0, 1, 1, 1, 1)
        worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
        base = FiniteTask(worlds, (Query("q0", 1, targets),))
        return _duplicate_pad(base, query_count)
    if query_count <= 4:
        return _duplicate_pad(exact_balanced_eight_world_three_query_task(), query_count)
    return _duplicate_pad(exact_balanced_eight_world_five_query_task(), query_count)


def _all_queries_exactly_balanced(task: FiniteTask) -> bool:
    half = len(task.worlds) // 2
    return all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 1 for outcome in query.outcomes) == half
        for query in task.queries
    )


@lru_cache(maxsize=1)
def audit_exact_balanced_eight_world_sharp_profile() -> EightWorldSharpProfileReceipt:
    """Combine the cut cap, universal tree bounds, and direct witnesses."""
    cap = audit_eight_world_balanced_cut_cap()
    three = exact_balanced_eight_world_three_query_task()
    five = exact_balanced_eight_world_five_query_task()
    three_pair = (
        adaptive_minimum_resolution(three).minimum_worst_path_cost,
        fixed_minimum_resolution(three).minimum_cost,
    )
    five_pair = (
        adaptive_minimum_resolution(five).minimum_worst_path_cost,
        fixed_minimum_resolution(five).minimum_cost,
    )
    if three_pair != (2, 3) or five_pair != (3, 5):
        raise ArithmeticError("registered eight-world sharp witnesses changed cost pair")

    # Directly regression-check representative declared counts.  The proof for
    # all larger m is analytic: duplicate balanced query labels pad m without
    # changing either optimum.
    direct_through = 8
    for query_count in range(1, direct_through + 1):
        witness = exact_balanced_eight_world_sharp_witness(query_count)
        if not _all_queries_exactly_balanced(witness):
            raise ArithmeticError("sharp witness lost exact 50/50 balance")
        adaptive = adaptive_minimum_resolution(witness).minimum_worst_path_cost
        fixed = fixed_minimum_resolution(witness).minimum_cost
        if adaptive is None or fixed is None:
            raise ArithmeticError("sharp witness became unresolved")
        if Fraction(fixed, adaptive) != exact_balanced_eight_world_sharp_ratio(query_count):
            raise ArithmeticError("sharp witness does not attain registered ratio")

    # Upper bounds:
    # * m<=2: C_A=1 => C_F<=1; otherwise C_F/C_A<=m/2<=1.
    # * m=3,4: binary depth-two flattening gives <=3/2.
    # * m>=5: the exhaustive irredundant-cut theorem gives C_F<=5; if
    #   C_A<=2, flattening gives C_F<=3, and if C_A>=3 the ratio is <=5/3.
    theorem = (
        cap.theorem_holds
        and cap.universal_fixed_cost_upper_bound == 5
        and three_pair == (2, 3)
        and five_pair == (3, 5)
    )
    if not theorem:
        raise ArithmeticError("eight-world sharp profile audit failed")
    return EightWorldSharpProfileReceipt(
        world_count=8,
        sharp_profile_prefix=(
            (1, Fraction(1, 1)),
            (2, Fraction(1, 1)),
            (3, Fraction(3, 2)),
            (4, Fraction(3, 2)),
            (5, Fraction(5, 3)),
        ),
        all_m_at_least_five_ratio=Fraction(5, 3),
        fixed_cost_cap=5,
        three_query_witness_cost_pair=(2, 3),
        five_query_witness_cost_pair=(3, 5),
        direct_witness_checks_through_m=direct_through,
        theorem_holds=True,
    )
