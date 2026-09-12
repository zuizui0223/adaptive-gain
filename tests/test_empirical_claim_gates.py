from adaptive_gain.aedes_gonotrophic_fixture import (
    aedes_gonotrophic_coarsened_target_task,
    aedes_gonotrophic_q1_task,
)
from adaptive_gain.empirical_claim_gates import (
    EmpiricalAdmissionEvidence,
    empirical_claim_gate_receipt,
)


def _admitted_base(**overrides):
    values = dict(
        task_semantics_qualified=True,
        measurement_resolution_qualified=True,
        target_ontology_qualified=True,
        cost_semantics_qualified=True,
    )
    values.update(overrides)
    return EmpiricalAdmissionEvidence(**values)


def test_prospective_mathematical_fixture_does_not_become_empirical_claim():
    receipt = empirical_claim_gate_receipt(
        aedes_gonotrophic_q1_task(),
        EmpiricalAdmissionEvidence(),
    )
    assert receipt.adaptive_cost == 2
    assert receipt.fixed_cost == 3
    assert receipt.structural_gap == 1
    assert receipt.mathematical_positive_gap is True
    assert receipt.empirical_task_admitted is False
    assert receipt.empirical_positive_gap_licensed is False
    assert receipt.context_routing_mechanism_licensed is False
    assert "empirical_positive_adaptive_fixed_gap" in receipt.prohibited_claims


def test_downstream_evidence_cannot_bypass_failed_task_admission():
    evidence = EmpiricalAdmissionEvidence(
        terminal_channel_causality_qualified=True,
        state_routing_causality_qualified=True,
        genotype_policy_map_qualified=True,
        mutation_support_graph_qualified=True,
        start_state_declared=True,
        mutation_bias_or_neutral_measure_qualified=True,
        population_process_declared=True,
        absolute_rate_scale_qualified=True,
    )
    receipt = empirical_claim_gate_receipt(aedes_gonotrophic_q1_task(), evidence)
    assert receipt.mathematical_positive_gap is True
    assert receipt.empirical_task_admitted is False
    assert receipt.context_routing_mechanism_licensed is False
    assert receipt.mutational_accessibility_licensed is False
    assert receipt.stationary_occupancy_licensed is False
    assert receipt.biological_waiting_time_licensed is False


def test_admitted_positive_task_licenses_gap_but_not_causal_routing():
    receipt = empirical_claim_gate_receipt(
        aedes_gonotrophic_q1_task(),
        _admitted_base(),
    )
    assert receipt.empirical_task_admitted is True
    assert receipt.empirical_positive_gap_licensed is True
    assert receipt.context_routing_mechanism_licensed is False
    assert receipt.positive_gap_with_causal_routing_licensed is False


def test_terminal_and_state_causality_are_both_required_for_routing_claim():
    terminal_only = empirical_claim_gate_receipt(
        aedes_gonotrophic_q1_task(),
        _admitted_base(terminal_channel_causality_qualified=True),
    )
    assert terminal_only.context_routing_mechanism_licensed is False

    routed = empirical_claim_gate_receipt(
        aedes_gonotrophic_q1_task(),
        _admitted_base(
            terminal_channel_causality_qualified=True,
            state_routing_causality_qualified=True,
        ),
    )
    assert routed.context_routing_mechanism_licensed is True
    assert routed.positive_gap_with_causal_routing_licensed is True


def test_zero_gap_can_still_license_real_context_routing_mechanism():
    task = aedes_gonotrophic_coarsened_target_task(1, 1, 1)
    receipt = empirical_claim_gate_receipt(
        task,
        _admitted_base(
            terminal_channel_causality_qualified=True,
            state_routing_causality_qualified=True,
        ),
    )
    assert receipt.structural_gap == 0
    assert receipt.empirical_positive_gap_licensed is False
    assert receipt.context_routing_mechanism_licensed is True
    assert receipt.positive_gap_with_causal_routing_licensed is False


def test_accessibility_requires_map_support_and_start_state():
    incomplete = empirical_claim_gate_receipt(
        aedes_gonotrophic_q1_task(),
        _admitted_base(
            genotype_policy_map_qualified=True,
            mutation_support_graph_qualified=True,
        ),
    )
    assert incomplete.mutational_accessibility_licensed is False

    complete = empirical_claim_gate_receipt(
        aedes_gonotrophic_q1_task(),
        _admitted_base(
            genotype_policy_map_qualified=True,
            mutation_support_graph_qualified=True,
            start_state_declared=True,
        ),
    )
    assert complete.mutational_accessibility_licensed is True
    assert complete.stationary_occupancy_licensed is False
    assert complete.biological_waiting_time_licensed is False


def test_stationary_occupancy_requires_mutation_bias_and_population_process():
    evidence = _admitted_base(
        genotype_policy_map_qualified=True,
        mutation_support_graph_qualified=True,
        mutation_bias_or_neutral_measure_qualified=True,
        population_process_declared=True,
    )
    receipt = empirical_claim_gate_receipt(aedes_gonotrophic_q1_task(), evidence)
    assert receipt.stationary_occupancy_licensed is True
    assert receipt.mutational_accessibility_licensed is False  # no start state
    assert receipt.biological_waiting_time_licensed is False


def test_biological_waiting_time_requires_absolute_rate_scale():
    base = dict(
        genotype_policy_map_qualified=True,
        mutation_support_graph_qualified=True,
        start_state_declared=True,
        population_process_declared=True,
    )
    no_rate = empirical_claim_gate_receipt(
        aedes_gonotrophic_q1_task(),
        _admitted_base(**base),
    )
    assert no_rate.biological_waiting_time_licensed is False

    with_rate = empirical_claim_gate_receipt(
        aedes_gonotrophic_q1_task(),
        _admitted_base(**base, absolute_rate_scale_qualified=True),
    )
    assert with_rate.biological_waiting_time_licensed is True
