from __future__ import annotations

import pytest

from adaptive_gain.continuation_witnesses import continuation_fixed_cost_collision
from adaptive_gain.core import FiniteTask, World
from adaptive_gain.declared_topology_sensing_family import (
    build_declared_topology_sensing_family,
    declared_family_regime_reachability,
)
from adaptive_gain.topology_sensing_kernel_witnesses import (
    same_frontier_different_adaptive_cost_collision,
)


def test_declared_family_recovers_same_continuation_different_frontier_gap_landscape() -> None:
    strict, bypass = continuation_fixed_cost_collision()
    receipt = build_declared_topology_sensing_family(
        {"strict_topology": strict, "bypass_topology": bypass}
    )

    rows = {row.topology: row for row in receipt.rows}
    assert receipt.continuation_verified is True
    assert rows["strict_topology"].continuation_root_class == rows["bypass_topology"].continuation_root_class
    assert rows["strict_topology"].structural_gap == 1
    assert rows["bypass_topology"].structural_gap == 0
    assert rows["strict_topology"].minimal_productive_sets != rows["bypass_topology"].minimal_productive_sets
    assert receipt.gaps == {"strict_topology": 1, "bypass_topology": 0}


def test_declared_family_recovers_same_frontier_different_continuation_gap_landscape() -> None:
    expensive, cheaper = same_frontier_different_adaptive_cost_collision()
    receipt = build_declared_topology_sensing_family(
        {"expensive": expensive, "cheaper": cheaper}
    )

    rows = {row.topology: row for row in receipt.rows}
    assert rows["expensive"].minimal_productive_sets == rows["cheaper"].minimal_productive_sets == (1, 2, 4)
    assert rows["expensive"].continuation_root_class != rows["cheaper"].continuation_root_class
    assert (rows["expensive"].adaptive_cost, rows["expensive"].fixed_cost, rows["expensive"].structural_gap) == (3, 3, 0)
    assert (rows["cheaper"].adaptive_cost, rows["cheaper"].fixed_cost, rows["cheaper"].structural_gap) == (2, 3, 1)


def test_declared_family_composes_exact_gap_with_mutation_valley() -> None:
    strict, bypass = continuation_fixed_cost_collision()
    family, reachability = declared_family_regime_reachability(
        adjacency={"resident": {"capable"}, "capable": {"resident"}},
        payoffs={"resident": 10.0, "capable": 9.0},
        tasks_by_topology={"resident": bypass, "capable": strict},
        start="resident",
        required_gap=1,
    )

    assert family.gaps == {"resident": 0, "capable": 1}
    assert reachability.capable_nodes == frozenset({"capable"})
    assert reachability.graph_distance == 1.0
    assert reachability.best_bottleneck_payoff == 9.0
    assert reachability.valley_depth == 1.0
    assert reachability.zero_valley_route_exists is False


def test_declared_family_rejects_empty_and_unresolvable_task_maps() -> None:
    with pytest.raises(ValueError, match="nonempty"):
        build_declared_topology_sensing_family({})

    unresolved = FiniteTask(
        worlds=(World("w0", 0), World("w1", 1)),
        queries=(),
    )
    with pytest.raises(ValueError, match="not adaptively resolvable"):
        build_declared_topology_sensing_family({"bad": unresolved})
