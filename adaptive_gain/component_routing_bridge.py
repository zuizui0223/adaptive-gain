"""Prospective component-addressability bridge from topology to finite sensing.

This module defines an explicit NEW bridge axiom for side-theory development.
It is not inferred from PAYOFF's current source semantics.

Component-addressability axiom
-----------------------------
A retained undirected coupling topology is interpreted as follows:

* function nodes in one connected component share one jointly controlled module;
* distinct connected components are independently addressable modules;
* a coarse context observation identifies which module is currently relevant;
* each module has one module-specific terminal cue that resolves the local binary
  target once that module is selected.

Under this axiom a topology with c connected components is mapped to the existing
unit-cost extremal routing family with c branches.  Therefore its exact structural
gap is c-1.  The graph-theoretic consequences are elementary and are not claimed
as independent novelty; the purpose is to put topology mutation accessibility and
finite sensing reachability in one declared state space.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import inf
from typing import Hashable, Iterable, Mapping

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution
from .extremal_routing_family import extremal_routing_task


Node = Hashable
Edge = frozenset[Node]


class ComponentBridgeSearchLimitError(RuntimeError):
    """Raised when exact edge-subset enumeration exceeds the declared cap."""


@dataclass(frozen=True)
class ComponentRoutingReceipt:
    function_count: int
    component_count: int
    adaptive_cost: int
    fixed_cost: int
    structural_gap: int
    expected_adaptive_cost: int
    expected_fixed_cost: int
    theorem_holds: bool


@dataclass(frozen=True)
class SingleEdgeFlipReceipt:
    edge: Edge
    edge_was_present: bool
    before_components: int
    after_components: int
    before_gap: int
    after_gap: int
    delta_gap: int
    flip_class: str


@dataclass(frozen=True)
class GapCutReceipt:
    required_gap: int
    function_count: int
    initial_components: int
    initial_gap: int
    target_components: int
    target_possible: bool
    lower_bound_from_gap_change: int | None
    minimum_edge_mutations: int | None
    coupling_redundancy_overhead: int | None
    witness_deletions: tuple[Edge, ...]

    @property
    def structurally_impossible(self) -> bool:
        return not self.target_possible


def _edge_key(edge: Edge) -> tuple[str, ...]:
    return tuple(sorted(repr(node) for node in edge))


def _normalize_topology(
    adjacency: Mapping[Node, Iterable[Node]],
) -> dict[Node, frozenset[Node]]:
    if not adjacency:
        raise ValueError("topology must contain at least one explicitly declared function node")

    declared = set(adjacency)
    normalized: dict[Node, frozenset[Node]] = {}
    for node, raw_neighbors in adjacency.items():
        neighbors = frozenset(raw_neighbors)
        if node in neighbors:
            raise ValueError(f"self-loop is not allowed for function node {node!r}")
        unknown = neighbors.difference(declared)
        if unknown:
            raise ValueError(
                "all function nodes, including isolated nodes, must be explicit adjacency keys; "
                f"undeclared neighbors from {node!r}: {sorted(map(str, unknown))}"
            )
        normalized[node] = neighbors

    for node, neighbors in normalized.items():
        for neighbor in neighbors:
            if node not in normalized[neighbor]:
                raise ValueError(
                    "coupling topology must be undirected/symmetric: "
                    f"{node!r}->{neighbor!r} lacks reverse edge"
                )
    return normalized


def _component_partition_normalized(
    adjacency: Mapping[Node, frozenset[Node]],
) -> tuple[frozenset[Node], ...]:
    remaining = set(adjacency)
    components: list[frozenset[Node]] = []
    while remaining:
        start = next(iter(remaining))
        stack = [start]
        seen = {start}
        while stack:
            node = stack.pop()
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        remaining.difference_update(seen)
        components.append(frozenset(seen))
    components.sort(key=lambda comp: tuple(sorted(repr(node) for node in comp)))
    return tuple(components)


def component_partition(
    adjacency: Mapping[Node, Iterable[Node]],
) -> tuple[frozenset[Node], ...]:
    """Return connected components of a validated undirected function topology."""

    return _component_partition_normalized(_normalize_topology(adjacency))


def component_count(adjacency: Mapping[Node, Iterable[Node]]) -> int:
    return len(component_partition(adjacency))


def component_structural_gap(adjacency: Mapping[Node, Iterable[Node]]) -> int:
    """Structural gap under the declared component-addressability bridge axiom."""

    return component_count(adjacency) - 1


def _single_component_task() -> FiniteTask:
    return FiniteTask(
        (World("a0", 0), World("b0", 1)),
        (Query("terminal_0", 1, (0, 1)),),
    )


def component_routing_task(adjacency: Mapping[Node, Iterable[Node]]) -> FiniteTask:
    """Map a topology to the declared module-routing task.

    For one connected component there is only one module and no router is needed.
    For c>=2 components, reuse the exact c-branch extremal routing family.
    """

    count = component_count(adjacency)
    if count == 1:
        return _single_component_task()
    return extremal_routing_task(count)


def component_routing_audit(
    adjacency: Mapping[Node, Iterable[Node]],
) -> ComponentRoutingReceipt:
    """Executable proof of g(T)=number_of_components(T)-1 under the bridge axiom."""

    normalized = _normalize_topology(adjacency)
    components = _component_partition_normalized(normalized)
    count = len(components)
    task = _single_component_task() if count == 1 else extremal_routing_task(count)
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive is None or fixed is None:
        raise ArithmeticError("component-routing task unexpectedly failed to resolve")

    expected_adaptive = 1 if count == 1 else 2
    expected_fixed = 1 if count == 1 else count + 1
    gap = fixed - adaptive
    theorem_holds = (
        adaptive == expected_adaptive
        and fixed == expected_fixed
        and gap == count - 1
    )
    if not theorem_holds:
        raise ArithmeticError("component-routing bridge theorem failed executable audit")

    return ComponentRoutingReceipt(
        function_count=len(normalized),
        component_count=count,
        adaptive_cost=adaptive,
        fixed_cost=fixed,
        structural_gap=gap,
        expected_adaptive_cost=expected_adaptive,
        expected_fixed_cost=expected_fixed,
        theorem_holds=theorem_holds,
    )


def _edges(normalized: Mapping[Node, frozenset[Node]]) -> tuple[Edge, ...]:
    edges: set[Edge] = set()
    for node, neighbors in normalized.items():
        for neighbor in neighbors:
            edges.add(frozenset((node, neighbor)))
    return tuple(sorted(edges, key=_edge_key))


def _toggle_edge(
    normalized: Mapping[Node, frozenset[Node]],
    u: Node,
    v: Node,
) -> dict[Node, frozenset[Node]]:
    mutable = {node: set(neighbors) for node, neighbors in normalized.items()}
    if v in mutable[u]:
        mutable[u].remove(v)
        mutable[v].remove(u)
    else:
        mutable[u].add(v)
        mutable[v].add(u)
    return {node: frozenset(neighbors) for node, neighbors in mutable.items()}


def classify_single_edge_flip(
    adjacency: Mapping[Node, Iterable[Node]],
    u: Node,
    v: Node,
) -> SingleEdgeFlipReceipt:
    """Classify the exact structural-gap effect of one retained/released edge flip."""

    normalized = _normalize_topology(adjacency)
    if u == v:
        raise ValueError("edge flip requires two distinct function nodes")
    if u not in normalized or v not in normalized:
        raise ValueError("edge flip endpoints must be declared function nodes")

    before_components = len(_component_partition_normalized(normalized))
    present = v in normalized[u]
    after = _toggle_edge(normalized, u, v)
    after_components = len(_component_partition_normalized(after))
    before_gap = before_components - 1
    after_gap = after_components - 1
    delta = after_gap - before_gap
    if delta not in (-1, 0, 1):
        raise ArithmeticError("one undirected edge flip changed component count by more than one")

    if present and delta == 1:
        flip_class = "bridge_deletion"
    elif present and delta == 0:
        flip_class = "redundant_edge_deletion"
    elif not present and delta == -1:
        flip_class = "component_joining_addition"
    elif not present and delta == 0:
        flip_class = "within_component_addition"
    else:
        raise ArithmeticError("unexpected single-edge component transition")

    return SingleEdgeFlipReceipt(
        edge=frozenset((u, v)),
        edge_was_present=present,
        before_components=before_components,
        after_components=after_components,
        before_gap=before_gap,
        after_gap=after_gap,
        delta_gap=delta,
        flip_class=flip_class,
    )


def _delete_edges(
    normalized: Mapping[Node, frozenset[Node]],
    deleted: Iterable[Edge],
) -> dict[Node, frozenset[Node]]:
    mutable = {node: set(neighbors) for node, neighbors in normalized.items()}
    for edge in deleted:
        if len(edge) != 2:
            raise ValueError("deleted topology edges must contain exactly two endpoints")
        u, v = tuple(edge)
        mutable[u].discard(v)
        mutable[v].discard(u)
    return {node: frozenset(neighbors) for node, neighbors in mutable.items()}


def minimum_edge_mutations_to_required_gap(
    adjacency: Mapping[Node, Iterable[Node]],
    required_gap: int,
    *,
    edge_enumeration_limit: int = 20,
) -> GapCutReceipt:
    """Exact edge-flip distance to a component-routing gap threshold for small graphs.

    Under the bridge axiom, g=c-1.  Any edge addition can only preserve or reduce
    the number of components, so a shortest path to g>=q can be taken to use edge
    deletions only.  The exact distance is therefore the minimum number of retained
    edges whose deletion leaves at least q+1 connected components: the unweighted
    minimum k-cut objective with k=q+1 (generalized to an already-disconnected
    starting topology).

    The implementation enumerates edge subsets and is intended only for finite
    audit fixtures.  Hitting the enumeration cap is an explicit resource limit,
    not an impossibility certificate.
    """

    if not isinstance(required_gap, int) or isinstance(required_gap, bool) or required_gap < 0:
        raise ValueError("required_gap must be a nonnegative integer")
    if not isinstance(edge_enumeration_limit, int) or edge_enumeration_limit < 0:
        raise ValueError("edge_enumeration_limit must be a nonnegative integer")

    normalized = _normalize_topology(adjacency)
    function_count = len(normalized)
    initial_components = len(_component_partition_normalized(normalized))
    initial_gap = initial_components - 1
    target_components = required_gap + 1

    if required_gap <= initial_gap:
        return GapCutReceipt(
            required_gap=required_gap,
            function_count=function_count,
            initial_components=initial_components,
            initial_gap=initial_gap,
            target_components=target_components,
            target_possible=True,
            lower_bound_from_gap_change=0,
            minimum_edge_mutations=0,
            coupling_redundancy_overhead=0,
            witness_deletions=(),
        )

    if target_components > function_count:
        return GapCutReceipt(
            required_gap=required_gap,
            function_count=function_count,
            initial_components=initial_components,
            initial_gap=initial_gap,
            target_components=target_components,
            target_possible=False,
            lower_bound_from_gap_change=None,
            minimum_edge_mutations=None,
            coupling_redundancy_overhead=None,
            witness_deletions=(),
        )

    edges = _edges(normalized)
    if len(edges) > edge_enumeration_limit:
        raise ComponentBridgeSearchLimitError(
            f"exact k-cut audit requires enumerating subsets of {len(edges)} edges; "
            f"declared limit is {edge_enumeration_limit}"
        )

    lower_bound = required_gap - initial_gap
    for deletion_count in range(lower_bound, len(edges) + 1):
        for deleted in combinations(edges, deletion_count):
            reduced = _delete_edges(normalized, deleted)
            components = len(_component_partition_normalized(reduced))
            if components >= target_components:
                return GapCutReceipt(
                    required_gap=required_gap,
                    function_count=function_count,
                    initial_components=initial_components,
                    initial_gap=initial_gap,
                    target_components=target_components,
                    target_possible=True,
                    lower_bound_from_gap_change=lower_bound,
                    minimum_edge_mutations=deletion_count,
                    coupling_redundancy_overhead=deletion_count - lower_bound,
                    witness_deletions=tuple(deleted),
                )

    # Deleting every retained edge yields one component per function node, so the
    # branch above must succeed whenever target_components <= function_count.
    raise ArithmeticError("failed to find a feasible edge-deletion k-cut despite feasible target")


def component_gap_landscape(
    topologies: Mapping[Node, Mapping[Node, Iterable[Node]]],
) -> dict[Node, int]:
    """Compute g(T)=components(T)-1 for a declared family of topology states."""

    if not topologies:
        raise ValueError("topology family must be nonempty")
    return {state: component_structural_gap(graph) for state, graph in topologies.items()}
