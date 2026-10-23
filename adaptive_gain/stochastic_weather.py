"""Exact Markov-weather stochastic-deadline adaptive information routing.

Synthetic ecological-decision system, NOT an empirical wind effect or species
interaction. Branch B uniform in 2^d resources, binary target T uniform and
independent. Flowers emit 1 iff (B=flower_index AND T=1). Other species cues
supply distinct bits of B under conditionally independent-of-T errors.

An observed wind state controls source acquisition cost and the per-time-tick
hazard that the encounter ends. Q=diag(survival) R is a sub-stochastic wind
transition matrix. A query requiring c ticks has completion kernel Q**c;
if interrupted it gives no information and the subject guesses at the deadline.
All probabilities and optimization results use Fraction, not Monte Carlo.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from math import lcm


def validate_weather(survival, stay, initial):
    survival=tuple(F(x) for x in survival)
    stay=F(stay)
    initial=tuple(F(x) for x in initial)
    if len(survival)!=2 or any(not 0<=s<=1 for s in survival):
        raise ValueError('calm/gust survival must each lie in [0,1]')
    if not 0<=stay<=1:
        raise ValueError('wind persistence must lie in [0,1]')
    if len(initial)!=2 or any(x<0 for x in initial) or sum(initial)!=1:
        raise ValueError('starting wind probabilities must be normalized')
    return survival,stay,initial


def weather_kernel(survival=(F(19,20),F(13,20)),stay=F(1,2)):
    survival,stay,_=validate_weather(survival,stay,(F(1,2),F(1,2)))
    a,b=survival
    return ((a*stay,a*(1-stay)),(b*(1-stay),b*stay))


def kernel_powers(Q,K):
    """2×2 matrix powers 0..K as exact survival-and-weather kernels."""
    A=((F(1),F(0)),(F(0),F(1)))
    out=[A]
    for i in range(K):
        A=tuple(tuple(sum((A[j][h]*Q[h][k] for h in (0,1)),F(0))
                      for k in (0,1)) for j in (0,1))
        out.append(A)
    return tuple(out)


def _validate_task(d,budget,bits,source_costs,error,joint):
    if type(d) is not int or not 2<=d<=5:
        raise ValueError('d must be integer 2..5')
    if type(budget) is not int or not 0<=budget<=16:
        raise ValueError('budget must be integer 0..16')
    bits=tuple(bits)
    if len(bits)>2 or len(set(bits))!=len(bits) or any(type(k) is not int or not 0<=k<d for k in bits):
        raise ValueError('must provide up to two distinct habitat bit indices')
    costs=tuple(tuple(x for x in row) for row in source_costs)
    if len(costs)!=2 or any(len(x)!=len(bits) for x in costs):
        raise ValueError('one acquisition cost per cue for both weather states')
    if any(type(c) is not int or c<1 for row in costs for c in row):
        raise ValueError('source cue costs must be positive integers')
    e=F(error)
    q=e*e if joint is None else F(joint)
    if not (0<=e<=F(1,2) and max(F(0),2*e-1)<=q<=e):
        raise ValueError('invalid correlated two-source noise distribution')
    return bits,costs,e,q


def optimal_accuracy(d,budget,bits=(),error=F(1,10),joint=None,
                     source_costs=((),()),
                     survival=(F(19,20),F(13,20)),stay=F(1,2),
                     initial=(F(1,2),F(1,2)),stats=False):
    """Bayes-optimal correct decision, with observed Markov wind and termination.

    History compressed to 2^r groups: branch states are exchangeable within
    each source-bit group because of uniform resource prior and identical flower
    cost/reward. The DP maximizes surplus successes for T=1 after a positive
    flower observation, while T=0 remains a weakly dominant stopping guess.

    A source observation gives only a branch bit; even the joint distribution
    of two cues is independent of the profitable target T. Source acquisition
    is useful only by conditioning subsequent flower queries on outcomes.
    """
    bits,costs,e,q=_validate_task(d,budget,bits,source_costs,error,joint)
    survival,stay,initial=validate_weather(survival,stay,initial)
    n=1<<d; r=len(bits); n_groups=1<<r; each=n//n_groups
    noise=(1-2*e+q,e-q,e-q,q)
    denom=lcm(*(p.denominator for p in noise))
    integer_mass=tuple(int(p*denom) for p in noise)
    kernel=kernel_powers(weather_kernel(survival,stay),budget)

    @lru_cache(None)
    def mass_for_group(read,observed):
        out=[]
        for g in range(n_groups):
            val=0
            for hidden_noise,weight in enumerate(integer_mass):
                if all(not read&(1<<sid) or
                    (((g>>sid)&1)^((hidden_noise>>sid)&1))==((observed>>sid)&1)
                    for sid in range(r)):
                    val+=weight
            out.append(val)
        return tuple(out)

    @lru_cache(None)
    def recurse(counts,read,observed,wind,left):
        if left<=0:
            return F(0)
        masses=mass_for_group(read,observed)
        best=F(0)
        # Query one recorded-flowering alternative, unit cost, if not previously tested.
        for g,count in enumerate(counts):
            if count>=each:continue
            newer=list(counts);newer[g]+=1;newer=tuple(newer)
            score=sum((kernel[1][wind][w2]*(masses[g]+recurse(newer,read,observed,w2,left-1))
                       for w2 in (0,1)),F(0))
            if score>best:best=score
        # Observe another species' habitat signal (not the flower's payoff).
        for sid in range(r):
            if read&(1<<sid):continue
            c=costs[wind][sid]
            if c>left:continue
            updated=read|(1<<sid)
            low=observed&~(1<<sid)
            high=observed|(1<<sid)
            score=sum((kernel[c][wind][w2]*(
                recurse(counts,updated,low,w2,left-c)
                +recurse(counts,updated,high,w2,left-c)) for w2 in (0,1)),F(0))
            if score>best:best=score
        return best

    start=(0,)*n_groups
    bonus=sum((initial[w]*recurse(start,0,0,w,budget) for w in (0,1)),F(0))
    answer=F(1,2)+bonus/(2*n*denom)
    if stats:
        return answer,{'states':recurse.cache_info().currsize,
            'mass_states':mass_for_group.cache_info().currsize,
            'source_noise_denominator':denom,
            'n_worlds':2*n,'n_groups':n_groups,'each_group':each}
    return answer


def fixed_accuracy(d,budget,survival=(F(19,20),F(13,20)),
                   stay=F(1,2),initial=(F(1,2),F(1,2))):
    """Precommitted distinct-flower policy; source cues cannot help a fixed order."""
    _validate_task(d,budget,(),((),()),F(0),None)
    survival,stay,initial=validate_weather(survival,stay,initial)
    M=kernel_powers(weather_kernel(survival,stay),min(budget,1<<d))
    total=F(0)
    for tick in range(1,min(budget,1<<d)+1):
        total+=sum((initial[w]*sum(M[tick][w],F(0)) for w in (0,1)),F(0))
    return F(1,2)+total/(2*(1<<d))


def four_contexts(d,budget,stay,*,error=F(1,10),
                  survival=(F(19,20),F(13,20)),initial=(F(1,2),F(1,2))):
    scenarios={
        'none':((),((),())),
        'A':((0,),((1,),(1,))),
        'B':((1,),((1,),(2,))),
        'AB':((0,1),((1,1),(1,2))),
    }
    answers={}
    for name,(bits,costs) in scenarios.items():
        answers[name]=optimal_accuracy(d,budget,bits,error,
                                     source_costs=costs,survival=survival,
                                     stay=stay,initial=initial)
    ans=answers
    ans['interaction']=ans['AB']-ans['A']-ans['B']+ans['none']
    ans['fixed']=fixed_accuracy(d,budget,survival,stay,initial)
    ans['conditional_advantage']=ans['AB']-ans['fixed']
    return ans


def full_grid():
    rows=[]
    for K in (5,7):
        for p in (F(1,10),F(1,2),F(9,10)):
            context=four_contexts(4,K,p)
            for name in ('none','A','B','AB'):
                rows.append({'K':K,'stay':str(p),'cue':name,
                             'accuracy':str(context[name]),
                             'interaction':str(context['interaction']),
                             'fixed':str(context['fixed']),
                             'conditional_advantage':str(context['conditional_advantage'])})
    return rows


if __name__=='__main__':
    import json
    v=full_grid()
    print(json.dumps(v,ensure_ascii=False,indent=2))