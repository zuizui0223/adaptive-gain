"""Information diagnostics for deterministic finite tasks and selected policies.

These diagnostics are secondary to the guaranteed-resolution theorem. They show
why a routing observation can have zero direct target information while still
being useful for selecting a continuation action.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import fsum, isfinite, log2
from typing import Hashable, Sequence

from .core import AdaptiveNode, FiniteTask


def _weights(task: FiniteTask, weights: Sequence[float] | None) -> tuple[float, ...]:
    if weights is None:
        return (1.0 / len(task.worlds),) * len(task.worlds)
    values = tuple(float(x) for x in weights)
    if len(values) != len(task.worlds) or any(not isfinite(x) or x <= 0 for x in values):
        raise ValueError("weights must be finite, strictly positive, and cover every world")
    # Scale before summing so large but finite user weights cannot overflow and
    # silently create NaN normalized masses.
    scale = max(values)
    scaled = tuple(x / scale for x in values)
    total = fsum(scaled)
    normalized = tuple(x / total for x in scaled)
    if any(not isfinite(x) or x <= 0 for x in normalized):
        raise ValueError("weight normalization failed without preserving every world")
    return normalized


def _entropy(masses) -> float:
    return -fsum(p * log2(p) for p in masses if p > 0)


def _mi(task: FiniteTask, signatures: Sequence[Hashable], weights=None) -> float:
    w = _weights(task, weights)
    target_mass = defaultdict(float)
    obs_mass = defaultdict(float)
    joint = defaultdict(float)
    for world, signature, mass in zip(task.worlds, signatures, w):
        target_mass[world.target] += mass
        obs_mass[signature] += mass
        joint[world.target, signature] += mass
    value = 0.0
    for (target, signature), mass in joint.items():
        value += mass * log2(mass / (target_mass[target] * obs_mass[signature]))
    if value < -1e-10:
        raise ArithmeticError("mutual information became materially negative")
    return max(0.0, value)


def target_entropy_bits(task: FiniteTask, weights=None) -> float:
    w = _weights(task, weights)
    masses = defaultdict(float)
    for world, mass in zip(task.worlds, w):
        masses[world.target] += mass
    return _entropy(masses.values())


def bundle_information_bits(
    task: FiniteTask, bundle: Sequence[str], weights: Sequence[float] | None = None
) -> float:
    lookup = {q.name: q for q in task.queries}
    names = tuple(bundle)
    if len(set(names)) != len(names) or any(name not in lookup for name in names):
        raise ValueError("bundle must contain unique declared query names")
    signatures = tuple(
        tuple(lookup[name].outcomes[i] for name in names)
        for i in range(len(task.worlds))
    )
    return _mi(task, signatures, weights)


def best_fixed_information_bits(task: FiniteTask, budget: int, weights=None) -> float:
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    best = 0.0
    n = len(task.queries)
    for subset in range(1 << n):
        names = tuple(task.queries[j].name for j in range(n) if subset & (1 << j))
        cost = sum(task.queries[j].cost for j in range(n) if subset & (1 << j))
        if cost <= budget:
            best = max(best, bundle_information_bits(task, names, weights))
    return best


def _transcript_for_world(task: FiniteTask, node: AdaptiveNode, world_index: int):
    lookup = {q.name: q for q in task.queries}
    transcript = []
    current = node
    while current.query is not None:
        query = lookup[current.query]
        outcome = query.outcomes[world_index]
        transcript.append((current.query, outcome))
        branches = dict(current.branches)
        if outcome not in branches:
            raise ValueError("policy omits a declared deterministic outcome")
        current = branches[outcome]
    return tuple(transcript)


def policy_information_bits(
    task: FiniteTask, policy: AdaptiveNode, weights: Sequence[float] | None = None
) -> float:
    signatures = tuple(
        _transcript_for_world(task, policy, i) for i in range(len(task.worlds))
    )
    return _mi(task, signatures, weights)


@dataclass(frozen=True)
class RoutingInformationReceipt:
    target_entropy_bits: float
    root_query: str | None
    root_direct_target_information_bits: float
    total_policy_target_information_bits: float
    continuation_target_information_bits: float
    next_action_entropy_bits: float
    branch_dependent_next_action: bool
    zero_direct_information_routing_witness: bool


def routing_information_receipt(
    task: FiniteTask, policy: AdaptiveNode, weights: Sequence[float] | None = None
) -> RoutingInformationReceipt:
    w = _weights(task, weights)
    h = target_entropy_bits(task, w)
    if policy.query is None:
        total = policy_information_bits(task, policy, w)
        return RoutingInformationReceipt(h, None, 0.0, total, total, 0.0, False, False)
    root = policy.query
    direct = bundle_information_bits(task, (root,), w)
    total = policy_information_bits(task, policy, w)
    continuation = total - direct
    if continuation < -1e-10:
        raise ArithmeticError("full policy lost information already present at its root")
    continuation = max(0.0, continuation)
    query = next(q for q in task.queries if q.name == root)
    children = dict(policy.branches)
    action_mass = defaultdict(float)
    for i, mass in enumerate(w):
        outcome = query.outcomes[i]
        child = children[outcome]
        action = child.query if child.query is not None else "__stop__"
        action_mass[action] += mass
    action_entropy = _entropy(action_mass.values())
    branch_dependent = len(action_mass) > 1
    witness = direct <= 1e-12 and continuation > 1e-12 and branch_dependent
    return RoutingInformationReceipt(
        h, root, direct, total, continuation, action_entropy, branch_dependent, witness
    )
