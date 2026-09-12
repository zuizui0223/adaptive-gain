"""Prospective four-world Aedes gonotrophic finite-task fixture.

This module does not encode a published empirical adaptive-gain result.  It
freezes the exact q=1 laboratory task proposed in
``biology/AEDES_GONOTROPHIC_FINITE_TASK_QUALIFICATION_V1.md`` so the structural
claim can be checked independently by the repository's exact solver before any
future biological outcome matrix is opened.

The declared unit-cost task is

    H0 = (R,A,B) = (0,0,0)
    H1 =           (0,1,0)
    O0 =           (1,0,0)
    O1 =           (1,0,1)

where R is gonotrophic state, A is the host-branch acidic-cue channel and B is
the oviposition-branch odor channel.  Four distinct target actions are declared.

The mathematical fixture has C_A=2, C_F=3 and g=1.  Whether the biological
system is admissible under these cue/cost semantics is a separate empirical
gate and must not be inferred from this file.
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


def aedes_gonotrophic_q1_task() -> FiniteTask:
    """Return the prospectively frozen unit-cost four-world star task."""

    worlds = (
        World("H0", "reject_host"),
        World("H1", "approach_host"),
        World("O0", "reject_oviposition"),
        World("O1", "accept_oviposition"),
    )
    queries = (
        Query("gonotrophic_state", 1, (0, 0, 1, 1)),
        Query("host_acidic_cue", 1, (0, 1, 0, 0)),
        Query("oviposition_odor_cue", 1, (0, 0, 0, 1)),
    )
    return FiniteTask(worlds, queries)


@dataclass(frozen=True)
class AedesGonotrophicFixtureReceipt:
    adaptive_cost: int
    fixed_cost: int
    structural_gap: int
    optimal_first_queries: tuple[str, ...]
    optimal_fixed_bundles: tuple[tuple[str, ...], ...]
    prospective_only: bool = True


def aedes_gonotrophic_q1_receipt() -> AedesGonotrophicFixtureReceipt:
    """Independently solve the frozen task and return its structural receipt."""

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
