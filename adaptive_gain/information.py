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



def fixed_information_minimum_cost(
    task: FiniteTask,
    weights: Sequence[float] | None = None,
    *,
    tolerance: float = 1e-10,
) -> int | None:
    """Minimum fixed cost whose bundle contains all target information.

    For deterministic finite tasks and any strictly positive full-support world
    weighting, a fixed bundle resolves the target exactly iff

        I(T; Q_S) = H(T).

    Hence this information-theoretic optimization must equal the ordinary
    fixed minimum-resolution cost.  The tolerance is only for floating-point
    comparison of Shannon quantities; the structural theorem is exact.
    """
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    # Validate full support even when target entropy is already zero.
    _weights(task, weights)
    target_h = target_entropy_bits(task, weights)
    if target_h <= tolerance:
        return 0

    best: int | None = None
    n = len(task.queries)
    for subset in range(1 << n):
        cost = sum(task.queries[j].cost for j in range(n) if subset & (1 << j))
        if best is not None and cost >= best:
            continue
        names = tuple(task.queries[j].name for j in range(n) if subset & (1 << j))
        info = bundle_information_bits(task, names, weights)
        if target_h - info <= tolerance:
            best = cost
    return best


def _history_support_indices(
    task: FiniteTask,
    history: Sequence[tuple[str, Hashable]],
) -> tuple[int, ...]:
    pairs = tuple(history)
    names = tuple(name for name, _ in pairs)
    lookup = {q.name: q for q in task.queries}
    if len(set(names)) != len(names):
        raise ValueError("history cannot query the same cue twice")
    if any(name not in lookup for name in names):
        raise ValueError("history contains an undeclared query")

    indices = tuple(
        i
        for i in range(len(task.worlds))
        if all(lookup[name].outcomes[i] == outcome for name, outcome in pairs)
    )
    if not indices:
        raise ValueError("history has no supporting represented worlds")
    return indices


def _conditioned_weights(
    task: FiniteTask,
    history: Sequence[tuple[str, Hashable]],
    weights: Sequence[float] | None,
) -> tuple[tuple[int, ...], tuple[float, ...]]:
    indices = _history_support_indices(task, history)
    full = _weights(task, weights)
    total = fsum(full[i] for i in indices)
    if total <= 0 or not isfinite(total):
        raise ArithmeticError("history conditioning produced invalid mass")
    return indices, tuple(full[i] / total for i in indices)


def target_entropy_given_history_bits(
    task: FiniteTask,
    history: Sequence[tuple[str, Hashable]],
    weights: Sequence[float] | None = None,
) -> float:
    """Target entropy after one specific realized query-outcome history."""
    indices, masses = _conditioned_weights(task, history, weights)
    target_mass = defaultdict(float)
    for i, mass in zip(indices, masses):
        target_mass[task.worlds[i].target] += mass
    return _entropy(target_mass.values())


def conditional_bundle_information_bits(
    task: FiniteTask,
    bundle: Sequence[str],
    history: Sequence[tuple[str, Hashable]],
    weights: Sequence[float] | None = None,
) -> float:
    """I(T; Q_bundle | one realized history).

    This is deliberately outcome-resolved rather than an average over histories.
    It supports the routeability distinction: the same unobserved query can be
    fully informative after one outcome and irrelevant after another.
    """
    lookup = {q.name: q for q in task.queries}
    names = tuple(bundle)
    if len(set(names)) != len(names) or any(name not in lookup for name in names):
        raise ValueError("bundle must contain unique declared query names")

    indices, masses = _conditioned_weights(task, history, weights)
    target_mass = defaultdict(float)
    obs_mass = defaultdict(float)
    joint = defaultdict(float)
    for i, mass in zip(indices, masses):
        target = task.worlds[i].target
        signature = tuple(lookup[name].outcomes[i] for name in names)
        target_mass[target] += mass
        obs_mass[signature] += mass
        joint[target, signature] += mass

    value = 0.0
    for (target, signature), mass in joint.items():
        value += mass * log2(mass / (target_mass[target] * obs_mass[signature]))
    if value < -1e-10:
        raise ArithmeticError("conditional mutual information became materially negative")
    return max(0.0, value)


@dataclass(frozen=True)
class QueryOutcomeInformationRow:
    outcome: Hashable
    probability: float
    residual_target_entropy_bits: float
    realized_entropy_reduction_bits: float


@dataclass(frozen=True)
class OutcomeResolvedQueryInformationReceipt:
    history: tuple[tuple[str, Hashable], ...]
    query: str
    current_target_entropy_bits: float
    conditional_mutual_information_bits: float
    outcomes: tuple[QueryOutcomeInformationRow, ...]


def outcome_resolved_query_information(
    task: FiniteTask,
    query_name: str,
    history: Sequence[tuple[str, Hashable]] = (),
    weights: Sequence[float] | None = None,
) -> OutcomeResolvedQueryInformationReceipt:
    """Describe the branchwise target uncertainty created by one next query.

    Conditional mutual information is the *average* entropy reduction.  Exact
    worst-case adaptive resolution additionally depends on the separate child
    histories, because different outcomes can make different future cues
    relevant.  This receipt exposes those children instead of collapsing them
    into one scalar.
    """
    lookup = {q.name: q for q in task.queries}
    if query_name not in lookup:
        raise ValueError("query_name must be a declared query")
    hist = tuple(history)
    if query_name in {name for name, _ in hist}:
        raise ValueError("query has already been observed in this history")

    indices, masses = _conditioned_weights(task, hist, weights)
    current_h = target_entropy_given_history_bits(task, hist, weights)
    query = lookup[query_name]
    outcome_mass = defaultdict(float)
    for i, mass in zip(indices, masses):
        outcome_mass[query.outcomes[i]] += mass

    rows = []
    expected_residual_h = 0.0
    for outcome in sorted(outcome_mass, key=repr):
        probability = outcome_mass[outcome]
        child_history = hist + ((query_name, outcome),)
        residual_h = target_entropy_given_history_bits(task, child_history, weights)
        rows.append(
            QueryOutcomeInformationRow(
                outcome=outcome,
                probability=probability,
                residual_target_entropy_bits=residual_h,
                realized_entropy_reduction_bits=current_h - residual_h,
            )
        )
        expected_residual_h += probability * residual_h

    cmi = current_h - expected_residual_h
    if cmi < -1e-10:
        raise ArithmeticError("conditional mutual information became materially negative")
    return OutcomeResolvedQueryInformationReceipt(
        history=hist,
        query=query_name,
        current_target_entropy_bits=current_h,
        conditional_mutual_information_bits=max(0.0, cmi),
        outcomes=tuple(rows),
    )

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
