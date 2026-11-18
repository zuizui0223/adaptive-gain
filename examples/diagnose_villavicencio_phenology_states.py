"""Describe how fixed phenological overlap stratifies annual dyad states.

This is a post-result ecological diagnostic. It asks whether phenological
overlap behaves as an eligibility/persistence filter rather than a directional
predictor of whether a changing dyad will be a gain or a loss.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

SCOPES = {
    "strict_core_2008_2011": ("2008->2009", "2009->2010", "2010->2011"),
    "near_core_2007_2011": (
        "2007->2008",
        "2008->2009",
        "2009->2010",
        "2010->2011",
    ),
    "all_annual_2006_2011": (
        "2006->2007",
        "2007->2008",
        "2008->2009",
        "2009->2010",
        "2010->2011",
    ),
}


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _auc(y, score):
    positives = sum(y)
    negatives = len(y) - positives
    if positives == 0 or negatives == 0:
        return None
    ordered = sorted(zip(score, y), key=lambda item: item[0])
    rank_sum = 0.0
    index = 0
    rank = 1
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = (rank + (rank + end - index - 1)) / 2
        rank_sum += average_rank * sum(outcome for _, outcome in ordered[index:end])
        rank += end - index
        index = end
    return (rank_sum - positives * (positives + 1) / 2) / (
        positives * negatives
    )


def _median(values):
    values = sorted(values)
    n = len(values)
    if n == 0:
        return None
    mid = n // 2
    if n % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2


def _summary(values):
    if not values:
        return {"n": 0, "mean": None, "median": None}
    return {
        "n": len(values),
        "mean": sum(values) / len(values),
        "median": _median(values),
    }


def _state(row):
    prev = _bool(row["previous_link"])
    curr = _bool(row["current_link"])
    if not prev and not curr:
        return "stable_absent"
    if not prev and curr:
        return "gain"
    if prev and not curr:
        return "loss"
    return "retained"


def _contrast(rows, positive_state, negative_state, *, positive_overlap_only=False):
    selected = [
        row
        for row in rows
        if row["state"] in {positive_state, negative_state}
        and (
            not positive_overlap_only
            or row["phenological_overlap"] > 0
        )
    ]
    y = [int(row["state"] == positive_state) for row in selected]
    score = [row["phenological_overlap"] for row in selected]
    return {
        "n": len(selected),
        "positive_n": sum(y),
        "auc_high_overlap_predicts_positive": _auc(y, score),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dyads", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    raw = _read(args.dyads)
    rows = []
    for row in raw:
        if not _bool(row["complete_case"]):
            continue
        rows.append(
            {
                "transition": row["transition"],
                "state": _state(row),
                "phenological_overlap": float(row["phenological_overlap"]),
            }
        )

    scopes = {}
    for scope, transitions in SCOPES.items():
        scope_rows = [
            row for row in rows if row["transition"] in transitions
        ]
        folds = []
        for transition in transitions:
            fold = [
                row for row in scope_rows
                if row["transition"] == transition
            ]
            states = defaultdict(list)
            for row in fold:
                states[row["state"]].append(row["phenological_overlap"])

            folds.append(
                {
                    "transition": transition,
                    "states": {
                        state: _summary(states[state])
                        for state in (
                            "stable_absent",
                            "gain",
                            "loss",
                            "retained",
                        )
                    },
                    "gain_vs_stable_absent": _contrast(
                        fold, "gain", "stable_absent"
                    ),
                    "retained_vs_loss": _contrast(
                        fold, "retained", "loss"
                    ),
                    "gain_vs_loss_among_changed": _contrast(
                        fold, "gain", "loss"
                    ),
                    "positive_overlap_only": {
                        "gain_vs_stable_absent": _contrast(
                            fold,
                            "gain",
                            "stable_absent",
                            positive_overlap_only=True,
                        ),
                        "retained_vs_loss": _contrast(
                            fold,
                            "retained",
                            "loss",
                            positive_overlap_only=True,
                        ),
                    },
                    "zero_overlap_fraction": {
                        state: (
                            None
                            if not states[state]
                            else sum(value == 0 for value in states[state])
                            / len(states[state])
                        )
                        for state in (
                            "stable_absent",
                            "gain",
                            "loss",
                            "retained",
                        )
                    },
                }
            )

        state_values = defaultdict(list)
        for row in scope_rows:
            state_values[row["state"]].append(row["phenological_overlap"])
        pooled = {
            "states": {
                state: _summary(state_values[state])
                for state in (
                    "stable_absent",
                    "gain",
                    "loss",
                    "retained",
                )
            },
            "gain_vs_stable_absent": _contrast(
                scope_rows, "gain", "stable_absent"
            ),
            "retained_vs_loss": _contrast(
                scope_rows, "retained", "loss"
            ),
            "gain_vs_loss_among_changed": _contrast(
                scope_rows, "gain", "loss"
            ),
            "positive_overlap_only": {
                "gain_vs_stable_absent": _contrast(
                    scope_rows,
                    "gain",
                    "stable_absent",
                    positive_overlap_only=True,
                ),
                "retained_vs_loss": _contrast(
                    scope_rows,
                    "retained",
                    "loss",
                    positive_overlap_only=True,
                ),
            },
            "zero_overlap_fraction": {
                state: (
                    None
                    if not state_values[state]
                    else sum(value == 0 for value in state_values[state])
                    / len(state_values[state])
                )
                for state in (
                    "stable_absent",
                    "gain",
                    "loss",
                    "retained",
                )
            },
        }
        scopes[scope] = {"folds": folds, "pooled": pooled}

    primary = scopes["strict_core_2008_2011"]
    result = {
        "schema": "adaptive-gain-villavicencio-phenology-state-stratification-v1",
        "date": "2026-09-28",
        "status": "post_result_ecological_diagnostic",
        "prospective_status": "post_hoc_not_confirmatory",
        "exposure": (
            "single dyad-level phenological-overlap matrix reused across "
            "annual transitions"
        ),
        "scopes": scopes,
        "primary_summary": {
            "pooled_gain_vs_stable_absent_auc": (
                primary["pooled"]["gain_vs_stable_absent"][
                    "auc_high_overlap_predicts_positive"
                ]
            ),
            "pooled_retained_vs_loss_auc": (
                primary["pooled"]["retained_vs_loss"][
                    "auc_high_overlap_predicts_positive"
                ]
            ),
            "pooled_gain_vs_loss_auc": (
                primary["pooled"]["gain_vs_loss_among_changed"][
                    "auc_high_overlap_predicts_positive"
                ]
            ),
            "state_medians": {
                state: primary["pooled"]["states"][state]["median"]
                for state in (
                    "stable_absent",
                    "gain",
                    "loss",
                    "retained",
                )
            },
            "zero_overlap_fraction": primary["pooled"]["zero_overlap_fraction"],
            "positive_overlap_only_gain_vs_stable_absent_auc": (
                primary["pooled"]["positive_overlap_only"][
                    "gain_vs_stable_absent"
                ]["auc_high_overlap_predicts_positive"]
            ),
            "positive_overlap_only_retained_vs_loss_auc": (
                primary["pooled"]["positive_overlap_only"][
                    "retained_vs_loss"
                ]["auc_high_overlap_predicts_positive"]
            ),
        },
        "interpretation": {
            "supported": (
                "Phenological overlap strongly separates candidate gains from "
                "stable absences primarily through a zero-versus-positive overlap "
                "gate, while overlap magnitude retains moderate information about "
                "persistence among established positive-overlap links and carries "
                "almost no directional information distinguishing gain from loss "
                "among changed dyads."
            ),
            "ecological_read": (
                "In this annual fallback, phenology behaves first like a near-binary "
                "interaction-eligibility filter and secondarily like a persistence "
                "gradient, not like a directional switch for rewiring."
            ),
            "not_supported": (
                "Year-to-year phenological shifts caused rewiring, or phenology "
                "determines the direction of a link change."
            ),
        },
        "claim_firewall": [
            "the phenological-overlap exposure is not year-specific in this annual fallback",
            "the diagnostic is descriptive and post hoc",
            "gain/loss state contrasts are not routeability or decision-equivalence tests",
            "repeated dyads across transitions are not independent biological replicates",
            "zero overlap is not a deterministic impossibility because some observed gains have zero in the study-wide overlap matrix",
            "do not promote the state pattern as a universal threshold without independent replication",
        ],
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
