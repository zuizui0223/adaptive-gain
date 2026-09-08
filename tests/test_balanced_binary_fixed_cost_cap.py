from adaptive_gain.balanced_binary_fixed_cost_cap import (
    audit_exact_balanced_binary_fixed_cost_cap,
    exact_balanced_binary_fixed_cost_cap_private_pairs,
    exact_balanced_binary_fixed_cost_cap_witness,
    sharp_exact_balanced_binary_fixed_cost_cap,
)
from adaptive_gain.core import fixed_minimum_resolution


def test_sharp_exact_balanced_fixed_cost_cap_formula():
    assert sharp_exact_balanced_binary_fixed_cost_cap(2) == 1
    assert sharp_exact_balanced_binary_fixed_cost_cap(4) == 2
    for world_count in (6, 8, 10, 12, 20, 100):
        assert sharp_exact_balanced_binary_fixed_cost_cap(world_count) == world_count - 3


def test_invalid_world_counts_are_rejected():
    for world_count in (0, 1, 3, 5, 7):
        try:
            sharp_exact_balanced_binary_fixed_cost_cap(world_count)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid exact-balanced world count was accepted")


def test_cap_witnesses_are_exactly_balanced_and_fixed_sharp():
    for world_count in (2, 4, 6, 8, 10, 12):
        task = exact_balanced_binary_fixed_cost_cap_witness(world_count)
        cap = sharp_exact_balanced_binary_fixed_cost_cap(world_count)
        assert len(task.queries) == cap
        half = world_count // 2
        for query in task.queries:
            assert set(query.outcomes) <= {0, 1}
            assert sum(outcome == 0 for outcome in query.outcomes) == half
            assert sum(outcome == 1 for outcome in query.outcomes) == half
        assert fixed_minimum_resolution(task).minimum_cost == cap


def test_registered_private_pairs_are_query_unique():
    for world_count in (4, 6, 8, 10, 12):
        task = exact_balanced_binary_fixed_cost_cap_witness(world_count)
        pairs = exact_balanced_binary_fixed_cost_cap_private_pairs(world_count)
        assert len(pairs) == len(task.queries)
        assert len(set(tuple(sorted(pair)) for pair in pairs)) == len(pairs)
        for q_index, (left, right) in enumerate(pairs):
            assert task.worlds[left].target != task.worlds[right].target
            separating = [
                index
                for index, query in enumerate(task.queries)
                if query.outcomes[left] != query.outcomes[right]
            ]
            assert separating == [q_index]


def test_cap_audit_receipts():
    for world_count in (2, 4, 6, 8, 10, 12):
        receipt = audit_exact_balanced_binary_fixed_cost_cap(world_count)
        assert receipt.theorem_holds
        assert receipt.sharp_fixed_cost_cap == sharp_exact_balanced_binary_fixed_cost_cap(world_count)
        assert receipt.witness_fixed_cost == receipt.sharp_fixed_cost_cap
        assert receipt.all_queries_exactly_balanced
        assert receipt.all_registered_private_pairs_unique
        assert receipt.all_registered_private_pairs_cross_target
