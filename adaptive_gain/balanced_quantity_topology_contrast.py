"""Quantity-matched topology contrast for balanced routeability.

This module pairs the existing exactly-balanced unbounded family with a control
that has the *same represented worlds and exactly the same query outcome matrix*.
Only the target/action map is changed.

For routing depth d>=2, k=2**d:

routeable task:
    existing balanced family
    C_F >= k
    C_A <= d+1

matched control:
    target = 0 iff the first two routing bits are equal
    target = 1 otherwise

The first two routing queries therefore resolve the control exactly, while no
single query can resolve it because every declared query is exactly 50/50 but
the matched target classes have sizes k+2 and k. Hence

    C_A(control) = C_F(control) = 2.

The two tasks have:
- identical n and m;
- identical world identities;
- identical query outcome matrix;
- identical per-query marginals and all cue-only joint distributions;
- identical target multiplicities (k+2, k);
- therefore identical target entropy;
- and, because the full vocabulary resolves each target, identical total
  full-vocabulary mutual information I(T;Q_all)=H(T) under the uniform world
  distribution.

Thus low-order environmental quantity and even total available target
information can be held fixed while conditional decision architecture differs.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .balanced_binary_extremal_family import (
    balanced_binary_extremal_task,
    balanced_binary_family_counts,
    balanced_binary_ratio_lower_bound,
)
from .core import FiniteTask, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class BalancedQuantityTopologyContrastReceipt:
    routing_depth: int
    branch_count: int
    world_count: int
    query_count: int
    same_world_names: bool
    same_query_outcome_matrix: bool
    same_query_marginals: bool
    same_target_multiplicities: bool
    routeable_target_multiplicities: tuple[int, int]
    control_target_multiplicities: tuple[int, int]
    same_target_entropy: bool
    same_full_vocabulary_target_information: bool
    control_adaptive_cost: int
    control_fixed_cost: int
    control_exact_no_gain: bool
    routeable_ratio_lower_bound: Fraction
    matched_ratio_gap_lower_bound: Fraction
    direct_routeable_adaptive_cost: int | None
    direct_routeable_fixed_cost: int | None
    direct_check_performed: bool
    theorem_holds: bool
    scope: str = "exact_balanced_quantity_matched_target_topology_contrast"


def _target_multiplicities(task: FiniteTask) -> tuple[int, int]:
    counts: dict[object, int] = {}
    for world in task.worlds:
        counts[world.target] = counts.get(world.target, 0) + 1
    values = tuple(sorted(counts.values(), reverse=True))
    if len(values) != 2:
        raise ArithmeticError("contrast expects exactly two target classes")
    return values  # type: ignore[return-value]


def _query_marginals(task: FiniteTask) -> tuple[tuple[int, int], ...]:
    rows = []
    for query in task.queries:
        zeros = sum(outcome == 0 for outcome in query.outcomes)
        ones = sum(outcome == 1 for outcome in query.outcomes)
        rows.append((zeros, ones))
    return tuple(rows)


def balanced_quantity_matched_control_task(routing_depth: int) -> FiniteTask:
    """Return the target-remapped no-gain control for an explicit balanced task."""
    if type(routing_depth) is not int or routing_depth < 2:
        raise ValueError("routing_depth must be an integer >=2")

    routeable = balanced_binary_extremal_task(routing_depth)
    route0 = routeable.queries[0]
    route1 = routeable.queries[1]

    worlds = tuple(
        World(
            world.name,
            0 if route0.outcomes[i] == route1.outcomes[i] else 1,
        )
        for i, world in enumerate(routeable.worlds)
    )
    return FiniteTask(worlds, routeable.queries)


def balanced_quantity_topology_contrast_audit(
    routing_depth: int,
    *,
    direct_check: bool = True,
) -> BalancedQuantityTopologyContrastReceipt:
    """Audit the matched pair when explicit materialization fits the query cap."""
    if type(routing_depth) is not int or routing_depth < 2:
        raise ValueError("routing_depth must be an integer >=2")

    k, world_count, query_count = balanced_binary_family_counts(routing_depth)
    routeable_ratio_lb = balanced_binary_ratio_lower_bound(routing_depth)

    routeable_ca = routeable_cf = None

    if direct_check:
        routeable = balanced_binary_extremal_task(routing_depth)
        control = balanced_quantity_matched_control_task(routing_depth)

        same_world_names = tuple(w.name for w in routeable.worlds) == tuple(
            w.name for w in control.worlds
        )
        same_query_matrix = all(
            q1.name == q2.name and q1.cost == q2.cost and q1.outcomes == q2.outcomes
            for q1, q2 in zip(routeable.queries, control.queries)
        )
        same_query_marginals = _query_marginals(routeable) == _query_marginals(control)
        routeable_targets = _target_multiplicities(routeable)
        control_targets = _target_multiplicities(control)
        same_target_multiplicities = routeable_targets == control_targets

        control_ca = adaptive_minimum_resolution(control).minimum_worst_path_cost
        control_cf = fixed_minimum_resolution(control).minimum_cost
        if control_ca is None or control_cf is None:
            raise ArithmeticError("matched control must be resolvable")

        routeable_ca = adaptive_minimum_resolution(routeable).minimum_worst_path_cost
        routeable_cf = fixed_minimum_resolution(routeable).minimum_cost

        # Every declared query has two balanced outcome classes of size k+1,
        # whereas the two target classes have sizes k+2 and k. Therefore no
        # single query can resolve the binary target. The first two routing bits
        # do resolve it by construction, so the exact control costs are 2.
        no_single_query_can_resolve = all(
            _query_marginals(control)[i] == (k + 1, k + 1)
            for i in range(len(control.queries))
        )
        control_exact = (
            no_single_query_can_resolve
            and control_ca == 2
            and control_cf == 2
        )

        # The physical query matrix is identical. Under a uniform prior the
        # cue-only joint distribution is therefore identical exactly. Both full
        # vocabularies resolve their targets, and target multiplicities match,
        # so I(T;Q_all)=H(T) is the same in both tasks.
        same_target_entropy = same_target_multiplicities
        same_full_info = same_target_multiplicities

        theorem = (
            same_world_names
            and same_query_matrix
            and same_query_marginals
            and same_target_multiplicities
            and routeable_targets == (k + 2, k)
            and control_targets == (k + 2, k)
            and control_exact
            and routeable_ca is not None
            and routeable_cf is not None
            and routeable_ca <= routing_depth + 1
            and routeable_cf >= k
        )
    else:
        same_world_names = True
        same_query_matrix = True
        same_query_marginals = True
        routeable_targets = (k + 2, k)
        control_targets = (k + 2, k)
        same_target_multiplicities = True
        same_target_entropy = True
        same_full_info = True
        control_ca = 2
        control_cf = 2
        control_exact = True
        theorem = True

    if not theorem:
        raise ArithmeticError("balanced quantity/topology contrast audit failed")

    return BalancedQuantityTopologyContrastReceipt(
        routing_depth=routing_depth,
        branch_count=k,
        world_count=world_count,
        query_count=query_count,
        same_world_names=same_world_names,
        same_query_outcome_matrix=same_query_matrix,
        same_query_marginals=same_query_marginals,
        same_target_multiplicities=same_target_multiplicities,
        routeable_target_multiplicities=routeable_targets,
        control_target_multiplicities=control_targets,
        same_target_entropy=same_target_entropy,
        same_full_vocabulary_target_information=same_full_info,
        control_adaptive_cost=control_ca,
        control_fixed_cost=control_cf,
        control_exact_no_gain=control_exact,
        routeable_ratio_lower_bound=routeable_ratio_lb,
        matched_ratio_gap_lower_bound=routeable_ratio_lb - 1,
        direct_routeable_adaptive_cost=routeable_ca,
        direct_routeable_fixed_cost=routeable_cf,
        direct_check_performed=direct_check,
        theorem_holds=theorem,
    )
