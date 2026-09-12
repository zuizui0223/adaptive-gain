"""Claim-gating helpers for prospective empirical adaptive-gain studies.

This module is deliberately conservative. It does not turn a mathematical
finite-task fixture into empirical evidence. Instead it records which layers
of biological qualification have been supplied and returns only the claims
licensed by those declarations.

The intended use is prospective: freeze a task and an evidence receipt before
opening the final outcome matrix, then update the evidence fields without
changing the task semantics after seeing the structural gap.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import FiniteTask, adaptive_gain_receipt


@dataclass(frozen=True)
class EmpiricalAdmissionEvidence:
    """Declared evidence layers for one frozen biological finite task."""

    task_semantics_qualified: bool = False
    measurement_resolution_qualified: bool = False
    target_ontology_qualified: bool = False
    cost_semantics_qualified: bool = False
    terminal_channel_causality_qualified: bool = False
    state_routing_causality_qualified: bool = False
    genotype_policy_map_qualified: bool = False
    mutation_support_graph_qualified: bool = False
    start_state_declared: bool = False
    mutation_bias_or_neutral_measure_qualified: bool = False
    population_process_declared: bool = False
    absolute_rate_scale_qualified: bool = False


@dataclass(frozen=True)
class EmpiricalClaimGateReceipt:
    adaptive_cost: int | None
    fixed_cost: int | None
    structural_gap: int | None
    mathematical_positive_gap: bool
    empirical_task_admitted: bool
    empirical_positive_gap_licensed: bool
    context_routing_mechanism_licensed: bool
    positive_gap_with_causal_routing_licensed: bool
    mutational_accessibility_licensed: bool
    stationary_occupancy_licensed: bool
    biological_waiting_time_licensed: bool
    licensed_claims: tuple[str, ...]
    prohibited_claims: tuple[str, ...]


def empirical_claim_gate_receipt(
    task: FiniteTask,
    evidence: EmpiricalAdmissionEvidence,
) -> EmpiricalClaimGateReceipt:
    """Return the exact structural result and separately gated empirical claims."""

    exact = adaptive_gain_receipt(task)
    ca, cf = exact.adaptive_cost, exact.fixed_cost
    gap = None if ca is None or cf is None else cf - ca
    mathematical_positive = gap is not None and gap > 0

    admitted = (
        evidence.task_semantics_qualified
        and evidence.measurement_resolution_qualified
        and evidence.target_ontology_qualified
        and evidence.cost_semantics_qualified
        and ca is not None
        and cf is not None
    )
    empirical_positive = admitted and mathematical_positive

    # Context-dependent sensory routing is a mechanistic claim distinct from
    # positive structural gain. A zero-gap system may still have real routing.
    routing = (
        admitted
        and evidence.terminal_channel_causality_qualified
        and evidence.state_routing_causality_qualified
    )
    positive_routing = empirical_positive and routing

    # Every downstream biological claim is stacked on an admitted finite task.
    # A genotype representation attached only to a prospective/mathematical
    # fixture must not bypass the biological admission gate.
    accessibility = (
        admitted
        and evidence.genotype_policy_map_qualified
        and evidence.mutation_support_graph_qualified
        and evidence.start_state_declared
    )

    # Stationary occupancy additionally depends on relative mutation bias and a
    # population process. A start state is not mathematically required for a
    # stationary law, so it is intentionally not part of this gate.
    stationary = (
        admitted
        and evidence.genotype_policy_map_qualified
        and evidence.mutation_support_graph_qualified
        and evidence.mutation_bias_or_neutral_measure_qualified
        and evidence.population_process_declared
    )

    # Biological waiting time needs an accessible representation, a declared
    # population process, and an absolute rate scale connecting model events to
    # biological time.
    waiting = (
        accessibility
        and evidence.population_process_declared
        and evidence.absolute_rate_scale_qualified
    )

    claims: list[str] = []
    prohibited: list[str] = []

    if admitted:
        claims.append("frozen_empirical_finite_task_admitted")
    else:
        prohibited.append("empirical_finite_task_admission")

    if empirical_positive:
        claims.append("empirical_positive_adaptive_fixed_gap")
    else:
        prohibited.append("empirical_positive_adaptive_fixed_gap")

    if routing:
        claims.append("causal_context_dependent_terminal_information_use")
    else:
        prohibited.append("causal_context_dependent_terminal_information_use")

    if positive_routing:
        claims.append("positive_adaptive_gap_with_causal_context_routing")
    else:
        prohibited.append("positive_adaptive_gap_with_causal_context_routing")

    if accessibility:
        claims.append("mutational_accessibility_within_declared_representation")
    else:
        prohibited.append("mutational_accessibility")

    if stationary:
        claims.append("stationary_occupancy_within_declared_mutation_selection_model")
    else:
        prohibited.append("stationary_population_occupancy")

    if waiting:
        claims.append("biological_waiting_time_within_declared_rate_model")
    else:
        prohibited.append("biological_waiting_time")

    return EmpiricalClaimGateReceipt(
        adaptive_cost=ca,
        fixed_cost=cf,
        structural_gap=gap,
        mathematical_positive_gap=mathematical_positive,
        empirical_task_admitted=admitted,
        empirical_positive_gap_licensed=empirical_positive,
        context_routing_mechanism_licensed=routing,
        positive_gap_with_causal_routing_licensed=positive_routing,
        mutational_accessibility_licensed=accessibility,
        stationary_occupancy_licensed=stationary,
        biological_waiting_time_licensed=waiting,
        licensed_claims=tuple(claims),
        prohibited_claims=tuple(prohibited),
    )
