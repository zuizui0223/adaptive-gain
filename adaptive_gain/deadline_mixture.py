"""Exact finite Bayesian routing when the exogenous opportunity deadline is hidden.

32-world demonstration. Independent of wind/branch/target, a hard K is drawn
and not announced; only survival after each query is observed. Fraction exact.
No actual species interactions or pollen fitness are estimated.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import lcm
from .stochastic_weather import _validate_task,validate_weather,weather_kernel,kernel_powers,optimal_accuracy,fixed_accuracy

def _deadlines(distribution):
    raw=tuple((k,F(p)) for k,p in distribution)
    if not raw or any(type(k)!=int or not 0<=k<=16 or p<0 for k,p in raw) or sum((p for _,p in raw),F(0))!=1:
        raise ValueError("deadlines must form a probability distribution on integer K=0..16")
    merged={}
    for k,p in raw:merged[k]=merged.get(k,F(0))+p
    return tuple(sorted((k,p) for k,p in merged.items() if p))

def announced_deadline_accuracy(distribution,d=4,bits=(),error=F(1,10),joint=None,
                               source_costs=((),()),survival=(F(19,20),F(13,20)),
                               stay=F(1,2),initial=(F(1,2),F(1,2))):
    return sum((pr*optimal_accuracy(d,k,bits,error,joint,source_costs,survival,stay,initial)
                for k,pr in _deadlines(distribution)),F(0))

def hidden_deadline_accuracy(distribution,d=4,bits=(),error=F(1,10),joint=None,
                            source_costs=((),()),survival=(F(19,20),F(13,20)),
                            stay=F(1,2),initial=(F(1,2),F(1,2)),stats=False):
    dist=_deadlines(distribution)
    Kmax=max(k for k,_ in dist)
    bits,costs,e,q=_validate_task(d,Kmax,bits,source_costs,error,joint)
    survival,stay,initial=validate_weather(survival,stay,initial)
    n=1<<d;r=len(bits);groups=1<<r;group_size=n//groups
    latent_mass=(1-2*e+q,e-q,e-q,q)
    D=lcm(*(v.denominator for v in latent_mass))
    mass_int=tuple(int(v*D) for v in latent_mass)
    Q=kernel_powers(weather_kernel(survival,stay),Kmax)
    cap=tuple(sum((p for k,p in dist if k>=t),F(0)) for t in range(Kmax+1))
    @lru_cache(None)
    def belief(read,seen):
        out=[]
        for g in range(groups):
            mass=0
            for noise,v in enumerate(mass_int):
                if all(not read&(1<<i) or
                       (((g>>i)&1)^((noise>>i)&1))==((seen>>i)&1) for i in range(r)):
                    mass+=v
            out.append(mass)
        return tuple(out)
    @lru_cache(None)
    def solve(used,read,seen,wind,t):
        if t>=Kmax or cap[t]==0:return F(0)
        mass=belief(read,seen);best=F(0)
        future=cap[t+1]/cap[t]
        for g,nused in enumerate(used):
            if nused>=group_size:continue
            nxt=list(used);nxt[g]+=1;nxt=tuple(nxt)
            value=sum((future*Q[1][wind][w]*(mass[g]+solve(nxt,read,seen,w,t+1))
                       for w in (0,1)),F(0))
            best=max(best,value)
        for sid in range(r):
            if read&(1<<sid):continue
            c=costs[wind][sid]
            if t+c>Kmax or cap[t+c]==0:continue
            scale=cap[t+c]/cap[t]
            newread=read|(1<<sid)
            low=seen&~(1<<sid);high=seen|(1<<sid)
            value=sum((scale*Q[c][wind][w]*(
                solve(used,newread,low,w,t+c)+solve(used,newread,high,w,t+c))
                       for w in (0,1)),F(0))
            best=max(best,value)
        return best
    surplus=sum((initial[w]*solve((0,)*groups,0,0,w,0) for w in (0,1)),F(0))
    answer=F(1,2)+surplus/(2*n*D)
    return (answer,{'states':solve.cache_info().currsize}) if stats else answer

def fixed_deadline_mixture(distribution,d=4,
                           survival=(F(19,20),F(13,20)),stay=F(1,2),
                           initial=(F(1,2),F(1,2))):
    return sum((p*fixed_accuracy(d,k,survival,stay,initial)
                for k,p in _deadlines(distribution)),F(0))

def mixed_contexts(d=4,distribution=((3,F(1,2)),(7,F(1,2))),*,error=F(1,10),
                   joint=None,survival=(F(19,20),F(13,20)),
                   stay=F(1,2),initial=(F(1,2),F(1,2))):
    configurations={
       'none':((),((),())),
       'A':((0,),((1,),(1,))),
       'B':((1,),((1,),(2,))),
       'AB':((0,1),((1,1),(1,2))),
    }
    outputs={}
    for name,solver in [('announced',announced_deadline_accuracy),('hidden',hidden_deadline_accuracy)]:
        out={key:solver(distribution,d,bits,error,joint,costs,survival,stay,initial)
             for key,(bits,costs) in configurations.items()}
        out['interaction']=out['AB']-out['A']-out['B']+out['none']
        out['fixed']=fixed_deadline_mixture(distribution,d,survival,stay,initial)
        out['adaptive_minus_fixed']=out['AB']-out['fixed']
        outputs[name]=out
    return outputs
