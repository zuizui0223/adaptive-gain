from __future__ import annotations

from collections import deque
from itertools import combinations
from math import inf

from adaptive_gain.component_context_obligation import (
    minimum_edge_mutations_to_required_gap_context_bypassable,
)
from adaptive_gain.component_routing_bridge import (
    component_count,
    minimum_edge_mutations_to_required_gap,
)


def _edge_universe(nodes: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(combinations(nodes, 2))


def _adjacency(nodes: tuple[int, ...], edges: frozenset[tuple[int, int]]):
    result = {node: set() for node in nodes}
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return result


def _brute_force_edge_flip_distance(
    nodes: tuple[int, ...],
    start_edges: frozenset[tuple[int, int]],
    target_components: int,
) -> float:
    """Independent BFS over the full retained/released edge-state hypercube."""

    if component_count(_adjacency(nodes, start_edges)) >= target_components:
        return 0.0

    universe = _edge_universe(nodes)
    queue = deque([(start_edges, 0)])
    seen = {start_edges}

    while queue:
        edges, distance = queue.popleft()
        for edge in universe:
            next_edges = set(edges)
            if edge in next_edges:
                next_edges.remove(edge)
            else:
                next_edges.add(edge)
            state = frozenset(next_edges)
            if state in seen:
                continue
            if component_count(_adjacency(nodes, state)) >= target_components:
                return float(distance + 1)
            seen.add(state)
            queue.append((state, distance + 1))
    return inf


def test_cr3_matches_full_edge_flip_bfs_for_all_simple_graphs_through_four_nodes() -> None:
    # This verifies the key exchange argument in CR3 independently of the solver:
    # allowing arbitrary additions/deletions never beats deletion-only search when
    # the target is a lower bound on connected-component count.
    for n in range(1, 5):
        nodes = tuple(range(n))
        universe = _edge_universe(nodes)
        for mask in range(1 << len(universe)):
            start_edges = frozenset(
                edge for index, edge in enumerate(universe) if mask & (1 << index)
            )
            graph = _adjacency(nodes, start_edges)
            for required_gap in range(n):
                target_components = required_gap + 1
                brute = _brute_force_edge_flip_distance(
                    nodes,
                    start_edges,
                    target_components,
                )
                receipt = minimum_edge_mutations_to_required_gap(
                    graph,
                    required_gap,
                    edge_enumeration_limit=len(universe),
                )
                assert receipt.target_possible is True
                assert receipt.minimum_edge_mutations == int(brute)


def test_context_bypass_cut_transform_matches_full_edge_flip_bfs() -> None:
    # Under bypassable context, positive q requires at least q+2 components.
    # Verify the transformed-threshold implementation against the same independent
    # full edge-flip BFS for every labeled simple graph through four function nodes.
    for n in range(1, 5):
        nodes = tuple(range(n))
        universe = _edge_universe(nodes)
        for mask in range(1 << len(universe)):
            start_edges = frozenset(
                edge for index, edge in enumerate(universe) if mask & (1 << index)
            )
            graph = _adjacency(nodes, start_edges)

            zero = minimum_edge_mutations_to_required_gap_context_bypassable(
                graph,
                0,
                edge_enumeration_limit=len(universe),
            )
            assert zero.minimum_edge_mutations == 0

            for required_gap in range(1, max(1, n - 1)):
                target_components = required_gap + 2
                receipt = minimum_edge_mutations_to_required_gap_context_bypassable(
                    graph,
                    required_gap,
                    edge_enumeration_limit=len(universe),
                )
                if target_components > n:
                    assert receipt.structurally_impossible is True
                    assert receipt.minimum_edge_mutations is None
                else:
                    brute = _brute_force_edge_flip_distance(
                        nodes,
                        start_edges,
                        target_components,
                    )
                    assert receipt.target_possible is True
                    assert receipt.minimum_edge_mutations == int(brute)


def test_cr3_impossible_threshold_matches_vertex_count() -> None:
    nodes = (0, 1, 2, 3)
    graph = _adjacency(nodes, frozenset(_edge_universe(nodes)))
    receipt = minimum_edge_mutations_to_required_gap(
        graph,
        required_gap=len(nodes),
        edge_enumeration_limit=len(_edge_universe(nodes)),
    )
    assert receipt.structurally_impossible is True
    assert receipt.minimum_edge_mutations is None
