from adaptive_gain.static_information_adaptive_separation import (
    conditional_entropy_log_fingerprint,
    joint_entropy_log_fingerprint,
    static_information_adaptive_separation_audit,
    static_information_twin_a_task,
    static_information_twin_b_task,
)


def test_static_subset_information_profile_is_exactly_matched_but_adaptive_cost_differs():
    receipt = static_information_adaptive_separation_audit()
    assert receipt.world_count == 12
    assert receipt.query_count == 4
    assert receipt.every_query_exactly_balanced
    assert receipt.target_multiplicities == (8, 4)
    assert receipt.same_named_subset_information_profile_exactly
    assert receipt.same_full_shannon_entropy_vector_exactly
    assert (receipt.twin_a_adaptive_cost, receipt.twin_a_fixed_cost) == (4, 4)
    assert (receipt.twin_b_adaptive_cost, receipt.twin_b_fixed_cost) == (3, 4)
    assert receipt.theorem_holds


def test_every_named_subset_has_the_same_exact_conditional_entropy_fingerprint():
    a = static_information_twin_a_task()
    b = static_information_twin_b_task()
    names = tuple(q.name for q in a.queries)
    for mask in range(1 << len(names)):
        subset = tuple(names[j] for j in range(len(names)) if mask & (1 << j))
        assert conditional_entropy_log_fingerprint(a, subset) == conditional_entropy_log_fingerprint(
            b, subset
        )


def test_complete_shannon_entropy_vector_matches_exactly():
    a = static_information_twin_a_task()
    b = static_information_twin_b_task()
    names = tuple(q.name for q in a.queries)
    for mask in range(1 << len(names)):
        subset = tuple(names[j] for j in range(len(names)) if mask & (1 << j))
        for include_target in (False, True):
            assert joint_entropy_log_fingerprint(
                a, subset, include_target=include_target
            ) == joint_entropy_log_fingerprint(
                b, subset, include_target=include_target
            )
