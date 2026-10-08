"""Exact uniform-world expected-value envelope for binary decision tasks.

Scope:
- n equiprobable represented worlds (including target-equivalent worlds);
- binary, deterministic, unit-cost queries;
- declared query budget m >= n-1;
- exact guaranteed target resolution;
- arbitrary finite nonincreasing completion value U(c).

The mathematical bound holds for all finite n. This enumeration implementation
intentionally caps n at 14 to avoid uncontrolled combinatorial work.

A tree with j internal nodes has j+1 terminal leaves. To maximize the
uniform-world completion value, assign the n-(j+1) extra represented worlds to
a shallowest target-pure leaf. The fixed cost is at most j; a private-pair
construction realizes C_F=j for every binary tree shape.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from collections.abc import Callable
import math

from .bounded_arity_extremal_bounds import BoundedArityTree, _tree_task
from .core import FiniteTask


@dataclass(frozen=True)
class UniformExpectedEnvelope:
    world_count: int
    query_count: int
    max_arity: int
    optimal_fixed_cost: int
    optimal_leaf_depths: tuple[int, ...]
    duplicate_world_count: int
    optimal_expected_gain: float
    evaluated_depth_profiles: int
    scope: str = "exact_uniform_world_binary_expected_gain_m_at_least_n_minus_one"


@lru_cache(maxsize=None)
def _binary_leaf_depth_profiles(leaf_count: int) -> tuple[tuple[int, ...], ...]:
    """All realizable depth multisets of full rooted binary trees."""
    if leaf_count == 1:
        return ((0,),)
    profiles: set[tuple[int, ...]] = set()
    for left_count in range(1, leaf_count):
        right_count = leaf_count - left_count
        for left in _binary_leaf_depth_profiles(left_count):
            for right in _binary_leaf_depth_profiles(right_count):
                profile = tuple(sorted(
                    tuple(d + 1 for d in left)
                    + tuple(d + 1 for d in right)
                ))
                profiles.add(profile)
    return tuple(sorted(profiles))


def exact_uniform_expected_envelope(
    world_count: int,
    query_count: int,
    completion_value: Callable[[float], float],
) -> UniformExpectedEnvelope:
    """Find the sharp uniform-world expected advantage for m >= n-1.

    Enumerates distinct binary leaf-depth multisets rather than all ordered
    tree shapes. It optimizes over C_F=j between 1 and n-1, so it also allows
    target-equivalent represented worlds to share an early terminal leaf.
    """
    if type(world_count) is not int or not (2 <= world_count <= 14):
        raise ValueError("world_count must be an integer between 2 and 14")
    if type(query_count) is not int or query_count < world_count - 1:
        raise ValueError("this sharp method requires query_count >= world_count - 1")

    values: dict[int, float] = {}
    previous = None
    for depth in range(1, world_count):
        value = float(completion_value(float(depth)))
        if not math.isfinite(value):
            raise ValueError("completion_value must be finite on relevant costs")
        if previous is not None and value > previous + 1e-12:
            raise ValueError("completion_value must be nonincreasing")
        values[depth] = value
        previous = value

    best_gain = -math.inf
    best_fixed = 0
    best_depths: tuple[int, ...] = ()
    tested = 0
    for leaf_count in range(2, world_count + 1):
        fixed_cost = leaf_count - 1
        duplicates = world_count - leaf_count
        for depths in _binary_leaf_depth_profiles(leaf_count):
            tested += 1
            shortest = depths[0]
            expected_value = (
                sum(values[d] for d in depths)
                + duplicates * values[shortest]
            ) / world_count
            advantage = expected_value - values[fixed_cost]
            if advantage > best_gain + 1e-14:
                best_gain = advantage
                best_fixed = fixed_cost
                best_depths = depths

    return UniformExpectedEnvelope(
        world_count=world_count,
        query_count=query_count,
        max_arity=2,
        optimal_fixed_cost=best_fixed,
        optimal_leaf_depths=best_depths,
        duplicate_world_count=world_count - len(best_depths),
        optimal_expected_gain=best_gain,
        evaluated_depth_profiles=tested,
    )


def _tree_for_binary_depth_profile(depths: tuple[int, ...]) -> BoundedArityTree:
    """Make a canonical complete binary prefix tree for a realizable profile."""
    if not depths or any(type(d) is not int or d < 1 for d in depths):
        raise ValueError("depths must be positive integers")
    ordered = tuple(sorted(depths))
    root: dict[str, object] = {}
    code = 0
    prev_depth = ordered[0]
    for index, depth in enumerate(ordered):
        if index:
            code = (code + 1) << (depth - prev_depth)
        word = format(code, f"0{depth}b")
        if len(word) != depth:
            raise ValueError("depth profile violates the prefix-code capacity")
        node = root
        for bit in word[:-1]:
            if bit not in node:
                node[bit] = {}
            child = node[bit]
            if not isinstance(child, dict):
                raise ValueError("depth profile is not prefix-free")
            node = child
        last = word[-1]
        if last in node:
            raise ValueError("repeated prefix-code leaf")
        node[last] = None
        prev_depth = depth

    def realize(node: object) -> BoundedArityTree:
        if node is None:
            return BoundedArityTree()
        if not isinstance(node, dict) or set(node) != {"0", "1"}:
            raise ValueError("profile cannot form a full binary tree")
        return BoundedArityTree((realize(node["0"]), realize(node["1"])))

    return realize(root)


def exact_uniform_expected_witness(receipt: UniformExpectedEnvelope) -> FiniteTask:
    """Build an explicit task attaining the envelope for uniform world weights.

    Requires a query budget within the exact solver implementation's 20-query
    cap. Surplus worlds duplicate the leftmost shortest-depth leaf, so they
    remain equiprobable as represented worlds but target-equivalent.
    """
    if receipt.query_count > 20:
        raise ValueError("explicit FiniteTask requires at most 20 queries")
    tree = _tree_for_binary_depth_profile(receipt.optimal_leaf_depths)
    task, mandatory = _tree_task(
        tree, receipt.world_count, receipt.query_count
    )
    if mandatory != receipt.optimal_fixed_cost:
        raise ArithmeticError("private-pair construction failed")
    if any(len(set(q.outcomes)) > 2 for q in task.queries):
        raise ArithmeticError("binary cue-arity restriction violated")
    return task
