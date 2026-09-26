"""Context-obligation sensitivity for the prospective component bridge.

The same coupling topology and the same component-addressability story can induce
different fixed-side burdens depending on whether the coarse context cue is
semantically indispensable for interpreting module-specific terminal cues.

Two prospective semantics are kept distinct:

* context-mandatory: the existing component bridge, with g=c-1;
* context-bypassable: all module-specific terminal cues together resolve the
  target without the context cue, with g=max(0,c-2).

Neither semantics is inferred from PAYOFF automatically.  They are declared
bridge models used to expose why the productive-frontier half of the joint
sensing kernel is biologically consequential.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable, Mapping

from .component_routing_bridge import (
    ComponentBridgeSearchLimitError,
    component_count,
    component_routing_task,
    minimum_edge_mutations_to_required_gap,
)
from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution
from .productive_frontier import build_productive_frontier


Node = Hashable


@dataclass(frozen=True)
class ContextBypassRoutingReceipt:
    function_count: int
    component_count: int
    adaptive_cost: int
    fixed_cost: int
    structural_gap: int
    expected_adaptive_cost: int
    expected_fixed_cost: int
    minimal_productive_sets: tuple[int, ...]
    theorem_holds: bool


@dataclass(frozen=True)
class ContextSemanticsComparison:
    component_count: int
    mandatory_adaptive_cost: int
    mandatory_fixed_cost: int
    mandatory_gap: int
    mandatory_frontier: tuple[int, ...]
    bypassable_adaptive_cost: int
    bypassable_fixed_cost: int
    bypassable_gap: int
    bypassable_frontier: tuple[int, ...]
    gap_difference: int


@dataclass(frozen=True)
class ContextBypassGapCutReceipt:
    required_gap: int
    function_count: int
    initial_components: int
    initial_gap: int
    target_components: int
    target_possible: bool
    minimum_edge_mutations: int | None
    witness_deletions: tuple[frozenset[Node], ...]

    @property
    def structurally_impossible(self) -> bool:
        return not self.target_possible


def context_bypassable_component_task(
    adjacency: Mapping[Node, Iterable[Node]],
) -> FiniteTask:
    """Generate the local-terminal variant of the component-routing task.

    With c>=2 independently addressable modules, the adaptive policy first reads
    a c-ary context router and then the active module's terminal cue.  In the fixed
    comparator, however, collecting all c terminal cues is sufficient: target-0
    worlds produce the all-zero terminal vector and target-1 world b_i is uniquely
    marked by terminal_i.  Hence the router is bypassable by the fixed bundle.
    """

    count = component_count(adjacency)
    if count == 1:
        return FiniteTask(
            (World("a0", 0), World("b0", 1)),
            (Query("terminal_0", 1, (0, 1)),),
        )

    worlds = []
    for module in range(count):
        worlds.append(World(f"a{module}", 0))
        worlds.append(World(f"b{module}", 1))

    router_outcomes = []
    for module in range(count):
        router_outcomes.extend((module, module))
    queries = [Query("router", 1, tuple(router_outcomes))]

    for terminal in range(count):
        outcomes = []
        for module in range(count):
            outcomes.extend((0, int(module == terminal)))
        queries.append(Query(f"terminal_{terminal}", 1, tuple(outcomes)))

    return FiniteTask(tuple(worlds), tuple(queries))


def context_bypassable_structural_gap(
    adjacency: Mapping[Node, Iterable[Node]],
) -> int:
    """Closed-form gap under bypassable-context semantics."""

    count = component_count(adjacency)
    return max(0, count - 2)


def context_bypassable_routing_audit(
    adjacency: Mapping[Node, Iterable[Node]],
) -> ContextBypassRoutingReceipt:
    """Executable proof of g=max(0,c-2) under bypassable-context semantics."""

    count = component_count(adjacency)
    task = context_bypassable_component_task(adjacency)
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive is None or fixed is None:
        raise ArithmeticError("context-bypassable component task unexpectedly failed to resolve")

    expected_adaptive = 1 if count == 1 else 2
    expected_fixed = 1 if count == 1 else count
    expected_gap = max(0, count - 2)
    frontier = build_productive_frontier(task)
    theorem_holds = (
        adaptive == expected_adaptive
        and fixed == expected_fixed
        and fixed - adaptive == expected_gap
    )
    if not theorem_holds:
        raise ArithmeticError("context-bypassable component theorem failed executable audit")

    return ContextBypassRoutingReceipt(
        function_count=len(adjacency),
        component_count=count,
        adaptive_cost=adaptive,
        fixed_cost=fixed,
        structural_gap=fixed - adaptive,
        expected_adaptive_cost=expected_adaptive,
        expected_fixed_cost=expected_fixed,
        minimal_productive_sets=tuple(sorted(frontier.minimal_productive_sets)),
        theorem_holds=True,
    )


def compare_context_semantics(
    adjacency: Mapping[Node, Iterable[Node]],
) -> ContextSemanticsComparison:
    """Compare mandatory versus bypassable context on the same topology."""

    mandatory_task = component_routing_task(adjacency)
    bypass_task = context_bypassable_component_task(adjacency)

    mandatory_adaptive = adaptive_minimum_resolution(mandatory_task).minimum_worst_path_cost
    mandatory_fixed = fixed_minimum_resolution(mandatory_task).minimum_cost
    bypass_adaptive = adaptive_minimum_resolution(bypass_task).minimum_worst_path_cost
    bypass_fixed = fixed_minimum_resolution(bypass_task).minimum_cost
    if None in (mandatory_adaptive, mandatory_fixed, bypass_adaptive, bypass_fixed):
        raise ArithmeticError("declared component semantics unexpectedly produced an unresolved task")

    mandatory_frontier = tuple(sorted(build_productive_frontier(mandatory_task).minimal_productive_sets))
    bypass_frontier = tuple(sorted(build_productive_frontier(bypass_task).minimal_productive_sets))

    return ContextSemanticsComparison(
        component_count=component_count(adjacency),
        mandatory_adaptive_cost=mandatory_adaptive,
        mandatory_fixed_cost=mandatory_fixed,
        mandatory_gap=mandatory_fixed - mandatory_adaptive,
        mandatory_frontier=mandatory_frontier,
        bypassable_adaptive_cost=bypass_adaptive,
        bypassable_fixed_cost=bypass_fixed,
        bypassable_gap=bypass_fixed - bypass_adaptive,
        bypassable_frontier=bypass_frontier,
        gap_difference=(mandatory_fixed - mandatory_adaptive) - (bypass_fixed - bypass_adaptive),
    )


def minimum_edge_mutations_to_required_gap_context_bypassable(
    adjacency: Mapping[Node, Iterable[Node]],
    required_gap: int,
    *,
    edge_enumeration_limit: int = 20,
) -> ContextBypassGapCutReceipt:
    """Exact topology-mutation burden under bypassable-context semantics.

    For q>=1, g=max(0,c-2)>=q iff c>=q+2.  Reusing the mandatory-context
    component-cut solver with transformed threshold q+1 therefore computes the
    exact minimum number of retained edges that must be deleted to reach at least
    q+2 components.  q=0 is already satisfied by every declared topology.
    """

    if not isinstance(required_gap, int) or isinstance(required_gap, bool) or required_gap < 0:
        raise ValueError("required_gap must be a nonnegative integer")

    count = component_count(adjacency)
    function_count = len(adjacency)
    initial_gap = max(0, count - 2)
    target_components = 1 if required_gap == 0 else required_gap + 2

    if required_gap == 0 or initial_gap >= required_gap:
        return ContextBypassGapCutReceipt(
            required_gap=required_gap,
            function_count=function_count,
            initial_components=count,
            initial_gap=initial_gap,
            target_components=target_components,
            target_possible=True,
            minimum_edge_mutations=0,
            witness_deletions=(),
        )

    if target_components > function_count:
        return ContextBypassGapCutReceipt(
            required_gap=required_gap,
            function_count=function_count,
            initial_components=count,
            initial_gap=initial_gap,
            target_components=target_components,
            target_possible=False,
            minimum_edge_mutations=None,
            witness_deletions=(),
        )

    # The mandatory solver's transformed threshold r=required_gap+1 asks for
    # r+1=required_gap+2 components, exactly the bypassable-context requirement.
    transformed = minimum_edge_mutations_to_required_gap(
        adjacency,
        required_gap + 1,
        edge_enumeration_limit=edge_enumeration_limit,
    )
    if not transformed.target_possible or transformed.minimum_edge_mutations is None:
        raise ArithmeticError("transformed component-cut solver disagreed with feasible bypass target")

    return ContextBypassGapCutReceipt(
        required_gap=required_gap,
        function_count=function_count,
        initial_components=count,
        initial_gap=initial_gap,
        target_components=target_components,
        target_possible=True,
        minimum_edge_mutations=transformed.minimum_edge_mutations,
        witness_deletions=transformed.witness_deletions,
    )


def context_bypass_gap_landscape(
    topologies: Mapping[Node, Mapping[Node, Iterable[Node]]],
) -> dict[Node, int]:
    if not topologies:
        raise ValueError("topology family must be nonempty")
    return {state: context_bypassable_structural_gap(graph) for state, graph in topologies.items()}
