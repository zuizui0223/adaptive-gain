from adaptive_gain.resource_overlap_exhaustive import (
    enumerate_balanced_four_query_colocation_repair,
)


def test_state_resource_colocation_repairs_first_four_query_role_ambiguity():
    summary = enumerate_balanced_four_query_colocation_repair()
    assert summary.task_count == 65_536
    assert summary.resource_role_signature_count == 60
    assert summary.role_ambiguous_signature_count == 1
    assert summary.role_ambiguous_task_count == 2_304
    assert summary.colocation_signature_count_within_ambiguous_role_class == 2
    assert summary.colocation_ambiguous_signature_count == 0
    assert dict(summary.colocation_cost_pair_counts) == {
        (2, 2): 1_536,
        (2, 3): 768,
    }
