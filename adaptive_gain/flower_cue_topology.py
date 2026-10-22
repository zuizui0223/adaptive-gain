"""Finite four-world binary flower-cue architecture census (not empirical).

Uniform independent branch B and target T, two arbitrary deterministic floral
observation channels, and optionally one noisy heterospecific branch indicator.
All 256 floral truth-table pairs are exhaustively scored at a TWO-query budget.

Distinguishes heterospecific source value from strictly adaptive order value.
Exact fractions, including an independently enumerated decision-tree oracle.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from functools import lru_cache

_STATES=((0,0),(0,1),(1,0),(1,1))
_PRIOR=(Fraction(1,4),)*4

def cue_matrix(mask: int) -> tuple[int,int,int,int]:
    if type(mask) is not int or not 0 <= mask < 16:
        raise ValueError("four-state signal mask must be an integer from 0 to 15")
    return tuple((mask>>i)&1 for i in range(4))

def _check(x,y,error):
    for name,z in (("F0",x),("F1",y)):
        if len(z)!=4 or any(type(v) is not int or v not in (0,1) for v in z):
            raise ValueError(f"{name} must be exactly four binary outputs")
    if error is None:
        return None
    e=Fraction(error)
    if not 0<=e<=Fraction(1,2):
        raise ValueError("other-species branch cue error must be in [0,1/2]")
    return e

def _channels(e):
    return ("F0","F1") if e is None else ("F0","F1","H")

def _prob(name,obs,i,x,y,e):
    if name=="F0":
        return Fraction(int(x[i]==obs))
    if name=="F1":
        return Fraction(int(y[i]==obs))
    if name=="H":
        if e is None:
            raise ValueError("species cue unavailable")
        return 1-e if _STATES[i][0]==obs else e
    raise ValueError("unsupported cue")

def _leaf(w):
    return max(w[0]+w[2],w[1]+w[3])

def adaptive_score(f0,f1,error):
    """Maximum Bayes target accuracy, up to two outcome-contingent queries."""
    e=_check(f0,f1,error)
    @lru_cache(None)
    def solve(mass,unused,remaining):
        best=_leaf(mass)
        if not remaining:
            return best
        for q in unused:
            rest=tuple(z for z in unused if z!=q)
            score=Fraction(0)
            for output in (0,1):
                child=tuple(mass[i]*_prob(q,output,i,f0,f1,e) for i in range(4))
                if any(child):
                    score+=solve(child,rest,remaining-1)
            best=max(best,score)
        return best
    return solve(_PRIOR,_channels(e),2)

def fixed_score(f0,f1,error):
    """Best precommitted subset of zero, one or two queries."""
    e=_check(f0,f1,error)
    best=Fraction(1,2)
    for length in (1,2):
        for chosen in combinations(_channels(e),length):
            score=Fraction(0)
            for observed in product((0,1),repeat=length):
                mass=list(_PRIOR)
                for cue,output in zip(chosen,observed):
                    mass=[mass[i]*_prob(cue,output,i,f0,f1,e) for i in range(4)]
                score+=_leaf(mass)
            best=max(best,score)
    return best

def exact_policy_enumeration(f0,f1,error):
    """Separate exhaustive policy listing, not the adaptive DP or subset code."""
    e=_check(f0,f1,error)
    best=Fraction(1,2)
    for q1 in _channels(e):
        alternatives=(None,)+tuple(q for q in _channels(e) if q!=q1)
        for next0,next1 in product(alternatives,repeat=2):
            val=Fraction(0)
            for obs1,q2 in ((0,next0),(1,next1)):
                if q2 is None:
                    masses=[_PRIOR[i]*_prob(q1,obs1,i,f0,f1,e) for i in range(4)]
                    val+=max(masses[0]+masses[2],masses[1]+masses[3])
                else:
                    for obs2 in (0,1):
                        totals=[Fraction(0),Fraction(0)]
                        for i,(_,target) in enumerate(_STATES):
                            totals[target]+=_PRIOR[i]*_prob(q1,obs1,i,f0,f1,e)*_prob(q2,obs2,i,f0,f1,e)
                        val+=max(totals)
            best=max(best,val)
    return best

def catalog(error: Fraction=Fraction(1,10)):
    """All 256 binary-map pairs; labeled truth-table counts are not field frequencies."""
    e=_check(cue_matrix(0),cue_matrix(0),error)
    if e is None:raise ValueError("catalog requires a species-cue error rate")
    out=[]
    for a,b in product(range(16),repeat=2):
        x,y=cue_matrix(a),cue_matrix(b)
        base=adaptive_score(x,y,None)
        adapt=adaptive_score(x,y,e)
        fixed=fixed_score(x,y,e)
        if adapt<base or adapt<fixed:
            raise ArithmeticError("monotonicity failed")
        out.append({
          "floral0_mask":a,"floral1_mask":b,"floral0":x,"floral1":y,
          "correct_branch_specific":x[0]!=x[1] and y[2]!=y[3],
          "canonical_orientation":x[:2]==(0,1) and y[2:]==(0,1),
          "baseline_without_species":base,
          "species_adaptive":adapt,"species_fixed":fixed,
          "other_species_absolute_value":adapt-base,
          "strict_sequential_value":adapt-fixed,
        })
    return tuple(out)

def _count(rows):
    from collections import Counter
    rows=tuple(rows)
    gains=Counter(str(r["other_species_absolute_value"]) for r in rows)
    fixed=Counter(str(r["species_fixed"]) for r in rows)
    return {
      "total":len(rows),
      "gain_none":sum(r["other_species_absolute_value"]==0 for r in rows),
      "source_helps_fixed_only":sum(r["other_species_absolute_value"]>0 and
                                    r["strict_sequential_value"]==0 for r in rows),
      "strict_adaptive_over_fixed":sum(r["strict_sequential_value"]>0 for r in rows),
      "other_species_gain_values":dict(sorted(gains.items())),
      "fixed_values":dict(sorted(fixed.items())),
    }

def summarize(rows):
    rows=tuple(rows)
    valid=[r for r in rows if r["correct_branch_specific"]]
    canon=[r for r in rows if r["canonical_orientation"]]
    return {
      "all_pairs":len(rows),"branch_specific_pairs":len(valid),
      "canonical_oriented_pairs":len(canon),
      "all":_count(rows),"branch_specific":_count(valid),"canonical":_count(canon),
    }

def write_outputs(directory):
    import csv,json
    from pathlib import Path
    path=Path(directory);path.mkdir(parents=True,exist_ok=True)
    rows=catalog()
    keys=("floral0_mask","floral1_mask","correct_branch_specific",
          "canonical_orientation","baseline_without_species",
          "species_adaptive","species_fixed","other_species_absolute_value",
          "strict_sequential_value")
    with (path/"256_flower_cue_architectures.csv").open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({k:str(row[k]) if isinstance(row[k],Fraction) else row[k]
                             for k in keys})
    summary=summarize(rows)
    (path/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print("EXHAUSTIVE_FLORAL_CUE_TOPOLOGY_PASS",json.dumps(summary))
    return summary

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="floral_cue_topology_results")
    args=ap.parse_args()
    write_outputs(args.out)
