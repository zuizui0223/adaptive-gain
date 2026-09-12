"""Context-semantics controls for the prospective Aedes gonotrophic task.

The positive four-world adaptive-gain fixture treats gonotrophic state as an
information source used *inside one decision architecture*.  This module encodes
the crucial negative control: if gonotrophic state is instead externally known
before policy commitment, and the fixed comparator may choose a different
terminal bundle in each state, the problem decomposes into two branch-local
tasks and the adaptive/fixed gap is zero in each branch.

This distinction is biological, not algebraic bookkeeping.  A prospective
experiment must therefore justify which comparator semantics correspond to the
organism's sensing architecture before interpreting a positive integrated gap.
"""
from __future__ import annotations

from dataclasses import dataclass

from .aedes_gonotrophic_fixture import aedes_gonotrophic_weighted_receipt
from .core import FiniteTask, Query, World, adaptive_gain_receipt


def _validate_cost(value: int, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def aedes_preindexed_host_task(host_cost: int) -> FiniteTask:
    """Host branch when gonotrophic context is known before policy choice."""

    a = _validate_cost(host_cost, "host_cost")
    worlds = (
        World("H0", "continue_host_search"),
        World("H1", "approach_host"),
    )
    return FiniteTask(worlds, (Query("host_acidic_cue", a, (0, 1)),))


def aedes_preindexed_oviposition_task(oviposition_cost: int) -> FiniteTask:
    """Oviposition branch when gonotrophic context is known before policy choice."""

    b = _validate_cost(oviposition_cost, "oviposition_cost")
    worlds = (
        World("O0", "continue_oviposition_search"),
        World("O1", "accept_oviposition_site"),
    )
    return FiniteTask(worlds, (Query("oviposition_site_cue", b, (0, 1)),))


@dataclass(frozen=True)
class AedesContextSemanticsReceipt:
    state_cost: int
    host_cost: int
    oviposition_cost: int
    integrated_adaptive_cost: int
    integrated_fixed_cost: int
    integrated_gap: int
    host_branch_adaptive_cost: int
    host_branch_fixed_cost: int
    host_branch_gap: int
    oviposition_branch_adaptive_cost: int
    oviposition_branch_fixed_cost: int
    oviposition_branch_gap: int
    positive_gain_requires_within_architecture_state_use: bool
    prospective_only: bool = True


def aedes_context_semantics_receipt(
    state_cost: int,
    host_cost: int,
    oviposition_cost: int,
) -> AedesContextSemanticsReceipt:
    """Compare integrated-state sensing to externally pre-indexed contexts."""

    r = _validate_cost(state_cost, "state_cost")
    a = _validate_cost(host_cost, "host_cost")
    b = _validate_cost(oviposition_cost, "oviposition_cost")

    integrated = aedes_gonotrophic_weighted_receipt(r, a, b)
    host = adaptive_gain_receipt(aedes_preindexed_host_task(a))
    oviposition = adaptive_gain_receipt(aedes_preindexed_oviposition_task(b))

    if host.adaptive_cost != a or host.fixed_cost != a:
        raise ArithmeticError("pre-indexed host branch should have zero structural gap")
    if oviposition.adaptive_cost != b or oviposition.fixed_cost != b:
        raise ArithmeticError("pre-indexed oviposition branch should have zero structural gap")

    host_gap = host.fixed_cost - host.adaptive_cost
    oviposition_gap = oviposition.fixed_cost - oviposition.adaptive_cost
    if host_gap != 0 or oviposition_gap != 0:
        raise ArithmeticError("pre-indexed context control unexpectedly retained adaptive gain")

    return AedesContextSemanticsReceipt(
        state_cost=r,
        host_cost=a,
        oviposition_cost=b,
        integrated_adaptive_cost=integrated.adaptive_cost,
        integrated_fixed_cost=integrated.fixed_cost,
        integrated_gap=integrated.structural_gap,
        host_branch_adaptive_cost=host.adaptive_cost,
        host_branch_fixed_cost=host.fixed_cost,
        host_branch_gap=host_gap,
        oviposition_branch_adaptive_cost=oviposition.adaptive_cost,
        oviposition_branch_fixed_cost=oviposition.fixed_cost,
        oviposition_branch_gap=oviposition_gap,
        positive_gain_requires_within_architecture_state_use=True,
    )
