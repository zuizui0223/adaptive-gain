"""Independently enumerate finite trees under joint (possibly correlated) bit errors."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import math

import pytest

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.deadline_noisy_reward import optimal_noisy_deadline_reward
from adaptive_gain.joint_bitflip_reward import (
    joint_bitflip_law,
    optimal_joint_bitflip_reward,
    joint_bitflip_abstention_threshold,
)

TARGETS=(0,1,1,0,0)
CUES={
    "A":((0,0,1,1,0),(0,1,0,0,0),(0,0,0,1,0)),
    "B":((1,0,0,0,0),(0,0,0,1,0),(1,1,1,1,0)),
}
PRIOR=(F(1,3),)+(F(1,6),)*4
EPS=F(1,10)


def task(name="A"):
    return FiniteTask(
        tuple(World(f"w{i}",t) for i,t in enumerate(TARGETS)),
        tuple(Query(f"q{j}",1,c) for j,c in enumerate(CUES[name])),
    )


def law_independent():
    return {e:EPS**sum(e)*(1-EPS)**(3-sum(e)) for e in product((0,1),repeat=3)}


def law_shared():
    return {(0,0,0):1-EPS,(1,1,1):EPS}


def law_mixed(rho):
    return {e:(1-rho)*law_independent()[e]+rho*law_shared().get(e,0)
            for e in product((0,1),repeat=3)}


def full_response_rows(t,law):
    rows=[]
    for i,world in enumerate(t.worlds):
        for err,prob in law.items():
            if prob:
                bits=tuple(t.queries[j].outcomes[i]^err[j] for j in range(len(t.queries)))
                rows.append((world.target,bits,PRIOR[i]*prob))
    assert sum((mass for _,_,mass in rows),F(0)) == 1
    return rows


@lru_cache(None)
def trees(unused,budget):
    result=[None]
    for j in unused:
        if budget>=1:
            children=trees(tuple(k for k in unused if k!=j),budget-1)
            result.extend((j,left,right) for left,right in product(children,repeat=2))
    return tuple(result)


def path(t,observed):
    route=[]
    while t is not None:
        j,left,right=t
        bit=observed[j]
        route.append((j,bit))
        t=right if bit else left
    return tuple(route)


def partition_reward(rows,by,L):
    groups={}
    for target,bits,weight in rows:
        group=groups.setdefault(by(bits),{0:F(0),1:F(0)})
        group[target]+=weight
    return sum((max(F(0),g[0]-L*g[1],g[1]-L*g[0]) for g in groups.values()),F(0))


def oracle(t,law,L,budget,adaptive):
    rows=full_response_rows(t,law)
    if adaptive:
        return max(partition_reward(rows,lambda x,tr=tr:path(tr,x),L)
                   for tr in trees(tuple(range(len(t.queries))),budget))
    return max(partition_reward(rows,lambda x,sub=sub:tuple(x[j] for j in sub),L)
               for k in range(min(budget,len(t.queries))+1)
               for sub in combinations(range(len(t.queries)),k))


def test_joint_law_preserves_all_univariate_error_marginals():
    for rho in (F(0),F(1,10),F(1,2),F(9,10),F(1)):
        law=joint_bitflip_law(3,flip_probability=EPS,common_mode_fraction=rho)
        assert sum((F(value) for value in law.values()),F(0)) == 1
        for j in range(3):
            assert sum((F(m) for e,m in law.items() if e[j]),F(0)) == EPS
        for j,k in ((0,1),(1,2),(0,2)):
            joint=sum((F(m) for e,m in law.items() if e[j] and e[k]),F(0))
            corr=(joint-EPS*EPS)/(EPS*(1-EPS))
            assert corr == rho


@pytest.mark.parametrize("name",("A","B"))
@pytest.mark.parametrize("rho",(F(0),F(1,2),F(1)))
@pytest.mark.parametrize("L",(F(0),F(1),F(4),F(20)))
@pytest.mark.parametrize("budget",(0,1,2))
def test_independent_fraction_oracle_across_joint_noise(name,rho,L,budget):
    t=task(name)
    pattern=law_mixed(rho)
    actual_law=joint_bitflip_law(3,flip_probability=EPS,common_mode_fraction=rho)
    for adaptive in (False,True):
        expected=oracle(t,pattern,L,budget,adaptive)
        actual=optimal_joint_bitflip_reward(t,PRIOR,budget=budget,error_pattern_probabilities=actual_law,
                                            error_cost=L,adaptive=adaptive)
        assert actual == pytest.approx(float(expected),abs=1e-12)


@pytest.mark.parametrize("name",("A","B"))
@pytest.mark.parametrize("loss",(0,1,4,14,20))
@pytest.mark.parametrize("budget",range(4))
@pytest.mark.parametrize("adaptive",(False,True))
def test_independent_channel_recovers_existing_model(name,loss,budget,adaptive):
    law=joint_bitflip_law(3,flip_probability=EPS,common_mode_fraction=0)
    t=task(name)
    want=optimal_noisy_deadline_reward(t,PRIOR,budget=budget,flip_probability=EPS,error_cost=loss,adaptive=adaptive)
    got=optimal_joint_bitflip_reward(t,PRIOR,budget=budget,error_pattern_probabilities=law,
                                      error_cost=loss,adaptive=adaptive)
    assert got == pytest.approx(want,abs=1e-12)


def test_equal_marginal_accuracy_different_evolutionary_repayment():
    t=task("A")
    out=[]
    for rho in (F(0),F(1)):
        law=joint_bitflip_law(3,flip_probability=EPS,common_mode_fraction=rho)
        aa=optimal_joint_bitflip_reward(t,PRIOR,budget=2,error_pattern_probabilities=law,error_cost=4)
        na=optimal_joint_bitflip_reward(t,PRIOR,budget=2,error_pattern_probabilities=law,error_cost=4,adaptive=False)
        out.append(aa-na)
    assert out == pytest.approx((float(F(11,150)),float(F(7,30))))
    maintenance=.1
    assert out[0] < maintenance < out[1]


def test_high_loss_does_not_erase_correlated_certificate():
    t=task("A")
    independent=joint_bitflip_law(3,flip_probability=EPS,common_mode_fraction=0)
    shared=joint_bitflip_law(3,flip_probability=EPS,common_mode_fraction=1)
    assert joint_bitflip_abstention_threshold(t,PRIOR,budget=2,error_pattern_probabilities=independent) == pytest.approx(14)
    assert joint_bitflip_abstention_threshold(t,PRIOR,budget=2,error_pattern_probabilities=shared) == math.inf
    for L in (F(20),F(100),F(10000)):
        assert optimal_joint_bitflip_reward(t,PRIOR,budget=2,error_pattern_probabilities=independent,error_cost=L) == 0
        assert optimal_joint_bitflip_reward(t,PRIOR,budget=2,error_pattern_probabilities=shared,error_cost=L) == pytest.approx(.6)
        assert optimal_joint_bitflip_reward(t,PRIOR,budget=2,error_pattern_probabilities=shared,error_cost=L,adaptive=False) == pytest.approx(.5)


def test_full_support_mixture_restores_finite_cutoff():
    t=task("A")
    for rho,expected in ((F(0),F(14)),(F(1,10),F(47,3)),(F(1,2),F(29)),(F(9,10),F(149))):
        law=joint_bitflip_law(3,flip_probability=EPS,common_mode_fraction=rho)
        c=joint_bitflip_abstention_threshold(t,PRIOR,budget=2,error_pattern_probabilities=law)
        assert c == pytest.approx(float(expected),abs=1e-9)
        assert optimal_joint_bitflip_reward(t,PRIOR,budget=2,error_pattern_probabilities=law,error_cost=c+1) == 0


@pytest.mark.parametrize("law",[
    {(0,0,0):F(1,2)},
    {(0,0,0):F(3,4),(1,1,1):F(1,2)},
    {(0,0,0):-1,(1,1,1):2},
    {(0,0):1},
    {(0,0,2):1},
    {},
])
def test_bad_joint_law_rejected(law):
    with pytest.raises(ValueError):
        optimal_joint_bitflip_reward(task("A"),PRIOR,budget=2,error_pattern_probabilities=law)


@pytest.mark.parametrize("kwargs",[
    {"budget":-1},{"budget":True},{"adaptive":1},{"error_cost":-1},
    {"correct_reward":0},{"correct_reward":math.nan},
])
def test_bad_arguments_rejected(kwargs):
    d={"budget":2}
    d.update(kwargs)
    with pytest.raises(ValueError):
        optimal_joint_bitflip_reward(task("A"),PRIOR,error_pattern_probabilities=law_shared(),**d)


def test_no_cues_joint_law_has_one_empty_pattern_and_prior_action_only():
    t=FiniteTask((World('w0',0),World('w1',1)),())
    law=joint_bitflip_law(0,flip_probability=EPS,common_mode_fraction=F(1,2))
    assert law == {():1}
    assert optimal_joint_bitflip_reward(t,(F(2,3),F(1,3)),budget=0,
                                        error_pattern_probabilities=law,error_cost=2) == 0
