"""Frozen robustness-grid construction for final routeability GLMM planning.

This module converts a nuisance-only pooled Pilot B receipt into the exact
robustness scenario set frozen before real pilot data. It never reads focal
architecture/access effects and never changes the H1/H2 SESOI.
"""

from __future__ import annotations

from math import isfinite
from typing import Iterable, Mapping

from .routeability_experiment_power import RouteabilitySESoi
from .routeability_operating_characteristics import (
    build_probability_scenario_from_sesoi,
)


BASELINE_PROFILE_NAMES = (
    "hard_center",
    "pilot_anchored",
    "high_performance",
)

NUISANCE_PROFILES = {
    "nominal": {
        "individual_sd_multiplier": 1.0,
        "individual_sd_floor": 0.0,
        "colony_sd_multiplier": 1.0,
        "colony_sd_floor": 0.0,
        "dropout_add": 0.0,
        "timeout_add": 0.0,
    },
    "variance_stress": {
        "individual_sd_multiplier": 1.5,
        "individual_sd_floor": 0.25,
        "colony_sd_multiplier": 1.5,
        "colony_sd_floor": 0.15,
        "dropout_add": 0.0,
        "timeout_add": 0.0,
    },
    "attrition_stress": {
        "individual_sd_multiplier": 1.0,
        "individual_sd_floor": 0.0,
        "colony_sd_multiplier": 1.0,
        "colony_sd_floor": 0.0,
        "dropout_add": 0.05,
        "timeout_add": 0.05,
    },
    "combined_stress": {
        "individual_sd_multiplier": 1.5,
        "individual_sd_floor": 0.25,
        "colony_sd_multiplier": 1.5,
        "colony_sd_floor": 0.15,
        "dropout_add": 0.05,
        "timeout_add": 0.05,
    },
}

FROZEN_SESOI = RouteabilitySESoi(
    h1_probability_interaction=0.10,
    h2_probability_localization=0.10,
    provenance="practical_decision_threshold",
).validated()


def _finite_nonnegative(value: object, name: str) -> float:
    out = float(value)
    if not isfinite(out) or out < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return out


def _probability(value: object, name: str, *, open_interval: bool = False) -> float:
    out = float(value)
    if not isfinite(out):
        raise ValueError(f"{name} must be finite")
    valid = 0.0 < out < 1.0 if open_interval else 0.0 <= out < 1.0
    if not valid:
        bounds = "(0,1)" if open_interval else "[0,1)"
        raise ValueError(f"{name} must lie in {bounds}")
    return out


def _positive_int(value: object, name: str) -> int:
    out = int(value)
    if out < 1 or float(value) != out:
        raise ValueError(f"{name} must be a positive integer")
    return out


def validate_nuisance_receipt(receipt: Mapping[str, object]) -> dict[str, float | int]:
    if receipt.get("focal_architecture_access_contrast_opened") is not False:
        raise ValueError("nuisance receipt must certify a closed focal contrast")

    required = (
        "pooled_success_fraction",
        "pooled_timeout_fraction",
        "randomized_individual_dropout_fraction",
        "trials_per_individual",
        "individual_sd_logit",
        "colony_sd_logit",
    )
    missing = [name for name in required if receipt.get(name) is None]
    if missing:
        raise ValueError(
            "nuisance receipt missing required values: " + ", ".join(missing)
        )

    return {
        "pooled_success_fraction": _probability(
            receipt["pooled_success_fraction"],
            "pooled_success_fraction",
            open_interval=True,
        ),
        "pooled_timeout_fraction": _probability(
            receipt["pooled_timeout_fraction"],
            "pooled_timeout_fraction",
        ),
        "randomized_individual_dropout_fraction": _probability(
            receipt["randomized_individual_dropout_fraction"],
            "randomized_individual_dropout_fraction",
        ),
        "trials_per_individual": _positive_int(
            receipt["trials_per_individual"],
            "trials_per_individual",
        ),
        "individual_sd_logit": _finite_nonnegative(
            receipt["individual_sd_logit"],
            "individual_sd_logit",
        ),
        "colony_sd_logit": _finite_nonnegative(
            receipt["colony_sd_logit"],
            "colony_sd_logit",
        ),
    }


def balanced_colony_block_counts(
    individuals_per_cell: int,
    colony_count: int,
) -> tuple[int, ...]:
    n = _positive_int(individuals_per_cell, "individuals_per_cell")
    colonies = _positive_int(colony_count, "colony_count")
    if n % 4 != 0:
        raise ValueError("individuals_per_cell must be a multiple of four")
    if colonies > n:
        raise ValueError(
            "colony_count cannot exceed individuals_per_cell under complete-block allocation"
        )
    quotient, remainder = divmod(n, colonies)
    counts = tuple(
        quotient + (1 if index < remainder else 0)
        for index in range(colonies)
    )
    if min(counts) < 1 or sum(counts) != n:
        raise AssertionError("balanced colony allocation invariant failed")
    if max(counts) - min(counts) > 1:
        raise AssertionError("balanced colony allocation differs by more than one block")
    return counts


def baseline_profiles(
    pooled_success_fraction: float,
) -> dict[str, dict[str, dict[int, float]]]:
    p3 = _probability(
        pooled_success_fraction,
        "pooled_success_fraction",
        open_interval=True,
    )
    return {
        "hard_center": {
            "bypass_fixed_by_budget": {1: 0.50, 2: 0.55, 3: 0.65},
            "bypass_access_effect_by_budget": {1: 0.00, 2: 0.00, 3: 0.00},
            "routeable_fixed_effect_by_budget": {1: 0.00, 2: 0.00, 3: 0.00},
        },
        "pilot_anchored": {
            "bypass_fixed_by_budget": {
                1: p3 - 0.20,
                2: p3 - 0.10,
                3: p3,
            },
            "bypass_access_effect_by_budget": {1: 0.02, 2: 0.02, 3: 0.00},
            "routeable_fixed_effect_by_budget": {1: 0.00, 2: -0.02, 3: 0.00},
        },
        "high_performance": {
            "bypass_fixed_by_budget": {1: 0.65, 2: 0.70, 3: 0.80},
            "bypass_access_effect_by_budget": {1: 0.02, 2: 0.02, 3: 0.00},
            "routeable_fixed_effect_by_budget": {1: 0.00, 2: -0.02, 3: 0.00},
        },
    }


def _stressed_nuisance(
    nuisance: Mapping[str, float | int],
    profile: Mapping[str, float],
) -> dict[str, float]:
    individual_sd = max(
        float(nuisance["individual_sd_logit"])
        * float(profile["individual_sd_multiplier"]),
        float(profile["individual_sd_floor"]),
    )
    colony_sd = max(
        float(nuisance["colony_sd_logit"])
        * float(profile["colony_sd_multiplier"]),
        float(profile["colony_sd_floor"]),
    )
    dropout = (
        float(nuisance["randomized_individual_dropout_fraction"])
        + float(profile["dropout_add"])
    )
    timeout = (
        float(nuisance["pooled_timeout_fraction"])
        + float(profile["timeout_add"])
    )
    _probability(dropout, "stressed dropout_fraction")
    _probability(timeout, "stressed timeout_fraction")
    return {
        "individual_sd_logit": individual_sd,
        "colony_sd_logit": colony_sd,
        "dropout_fraction": dropout,
        "timeout_fraction": timeout,
    }


def build_frozen_robustness_scenarios(
    nuisance_receipt: Mapping[str, object],
    *,
    candidate_individuals_per_cell: Iterable[int],
    colony_count: int,
    simulations_per_scenario: int,
    seed_base: int,
    alpha_two_sided: float = 0.05,
) -> tuple[dict[str, object], ...]:
    nuisance = validate_nuisance_receipt(nuisance_receipt)
    raw_ns = tuple(candidate_individuals_per_cell)
    if not raw_ns:
        raise ValueError("candidate_individuals_per_cell cannot be empty")
    parsed_ns = tuple(
        _positive_int(value, "candidate individuals_per_cell")
        for value in raw_ns
    )
    ns = tuple(sorted(set(parsed_ns)))
    for n in ns:
        if n % 4 != 0:
            raise ValueError("every candidate individuals_per_cell must be a multiple of four")

    colonies = _positive_int(colony_count, "colony_count")
    minimum_feasible_n = 4 * ((colonies + 3) // 4)
    expected_ns = tuple(
        range(minimum_feasible_n, ns[-1] + 4, 4)
    )
    if ns != expected_ns:
        raise ValueError(
            "candidate individuals_per_cell must contain every multiple of four "
            f"from the smallest colony-feasible value {minimum_feasible_n} "
            f"through {ns[-1]}; observed {ns!r}"
        )
    simulations = _positive_int(simulations_per_scenario, "simulations_per_scenario")
    seed0 = int(seed_base)
    if seed0 < 0:
        raise ValueError("seed_base must be non-negative")
    alpha = float(alpha_two_sided)
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha_two_sided must be in (0,1)")

    baselines = baseline_profiles(float(nuisance["pooled_success_fraction"]))
    if tuple(baselines) != BASELINE_PROFILE_NAMES:
        raise AssertionError("baseline profile order changed")

    robustness_pairs = tuple(
        (baseline_name, nuisance_name)
        for baseline_name in BASELINE_PROFILE_NAMES
        for nuisance_name in NUISANCE_PROFILES
    )

    scenarios: list[dict[str, object]] = []
    for n_index, n in enumerate(ns):
        colony_counts = balanced_colony_block_counts(n, colonies)
        for robustness_index, (baseline_name, nuisance_name) in enumerate(
            robustness_pairs
        ):
            baseline = baselines[baseline_name]
            stressed = _stressed_nuisance(
                nuisance,
                NUISANCE_PROFILES[nuisance_name],
            )
            surface = build_probability_scenario_from_sesoi(
                FROZEN_SESOI,
                bypass_fixed_by_budget=baseline["bypass_fixed_by_budget"],
                bypass_access_effect_by_budget=baseline[
                    "bypass_access_effect_by_budget"
                ],
                routeable_fixed_effect_by_budget=baseline[
                    "routeable_fixed_effect_by_budget"
                ],
            )
            max_allowed = 1.0 - stressed["timeout_fraction"]
            violating = {
                key: probability
                for key, probability in surface.cell_probabilities.items()
                if probability > max_allowed + 1e-12
            }
            if violating:
                raise ValueError(
                    f"{baseline_name}/{nuisance_name}: target primary-success "
                    f"probability exceeds 1-timeout_fraction={max_allowed:.6g}: "
                    f"{violating!r}; fail closed rather than clipping"
                )

            robustness_id = f"{baseline_name}__{nuisance_name}"
            scenarios.append(
                {
                    "scenario_id": f"N{n}__{robustness_id}",
                    "robustness_id": robustness_id,
                    "sesoi": {
                        "h1_probability_interaction": 0.10,
                        "h2_probability_localization": 0.10,
                        "provenance": "practical_decision_threshold",
                    },
                    "baseline": {
                        name: {
                            str(budget): float(value)
                            for budget, value in mapping.items()
                        }
                        for name, mapping in baseline.items()
                    },
                    "simulation": {
                        "simulations": simulations,
                        "individuals_per_cell": n,
                        "trials_per_individual": int(
                            nuisance["trials_per_individual"]
                        ),
                        "colony_count": colonies,
                        "colony_block_counts": list(colony_counts),
                        **stressed,
                        "alpha_two_sided": alpha,
                        "seed": (
                            seed0
                            + n_index * 1000
                            + robustness_index
                        ),
                    },
                }
            )

    expected_per_n = len(robustness_pairs)
    expected_ids = {
        f"{baseline}__{nuisance_name}"
        for baseline, nuisance_name in robustness_pairs
    }
    for n in ns:
        rows = [
            row for row in scenarios
            if row["simulation"]["individuals_per_cell"] == n
        ]
        if len(rows) != expected_per_n:
            raise AssertionError("robustness scenario count differs across candidate N")
        if {row["robustness_id"] for row in rows} != expected_ids:
            raise AssertionError("robustness_id set differs across candidate N")

    return tuple(scenarios)
