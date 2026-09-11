from __future__ import annotations

from math import inf

import pytest

from adaptive_gain.topology_sensing_reachability import (
    best_bottleneck_payoff,
    regime_capable_nodes,
    shortest_mutation_distance,
    topology_regime_reachability,
)


def test_regime_capable_nodes() -> None:
    gaps = {"A": 0, "B": 1, "C": 3}
    assert regime_capable_nodes(gaps, 2) == frozenset({"C"})
    assert regime_capable_nodes(gaps, 0) == frozenset(gaps)


def test_structural_family_exclusion_when_no_topology_meets_q() -> None:
    adjacency = {"A": {"B"}, "B": {"A"}}
    result = topology_regime_reachability(
        adjacency=adjacency,
        payoffs={"A": 10.0, "B": 12.0},
        gaps={"A": 0, "B": 1},
        start="A",
        required_gap=2,
    )
    assert result.structurally_excluded is True
    assert result.mutation_disconnected is False
    assert result.capable_nodes == frozenset()
    assert result.reachable_capable_nodes == frozenset()
    assert result.graph_distance == inf
    assert result.best_bottleneck_payoff is None
    assert result.valley_depth == inf
    assert result.zero_valley_route_exists is False


def test_start_already_regime_capable() -> None:
    adjacency = {"A": {"B"}, "B": {"A"}}
    result = topology_regime_reachability(
        adjacency=adjacency,
        payoffs={"A": 10.0, "B": 8.0},
        gaps={"A": 2, "B": 0},
        start="A",
        required_gap=2,
    )
    assert result.graph_distance == 0.0
    assert result.best_bottleneck_payoff == 10.0
    assert result.valley_depth == 0.0
    assert result.zero_valley_route_exists is True


def test_positive_joint_valley_uses_best_available_path() -> None:
    # Two equal-length routes to capable topology C:
    # A-B-C has bottleneck 8, while A-D-C has bottleneck 9.
    # The exact set-valued valley depth is therefore 10-9 = 1.
    adjacency = {
        "A": {"B", "D"},
        "B": {"A", "C"},
        "D": {"A", "C"},
        "C": {"B", "D"},
    }
    payoffs = {"A": 10.0, "B": 8.0, "D": 9.0, "C": 12.0}
    gaps = {"A": 0, "B": 1, "D": 1, "C": 2}

    result = topology_regime_reachability(adjacency, payoffs, gaps, "A", 2)

    assert result.capable_nodes == frozenset({"C"})
    assert result.reachable_capable_nodes == frozenset({"C"})
    assert result.graph_distance == 2.0
    assert result.best_bottleneck_payoff == 9.0
    assert result.valley_depth == 1.0
    assert result.zero_valley_route_exists is False


def test_zero_valley_route_exactly_matches_above_source_corridor() -> None:
    adjacency = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B"},
    }
    payoffs = {"A": 10.0, "B": 10.5, "C": 11.0}
    gaps = {"A": 0, "B": 1, "C": 2}

    result = topology_regime_reachability(adjacency, payoffs, gaps, "A", 2)

    assert result.graph_distance == 2.0
    assert result.best_bottleneck_payoff == 10.0
    assert result.valley_depth == 0.0
    assert result.zero_valley_route_exists is True


def test_capable_topology_can_exist_but_be_mutation_disconnected() -> None:
    adjacency = {
        "A": {"B"},
        "B": {"A"},
        "C": set(),
    }
    result = topology_regime_reachability(
        adjacency=adjacency,
        payoffs={"A": 10.0, "B": 9.0, "C": 20.0},
        gaps={"A": 0, "B": 0, "C": 3},
        start="A",
        required_gap=2,
    )
    assert result.structurally_excluded is False
    assert result.mutation_disconnected is True
    assert result.capable_nodes == frozenset({"C"})
    assert result.reachable_capable_nodes == frozenset()
    assert result.graph_distance == inf
    assert result.best_bottleneck_payoff is None
    assert result.valley_depth == inf


def test_shortest_distance_and_bottleneck_helpers() -> None:
    adjacency = {
        "A": frozenset({"B", "D"}),
        "B": frozenset({"A", "C"}),
        "D": frozenset({"A", "C"}),
        "C": frozenset({"B", "D"}),
    }
    targets = frozenset({"C"})
    assert shortest_mutation_distance(adjacency, "A", targets) == 2.0
    assert best_bottleneck_payoff(
        adjacency,
        {"A": 10.0, "B": 7.0, "D": 9.0, "C": 12.0},
        "A",
        targets,
    ) == 9.0


def test_graph_validation_requires_undirected_mutation_edges() -> None:
    with pytest.raises(ValueError, match="undirected/symmetric"):
        topology_regime_reachability(
            adjacency={"A": {"B"}, "B": set()},
            payoffs={"A": 0.0, "B": 1.0},
            gaps={"A": 0, "B": 1},
            start="A",
            required_gap=1,
        )


def test_gap_and_payoff_validation() -> None:
    adjacency = {"A": {"B"}, "B": {"A"}}
    with pytest.raises(ValueError, match="nonnegative integer"):
        topology_regime_reachability(
            adjacency,
            {"A": 0.0, "B": 1.0},
            {"A": 0, "B": -1},
            "A",
            1,
        )
    with pytest.raises(ValueError, match="finite"):
        topology_regime_reachability(
            adjacency,
            {"A": 0.0, "B": float("inf")},
            {"A": 0, "B": 1},
            "A",
            1,
        )


def test_gap_and_payoff_node_sets_must_match_graph_exactly() -> None:
    adjacency = {"A": {"B"}, "B": {"A"}}

    with pytest.raises(ValueError, match="structural-gap node set"):
        topology_regime_reachability(
            adjacency=adjacency,
            payoffs={"A": 0.0, "B": 1.0},
            gaps={"A": 0, "B": 1, "ghost": 5},
            start="A",
            required_gap=1,
        )

    with pytest.raises(ValueError, match="payoff node set"):
        topology_regime_reachability(
            adjacency=adjacency,
            payoffs={"A": 0.0, "B": 1.0, "ghost": 9.0},
            gaps={"A": 0, "B": 1},
            start="A",
            required_gap=1,
        )
