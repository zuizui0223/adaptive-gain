"""Finite witnesses abstracted from MROD, PAYOFF, and BALANCE structures."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from .core import FiniteTask, Query, World
from .certificates import branch_invariant_no_routing_certificate

def mrod_routing_task() -> FiniteTask:
    states = tuple(product((0, 1), repeat=4))  # c,t,n0,n1
    worlds = tuple(World(f"c{c}_t{t}_n{n0}{n1}", t) for c, t, n0, n1 in states)
    context = tuple(str(c) for c, t, n0, n1 in states)
    assay0 = tuple(str(t if c == 0 else n0) for c, t, n0, n1 in states)
    assay1 = tuple(str(n1 if c == 0 else t) for c, t, n0, n1 in states)
    return FiniteTask(
        worlds,
        (
            Query("context", 1, context),
            Query("assay0", 1, assay0),
            Query("assay1", 1, assay1),
        ),
    )

def payoff_routing_task() -> FiniteTask:
    worlds = (
        World("low_alpha_wide", False),
        World("low_alpha_middle", True),
        World("high_alpha_middle", False),
        World("high_alpha_narrow", True),
    )
    return FiniteTask(
        worlds,
        (
            Query("intrinsic_r_0.5", 1, ("low", "low", "high", "high")),
            Query("interaction_d_0.2", 1, ("wide", "middle", "middle", "middle")),
            Query("interaction_d_0.1", 1, ("baseline", "baseline", "baseline", "narrow")),
        ),
    )

def direct_resolution_control() -> FiniteTask:
    worlds = (World("no", False), World("yes", True))
    return FiniteTask(worlds, (Query("direct", 1, ("no", "yes")),))

@dataclass(frozen=True)
class BalanceSpanWitness:
    forward_branch_signatures: dict[str, tuple[Fraction, ...]]
    reverse_branch_signatures: dict[str, tuple[Fraction, ...]]

def _a(span: Fraction, error: Fraction) -> Fraction:
    return min(span, span / 2 + error)

def balance_span_witness(
    *,
    forward_span: Fraction = Fraction(3, 100),
    reverse_span: Fraction = Fraction(4, 100),
    forward_error: Fraction = Fraction(1, 200),
    reverse_error: Fraction = Fraction(1, 200),
    remaining_budget_after_query: int = 1,
    forward_cost: int = 1,
    reverse_cost: int = 1,
) -> BalanceSpanWitness:
    if remaining_budget_after_query < 0 or min(forward_cost, reverse_cost) <= 0:
        raise ValueError("budget must be nonnegative and costs positive")
    common_tail = (
        Fraction(remaining_budget_after_query),
        forward_error,
        reverse_error,
        Fraction(forward_cost),
        Fraction(reverse_cost),
    )
    f_signature = (_a(forward_span, forward_error), reverse_span, *common_tail)
    r_signature = (forward_span, _a(reverse_span, reverse_error), *common_tail)
    return BalanceSpanWitness(
        {"stay": f_signature, "switch": f_signature},
        {"stay": r_signature, "switch": r_signature},
    )

def balance_no_routing_certificates():
    witness = balance_span_witness()
    return (
        branch_invariant_no_routing_certificate(witness.forward_branch_signatures),
        branch_invariant_no_routing_certificate(witness.reverse_branch_signatures),
    )
