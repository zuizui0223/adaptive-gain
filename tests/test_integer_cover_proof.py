import pytest

from adaptive_gain import (
    FiniteTask,
    IntegerCoverProofLimitError,
    Query,
    World,
    adaptive_gain_receipt,
    exact_fractional_pair_packing,
    fixed_budget_cover_decision,
    selected_policy_integer_cover_gain_certificate,
    verify_fixed_budget_decision_certificate,
)
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def _integrality_gap_task():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1), World("w4", 1),
    )
    maps = (
        (1, 0, 0, 0, 0),
        (1, 0, 0, 1, 1),
        (1, 0, 1, 0, 1),
        (0, 1, 0, 0, 1),
    )
    return FiniteTask(worlds, tuple(Query(f"q{i}", 1, row) for i, row in enumerate(maps)))


def test_integer_cover_proof_closes_fractional_integrality_gap():
    task = _integrality_gap_task()
    actual = adaptive_gain_receipt(task)
    assert (actual.adaptive_cost, actual.fixed_cost) == (2, 3)
    fractional = exact_fractional_pair_packing(task)
    assert fractional.objective_exact == "2"
    assert fractional.integer_fixed_cost_lower_bound == 2

    certificate = selected_policy_integer_cover_gain_certificate(task)
    assert certificate.adaptive_cost == 2
    assert certificate.strict_adaptive_gain_certified_without_fixed_optimum
    decision = certificate.fixed_budget_decision
    assert decision is not None
    assert decision.budget == 2
    assert not decision.fixed_resolver_exists_within_budget
    assert decision.infeasibility_proof is not None
    assert verify_fixed_budget_decision_certificate(task, decision)


def test_integer_cover_decision_returns_constructive_fixed_bundle_on_no_gain_control():
    task = routing_bypass_control()
    decision = fixed_budget_cover_decision(task, budget=2)
    assert decision.fixed_resolver_exists_within_budget
    assert decision.feasible_bundle is not None
    assert decision.infeasibility_proof is None
    assert verify_fixed_budget_decision_certificate(task, decision)
    assert not selected_policy_integer_cover_gain_certificate(
        task
    ).strict_adaptive_gain_certified_without_fixed_optimum


def test_integer_cover_proof_also_certifies_registered_payoff_witness():
    task = payoff_routing_task()
    certificate = selected_policy_integer_cover_gain_certificate(task)
    assert certificate.strict_adaptive_gain_certified_without_fixed_optimum
    assert certificate.fixed_budget_decision is not None
    assert verify_fixed_budget_decision_certificate(task, certificate.fixed_budget_decision)


def test_tampered_proof_fails_verification():
    task = _integrality_gap_task()
    decision = fixed_budget_cover_decision(task, budget=2)
    proof = decision.infeasibility_proof
    assert proof is not None
    from dataclasses import replace
    tampered = replace(decision, infeasibility_proof=replace(proof, remaining_budget=99))
    assert not verify_fixed_budget_decision_certificate(task, tampered)


def test_integer_cover_proof_fails_closed_at_state_cap():
    with pytest.raises(IntegerCoverProofLimitError):
        fixed_budget_cover_decision(_integrality_gap_task(), budget=2, max_states=1)
