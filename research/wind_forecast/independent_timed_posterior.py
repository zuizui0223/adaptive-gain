"""Independent exact Bayesian audit of forecast timing with full latent worlds.

Enumerates ecological branch B, target T, two other-species observation
error bits and BOTH flower responses, terminal guesses, and all weather
trajectories. This does not import the production compressed DP.
Restrict to d<=2 and maximum duration<=4 for independent verification.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product


def direct_posterior_accuracy(distribution,d=2,bits=(0,1),
                              error=F(1,10),joint=None,
                              source_costs=((1,1),(1,2)),
                              survival=(F(19,20),F(13,20)),stay=F(1,2),
                              initial=(F(1,2),F(1,2)),
                              forecast_error=F(1,2),
                              available_from_tick=0,forecast_ticks=None):
    if type(d) is not int or not 1<=d<=2:raise ValueError("audit allows d=1,2")
    Kmax=max(k for k,_ in distribution)
    if Kmax>4:raise ValueError("audit maximum deadline is 4")
    e=F(error);q=e*e if joint is None else F(joint); zerr=F(forecast_error)
    survival=tuple(F(x) for x in survival);stay=F(stay)
    R=((stay,1-stay),(1-stay,stay));init=tuple(F(x) for x in initial)
    if type(available_from_tick) is not int or available_from_tick<0:
        raise ValueError("bad forecast arrival")
    if forecast_ticks is not None and (
        type(forecast_ticks) is not tuple or
        any(type(t) is not int or t<0 for t in forecast_ticks) or
        len(set(forecast_ticks)) != len(forecast_ticks)):
        raise ValueError("bad forecast schedule")
    def effective_error(t):
        return zerr if t>=available_from_tick and (
            forecast_ticks is None or t in forecast_ticks) else F(1,2)
    n=1<<d
    distribution=tuple((int(k),F(pr)) for k,pr in distribution)
    cap=tuple(sum((pr for k,pr in distribution if k>=t),F(0))
              for t in range(Kmax+1))
    latent_probs=(1-2*e+q,e-q,e-q,q)
    worlds=tuple((b,t,latent) for b in range(n) for t in (0,1)
                 for latent in range(4))
    root=tuple(latent_probs[l]/(2*n) for b,t,l in worlds)

    def weather_path_mass(z,c,current,end,forecast_noise):
        total=F(0)
        for path in product((0,1),repeat=c):
            if path[-1]!=end:continue
            mass=F(1);last=current
            for i,w in enumerate(path):
                mass*=survival[last]*R[last][w]
                if i==0:mass*=1-forecast_noise if w==z else forecast_noise
                last=w
            total+=mass
        return total

    H={(noise,z,c,w,v):weather_path_mass(z,c,w,v,noise)
       for noise in (zerr,F(1,2)) for z in (0,1)
       for c in range(1,Kmax+1) for w in (0,1) for v in (0,1)}
    Z={(noise,z,w):sum((R[w][v]*(1-noise if v==z else noise)
       for v in (0,1)),F(0)) for noise in (zerr,F(1,2))
       for z in (0,1) for w in (0,1)}

    def best_guess(m):
        return max(sum((v for i,v in enumerate(m) if worlds[i][1]==t),F(0))
                   for t in (0,1))

    def outcomes(m,kind,index):
        parts=[]
        for value in (0,1):
            parts.append(tuple(m[i] if (
               (int(b==index and t==1) if kind=="flower"
                else (((b>>bits[index])&1)^((latent>>index)&1)))==value
               else F(0) for i,(b,t,latent) in enumerate(worlds)))
        return tuple(parts)

    @lru_cache(None)
    def V(mass,wind,elapsed,flowers,sources):
        stop=best_guess(mass)
        if elapsed>=Kmax or cap[elapsed]==0:return stop
        actions=[("flower",i,1) for i in range(n) if not flowers&(1<<i)]
        actions += [("source",j,source_costs[wind][j])
                    for j in range(len(bits)) if not sources&(1<<j)]
        answer=F(0);eps=effective_error(elapsed)
        for z in (0,1):
            pz=Z[eps,z,wind]
            best=pz*stop
            for kind,index,cost in actions:
                if elapsed+cost>Kmax or cap[elapsed+cost]==0:continue
                rate=cap[elapsed+cost]/cap[elapsed]
                paths=(H[eps,z,cost,wind,0],H[eps,z,cost,wind,1])
                finished=rate*sum(paths)
                following=outcomes(mass,kind,index)
                score=(pz-finished)*stop
                for w,hazard in enumerate(paths):
                    if hazard==0:continue
                    new_flowers=flowers|(1<<index) if kind=="flower" else flowers
                    new_sources=sources|(1<<index) if kind=="source" else sources
                    score+=rate*hazard*sum((V(part,w,elapsed+cost,
                                      new_flowers,new_sources) for part in following
                                      if any(part)),F(0))
                best=max(best,score)
            answer+=best
        return answer
    return sum((init[w]*V(root,w,0,0,0) for w in (0,1)),F(0))
