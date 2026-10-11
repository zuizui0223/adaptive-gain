"""Exact Fraction/Bernstein certificate for a benchmark correlation cutoff.

This proof test constructs the two endpoint joint-noise laws independently of
the production law/optimizer. No symbolic algebra package is required by CI.
"""
from fractions import Fraction as F
from itertools import combinations, product
import math

import pytest

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.joint_bitflip_reward import (
    joint_bitflip_law, joint_bitflip_abstention_threshold,
    optimal_joint_bitflip_reward,
)

T=(0,1,1,0,0)
Q=((0,0,1,1,0),(0,1,0,0,0),(0,0,0,1,0))
P=(F(1,3),)+(F(1,6),)*4
E=F(1,10)
INDEP={a:E**sum(a)*(1-E)**(3-sum(a)) for a in product((0,1),repeat=3)}
SHARED={(0,0,0):1-E,(1,1,1):E}


def task():
    return FiniteTask(
        tuple(World(f'w{i}',y) for i,y in enumerate(T)),
        tuple(Query(f'q{j}',1,seq) for j,seq in enumerate(Q)),
    )


def mass_for(target,subset,outcomes,law):
    return sum((P[i]*w for i in range(5) for errors,w in law.items()
                if T[i]==target and
                tuple(Q[j][i]^errors[j] for j in subset)==outcomes),F(0))


def all_histories():
    return ((subset,outcomes,target)
            for length in range(3)
            for subset in combinations(range(3),length)
            for outcomes in product((0,1),repeat=length)
            for target in (0,1))


def test_exact_all_rho_cutoff_via_nonnegative_bernstein_coefficients():
    """All 38 posterior-odds inequalities hold for every rho in [0,1]."""
    audited=0
    sharp=[]
    for subset,observed,target in all_histories():
        gi=mass_for(target,subset,observed,INDEP)
        gs=mass_for(target,subset,observed,SHARED)
        bi=mass_for(1-target,subset,observed,INDEP)
        bs=mass_for(1-target,subset,observed,SHARED)
        def polynomial(rho):
            good=(1-rho)*gi+rho*gs
            bad=(1-rho)*bi+rho*bs
            return (14+rho)*bad-(1-rho)*good
        # A quadratic P(rho) has Bernstein representation
        # b0*(1-rho)^2 + 2*b1*rho*(1-rho) + b2*rho^2.
        # Nonnegative Bernstein coefficients imply P(rho)>=0 on [0,1].
        b0=polynomial(F(0))
        b2=polynomial(F(1))
        b1=2*polynomial(F(1,2))-(b0+b2)/2
        assert min(b0,b1,b2)>=0, (subset,observed,target,b0,b1,b2)
        if (b0,b1,b2)==(0,0,0):
            sharp.append((subset,observed,target,gi,gs,bi,bs))
        audited+=1
    assert audited==38
    # The same accessible history realizes (14+rho)/(1-rho) for all rho<1.
    assert sharp==[((0,1),(0,0),0,F(21,50),F(9,20),F(3,100),F(0))]


@pytest.mark.parametrize('rho',[
    F(0),F(1,100),F(1,10),F(1,4),F(2,7),F(1,2),F(3,4),F(9,10),F(99,100),F(999,1000)
])
def test_production_cutoff_matches_exact_continuous_family(rho):
    law=joint_bitflip_law(3,flip_probability=E,common_mode_fraction=rho)
    expected=(14+rho)/(1-rho)
    actual=joint_bitflip_abstention_threshold(task(),P,budget=2,error_pattern_probabilities=law)
    assert actual==pytest.approx(float(expected),rel=1e-12)


def test_perfect_shared_error_has_infinite_cutoff():
    law=joint_bitflip_law(3,flip_probability=E,common_mode_fraction=1)
    assert joint_bitflip_abstention_threshold(task(),P,budget=2,error_pattern_probabilities=law)==math.inf


def test_correlated_error_rescues_positive_reward_but_not_necessarily_adaptivity():
    # For L/v=20: zero gross payoff iff rho<=2/7; equality is a tie.
    L=20
    for rho,expected_positive in ((F(1,4),False),(F(2,7),False),(F(3,10),True)):
        law=joint_bitflip_law(3,flip_probability=E,common_mode_fraction=rho)
        a=optimal_joint_bitflip_reward(task(),P,budget=2,error_pattern_probabilities=law,error_cost=L)
        n=optimal_joint_bitflip_reward(task(),P,budget=2,error_pattern_probabilities=law,error_cost=L,adaptive=False)
        assert (a>1e-12)==expected_positive
        assert (n>1e-12)==expected_positive
        assert a==pytest.approx(n,abs=1e-12)
