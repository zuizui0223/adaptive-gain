import math
import pytest
from adaptive_gain.ou_sampling_saturation import (
    finite_moving_ou_covariance,rapid_relaxation_covariance_limit
)

@pytest.mark.parametrize("s,t",[(0.1,0.1),(0.1,1.5),(1.5,0.1),(1.,1.),(0.,2.)])
def test_high_alpha_limit(s,t):
    S,vo=.01476924189464519,2.5206495950619603
    got=finite_moving_ou_covariance(s,t,1e7,S,vo)
    expected=rapid_relaxation_covariance_limit(s,t,S,vo)
    assert got==pytest.approx(expected,abs=2e-6,rel=2e-6)

def test_symmetric_and_nugget():
    a=finite_moving_ou_covariance(.01,.1,1000,.015,2.5)
    b=finite_moving_ou_covariance(.1,.01,1000,.015,2.5)
    assert a==pytest.approx(b)
    assert rapid_relaxation_covariance_limit(.1,.1,.015,2.5)==pytest.approx(.265)
    assert rapid_relaxation_covariance_limit(.1,.2,.015,2.5)==pytest.approx(.25)

@pytest.mark.parametrize("args",[(0,1,-1,.1,1),(1,2,1,-.1,1),(1,2,1,.1,-1)])
def test_invalid(args):
    with pytest.raises(ValueError):
        finite_moving_ou_covariance(*args)
