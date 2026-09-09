from math import inf

import pytest

from adaptive_gain.general_response_identifiability import (
    candidate_from_intrinsic_persistence,
    candidate_from_memory,
    feasible_memory_interval,
    gain_identifiability_envelope,
    generalized_ar2_coefficients,
    generalized_trace_determinant,
    is_schur_stable_trace_determinant,
    parent_haploid_inverse,
)


def test_generalized_trace_determinant_and_ar2_coefficients():
    trace, determinant = generalized_trace_determinant(0.7, 0.4, 0.3)
    assert trace == pytest.approx(1.1)
    assert determinant == pytest.approx(0.46)
    assert generalized_ar2_coefficients(0.7, 0.4, 0.3) == pytest.approx((1.1, -0.46))


def test_parent_haploid_inverse_is_exact_alpha_one_special_case():
    trace, determinant = generalized_trace_determinant(1.0, 0.8, 0.125)
    assert (trace, determinant) == pytest.approx((1.8, 0.825))
    estimate = parent_haploid_inverse(trace, determinant)
    assert estimate.intrinsic_persistence == pytest.approx(1.0)
    assert estimate.community_memory == pytest.approx(0.8)
    assert estimate.loop_gain == pytest.approx(0.125)


def test_same_transient_has_distinct_generalized_biological_decompositions():
    trace = 1.8
    determinant = 0.825
    expected = (
        (0.8, 1.0, 0.125),
        (0.9, 0.9, 0.15),
        (0.99, 0.81, 2.31),
    )
    for phi, alpha, gain in expected:
        candidate = candidate_from_memory(trace, determinant, phi)
        assert candidate.community_memory == pytest.approx(phi)
        assert candidate.intrinsic_persistence == pytest.approx(alpha)
        assert candidate.loop_gain == pytest.approx(gain)
        recovered = generalized_trace_determinant(
            candidate.intrinsic_persistence,
            candidate.community_memory,
            candidate.loop_gain,
        )
        assert recovered == pytest.approx((trace, determinant))


def test_feasible_memory_interval_is_set_by_observed_trace():
    high_trace = feasible_memory_interval(1.8)
    assert high_trace.lower == pytest.approx(0.8)
    assert high_trace.upper == pytest.approx(1.0)
    assert high_trace.upper_open

    low_trace = feasible_memory_interval(0.7)
    assert low_trace.lower == pytest.approx(0.0)
    assert low_trace.upper == pytest.approx(0.7)
    assert not low_trace.upper_open


def test_stable_high_trace_observation_has_unbounded_gain_above():
    trace = 1.8
    determinant = 0.825
    assert is_schur_stable_trace_determinant(trace, determinant)
    envelope = gain_identifiability_envelope(trace, determinant)
    assert envelope.gain_upper_unbounded
    assert envelope.gain_upper_bound == inf
    assert envelope.stationary_memory == pytest.approx(0.841886116991581)
    assert envelope.gain_lower_bound == pytest.approx(0.116227766016838)

    # The divergence is visible directly while trace and determinant stay fixed.
    assert candidate_from_memory(trace, determinant, 0.99).loop_gain == pytest.approx(2.31)
    assert candidate_from_memory(trace, determinant, 0.999).loop_gain == pytest.approx(24.801)


def test_trace_below_one_has_finite_gain_envelope():
    trace, determinant = generalized_trace_determinant(0.4, 0.3, 0.2)
    assert (trace, determinant) == pytest.approx((0.7, 0.26))
    assert is_schur_stable_trace_determinant(trace, determinant)
    envelope = gain_identifiability_envelope(trace, determinant)
    assert not envelope.gain_upper_unbounded
    assert envelope.gain_lower_bound == pytest.approx(0.196662954709577)
    assert envelope.gain_upper_bound == pytest.approx(0.866666666666667)
    assert envelope.stationary_memory == pytest.approx(0.251668522645212)
    assert envelope.gain_lower_bound <= 0.2 <= envelope.gain_upper_bound


def test_independent_alpha_or_phi_collapses_the_ridge():
    trace = 1.8
    determinant = 0.825
    from_alpha = candidate_from_intrinsic_persistence(trace, determinant, 1.0)
    from_phi = candidate_from_memory(trace, determinant, 0.8)
    assert from_alpha == from_phi
    assert from_alpha.loop_gain == pytest.approx(0.125)


def test_unstable_observation_rejected_by_default_envelope():
    trace = 1.2
    determinant = 1.1
    assert not is_schur_stable_trace_determinant(trace, determinant)
    with pytest.raises(ValueError):
        gain_identifiability_envelope(trace, determinant)
    # The algebraic compatibility class can still be inspected explicitly.
    envelope = gain_identifiability_envelope(trace, determinant, require_stable=False)
    assert not envelope.stable_observation


def test_invalid_trace_or_incompatible_factor_rejected():
    with pytest.raises(ValueError):
        feasible_memory_interval(-0.1)
    with pytest.raises(ValueError):
        feasible_memory_interval(2.0)
    with pytest.raises(ValueError):
        candidate_from_memory(0.7, 0.26, 0.8)
    with pytest.raises(ValueError):
        candidate_from_intrinsic_persistence(1.8, 0.825, 0.5)
