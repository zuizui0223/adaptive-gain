from itertools import product

import pytest

from adaptive_gain import (
    FiniteTask,
    Query,
    ResidualIsomorphismLimitError,
    ResidualPairCoverInstance,
    World,
    adaptive_gain_receipt,
    canonical_residual_pair_cover_signature,
    refined_canonical_residual_pair_cover_signature,
    refined_isomorphic_fixed_budget_cover_decision,
    refine_residual_incidence_colors,
    selected_policy_refined_isomorphism_gain_audit,
)
from adaptive_gain.witnesses import routing_bypass_control


def _refinement_benchmark_instance():
    # q0..q5 are indistinguishable to the original one-step invariant: all have
    # cost 1 and cover two degree-2 rows, so the baseline search is 6! = 720.
    # q6 and q7 have distinct costs. Bipartite refinement propagates those row
    # distinctions back to q0..q5 and splits them 2+3+1, leaving 2!*3! = 12.
    rows = []
    for q in (0, 1):
        rows.extend(((1 << q) | (1 << 6),) * 2)
    for q in (2, 3, 4):
        rows.append((1 << q) | (1 << 6))
        rows.append((1 << q) | (1 << 7))
    rows.extend(((1 << 5) | (1 << 7),) * 2)
    return ResidualPairCoverInstance((1, 1, 1, 1, 1, 1, 2, 3), tuple(rows), 4)


def _isomorphism_compression_control():
    worlds = tuple(World(f"w{i}", 0 if i < 3 else 1) for i in range(6))
    maps = (
        (0, 1, 0, 0, 1, 0),
        (1, 1, 0, 1, 1, 0),
        (0, 0, 1, 1, 1, 1),
        (1, 0, 0, 0, 1, 1),
        (0, 0, 0, 1, 0, 1),
        (0, 0, 1, 0, 1, 0),
    )
    return FiniteTask(
        worlds,
        tuple(Query(f"q{i}", 1, row) for i, row in enumerate(maps)),
    )


def _minimal_instance_from_maps(maps):
    rows = []
    for i in (0, 1):
        for j in (2, 3):
            mask = 0
            for q, outcomes in enumerate(maps):
                if outcomes[i] != outcomes[j]:
                    mask |= 1 << q
            rows.append(mask)
    return ResidualPairCoverInstance((1, 1, 1), tuple(rows), 2)


def test_bipartite_refinement_reduces_720_exact_permutations_to_12():
    instance = _refinement_benchmark_instance()
    _, _, receipt = refine_residual_incidence_colors(instance)
    assert receipt.initial_query_color_class_sizes == (6, 1, 1)
    assert receipt.refined_query_color_class_sizes == (2, 3, 1, 1, 1)
    assert receipt.initial_permutation_count == 720
    assert receipt.refined_permutation_count == 12
    assert receipt.refinement_rounds >= 2
    assert receipt.stable

    baseline = canonical_residual_pair_cover_signature(instance, max_permutations=720)
    refined = refined_canonical_residual_pair_cover_signature(instance, max_permutations=12)
    assert refined.signature == baseline.signature
    assert refined.permutations_before_refinement == 720
    assert refined.permutations_examined == 12


def test_refinement_can_close_exact_canonicalization_under_a_tighter_cap():
    instance = _refinement_benchmark_instance()
    with pytest.raises(ResidualIsomorphismLimitError):
        canonical_residual_pair_cover_signature(instance, max_permutations=12)
    refined = refined_canonical_residual_pair_cover_signature(
        instance, max_permutations=12
    )
    assert refined.permutations_examined == 12


def test_refined_quotient_preserves_existing_isomorphism_compression_and_gain():
    task = _isomorphism_compression_control()
    exact = adaptive_gain_receipt(task)
    assert (exact.adaptive_cost, exact.fixed_cost) == (2, 3)
    decision = refined_isomorphic_fixed_budget_cover_decision(task, budget=2)
    assert not decision.fixed_resolver_exists_within_budget
    assert decision.exact_residual_state_count == 4
    assert decision.isomorphism_class_count == 2
    assert decision.isomorphism_merge_count == 2
    assert decision.canonical_permutations_examined <= decision.canonical_permutations_before_refinement
    assert selected_policy_refined_isomorphism_gain_audit(task).strict_adaptive_gain


def test_refined_quotient_constructively_refuses_no_gain_control():
    task = routing_bypass_control()
    decision = refined_isomorphic_fixed_budget_cover_decision(task, budget=2)
    assert decision.fixed_resolver_exists_within_budget
    assert decision.feasible_bundle is not None
    assert not selected_policy_refined_isomorphism_gain_audit(task).strict_adaptive_gain


def test_refined_and_original_canonical_signatures_match_on_all_4096_minimal_tasks():
    patterns = tuple(product((0, 1), repeat=4))
    for maps in product(patterns, repeat=3):
        instance = _minimal_instance_from_maps(maps)
        baseline = canonical_residual_pair_cover_signature(
            instance, max_permutations=6
        )
        refined = refined_canonical_residual_pair_cover_signature(
            instance, max_permutations=6
        )
        assert refined.signature == baseline.signature
