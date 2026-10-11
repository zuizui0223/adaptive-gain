"""Independent full response-table audit of a noisy finite cue model.

Mutations caught: deterministic filtering of noisy evidence, adaptive queries
chosen from true rather than perceived cues, wrong fixed-subset comparator,
missing stop option, and incorrect shared all-abstention threshold.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import math

import pytest
from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.deadline_reward import optimal_deadline_expected_reward

TARGETS = (0, 1, 1, 0, 0)
CUES = {
    'A': ((0,0,1,1,0), (0,1,0,0,0), (0,0,0,1,0)),
    'B': ((1,0,0,0,0), (0,0,0,1,0), (1,1,1,1,0)),
}


def make_task(name, costs=(1,1,1)):
    return FiniteTask(tuple(World(str(i), t) for i,t in enumerate(TARGETS)),
                      tuple(Query(str(j), costs[j], x) for j,x in enumerate(CUES[name])))


def prior(t=F(1,3)):
    return (t,)+((1-t)/4,)*4


def reward(*args, **kwargs):
    from adaptive_gain.deadline_noisy_reward import optimal_noisy_deadline_reward
    return optimal_noisy_deadline_reward(*args, **kwargs)


def cutoff(*args, **kwargs):
    from adaptive_gain.deadline_noisy_reward import noisy_deadline_abstention_threshold
    return noisy_deadline_abstention_threshold(*args, **kwargs)


def full_response_table(task, probabilities, error):
    """Latent state x FULL perceived cue vector, with exact rational mass."""
    rows = []
    for i, state in enumerate(task.worlds):
        for response in product((0,1), repeat=len(task.queries)):
            mass = probabilities[i]
            for j,z in enumerate(response):
                mass *= (1-error) if z == task.queries[j].outcomes[i] else error
            if mass:
                rows.append((state.target, response, mass))
    assert sum((r[2] for r in rows), F(0)) == 1
    return rows


@lru_cache(None)
def query_trees(costs, available, budget):
    # None = stop. The tree is chosen without any access to a true state.
    result = [None]
    for j in available:
        if costs[j] > budget:
            continue
        children = query_trees(costs, tuple(k for k in available if k != j), budget-costs[j])
        result.extend((j,left,right) for left,right in product(children, repeat=2))
    return tuple(result)


def leaf_for(tree, response):
    path = []
    while tree is not None:
        j,left,right = tree
        observed = response[j]
        path.append((j,observed))
        tree = right if observed else left
    return tuple(path)


def class_masses(rows, grouping):
    groups = {}
    for target, response, mass in rows:
        k = grouping(response)
        masses = groups.setdefault(k,{})
        masses[target] = masses.get(target,F(0)) + mass
    return groups.values()


def independent_values(task, probabilities, error, budget, losses):
    """Enumerate full query trees and fixed subsets, score terminal Bayes actions.

    This does not propagate posteriors or reuse production DP/likelihood code.
    """
    rows = full_response_table(task, probabilities, error)
    costs = tuple(q.cost for q in task.queries)
    trees = query_trees(costs, tuple(range(len(costs))), budget)
    adaptive_groups = [tuple(class_masses(rows, lambda x,t=t: leaf_for(t,x))) for t in trees]
    fixed_groups = []
    for size in range(len(costs)+1):
        for subset in combinations(range(len(costs)),size):
            if sum(costs[j] for j in subset) <= budget:
                fixed_groups.append(tuple(class_masses(rows,lambda x,s=subset: tuple(x[j] for j in s))))
    def score(groups, loss):
        total = F(0)
        for masses in groups:
            all_mass = sum(masses.values(),F(0))
            total += max(F(0), max(c-loss*(all_mass-c) for c in masses.values()))
        return total
    return {adaptive: tuple(max(score(g,l) for g in groups) for l in losses)
            for adaptive,groups in ((True,adaptive_groups),(False,fixed_groups))}


def test_feature_and_zero_noise_recovery():
    task, p = make_task('A'), prior()
    assert reward(task,p,budget=2,flip_probability=0,error_cost=2) == pytest.approx(1)
    for a in (False,True):
        for b in range(4):
            for l in (0,0.5,1,3,10):
                old = optimal_deadline_expected_reward(task,p,budget=b,error_cost=l,adaptive=a)
                assert reward(task,p,budget=b,flip_probability=0,error_cost=l,adaptive=a) == pytest.approx(old)


@pytest.mark.parametrize('name',('A','B'))
@pytest.mark.parametrize('t',(F(1,5),F(1,3),F(4,5)))
@pytest.mark.parametrize('error',(F(0),F(1,20),F(1,10),F(1,2)))
@pytest.mark.parametrize('budget',range(4))
def test_matches_exhaustive_fraction_response_oracle(name,t,error,budget):
    task,p = make_task(name),prior(t)
    losses = (F(0),F(1,2),F(1),F(3),F(10),F(100))
    exact = independent_values(task,p,error,budget,losses)
    for a in (False,True):
        for l,want in zip(losses,exact[a]):
            actual = reward(task,p,budget=budget,flip_probability=error,error_cost=l,adaptive=a)
            assert actual == pytest.approx(float(want),abs=5e-12)


@pytest.mark.parametrize('name',('A','B'))
@pytest.mark.parametrize('error',(F(1,20),F(1,10),F(1,2)))
@pytest.mark.parametrize('budget',range(4))
def test_shared_finite_zero_reward_threshold(name,error,budget):
    task,p=make_task(name),prior()
    r=cutoff(task,p,budget=budget,flip_probability=error)
    assert math.isfinite(r) and r > 0
    for a in (False,True):
        assert reward(task,p,budget=budget,flip_probability=error,error_cost=r,adaptive=a) == pytest.approx(0,abs=1e-12)
        assert reward(task,p,budget=budget,flip_probability=error,error_cost=r+1,adaptive=a) == 0
        assert reward(task,p,budget=budget,flip_probability=error,error_cost=r*0.99,adaptive=a) > 0


def test_completely_uninformative_cues_equal_no_observation():
    p=prior()
    for name,b,l,a in product(('A','B'),range(4),(0,1,4),(False,True)):
        want=max(0,2/3-l/3)
        assert reward(make_task(name),p,budget=b,flip_probability=.5,error_cost=l,adaptive=a) == pytest.approx(want)


def test_binary_noiseless_certification_has_infinite_cutoff():
    assert cutoff(make_task('A'),prior(),budget=2,flip_probability=0) == math.inf


def test_unequal_costs_match_response_oracle():
    task,p=make_task('A',costs=(2,1,3)),prior()
    losses=(F(0),F(2),F(7))
    exact=independent_values(task,p,F(1,10),3,losses)
    for a in (False,True):
        for l,want in zip(losses,exact[a]):
            assert reward(task,p,budget=3,flip_probability=.1,error_cost=l,adaptive=a) == pytest.approx(float(want),abs=1e-12)


def test_reward_units_and_pure_targets():
    task,p=make_task('A'),prior()
    assert reward(task,p,budget=2,flip_probability=.1,correct_reward=2,error_cost=6) == pytest.approx(
        2*reward(task,p,budget=2,flip_probability=.1,error_cost=3))
    pure=FiniteTask((World('a',0),),())
    assert reward(pure,(1,),budget=0,flip_probability=.1,error_cost=100) == 1
    assert cutoff(pure,(1,),budget=0,flip_probability=.1) == math.inf


@pytest.mark.parametrize('kwargs',({'budget':-1},{'budget':True},{'flip_probability':-.01},
    {'flip_probability':.51},{'flip_probability':math.nan},{'error_cost':-1},
    {'error_cost':math.inf},{'correct_reward':0},{'adaptive':1}))
def test_invalid_parameters_rejected(kwargs):
    options={'budget':2,'flip_probability':.1}; options.update(kwargs)
    with pytest.raises(ValueError): reward(make_task('A'),prior(),**options)


def test_nonbinary_query_rejected():
    task=FiniteTask((World('0',0),World('1',1)),(Query('bad',1,(0,2)),))
    with pytest.raises(ValueError): reward(task,(.5,.5),budget=1,flip_probability=.1)


def reward_lines(task,p,e,budget,adaptive):
    """ALL deterministic terminal-action choices as exact (correct,error) lines."""
    rows=full_response_table(task,p,e)
    costs=tuple(q.cost for q in task.queries)
    if adaptive:
        partitions=[tuple(class_masses(rows,lambda x,t=t:leaf_for(t,x)))
                    for t in query_trees(costs,tuple(range(len(costs))),budget)]
    else:
        partitions=[]
        for size in range(len(costs)+1):
            for subset in combinations(range(len(costs)),size):
                if sum(costs[j] for j in subset)<=budget:
                    partitions.append(tuple(class_masses(rows,lambda x,s=subset:tuple(x[j] for j in s))))
    lines=set()
    for groups in partitions:
        options=[]
        for masses in groups:
            total=sum(masses.values(),F(0))
            options.append([(F(0),F(0))]+[(c,total-c) for c in masses.values()])
        for choice in product(*options):
            lines.add((sum((c for c,e in choice),F(0)),sum((e for c,e in choice),F(0))))
    return lines


# These lists describe expected-value lines C-L*E and their exact start points.
# Verification below proves dominance on WHOLE intervals, not only a grid.
A_HULL=((F(0),F(127,150),F(23,150)),
        (F(5,2),F(209,300),F(7,75)),
        (F(41,14),F(14,25),F(7,150)),
        (F(42,5),F(21,50),F(3,100)),
        (F(14),F(0),F(0)))
F_HULL=((F(0),F(77,100),F(23,100)),
        (F(6,5),F(3,4),F(16,75)),
        (F(7,5),F(44,75),F(29,300)),
        (F(3,2),F(167,300),F(23,300)),
        (F(41,14),F(21,50),F(3,100)),
        (F(14),F(0),F(0)))


@pytest.mark.parametrize('adaptive,hull,count',((True,A_HULL,391),(False,F_HULL,208)))
def test_exact_all_loss_envelope_certificate(adaptive,hull,count):
    task,p,e=make_task('A'),prior(),F(1,10)
    lines=reward_lines(task,p,e,2,adaptive)
    assert len(lines)==count
    for i,(lo,costless,error) in enumerate(hull):
        assert (costless,error) in lines
        hi=hull[i+1][0] if i+1<len(hull) else None
        # A linear function dominates another throughout a bounded interval
        # iff it dominates both ends. On the final ray all slopes are <= 0.
        for point in ((lo,hi) if hi is not None else (lo,)):
            assert all(costless-point*error >= c-point*err for c,err in lines)
            assert reward(task,p,budget=2,flip_probability=e,error_cost=point,adaptive=adaptive) == pytest.approx(float(costless-point*error),abs=2e-12)
        if hi is None:
            assert costless==error==0 and all(err>=0 for _,err in lines)


def hull_value(hull,loss):
    return max(c-loss*e for _,c,e in hull)


def test_exact_controller_viability_band_and_three_distinct_boundaries():
    K=F(1,10)
    lo,hi=F(7,23),F(57,23)
    cuts=sorted({x for h in (A_HULL,F_HULL) for x,_,_ in h}|{lo,hi})
    for a,b in zip(cuts,cuts[1:]+[cuts[-1]+1]):
        mid=(a+b)/2
        net=hull_value(A_HULL,mid)-hull_value(F_HULL,mid)-K
        assert (net>0)==(lo<mid<hi)
    for boundary in (lo,hi):
        assert hull_value(A_HULL,boundary)-hull_value(F_HULL,boundary)==K
    # Added value vanishes before both classes' gross value vanishes.
    assert hull_value(A_HULL,F(42,5))==hull_value(F_HULL,F(42,5))>0
    assert hull_value(A_HULL,F(14))==hull_value(F_HULL,F(14))==0
    premium_at_knots=[hull_value(A_HULL,x)-hull_value(F_HULL,x) for x in cuts]
    assert max(premium_at_knots)==F(271,1500)
    assert hull_value(A_HULL,F(7,5))-hull_value(F_HULL,F(7,5))==F(271,1500)


@pytest.mark.parametrize('name',('A','B'))
def test_exact_max_posterior_odds_from_19_affordable_histories(name):
    task,p,e=make_task(name),prior(),F(1,10)
    rows=full_response_table(task,p,e)
    odds=[]
    for size in range(3):
        for subset in combinations(range(3),size):
            groups=class_masses(rows,lambda x,s=subset:tuple(x[j] for j in s))
            for masses in groups:
                total=sum(masses.values(),F(0))
                assert len(masses)==2  # No exact certification with full-support noise.
                odds.append(max(c/(total-c) for c in masses.values()))
    assert len(odds)==19
    assert max(odds)==F(14)
    assert cutoff(task,p,budget=2,flip_probability=e)==pytest.approx(14)


def test_extreme_underflow_does_not_create_false_certainty():
    with pytest.raises(ArithmeticError,match='underflow'):
        cutoff(make_task('A'),prior(),budget=3,flip_probability=1e-200)


@pytest.mark.parametrize('p',((.25,)*4,(.1,)*5,(0,.25,.25,.25,.25),(math.nan,.2,.2,.2,.2)))
def test_invalid_probabilities_rejected(p):
    for f in (reward,cutoff):
        with pytest.raises(ValueError): f(make_task('A'),p,budget=2,flip_probability=.1)
