"""Deterministic final-N selection from a frozen GLMM operating-characteristic surface.

The selector chooses the smallest balanced individuals-per-cell value that
passes the prespecified operating-characteristic thresholds in *every*
robustness scenario evaluated at that N. It does not optimize thresholds after
seeing the surface.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class FinalNRule:
    minimum_fit_success_fraction: float
    minimum_h1_directional_rejection_fraction: float
    minimum_h2_hierarchical_pass_fraction: float
    minimum_scenarios_per_n: int = 2
    minimum_simulations_per_scenario: int = 1000
    counterbalance_multiple: int = 4

    def validated(self) -> "FinalNRule":
        for name, value in (
            ("minimum_fit_success_fraction", self.minimum_fit_success_fraction),
            (
                "minimum_h1_directional_rejection_fraction",
                self.minimum_h1_directional_rejection_fraction,
            ),
            (
                "minimum_h2_hierarchical_pass_fraction",
                self.minimum_h2_hierarchical_pass_fraction,
            ),
        ):
            value = float(value)
            if not 0.0 < value <= 1.0:
                raise ValueError(f"{name} must be in (0,1]")
        if type(self.minimum_scenarios_per_n) is not int or self.minimum_scenarios_per_n < 2:
            raise ValueError("minimum_scenarios_per_n must be an integer >= 2")
        if (
            type(self.minimum_simulations_per_scenario) is not int
            or self.minimum_simulations_per_scenario < 1
        ):
            raise ValueError(
                "minimum_simulations_per_scenario must be a positive integer"
            )
        if type(self.counterbalance_multiple) is not int or self.counterbalance_multiple < 1:
            raise ValueError("counterbalance_multiple must be a positive integer")
        return self


@dataclass(frozen=True)
class CandidateNReceipt:
    individuals_per_cell: int
    scenario_count: int
    robustness_ids: tuple[str, ...]
    worst_fit_success_fraction: float
    worst_h1_directional_rejection_fraction: float
    worst_h2_hierarchical_pass_fraction: float
    passes: bool


@dataclass(frozen=True)
class FinalNSelectionReceipt:
    selected_individuals_per_cell: int
    total_randomized_individuals: int
    evaluated_n_values: tuple[int, ...]
    candidate_receipts: tuple[CandidateNReceipt, ...]
    rule: FinalNRule
    selection_rule: str


ROBUSTNESS_MATCH_FLOAT_COLUMNS = (
    "individual_sd_logit",
    "colony_sd_logit",
    "dropout_fraction",
    "timeout_fraction",
    "alpha_two_sided",
    "p_KF_B1", "p_KC_B1", "p_RF_B1", "p_RC_B1",
    "p_KF_B2", "p_KC_B2", "p_RF_B2", "p_RC_B2",
    "p_KF_B3", "p_KC_B3", "p_RF_B3", "p_RC_B3",
    "expected_h1_delta_b2",
    "expected_h2_localization",
)

REQUIRED_COLUMNS = {
    "scenario_id",
    "robustness_id",
    "individuals_per_cell",
    "simulations",
    "trials_per_individual",
    "colony_count",
    *ROBUSTNESS_MATCH_FLOAT_COLUMNS,
    "fit_success_fraction",
    "h1_directional_rejection_fraction",
    "h2_hierarchical_pass_fraction",
    "sesoi_provenance",
}


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("operating-characteristic surface is empty")
    fields = set(rows[0])
    missing = REQUIRED_COLUMNS - fields
    if missing:
        raise ValueError(
            "operating-characteristic surface missing columns: "
            + ", ".join(sorted(missing))
        )
    ids = [row["scenario_id"].strip() for row in rows]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("scenario_id values must be non-empty and unique")
    return rows


def select_final_individuals_per_cell(
    power_surface_csv: Path,
    rule: FinalNRule,
) -> FinalNSelectionReceipt:
    """Select the smallest N passing all prespecified robustness scenarios."""

    rule.validated()
    rows = _read_rows(power_surface_csv)

    h1_values = {float(row["expected_h1_delta_b2"]) for row in rows}
    h2_values = {float(row["expected_h2_localization"]) for row in rows}
    provenance_values = {row["sesoi_provenance"].strip() for row in rows}
    trial_values = {int(row["trials_per_individual"]) for row in rows}
    simulation_values = {int(row["simulations"]) for row in rows}

    if len(h1_values) != 1 or len(h2_values) != 1:
        raise ValueError(
            "operating-characteristic surface mixes H1/H2 SESOI values; final-N selection requires one frozen effect target across the full robustness surface"
        )
    if len(provenance_values) != 1 or "" in provenance_values:
        raise ValueError(
            "operating-characteristic surface mixes or omits SESOI provenance"
        )
    if len(trial_values) != 1 or next(iter(trial_values)) < 1:
        raise ValueError(
            "operating-characteristic surface must use one frozen positive trials_per_individual value across all scenarios"
        )
    if len(simulation_values) != 1:
        raise ValueError(
            "operating-characteristic surface must use one frozen simulation count across all scenarios and candidate N values"
        )
    simulations = next(iter(simulation_values))
    if simulations < rule.minimum_simulations_per_scenario:
        raise ValueError(
            f"operating-characteristic surface uses only {simulations} simulations per scenario; "
            f"frozen minimum is {rule.minimum_simulations_per_scenario}"
        )

    grouped: dict[int, list[dict[str, str]]] = {}
    for row in rows:
        n = int(row["individuals_per_cell"])
        if n < 1:
            raise ValueError("individuals_per_cell must be positive")
        if n % rule.counterbalance_multiple != 0:
            raise ValueError(
                f"individuals_per_cell={n} is not a multiple of "
                f"{rule.counterbalance_multiple}"
            )
        grouped.setdefault(n, []).append(row)

    robustness_signatures: dict[str, tuple[object, ...]] = {}
    for row in rows:
        robustness_id = row["robustness_id"].strip()
        signature = (
            int(row["trials_per_individual"]),
            int(row["colony_count"]),
            row["sesoi_provenance"].strip(),
            *(
                float(row[column])
                for column in ROBUSTNESS_MATCH_FLOAT_COLUMNS
            ),
        )
        previous = robustness_signatures.setdefault(
            robustness_id,
            signature,
        )
        if previous != signature:
            raise ValueError(
                f"robustness_id={robustness_id!r} changes nuisance, baseline, "
                "trial, colony, SESOI or alpha assumptions across candidate N"
            )

    robustness_sets: dict[int, set[str]] = {}
    for n, group in grouped.items():
        ids = [row["robustness_id"].strip() for row in group]
        if any(not value for value in ids):
            raise ValueError("robustness_id values must be non-empty")
        if len(ids) != len(set(ids)):
            raise ValueError(
                f"N={n} contains duplicate robustness_id values"
            )
        robustness_sets[n] = set(ids)

    reference_n = min(robustness_sets)
    reference_robustness = robustness_sets[reference_n]
    for n, values in robustness_sets.items():
        if values != reference_robustness:
            raise ValueError(
                "every candidate N must be evaluated on the exact same "
                "robustness_id set"
            )

    receipts = []
    for n in sorted(grouped):
        group = grouped[n]
        if len(group) < rule.minimum_scenarios_per_n:
            raise ValueError(
                f"N={n} has only {len(group)} robustness scenarios; "
                f"minimum is {rule.minimum_scenarios_per_n}"
            )

        fit = [float(row["fit_success_fraction"]) for row in group]
        h1 = [float(row["h1_directional_rejection_fraction"]) for row in group]
        h2 = [float(row["h2_hierarchical_pass_fraction"]) for row in group]
        for name, values in (("fit_success_fraction", fit), ("H1", h1), ("H2", h2)):
            if any(value < 0 or value > 1 for value in values):
                raise ValueError(f"{name} values must lie in [0,1]")

        worst_fit = min(fit)
        worst_h1 = min(h1)
        worst_h2 = min(h2)
        passes = (
            worst_fit >= rule.minimum_fit_success_fraction
            and worst_h1 >= rule.minimum_h1_directional_rejection_fraction
            and worst_h2 >= rule.minimum_h2_hierarchical_pass_fraction
        )
        receipts.append(
            CandidateNReceipt(
                individuals_per_cell=n,
                scenario_count=len(group),
                robustness_ids=tuple(sorted(robustness_sets[n])),
                worst_fit_success_fraction=worst_fit,
                worst_h1_directional_rejection_fraction=worst_h1,
                worst_h2_hierarchical_pass_fraction=worst_h2,
                passes=passes,
            )
        )

    passing = [row.individuals_per_cell for row in receipts if row.passes]
    if not passing:
        raise ValueError(
            "no evaluated individuals-per-cell value passes the frozen "
            "operating-characteristic rule across every robustness scenario"
        )

    selected = min(passing)
    return FinalNSelectionReceipt(
        selected_individuals_per_cell=selected,
        total_randomized_individuals=12 * selected,
        evaluated_n_values=tuple(sorted(grouped)),
        candidate_receipts=tuple(receipts),
        rule=rule,
        selection_rule=(
            "smallest individuals_per_cell that meets all frozen fit-success, "
            "H1 and hierarchical-H2 thresholds in every robustness scenario"
        ),
    )


def receipt_as_dict(receipt: FinalNSelectionReceipt) -> dict[str, object]:
    return {
        "schema": "adaptive-gain-routeability-final-n-selection-v1",
        "selected_individuals_per_cell": receipt.selected_individuals_per_cell,
        "total_randomized_individuals": receipt.total_randomized_individuals,
        "evaluated_n_values": list(receipt.evaluated_n_values),
        "candidate_receipts": [
            asdict(row) for row in receipt.candidate_receipts
        ],
        "rule": asdict(receipt.rule),
        "selection_rule": receipt.selection_rule,
    }
