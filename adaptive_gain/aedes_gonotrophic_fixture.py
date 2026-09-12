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
the oviposition-branch odor channel.  Four distinct target actions are declared.

With unit costs the mathematical fixture has C_A=2, C_F=3 and g=1.  More
generally, for positive integer costs (r,a,b), the same task has

    C_A = r + max(a,b)
    C_F = r + a + b
    g   = min(a,b) > 0.

Thus equal cue costs are not required for strict structural gain in this
prospective witness.  Whether the biological system is admissible under any
particular cue/cost semantics is a separate empirical gate and must not be
inferred from this file.
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


def aedes_gonotrophic_weighted_task(
    state_cost: int,
    host_cost: int,
    oviposition_cost: int,
) -> FiniteTask:
    """Return the frozen four-world star with declared positive integer costs."""

    r = _validate_cost(state_cost, "state_cost")
    a = _validate_cost(host_cost, "host_cost")
    b = _validate_cost(oviposition_cost, "oviposition_cost")
    worlds = (
        World("H0", "reject_host"),
        World("H1", "approach_host"),
        World("O0", "reject_oviposition"),
        World("O1", "accept_oviposition"),
    )
    queries = (
        Query("gonotrophic_state", r, (0, 0, 1, 1)),
        Query("host_acidic_cue", a, (0, 1, 0, 0)),
        Query("oviposition_odor_cue", b, (0, 0, 0, 1)),
    )
    return FiniteTask(worlds, queries)


def aedes_gonotrophic_q1_task() -> FiniteTask:
    """Return the prospectively frozen unit-cost four-world star task."""

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


def aedes_gonotrophic_weighted_receipt(
    state_cost: int,
    host_cost: int,
    oviposition_cost: int,
) -> AedesWeightedCostReceipt:
    """Verify the exact unequal-cost formula against the generic solver."""

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


def aedes_gonotrophic_q1_receipt() -> AedesGonotrophicFixtureReceipt:
    """Independently solve the unit-cost frozen task and return its receipt."""

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
