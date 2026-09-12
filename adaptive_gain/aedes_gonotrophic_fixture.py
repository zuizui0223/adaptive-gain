"""Prospective four-world Aedes gonotrophic finite-task fixture.

This module does not encode a published empirical adaptive-gain result.  It
freezes the exact q=1 laboratory task proposed in
``biology/AEDES_GONOTROPHIC_FINITE_TASK_QUALIFICATION_V1.md`` so the structural
claim can be checked independently by the repository's exact solver before any
future biological outcome matrix is opened.

The declared outcome table is

    H0 = (R,A,B) = (0,0,0)
    H1 =           (0,1,0)
    O0 =           (1,0,0)
    O1 =           (1,0,1)

where R is gonotrophic state, A is the host-branch acidic-cue channel and B is
the oviposition-branch odor channel.

With four biologically distinct target actions and unit costs the mathematical
fixture has C_A=2, C_F=3 and g=1.  More generally, for positive integer costs
(r,a,b), the same target partition has

    C_A = r + max(a,b)
    C_F = r + a + b
    g   = min(a,b) > 0.

A target-coarsening control is included deliberately.  If host/oviposition
actions are collapsed to generic ``accept`` versus ``reject``, then

    C_F = a + b
    C_A = min(a+b, r+max(a,b))
    g   = max(0, min(a,b)-r).

Thus the equal-cost coarsened task has g=0.  Positive gain must not be created by
post-hoc target semantics.  Whether either target partition is biologically
admissible is an empirical gate, not a consequence of this fixture.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    adaptive_minimum_resolution,
    fixed_minimum_resolution,
)


def _validate_cost(value: int, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _queries(r: int, a: int, b: int) -> tuple[Query, ...]:
    return (
        Query("gonotrophic_state", r, (0, 0, 1, 1)),
        Query("host_acidic_cue", a, (0, 1, 0, 0)),
        Query("oviposition_odor_cue", b, (0, 0, 0, 1)),
    )


def aedes_gonotrophic_weighted_task(
    state_cost: int,
    host_cost: int,
    oviposition_cost: int,
) -> FiniteTask:
    """Four distinct host/oviposition target actions."""

    r = _validate_cost(state_cost, "state_cost")
    a = _validate_cost(host_cost, "host_cost")
    b = _validate_cost(oviposition_cost, "oviposition_cost")
    worlds = (
        World("H0", "continue_host_search"),
        World("H1", "approach_host"),
        World("O0", "continue_oviposition_search"),
        World("O1", "accept_oviposition_site"),
    )
    return FiniteTask(worlds, _queries(r, a, b))


def aedes_gonotrophic_coarsened_target_task(
    state_cost: int,
    host_cost: int,
    oviposition_cost: int,
) -> FiniteTask:
    """Falsification control collapsing the targets to generic reject/accept."""

    r = _validate_cost(state_cost, "state_cost")
    a = _validate_cost(host_cost, "host_cost")
    b = _validate_cost(oviposition_cost, "oviposition_cost")
    worlds = (
        World("H0", "reject"),
        World("H1", "accept"),
        World("O0", "reject"),
        World("O1", "accept"),
    )
    return FiniteTask(worlds, _queries(r, a, b))


def aedes_gonotrophic_q1_task() -> FiniteTask:
    """Return the prospectively frozen unit-cost four-target star task."""

    return aedes_gonotrophic_weighted_task(1, 1, 1)


@dataclass(frozen=True)
class AedesGonotrophicFixtureReceipt:
    adaptive_cost: int
    fixed_cost: int
    structural_gap: int
    optimal_first_queries: tuple[str, ...]
    optimal_fixed_bundles: tuple[tuple[str, ...], ...]
    prospective_only: bool = True


@dataclass(frozen=True)
class AedesWeightedCostReceipt:
    state_cost: int
    host_cost: int
    oviposition_cost: int
    adaptive_cost: int
    fixed_cost: int
    structural_gap: int
    expected_adaptive_cost: int
    expected_fixed_cost: int
    expected_gap: int
    exact_formula_verified: bool
    prospective_only: bool = True


@dataclass(frozen=True)
class AedesTargetCoarseningReceipt:
    state_cost: int
    host_cost: int
    oviposition_cost: int
    adaptive_cost: int
    fixed_cost: int
    structural_gap: int
    expected_gap: int
    strict_gain: bool
    prospective_only: bool = True


def aedes_gonotrophic_weighted_receipt(
    state_cost: int,
    host_cost: int,
    oviposition_cost: int,
) -> AedesWeightedCostReceipt:
    """Verify the exact unequal-cost four-target formula against the solver."""

    r = _validate_cost(state_cost, "state_cost")
    a = _validate_cost(host_cost, "host_cost")
    b = _validate_cost(oviposition_cost, "oviposition_cost")
    task = aedes_gonotrophic_weighted_task(r, a, b)
    exact = adaptive_gain_receipt(task)
    if exact.adaptive_cost is None or exact.fixed_cost is None:
        raise ArithmeticError("prospective Aedes weighted fixture became unresolved")

    expected_ca = r + max(a, b)
    expected_cf = r + a + b
    expected_gap = min(a, b)
    verified = (
        exact.adaptive_cost == expected_ca
        and exact.fixed_cost == expected_cf
        and exact.fixed_cost - exact.adaptive_cost == expected_gap
        and exact.strict_adaptive_gain
    )
    if not verified:
        raise ArithmeticError("prospective Aedes weighted-cost formula failed exact audit")

    return AedesWeightedCostReceipt(
        state_cost=r,
        host_cost=a,
        oviposition_cost=b,
        adaptive_cost=exact.adaptive_cost,
        fixed_cost=exact.fixed_cost,
        structural_gap=exact.fixed_cost - exact.adaptive_cost,
        expected_adaptive_cost=expected_ca,
        expected_fixed_cost=expected_cf,
        expected_gap=expected_gap,
        exact_formula_verified=True,
    )


def aedes_target_coarsening_receipt(
    state_cost: int,
    host_cost: int,
    oviposition_cost: int,
) -> AedesTargetCoarseningReceipt:
    """Audit the generic accept/reject target partition as a negative control."""

    r = _validate_cost(state_cost, "state_cost")
    a = _validate_cost(host_cost, "host_cost")
    b = _validate_cost(oviposition_cost, "oviposition_cost")
    task = aedes_gonotrophic_coarsened_target_task(r, a, b)
    exact = adaptive_gain_receipt(task)
    if exact.adaptive_cost is None or exact.fixed_cost is None:
        raise ArithmeticError("coarsened Aedes control unexpectedly became unresolved")

    expected_cf = a + b
    expected_ca = min(a + b, r + max(a, b))
    expected_gap = max(0, min(a, b) - r)
    if (
        exact.adaptive_cost != expected_ca
        or exact.fixed_cost != expected_cf
        or exact.fixed_cost - exact.adaptive_cost != expected_gap
    ):
        raise ArithmeticError("Aedes target-coarsening formula failed exact audit")

    return AedesTargetCoarseningReceipt(
        state_cost=r,
        host_cost=a,
        oviposition_cost=b,
        adaptive_cost=exact.adaptive_cost,
        fixed_cost=exact.fixed_cost,
        structural_gap=exact.fixed_cost - exact.adaptive_cost,
        expected_gap=expected_gap,
        strict_gain=exact.strict_adaptive_gain,
    )


def aedes_gonotrophic_q1_receipt() -> AedesGonotrophicFixtureReceipt:
    """Independently solve the unit-cost frozen four-target task."""

    task = aedes_gonotrophic_q1_task()
    gain = adaptive_gain_receipt(task)
    adaptive = adaptive_minimum_resolution(task)
    fixed = fixed_minimum_resolution(task)

    if gain.adaptive_cost is None or gain.fixed_cost is None:
        raise ArithmeticError("prospective Aedes fixture unexpectedly became unresolved")
    if gain.adaptive_cost != 2 or gain.fixed_cost != 3:
        raise ArithmeticError("prospective Aedes q=1 fixture changed exact costs")
    if not gain.strict_adaptive_gain:
        raise ArithmeticError("prospective Aedes q=1 fixture lost strict adaptive gain")
    if adaptive.optimal_first_queries != ("gonotrophic_state",):
        raise ArithmeticError("gonotrophic state is no longer the unique optimal root query")
    if fixed.optimal_bundles != (
        ("gonotrophic_state", "host_acidic_cue", "oviposition_odor_cue"),
    ):
        raise ArithmeticError("prospective Aedes fixture changed its unique optimal fixed bundle")

    return AedesGonotrophicFixtureReceipt(
        adaptive_cost=gain.adaptive_cost,
        fixed_cost=gain.fixed_cost,
        structural_gap=gain.fixed_cost - gain.adaptive_cost,
        optimal_first_queries=adaptive.optimal_first_queries,
        optimal_fixed_bundles=fixed.optimal_bundles,
    )
