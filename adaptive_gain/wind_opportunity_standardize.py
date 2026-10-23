"""Standardize expected completed exploration time across wind persistence.

This deliberately changes underlying state-specific encounter survival rates to
isolate a model sensitivity. Not the same real-wind treatment or field inference.
"""
from fractions import Fraction as F
from .stochastic_weather import weather_kernel,kernel_powers
from .deadline_mixture import mixed_contexts

BASE=(F(19,20),F(13,20))
PRIOR=((3,F(1,2)),(7,F(1,2)))

def expected_ticks(stay,survival,deadlines=PRIOR):
    deadlines=tuple((k,F(p)) for k,p in deadlines)
    maxk=max(k for k,_ in deadlines)
    A=kernel_powers(weather_kernel(survival,stay),maxk)
    return sum((sum((p for k,p in deadlines if k>=t),F(0))*
             (sum(A[t][0])+sum(A[t][1]))/2 for t in range(1,maxk+1)),F(0))

def match_mean_ticks(stay,target,steps=25):
    lo,hi=F(0),F(20,19)
    if target<0 or target>expected_ticks(stay,tuple(x*hi for x in BASE)):
        raise ValueError("target expected life cannot be matched")
    for _ in range(steps):
        mid=(lo+hi)/2
        if expected_ticks(stay,tuple(x*mid for x in BASE))<target:
            lo=mid
        else:
            hi=mid
    return (lo+hi)/2

def matched_results():
    reference=expected_ticks(F(1,2),BASE)
    rows=[]
    for p in (F(1,10),F(1,2),F(9,10)):
        scale=F(1) if p==F(1,2) else match_mean_ticks(p,reference)
        survival=tuple(x*scale for x in BASE)
        actual=expected_ticks(p,survival)
        z=mixed_contexts(4,PRIOR,survival=survival,stay=p)['hidden']
        rows.append({"stay":str(p),"scale":str(scale),"expected_ticks":str(actual),
              "residual":str(actual-reference),"P_AB":str(z['AB']),
              "interaction":str(z['interaction'])})
    return rows
