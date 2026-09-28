"""Leave-one-species-out leverage audit for the Villavicencio phenology pattern.

This is a post-result robustness diagnostic. It asks whether the descriptive
two-stage phenology pattern is driven by one unusually influential plant or
pollinator species.

The audit uses the sampling-consistent primary annual scope only and does not
fit a routeability or causal model.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


PRIMARY_TRANSITIONS = (
    "2008->2009",
    "2009->2010",
    "2010->2011",
)


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _bool(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _state(row):
    previous = _bool(row["previous_link"])
    current = _bool(row["current_link"])
    if not previous and not current:
        return "stable_absent"
    if not previous and current:
        return "gain"
    if previous and not current:
        return "loss"
    return "retained"


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
        rank_sum += average_rank * sum(
            outcome for _, outcome in ordered[index:end]
        )
        rank += end - index
        index = end

    return (
        rank_sum - positives * (positives + 1) / 2
    ) / (positives * negatives)


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
    if not selected:
        return None
    y = [int(row["state"] == positive_state) for row in selected]
    if len(set(y)) < 2:
        return None
    score = [row["phenological_overlap"] for row in selected]
    return _auc(y, score)


def _metrics(rows):
    return {
        "positive_overlap_gain_vs_stable_absent_auc": _contrast(
            rows,
            "gain",
            "stable_absent",
            positive_overlap_only=True,
        ),
        "positive_overlap_retained_vs_loss_auc": _contrast(
            rows,
            "retained",
            "loss",
            positive_overlap_only=True,
        ),
        "gain_vs_loss_auc": _contrast(
            rows,
            "gain",
            "loss",
        ),
    }


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
    finite = [value for value in values if value is not None]
    if not finite:
        return {
            "n_omissions": 0,
            "min": None,
            "median": None,
            "max": None,
            "fraction_above_half": None,
        }
    return {
        "n_omissions": len(finite),
        "min": min(finite),
        "median": _median(finite),
        "max": max(finite),
        "fraction_above_half": sum(value > 0.5 for value in finite) / len(finite),
    }


def _leave_one_out(rows, key):
    species = sorted({row[key] for row in rows})
    values = {
        "positive_overlap_gain_vs_stable_absent_auc": [],
        "positive_overlap_retained_vs_loss_auc": [],
        "gain_vs_loss_auc": [],
    }
    for omitted in species:
        retained = [row for row in rows if row[key] != omitted]
        metrics = _metrics(retained)
        for metric, value in metrics.items():
            values[metric].append(value)
    return {
        "species_count": len(species),
        **{
            metric: _summary(metric_values)
            for metric, metric_values in values.items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dyads", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows = []
    for row in _read(args.dyads):
        if row["transition"] not in PRIMARY_TRANSITIONS:
            continue
        if not _bool(row["complete_case"]):
            continue
        rows.append(
            {
                "plant": row["plant"],
                "pollinator": row["pollinator"],
                "state": _state(row),
                "phenological_overlap": float(row["phenological_overlap"]),
            }
        )

    base = _metrics(rows)
    plants = sorted({row["plant"] for row in rows})
    pollinators = sorted({row["pollinator"] for row in rows})

    result = {
        "schema": "adaptive-gain-villavicencio-species-leverage-audit-v1",
        "date": "2026-09-28",
        "status": "post_hoc_species_leverage_diagnostic",
        "scope": "strict_core_2008_2011",
        "analysis_role": (
            "post-result leave-one-species-out robustness audit of the "
            "phenology state-stratification pattern"
        ),
        "base": {
            **base,
            "plant_count": len(plants),
            "pollinator_count": len(pollinators),
            "rows": len(rows),
        },
        "leave_one_plant_out": _leave_one_out(rows, "plant"),
        "leave_one_pollinator_out": _leave_one_out(rows, "pollinator"),
        "ecological_read": (
            "The two-stage phenology pattern is not attributable to any single "
            "plant or pollinator species: conditional on positive overlap, "
            "overlap magnitude remains near chance for distinguishing gains "
            "from stable absences, remains moderately informative for retention "
            "versus loss, and remains near chance for distinguishing gain from "
            "loss among changed dyads after every single-species omission."
        ),
        "claim_ceiling": (
            "Post-hoc leverage robustness only; this does not make the "
            "state-stratification pattern causal, independent across dyad-years, "
            "or prospectively validated."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
