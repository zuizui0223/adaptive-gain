"""Exact rational fractional pair-packing lower bounds for small finite tasks.

The fixed target-resolution problem is a weighted pair cover.  Its LP-dual
relaxation assigns nonnegative weights y_p to cross-target pairs subject to

    sum_{p separated by q} y_p <= cost(q)    for every query q.

Every feasible weighting gives a lower bound on fixed resolving cost.  Because
query costs are integer and fixed bundles have integer total cost,

    C_F >= ceil(sum_p y_p).

This module exactly maximizes that fractional packing for SMALL tasks by
enumerating vertex supports and active query constraints using Fraction arithmetic.
It deliberately has a combinatorial candidate cap and raises rather than silently
returning an approximate optimum when the cap is exceeded.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import comb

from .core import FiniteTask, adaptive_minimum_resolution


class FractionalPackingSearchLimitError(RuntimeError):
    """Exact vertex enumeration would exceed the declared candidate cap."""


@dataclass(frozen=True)
class FractionalPackedPair:
    world_pair: tuple[str, str]
    weight_exact: str
    separator_queries: tuple[str, ...]


@dataclass(frozen=True)
class FractionalPairPackingCertificate:
    status: str
    objective_exact: str | None
    objective_float: float | None
    integer_fixed_cost_lower_bound: int | None
    positive_pairs: tuple[FractionalPackedPair, ...]
    query_loads_exact: tuple[tuple[str, str], ...]
    query_capacities: tuple[tuple[str, int], ...]
    exact_optimum_certified: bool
    basis_candidates_evaluated: int
    scope: str = "exact_rational_fractional_dual_of_declared_target_pair_cover"


@dataclass(frozen=True)
class FractionalPackingAdaptiveGainCertificate:
    status: str
    adaptive_cost: int | None
    fractional_fixed_lower_bound_exact: str | None
    integer_fixed_cost_lower_bound: int | None
    fractional_packing: FractionalPairPackingCertificate | None
    strict_adaptive_gain_certified_without_fixed_integer_optimization: bool
    interpretation: str
    scope: str = "integer_cost_adaptive_optimum_plus_exact_fractional_pair_cover_dual"


def _pair_rows(task: FiniteTask):
    rows = []
    for i, j in combinations(range(len(task.worlds)), 2):
        if task.worlds[i].target == task.worlds[j].target:
            continue
        separators = tuple(
            q for q, query in enumerate(task.queries)
            if query.outcomes[i] != query.outcomes[j]
        )
        rows.append((i, j, separators))
    return tuple(rows)


def _solve_square(matrix, rhs):
    """Exact Gauss-Jordan solve; return None for a singular active basis."""
    n = len(matrix)
    if n == 0:
        return ()
    a = [
        [Fraction(value) for value in row] + [Fraction(rhs_value)]
        for row, rhs_value in zip(matrix, rhs)
    ]
    for column in range(n):
        pivot = next((row for row in range(column, n) if a[row][column] != 0), None)
        if pivot is None:
            return None
        a[column], a[pivot] = a[pivot], a[column]
        scale = a[column][column]
        a[column] = [value / scale for value in a[column]]
        for row in range(n):
            if row == column:
                continue
            factor = a[row][column]
            if factor:
                a[row] = [x - factor * y for x, y in zip(a[row], a[column])]
    return tuple(a[row][-1] for row in range(n))


def _ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def exact_fractional_pair_packing(
    task: FiniteTask,
    *,
    max_basis_candidates: int = 200_000,
) -> FractionalPairPackingCertificate:
    """Solve the fractional pair-cover dual exactly for a small declared task.

    At a vertex with k positive pair weights there are k linearly independent
    active query-capacity constraints.  Enumerating a support of k pairs and k
    active queries therefore covers every vertex.  Zero-weight variables supply
    the remaining nonnegativity constraints.
    """
    if type(max_basis_candidates) is not int or max_basis_candidates < 1:
        raise ValueError("max_basis_candidates must be a positive integer")
    rows = _pair_rows(task)
    if not rows:
        return FractionalPairPackingCertificate(
            "target_already_identified", "0", 0.0, 0, (),
            tuple((q.name, "0") for q in task.queries),
            tuple((q.name, q.cost) for q in task.queries),
            True, 1,
        )
    if any(not separators for _, _, separators in rows):
        return FractionalPairPackingCertificate(
            "unseparable_cross_target_pair", None, None, None, (),
            tuple((q.name, "0") for q in task.queries),
            tuple((q.name, q.cost) for q in task.queries),
            False, 1,
        )

    pair_count = len(rows)
    query_count = len(task.queries)
    max_k = min(pair_count, query_count)
    candidate_count = sum(
        comb(pair_count, k) * comb(query_count, k)
        for k in range(max_k + 1)
    )
    if candidate_count > max_basis_candidates:
        raise FractionalPackingSearchLimitError(
            f"exact fractional packing needs {candidate_count} basis candidates, exceeding cap {max_basis_candidates}"
        )

    incidence = tuple(
        tuple(1 if q in separators else 0 for _, _, separators in rows)
        for q in range(query_count)
    )
    capacities = tuple(Fraction(query.cost) for query in task.queries)
    best_value = Fraction(0)
    best_weights = tuple(Fraction(0) for _ in rows)
    evaluated = 0

    for k in range(max_k + 1):
        for support in combinations(range(pair_count), k):
            for active_queries in combinations(range(query_count), k):
                evaluated += 1
                matrix = tuple(
                    tuple(incidence[q][p] for p in support)
                    for q in active_queries
                )
                solution = _solve_square(matrix, tuple(capacities[q] for q in active_queries))
                if solution is None or any(value < 0 for value in solution):
                    continue
                weights = [Fraction(0) for _ in rows]
                for p, value in zip(support, solution):
                    weights[p] = value
                if any(
                    sum(Fraction(incidence[q][p]) * weights[p] for p in range(pair_count)) > capacities[q]
                    for q in range(query_count)
                ):
                    continue
                objective = sum(weights)
                if objective > best_value:
                    best_value = objective
                    best_weights = tuple(weights)

    loads = tuple(
        sum(Fraction(incidence[q][p]) * best_weights[p] for p in range(pair_count))
        for q in range(query_count)
    )
    if any(load > capacity for load, capacity in zip(loads, capacities)):
        raise ArithmeticError("fractional packing optimum violates a query capacity")
    positive = tuple(
        FractionalPackedPair(
            (task.worlds[i].name, task.worlds[j].name),
            str(best_weights[p]),
            tuple(task.queries[q].name for q in separators),
        )
        for p, (i, j, separators) in enumerate(rows)
        if best_weights[p] > 0
    )
    return FractionalPairPackingCertificate(
        "exact_fractional_optimum",
        str(best_value),
        float(best_value),
        _ceil_fraction(best_value),
        positive,
        tuple((task.queries[q].name, str(loads[q])) for q in range(query_count)),
        tuple((task.queries[q].name, task.queries[q].cost) for q in range(query_count)),
        True,
        evaluated,
    )


def selected_policy_fractional_pair_packing_gain_certificate(
    task: FiniteTask,
    *,
    max_basis_candidates: int = 200_000,
) -> FractionalPackingAdaptiveGainCertificate:
    """Certify strict gain when ceil(fractional fixed lower bound) exceeds C_A."""
    adaptive = adaptive_minimum_resolution(task)
    ca = adaptive.minimum_worst_path_cost
    if ca is None:
        return FractionalPackingAdaptiveGainCertificate(
            "no_resolving_adaptive_policy", None, None, None, None, False,
            "no adaptive resolver is available to compare against fixed cost",
        )
    packing = exact_fractional_pair_packing(task, max_basis_candidates=max_basis_candidates)
    lower = packing.integer_fixed_cost_lower_bound
    strict = lower is not None and lower > ca
    return FractionalPackingAdaptiveGainCertificate(
        "strict_gain_certified" if strict else "certificate_incomplete",
        ca,
        packing.objective_exact,
        lower,
        packing,
        strict,
        (
            f"fractional dual proves integer fixed cost >= {lower} > adaptive cost {ca}"
            if strict
            else "fractional pair-cover relaxation does not separate fixed cost from adaptive cost; integer cover structure may still create strict gain"
        ),
    )
