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


def routing_bypass_control() -> FiniteTask:
    """Branch-dependent routing where the selected tree union contains redundancy.

    The selected optimal tree can use all three query identities, but the fixed
    subset (q_left,q_right) already resolves the target.  In the refined bypass
    decomposition this is INTERNAL union redundancy rather than an external
    shortcut: C_A=2, C_F=C_U=2, U=3.
    """
    worlds = (
        World("w0", 0),
        World("w1", 0),
        World("w2", 1),
        World("w3", 1),
    )
    return FiniteTask(
        worlds,
        (
            Query("q_left", 1, (0, 0, 0, 1)),
            Query("q_route", 1, (0, 1, 0, 1)),
            Query("q_right", 1, (0, 1, 1, 0)),
        ),
    )


def external_shortcut_control() -> FiniteTask:
    """No strict gain because a query OUTSIDE the selected tree union shortcuts it.

    The selected optimal adaptive tree uses q0,q1,q2 with worst-path cost 2.
    Flattening that union requires all three queries (C_U=3), but the global fixed
    bundle (q2,q3) resolves at cost 2.  Thus U=3, C_U=3, C_F=C_A=2 and the entire
    bypass discount is external.
    """
    worlds = (
        World("w0", 0),
        World("w1", 0),
        World("w2", 1),
        World("w3", 1),
    )
    return FiniteTask(
        worlds,
        (
            Query("q0", 1, (0, 0, 0, 1)),
            Query("q1", 1, (0, 1, 0, 0)),
            Query("q2", 1, (0, 1, 1, 0)),
            Query("q3_external", 1, (0, 1, 0, 1)),
        ),
    )


def internal_redundancy_control() -> FiniteTask:
    """No strict gain because the selected tree union itself has a cheaper fixed subset.

    q_unused is constant.  The selected adaptive tree's union contains q1,q2,q3
    with U=3, but q2+q3 already resolve, so C_U=C_F=2 and the entire bypass
    discount is internal to the union.
    """
    worlds = (
        World("w0", 0),
        World("w1", 0),
        World("w2", 1),
        World("w3", 1),
    )
    return FiniteTask(
        worlds,
        (
            Query("q_unused", 1, (0, 0, 0, 0)),
            Query("q1", 1, (0, 0, 0, 1)),
            Query("q2", 1, (0, 1, 0, 1)),
            Query("q3", 1, (0, 1, 1, 0)),
        ),
    )


def partial_internal_bypass_gain_control() -> FiniteTask:
    """Strict gain survives one unit of INTERNAL union redundancy.

    Six balanced target worlds and six unit-cost binary queries give

        C_A=3, C_F=C_U=4, U=5.

    Hence branch-exclusive overhead is 2, internal union redundancy is 1, and
    realized adaptive gain remains 1.  q5 is constant and unused.
    """
    worlds = tuple(
        World(f"w{i}", 0 if i < 3 else 1)
        for i in range(6)
    )
    maps = (
        (1, 0, 1, 1, 1, 0),
        (0, 1, 1, 0, 1, 1),
        (1, 1, 0, 1, 0, 0),
        (0, 1, 1, 1, 1, 1),
        (0, 0, 1, 0, 0, 0),
        (1, 1, 1, 1, 1, 1),
    )
    return FiniteTask(worlds, tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)))


def partial_external_bypass_gain_control() -> FiniteTask:
    """Strict gain survives one unit of EXTERNAL fixed shortcut discount.

    Six balanced target worlds and six unit-cost binary queries give

        C_A=3, C_F=4, C_U=5, U=5.

    The selected adaptive union is internally irreducible, but an outside query
    lets the global fixed class save one unit; one unit of adaptive gain remains.
    """
    worlds = tuple(
        World(f"w{i}", 0 if i < 3 else 1)
        for i in range(6)
    )
    maps = (
        (1, 1, 1, 1, 1, 0),
        (1, 0, 1, 1, 1, 0),
        (1, 0, 0, 0, 1, 0),
        (0, 0, 1, 0, 0, 0),
        (1, 1, 0, 1, 1, 0),
        (0, 0, 0, 0, 1, 0),
    )
    return FiniteTask(worlds, tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)))


def positive_root_information_gain_control() -> FiniteTask:
    """Strict gain where an optimal root has POSITIVE direct target information."""
    worlds = (
        World("w0", 0),
        World("w1", 0),
        World("w2", 1),
        World("w3", 1),
        World("w4", 1),
    )
    return FiniteTask(
        worlds,
        (
            Query("q_left", 1, (0, 0, 0, 0, 1)),
            Query("q_right", 1, (0, 1, 0, 0, 0)),
            Query("q_route", 1, (0, 1, 1, 1, 0)),
        ),
    )


def fractional_only_gain_control() -> FiniteTask:
    """Strict gain certified by fractional but not integral pair packing.

    C_A=2, C_F=3.  Maximum integral pair packing is 2, while the exact
    fractional pair-cover dual optimum is 5/2 and therefore rounds to the integer
    lower bound C_F>=3.
    """
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1), World("w4", 1),
    )
    maps = (
        (1, 0, 1, 0, 1),
        (0, 1, 1, 0, 0),
        (0, 1, 1, 1, 1),
        (1, 1, 0, 1, 0),
    )
    return FiniteTask(worlds, tuple(Query(f"q{i}", 1, row) for i, row in enumerate(maps)))


def fractional_integrality_gap_gain_control() -> FiniteTask:
    """Strict gain whose fixed-cost proof survives only at the integer cover layer.

    C_A=2 and C_F=3, but both the maximum integral pair packing and exact
    fractional pair-cover dual optimum equal 2.  Thus the LP relaxation has an
    integrality gap and cannot certify the true strict gain.
    """
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
