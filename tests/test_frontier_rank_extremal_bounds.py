from adaptive_gain.bounded_arity_extremal_bounds import (
    sharp_bounded_arity_unit_cost_ratio,
)
from adaptive_gain.frontier_rank_extremal_bounds import (
    productive_frontier_rank,
    sharp_frontier_rank_capped_unit_cost_ratio,
    sharp_frontier_rank_capped_unit_cost_ratio_receipt,
)


def test_rank_cap_one_already_attains_bounded_arity_extremum_on_small_grid():
    for n in range(2, 9):
        for m in range(1, 7):
            for b in range(2, 5):
                expected = sharp_bounded_arity_unit_cost_ratio(n, m, b)
                assert sharp_frontier_rank_capped_unit_cost_ratio(n, m, b, 1) == expected
                receipt = sharp_frontier_rank_capped_unit_cost_ratio_receipt(n, m, b, 1)
                assert receipt.sharp_ratio == expected
                assert receipt.witness_ratio == expected
                assert receipt.witness_frontier_rank == 1
                assert receipt.rank_cap_holds
                assert receipt.direct_check_agrees


def test_larger_rank_caps_do_not_change_extremal_ratio():
    cases = [
        (4, 3, 2),
        (6, 5, 2),
        (8, 7, 3),
        (10, 8, 4),
    ]
    for n, m, b in cases:
        baseline = sharp_bounded_arity_unit_cost_ratio(n, m, b)
        for rank_cap in (1, 2, 3, 5):
            assert sharp_frontier_rank_capped_unit_cost_ratio(n, m, b, rank_cap) == baseline


def test_frontier_rank_helper():
    assert productive_frontier_rank(()) == 0
    assert productive_frontier_rank((1, 2, 4)) == 1
    assert productive_frontier_rank((3, 5, 12)) == 2
    assert productive_frontier_rank((7, 24)) == 3


def test_invalid_rank_cap_fails_closed():
    for bad in (0, -1):
        try:
            sharp_frontier_rank_capped_unit_cost_ratio(4, 3, 2, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("nonpositive frontier rank cap should fail closed")
