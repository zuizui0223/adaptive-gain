"""Exact global resource-renaming quotient of resource-labelled continuation.

A physical query token may be renamed, but one GLOBAL cost-preserving bijection
must be used consistently at every reachable state.  This keeps cross-branch
resource reuse and capacity intact while forgetting arbitrary query names/order.

The underlying resource-labelled continuation certificate is already the verified
joint-sufficient representation for deterministic guaranteed resolution.  This
module quotients only its global resource labels, so isomorphic tasks have the same
adaptive and fixed costs.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from math import factorial

from .core import FiniteTask, adaptive_gain_receipt
from .resource_continuation import (
    ResourceContinuationCertificate,
    build_resource_continuation_quotient,
    verify_resource_continuation_quotient,
)


class ResourceTransitionIsomorphismLimitError(RuntimeError):
    """Exact cost-preserving global query renaming exceeded the declared cap."""


@dataclass(frozen=True)
class CanonicalResourceTransitionSignature:
    signature: tuple
    query_to_canonical: tuple[int, ...]
    cost_class_sizes: tuple[int, ...]
    permutations_examined: int
    scope: str = "exact_global_cost_preserving_resource_transition_canonicalization"


@dataclass(frozen=True)
class ResourceTransitionIsomorphismWitness:
    left_to_right_query: tuple[int, ...]
    scope: str = "explicit_global_resource_bijection_between_verified_transition_quotients"


@dataclass(frozen=True)
class ResourceTransitionIsomorphismAudit:
    isomorphic: bool
    left_costs: tuple[int | None, int | None]
    right_costs: tuple[int | None, int | None]
    costs_agree_when_isomorphic: bool
    witness: ResourceTransitionIsomorphismWitness | None
    scope: str = "joint_adaptive_fixed_cost_audit_under_global_resource_transition_isomorphism"


def _cost_groups(costs: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    groups: dict[int, list[int]] = {}
    for q, cost in enumerate(costs):
        groups.setdefault(cost, []).append(q)
    return tuple(tuple(groups[cost]) for cost in sorted(groups))


def _candidate_mappings(groups: tuple[tuple[int, ...], ...], qn: int):
    families = tuple(tuple(permutations(group)) for group in groups)
    for selected in product(*families):
        mapping = list(range(qn))
        for group, image in zip(groups, selected):
            for old, new in zip(group, image):
                mapping[old] = new
        yield tuple(mapping)


def _permutation_count(groups: tuple[tuple[int, ...], ...]) -> int:
    result = 1
    for group in groups:
        result *= factorial(len(group))
    return result


def _root_type(
    certificate: ResourceContinuationCertificate,
    mapping: tuple[int, ...],
) -> tuple:
    types: list[tuple] = [("R",)]
    for cls in certificate.classes[1:]:
        rows = []
        for action in cls.actions:
            rows.append((
                "Q",
                mapping[action.query_index],
                action.cost,
                tuple(types[child] for child in action.child_classes),
            ))
        types.append(("M", tuple(sorted(rows, key=repr))))
    return types[certificate.root_class]


def canonical_resource_transition_signature(
    task: FiniteTask,
    *,
    max_permutations: int = 100_000,
) -> CanonicalResourceTransitionSignature:
    """Canonicalize one verified resource-labelled transition system."""
    if not isinstance(task, FiniteTask):
        raise ValueError("task must be a FiniteTask")
    if type(max_permutations) is not int or max_permutations < 1:
        raise ValueError("max_permutations must be a positive integer")
    certificate = build_resource_continuation_quotient(task)
    if not verify_resource_continuation_quotient(task, certificate):
        raise ArithmeticError("resource continuation certificate failed verification")
    groups = _cost_groups(certificate.query_costs)
    count = _permutation_count(groups)
    if count > max_permutations:
        raise ResourceTransitionIsomorphismLimitError(
            f"exact resource-transition canonicalization needs {count} query permutations, "
            f"exceeding cap {max_permutations}"
        )
    best = None
    best_key = None
    best_mapping = None
    examined = 0
    for mapping in _candidate_mappings(groups, len(certificate.query_costs)):
        examined += 1
        signature = _root_type(certificate, mapping)
        key = repr(signature)
        if best_key is None or key < best_key or (
            key == best_key and mapping < best_mapping
        ):
            best = signature
            best_key = key
            best_mapping = mapping
    assert best is not None and best_mapping is not None
    return CanonicalResourceTransitionSignature(
        best,
        best_mapping,
        tuple(len(group) for group in groups),
        examined,
    )


def _inverse(mapping: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(mapping)
    for old, new in enumerate(mapping):
        inverse[new] = old
    return tuple(inverse)


def resource_transition_isomorphism_witness(
    left: FiniteTask,
    right: FiniteTask,
    *,
    max_permutations: int = 100_000,
) -> ResourceTransitionIsomorphismWitness | None:
    """Return an explicit global resource bijection when canonical systems match."""
    if len(left.queries) != len(right.queries):
        return None
    left_sig = canonical_resource_transition_signature(
        left, max_permutations=max_permutations
    )
    right_sig = canonical_resource_transition_signature(
        right, max_permutations=max_permutations
    )
    if left_sig.signature != right_sig.signature:
        return None
    right_inverse = _inverse(right_sig.query_to_canonical)
    mapping = tuple(
        right_inverse[left_sig.query_to_canonical[q]]
        for q in range(len(left.queries))
    )
    witness = ResourceTransitionIsomorphismWitness(mapping)
    if not verify_resource_transition_isomorphism(left, right, witness):
        raise ArithmeticError("canonical match did not yield a valid resource isomorphism")
    return witness


def verify_resource_transition_isomorphism(
    left: FiniteTask,
    right: FiniteTask,
    witness: ResourceTransitionIsomorphismWitness,
) -> bool:
    """Verify one proposed global query bijection without trusting canonical hashes."""
    try:
        if not isinstance(witness, ResourceTransitionIsomorphismWitness):
            return False
        if len(left.queries) != len(right.queries):
            return False
        mapping = witness.left_to_right_query
        qn = len(left.queries)
        if len(mapping) != qn or set(mapping) != set(range(qn)):
            return False
        if any(
            left.queries[q].cost != right.queries[mapping[q]].cost
            for q in range(qn)
        ):
            return False
        left_certificate = build_resource_continuation_quotient(left)
        right_certificate = build_resource_continuation_quotient(right)
        if not verify_resource_continuation_quotient(left, left_certificate):
            return False
        if not verify_resource_continuation_quotient(right, right_certificate):
            return False
        left_type = _root_type(left_certificate, mapping)
        identity = tuple(range(qn))
        right_type = _root_type(right_certificate, identity)
        return left_type == right_type
    except (TypeError, ValueError, ArithmeticError, IndexError):
        return False


def resource_transition_isomorphism_audit(
    left: FiniteTask,
    right: FiniteTask,
    *,
    max_permutations: int = 100_000,
) -> ResourceTransitionIsomorphismAudit:
    witness = resource_transition_isomorphism_witness(
        left, right, max_permutations=max_permutations
    )
    left_receipt = adaptive_gain_receipt(left)
    right_receipt = adaptive_gain_receipt(right)
    left_costs = (left_receipt.adaptive_cost, left_receipt.fixed_cost)
    right_costs = (right_receipt.adaptive_cost, right_receipt.fixed_cost)
    agree = witness is None or left_costs == right_costs
    if witness is not None and not agree:
        raise ArithmeticError("verified resource-transition isomorphism changed joint costs")
    return ResourceTransitionIsomorphismAudit(
        witness is not None,
        left_costs,
        right_costs,
        agree,
        witness,
    )
