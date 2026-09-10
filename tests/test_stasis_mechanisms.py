from math import isclose

import pytest

from adaptive_gain.endogenous_community_feedback import interior_feedback_equilibrium
from adaptive_gain.stasis_mechanisms import (
    cancellation_cycle_map,
    summarize_cancellation_stasis,
    summarize_restoring_stasis,
)


def test_zero_sum_cycle_has_identity_period_map():
    cycle = (2.0, -2.0)
    for state in (-5.0, -0.3, 0.0, 1.7, 20.0):
        assert isclose(cancellation_cycle_map(state, cycle), state)

    summary = summarize_cancellation_stasis(cycle)
    assert summary.period == 2
    assert isclose(summary.activity, 4.0)
    assert isclose(summary.retained_change, 0.0)
    assert isclose(summary.period_multiplier, 1.0)
    assert summary.neutral


def test_cancellation_can_have_arbitrarily_large_within_cycle_activity():
    summary = summarize_cancellation_stasis((100.0, -100.0))
    assert isclose(summary.activity, 200.0)
    assert isclose(summary.retained_change, 0.0)
    assert isclose(summary.period_multiplier, 1.0)


def test_cancellation_summary_rejects_nonzero_period_drift():
    with pytest.raises(ValueError):
        summarize_cancellation_stasis((2.0, -1.0))


def test_real_stable_eigenvalues_define_monotone_restoring_candidate():
    summary = summarize_restoring_stasis((0.7, 0.4))
    assert isclose(summary.spectral_radius, 0.7)
    assert summary.locally_attractive
    assert not summary.oscillatory
    assert summary.monotone_candidate


def test_complex_stable_pair_defines_oscillatory_restoring_stasis():
    summary = summarize_restoring_stasis((0.7 + 0.2j, 0.7 - 0.2j))
    assert summary.spectral_radius < 1.0
    assert summary.locally_attractive
    assert summary.oscillatory
    assert not summary.monotone_candidate


def test_unit_multiplier_is_not_restoring():
    summary = summarize_restoring_stasis((1.0, 0.5))
    assert isclose(summary.spectral_radius, 1.0)
    assert not summary.locally_attractive


def test_parent_feedback_equilibrium_is_classified_as_restoring():
    equilibrium = interior_feedback_equilibrium(
        low_reward=-0.5,
        high_reward=0.5,
        q_base=0.5,
        feedback_strength=-0.5,
        community_memory=0.8,
    )
    assert equilibrium.locally_stable
    assert equilibrium.eigenvalues is not None
    restoring = summarize_restoring_stasis(equilibrium.eigenvalues)
    assert restoring.locally_attractive


def test_neutral_cancellation_and_attractive_restoring_are_dynamically_distinct():
    cancellation = summarize_cancellation_stasis((3.0, -3.0))
    restoring = summarize_restoring_stasis((0.8, 0.5))
    assert isclose(cancellation.period_multiplier, 1.0)
    assert restoring.spectral_radius < 1.0
    assert cancellation.neutral
    assert restoring.locally_attractive
