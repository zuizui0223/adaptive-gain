from adaptive_gain.resource_overlap import (
    enumerate_balanced_resource_role_overlap_universe,
    resource_overlap_collision_audit,
    resource_overlap_signatures,
    resource_role_profile_collision,
)


def test_orbit_capacity_and_resource_role_profiles_have_distinct_fixed_cost_collisions():
    audit = resource_overlap_collision_audit()
    assert audit.orbit_capacity_signatures_equal
    assert set(audit.orbit_capacity_costs) == {(2, 2), (2, 3)}
    assert audit.role_profile_signatures_equal
    assert set(audit.role_profile_costs) == {(2, 2), (2, 3)}
    # Concrete state-resource co-location contains information that the
    # first-order per-resource role multiset loses.
    assert not audit.role_profile_colocation_signatures_equal


def test_registered_four_query_role_collision_is_separated_by_state_colocation():
    tasks = resource_role_profile_collision()
    left, right = resource_overlap_signatures(tasks)
    assert left.continuation_root_type == right.continuation_root_type
    assert left.resource_role_profile_multiset == right.resource_role_profile_multiset
    assert left.state_resource_colocation_signature != right.state_resource_colocation_signature


def test_complete_three_query_scope_has_no_resource_role_ambiguity():
    summary = enumerate_balanced_resource_role_overlap_universe(3)
    assert summary.task_count == 16 ** 3 == 4_096
    assert summary.signature_count == 25
    assert summary.ambiguous_signature_count == 0
    assert summary.ambiguous_task_count == 0
    assert summary.ambiguous_cost_pair_counts == ()


def test_complete_four_query_scope_has_one_resource_role_ambiguity_class():
    summary = enumerate_balanced_resource_role_overlap_universe(4)
    assert summary.task_count == 16 ** 4 == 65_536
    assert summary.signature_count == 60
    assert summary.ambiguous_signature_count == 1
    assert summary.ambiguous_task_count == 2_304
    assert dict(summary.ambiguous_cost_pair_counts) == {
        (2, 2): 1_536,
        (2, 3): 768,
    }
