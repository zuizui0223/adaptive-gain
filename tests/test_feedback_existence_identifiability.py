import math

import pytest

from adaptive_gain.feedback_existence_identifiability import (
    characteristic_polynomial_at,
    compatible_gain,
    discriminant,
    has_nonnegative_real_no_feedback_decomposition,
    minimum_compatible_gain_over_unit_memory_interval,
    no_feedback_decomposition,
    oscillatory_transient_forces_positive_feedback,
    real_eigenvalues,
    summarize_feedback_existence,
)


def test_real_nonnegative_eigenvalues_admit_zero_feedback_decomposition():
    r1, r2 = 0.4, 0.8
    T = r1 + r2
    D = r1 * r2
    assert has_nonnegative_real_no_feedback_decomposition(T, D)
    alpha, phi, G = no_feedback_decomposition(T, D)
    assert (alpha, phi, G) == pytest.approx((0.8, 0.4, 0.0))
    assert compatible_gain(T, D, phi) == pytest.approx(0.0)


def test_real_repeated_mode_also_allows_zero_feedback():
    r = 0.7
    T = 2.0 * r
    D = r * r
    assert discriminant(T, D) == pytest.approx(0.0)
    assert real_eigenvalues(T, D) == pytest.approx((r, r))
    assert has_nonnegative_real_no_feedback_decomposition(T, D)
    assert no_feedback_decomposition(T, D) == pytest.approx((r, r, 0.0))


def test_complex_eigenpair_forces_positive_feedback_for_all_unit_interval_memories():
    rho = 0.85
    theta = 0.7
    T = 2.0 * rho * math.cos(theta)
    D = rho * rho
    assert oscillatory_transient_forces_positive_feedback(T, D)
    assert discriminant(T, D) < 0.0
    for phi in (0.0, 0.1, 0.3, 0.6, 0.9, 0.99):
        assert compatible_gain(T, D, phi) > 0.0
    assert minimum_compatible_gain_over_unit_memory_interval(T, D) > 0.0


def test_characteristic_polynomial_is_exact_gain_numerator():
    T, D, phi = 1.2, 0.5, 0.35
    assert compatible_gain(T, D, phi) * (1.0 - phi) == pytest.approx(
        characteristic_polynomial_at(T, D, phi)
    )


def test_parent_oscillatory_example_forces_feedback():
    # A stable complex pair with modulus sqrt(D)<1.
    T, D = 1.2, 0.5
    summary = summarize_feedback_existence(T, D)
    assert summary.oscillatory
    assert summary.feedback_existence_forced
    assert not summary.no_feedback_decomposition_exists
    assert summary.minimum_gain_over_unit_memory is not None
    assert summary.minimum_gain_over_unit_memory > 0.0


def test_monotone_stable_example_cannot_establish_feedback_existence():
    r1, r2 = 0.3, 0.9
    T, D = r1 + r2, r1 * r2
    summary = summarize_feedback_existence(T, D)
    assert not summary.oscillatory
    assert summary.no_feedback_decomposition_exists
    assert not summary.feedback_existence_forced


def test_negative_real_mode_is_outside_nonnegative_persistence_corollary():
    r1, r2 = -0.2, 0.8
    T, D = r1 + r2, r1 * r2
    assert discriminant(T, D) >= 0.0
    assert not has_nonnegative_real_no_feedback_decomposition(T, D)
    with pytest.raises(ValueError):
        no_feedback_decomposition(T, D)


def test_complex_pair_has_no_real_eigenvalue_decomposition():
    T, D = 1.0, 0.6
    assert discriminant(T, D) < 0.0
    with pytest.raises(ValueError):
        real_eigenvalues(T, D)
    with pytest.raises(ValueError):
        no_feedback_decomposition(T, D)


def test_phi_must_be_below_one():
    with pytest.raises(ValueError):
        compatible_gain(1.0, 0.5, 1.0)
