"""Run a detection-sensitive Stage-1 rewiring audit on the RMBL daily matrices.

Source format
-------------
The external TemporalOriginNestedness example data contain 106 daily 46 x 93
plant-pollinator matrices plus counts mapping days into 24 weeks and three
years.  The matrices are adapted from CaraDonna (2020), EDI
10.6073/pasta/27dc02fe1655e3896f20326fed5cb95f.

This audit aggregates days to weeks, freezes within-year adjacent transitions
as primary, and treats year-boundary transitions as sensitivity analyses.

Important: weekly species presence is inferred from positive observed degree.
The output is therefore explicitly detection-sensitive and is a response
feasibility audit, not an ecological test of decision equivalence.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

from adaptive_gain.empirical_rewiring import transition_rewiring_receipt


def _read_counts(path: Path) -> list[int]:
    out: list[int] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if len(row) != 2:
                raise ValueError(f"{path} must contain index,count rows")
            count = int(row[1])
            if count <= 0:
                raise ValueError("aggregation counts must be positive")
            out.append(count)
    return out


def _read_matrix(path: Path) -> list[list[float]]:
    rows: list[list[float]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.reader(handle):
            rows.append([float(value) for value in row])
    if not rows or not rows[0]:
        raise ValueError(f"empty matrix: {path}")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError(f"ragged matrix: {path}")
    if any(value < 0 for row in rows for value in row):
        raise ValueError(f"negative interaction count: {path}")
    return rows


def _sum_matrices(matrices: list[list[list[float]]]) -> list[list[float]]:
    if not matrices:
        raise ValueError("cannot sum an empty matrix group")
    nrow = len(matrices[0])
    ncol = len(matrices[0][0])
    out = [[0.0 for _ in range(ncol)] for _ in range(nrow)]
    for matrix in matrices:
        if len(matrix) != nrow or any(len(row) != ncol for row in matrix):
            raise ValueError("daily matrices do not share one fixed shape")
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                out[i][j] += value
    return out


def _network_from_matrix(matrix: list[list[float]]) -> dict[tuple[str, str], float]:
    network: dict[tuple[str, str], float] = {}
    for i, row in enumerate(matrix, start=1):
        for j, value in enumerate(row, start=1):
            if value > 0:
                network[(f"plant_{i:03d}", f"pollinator_{j:03d}")] = value
    return network


def aggregate_daily_to_weeks(
    matrices_dir: Path,
    week_counts: list[int],
) -> list[dict[tuple[str, str], float]]:
    total_days = sum(week_counts)
    daily: list[list[list[float]]] = []
    for index in range(1, total_days + 1):
        path = matrices_dir / f"daily_adjacency_{index}.csv"
        if not path.exists():
            raise ValueError(f"missing daily matrix: {path}")
        daily.append(_read_matrix(path))

    weeks: list[dict[tuple[str, str], float]] = []
    cursor = 0
    for count in week_counts:
        matrix = _sum_matrices(daily[cursor : cursor + count])
        weeks.append(_network_from_matrix(matrix))
        cursor += count
    if cursor != len(daily):
        raise AssertionError("week aggregation did not consume all daily matrices")
    return weeks


def assign_weeks_to_years(
    week_counts: list[int],
    year_counts: list[int],
) -> list[int]:
    """Return zero-based year index for every week.

    Year boundaries must coincide exactly with week boundaries. This prevents
    silently splitting a week across years.
    """

    week_edges = []
    total = 0
    for count in week_counts:
        total += count
        week_edges.append(total)

    year_edges = []
    total = 0
    for count in year_counts:
        total += count
        year_edges.append(total)

    if not year_edges or week_edges[-1] != year_edges[-1]:
        raise ValueError("week and year metadata cover different day totals")
    if any(edge not in week_edges for edge in year_edges):
        raise ValueError("year boundary does not coincide with a week boundary")

    assignments: list[int] = []
    year_index = 0
    for edge in week_edges:
        while year_index < len(year_edges) - 1 and edge > year_edges[year_index]:
            year_index += 1
        assignments.append(year_index)
    return assignments


def _receipt_payload(receipt):
    out = asdict(receipt)
    out.update(
        {
            "shared_species_rewiring_count": receipt.shared_species_rewiring_count,
            "species_turnover_link_count": receipt.species_turnover_link_count,
            "exact_partition": receipt.exact_partition,
            "link_jaccard_dissimilarity": receipt.link_jaccard_dissimilarity,
            "shared_species_rewiring_fraction_of_union": (
                receipt.shared_species_rewiring_fraction_of_union
            ),
            "species_turnover_fraction_of_union": (
                receipt.species_turnover_fraction_of_union
            ),
        }
    )
    return out


def build_audit(
    matrices_dir: Path,
    days_in_weeks: Path,
    days_in_years: Path,
) -> dict:
    week_counts = _read_counts(days_in_weeks)
    year_counts = _read_counts(days_in_years)
    weeks = aggregate_daily_to_weeks(matrices_dir, week_counts)
    year_assignment = assign_weeks_to_years(week_counts, year_counts)

    if len(weeks) != 24 or len(year_counts) != 3:
        raise ValueError("RMBL mirror gate expects 24 weeks across three years")

    transitions = []
    for i in range(len(weeks) - 1):
        same_year = year_assignment[i] == year_assignment[i + 1]
        role = "primary" if same_year else "sensitivity"
        receipt = transition_rewiring_receipt(weeks[i], weeks[i + 1])
        transitions.append(
            {
                "previous_week": i + 1,
                "current_week": i + 2,
                "previous_year_index": year_assignment[i] + 1,
                "current_year_index": year_assignment[i + 1] + 1,
                "role": role,
                "receipt": _receipt_payload(receipt),
            }
        )

    primary = [row for row in transitions if row["role"] == "primary"]
    sensitivity = [row for row in transitions if row["role"] == "sensitivity"]

    total_primary_turnover = sum(
        row["receipt"]["total_link_turnover_count"] for row in primary
    )
    total_primary_rewiring = sum(
        row["receipt"]["shared_species_rewiring_count"] for row in primary
    )
    total_primary_species_turnover = sum(
        row["receipt"]["species_turnover_link_count"] for row in primary
    )

    return {
        "schema": "adaptive-gain-rmbl-weekly-stage1-v1",
        "source": {
            "repository": "pstaniczenko/TemporalOriginNestedness",
            "path": "ExampleData",
            "upstream": "CaraDonna 2020 EDI 10.6073/pasta/27dc02fe1655e3896f20326fed5cb95f",
            "provenance_status": "adapted_public_mirror",
        },
        "daily_matrix_count": sum(week_counts),
        "weekly_network_count": len(weeks),
        "year_count": len(year_counts),
        "primary_transition_count": len(primary),
        "sensitivity_transition_count": len(sensitivity),
        "presence_basis": "positive_observed_degree_within_week",
        "detection_sensitive": True,
        "decision_equivalence_inferred": False,
        "primary_totals": {
            "link_turnover": total_primary_turnover,
            "shared_species_rewiring": total_primary_rewiring,
            "species_turnover_link_change": total_primary_species_turnover,
            "shared_species_rewiring_share": (
                None
                if total_primary_turnover == 0
                else total_primary_rewiring / total_primary_turnover
            ),
        },
        "primary_transition_diagnostics": {
            "nonzero_shared_dyad_opportunity_count": sum(
                row["receipt"]["shared_species_dyad_count"] > 0 for row in primary
            ),
            "nonzero_rewiring_count": sum(
                row["receipt"]["shared_species_rewiring_count"] > 0 for row in primary
            ),
            "exact_partition_count": sum(
                row["receipt"]["exact_partition"] for row in primary
            ),
        },
        "transitions": transitions,
        "claim_ceiling": (
            "This audit establishes only that a repeated-network rewiring response "
            "is observable under a detection-sensitive presence proxy. It does not "
            "identify decision-equivalence classes or test environmental routeability."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("matrices_dir", type=Path)
    parser.add_argument("days_in_weeks", type=Path)
    parser.add_argument("days_in_years", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build_audit(
        args.matrices_dir,
        args.days_in_weeks,
        args.days_in_years,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output is None:
        print(rendered)
    else:
        args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
