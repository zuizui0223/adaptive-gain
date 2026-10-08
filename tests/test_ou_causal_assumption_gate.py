from __future__ import annotations

import pytest

from adaptive_gain.ou_causal_assumption_gate import (
    independent_innovation_equivalence_forces_one_way,
    output_preserving_gauge,
    reciprocal_gauge_requires_shared_innovation,
)


def test_identity_gauge_preserves_original_one_way_model() -> None:
    g = output_preserving_gauge(
        alpha=0.8,
        v_trait=0.12,
        v_optimum=0.07,
        t=0.0,
        u=1.0,
    )
    assert g.A[0] == pytest.approx((0.8, -0.8))
    assert g.A[1] == pytest.approx((0.0, 0.0))
    assert g.Q[0] == pytest.approx((0.12, 0.0))
    assert g.Q[1] == pytest.approx((0.0, 0.07))
    assert not g.reciprocal


@pytest.mark.parametrize("t,u", [(0.2, 1.0), (-0.2, 1.0), (1.0, 2.0)])
def test_reciprocal_output_preserving_gauge_induces_shared_innovation(
    t: float, u: float
) -> None:
    g = output_preserving_gauge(
        alpha=0.8,
        v_trait=0.12,
        v_optimum=0.07,
        t=t,
        u=u,
    )
    assert g.reciprocal
    assert g.innovation_covariance != pytest.approx(0.0)
    assert reciprocal_gauge_requires_shared_innovation(
        v_trait=0.12, t=t, u=u
    )


def test_nonzero_transform_can_still_be_one_way_at_degenerate_boundary() -> None:
    # t=-u gives reverse coupling zero even though the transformed diffusion
    # has cross-innovation covariance.
    g = output_preserving_gauge(
        alpha=0.8,
        v_trait=0.12,
        v_optimum=0.07,
        t=-1.0,
        u=1.0,
    )
    assert not g.reciprocal
    assert g.reverse_coupling == pytest.approx(0.0)
    assert g.innovation_covariance == pytest.approx(-0.12)


def test_independent_innovation_exact_equivalence_forces_one_way() -> None:
    # The evoTS exogenous model satisfies the prerequisite coefficient matches
    # and the conclusion: hidden -> trait only, no reverse coupling.
    assert independent_innovation_equivalence_forces_one_way(
        alpha=0.8,
        v_trait=0.12,
        q_trait=0.12,
        a11=0.8,
        a12=-0.8,
        a21=0.0,
        a22=0.0,
        q_latent=0.07,
    )


def test_reciprocal_independent_noise_candidate_cannot_match_required_coefficients() -> None:
    # Trace=alpha and det=0 can be satisfied by reciprocal zero-mode drift,
    # but equality of the observed finite-time covariance also requires
    # q_trait*a11=v_trait*alpha. With q_trait=v_trait>0 this forces a11=alpha,
    # ruling out this reciprocal candidate.
    assert not independent_innovation_equivalence_forces_one_way(
        alpha=0.8,
        v_trait=0.12,
        q_trait=0.12,
        a11=0.4,
        a12=-0.4,
        a21=-0.4,
        a22=0.4,
        q_latent=0.07,
    )


def test_zero_trait_innovation_is_explicitly_outside_the_assumption_gate() -> None:
    with pytest.raises(ValueError):
        reciprocal_gauge_requires_shared_innovation(v_trait=0.0, t=0.3, u=1.0)
