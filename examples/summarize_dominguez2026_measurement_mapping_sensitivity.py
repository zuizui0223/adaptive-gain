"""Summarize post-result external measurement-mapping sensitivity."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


PAIRS = {
    "phenology_vs_pollinator_abundance": (
        "pheno_pollabund_full",
        "pheno_pollabund_plant_only",
        "pheno_pollabund_poll_only",
    ),
    "phenology_vs_pollinator_phenology": (
        "pheno_pollpheno_full",
        "pheno_pollpheno_plant_only",
        "pheno_pollpheno_poll_only",
    ),
    "abundance_vs_pollinator_abundance": (
        "abund_pollabund_full",
        "abund_pollabund_plant_only",
        "abund_pollabund_poll_only",
    ),
}


def _read(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(x):
    return str(x).strip().lower() in {"true", "1", "yes", "y"}


def _ll(rows):
    total = 0.0
    for row in rows:
        y = int(row["outcome"])
        p = min(max(float(row["probability"]), 1e-8), 1 - 1e-8)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(rows)


def _auc(rows):
    y = [int(row["outcome"]) for row in rows]
    p = [float(row["probability"]) for row in rows]
    pos = sum(y)
    neg = len(y) - pos
    if pos == 0 or neg == 0:
        return None
    ordered = sorted(zip(p, y), key=lambda z: z[0])
    rank_sum = 0.0
    rank = 1
    i = 0
    while i < len(ordered):
        j = i + 1
        while j < len(ordered) and ordered[j][0] == ordered[i][0]:
            j += 1
        avg = (rank + (rank + j - i - 1)) / 2
        rank_sum += avg * sum(v for _, v in ordered[i:j])
        rank += j - i
        i = j
    return (rank_sum - pos * (pos + 1) / 2) / (pos * neg)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("predictions", type=Path)
    ap.add_argument("folds", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()

    predictions = _read(args.predictions)
    folds = _read(args.folds)

    grouped = defaultdict(list)
    for row in predictions:
        grouped[
            (row["risk_set"], row["held_out_site"], row["model"])
        ].append(row)

    receipts = defaultdict(list)
    for row in folds:
        receipts[(row["risk_set"], row["model"])].append(row)

    result_pairs = {}
    for pair_name, (full_name, plant_name, poll_name) in PAIRS.items():
        pair_result = {}
        for risk in ("gain", "loss"):
            sites = sorted(
                {
                    site
                    for r, site, model in grouped
                    if r == risk and model == full_name
                }
            )
            pooled = {}
            per_site = {}
            for model in (full_name, plant_name, poll_name):
                model_rows = []
                site_metrics = {}
                for site in sites:
                    rows = grouped[(risk, site, model)]
                    model_rows.extend(rows)
                    site_metrics[site] = {
                        "log_loss": _ll(rows),
                        "auc": _auc(rows),
                    }
                state = receipts[(risk, model)]
                if len(state) != len(sites):
                    raise SystemExit(
                        f"{pair_name}/{risk}/{model}: fold count mismatch"
                    )
                if not all(
                    _bool(row["converged"])
                    and int(row["coefficient_count"])
                    == int(row["finite_coefficient_count"])
                    for row in state
                ):
                    raise SystemExit(
                        f"{pair_name}/{risk}/{model}: convergence failure"
                    )
                pooled[model] = {
                    "log_loss": _ll(model_rows),
                    "auc": _auc(model_rows),
                }
                per_site[model] = site_metrics

            full = pooled[full_name]
            plant = pooled[plant_name]
            poll = pooled[poll_name]
            plant_increment = poll["log_loss"] - full["log_loss"]
            poll_increment = plant["log_loss"] - full["log_loss"]

            site_direction = {}
            for site in sites:
                p_inc = (
                    per_site[poll_name][site]["log_loss"]
                    - per_site[full_name][site]["log_loss"]
                )
                q_inc = (
                    per_site[plant_name][site]["log_loss"]
                    - per_site[full_name][site]["log_loss"]
                )
                direction = (
                    q_inc - p_inc
                    if risk == "gain"
                    else p_inc - q_inc
                )
                site_direction[site] = direction

            pooled_direction = (
                poll_increment - plant_increment
                if risk == "gain"
                else plant_increment - poll_increment
            )

            pair_result[risk] = {
                "full_auc": full["auc"],
                "plant_increment": plant_increment,
                "pollinator_increment": poll_increment,
                "frozen_direction_contrast": pooled_direction,
                "positive_site_count": sum(
                    value > 0 for value in site_direction.values()
                ),
                "site_count": len(sites),
                "site_direction_contrasts": site_direction,
            }
        result_pairs[pair_name] = pair_result

    result = {
        "schema": (
            "adaptive-gain-dominguez2026-measurement-mapping-sensitivity-v1"
        ),
        "date": "2026-09-29",
        "status": "post_result_measurement_sensitivity_complete",
        "analysis_status": (
            "post-result diagnostic after primary external gain mismatch; "
            "cannot redefine primary replication"
        ),
        "parent_result": (
            "validation/"
            "dominguez2026_external_axis_replication_result_v1.json"
        ),
        "pairs": result_pairs,
        "interpretation": (
            "Alternative published pollinator measurements may diagnose "
            "measurement mapping, but they may share observation support with "
            "the focal link response and therefore cannot rescue the pre-frozen "
            "focal-excluded primary external gain test."
        ),
        "claim_ceiling": (
            "Measurement sensitivity only. Do not relabel the primary mixed "
            "external replication as successful regardless of these directions."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
