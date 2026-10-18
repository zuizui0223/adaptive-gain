#!/usr/bin/env python3
"""Independent exact witness: cue-by-target marginals identical, routing changes.

This is a small analytic witness, NOT observed animal data or novelty priority.
No imports from adaptive-gain, and no inferred biology.
"""
from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement

TARGET=(0,0,0,1,1,1)
# columns are six worlds; rows are three binary cues in both environments
TASKS={
 'nonrouteable': ((1,1,0,0,0,0),(1,0,1,1,0,0),(0,1,1,0,1,0)),
 'routeable': ((1,1,0,0,0,0),(1,0,1,1,0,0),(1,0,1,0,1,0)),
}

def table(q):
    return tuple(tuple(sum(t==target and bit==outcome for t,bit in zip(TARGET,q))
                       for outcome in (0,1)) for target in (0,1))

def leaf(mask,kind):
    a=sum((mask>>i)&1 for i in range(3)); b=sum((mask>>i)&1 for i in range(3,6))
    if kind=='guess':return max(a,b)
    if kind=='cert':return (a+b) if min(a,b)==0 else 0
    raise ValueError(kind)

def dp_access(queries,budget,kind):
    @lru_cache(None)
    def opt(mask,remaining,used):
        score=leaf(mask,kind)
        if remaining:
            for j,q in enumerate(queries):
                if (used>>j)&1:continue
                mask1=sum(1<<i for i in range(6) if (mask>>i)&1 and q[i]==1)
                mask0=mask^mask1
                if mask1 and mask0:
                    score=max(score,opt(mask0,remaining-1,used|(1<<j))+
                                    opt(mask1,remaining-1,used|(1<<j)))
        return score
    return F(opt(63,budget,0),6)

def brute_access(queries,budget,kind):
    """Second independent oracle enumerates all full-depth policy trees."""
    @lru_cache(None)
    def all_trees(available,remaining):
        trees=(None,)
        if remaining:
            for j in available:
                other=tuple(k for k in available if k!=j)
                child=all_trees(other,remaining-1)
                trees += tuple((j,a,b) for a in child for b in child)
        return trees
    def visit(tree,mask):
        if tree is None:return leaf(mask,kind)
        j,a,b=tree
        bit1=sum(1<<i for i in range(6) if (mask>>i)&1 and queries[j][i])
        return visit(a,mask^bit1)+visit(b,bit1)
    return F(max(visit(tr,63) for tr in all_trees((0,1,2),budget)),6)

def fixed_access(queries,budget,kind):
    high=F(0)
    for size in range(budget+1):
        for selection in combinations(range(3),size):
            masks={}
            for i in range(6):
                outcome=tuple(queries[j][i] for j in selection)
                masks[outcome]=masks.get(outcome,0)|(1<<i)
            high=max(high,F(sum(leaf(mask,kind) for mask in masks.values()),6))
    return high

def perfect_fixed(queries):
    return next(n for n in range(4) if fixed_access(queries,n,'cert')==1)

def perfect_adaptive(queries):
    return next(n for n in range(4) if dp_access(queries,n,'cert')==1)

def encode(qs):
    return tuple(tuple(q[i] for q in qs) for i in range(6))

result={'case':'six worlds; three binary unit-cost cues; three target-0 and three target-1 worlds', 'status':'exact_fraction_verified'}
left,right=TASKS.values()
assert len(set(encode(left)))==len(set(encode(right)))==6
assert tuple(table(q) for q in left)==tuple(table(q) for q in right)
result['per_cue_target_by_outcome_tables']=tuple(table(q) for q in left)
result['cue_matrices']=TASKS
for name,queries in TASKS.items():
    assert len(set(encode(queries)))==6
    result[name]={'C_A':perfect_adaptive(queries),'C_F':perfect_fixed(queries),'by_budget':{}}
    for budget in range(4):
        metrics={}
        for kind in ('guess','cert'):
            a=dp_access(queries,budget,kind)
            brute=brute_access(queries,budget,kind)
            assert a==brute, (name,budget,kind,a,brute)
            f=fixed_access(queries,budget,kind)
            metrics[kind]={'adaptive':str(a),'precommitted':str(f),'premium':str(a-f)}
        result[name]['by_budget'][str(budget)]=metrics
assert result['nonrouteable']['C_A']==3 and result['nonrouteable']['C_F']==3
assert result['routeable']['C_A']==2 and result['routeable']['C_F']==3
assert result['routeable']['by_budget']['2']['guess']['premium']=='1/6'
assert result['nonrouteable']['by_budget']['2']['guess']['premium']=='0'
assert result['routeable']['by_budget']['2']['cert']['premium']=='1/3'

# Exhaust an explicit matched one-cue-contingency family: cue0 has (2,0)
# ones by target class; cue1 and cue2 each have (2,1). Counts describe the
# finite labeled design family, NOT how common routeability is in ecology.
def row(mask):return tuple((mask>>i)&1 for i in range(6))
q0=[row(q) for q in range(1,64) if (q&7).bit_count()==2 and ((q>>3)&7).bit_count()==0]
q12=[row(q) for q in range(1,64) if (q&7).bit_count()==2 and ((q>>3)&7).bit_count()==1]
assert len(q0)==3 and len(q12)==9
counts=Counter()
for a in q0:
 for b,c in combinations_with_replacement(q12,2):
    qs=(a,b,c)
    if len(set(encode(qs)))<6:counts['duplicate_world_signatures']+=1;continue
    cf=fixed_access(qs,3,'cert')
    if cf!=1:counts['unresolved_target']+=1;continue
    cfmin=perfect_fixed(qs)
    camin=perfect_adaptive(qs)
    counts[f'CA{camin}_CF{cfmin}']+=1
result['exhaustive_matched_family']={**dict(counts),'total':len(q0)*45,'note':'synthetic labeled cue systems, not an ecological prevalence sample'}
assert sum(counts.values())==135
if __name__=='__main__':print(json.dumps(result,indent=2,ensure_ascii=False))
