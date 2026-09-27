"""Build validated scenario rows for final routeability GLMM power simulation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from adaptive_gain.routeability_experiment_power import RouteabilitySESoi
from adaptive_gain.routeability_operating_characteristics import (
    build_probability_scenario_from_sesoi,
)


def _budget_map(payload, name):
    try:
        return {budget: float(payload[str(budget)]) for budget in (1, 2, 3)}
    except KeyError as exc:
        raise ValueError(f"{name} must define string keys 1, 2, 3") from exc


def _probability(value, name, *, allow_one=False):
    out = float(value)
    valid = 0.0 <= out <= 1.0 if allow_one else 0.0 <= out < 1.0
    if not valid:
        bound = "[0,1]" if allow_one else "[0,1)"
        raise ValueError(f"{name} must be in {bound}")
    return out


def _positive_int(value, name):
    out = int(value)
    if out < 1 or out != float(value):
        raise ValueError(f"{name} must be a positive integer")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    scenarios = payload.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("input JSON must contain a non-empty scenarios list")

    rows = []
    seen_ids = set()
    for item in scenarios:
        scenario_id = str(item["scenario_id"])
        if not scenario_id or scenario_id in seen_ids:
            raise ValueError("scenario_id values must be non-empty and unique")
        seen_ids.add(scenario_id)

        sesoi = RouteabilitySESoi(
            h1_probability_interaction=float(item["sesoi"]["h1_probability_interaction"]),
            h2_probability_localization=float(item["sesoi"]["h2_probability_localization"]),
            provenance=str(item["sesoi"]["provenance"]),
        ).validated()
        baseline = item["baseline"]
        surface = build_probability_scenario_from_sesoi(
            sesoi,
            bypass_fixed_by_budget=_budget_map(
                baseline["bypass_fixed_by_budget"], "bypass_fixed_by_budget"
            ),
            bypass_access_effect_by_budget=_budget_map(
                baseline["bypass_access_effect_by_budget"],
                "bypass_access_effect_by_budget",
            ),
            routeable_fixed_effect_by_budget=_budget_map(
                baseline["routeable_fixed_effect_by_budget"],
                "routeable_fixed_effect_by_budget",
            ),
        )

        sim = item["simulation"]
        individuals_per_cell = _positive_int(
            sim["individuals_per_cell"], "individuals_per_cell"
        )
        if individuals_per_cell % 4 != 0:
            raise ValueError("individuals_per_cell must be a multiple of four")
        trials_per_individual = _positive_int(
            sim["trials_per_individual"], "trials_per_individual"
        )
        colony_count = _positive_int(sim["colony_count"], "colony_count")
        simulations = _positive_int(sim["simulations"], "simulations")
        seed = int(sim["seed"])
        if seed < 0:
            raise ValueError("seed must be non-negative")

        individual_sd_logit = float(sim["individual_sd_logit"])
        colony_sd_logit = float(sim["colony_sd_logit"])
        if individual_sd_logit < 0 or colony_sd_logit < 0:
            raise ValueError("random-intercept SDs must be non-negative")
        dropout_fraction = _probability(
            sim["dropout_fraction"], "dropout_fraction"
        )
        timeout_fraction = _probability(
            sim["timeout_fraction"], "timeout_fraction"
        )
        alpha = float(sim.get("alpha_two_sided", 0.05))
        if not 0.0 < alpha < 1.0:
            raise ValueError("alpha_two_sided must be in (0,1)")

        row = {
            "scenario_id": scenario_id,
            "simulations": simulations,
            "individuals_per_cell": individuals_per_cell,
            "trials_per_individual": trials_per_individual,
            "colony_count": colony_count,
            "individual_sd_logit": individual_sd_logit,
            "colony_sd_logit": colony_sd_logit,
            "dropout_fraction": dropout_fraction,
            "timeout_fraction": timeout_fraction,
            "alpha_two_sided": alpha,
            "seed": seed,
            "sesoi_provenance": sesoi.provenance,
            "expected_h1_delta_b2": surface.h1_delta_b2,
            "expected_h2_localization": surface.h2_localization,
        }
        abbreviations = {
            "bypass_control": "K",
            "routeable": "R",
        }
        access_abbrev = {"fixed": "F", "contingent": "C"}
        for (architecture, access, budget), probability in surface.cell_probabilities.items():
            column = (
                f"p_{abbreviations[architecture]}{access_abbrev[access]}_B{budget}"
            )
            row[column] = probability
            if probability > 1.0 - timeout_fraction + 1e-12:
                raise ValueError(
                    f"{scenario_id}: {column} exceeds 1-timeout_fraction; "
                    "cannot realize the primary success probability by timeout-first simulation"
                )
        rows.append(row)

    fields = list(rows[0])
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
