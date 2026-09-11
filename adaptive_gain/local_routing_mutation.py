"""Local pruning accessibility inside the k-branch extremal routing task.

The ecological task and cue vocabulary are fixed.  Architecture state is the
branch-conditioned acquisition program used after the router.  In branch i the
required target-separating terminal q_i is retained as the final acquisition;
other terminal occurrences in that branch are target-irrelevant because they are
constant on the pair (a_i,b_i).

One local routing mutation removes one such irrelevant acquisition occurrence from
one branch.  The model therefore studies accessibility of a more efficient
contingent policy under a declared deletion-only wiring mutation graph.  It does
not model mutation of PAYOFF topology, sensor invention, query relabelling, or a
general decision-tree local-search process.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from .arity_gap_pareto import arity_gap_pareto_frontier
from .extremal_routing_family import extremal_routing_family_audit


@dataclass(frozen=True)
class RoutingPruningState:
    """Branch-program lengths for one target-resolving routing architecture."""

    branch_count: int
    branch_lengths: tuple[int, ...]

    def __post_init__(self) -> None:
        k = self.branch_count
        if type(k) is not int or k < 2:
            raise ValueError("branch_count must be an integer at least 2")
        if len(self.branch_lengths) != k:
            raise ValueError("branch_lengths must contain one entry per branch")
        for length in self.branch_lengths:
            if type(length) is not int or not (1 <= length <= k):
                raise ValueError("each branch length must be an integer in [1,k]")

    @property
    def fixed_task_cost(self) -> int:
        return self.branch_count + 1

    @property
    def worst_path_cost(self) -> int:
        return 1 + max(self.branch_lengths)

    @property
    def realized_structural_gain(self) -> int:
        return self.fixed_task_cost - self.worst_path_cost

    @property
    def optimal_task_gap(self) -> int:
        return self.branch_count - 1

    @property
    def pruned_occurrences(self) -> int:
        k = self.branch_count
        return sum(k - length for length in self.branch_lengths)


def initial_full_program_state(branch_count: int) -> RoutingPruningState:
    """Zero-saving branch-conditioned program with all k terminals per branch."""

    return RoutingPruningState(branch_count, (branch_count,) * branch_count)


def optimal_branch_specific_state(branch_count: int) -> RoutingPruningState:
    """Optimal router-plus-one-terminal program."""

    return RoutingPruningState(branch_count, (1,) * branch_count)


def prune_one_occurrence(state: RoutingPruningState, branch: int) -> RoutingPruningState:
    """Remove one target-irrelevant terminal occurrence from one branch."""

    k = state.branch_count
    if type(branch) is not int or not (0 <= branch < k):
        raise ValueError("branch index out of range")
    lengths = list(state.branch_lengths)
    if lengths[branch] <= 1:
        raise ValueError("branch has no irrelevant terminal occurrence left to prune")
    lengths[branch] -= 1
    return RoutingPruningState(k, tuple(lengths))


def minimum_local_prunings_for_gain(branch_count: int, required_gain: int) -> int:
    """Exact shortest deletion-only mutation distance from the full program.

    To obtain realized gain r, every branch length must be at most k-r.  Starting
    from length k in every branch therefore requires at least r deletions in each
    of k branches, and that lower bound is attained by doing exactly those edits.
    """

    k = branch_count
    r = required_gain
    if type(k) is not int or k < 2:
        raise ValueError("branch_count must be an integer at least 2")
    if type(r) is not int or not (0 <= r <= k - 1):
        raise ValueError("required_gain must be an integer in [0,k-1]")
    return k * r


def exhaustive_minimum_local_prunings_for_gain(branch_count: int, required_gain: int) -> int:
    """Small-scope BFS used as an independent executable check of the formula."""

    k = branch_count
    r = required_gain
    expected = minimum_local_prunings_for_gain(k, r)
    if k > 6:
        raise ValueError("exhaustive audit is restricted to branch_count <= 6")
    start = initial_full_program_state(k)
    if start.realized_structural_gain >= r:
        return 0

    queue: deque[tuple[RoutingPruningState, int]] = deque([(start, 0)])
    seen = {start.branch_lengths}
    while queue:
        state, distance = queue.popleft()
        for branch in range(k):
            if state.branch_lengths[branch] <= 1:
                continue
            nxt = prune_one_occurrence(state, branch)
            if nxt.branch_lengths in seen:
                continue
            if nxt.realized_structural_gain >= r:
                observed = distance + 1
                if observed != expected:
                    raise ArithmeticError("BFS disagreed with exact pruning-distance theorem")
                return observed
            seen.add(nxt.branch_lengths)
            queue.append((nxt, distance + 1))
    raise ArithmeticError("required gain was not reachable in pruning state graph")


@dataclass(frozen=True)
class RoutingPruningAccessibilityReceipt:
    branch_count: int
    required_gain: int
    world_count: int
    query_count: int
    task_adaptive_optimum: int
    task_fixed_optimum: int
    task_optimal_gap: int
    initial_worst_path_cost: int
    target_max_branch_length: int
    minimum_local_prunings: int
    neutral_prefix_before_first_gain: int
    theorem_holds: bool


def routing_pruning_accessibility_receipt(
    branch_count: int,
    required_gain: int,
) -> RoutingPruningAccessibilityReceipt:
    """Audit static task structure together with local policy accessibility."""

    k = branch_count
    r = required_gain
    minimum = minimum_local_prunings_for_gain(k, r)
    family = extremal_routing_family_audit(k)
    start = initial_full_program_state(k)

    theorem_holds = (
        family.adaptive_cost == 2
        and family.fixed_cost == k + 1
        and family.additive_gain == k - 1
        and start.realized_structural_gain == 0
        and start.worst_path_cost == k + 1
        and minimum == k * r
    )
    if not theorem_holds:
        raise ArithmeticError("routing-pruning accessibility audit failed")

    return RoutingPruningAccessibilityReceipt(
        branch_count=k,
        required_gain=r,
        world_count=family.world_count,
        query_count=family.query_count,
        task_adaptive_optimum=family.adaptive_cost,
        task_fixed_optimum=family.fixed_cost,
        task_optimal_gap=family.additive_gain,
        initial_worst_path_cost=start.worst_path_cost,
        target_max_branch_length=k - r,
        minimum_local_prunings=minimum,
        neutral_prefix_before_first_gain=k - 1,
        theorem_holds=True,
    )


def canonical_q2_k3_bridge_audit() -> RoutingPruningAccessibilityReceipt:
    """Check the canonical q=2, arity-3 bridge against the exact Pareto theorem."""

    receipt = routing_pruning_accessibility_receipt(3, 2)
    frontier = arity_gap_pareto_frontier(2, 3)
    coordinates = {
        (
            point.world_count,
            point.query_count,
            point.productive_frontier_edge_count,
            point.adaptive_depth,
        )
        for point in frontier
    }
    if (6, 4, 4, 2) not in coordinates:
        raise ArithmeticError("canonical q=2,k=3 task is not on the exact arity-3 frontier")
    if receipt.minimum_local_prunings != 6:
        raise ArithmeticError("canonical q=2,k=3 local mutation distance was not six")
    return receipt
