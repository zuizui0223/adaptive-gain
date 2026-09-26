"""Conditional topology-to-sensing reachability utilities.

This module does not construct the biological map psi: topology -> sensing task.
It assumes that exact topology-specific structural gaps have already been supplied
by a separately declared and justified map. It then composes those gaps with an
undirected mutation graph and topology payoffs.

The mathematics is elementary graph theory and a set-valued corollary of the
PAYOFF topology-valley construction. It is side-theory infrastructure, not an
independent novelty claim.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from math import inf, isfinite
from typing import Hashable, Iterable, Mapping


Node = Hashable


@dataclass(frozen=True)
class TopologyRegimeReachability:
    """Exact conditional reachability summary for one source topology."""

    required_gap: int
    capable_nodes: frozenset[Node]
    reachable_capable_nodes: frozenset[Node]
    graph_distance: float
    best_bottleneck_payoff: float | None
    valley_depth: float

    @property
    def structurally_excluded(self) -> bool:
        """True when no topology in the declared family has gap >= required_gap."""

        return not self.capable_nodes

    @property
    def mutation_disconnected(self) -> bool:
        """True when capable topologies exist but none is graph-reachable."""

        return bool(self.capable_nodes) and not self.reachable_capable_nodes

    @property
    def zero_valley_route_exists(self) -> bool:
        """True when some capable topology is reachable without dropping below source payoff."""

        return self.valley_depth == 0.0


def _all_nodes(adjacency: Mapping[Node, Iterable[Node]]) -> set[Node]:
    nodes = set(adjacency)
    for neighbors in adjacency.values():
        nodes.update(neighbors)
    return nodes


def _validated_neighbors(
    adjacency: Mapping[Node, Iterable[Node]],
    gaps: Mapping[Node, int],
    payoffs: Mapping[Node, float],
) -> dict[Node, frozenset[Node]]:
    nodes = _all_nodes(adjacency)
    if not nodes:
        raise ValueError("topology graph must contain at least one node")

    gap_nodes = set(gaps)
    payoff_nodes = set(payoffs)
    if gap_nodes != nodes:
        missing = nodes.difference(gap_nodes)
        extra = gap_nodes.difference(nodes)
        raise ValueError(
            "structural-gap node set must exactly match topology graph nodes; "
            f"missing={sorted(map(str, missing))}, extra={sorted(map(str, extra))}"
        )
    if payoff_nodes != nodes:
        missing = nodes.difference(payoff_nodes)
        extra = payoff_nodes.difference(nodes)
        raise ValueError(
            "payoff node set must exactly match topology graph nodes; "
            f"missing={sorted(map(str, missing))}, extra={sorted(map(str, extra))}"
        )

    normalized: dict[Node, frozenset[Node]] = {}
    for node in nodes:
        neighbors = frozenset(adjacency.get(node, ()))
        if node in neighbors:
            raise ValueError(f"self-loop is not allowed for topology node {node!r}")
        normalized[node] = neighbors

    for node, neighbors in normalized.items():
        for neighbor in neighbors:
            if node not in normalized.get(neighbor, frozenset()):
                raise ValueError(
                    "topology mutation graph must be undirected/symmetric: "
                    f"{node!r}->{neighbor!r} lacks reverse edge"
                )

    for node in nodes:
        gap = gaps[node]
        if not isinstance(gap, int) or isinstance(gap, bool) or gap < 0:
            raise ValueError(f"gap for {node!r} must be a nonnegative integer")
        payoff = float(payoffs[node])
        if not isfinite(payoff):
            raise ValueError(f"payoff for {node!r} must be finite")

    return normalized


def regime_capable_nodes(gaps: Mapping[Node, int], required_gap: int) -> frozenset[Node]:
    """Return topology states whose supplied structural gap meets the target."""

    if not isinstance(required_gap, int) or isinstance(required_gap, bool) or required_gap < 0:
        raise ValueError("required_gap must be a nonnegative integer")
    return frozenset(node for node, gap in gaps.items() if gap >= required_gap)


def _component(adjacency: Mapping[Node, frozenset[Node]], start: Node) -> frozenset[Node]:
    seen = {start}
    queue: deque[Node] = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return frozenset(seen)


def shortest_mutation_distance(
    adjacency: Mapping[Node, frozenset[Node]],
    start: Node,
    targets: frozenset[Node],
) -> float:
    """Minimum number of graph edges from start to any target, or infinity."""

    if start in targets:
        return 0.0
    if not targets:
        return inf

    seen = {start}
    queue: deque[tuple[Node, int]] = deque([(start, 0)])
    while queue:
        node, distance = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor in seen:
                continue
            if neighbor in targets:
                return float(distance + 1)
            seen.add(neighbor)
            queue.append((neighbor, distance + 1))
    return inf


def best_bottleneck_payoff(
    adjacency: Mapping[Node, frozenset[Node]],
    payoffs: Mapping[Node, float],
    start: Node,
    targets: frozenset[Node],
) -> float | None:
    """Maximize the minimum node payoff along a path to any target.

    This is the widest-path / maximin bottleneck problem with node rather than
    edge weights. The start payoff is included in every path bottleneck.
    Returns None when no target is graph-reachable.
    """

    if start in targets:
        return float(payoffs[start])
    if not targets:
        return None

    best: dict[Node, float] = {start: float(payoffs[start])}
    serial = count()
    heap: list[tuple[float, int, Node]] = [(-best[start], next(serial), start)]

    while heap:
        neg_score, _, node = heappop(heap)
        score = -neg_score
        if score < best.get(node, -inf):
            continue
        for neighbor in adjacency[node]:
            candidate = min(score, float(payoffs[neighbor]))
            if candidate > best.get(neighbor, -inf):
                best[neighbor] = candidate
                heappush(heap, (-candidate, next(serial), neighbor))

    target_scores = [best[target] for target in targets if target in best]
    if not target_scores:
        return None
    return max(target_scores)


def topology_regime_reachability(
    adjacency: Mapping[Node, Iterable[Node]],
    payoffs: Mapping[Node, float],
    gaps: Mapping[Node, int],
    start: Node,
    required_gap: int,
) -> TopologyRegimeReachability:
    """Compose a supplied gap landscape with mutation-graph accessibility.

    No topology-to-sensing map is inferred here. `gaps` must be externally
    supplied after that biological bridge has been declared and solved.
    The graph, gap map, and payoff map must describe exactly the same topology
    family; extra nodes are rejected rather than treated as inaccessible states.
    """

    normalized = _validated_neighbors(adjacency, gaps, payoffs)
    if start not in normalized:
        raise ValueError(f"start topology {start!r} is absent from the graph")

    capable = regime_capable_nodes(gaps, required_gap)
    component = _component(normalized, start)
    reachable = frozenset(capable.intersection(component))

    distance = shortest_mutation_distance(normalized, start, reachable)
    bottleneck = best_bottleneck_payoff(normalized, payoffs, start, reachable)

    if bottleneck is None:
        valley = inf
    else:
        valley = max(0.0, float(payoffs[start]) - bottleneck)

    return TopologyRegimeReachability(
        required_gap=required_gap,
        capable_nodes=capable,
        reachable_capable_nodes=reachable,
        graph_distance=distance,
        best_bottleneck_payoff=bottleneck,
        valley_depth=valley,
    )
