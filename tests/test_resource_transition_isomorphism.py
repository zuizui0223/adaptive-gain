from adaptive_gain.core import FiniteTask, Query
from adaptive_gain.resource_overlap import (
    orbit_capacity_collision,
    resource_role_profile_collision,
)
from adaptive_gain.resource_transition_isomorphism import (
    ResourceTransitionIsomorphismWitness,
    canonical_resource_transition_signature,
    resource_transition_isomorphism_audit,
    resource_transition_isomorphism_witness,
    verify_resource_transition_isomorphism,
)


def _reordered(task: FiniteTask, order: tuple[int, ...]) -> FiniteTask:
    return FiniteTask(
        task.worlds,
        tuple(
            Query(f"renamed_{k}", task.queries[q].cost, task.queries[q].outcomes)
            for k, q in enumerate(order)
        ),
    )


def test_global_resource_renaming_preserves_joint_transition_structure():
    task, _ = resource_role_profile_collision()
    renamed = _reordered(task, (2, 0, 3, 1))
    left = canonical_resource_transition_signature(task)
    right = canonical_resource_transition_signature(renamed)
    assert left.signature == right.signature

    witness = resource_transition_isomorphism_witness(task, renamed)
    assert witness is not None
    assert verify_resource_transition_isomorphism(task, renamed, witness)
    audit = resource_transition_isomorphism_audit(task, renamed)
    assert audit.isomorphic
    assert audit.left_costs == audit.right_costs == (2, 2)
    assert audit.costs_agree_when_isomorphic


def test_known_fixed_cost_collisions_are_not_resource_transition_isomorphic():
    for left, right in (
        orbit_capacity_collision(),
        resource_role_profile_collision(),
    ):
        assert resource_transition_isomorphism_witness(left, right) is None
        audit = resource_transition_isomorphism_audit(left, right)
        assert not audit.isomorphic
        assert set((audit.left_costs, audit.right_costs)) == {(2, 2), (2, 3)}


def test_tampered_global_resource_bijection_is_rejected():
    task, _ = resource_role_profile_collision()
    renamed = _reordered(task, (2, 0, 3, 1))
    witness = resource_transition_isomorphism_witness(task, renamed)
    assert witness is not None
    mapping = list(witness.left_to_right_query)
    mapping[0], mapping[1] = mapping[1], mapping[0]
    tampered = ResourceTransitionIsomorphismWitness(tuple(mapping))
    assert not verify_resource_transition_isomorphism(task, renamed, tampered)
