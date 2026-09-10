from math import isclose

import pytest

from adaptive_gain.community_spectral_timescale import asymptotic_variance_rate
from adaptive_gain.structural_spectral_joint_bounds import (
    bounded_arity_directional_crossover_proxy_upper_bound,
    bounded_arity_spectral_ceiling,
    directional_crossover_proxy_upper_bound,
    joint_asymptotic_variance_upper_bound,
    reversible_temporal_amplification_upper_bound,
    structural_reward_variance_upper_bound,
    structural_temporal_slack,
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


def test_directional_crossover_proxy_ceiling_divides_by_mean_selection_squared():
    # Joint variance ceiling is 27.  A declared |mu|=0.3 gives 27 / 0.09 = 300.
    bound = directional_crossover_proxy_upper_bound(
        3,
        lambda_cost=2.0,
        maximal_nontrivial_eigenvalue=0.5,
        stationary_mean_selection_magnitude=0.3,
    )
    assert isclose(bound, 300.0)
    with pytest.raises(ValueError):
        directional_crossover_proxy_upper_bound(
            3,
            lambda_cost=2.0,
            maximal_nontrivial_eigenvalue=0.5,
            stationary_mean_selection_magnitude=0.0,
        )


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

    stationary_variance = reward_width * reward_width / 4.0
    slack = structural_temporal_slack(
        gap_max,
        lambda_cost=lambda_cost,
        maximal_nontrivial_eigenvalue=r,
        stationary_reward_variance=stationary_variance,
        asymptotic_variance_rate=observed,
    )
    assert slack.range_variance_saturation == pytest.approx(1.0)
    assert slack.reward_slow_mode_alignment == pytest.approx(1.0)
    assert slack.realized_to_ceiling_ratio == pytest.approx(1.0)


def test_structural_temporal_slack_factors_multiply_to_realized_bound_ratio():
    # Structural ceiling=4, temporal ceiling=3, joint ceiling=12.
    # Realized variance=2 uses half the structural variance budget; sigma2=3
    # uses half the modal ceiling 2*3=6, so realized/joint = 1/4.
    slack = structural_temporal_slack(
        4.0,
        lambda_cost=1.0,
        maximal_nontrivial_eigenvalue=0.5,
        stationary_reward_variance=2.0,
        asymptotic_variance_rate=3.0,
    )
    assert slack.structural_variance_ceiling == pytest.approx(4.0)
    assert slack.temporal_amplification_ceiling == pytest.approx(3.0)
    assert slack.joint_variance_ceiling == pytest.approx(12.0)
    assert slack.range_variance_saturation == pytest.approx(0.5)
    assert slack.reward_slow_mode_alignment == pytest.approx(0.5)
    assert slack.realized_to_ceiling_ratio == pytest.approx(0.25)
    assert (
        slack.range_variance_saturation * slack.reward_slow_mode_alignment
        == pytest.approx(slack.realized_to_ceiling_ratio)
    )


def test_structural_temporal_slack_zero_variance_has_no_alignment_factor():
    slack = structural_temporal_slack(
        4.0,
        lambda_cost=1.0,
        maximal_nontrivial_eigenvalue=0.5,
        stationary_reward_variance=0.0,
        asymptotic_variance_rate=0.0,
    )
    assert slack.range_variance_saturation == 0.0
    assert slack.reward_slow_mode_alignment is None
    assert slack.realized_to_ceiling_ratio == 0.0


def test_structural_temporal_slack_rejects_inputs_that_violate_component_bounds():
    with pytest.raises(ValueError):
        structural_temporal_slack(
            4.0,
            lambda_cost=1.0,
            maximal_nontrivial_eigenvalue=0.5,
            stationary_reward_variance=4.1,
            asymptotic_variance_rate=0.0,
        )
    with pytest.raises(ValueError):
        structural_temporal_slack(
            4.0,
            lambda_cost=1.0,
            maximal_nontrivial_eigenvalue=0.5,
            stationary_reward_variance=2.0,
            asymptotic_variance_rate=6.1,
        )


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

    crossover = bounded_arity_directional_crossover_proxy_upper_bound(
        4,
        3,
        2,
        2,
        lambda_cost=2.0,
        maximal_nontrivial_eigenvalue=0.5,
        stationary_mean_selection_magnitude=0.25,
    )
    assert isclose(crossover, 48.0)


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
