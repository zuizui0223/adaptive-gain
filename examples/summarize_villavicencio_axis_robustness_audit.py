"""Summarize endpoint opportunity-axis robustness across measurement contexts."""

from __future__ import annotations
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

CONTEXTS = ("weekly_k1", "weekly_k2", "weekly_k3", "siteweek_k1")
TRANSITIONS = ("2008->2009", "2009->2010", "2010->2011")


def _read(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _mean(values):
    return sum(values) / len(values) if values else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("rows", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows = _read(args.rows)
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["context"], row["risk_set"])].append(row)

    contexts = {}
    all_green = True
    for context in CONTEXTS:
        endpoints = {}
        for risk in ("gain", "loss"):
            subset = grouped[(context, risk)]
            transitions = {row["held_out_transition"] for row in subset}
            if transitions != set(TRANSITIONS):
                raise SystemExit(
                    f"{context}/{risk}: transition surface changed"
                )
            passes = [_bool(row["expected_direction_pass"]) for row in subset]
            endpoint = {
                "fold_count": len(subset),
                "expected_direction_positive_folds": sum(passes),
                "all_folds_expected_direction": all(passes),
                "mean_plant_increment": _mean(
                    [float(row["plant_increment"]) for row in subset]
                ),
                "mean_pollinator_increment": _mean(
                    [float(row["pollinator_increment"]) for row in subset]
                ),
                "mean_expected_direction_difference": _mean(
                    [
                        float(row["expected_direction_difference"])
                        for row in subset
                    ]
                ),
                "folds": {
                    row["held_out_transition"]: {
                        "plant_increment": float(row["plant_increment"]),
                        "pollinator_increment": float(
                            row["pollinator_increment"]
                        ),
                        "expected_direction_difference": float(
                            row["expected_direction_difference"]
                        ),
                    }
                    for row in subset
                },
            }
            endpoints[risk] = endpoint
            all_green = all_green and endpoint["all_folds_expected_direction"]
        contexts[context] = endpoints

    result = {
        "schema": "adaptive-gain-villavicencio-axis-robustness-audit-v1",
        "date": "2026-09-29",
        "status": (
            "retrospective_axis_reversal_robust"
            if all_green
            else "retrospective_axis_reversal_mixed"
        ),
        "analysis_status": (
            "post-result endpoint-axis robustness across spatial and "
            "link-frequency definitions; hypothesis-generating only"
        ),
        "scope": "strict_core_2008_2011",
        "contexts": contexts,
        "ecological_read": (
            "If green, pollinator activity carries more held-out information "
            "than plant availability for link gains, while plant availability "
            "carries more than pollinator activity for link losses, in every "
            "primary fold under week-level, same-site same-week, >=2-visit, "
            "and >=3-visit definitions."
        ),
        "claim_ceiling": (
            "This is robustness of a predictive-information asymmetry, not "
            "evidence for distinct causal assembly/disassembly mechanisms, "
            "sampling-effort independence, behavioral causation, decision "
            "equivalence, or routeability."
        ),
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
