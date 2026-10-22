"""Independent original-truth-table audit for 256 synthetic cue architectures.

Does not import the production DP/fixed scoring code. Rebuilds all policy leaf
likelihoods directly from the output CSV and compares exact Fraction outputs.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations,product
from pathlib import Path
import csv,json

B=(0,0,1,1)
T=(0,1,0,1)
E=Q(1,10)
CUES=('species','flower0','flower1')

def leaf(observations,m0,m1):
    probs=[Q(0),Q(0)]
    for i in range(4):
        mass=Q(1,4)
        for cue,out in observations:
            if cue=='species':
                mass*=1-E if B[i]==out else E
            elif cue=='flower0':
                mass*=int(((m0>>i)&1)==out)
            elif cue=='flower1':
                mass*=int(((m1>>i)&1)==out)
            else:raise ValueError(cue)
        probs[T[i]]+=mass
    return max(probs)

def independent_adaptive(m0,m1):
    best=Q(1,2)
    for first in CUES:
        other=(None,)+tuple(z for z in CUES if z!=first)
        for second0,second1 in product(other,repeat=2):
            value=Q(0)
            for y,next_q in ((0,second0),(1,second1)):
                first_obs=((first,y),)
                if next_q is None:
                    value+=leaf(first_obs,m0,m1)
                else:
                    value+=sum((leaf(first_obs+((next_q,z),),m0,m1) for z in (0,1)),Q(0))
            best=max(best,value)
    return best

def independent_fixed(m0,m1):
    best=Q(1,2)
    for n in (1,2):
        for chosen in combinations(CUES,n):
            total=Q(0)
            for values in product((0,1),repeat=n):
                total+=leaf(tuple(zip(chosen,values)),m0,m1)
            best=max(best,total)
    return best

def audit(csv_path):
    with Path(csv_path).open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=256:raise ValueError('complete 16x16 source required')
    if len({(r['floral0_mask'],r['floral1_mask']) for r in rows})!=256:
        raise ValueError('duplicate or missing architecture')
    largest=Q(0)
    for r in rows:
        a,b=int(r['floral0_mask']),int(r['floral1_mask'])
        independent=(independent_adaptive(a,b),independent_fixed(a,b))
        primary=(Q(r['species_adaptive']),Q(r['species_fixed']))
        largest=max(largest,*(abs(x-y) for x,y in zip(independent,primary)))
    if largest:raise AssertionError('independent enumeration disagrees: '+str(largest))
    return {'n_architectures':len(rows),'max_exact_difference':str(largest),
            'method':'independent explicit depth-two trees and fixed cue subsets',
            'ecological_scope':'constructed four-state cues, not observations'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('source_csv')
    p.add_argument('--out',default='flower_cue_independent_audit.json')
    a=p.parse_args()
    result=audit(a.source_csv)
    Path(a.out).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('IND_FOUR_WORLD_ALL_256_PASS',json.dumps(result))
