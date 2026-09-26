from __future__ import annotations

import pytest

from adaptive_gain.component_routing_bridge import (
    ComponentBridgeSearchLimitError,
    classify_single_edge_flip,
    component_gap_landscape,
    component_partition,
    component_routing_audit,
    component_routing_task,
    component_structural_gap,
    minimum_edge_mutations_to_required_gap,
)
from adaptive_gain.continuation_bisimulation import (
    build_continuation_quotient,
    continuation_quotient_costs,
)
from adaptive_gain.productive_frontier import (
    build_productive_frontier,
    productive_frontier_fixed_minimum_resolution,
)
from adaptive_gain.topology_sensing_reachability import topology_regime_reachability


def _path3():
    return {"A": {"B"}, "B": {"A", "C"}, "C": {"B"}}


def _triangle():
    return {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B"},
    }


def _single_edge_plus_isolate():
    return {"A": {"B"}, "B": {"A"}, "C": set()}


def test_component_routing_exact_gap_is_components_minus_one() -> None:
    connected = component_routing_audit(_path3())
    assert connected.function_count == 3
    assert connected.component_count == 1
    assert connected.adaptive_cost == 1
    assert connected.fixed_cost == 1
    assert connected.structural_gap == 0
    assert connected.theorem_holds is True

    modular = component_routing_audit({"A": set(), "B": set(), "C": set()})
    assert modular.component_count == 3
    assert modular.adaptive_cost == 2
    assert modular.fixed_cost == 4
    assert modular.structural_gap == 2
    assert modular.theorem_holds is True


def test_component_bridge_realizes_the_joint_sufficient_kernel() -> None:
    graph = {"A": set(), "B": set(), "C": set()}
    task = component_routing_task(graph)

    continuation = build_continuation_quotient((task,))
    adaptive_cost = continuation_quotient_costs((task,), continuation)[0]

    frontier = build_productive_frontier(task)
    fixed_cost = productive_frontier_fixed_minimum_resolution(frontier).minimum_cost

    assert adaptive_cost == 2
    assert fixed_cost == 4
    assert fixed_cost - adaptive_cost == component_structural_gap(graph) == 2
    # The c=3 extremal routing realization has one fixed-mandatory router plus
    # three fixed-mandatory module terminals: four singleton frontier edges.
    assert tuple(sorted(frontier.minimal_productive_sets)) == (1, 2, 4, 8)


def test_component_partition_requires_explicit_undirected_node_family() -> None:
    assert component_partition(_single_edge_plus_isolate()) == (
        frozenset({"A", "B"}),
        frozenset({"C"}),
    )
    with pytest.raises(ValueError, match="explicit adjacency keys"):
        component_partition({"A": {"B"}})
    with pytest.raises(ValueError, match="undirected/symmetric"):
        component_partition({"A": {"B"}, "B": set()})
    with pytest.raises(ValueError, match="self-loop"):
        component_partition({"A": {"A"}})


def test_single_edge_flip_classification_exactly_matches_component_change() -> None:
    bridge = classify_single_edge_flip(_path3(), "B", "C")
    assert bridge.edge_was_present is True
    assert bridge.delta_gap == 1
    assert bridge.flip_class == "bridge_deletion"

    redundant = classify_single_edge_flip(_triangle(), "A", "B")
    assert redundant.edge_was_present is True
    assert redundant.delta_gap == 0
    assert redundant.flip_class == "redundant_edge_deletion"

    join = classify_single_edge_flip(_single_edge_plus_isolate(), "B", "C")
    assert join.edge_was_present is False
    assert join.delta_gap == -1
    assert join.flip_class == "component_joining_addition"

    within = classify_single_edge_flip(_path3(), "A", "C")
    assert within.edge_was_present is False
    assert within.delta_gap == 0
    assert within.flip_class == "within_component_addition"


def test_path_and_triangle_have_same_current_gap_but_different_mutation_distance() -> None:
    assert component_structural_gap(_path3()) == 0
    assert component_structural_gap(_triangle()) == 0

    path = minimum_edge_mutations_to_required_gap(_path3(), 1)
    tri = minimum_edge_mutations_to_required_gap(_triangle(), 1)

    assert path.minimum_edge_mutations == 1
    assert path.lower_bound_from_gap_change == 1
    assert path.coupling_redundancy_overhead == 0

    assert tri.minimum_edge_mutations == 2
    assert tri.lower_bound_from_gap_change == 1
    assert tri.coupling_redundancy_overhead == 1


def test_complete_graph_edge_connectivity_controls_first_gap_release() -> None:
    nodes = tuple("ABCD")
    complete = {
        node: {other for other in nodes if other != node}
        for node in nodes
    }
    receipt = minimum_edge_mutations_to_required_gap(complete, 1)
    # K4 has edge connectivity 3: three incident edges must be removed to
    # isolate one function and create the first extra component.
    assert receipt.minimum_edge_mutations == 3
    assert receipt.lower_bound_from_gap_change == 1
    assert receipt.coupling_redundancy_overhead == 2


def test_forest_attains_one_gap_unit_per_edge_deletion() -> None:
    path4 = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B", "D"},
        "D": {"C"},
    }
    receipt = minimum_edge_mutations_to_required_gap(path4, 2)
    assert receipt.initial_gap == 0
    assert receipt.minimum_edge_mutations == 2
    assert receipt.lower_bound_from_gap_change == 2
    assert receipt.coupling_redundancy_overhead == 0
    assert len(receipt.witness_deletions) == 2


def test_gap_above_function_count_is_structurally_impossible() -> None:
    receipt = minimum_edge_mutations_to_required_gap(_path3(), 3)
    assert receipt.structurally_impossible is True
    assert receipt.target_possible is False
    assert receipt.minimum_edge_mutations is None
    assert receipt.lower_bound_from_gap_change is None


def test_already_capable_topology_needs_no_mutation() -> None:
    graph = {"A": set(), "B": set(), "C": set()}
    receipt = minimum_edge_mutations_to_required_gap(graph, 1)
    assert receipt.initial_gap == 2
    assert receipt.minimum_edge_mutations == 0
    assert receipt.witness_deletions == ()


def test_exact_k_cut_audit_has_explicit_resource_limit() -> None:
    nodes = tuple("ABCDEFG")
    complete = {
        node: {other for other in nodes if other != node}
        for node in nodes
    }
    # K7 has 21 retained edges, above the default finite-audit cap of 20.
    with pytest.raises(ComponentBridgeSearchLimitError, match="21 edges"):
        minimum_edge_mutations_to_required_gap(complete, 1)


def test_component_gap_landscape_feeds_joint_topology_reachability() -> None:
    topologies = {
        "triangle": _triangle(),
        "path": _path3(),
        "split": _single_edge_plus_isolate(),
    }
    gaps = component_gap_landscape(topologies)
    assert gaps == {"triangle": 0, "path": 0, "split": 1}

    # One edge deletion takes triangle -> path without changing the component gap;
    # a second deletion takes path -> split.  The only regime-capable topology has
    # higher final payoff, but the route crosses a one-unit intrinsic valley.
    topology_mutation_graph = {
        "triangle": {"path"},
        "path": {"triangle", "split"},
        "split": {"path"},
    }
    payoffs = {"triangle": 10.0, "path": 9.0, "split": 12.0}

    result = topology_regime_reachability(
        topology_mutation_graph,
        payoffs,
        gaps,
        "triangle",
        1,
    )
    assert result.capable_nodes == frozenset({"split"})
    assert result.graph_distance == 2.0
    assert result.best_bottleneck_payoff == 9.0
    assert result.valley_depth == 1.0
    assert result.zero_valley_route_exists is False


def test_required_gap_validation() -> None:
    with pytest.raises(ValueError, match="nonnegative integer"):
        minimum_edge_mutations_to_required_gap(_path3(), -1)
    with pytest.raises(ValueError, match="nonnegative integer"):
        minimum_edge_mutations_to_required_gap(_path3(), True)
