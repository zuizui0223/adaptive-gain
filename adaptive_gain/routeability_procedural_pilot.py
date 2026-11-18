"""Nuisance-only summaries for the direct routeability procedural pilot.

These helpers intentionally do not accept or return focal architecture/access
contrasts. They are designed to freeze response-window and pooled full-
information nuisance quantities before the confirmatory experiment.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import isfinite
from statistics import mean
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



def _balanced_binary_repeatability(
    by_individual: dict[Hashable, list[FullInformationPilotTrial]],
) -> tuple[bool, int | None, float | None]:
    """Method-of-moments repeated-trial ICC for a balanced binary pilot.

    For equal m trials per individual,
    Var(individual mean) = p(1-p) * [1/m + rho*(1-1/m)].
    The moment estimate is truncated to [0,1]. Unequal trial counts return
    no ICC rather than applying a balanced formula silently.
    """

    counts = {len(group) for group in by_individual.values()}
    if len(counts) != 1 or not counts:
        return False, None, None
    m = next(iter(counts))
    if m < 2 or len(by_individual) < 2:
        return True, m, None

    individual_means = [
        mean(float(row.correct_within_window) for row in group)
        for group in by_individual.values()
    ]
    p = mean(
        float(row.correct_within_window)
        for group in by_individual.values()
        for row in group
    )
    binary_variance = p * (1.0 - p)
    if binary_variance == 0:
        return True, m, None

    between = _sample_variance(individual_means)
    if between is None:
        return True, m, None
    rho = (
        between / binary_variance - 1.0 / m
    ) / (1.0 - 1.0 / m)
    return True, m, max(0.0, min(1.0, rho))

def pooled_full_information_nuisance_receipt(
    trials: Iterable[FullInformationPilotTrial],
    *,
    randomized_individual_ids: Iterable[Hashable] | None = None,
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

    balanced, trials_per_individual, trial_icc = _balanced_binary_repeatability(
        by_individual
    )

    randomized_ids = (
        None
        if randomized_individual_ids is None
        else set(randomized_individual_ids)
    )
    if randomized_ids is not None:
        observed_ids = set(by_individual)
        if not observed_ids <= randomized_ids:
            raise ValueError(
                "pilot trials contain individuals absent from randomized_individual_ids"
            )
        randomized_count = len(randomized_ids)
        dropout_fraction = (
            None
            if randomized_count == 0
            else (randomized_count - len(observed_ids)) / randomized_count
        )
    else:
        randomized_count = None
        dropout_fraction = None

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
        "equal_trials_per_individual": balanced,
        "trials_per_individual": trials_per_individual,
        "trial_icc_moment": trial_icc,
        "randomized_individual_count": randomized_count,
        "randomized_individual_dropout_fraction": dropout_fraction,
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
