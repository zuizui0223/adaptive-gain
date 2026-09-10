import pytest

from adaptive_gain.general_response_scalar_observability import (
    identify_trace_determinant_from_four_points,
    scalar_mode_visibility_determinant,
    two_real_mode_visibility_determinant,
)


def _advance(trace, determinant, x0, x1):
    x2 = trace * x1 - determinant * x0
    x3 = trace * x2 - determinant * x1
    return x0, x1, x2, x3


def test_four_points_recover_generalized_local_invariants_exactly():
    points = _advance(1.8, 0.825, 1.0, 0.2)
    estimate = identify_trace_determinant_from_four_points(*points)
    assert estimate.trace == pytest.approx(1.8)
    assert estimate.determinant == pytest.approx(0.825)
    assert estimate.visibility_determinant == pytest.approx(-0.505)
    assert estimate.normalized_visibility_margin > 0.0


def test_single_visible_eigenmode_is_rank_deficient():
    r = 0.75
    points = (1.0, r, r * r, r**3)
    assert scalar_mode_visibility_determinant(*points[:3]) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        identify_trace_determinant_from_four_points(*points)


def test_two_real_mode_visibility_closed_form():
    c1, c2 = 2.0, -0.5
    r1, r2 = 0.8, 0.3
    x0 = c1 + c2
    x1 = c1 * r1 + c2 * r2
    x2 = c1 * r1**2 + c2 * r2**2
    direct = scalar_mode_visibility_determinant(x0, x1, x2)
    closed = two_real_mode_visibility_determinant(c1, c2, r1, r2)
    assert direct == pytest.approx(closed)
    assert closed == pytest.approx(-0.25)


def test_two_distinct_visible_modes_recover_sum_and_product():
    c1, c2 = 1.2, 0.7
    r1, r2 = 0.85, 0.35
    points = tuple(c1 * r1**t + c2 * r2**t for t in range(4))
    estimate = identify_trace_determinant_from_four_points(*points)
    assert estimate.trace == pytest.approx(r1 + r2)
    assert estimate.determinant == pytest.approx(r1 * r2)


def test_repeated_eigenvalue_or_missing_mode_closes_visibility_gate():
    assert two_real_mode_visibility_determinant(1.0, 1.0, 0.5, 0.5) == pytest.approx(0.0)
    assert two_real_mode_visibility_determinant(1.0, 0.0, 0.8, 0.2) == pytest.approx(0.0)


def test_numerically_near_single_mode_can_be_rejected_by_tolerance():
    c1, c2 = 1.0, 1e-14
    r1, r2 = 0.8, 0.2
    points = tuple(c1 * r1**t + c2 * r2**t for t in range(4))
    with pytest.raises(ValueError):
        identify_trace_determinant_from_four_points(
            *points,
            relative_tolerance=1e-10,
        )


def test_invalid_tolerance_rejected():
    with pytest.raises(ValueError):
        identify_trace_determinant_from_four_points(1, 2, 3, 4, relative_tolerance=-1)
