import pytest

from adaptive_gain.arity_dynamic_scope import stable_oscillation_pareto_scope


def _coords(receipt):
    return [
        (
            p.world_count,
            p.query_count,
            p.productive_frontier_edge_count,
            p.adaptive_depth,
        )
        for p in receipt.pareto_frontier
    ]


def test_binary_dynamic_scope_collapses_to_single_exact_corner():
    receipt = stable_oscillation_pareto_scope(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        gain_per_structural_gap=0.125,
        max_arity=2,
    )
    assert receipt.minimum_oscillatory_gap == 2
    assert receipt.maximum_stable_gap == 7
    assert receipt.stable_integer_oscillation_possible
    assert _coords(receipt) == [(6, 5, 5, 3)]


def test_ternary_cues_reduce_query_frontier_burden_without_world_minimum():
    receipt = stable_oscillation_pareto_scope(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        gain_per_structural_gap=0.125,
        max_arity=3,
    )
    assert receipt.minimum_oscillatory_gap == 2
    assert _coords(receipt) == [(6, 4, 4, 2)]


def test_response_requiring_gap_three_has_genuine_quaternary_pareto_tradeoff():
    # alpha=1, phi=1/2 gives G_osc=1/8.  With a=0.05 the first strict
    # oscillatory integer gap is q=3, while the upper stable integer gap is 19.
    receipt = stable_oscillation_pareto_scope(
        evolutionary_persistence=1.0,
        community_memory=0.5,
        gain_per_structural_gap=0.05,
        max_arity=4,
    )
    assert receipt.minimum_oscillatory_gap == 3
    assert receipt.maximum_stable_gap == 19
    assert receipt.stable_integer_oscillation_possible
    assert _coords(receipt) == [
        (8, 5, 5, 2),
        (7, 6, 6, 3),
    ]


def test_integer_gap_ladder_can_skip_stable_oscillatory_region_for_any_arity():
    for b in (2, 3, 5):
        receipt = stable_oscillation_pareto_scope(
            evolutionary_persistence=1.0,
            community_memory=0.5,
            gain_per_structural_gap=1.1,
            max_arity=b,
        )
        assert receipt.minimum_oscillatory_gap == 1
        assert receipt.maximum_stable_gap == 0
        assert not receipt.stable_integer_oscillation_possible
        assert receipt.pareto_frontier == ()


def test_invalid_arity_is_rejected():
    with pytest.raises(ValueError):
        stable_oscillation_pareto_scope(
            evolutionary_persistence=1.0,
            community_memory=0.5,
            gain_per_structural_gap=0.125,
            max_arity=1,
        )
