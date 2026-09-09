from math import isclose

import pytest

from adaptive_gain.community_spectral_timescale import asymptotic_variance_rate
from adaptive_gain.structural_spectral_joint_bounds import (
    bounded_arity_spectral_ceiling,
    joint_asymptotic_variance_upper_bound,
    reversible_temporal_amplification_upper_bound,
    structural_reward_variance_upper_bound,
)


def test_popoviciu_structural_reward_ceiling():
    # gap range 3, lambda 2 -> reward range width 6 -> variance <= 36/4 = 9.
    assert isclose(
        structural_reward_variance_upper_bound(3, lambda_cost=2.0),
        9.0,
    )


def test_reversible_temporal_amplification_ceiling():
    assert isclose(reversible_temporal_amplification_upper_bound(0.5), 3.0)
    assert isclose(reversible_temporal_amplification_upper_bound(0.0), 1.0)
    with pytest.raises(ValueError):
        reversible_temporal_amplification_upper_bound(1.0)


def test_joint_ceiling_multiplies_structural_amplitude_and_temporal_coherence():
    ceiling = joint_asymptotic_variance_upper_bound(
        3,
        lambda_cost=2.0,
        maximal_nontrivial_eigenvalue=0.5,
    )
    assert isclose(ceiling, 27.0)


def test_two_state_symmetric_chain_attains_joint_bound_exactly():
    # Symmetric chain has stationary pi=(1/2,1/2) and one nontrivial eigenvalue r.
    r = 0.6
    transition = (
        ((1.0 + r) / 2.0, (1.0 - r) / 2.0),
        ((1.0 - r) / 2.0, (1.0 + r) / 2.0),
    )
    stationary = (0.5, 0.5)

    gap_max = 4.0
    lambda_cost = 1.5
    reward_width = lambda_cost * gap_max
    rewards = (0.0, reward_width)

    observed = asymptotic_variance_rate(stationary, transition, rewards)
    bound = joint_asymptotic_variance_upper_bound(
        gap_max,
        lambda_cost=lambda_cost,
        maximal_nontrivial_eigenvalue=r,
    )
    assert isclose(observed, bound, rel_tol=1e-10, abs_tol=1e-10)


def test_bounded_arity_parent_scope_yields_joint_ceiling():
    # The four-world, three-query, binary, adaptive-depth-two scope has gap ceiling 1.
    receipt = bounded_arity_spectral_ceiling(
        4,
        3,
        2,
        2,
        lambda_cost=2.0,
        maximal_nontrivial_eigenvalue=0.5,
    )
    assert receipt.structural_gap_upper_bound == 1
    assert isclose(receipt.instantaneous_variance_upper_bound, 1.0)
    assert isclose(receipt.temporal_amplification_upper_bound, 3.0)
    assert isclose(receipt.asymptotic_variance_upper_bound, 3.0)


def test_frontier_edge_cap_can_tighten_joint_temporal_ceiling():
    unrestricted = bounded_arity_spectral_ceiling(
        12,
        12,
        3,
        2,
        lambda_cost=1.0,
        maximal_nontrivial_eigenvalue=0.5,
    )
    capped = bounded_arity_spectral_ceiling(
        12,
        12,
        3,
        2,
        lambda_cost=1.0,
        maximal_nontrivial_eigenvalue=0.5,
        frontier_edge_cap=4,
    )
    assert capped.structural_gap_upper_bound <= unrestricted.structural_gap_upper_bound
    assert capped.asymptotic_variance_upper_bound <= unrestricted.asymptotic_variance_upper_bound
