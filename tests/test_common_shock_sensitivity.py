from __future__ import annotations

import pytest

from adaptive_gain.common_shock_sensitivity import (
    direct_half_life_upper_bound,
    half_life_multiplier_upper_bound,
    minimum_response_fraction_from_common_shock_bound,
)


def test_zero_common_shock_recovers_one_way_half_life() -> None:
    assert minimum_response_fraction_from_common_shock_bound(0.2, 0.0) == pytest.approx(1.0)
    assert half_life_multiplier_upper_bound(0.2, 0.0) == pytest.approx(1.0)
    assert direct_half_life_upper_bound(12.0, 0.2, 0.0) == pytest.approx(12.0)


@pytest.mark.parametrize(
    "relative_bound,expected_multiplier",
    [(0.5, 1.5), (1.0, 2.0), (4.0, 5.0), (9.0, 10.0), (99.0, 100.0)],
)
def test_relative_common_shock_bound_maps_directly_to_half_life_multiplier(
    relative_bound: float, expected_multiplier: float
) -> None:
    v_trait = 0.2
    c = relative_bound * v_trait
    assert half_life_multiplier_upper_bound(v_trait, c) == pytest.approx(
        expected_multiplier
    )
    assert direct_half_life_upper_bound(12.0, v_trait, c) == pytest.approx(
        12.0 * expected_multiplier
    )


def test_tighter_common_shock_bound_tightens_identified_set() -> None:
    v_trait = 0.2
    bounds = [2.0, 1.0, 0.2, 0.02, 0.0]
    upper = [direct_half_life_upper_bound(12.0, v_trait, c) for c in bounds]
    assert all(a > b for a, b in zip(upper, upper[1:]))
    assert upper[-1] == pytest.approx(12.0)


@pytest.mark.parametrize(
    "v_trait,bound",
    [(0.0, 0.1), (-1.0, 0.1), (0.2, -0.1)],
)
def test_invalid_common_shock_bounds_fail(v_trait: float, bound: float) -> None:
    with pytest.raises(ValueError):
        minimum_response_fraction_from_common_shock_bound(v_trait, bound)
