from __future__ import annotations

from adaptive_gain.component_context_obligation import (
    compare_context_semantics,
    context_bypass_gap_landscape,
    context_bypassable_component_task,
    context_bypassable_routing_audit,
    minimum_edge_mutations_to_required_gap_context_bypassable,
)
from adaptive_gain.component_routing_bridge import (
    component_gap_landscape,
    component_routing_task,
    minimum_edge_mutations_to_required_gap,
)
from adaptive_gain.declared_topology_sensing_family import (
    build_declared_topology_sensing_family,
    declared_family_regime_reachability,
)
from adaptive_gain.productive_frontier import build_productive_frontier


def _path3():
    return {"A": {"B"}, "B": {"A", "C"}, "C": {"B"}}


def _triangle():
    return {
        "A": {"B", "C"},
        "B": {"A", "C"},
        "C": {"A", "B"},
    }


def _split3():
    return {"A": {"B"}, "B": {"A"}, "C": set()}


def _isolated3():
    return {"A": set(), "B": set(), "C": set()}


def test_same_three_component_topology_has_context_sensitive_fixed_burden() -> None:
    graph = _isolated3()
    comparison = compare_context_semantics(graph)

    assert comparison.component_count == 3
    assert comparison.mandatory_adaptive_cost == comparison.bypassable_adaptive_cost == 2
    assert comparison.mandatory_fixed_cost == 4
    assert comparison.bypassable_fixed_cost == 3
    assert comparison.mandatory_gap == 2
    assert comparison.bypassable_gap == 1
    assert comparison.gap_difference == 1

    # Mandatory semantics retain the context router as a singleton fixed-side
    # obligation.  Bypassable semantics retain only the three terminal obligations.
    assert comparison.mandatory_frontier == (1, 2, 4, 8)
    assert comparison.bypassable_frontier == (2, 4, 8)


def test_bypassable_formula_across_component_counts() -> None:
    connected = context_bypassable_routing_audit(_path3())
    split = context_bypassable_routing_audit(_split3())
    isolated = context_bypassable_routing_audit(_isolated3())

    assert (connected.component_count, connected.adaptive_cost, connected.fixed_cost, connected.structural_gap) == (1, 1, 1, 0)
    assert (split.component_count, split.adaptive_cost, split.fixed_cost, split.structural_gap) == (2, 2, 2, 0)
    assert (isolated.component_count, isolated.adaptive_cost, isolated.fixed_cost, isolated.structural_gap) == (3, 2, 3, 1)


def test_bypassable_task_is_a_valid_declared_joint_kernel_input() -> None:
    task = context_bypassable_component_task(_isolated3())
    family = build_declared_topology_sensing_family({"isolated": task})
    row = family.rows[0]

    assert row.adaptive_cost == 2
    assert row.fixed_cost == 3
    assert row.structural_gap == 1
    assert row.minimal_productive_sets == (2, 4, 8)

    # Direct frontier receipt agrees with the declared-family compression.
    assert tuple(sorted(build_productive_frontier(task).minimal_productive_sets)) == row.minimal_productive_sets


def test_context_semantics_shift_required_cut_order() -> None:
    path_mandatory = minimum_edge_mutations_to_required_gap(_path3(), 1)
    path_bypass = minimum_edge_mutations_to_required_gap_context_bypassable(_path3(), 1)
    assert path_mandatory.minimum_edge_mutations == 1
    assert path_mandatory.target_components == 2
    assert path_bypass.minimum_edge_mutations == 2
    assert path_bypass.target_components == 3

    triangle_mandatory = minimum_edge_mutations_to_required_gap(_triangle(), 1)
    triangle_bypass = minimum_edge_mutations_to_required_gap_context_bypassable(_triangle(), 1)
    assert triangle_mandatory.minimum_edge_mutations == 2
    assert triangle_bypass.minimum_edge_mutations == 3


def test_k4_context_bypass_requires_three_components_not_two() -> None:
    nodes = tuple("ABCD")
    complete = {node: {other for other in nodes if other != node} for node in nodes}

    mandatory = minimum_edge_mutations_to_required_gap(complete, 1)
    bypassable = minimum_edge_mutations_to_required_gap_context_bypassable(complete, 1)

    assert mandatory.target_components == 2
    assert mandatory.minimum_edge_mutations == 3
    assert bypassable.target_components == 3
    assert bypassable.minimum_edge_mutations == 5


def test_same_topology_family_yields_different_regime_capable_sets() -> None:
    topologies = {
        "triangle": _triangle(),
        "path": _path3(),
        "split": _split3(),
        "isolated": _isolated3(),
    }

    mandatory_gaps = component_gap_landscape(topologies)
    bypassable_gaps = context_bypass_gap_landscape(topologies)
    assert mandatory_gaps == {"triangle": 0, "path": 0, "split": 1, "isolated": 2}
    assert bypassable_gaps == {"triangle": 0, "path": 0, "split": 0, "isolated": 1}

    mutation_graph = {
        "triangle": {"path"},
        "path": {"triangle", "split"},
        "split": {"path", "isolated"},
        "isolated": {"split"},
    }
    payoffs = {"triangle": 10.0, "path": 9.0, "split": 12.0, "isolated": 13.0}

    mandatory_tasks = {state: component_routing_task(graph) for state, graph in topologies.items()}
    bypassable_tasks = {state: context_bypassable_component_task(graph) for state, graph in topologies.items()}

    mandatory_family, mandatory_reach = declared_family_regime_reachability(
        mutation_graph,
        payoffs,
        mandatory_tasks,
        "triangle",
        1,
    )
    bypass_family, bypass_reach = declared_family_regime_reachability(
        mutation_graph,
        payoffs,
        bypassable_tasks,
        "triangle",
        1,
    )

    assert mandatory_family.gaps == mandatory_gaps
    assert bypass_family.gaps == bypassable_gaps

    assert mandatory_reach.capable_nodes == frozenset({"split", "isolated"})
    assert mandatory_reach.graph_distance == 2.0
    assert bypass_reach.capable_nodes == frozenset({"isolated"})
    assert bypass_reach.graph_distance == 3.0

    # Both routes cross the same low-payoff path state in this fixture; the
    # difference is structural eligibility, not the payoff landscape itself.
    assert mandatory_reach.valley_depth == bypass_reach.valley_depth == 1.0


def test_bypassable_positive_gap_can_be_structurally_impossible_for_two_functions() -> None:
    graph = {"A": {"B"}, "B": {"A"}}
    receipt = minimum_edge_mutations_to_required_gap_context_bypassable(graph, 1)
    assert receipt.structurally_impossible is True
    assert receipt.target_components == 3
    assert receipt.minimum_edge_mutations is None
