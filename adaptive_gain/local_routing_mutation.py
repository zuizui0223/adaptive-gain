"""Local pruning accessibility inside the k-branch extremal routing task.

The ecological task and cue vocabulary are fixed. Architecture state is the
branch-conditioned acquisition program used after the router. In branch i the
required target-separating terminal q_i is retained as the final acquisition;
other terminal occurrences in that branch are target-irrelevant because they are
constant on the pair (a_i,b_i).

One local routing mutation removes one such irrelevant acquisition occurrence from
one branch. The model therefore studies accessibility of a more efficient
contingent policy under a declared deletion-only wiring mutation graph. It does
not model mutation of PAYOFF topology, sensor invention, query relabelling, or a
general decision-tree local-search process.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import factorial

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


def _validate_k_r(branch_count: int, required_gain: int) -> tuple[int, int]:
    k = branch_count
    r = required_gain
    if type(k) is not int or k < 2:
        raise ValueError("branch_count must be an integer at least 2")
    if type(r) is not int or not (0 <= r <= k - 1):
        raise ValueError("required_gain must be an integer in [0,k-1]")
    return k, r


def initial_full_program_state(branch_count: int) -> RoutingPruningState:
    """Zero-saving branch-conditioned program with all k terminals per branch."""

    if type(branch_count) is not int or branch_count < 2:
        raise ValueError("branch_count must be an integer at least 2")
    return RoutingPruningState(branch_count, (branch_count,) * branch_count)


def optimal_branch_specific_state(branch_count: int) -> RoutingPruningState:
    """Optimal router-plus-one-terminal program."""

    if type(branch_count) is not int or branch_count < 2:
        raise ValueError("branch_count must be an integer at least 2")
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

    To obtain realized gain r, every branch length must be at most k-r. Starting
    from length k in every branch therefore requires at least r deletions in each
    of k branches, and that lower bound is attained by doing exactly those edits.
    """

    k, r = _validate_k_r(branch_count, required_gain)
    return k * r


def gain_at_least_state_count(branch_count: int, required_gain: int) -> int:
    """Number of pruning states with realized structural gain at least r."""

    k, r = _validate_k_r(branch_count, required_gain)
    # g>=r iff every branch length lies in {1,...,k-r}.
    return (k - r) ** k


def exact_gain_state_count(branch_count: int, realized_gain: int) -> int:
    """Number of pruning states with realized structural gain exactly r."""

    k, r = _validate_k_r(branch_count, realized_gain)
    at_least_r = (k - r) ** k
    at_least_next = 0 if r == k - 1 else (k - r - 1) ** k
    return at_least_r - at_least_next


def shortest_pruning_path_count(branch_count: int, required_gain: int) -> int:
    """Number of branch-choice sequences attaining gain r in the minimum k*r edits.

    At minimum distance every branch must be pruned exactly r times, so paths are
    the multinomial interleavings of k groups of r identical branch edits.
    """

    k, r = _validate_k_r(branch_count, required_gain)
    if r == 0:
        return 1
    return factorial(k * r) // (factorial(r) ** k)


def full_program_is_strict_improvement_trap(branch_count: int) -> bool:
    """Whether every one-edit neighbor has the same realized gain as the full state.

    This property is relative to the declared worst-path structural reward. It
    means a dynamics that accepts only strictly gain-increasing one-edit mutants
    cannot leave the full program, even though neutral paths to better policies
    exist.
    """

    state = initial_full_program_state(branch_count)
    return all(
        prune_one_occurrence(state, branch).realized_structural_gain
        == state.realized_structural_gain
        for branch in range(branch_count)
    )


def exhaustive_minimum_local_prunings_for_gain(branch_count: int, required_gain: int) -> int:
    """Small-scope BFS used as an independent executable check of the formula."""

    k, r = _validate_k_r(branch_count, required_gain)
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
    strict_improvement_trapped_at_start: bool
    target_level_state_count: int
    shortest_path_count: int
    theorem_holds: bool


def routing_pruning_accessibility_receipt(
    branch_count: int,
    required_gain: int,
) -> RoutingPruningAccessibilityReceipt:
    """Audit static task structure together with local policy accessibility."""

    k, r = _validate_k_r(branch_count, required_gain)
    minimum = minimum_local_prunings_for_gain(k, r)
    family = extremal_routing_family_audit(k)
    start = initial_full_program_state(k)
    strict_trap = full_program_is_strict_improvement_trap(k)

    theorem_holds = (
        family.adaptive_cost == 2
        and family.fixed_cost == k + 1
        and family.additive_gain == k - 1
        and start.realized_structural_gain == 0
        and start.worst_path_cost == k + 1
        and minimum == k * r
        and strict_trap
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
        strict_improvement_trapped_at_start=strict_trap,
        target_level_state_count=exact_gain_state_count(k, r),
        shortest_path_count=shortest_pruning_path_count(k, r),
        theorem_holds=True,
    )


@dataclass(frozen=True)
class RequiredGapStarScalingReceipt:
    required_gap: int
    branch_count: int
    max_arity: int
    world_count: int
    query_count: int
    productive_frontier_edge_count: int
    adaptive_depth: int
    minimum_local_prunings: int
    neutral_prefix_before_first_gain: int
    shortest_path_count: int
    theorem_holds: bool


def required_gap_query_minimal_star_scaling_receipt(
    required_gap: int,
) -> RequiredGapStarScalingReceipt:
    """Compose the gap-q static Pareto point with the local pruning distance.

    Set k=q+1 and maximum cue arity b=k. The k-branch star routing task then has
    gap q and realizes the query/frontier-minimal depth-2 Pareto point

        (n,m,E,h)=(2q+2,q+2,q+2,2).

    Reaching the full realized policy gain q from the zero-saving branch program
    requires k*q=q(q+1) local pruning mutations under the declared syntax.
    """

    q = required_gap
    if type(q) is not int or q < 1:
        raise ValueError("required_gap must be a positive integer")
    k = q + 1
    expected = (2 * q + 2, q + 2, q + 2, 2)
    frontier = arity_gap_pareto_frontier(q, k)
    coordinates = {
        (
            point.world_count,
            point.query_count,
            point.productive_frontier_edge_count,
            point.adaptive_depth,
        )
        for point in frontier
    }
    if expected not in coordinates:
        raise ArithmeticError("gap-q star task was not on the exact b=q+1 Pareto frontier")

    accessibility = routing_pruning_accessibility_receipt(k, q)
    minimum = q * (q + 1)
    theorem_holds = (
        accessibility.world_count == expected[0]
        and accessibility.query_count == expected[1]
        and accessibility.task_adaptive_optimum == 2
        and accessibility.task_fixed_optimum == q + 2
        and accessibility.task_optimal_gap == q
        and accessibility.minimum_local_prunings == minimum
        and accessibility.neutral_prefix_before_first_gain == q
    )
    if not theorem_holds:
        raise ArithmeticError("required-gap star scaling audit failed")

    return RequiredGapStarScalingReceipt(
        required_gap=q,
        branch_count=k,
        max_arity=k,
        world_count=expected[0],
        query_count=expected[1],
        productive_frontier_edge_count=expected[2],
        adaptive_depth=expected[3],
        minimum_local_prunings=minimum,
        neutral_prefix_before_first_gain=q,
        shortest_path_count=accessibility.shortest_path_count,
        theorem_holds=True,
    )


def canonical_q2_k3_bridge_audit() -> RoutingPruningAccessibilityReceipt:
    """Check the canonical q=2, arity-3 bridge against the exact Pareto theorem."""

    scaling = required_gap_query_minimal_star_scaling_receipt(2)
    if (
        scaling.world_count,
        scaling.query_count,
        scaling.productive_frontier_edge_count,
        scaling.adaptive_depth,
    ) != (6, 4, 4, 2):
        raise ArithmeticError("canonical q=2,k=3 point changed unexpectedly")
    receipt = routing_pruning_accessibility_receipt(3, 2)
    if receipt.minimum_local_prunings != 6:
        raise ArithmeticError("canonical q=2,k=3 local mutation distance was not six")
    return receipt
