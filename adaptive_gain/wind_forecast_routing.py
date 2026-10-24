"""Weather lookahead and other-species cue routing, exactly optimized.

Constructed ecological Bayesian counterfactual, NOT a field-measured wind effect.
Next-step wind forecast Z has zero mutual information about profitable target.
The current wind is observable. A free forecast predicts weather after the
next wind-transition tick with BSC error, separately before EACH new query.
A c-tick cue obtains data only if all c opportunity ticks survive; its forecast-
conditional completion kernel is H_z * Q**(c-1), preserving the original
sub-stochastic Markov survival process when summing over forecasts.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction as F
from math import lcm
from collections import deque

from .deadline_mixture import _deadlines
from .stochastic_weather import _validate_task,validate_weather,weather_kernel,kernel_powers


def forecast_joint_kernel(c,forecast_error,Q,powers):
    """Joint P(forecast z, complete c-tick query, end-weather) matrices."""
    e=F(forecast_error)
    if type(c) is not int or c<1 or c>=len(powers) or not 0<=e<=F(1,2):
        raise ValueError("invalid forecast error or acquisition duration")
    return tuple(tuple(tuple(sum((
         Q[w][v]*(1-e if z==v else e)*powers[c-1][v][end]
         for v in (0,1)),F(0)) for end in (0,1))
         for w in (0,1)) for z in (0,1))


def forecast_accuracy(distribution,d=4,bits=(),error=F(1,10),joint=None,
       source_costs=((),()),survival=(F(19,20),F(13,20)),
       stay=F(1,2),initial=(F(1,2),F(1,2)),
       forecast_error=F(1,2),stats=False):
    """Bayesian maximum P(correct T) at an unknown hard cap and wind hazard.

    Exactly optimizes after every new weather forecast and after all previous
    source cue outcomes. A positive flower response identifies T=1; a failed
    acquisition or a stop guesses T=0 (weakly Bayes optimal in this family).
    """
    distribution=_deadlines(distribution)
    Kmax=max(k for k,_ in distribution)
    bits,costs,e,q=_validate_task(d,Kmax,bits,source_costs,error,joint)
    survival,stay,initial=validate_weather(survival,stay,initial)
    fe=F(forecast_error)
    if not 0<=fe<=F(1,2):raise ValueError("forecast error must be in [0,1/2]")
    n=1<<d;r=len(bits);n_groups=1<<r;per_group=n//n_groups
    latent=(1-2*e+q,e-q,e-q,q)
    D=lcm(*(v.denominator for v in latent))
    noise=tuple(int(v*D) for v in latent)
    Q=weather_kernel(survival,stay)
    powers=kernel_powers(Q,Kmax)
    hk={c:forecast_joint_kernel(c,fe,Q,powers) for c in range(1,Kmax+1)}
    cap=tuple(sum((pr for k,pr in distribution if k>=t),F(0)) for t in range(Kmax+1))
    assert cap[0]==1
    first={}
    policies={} if stats else None

    @lru_cache(None)
    def masses(read,reported):
        result=[]
        for g in range(n_groups):
            count=0
            for latent_err,mass in enumerate(noise):
                if all(not read&(1<<sid) or
                       (((g>>sid)&1)^((latent_err>>sid)&1))==((reported>>sid)&1)
                       for sid in range(r)):
                    count+=mass
            result.append(count)
        return tuple(result)

    @lru_cache(None)
    def solve(counts,read,reported,wind,elapsed):
        if elapsed>=Kmax or not cap[elapsed]:return F(0)
        gm=masses(read,reported);start=(counts==(0,)*n_groups and
                                       read==0 and reported==0 and elapsed==0)
        result=F(0);chosen={}
        for z in (0,1):
            scores=[("stop",F(0))]
            if elapsed+1<=Kmax and cap[elapsed+1]:
                survival_ratio=cap[elapsed+1]/cap[elapsed]
                for g,count in enumerate(counts):
                    if count>=per_group:continue
                    new=list(counts);new[g]+=1;new=tuple(new)
                    score=sum((
                        survival_ratio*hk[1][z][wind][nextwind]*
                        (gm[g]+solve(new,read,reported,nextwind,elapsed+1))
                        for nextwind in (0,1)),F(0))
                    scores.append(("flower_"+str(g),score))
            for sid in range(r):
                if read&(1<<sid):continue
                c=costs[wind][sid]
                if elapsed+c>Kmax or not cap[elapsed+c]:continue
                newmask=read|(1<<sid)
                no=reported&~(1<<sid);yes=reported|(1<<sid)
                survival_ratio=cap[elapsed+c]/cap[elapsed]
                score=sum((
                   survival_ratio*hk[c][z][wind][nextwind]*
                   (solve(counts,newmask,no,nextwind,elapsed+c)+
                    solve(counts,newmask,yes,nextwind,elapsed+c))
                   for nextwind in (0,1)),F(0))
                scores.append((chr(65+sid),score))
            m=max(val for _,val in scores)
            chosen[z]=tuple(name for name,val in scores if val==m)
            result+=m
            if start:first.setdefault(str(wind),{})[str(z)]=list(chosen[z])
        if stats:policies[(counts,read,reported,wind,elapsed)]=chosen
        return result

    initial_counts=(0,)*n_groups
    bonus=sum((initial[w]*solve(initial_counts,0,0,w,0) for w in (0,1)),F(0))
    v=F(1,2)+bonus/(2*n*D)
    if not stats:return v

    reachable=deque((initial_counts,0,0,w,0) for w in (0,1) if initial[w])
    visited=set();witnesses=[]
    while reachable:
        counts,read,reported,w,t=reachable.popleft()
        key=(counts,read,reported,w,t)
        if key in visited or key not in policies:continue
        visited.add(key)
        choices=policies[key]
        if not set(choices[0]).intersection(choices[1]):
            witnesses.append({"elapsed":t,"wind":w,"source_read_mask":read,
                "source_read_values":reported,"floral_count_per_group":counts,
                "forecast_calm":list(choices[0]),
                "forecast_gust":list(choices[1])})
        for z in (0,1):
            pz=sum((Q[w][v2]/survival[w]*(1-fe if z==v2 else fe)
                    for v2 in (0,1)),F(0)) if survival[w]>0 else F(0)
            if not pz:continue
            action=choices[z][0]
            if action=="stop":continue
            if action.startswith("flower_"):
                g=int(action.split("_")[1]);nextcount=list(counts);nextcount[g]+=1
                children=[(tuple(nextcount),read,reported,1)]
            else:
                sid=ord(action)-65;mask=read|(1<<sid)
                children=[(counts,mask,reported&~(1<<sid),costs[w][sid]),
                          (counts,mask,reported|(1<<sid),costs[w][sid])]
            for cs,rs,os,c in children:
                if t+c>Kmax or not cap[t+c] or not any(masses(rs,os)):continue
                for wn in (0,1):
                    if hk[c][z][w][wn]:
                        reachable.append((cs,rs,os,wn,t+c))
    return v,{"initial_policy":first,"reachable_policy_states":len(visited),
              "strict_forecast_action_switch_examples":witnesses[:15],
              "total_dp_states":solve.cache_info().currsize}


def cue_contexts(distribution=((3,F(1,2)),(7,F(1,2))),
       *,stay=F(1,2),forecast_error=F(1,2),
       survival=(F(19,20),F(13,20))):
    setups={"none":((),((),())),
            "A":((0,),((1,),(1,))),
            "B":((1,),((1,),(2,))),
            "AB":((0,1),((1,1),(1,2)))}
    values={name:forecast_accuracy(distribution,4,bits,
                 source_costs=costs,stay=stay,forecast_error=forecast_error,
                 survival=survival) for name,(bits,costs) in setups.items()}
    values["synergy"]=values["AB"]-values["A"]-values["B"]+values["none"]
    return values
