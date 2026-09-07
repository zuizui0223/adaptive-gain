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
    isomorphic_fixed_budget_cover_decision,
    residual_pair_cover_isomorphism_witness,
    selected_policy_isomorphism_quotient_gain_audit,
    verify_residual_pair_cover_isomorphism,
)
from adaptive_gain.witnesses import routing_bypass_control


def _isomorphism_compression_control():
    # Seeded strict-gain witness. Exact costs C_A=2,C_F=3.  At B=2 the
    # kernelized residual search encounters four label-specific states but only
    # two weighted-incidence isomorphism classes.
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


def _permute_instance(instance, order, row_order):
    position = {old: new for new, old in enumerate(order)}
    rows = []
    for row in instance.separator_rows:
        mask = 0
        for old in order:
            if row & (1 << old):
                mask |= 1 << position[old]
        rows.append(mask)
    return ResidualPairCoverInstance(
        tuple(instance.query_costs[q] for q in order),
        tuple(rows[i] for i in row_order),
        instance.remaining_budget,
    )


def test_canonical_signature_ignores_pair_order_and_cost_preserving_query_names():
    left = ResidualPairCoverInstance(
        (1, 2, 1, 2),
        (0b0011, 0b1100, 0b0101, 0b1010),
        3,
    )
    # Swap the two cost-1 columns, swap the two cost-2 columns, and reorder rows.
    right = _permute_instance(left, (2, 3, 0, 1), (3, 1, 0, 2))
    left_c = canonical_residual_pair_cover_signature(left)
    right_c = canonical_residual_pair_cover_signature(right)
    assert left_c.signature == right_c.signature
    witness = residual_pair_cover_isomorphism_witness(left, right)
    assert witness is not None
    assert verify_residual_pair_cover_isomorphism(witness)


def test_verifier_rejects_cost_incompatible_query_mapping():
    left = ResidualPairCoverInstance((1, 2), (0b01, 0b10), 2)
    right = ResidualPairCoverInstance((2, 1), (0b01, 0b10), 2)
    witness = residual_pair_cover_isomorphism_witness(left, right)
    assert witness is not None
    bad = type(witness)(left, right, (0, 1))
    assert not verify_residual_pair_cover_isomorphism(bad)


def test_canonicalizer_fails_closed_when_symmetry_permutation_cap_is_too_small():
    instance = ResidualPairCoverInstance(
        (1,) * 9,
        ((1 << 9) - 1,),
        4,
    )
    with pytest.raises(ResidualIsomorphismLimitError):
        canonical_residual_pair_cover_signature(instance, max_permutations=100)


def test_isomorphism_quotient_merges_label_distinct_residual_states_on_strict_gain_control():
    task = _isomorphism_compression_control()
    exact = adaptive_gain_receipt(task)
    assert (exact.adaptive_cost, exact.fixed_cost) == (2, 3)
    decision = isomorphic_fixed_budget_cover_decision(task, budget=2)
    assert not decision.fixed_resolver_exists_within_budget
    assert decision.exact_residual_state_count == 4
    assert decision.isomorphism_class_count == 2
    assert decision.isomorphism_merge_count == 2
    assert decision.infeasible_isomorphism_cache_hits == 2
    assert decision.first_merge_witness is not None
    assert verify_residual_pair_cover_isomorphism(decision.first_merge_witness)
    assert selected_policy_isomorphism_quotient_gain_audit(task).strict_adaptive_gain


def test_isomorphism_quotient_constructively_refuses_false_gain_on_bypass_control():
    task = routing_bypass_control()
    decision = isomorphic_fixed_budget_cover_decision(task, budget=2)
    assert decision.fixed_resolver_exists_within_budget
    assert decision.feasible_bundle is not None
    assert not selected_policy_isomorphism_quotient_gain_audit(task).strict_adaptive_gain


def test_isomorphism_quotient_matches_exact_gain_on_complete_minimal_universe():
    targets = (0, 0, 1, 1)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    patterns = tuple(product((0, 1), repeat=4))
    strict = quotient_strict = false_positive = false_negative = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, outcomes) for j, outcomes in enumerate(maps)),
        )
        exact = adaptive_gain_receipt(task)
        actual = exact.strict_adaptive_gain
        predicted = False
        if exact.adaptive_cost is not None:
            predicted = not isomorphic_fixed_budget_cover_decision(
                task, budget=exact.adaptive_cost
            ).fixed_resolver_exists_within_budget
        strict += int(actual)
        quotient_strict += int(predicted)
        false_positive += int(predicted and not actual)
        false_negative += int(actual and not predicted)
    assert strict == 192
    assert quotient_strict == 192
    assert false_positive == 0
    assert false_negative == 0
