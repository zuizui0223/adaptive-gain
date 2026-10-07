"""Reconstruct coarse individual first-probe intervals from Uehara 2026 Source Data.

The Supplementary Data Figure 2D/S2 sheet stores one row per included
individual and nine one-minute Probe percentages: -1–0 min followed by 0–1
through 7–8 min after host-cue onset.

Primary analysis restricts to individuals with zero probing in the pre-stimulus
(-1–0 min) bin.  For those animals, the first post-stimulus minute bin with
Probe% > 0 is an interval-censored first-probe onset.  Animals with no positive
Probe% in 0–8 min are right-censored at 8 min.

This is coarser than the frame-level 60-fps behavior files used by the original
analysis pipeline.  It must not be described as frame-resolved latency.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


SPECIES = (
    "Aedes aegypti",
    "Aedes albopictus",
    "Anopheles gambiae",
    "Anopheles stephensi",
    "Culex tarsalis",
    "Culex quinquefasciatus",
)

PRE_PROBE_COLUMN = 11
POST_PROBE_COLUMNS = tuple(range(12, 20))


@dataclass(frozen=True)
class IndividualProbeInterval:
    species: str
    source_row: int
    pre_probe_percent: float
    first_probe_interval_start_min: int | None
    first_probe_interval_end_min: int | None
    status: str


def _float_cell(row: Sequence[str], column: int) -> float | None:
    if column >= len(row):
        return None
    value = str(row[column]).strip()
    if not value:
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def _species_header_rows(rows: Sequence[Sequence[str]]) -> list[tuple[int, str]]:
    out = []
    for index, row in enumerate(rows):
        value = str(row[2]).strip() if len(row) > 2 else ""
        if value in SPECIES:
            out.append((index, value))
    if tuple(species for _, species in out) != SPECIES:
        raise ValueError(
            "Could not identify the six canonical species blocks in Figure 2D/S2"
        )
    return out


def parse_fig2d_individuals(
    rows: Sequence[Sequence[str]],
) -> dict[str, list[tuple[int, tuple[float, ...]]]]:
    """Return source-row and nine Probe-bin percentages for each species."""
    headers = _species_header_rows(rows)
    result: dict[str, list[tuple[int, tuple[float, ...]]]] = {}

    for position, (start, species) in enumerate(headers):
        end = headers[position + 1][0] if position + 1 < len(headers) else len(rows)
        individuals: list[tuple[int, tuple[float, ...]]] = []
        for row_index in range(start + 3, end):
            row = rows[row_index]
            values = tuple(
                _float_cell(row, column)
                for column in (PRE_PROBE_COLUMN,) + POST_PROBE_COLUMNS
            )
            if any(value is None for value in values):
                continue
            individuals.append(
                (
                    row_index + 1,
                    tuple(float(value) for value in values if value is not None),
                )
            )
        if not individuals:
            raise ValueError(f"No individual Probe rows found for {species}")
        result[species] = individuals
    return result


def parse_inactive_counts(rows: Sequence[Sequence[str]]) -> dict[str, int]:
    """Read timepoint-0 inactive-before-cue counts from Excl_Spp_Cond."""
    counts: dict[str, int] = {}
    for row in rows:
        if len(row) < 5:
            continue
        species = str(row[1]).strip()
        timepoint = str(row[2]).strip()
        if species not in SPECIES or timepoint not in {"0", "0.0"}:
            continue
        try:
            counts[species] = int(float(str(row[4]).strip()))
        except ValueError as exc:
            raise ValueError(f"Invalid inactive count for {species}") from exc
    if tuple(counts) != SPECIES:
        raise ValueError("Could not recover canonical timepoint-0 inactive counts")
    return counts


def interval_from_probe_bins(
    species: str,
    source_row: int,
    probe_bins: Sequence[float],
) -> IndividualProbeInterval:
    if len(probe_bins) != 9:
        raise ValueError("Expected nine Probe bins: pre plus eight post-stimulus bins")
    pre = float(probe_bins[0])
    if pre != 0.0:
        return IndividualProbeInterval(
            species,
            source_row,
            pre,
            None,
            None,
            "excluded_pre_probe_positive",
        )

    post = tuple(float(x) for x in probe_bins[1:])
    for index, value in enumerate(post):
        if value > 0.0:
            return IndividualProbeInterval(
                species,
                source_row,
                pre,
                index,
                index + 1,
                "interval_censored_first_probe",
            )
    return IndividualProbeInterval(
        species,
        source_row,
        pre,
        None,
        None,
        "right_censored_at_8min",
    )


def summarize_species(
    intervals: Sequence[IndividualProbeInterval],
) -> dict[str, object]:
    primary = [
        row
        for row in intervals
        if row.status != "excluded_pre_probe_positive"
    ]
    if not primary:
        raise ValueError("Primary pre-probe-zero cohort is empty")

    n = len(primary)
    cdf = {}
    interval_counts = {}
    for minute in range(1, 9):
        event_count = sum(
            row.first_probe_interval_end_min is not None
            and row.first_probe_interval_end_min <= minute
            for row in primary
        )
        cdf[str(minute)] = event_count / n
        interval_counts[f"{minute-1}-{minute}"] = sum(
            row.first_probe_interval_start_min == minute - 1
            for row in primary
        )

    event_n = sum(
        row.status == "interval_censored_first_probe"
        for row in primary
    )
    median_end = next(
        (minute for minute in range(1, 9) if cdf[str(minute)] >= 0.5),
        None,
    )

    return {
        "n_all_source_individuals": len(intervals),
        "n_primary_pre_probe_zero": n,
        "n_excluded_pre_probe_positive": len(intervals) - n,
        "n_probe_by_8min": event_n,
        "n_right_censored_at_8min": n - event_n,
        "probe_by_1min_probability": cdf["1"],
        "probe_by_8min_probability": cdf["8"],
        "discrete_cdf_by_minute_end": cdf,
        "first_probe_interval_counts": interval_counts,
        "median_interval_end_min": median_end,
    }


def analyze(
    fig2d_csv: Path,
    exclusion_csv: Path,
) -> tuple[dict[str, object], list[IndividualProbeInterval]]:
    with fig2d_csv.open(newline="", encoding="utf-8-sig") as handle:
        fig_rows = list(csv.reader(handle))
    with exclusion_csv.open(newline="", encoding="utf-8-sig") as handle:
        exclusion_rows = list(csv.reader(handle))

    parsed = parse_fig2d_individuals(fig_rows)
    inactive_counts = parse_inactive_counts(exclusion_rows)

    all_intervals: list[IndividualProbeInterval] = []
    summaries: dict[str, object] = {}
    for species in SPECIES:
        rows = [
            interval_from_probe_bins(species, source_row, bins)
            for source_row, bins in parsed[species]
        ]
        all_intervals.extend(rows)
        if len(rows) != inactive_counts[species]:
            raise ValueError(
                f"{species}: Figure 2D/S2 individual rows ({len(rows)}) do not "
                f"match exclusion-table inactive count ({inactive_counts[species]})"
            )
        summaries[species] = summarize_species(rows)

    first_minute = {
        species: float(summaries[species]["probe_by_1min_probability"])
        for species in SPECIES
    }
    slowest = min(first_minute, key=first_minute.get)
    fastest = max(first_minute, key=first_minute.get)

    result = {
        "status": "INDIVIDUAL_ONE_MINUTE_INTERVAL_CENSORED_PROBE_ONSET",
        "source": {
            "fig2d_csv": str(fig2d_csv),
            "exclusion_csv": str(exclusion_csv),
            "probe_bins": ["-1-0"] + [f"{i}-{i+1}" for i in range(8)],
        },
        "primary_cohort_rule": (
            "Restrict to individuals with Probe%=0 in the -1 to 0 minute "
            "pre-stimulus bin. First post-stimulus bin with Probe%>0 defines "
            "a one-minute interval-censored onset; otherwise right-censor at 8 min."
        ),
        "row_count_validation": {
            species: {
                "fig2d_individual_rows": len(parsed[species]),
                "timepoint0_inactive_count": inactive_counts[species],
                "match": len(parsed[species]) == inactive_counts[species],
            }
            for species in SPECIES
        },
        "species": summaries,
        "cross_species_descriptive": {
            "fastest_first_minute_species": fastest,
            "fastest_first_minute_probability": first_minute[fastest],
            "slowest_first_minute_species": slowest,
            "slowest_first_minute_probability": first_minute[slowest],
            "first_minute_probability_range": (
                first_minute[fastest] - first_minute[slowest]
            ),
        },
        "claim_ceiling": (
            "These are individual-level one-minute interval-censored first "
            "post-stimulus probe bins derived from published percent-probing "
            "source data. They are not frame-resolved latencies, feeding success, "
            "fitness, a natural opportunity distribution, or an adaptive-versus-fixed comparison."
        ),
    }
    return result, all_intervals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fig2d-csv", required=True, type=Path)
    parser.add_argument("--exclusion-csv", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-individual-csv", required=True, type=Path)
    args = parser.parse_args()

    result, intervals = analyze(args.fig2d_csv, args.exclusion_csv)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    args.output_individual_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_individual_csv.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = list(asdict(intervals[0]))
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(row) for row in intervals)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
