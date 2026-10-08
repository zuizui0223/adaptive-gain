"""Verify dimensionless causal-gauge correlation bounds without external data."""
import math
import pytest
from adaptive_gain.common_shock_correlation_sensitivity import (
    innovation_correlation,
    critical_innovation_correlation,
    minimum_response_fraction_from_correlation_cap,
    direct_half_life_multiplier_from_correlation_cap,
)
from adaptive_gain.ou_moving_optimum_congruence import reciprocal_realization

@pytest.mark.parametrize("q", [0.05,0.1,0.25,0.5,0.75,0.95,1.0])
def test_correlation_matches_diffusion_matrix(q):
    vx,vo=0.2,0.1
    if q==1.0:
        assert innovation_correlation(q,vx,vo)==0.0
    else:
        r=reciprocal_realization(alpha=0.8,v_trait=vx,v_optimum=vo,
                                 anc=0.0,theta0=0.1,response_fraction=q)
        s11,s12=r.S[0]
        s21,s22=r.S[1]
        q11=s11*s11+s12*s12
        q12=s11*s21+s12*s22
        q22=s21*s21+s22*s22
        assert innovation_correlation(q,vx,vo)==pytest.approx(
            q12/math.sqrt(q11*q22),rel=1e-12,abs=1e-12)

@pytest.mark.parametrize("q", [0.1,0.25,0.5,0.8])
def test_exact_inverse_bound(q):
    vx,vo=0.2,0.1
    cap=abs(innovation_correlation(q,vx,vo))
    q_min=minimum_response_fraction_from_correlation_cap(vx,vo,cap)
    assert q_min==pytest.approx(q,abs=1e-12)
    assert direct_half_life_multiplier_from_correlation_cap(
        vx,vo,cap)==pytest.approx(1.0/q,rel=1e-12)

def test_unbounded_above_critical_cap():
    critical=critical_innovation_correlation(0.2,0.1)
    assert critical==pytest.approx(math.sqrt(2.0/3.0))
    assert minimum_response_fraction_from_correlation_cap(0.2,0.1,critical)==0.0
    assert math.isinf(direct_half_life_multiplier_from_correlation_cap(0.2,0.1,0.9))

def test_zero_cap_forces_one_way():
    assert minimum_response_fraction_from_correlation_cap(0.2,0.1,0.0)==1.0
    assert direct_half_life_multiplier_from_correlation_cap(0.2,0.1,0.0)==1.0

@pytest.mark.parametrize("bad",[-0.1,1.0,float('nan'),float('inf')])
def test_bad_caps_rejected(bad):
    with pytest.raises(ValueError):
        minimum_response_fraction_from_correlation_cap(0.2,0.1,bad)
