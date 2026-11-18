"""Summarize the pre-frozen Dominguez-Garcia external axis replication."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


PRIMARY_MODELS = (
    "primary_full",
    "primary_plant_only",
    "primary_pollinator_only",
)
ABUNDANCE_MODELS = (
    "abundance_full",
    "abundance_plant_only",
    "abundance_pollinator_only",
)


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _log_loss(rows):
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row["model_probability"]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _null_log_loss(rows):
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row["null_probability"]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _auc(rows):
    y = [int(row["outcome"]) for row in rows]
    p = [float(row["model_probability"]) for row in rows]
    positives = sum(y)
    negatives = len(y) - positives
    if positives == 0 or negatives == 0:
        return None

    ordered = sorted(zip(p, y), key=lambda item: item[0])
    rank_sum = 0.0
    rank = 1
    i = 0
    while i < len(ordered):
        j = i + 1
        while j < len(ordered) and ordered[j][0] == ordered[i][0]:
            j += 1
        average_rank = (rank + (rank + j - i - 1)) / 2
        rank_sum += average_rank * sum(v for _, v in ordered[i:j])
        rank += j - i
        i = j
    return (
        rank_sum - positives * (positives + 1) / 2
    ) / (positives * negatives)


def _model_metrics(rows):
    ll = _log_loss(rows)
    null = _null_log_loss(rows)
    return {
        "n": len(rows),
        "events": sum(int(row["outcome"]) for row in rows),
        "log_loss": ll,
        "relative_log_loss_reduction_vs_null": (
            None if null == 0 else (null - ll) / null
        ),
        "roc_auc": _auc(rows),
    }


def _endpoint(grouped, fold_grouped, risk, models, plant_only_name, poll_only_name):
    sites = sorted(
        {
            site
            for r, site, model in grouped
            if r == risk and model == models[0]
        }
    )
    if not sites:
        raise SystemExit(f"{risk}: no held-out sites")

    pooled = {}
    fold_metrics = {}
    for model in models:
        rows = []
        per_site = {}
        for site in sites:
            site_rows = grouped[(risk, site, model)]
            if not site_rows:
                raise SystemExit(f"{risk}/{site}/{model}: no predictions")
            rows.extend(site_rows)
            per_site[site] = _model_metrics(site_rows)

        receipts = fold_grouped[(risk, model)]
        if len(receipts) != len(sites):
            raise SystemExit(
                f"{risk}/{model}: expected {len(sites)} fold receipts"
            )
        if not all(
            _bool(row["converged"])
            and int(row["coefficient_count"])
            == int(row["finite_coefficient_count"])
            for row in receipts
        ):
            raise SystemExit(f"{risk}/{model}: convergence failure")

        pooled[model] = _model_metrics(rows)
        fold_metrics[model] = per_site

    full = pooled[models[0]]
    plant_only = pooled[plant_only_name]
    poll_only = pooled[poll_only_name]

    plant_increment = poll_only["log_loss"] - full["log_loss"]
    pollinator_increment = plant_only["log_loss"] - full["log_loss"]

    site_contrasts = {}
    for site in sites:
        plant_delta = (
            fold_metrics[poll_only_name][site]["log_loss"]
            - fold_metrics[models[0]][site]["log_loss"]
        )
        poll_delta = (
            fold_metrics[plant_only_name][site]["log_loss"]
            - fold_metrics[models[0]][site]["log_loss"]
        )
        if risk == "gain":
            directional = poll_delta - plant_delta
        else:
            directional = plant_delta - poll_delta
        site_contrasts[site] = {
            "plant_increment": plant_delta,
            "pollinator_increment": poll_delta,
            "frozen_direction_contrast": directional,
        }

    if risk == "gain":
        pooled_direction = pollinator_increment - plant_increment
        definition = "pollinator_activity_increment_minus_plant_availability_increment"
    else:
        pooled_direction = plant_increment - pollinator_increment
        definition = "plant_availability_increment_minus_pollinator_activity_increment"

    return {
        "site_count": len(sites),
        "full": full,
        "plant_only": plant_only,
        "pollinator_only": poll_only,
        "plant_availability_increment": plant_increment,
        "pollinator_activity_increment": pollinator_increment,
        "frozen_direction": {
            "definition": definition,
            "pooled_difference": pooled_direction,
            "positive_site_count": sum(
                item["frozen_direction_contrast"] > 0
                for item in site_contrasts.values()
            ),
            "site_count": len(sites),
            "site_contrasts": site_contrasts,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("table_summary", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("folds", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    table_summary = json.loads(
        args.table_summary.read_text(encoding="utf-8")
    )
    predictions = _read(args.predictions)
    folds = _read(args.folds)

    grouped = defaultdict(list)
    for row in predictions:
        grouped[
            (
                row["risk_set"],
                row["held_out_site"],
                row["model"],
            )
        ].append(row)

    fold_grouped = defaultdict(list)
    for row in folds:
        fold_grouped[(row["risk_set"], row["model"])].append(row)

    primary = {
        risk: _endpoint(
            grouped,
            fold_grouped,
            risk,
            PRIMARY_MODELS,
            "primary_plant_only",
            "primary_pollinator_only",
        )
        for risk in ("gain", "loss")
    }

    abundance = {
        risk: _endpoint(
            grouped,
            fold_grouped,
            risk,
            ABUNDANCE_MODELS,
            "abundance_plant_only",
            "abundance_pollinator_only",
        )
        for risk in ("gain", "loss")
    }

    primary_matches = (
        primary["gain"]["frozen_direction"]["pooled_difference"] > 0
        and primary["loss"]["frozen_direction"]["pooled_difference"] > 0
    )

    result = {
        "schema": "adaptive-gain-dominguez2026-external-axis-replication-v1",
        "date": "2026-09-29",
        "status": (
            "external_direction_matches_both_endpoints"
            if primary_matches
            else "external_direction_mixed"
        ),
        "analysis_status": (
            "effect-blind directional replication frozen before dyad-level "
            "gain/loss effects were inspected"
        ),
        "source": {
            "article": "Dominguez-Garcia et al. 2026 Ecology Letters e70293",
            "zenodo_record": 17362189,
            "design_gate": (
                "validation/"
                "dominguez2026_external_replication_screen_gate_v1.json"
            ),
        },
        "table_audit": table_summary,
        "primary_phenology_axis": primary,
        "plant_abundance_sensitivity": abundance,
        "primary_direction_matches_both_endpoints": primary_matches,
        "ecological_read": (
            "The external test asks only whether the Villavicencio endpoint-"
            "specific predictive-information direction reappears across "
            "independent sites using a focal-response-excluded pollinator "
            "activity axis and a plant availability axis."
        ),
        "not_established": [
            "causal assembly-disassembly asymmetry",
            "sampling-effort-independent mechanism",
            "equivalence of the two datasets' measurement scales",
            "decision-equivalence classes",
            "environmental routeability",
        ],
        "claim_ceiling": (
            "External predictive-direction replication only. A matching "
            "direction would strengthen the ecological opportunity asymmetry "
            "as a cross-system pattern but would not establish causality or "
            "routeability."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
