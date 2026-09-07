"""Exact symmetry-pruned proof DAGs for bounded fixed target-pair cover.

At an infeasible residual instance, the usual integer proof must consider every
affordable separator of the chosen obligation. If two such queries lie in the
same exact query-automorphism orbit of the residual weighted incidence, deleting
one or the other produces isomorphic child instances. Therefore one child proof
per orbit is sufficient, provided the skipped branches carry explicit child
isomorphism transports that can be checked independently.

This module combines:
- exact automorphism receipts for the parent residual instance;
- one representative affordable branch per parent-query orbit;
- exact isomorphism sharing across residual states; and
- explicit transports for every skipped symmetric branch.

The verifier reconstructs every child and checks all stated transports. It does
not trust a branch count, an orbit label, or a canonical signature by itself.
"""
from __future__ import annotations

from dataclasses import dataclass

from .automorphism import (
    ResidualAutomorphismGroupReceipt,
    residual_automorphism_group,
    verify_residual_automorphism_group,
)
from .color_refinement import (
    refined_canonical_residual_pair_cover_signature,
    refined_residual_pair_cover_isomorphism_witness,
)
from .core import FiniteTask, adaptive_minimum_resolution, bundle_resolves
from .isomorphism_proof_dag import (
    _affordable_separators,
    _child_instance,
    _choose_obligation,
    _instance_key,
    _root_instance,
)
from .isomorphism_quotient import (
    ResidualIsomorphismWitness,
    ResidualPairCoverInstance,
    verify_residual_pair_cover_isomorphism,
)


class SymmetryPrunedProofDagLimitError(RuntimeError):
    """Exact symmetry-pruned proof generation exceeded a declared resource cap."""


@dataclass(frozen=True)
class SymmetricBranchMember:
    query_index: int
    child_to_orbit_representative_query: tuple[int, ...]


@dataclass(frozen=True)
class SymmetricBranchOrbit:
    member_queries: tuple[int, ...]
    representative_query_index: int
    members: tuple[SymmetricBranchMember, ...]
    representative_child_node_id: int
    representative_child_to_node_query: tuple[int, ...]


@dataclass(frozen=True)
class SymmetryPrunedProofDagNode:
    node_id: int
    instance: ResidualPairCoverInstance
    status: str
    chosen_obligation_index: int
    affordable_separator_queries: tuple[int, ...]
    automorphism_receipt: ResidualAutomorphismGroupReceipt | None
    branch_orbits: tuple[SymmetricBranchOrbit, ...]


@dataclass(frozen=True)
class SymmetryPrunedProofDagCertificate:
    budget: int
    fixed_resolver_exists_within_budget: bool
    feasible_bundle: tuple[str, ...] | None
    root_node_id: int | None
    nodes: tuple[SymmetryPrunedProofDagNode, ...]
    raw_affordable_branch_count: int
    representative_branch_count: int
    symmetric_branch_savings: int
    exact_residual_instance_count: int
    isomorphism_class_count: int
    isomorphism_merge_count: int
    explicit_skipped_branch_transports: int
    canonicalization_calls: int
    automorphism_receipts_built: int
    complete_search: bool
    scope: str = "exact_fixed_cover_infeasibility_DAG_with_parent_automorphism_orbit_branch_pruning"


@dataclass(frozen=True)
class SymmetryPrunedAdaptiveGainAudit:
    adaptive_cost: int | None
    strict_adaptive_gain: bool
    certificate: SymmetryPrunedProofDagCertificate | None
    interpretation: str


def _branch_orbits(
    affordable: tuple[int, ...],
    receipt: ResidualAutomorphismGroupReceipt,
) -> tuple[tuple[int, ...], ...]:
    allowed = set(affordable)
    groups = []
    covered: set[int] = set()
    for orbit in receipt.query_orbits:
        members = tuple(q for q in orbit if q in allowed)
        if members:
            groups.append(members)
            covered.update(members)
    if covered != allowed:
        raise ArithmeticError("automorphism orbit partition lost an affordable branch")
    return tuple(sorted(groups, key=lambda group: (min(group), group)))


def build_symmetry_pruned_proof_dag(
    task: FiniteTask,
    *,
    budget: int,
    max_nodes: int = 200_000,
    max_permutations: int = 100_000,
) -> SymmetryPrunedProofDagCertificate:
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(max_nodes) is not int or max_nodes < 1:
        raise ValueError("max_nodes must be a positive integer")

    root = _root_instance(task, budget)
    root_labels = tuple(query.name for query in task.queries)
    if not root.separator_rows:
        return SymmetryPrunedProofDagCertificate(
            budget, True, (), None, (), 0, 0, 0, 1, 0, 0, 0, 0, 0, True
        )

    nodes: dict[int, SymmetryPrunedProofDagNode] = {}
    signature_to_node: dict[tuple, int] = {}
    exact_instances: set[tuple] = set()
    raw_branches = representative_branches = skipped_transports = 0
    canonical_calls = automorphism_receipts = 0
    next_node_id = 0

    @dataclass(frozen=True)
    class SearchResult:
        feasible: bool
        bundle: tuple[str, ...] | None
        node_id: int | None
        source_to_node_query: tuple[int, ...] | None

    def search(instance: ResidualPairCoverInstance, labels: tuple[str, ...]) -> SearchResult:
        nonlocal raw_branches, representative_branches, skipped_transports
        nonlocal canonical_calls, automorphism_receipts, next_node_id

        exact_instances.add(_instance_key(instance))
        if not instance.separator_rows:
            return SearchResult(True, (), None, None)

        canonical = refined_canonical_residual_pair_cover_signature(
            instance, max_permutations=max_permutations
        )
        canonical_calls += 1
        signature = canonical.signature
        existing = signature_to_node.get(signature)
        if existing is not None:
            representative = nodes[existing].instance
            witness = refined_residual_pair_cover_isomorphism_witness(
                instance, representative, max_permutations=max_permutations
            )
            if witness is None or not verify_residual_pair_cover_isomorphism(witness):
                raise ArithmeticError("isomorphism cache hit lacked a valid explicit transport")
            return SearchResult(False, None, existing, witness.left_to_right_query)

        if len(nodes) >= max_nodes:
            raise SymmetryPrunedProofDagLimitError("symmetry-pruned proof DAG node cap reached")

        chosen, affordable = _choose_obligation(instance)
        if not affordable:
            node_id = next_node_id
            next_node_id += 1
            node = SymmetryPrunedProofDagNode(
                node_id, instance, "no_affordable_separator", chosen, (), None, ()
            )
            nodes[node_id] = node
            signature_to_node[signature] = node_id
            return SearchResult(False, None, node_id, tuple(range(len(instance.query_costs))))

        receipt = residual_automorphism_group(
            instance, max_permutations=max_permutations
        )
        automorphism_receipts += 1
        if not verify_residual_automorphism_group(instance, receipt):
            raise ArithmeticError("parent automorphism receipt failed independent verification")
        groups = _branch_orbits(affordable, receipt)
        raw_branches += len(affordable)
        representative_branches += len(groups)

        orbit_specs = []
        for group in groups:
            representative_query = min(group)
            representative_child = _child_instance(instance, representative_query)
            representative_labels = tuple(
                label for i, label in enumerate(labels) if i != representative_query
            )
            result = search(representative_child, representative_labels)
            if result.feasible:
                assert result.bundle is not None
                return SearchResult(
                    True,
                    (labels[representative_query],) + result.bundle,
                    None,
                    None,
                )
            assert result.node_id is not None and result.source_to_node_query is not None

            members = []
            for q in group:
                child = _child_instance(instance, q)
                exact_instances.add(_instance_key(child))
                if q == representative_query:
                    mapping = tuple(range(len(representative_child.query_costs)))
                else:
                    witness = refined_residual_pair_cover_isomorphism_witness(
                        child,
                        representative_child,
                        max_permutations=max_permutations,
                    )
                    if witness is None or not verify_residual_pair_cover_isomorphism(witness):
                        raise ArithmeticError(
                            "parent automorphism orbit produced non-isomorphic branch children"
                        )
                    mapping = witness.left_to_right_query
                    skipped_transports += 1
                members.append(SymmetricBranchMember(q, mapping))

            orbit_specs.append(
                SymmetricBranchOrbit(
                    tuple(group),
                    representative_query,
                    tuple(members),
                    result.node_id,
                    result.source_to_node_query,
                )
            )

        node_id = next_node_id
        next_node_id += 1
        node = SymmetryPrunedProofDagNode(
            node_id,
            instance,
            "all_automorphism_orbit_representatives_infeasible",
            chosen,
            affordable,
            receipt,
            tuple(orbit_specs),
        )
        nodes[node_id] = node
        signature_to_node[signature] = node_id
        return SearchResult(False, None, node_id, tuple(range(len(instance.query_costs))))

    result = search(root, root_labels)
    if result.feasible:
        assert result.bundle is not None
        lookup = {query.name: query.cost for query in task.queries}
        if len(set(result.bundle)) != len(result.bundle):
            raise ArithmeticError("symmetry-pruned solver repeated a query")
        if sum(lookup[name] for name in result.bundle) > budget or not bundle_resolves(task, result.bundle):
            raise ArithmeticError("symmetry-pruned solver returned an invalid fixed bundle")
        certificate = SymmetryPrunedProofDagCertificate(
            budget, True, result.bundle, None, (), raw_branches,
            representative_branches, raw_branches - representative_branches,
            len(exact_instances), 0, 0, skipped_transports,
            canonical_calls, automorphism_receipts, True,
        )
        if not verify_symmetry_pruned_proof_dag(task, certificate):
            raise ArithmeticError("generated feasible symmetry decision failed verification")
        return certificate

    assert result.node_id is not None
    ordered = tuple(nodes[node_id] for node_id in sorted(nodes))
    certificate = SymmetryPrunedProofDagCertificate(
        budget,
        False,
        None,
        result.node_id,
        ordered,
        raw_branches,
        representative_branches,
        raw_branches - representative_branches,
        len(exact_instances),
        len(ordered),
        len(exact_instances) - len(ordered),
        skipped_transports,
        canonical_calls,
        automorphism_receipts,
        True,
    )
    if not verify_symmetry_pruned_proof_dag(task, certificate):
        raise ArithmeticError("generated symmetry-pruned proof DAG failed verification")
    return certificate


def verify_symmetry_pruned_proof_dag(
    task: FiniteTask,
    certificate: SymmetryPrunedProofDagCertificate,
) -> bool:
    if not certificate.complete_search or certificate.budget < 0:
        return False
    if certificate.fixed_resolver_exists_within_budget:
        if certificate.root_node_id is not None or certificate.nodes:
            return False
        bundle = certificate.feasible_bundle
        if bundle is None:
            return False
        lookup = {query.name: query.cost for query in task.queries}
        if len(set(bundle)) != len(bundle) or any(name not in lookup for name in bundle):
            return False
        return (
            sum(lookup[name] for name in bundle) <= certificate.budget
            and bundle_resolves(task, bundle)
        )

    if certificate.feasible_bundle is not None or certificate.root_node_id is None:
        return False
    node_map = {node.node_id: node for node in certificate.nodes}
    if len(node_map) != len(certificate.nodes) or certificate.root_node_id not in node_map:
        return False
    root = _root_instance(task, certificate.budget)
    if _instance_key(node_map[certificate.root_node_id].instance) != _instance_key(root):
        return False

    raw_branches = representative_branches = skipped_transports = 0
    reconstructed_exact: set[tuple] = {_instance_key(root)}
    visiting: set[int] = set()
    verified: set[int] = set()

    def check(node_id: int) -> bool:
        nonlocal raw_branches, representative_branches, skipped_transports
        if node_id in verified:
            return True
        if node_id in visiting or node_id not in node_map:
            return False
        visiting.add(node_id)
        node = node_map[node_id]
        instance = node.instance
        if not instance.separator_rows:
            return False
        if not 0 <= node.chosen_obligation_index < len(instance.separator_rows):
            return False
        affordable = _affordable_separators(instance, node.chosen_obligation_index)

        if node.status == "no_affordable_separator":
            ok = (
                not affordable
                and not node.affordable_separator_queries
                and node.automorphism_receipt is None
                and not node.branch_orbits
            )
        elif node.status == "all_automorphism_orbit_representatives_infeasible":
            if node.affordable_separator_queries != affordable or node.automorphism_receipt is None:
                return False
            if not verify_residual_automorphism_group(instance, node.automorphism_receipt):
                return False
            expected_groups = _branch_orbits(affordable, node.automorphism_receipt)
            if tuple(orbit.member_queries for orbit in node.branch_orbits) != expected_groups:
                return False
            raw_branches += len(affordable)
            representative_branches += len(expected_groups)
            ok = True
            for orbit in node.branch_orbits:
                if orbit.representative_query_index != min(orbit.member_queries):
                    return False
                if tuple(member.query_index for member in orbit.members) != orbit.member_queries:
                    return False
                representative_child = _child_instance(
                    instance, orbit.representative_query_index
                )
                for member in orbit.members:
                    child = _child_instance(instance, member.query_index)
                    reconstructed_exact.add(_instance_key(child))
                    witness = ResidualIsomorphismWitness(
                        child,
                        representative_child,
                        member.child_to_orbit_representative_query,
                    )
                    if not verify_residual_pair_cover_isomorphism(witness):
                        return False
                    if member.query_index != orbit.representative_query_index:
                        skipped_transports += 1
                if orbit.representative_child_node_id not in node_map:
                    return False
                target = node_map[orbit.representative_child_node_id].instance
                witness = ResidualIsomorphismWitness(
                    representative_child,
                    target,
                    orbit.representative_child_to_node_query,
                )
                if not verify_residual_pair_cover_isomorphism(witness):
                    return False
                if target.remaining_budget >= instance.remaining_budget:
                    return False
                if not check(orbit.representative_child_node_id):
                    ok = False
                    break
        else:
            return False

        visiting.remove(node_id)
        if ok:
            verified.add(node_id)
        return ok

    if not check(certificate.root_node_id) or verified != set(node_map):
        return False
    if certificate.raw_affordable_branch_count != raw_branches:
        return False
    if certificate.representative_branch_count != representative_branches:
        return False
    if certificate.symmetric_branch_savings != raw_branches - representative_branches:
        return False
    if certificate.explicit_skipped_branch_transports != skipped_transports:
        return False
    if certificate.exact_residual_instance_count != len(reconstructed_exact):
        return False
    if certificate.isomorphism_class_count != len(node_map):
        return False
    if certificate.isomorphism_merge_count != len(reconstructed_exact) - len(node_map):
        return False
    return True


def selected_policy_symmetry_pruned_gain_audit(
    task: FiniteTask,
    *,
    max_nodes: int = 200_000,
    max_permutations: int = 100_000,
) -> SymmetryPrunedAdaptiveGainAudit:
    adaptive = adaptive_minimum_resolution(task)
    ca = adaptive.minimum_worst_path_cost
    if ca is None:
        return SymmetryPrunedAdaptiveGainAudit(
            None, False, None, "no resolving adaptive policy"
        )
    certificate = build_symmetry_pruned_proof_dag(
        task,
        budget=ca,
        max_nodes=max_nodes,
        max_permutations=max_permutations,
    )
    strict = not certificate.fixed_resolver_exists_within_budget
    return SymmetryPrunedAdaptiveGainAudit(
        ca,
        strict,
        certificate,
        (
            f"exact symmetry-pruned proof excludes every fixed resolver of cost <= {ca}"
            if strict
            else f"a fixed resolver exists within adaptive cost {ca}"
        ),
    )
