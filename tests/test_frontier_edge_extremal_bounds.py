from adaptive_gain.bounded_arity_extremal_bounds import sharp_bounded_arity_unit_cost_ratio
from adaptive_gain.frontier_edge_extremal_bounds import (
    sharp_frontier_edge_capped_unit_cost_ratio,
    sharp_frontier_edge_capped_unit_cost_ratio_receipt,
)


def test_edge_cap_one_forces_ratio_one():
    for arity in (2, 3, 4, 8):
        for n in range(2, 10):
            for m in range(1, 7):
                assert sharp_frontier_edge_capped_unit_cost_ratio(n, m, arity, 1) == 1


def test_edge_cap_at_least_query_count_recovers_uncapped_bound():
    for arity in (2, 3, 4):
        for n in range(2, 10):
            for m in range(1, 7):
                assert sharp_frontier_edge_capped_unit_cost_ratio(n, m, arity, m) == sharp_bounded_arity_unit_cost_ratio(n, m, arity)


def test_edge_capped_witnesses_attain_bound_on_small_grid():
    for arity in (2, 3, 4):
        for n in range(2, 9):
            for m in range(1, 7):
                for edge_cap in range(1, m + 1):
                    receipt = sharp_frontier_edge_capped_unit_cost_ratio_receipt(
                        n, m, arity, edge_cap
                    )
                    assert receipt.direct_check_agrees
                    assert receipt.edge_cap_holds
                    assert receipt.witness_ratio == receipt.sharp_ratio
                    assert receipt.witness_frontier_edge_count <= edge_cap


def test_ratio_is_monotone_in_frontier_edge_cap():
    for arity in (2, 3, 4):
        for n in range(2, 11):
            for m in range(2, 8):
                values = [
                    sharp_frontier_edge_capped_unit_cost_ratio(n, m, arity, edge_cap)
                    for edge_cap in range(1, m + 1)
                ]
                assert values == sorted(values)
