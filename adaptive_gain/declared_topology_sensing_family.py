"""Exact pipeline for an externally declared topology-to-sensing family.

This module does NOT infer or biologically justify a bridge from architecture
topology to sensing.  It starts only after a caller has supplied one finite
sensing task for every topology in a declared family.

The tasks are compressed through the already-proved joint scalar-cost objects:
continuation structure for adaptive cost and productive frontier for fixed cost.
The resulting exact gap landscape can then be composed with the conditional
mutation-graph reachability utilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable, Mapping

from .continuation_bisimulation import (
    build_continuation_quotient,
    continuation_quotient_costs,
    verify_continuation_quotient,
)
from .core import FiniteTask
from .productive_frontier import (
    build_productive_frontier,
    productive_frontier_fixed_minimum_resolution,
    verify_productive_frontier,
)
from .topology_sensing_reachability import (
    TopologyRegimeReachability,
    topology_regime_reachability,
)


Node = Hashable


@dataclass(frozen=True)
class TopologySensingKernelRow:
    topology: Node
    adaptive_cost: int
    fixed_cost: int
    structural_gap: int
    continuation_root_class: int
    query_names: tuple[str, ...]
    query_costs: tuple[int, ...]
    minimal_productive_sets: tuple[int, ...]


@dataclass(frozen=True)
class DeclaredTopologySensingFamilyReceipt:
    rows: tuple[TopologySensingKernelRow, ...]
    continuation_class_count: int
    continuation_verified: bool
    scope: str = "externally_declared_topology_to_finite_sensing_family"

    @property
    def gaps(self) -> dict[Node, int]:
        return {row.topology: row.structural_gap for row in self.rows}


def build_declared_topology_sensing_family(
    tasks_by_topology: Mapping[Node, FiniteTask],
) -> DeclaredTopologySensingFamilyReceipt:
    """Compute exact structural gaps for a caller-declared topology family.

    The mapping itself is treated as input.  No claim is made that topology
    semantically determines the supplied tasks.
    """

    items = tuple(tasks_by_topology.items())
    if not items:
        raise ValueError("declared topology sensing family must be nonempty")

    topologies = tuple(node for node, _ in items)
    if len(set(topologies)) != len(topologies):
        raise ValueError("topology keys must be unique")
    if any(not isinstance(task, FiniteTask) for _, task in items):
        raise ValueError("every declared topology must map to a FiniteTask")

    tasks = tuple(task for _, task in items)
    continuation = build_continuation_quotient(tasks)
    if not verify_continuation_quotient(tasks, continuation):
        raise ArithmeticError("joint continuation certificate failed verification")
    adaptive_costs = continuation_quotient_costs(tasks, continuation)

    rows: list[TopologySensingKernelRow] = []
    for index, ((topology, task), adaptive_cost) in enumerate(zip(items, adaptive_costs, strict=True)):
        if adaptive_cost is None:
            raise ValueError(f"declared sensing task for topology {topology!r} is not adaptively resolvable")

        frontier = build_productive_frontier(task)
        if not verify_productive_frontier(task, frontier):
            raise ArithmeticError(f"productive frontier failed verification for topology {topology!r}")
        fixed_cost = productive_frontier_fixed_minimum_resolution(frontier).minimum_cost
        if fixed_cost is None:
            raise ValueError(f"declared sensing task for topology {topology!r} is not fixed-resolvable")
        if adaptive_cost > fixed_cost:
            raise ArithmeticError("adaptive cost cannot exceed fixed cost")

        rows.append(
            TopologySensingKernelRow(
                topology=topology,
                adaptive_cost=adaptive_cost,
                fixed_cost=fixed_cost,
                structural_gap=fixed_cost - adaptive_cost,
                continuation_root_class=continuation.root_classes[index],
                query_names=frontier.query_names,
                query_costs=frontier.query_costs,
                minimal_productive_sets=frontier.minimal_productive_sets,
            )
        )

    return DeclaredTopologySensingFamilyReceipt(
        rows=tuple(rows),
        continuation_class_count=len(continuation.classes),
        continuation_verified=True,
    )


def declared_family_regime_reachability(
    adjacency: Mapping[Node, Iterable[Node]],
    payoffs: Mapping[Node, float],
    tasks_by_topology: Mapping[Node, FiniteTask],
    start: Node,
    required_gap: int,
) -> tuple[DeclaredTopologySensingFamilyReceipt, TopologyRegimeReachability]:
    """Compose a declared sensing family with mutation-graph regime reachability."""

    family = build_declared_topology_sensing_family(tasks_by_topology)
    reachability = topology_regime_reachability(
        adjacency=adjacency,
        payoffs=payoffs,
        gaps=family.gaps,
        start=start,
        required_gap=required_gap,
    )
    return family, reachability
