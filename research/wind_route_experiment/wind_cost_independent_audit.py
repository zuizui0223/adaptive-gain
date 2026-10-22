"""Independent full target-posterior audit of cost-weighted other-species cues.

Rather than using the main hit-count DP, this solver retains explicit latent
two-source flip patterns, terminal T=0 AND T=1 masses, and STOP-vs-CUE choices.
Expected correctness, not ecological fitness. Original source is synthetic.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import lcm
from adaptive_gain.multispecies_wind_synergy import optimal


def independent(d, budget, bits, costs, error=F(0), joint=None):
    e=F(error)
    q=e*e if joint is None else F(joint)
    probs=(1-2*e+q,e-q,e-q,q)
    den=lcm(*(a.denominator for a in probs))
    mult=tuple(int(a*den) for a in probs)
    n=1<<d
    bits=tuple(bits);costs=tuple(costs)

    @lru_cache(None)
    def worlds(read,observed):
        result=[]
        for b in range(n):
            for noise,weight in enumerate(mult):
                if not weight:continue
                if all(not (read&(1<<sid)) or
                       (((b>>bit)&1)^((noise>>sid)&1))==((observed>>sid)&1)
                       for sid,bit in enumerate(bits)):
                    result.append((b,weight))
        return tuple(result)

    @lru_cache(None)
    def solve(used,read,observed,left):
        wc=worlds(read,observed)
        mass_zero=sum(weight for b,weight in wc)
        mass_one=sum(weight for b,weight in wc if not (used&(1<<b)))
        best=max(mass_zero,mass_one)  # optimized terminal classification
        if left==0:return best
        for b in range(n):
            if used & (1<<b):continue
            hit=sum(weight for bb,weight in wc if bb==b)
            best=max(best,hit+solve(used|(1<<b),read,observed,left-1))
        for sid,cost in enumerate(costs):
            flag=1<<sid
            if read&flag or cost>left:continue
            best=max(best,solve(used,read|flag,observed&~flag,left-cost)
                          +solve(used,read|flag,observed|flag,left-cost))
        return best
    return F(solve(0,0,0,budget),2*n*den)


def audit():
    checks=0
    for d,K in ((3,4),(4,5),(4,6)):
        for e,q in ((F(0),F(0)),(F(1,10),F(1,100)),
                    (F(3,20),F(0)),(F(3,20),F(3,20))):
            for bits,costs in (((0,),(1,)),((1,),(2,)),
                               ((0,1),(1,1)),((0,1),(1,2)),((0,1),(2,2))):
                got=optimal(d,K,bits,e,q,costs=costs)
                actual=independent(d,K,bits,costs,e,q)
                assert got==actual,(d,K,e,q,bits,costs,got,actual)
                checks+=1
    return {'status':'INDEPENDENT_POSTERIOR_EXACT_MATCH','cases':checks}


if __name__=="__main__":
    import json
    print(json.dumps(audit()))
