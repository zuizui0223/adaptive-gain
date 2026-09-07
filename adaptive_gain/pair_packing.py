"""Integral cross-target pair packing certificates for fixed-resolution cost.

A selected cross-target pair consumes one unit of capacity from EVERY query that
separates that pair.  Query q has capacity equal to its positive integer cost.
If K pairs can be packed without exceeding any query capacity, then every fixed
resolving bundle has total cost at least K.

Proof: any fixed resolver must cover every packed pair.  The sum, over selected
queries, of how many packed pairs each query separates is therefore at least K.
By packing feasibility each selected query separates at most cost(q) packed pairs,
so K <= sum_q cost(q).

This is an integral feasible solution to the dual side of the target-pair-cover
relaxation.  It is a sufficient lower-bound certificate, not a claim that the
integral packing bound always equals the fixed optimum.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .core import FiniteTask, adaptive_minimum_resolution


class PairPackingSearchLimitError(RuntimeError):
    """Search cap reached; no negative optimality conclusion is licensed."""


@dataclass(frozen=True)
class PackedPair:
    world_pair: tuple[str, str]
    separator_queries: tuple[str, ...]


@dataclass(frozen=True)
class PairPackingCertificate:
    status: str
    required_lower_bound: int | None
    achieved_lower_bound: int
    packed_pairs: tuple[PackedPair, ...]
    query_loads: tuple[tuple[str, int], ...]
    query_capacities: tuple[tuple[str, int], ...]
    required_bound_certified: bool
    exact_maximum_certified: bool
    search_states: int
    scope: str = "integral_unit_pair_weights_dual_feasible_target_pair_packing"


@dataclass(frozen=True)
class PairPackingAdaptiveGainCertificate:
    status: str
    adaptive_cost: int | None
    required_fixed_lower_bound: int | None
    pair_packing: PairPackingCertificate | None
    strict_adaptive_gain_certified_without_fixed_optimization: bool
    interpretation: str
    scope: str = "integer_cost_selected_adaptive_optimum_plus_integral_pair_packing_lower_bound"


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


def pair_packing_lower_bound(
    task: FiniteTask,
    *,
    required_lower_bound: int | None = None,
    max_search_states: int = 200_000,
) -> PairPackingCertificate:
    """Find a valid integral pair packing; optionally stop once a target bound is met.

    If ``required_lower_bound`` is supplied, the search stops as soon as it finds
    that many packed pairs.  Failure after a COMPLETE search means this integral
    packing certificate cannot reach the requested bound; it does not mean no
    stronger fractional/set-cover lower bound exists.

    With no requested bound the search maximizes the integral packing exactly,
    subject to ``max_search_states``.  Hitting the cap raises rather than returning
    a misleading approximate optimum.
    """
    if required_lower_bound is not None and (
        type(required_lower_bound) is not int or required_lower_bound < 0
    ):
        raise ValueError("required_lower_bound must be a nonnegative integer or None")
    if type(max_search_states) is not int or max_search_states < 1:
        raise ValueError("max_search_states must be a positive integer")

    capacities = tuple(query.cost for query in task.queries)
    rows = _pair_rows(task)
    if not rows:
        satisfied = required_lower_bound in (None, 0)
        return PairPackingCertificate(
            "target_already_identified",
            required_lower_bound,
            0,
            (),
            tuple((q.name, 0) for q in task.queries),
            tuple((q.name, q.cost) for q in task.queries),
            satisfied,
            True,
            1,
        )
    if any(not separators for _, _, separators in rows):
        # The full vocabulary cannot resolve at least one cross-target pair.
        # Infinite/unavailable fixed cost is a different certificate from packing.
        return PairPackingCertificate(
            "unseparable_cross_target_pair",
            required_lower_bound,
            0,
            (),
            tuple((q.name, 0) for q in task.queries),
            tuple((q.name, q.cost) for q in task.queries),
            False,
            True,
            1,
        )

    # Constrained pairs first.  For equal cardinality, prefer pairs consuming less
    # total capacity fraction, which often produces a useful certificate quickly.
    order = sorted(
        range(len(rows)),
        key=lambda k: (
            len(rows[k][2]),
            sum(1 / capacities[q] for q in rows[k][2]),
            rows[k][0],
            rows[k][1],
        ),
    )
    loads = [0] * len(task.queries)
    best: list[int] = []
    states = 0
    target = required_lower_bound
    found_target = False

    def visit(position: int, chosen: list[int]) -> None:
        nonlocal states, best, found_target
        states += 1
        if states > max_search_states:
            raise PairPackingSearchLimitError(
                "pair packing search limit reached; lower-bound optimality not completed"
            )
        if len(chosen) > len(best):
            best = chosen.copy()
            if target is not None and len(best) >= target:
                found_target = True
                return
        if found_target:
            return
        if position == len(order):
            return
        if len(chosen) + (len(order) - position) <= len(best):
            return
        if target is not None and len(chosen) + (len(order) - position) < target:
            return

        row_index = order[position]
        separators = rows[row_index][2]
        if all(loads[q] < capacities[q] for q in separators):
            for q in separators:
                loads[q] += 1
            visit(position + 1, chosen + [row_index])
            for q in separators:
                loads[q] -= 1
            if found_target:
                return
        visit(position + 1, chosen)

    visit(0, [])

    # Reconstruct loads for the retained certificate rather than relying on the
    # backtracking scratch vector, which is zeroed on unwind.
    certificate_loads = [0] * len(task.queries)
    packed = []
    for row_index in best:
        i, j, separators = rows[row_index]
        for q in separators:
            certificate_loads[q] += 1
        packed.append(PackedPair(
            (task.worlds[i].name, task.worlds[j].name),
            tuple(task.queries[q].name for q in separators),
        ))
    if any(load > capacity for load, capacity in zip(certificate_loads, capacities)):
        raise ArithmeticError("constructed pair packing violates query capacity")

    required_ok = target is None or len(best) >= target
    exact = target is None or not found_target
    status = (
        "required_lower_bound_certified"
        if target is not None and required_ok
        else "exact_integral_packing_maximum"
        if target is None
        else "required_bound_not_reached_by_complete_integral_packing_search"
    )
    return PairPackingCertificate(
        status,
        target,
        len(best),
        tuple(packed),
        tuple((task.queries[q].name, certificate_loads[q]) for q in range(len(task.queries))),
        tuple((task.queries[q].name, capacities[q]) for q in range(len(task.queries))),
        required_ok,
        exact,
        states,
    )


def selected_policy_pair_packing_gain_certificate(
    task: FiniteTask,
    *,
    max_search_states: int = 200_000,
) -> PairPackingAdaptiveGainCertificate:
    """Certify C_F>C_A from a pair-packing lower bound, without solving C_F.

    Query costs are positive integers.  If the adaptive optimum is C_A, it is
    enough to certify the integer lower bound C_F >= C_A+1.  A feasible integral
    pair packing of that value proves strict adaptive gain.
    """
    adaptive = adaptive_minimum_resolution(task)
    ca = adaptive.minimum_worst_path_cost
    if ca is None:
        return PairPackingAdaptiveGainCertificate(
            "no_resolving_adaptive_policy",
            None,
            None,
            None,
            False,
            "no adaptive resolver is available to compare against fixed cost",
        )
    required = ca + 1
    packing = pair_packing_lower_bound(
        task,
        required_lower_bound=required,
        max_search_states=max_search_states,
    )
    strict = packing.required_bound_certified
    return PairPackingAdaptiveGainCertificate(
        "strict_gain_certified" if strict else "certificate_incomplete",
        ca,
        required,
        packing,
        strict,
        (
            f"integral pair packing proves fixed cost >= {required} > adaptive cost {ca}"
            if strict
            else "integral pair packing did not reach the strict-gain lower bound; stronger fixed-cost analysis may still succeed"
        ),
    )
