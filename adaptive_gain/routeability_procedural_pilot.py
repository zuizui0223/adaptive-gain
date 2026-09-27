"""Nuisance-only summaries for the direct routeability procedural pilot.

These helpers intentionally do not accept or return focal architecture/access
contrasts. They are designed to freeze response-window and pooled full-
information nuisance quantities before the confirmatory experiment.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import isfinite
from statistics import mean, pvariance
from typing import Hashable, Iterable, Sequence


def freeze_response_window(
    terminal_latencies: Iterable[float],
    *,
    candidate_windows: Sequence[float],
    required_coverage: float = 0.95,
    upper_bound: float,
) -> float:
    """Choose the smallest predeclared window meeting the coverage rule."""

    latencies = tuple(float(value) for value in terminal_latencies)
    if not latencies:
        raise ValueError("at least one terminal latency is required")
    if any((not isfinite(value) or value < 0) for value in latencies):
        raise ValueError("terminal latencies must be finite and non-negative")
    if not 0 < required_coverage <= 1:
        raise ValueError("required_coverage must lie in (0, 1]")
    upper_bound = float(upper_bound)
    if not isfinite(upper_bound) or upper_bound <= 0:
        raise ValueError("upper_bound must be finite and positive")

    windows = tuple(float(value) for value in candidate_windows)
    if not windows:
        raise ValueError("candidate_windows cannot be empty")
    if any((not isfinite(value) or value <= 0) for value in windows):
        raise ValueError("candidate windows must be finite and positive")
    if tuple(sorted(set(windows))) != windows:
        raise ValueError("candidate_windows must be strictly increasing and unique")
    if windows[-1] > upper_bound:
        raise ValueError("candidate window exceeds the predeclared upper bound")

    n = len(latencies)
    for window in windows:
        coverage = sum(value <= window for value in latencies) / n
        if coverage >= required_coverage:
            return window
    raise ValueError(
        "no prespecified candidate response window reaches required coverage"
    )


@dataclass(frozen=True)
class FullInformationPilotTrial:
    individual_id: Hashable
    colony_id: Hashable | None
    correct_within_window: bool
    timeout: bool
    block: int


def _sample_variance(values: Sequence[float]) -> float | None:
    if len(values) < 2:
        return None
    mu = mean(values)
    return sum((value - mu) ** 2 for value in values) / (len(values) - 1)


def pooled_full_information_nuisance_receipt(
    trials: Iterable[FullInformationPilotTrial],
) -> dict[str, object]:
    """Summarize pooled B=3 pilot data without focal treatment labels."""

    rows = tuple(trials)
    if not rows:
        raise ValueError("at least one full-information pilot trial is required")
    for row in rows:
        if type(row.block) is not int or row.block < 1:
            raise ValueError("block must be a positive integer")
        if row.timeout and row.correct_within_window:
            raise ValueError("a timeout cannot also be correct within window")

    by_individual: dict[Hashable, list[FullInformationPilotTrial]] = defaultdict(list)
    by_colony: dict[Hashable, list[FullInformationPilotTrial]] = defaultdict(list)
    by_block: dict[int, list[FullInformationPilotTrial]] = defaultdict(list)
    for row in rows:
        by_individual[row.individual_id].append(row)
        if row.colony_id is not None:
            by_colony[row.colony_id].append(row)
        by_block[row.block].append(row)

    individual_success = [
        mean(float(row.correct_within_window) for row in group)
        for group in by_individual.values()
    ]
    individual_timeout = [
        mean(float(row.timeout) for row in group)
        for group in by_individual.values()
    ]
    colony_success = [
        mean(float(row.correct_within_window) for row in group)
        for group in by_colony.values()
    ]

    block_summary = {}
    for block, group in sorted(by_block.items()):
        block_summary[str(block)] = {
            "trial_count": len(group),
            "success_fraction": mean(
                float(row.correct_within_window) for row in group
            ),
            "timeout_fraction": mean(float(row.timeout) for row in group),
        }

    return {
        "schema": "adaptive-gain-routeability-procedural-pilot-receipt-v1",
        "focal_architecture_contrast_opened": False,
        "trial_count": len(rows),
        "individual_count": len(by_individual),
        "colony_count": len(by_colony),
        "pooled_success_fraction": mean(
            float(row.correct_within_window) for row in rows
        ),
        "pooled_timeout_fraction": mean(float(row.timeout) for row in rows),
        "individual_success_fraction_mean": mean(individual_success),
        "individual_success_fraction_variance": _sample_variance(individual_success),
        "individual_timeout_fraction_mean": mean(individual_timeout),
        "individual_timeout_fraction_variance": _sample_variance(individual_timeout),
        "colony_success_fraction_variance": _sample_variance(colony_success),
        "block_summary": block_summary,
        "claim_ceiling": (
            "Pooled full-information nuisance summary only; no architecture, "
            "access, H1 or H2 effect is estimated."
        ),
    }
