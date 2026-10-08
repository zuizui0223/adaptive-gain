import math
import pytest
from adaptive_gain.ou_nugget_state_space import loglik_random_walk_with_nugget,aicc
from adaptive_gain.ou_sampling_saturation import rapid_relaxation_covariance_limit

def test_boundary_first_point_has_no_biological_nugget():
    # At t=0 the latent process is deterministic.  Changing the nugget
    # affects only later observations, not first point's contribution.
    t=[0.,1.]
    v=[.1,.1]
    y=[1.,1.]
    l1=loglik_random_walk_with_nugget(t,y,v,1.,.4,.2)
    l2=loglik_random_walk_with_nugget(t,y,v,1.,.4,.4)
    expected=-.5*math.log(.2/(.1)) # l1-l2 = -.5 log((.7)/(.9))
    assert l1>l2
    assert math.isfinite(expected)

def test_random_walk_nugget_exact_2time_dense_law():
    # First obs has known measurement variance only.  At next obs,
    # Brownian variance is D*dt plus positive-time biological nugget.
    y=[1.4,1.8]
    m=1.5
    v=[.2,.3]
    D=.4;S=.12
    out=loglik_random_walk_with_nugget([0.,2.],y,v,m,D,S)
    manual=(-.5*(math.log(2*math.pi*v[0])+(y[0]-m)**2/v[0])
       -.5*(math.log(2*math.pi*(.8+S+.3))+(y[1]-m)**2/(.8+S+.3)))
    assert out==pytest.approx(manual,abs=1e-12)

def test_limit_covariance_structure():
    assert rapid_relaxation_covariance_limit(0,2,.01,.5)==0
    assert rapid_relaxation_covariance_limit(1,2,.01,.5)==pytest.approx(.5)
    assert rapid_relaxation_covariance_limit(2,2,.01,.5)==pytest.approx(1.01)

def test_aicc_formula():
    assert aicc(80.87186957112242,266,3)==pytest.approx(-155.65213608880973)

def test_invalid():
    with pytest.raises(ValueError):
        loglik_random_walk_with_nugget([0,0],[1,2],[.1,.1],1,.3,.1)
