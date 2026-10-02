"""Prospective public-data bridge from Spaethe et al. 2026.

Source:
    Spaethe et al. (2026), Science Advances 12:e adw9320,
    DOI 10.1126/sciadv.adw9320.

The individual conflict-test values below are transcribed from the authors'
public analysis code:
    stoeckl-lab/Spaethe_et_al_2024_beeDecisions/bayesianModel.m

In each array the value is the fraction of conflict-test choices following
colour.  We predefine the secondary-cue recruitment index as

    R = 1 - p_colour.

This is an empirical bridge quantity, not an estimate of C_A or C_F.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median


EASY_PATTERN_COLOUR = (
    1.0, 1.0, 1.0, 1.0, 0.9, 0.9, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.9, 0.9, 1.0,
)
HARD_PATTERN_COLOUR = (
    0.6, 0.6, 0.8, 0.6, 0.4, 0.4, 0.3, 0.9, 0.7, 0.8,
    0.4, 0.6, 0.7, 0.8, 0.6, 0.4, 0.7, 0.7, 0.6, 0.8,
)
EASY_SHAPE_COLOUR = (
    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 1.0, 1.0, 1.0,
    0.8, 1.0, 1.0, 0.9, 1.0,
)
HARD_SHAPE_COLOUR = (
    0.8, 0.7, 0.8, 0.4, 0.6, 0.9, 0.3, 0.4, 0.7, 0.6,
    0.8, 0.6, 0.5, 0.7, 0.7,
)


def _recruitment(values: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(1.0 - value for value in values)


@dataclass(frozen=True)
class CueRecruitmentRow:
    secondary_feature: str
    difficulty: str
    n: int
    mean_colour_following: float
    median_colour_following: float
    mean_secondary_recruitment: float


@dataclass(frozen=True)
class BumblebeePublicBridgeReceipt:
    rows: tuple[CueRecruitmentRow, ...]
    pattern_recruitment_difference: float
    shape_recruitment_difference: float
    pooled_recruitment_difference: float
    registered_direction_holds_for_pattern: bool
    registered_direction_holds_for_shape: bool
    registered_direction_holds_pooled: bool
    claim_ceiling: str = (
        "conditional cue-set recruitment by task difficulty; "
        "not a direct estimate of adaptive/fixed routeability costs"
    )


def _row(feature: str, difficulty: str, values: tuple[float, ...]) -> CueRecruitmentRow:
    return CueRecruitmentRow(
        secondary_feature=feature,
        difficulty=difficulty,
        n=len(values),
        mean_colour_following=mean(values),
        median_colour_following=median(values),
        mean_secondary_recruitment=mean(_recruitment(values)),
    )


def spaethe_public_bridge_receipt() -> BumblebeePublicBridgeReceipt:
    easy_pattern = _row("pattern", "easy", EASY_PATTERN_COLOUR)
    hard_pattern = _row("pattern", "hard", HARD_PATTERN_COLOUR)
    easy_shape = _row("shape", "easy", EASY_SHAPE_COLOUR)
    hard_shape = _row("shape", "hard", HARD_SHAPE_COLOUR)

    pattern_delta = (
        hard_pattern.mean_secondary_recruitment
        - easy_pattern.mean_secondary_recruitment
    )
    shape_delta = (
        hard_shape.mean_secondary_recruitment
        - easy_shape.mean_secondary_recruitment
    )

    easy_pooled = EASY_PATTERN_COLOUR + EASY_SHAPE_COLOUR
    hard_pooled = HARD_PATTERN_COLOUR + HARD_SHAPE_COLOUR
    pooled_delta = mean(_recruitment(hard_pooled)) - mean(_recruitment(easy_pooled))

    return BumblebeePublicBridgeReceipt(
        rows=(easy_pattern, hard_pattern, easy_shape, hard_shape),
        pattern_recruitment_difference=pattern_delta,
        shape_recruitment_difference=shape_delta,
        pooled_recruitment_difference=pooled_delta,
        registered_direction_holds_for_pattern=pattern_delta > 0,
        registered_direction_holds_for_shape=shape_delta > 0,
        registered_direction_holds_pooled=pooled_delta > 0,
    )
