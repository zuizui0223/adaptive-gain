from adaptive_gain.binary_unit_cost_extremal_bounds import (
    binary_tree_fixed_cost_bound,
    sharp_binary_unit_cost_ratio,
)
from adaptive_gain.bounded_arity_extremal_bounds import (
    maximum_bounded_arity_tree_internal_nodes,
    sharp_bounded_arity_unit_cost_ratio,
    sharp_bounded_arity_unit_cost_ratio_receipt,
    sharp_bounded_arity_unit_cost_witness,
)
from adaptive_gain.unit_cost_extremal_bounds import (
    maximum_productive_tree_internal_nodes,
    sharp_unit_cost_ratio,
)


def test_bounded_arity_tree_recurrence_reduces_to_binary_formula():
    for n in range(2, 13):
        for depth in range(1, 6):
            assert maximum_bounded_arity_tree_internal_nodes(n, depth, 2) == binary_tree_fixed_cost_bound(
                n, 10**6, depth
            )


def test_bounded_arity_tree_recurrence_reduces_to_unrestricted_formula():
    for n in range(2, 13):
        for depth in range(1, 6):
            assert maximum_bounded_arity_tree_internal_nodes(n, depth, n) == maximum_productive_tree_internal_nodes(
                n, depth
            )


def test_sharp_ratio_reduces_to_binary_and_unrestricted_endpoints():
    for n in range(2, 11):
        for m in range(1, 8):
            assert sharp_bounded_arity_unit_cost_ratio(n, m, 2) == sharp_binary_unit_cost_ratio(n, m)
            assert sharp_bounded_arity_unit_cost_ratio(n, m, n) == sharp_unit_cost_ratio(n, m)


def test_intermediate_arity_witnesses_attain_theorem_on_small_grid():
    for arity in (3, 4):
        for n in range(2, 10):
            for m in range(1, 7):
                receipt = sharp_bounded_arity_unit_cost_ratio_receipt(
                    n, m, arity, direct_check=True
                )
                assert receipt.theorem_holds
                assert receipt.direct_check_agrees
                assert receipt.witness_ratio == receipt.sharp_ratio


def test_constructed_queries_respect_arity_and_private_resource_count():
    for arity, n, m in ((3, 8, 6), (3, 10, 7), (4, 10, 7)):
        task = sharp_bounded_arity_unit_cost_witness(n, m, arity)
        assert len(task.worlds) == n
        assert len(task.queries) == m
        assert all(len(set(query.outcomes)) <= arity for query in task.queries)
        receipt = sharp_bounded_arity_unit_cost_ratio_receipt(n, m, arity)
        assert receipt.private_pair_count <= m
        assert receipt.private_pair_count == receipt.witness_fixed_cost


def test_intermediate_arity_sits_between_binary_and_unrestricted_extrema():
    for n in range(3, 12):
        for m in range(2, 8):
            binary = sharp_bounded_arity_unit_cost_ratio(n, m, 2)
            ternary = sharp_bounded_arity_unit_cost_ratio(n, m, 3)
            unrestricted = sharp_bounded_arity_unit_cost_ratio(n, m, n)
            assert binary <= ternary <= unrestricted
