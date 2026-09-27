"""Scenario construction for routeability GLMM operating-characteristic simulation.

This module does not fit the final mixed model. It constructs validated 12-cell
probability scenarios from externally frozen H1/H2 SESOI values and baseline
planning assumptions. A separate R script simulates trial data, fits the
frozen binomial mixed model, and evaluates H1/H2.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .routeability_experiment_power import RouteabilitySESoi

ARCHITECTURES = ("bypass_control", "routeable")
ACCESS_MODES = ("fixed", "contingent")
BUDGETS = (1, 2, 3)


def _unit_probability(value: float, name: str) -> float:
    out = float(value)
    if not 0.0 < out < 1.0:
        raise ValueError(f"{name} must be in (0,1)")
    return out


@dataclass(frozen=True)
class RouteabilityCellScenario:
    cell_probabilities: Mapping[tuple[str, str, int], float]
    h1_delta_b2: float
    h2_localization: float
    sesoi_provenance: str

    def validated(self) -> "RouteabilityCellScenario":
        expected = {
            (architecture, access, budget)
            for architecture in ARCHITECTURES
            for access in ACCESS_MODES
            for budget in BUDGETS
        }
        keys = set(self.cell_probabilities)
        if keys != expected:
            missing = sorted(expected - keys)
            extra = sorted(keys - expected)
            raise ValueError(
                f"cell probability surface mismatch; missing={missing!r}, extra={extra!r}"
            )
        for key, value in self.cell_probabilities.items():
            _unit_probability(value, f"cell probability {key!r}")

        deltas = {
            budget: (
                self.cell_probabilities[("routeable", "contingent", budget)]
                - self.cell_probabilities[("routeable", "fixed", budget)]
                - self.cell_probabilities[("bypass_control", "contingent", budget)]
                + self.cell_probabilities[("bypass_control", "fixed", budget)]
            )
            for budget in BUDGETS
        }
        h1 = deltas[2]
        h2 = deltas[2] - 0.5 * (deltas[1] + deltas[3])
        if abs(h1 - self.h1_delta_b2) > 1e-12:
            raise ValueError("cell surface does not realize frozen H1 SESOI")
        if abs(h2 - self.h2_localization) > 1e-12:
            raise ValueError("cell surface does not realize frozen H2 SESOI")
        return self


def build_probability_scenario_from_sesoi(
    sesoi: RouteabilitySESoi,
    *,
    bypass_fixed_by_budget: Mapping[int, float],
    bypass_access_effect_by_budget: Mapping[int, float],
    routeable_fixed_effect_by_budget: Mapping[int, float],
) -> RouteabilityCellScenario:
    """Construct a 12-cell primary-success surface from external SESOI values.

    Let K/F denote bypass-control fixed access. For each budget B, the caller
    supplies:
    - baseline p(K,F,B);
    - ordinary access main effect p(K,C,B)-p(K,F,B);
    - ordinary architecture main effect p(R,F,B)-p(K,F,B).

    The routeability interaction Delta_B is then added only to the R/C cell.
    To realize both frozen SESOI values without silently assuming zero boundary
    interactions, we set Delta_2 = H1 and Delta_1 = Delta_3 = H1-H2.
    Therefore H2 = Delta_2 - 0.5*(Delta_1+Delta_3) exactly.
    """

    sesoi.validated()
    for name, mapping in (
        ("bypass_fixed_by_budget", bypass_fixed_by_budget),
        ("bypass_access_effect_by_budget", bypass_access_effect_by_budget),
        ("routeable_fixed_effect_by_budget", routeable_fixed_effect_by_budget),
    ):
        if set(mapping) != set(BUDGETS):
            raise ValueError(f"{name} must contain exactly budgets 1,2,3")

    delta = {
        2: float(sesoi.h1_probability_interaction),
        1: float(sesoi.h1_probability_interaction - sesoi.h2_probability_localization),
        3: float(sesoi.h1_probability_interaction - sesoi.h2_probability_localization),
    }

    probabilities: dict[tuple[str, str, int], float] = {}
    for budget in BUDGETS:
        kf = _unit_probability(
            bypass_fixed_by_budget[budget],
            f"bypass fixed B{budget}",
        )
        kc = kf + float(bypass_access_effect_by_budget[budget])
        rf = kf + float(routeable_fixed_effect_by_budget[budget])
        rc = rf + float(bypass_access_effect_by_budget[budget]) + delta[budget]
        for key, value in (
            (("bypass_control", "fixed", budget), kf),
            (("bypass_control", "contingent", budget), kc),
            (("routeable", "fixed", budget), rf),
            (("routeable", "contingent", budget), rc),
        ):
            probabilities[key] = _unit_probability(value, f"cell probability {key!r}")

    return RouteabilityCellScenario(
        cell_probabilities=probabilities,
        h1_delta_b2=float(sesoi.h1_probability_interaction),
        h2_localization=float(sesoi.h2_probability_localization),
        sesoi_provenance=sesoi.provenance,
    ).validated()


def scenario_rows(
    scenario: RouteabilityCellScenario,
) -> tuple[dict[str, object], ...]:
    """Return deterministic long-form rows for the 12 primary-success cells."""

    scenario.validated()
    rows = []
    for budget in BUDGETS:
        for architecture in ARCHITECTURES:
            for access in ACCESS_MODES:
                rows.append(
                    {
                        "architecture": architecture,
                        "access_mode": access,
                        "budget": budget,
                        "primary_success_probability": scenario.cell_probabilities[
                            (architecture, access, budget)
                        ],
                    }
                )
    return tuple(rows)
