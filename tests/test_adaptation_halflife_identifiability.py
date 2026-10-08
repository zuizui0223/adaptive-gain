from __future__ import annotations

import math

import pytest

from adaptive_gain.adaptation_halflife_identifiability import (
    direct_half_life_from_reported,
    direct_trait_half_life,
    ou_half_life,
)


def test_direct_half_life_scales_as_inverse_response_fraction() -> None:
    alpha = 0.8
    baseline = ou_half_life(alpha)
    for q in [0.5, 0.1, 0.01, 0.001]:
        assert direct_trait_half_life(alpha, q) == pytest.approx(baseline / q)
        assert direct_trait_half_life(alpha, q) > baseline


def test_voje_12_year_point_estimate_has_unbounded_congruent_direct_half_life() -> None:
    reported = 12.0
    assert direct_half_life_from_reported(reported, 0.5) == pytest.approx(24.0)
    assert direct_half_life_from_reported(reported, 0.1) == pytest.approx(120.0)
    assert direct_half_life_from_reported(reported, 0.01) == pytest.approx(1200.0)
    assert direct_half_life_from_reported(reported, 0.001) == pytest.approx(12000.0)


def test_direct_half_life_diverges_as_q_approaches_zero() -> None:
    reported = 12.0
    values = [direct_half_life_from_reported(reported, 10.0 ** (-k)) for k in range(1, 7)]
    assert all(b > a for a, b in zip(values, values[1:]))
    assert values[-1] == pytest.approx(12_000_000.0)


@pytest.mark.parametrize(
    "reported,q",
    [(0.0, 0.5), (-1.0, 0.5), (12.0, 0.0), (12.0, 1.0)],
)
def test_invalid_reported_half_life_arguments_fail(reported: float, q: float) -> None:
    with pytest.raises(ValueError):
        direct_half_life_from_reported(reported, q)
