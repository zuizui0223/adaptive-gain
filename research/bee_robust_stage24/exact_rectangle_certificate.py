"""Stage24: exact 8-parameter rectangular dominance certificate, SOURCE-FREE.

The fixed contingent policy uses Z0 -> SKIP, predict 0; Z1 -> buy V,
report V as the prediction. Any precommitted policy has a multiaffine
expected payoff on q,s0,s1,u0,u1,v0,v1,c. So min over parameters of
(fixed contingent value - optimal precommit value) occurs at a vertex
of the rectangular box. The proof never assumes that the optimal
contingent policy stays the same over the box.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json

WORLDS = tuple(product((0, 1), repeat=3))
ORDER = ('q','s0','s1','u0','u1','v0','v1','c')
BOX = {
    'q': ('0.16','0.24'), 's0': ('0.76','0.84'),
    's1': ('0.56','0.64'), 'u0': ('0.85','1.00'),
    'u1': ('0.85','1.00'), 'v0': ('0.96','1.00'),
    'v1': ('0.86','0.94'), 'c': ('0.13','0.17')
}
BASE = tuple(F(x) for x in ('.2','.8','.6','1','1','1','.9','.15'))
ZERO = F(0)


def _target(w):
    return w[1] if w[0] == 0 else w[2]


def _root_joint(q,s0,s1,z):
    return {w: F(1,4)*(q if w[1] else 1-q)*(
        (s0 if z==0 else 1-s0) if w[0]==0
        else ((1-s1) if z==0 else s1)) for w in WORLDS}


def _leaf_joint(d,leaf,bit,u0,u1,v0,v1):
    idx, rate0, rate1 = (1,u0,u1) if leaf == 'U' else (2,v0,v1)
    return {w: weight*((rate0 if bit==0 else 1-rate0)
                 if w[idx]==0 else ((1-rate1) if bit==0 else rate1))
            for w,weight in d.items()}


def _mass(d):
    return sum(d.values(), ZERO)


def _guess(d):
    return max(sum((wt for w,wt in d.items() if _target(w)==i), ZERO)
               for i in (0,1))


def _paid_first(d,leaf,c,u0,u1,v0,v1):
    other = 'V' if leaf=='U' else 'U'
    v = -c*_mass(d)
    for bit in (0,1):
        a = _leaf_joint(d,leaf,bit,u0,u1,v0,v1)
        stop = _guess(a)
        second = -c*_mass(a)+sum((_guess(_leaf_joint(a,other,b2,u0,u1,v0,v1))
                                     for b2 in (0,1)), ZERO)
        v += max(stop,second)
    return v


def precommit_value(q,s0,s1,u0,u1,v0,v1,c):
    """Exact best first SKIP/U/V before Z, optional second after Z/leaf."""
    d = [_root_joint(q,s0,s1,z) for z in (0,1)]
    return max(sum((_guess(x) for x in d), ZERO),
               sum((_paid_first(x,'U',c,u0,u1,v0,v1) for x in d), ZERO),
               sum((_paid_first(x,'V',c,u0,u1,v0,v1) for x in d), ZERO))


def fixed_contingent_value(q,s0,s1,u0,u1,v0,v1,c):
    """Direct independently derived closed-form gross success minus paid V."""
    return (s0*(1-q)/2 + (1-s1)/4 + s1*(v0+v1)/4
            + (1-s0)*(1+(1-2*q)*(v0-v1))/4
            - c*(1-s0+s1)/2)


def _validate(box):
    if set(box) != set(ORDER):
        raise ValueError('NO_GO_INCOMPLETE_EIGHT_PARAMETER_BOX')
    out = {}
    for k in ORDER:
        value = box[k]
        if not isinstance(value, (tuple,list)) or len(value)!=2:
            raise ValueError('NO_GO_MISSING_INTERVAL')
        try:
            lo,hi = (F(x) for x in value)
        except (ValueError,TypeError,ZeroDivisionError) as err:
            raise ValueError('NO_GO_NONRATIONAL_INTERVAL') from err
        min_rate = F(0) if k=='q' else F(0) if k=='c' else F(1,2)
        max_rate = F(1,2) if k=='q' else None if k=='c' else F(1)
        if lo < min_rate or hi < lo or (max_rate is not None and hi>max_rate):
            raise ValueError('NO_GO_OUTSIDE_MODEL_DOMAIN')
        out[k] = (lo,hi)
    return out


def certify(box=BOX):
    """Sharp worst-case advantage of ONE fixed strategy against ALL precommit policies."""
    region = _validate(box)
    smallest = None
    witnesses = []
    positive_count = 0
    for corner in product(*(region[k] for k in ORDER)):
        gap = fixed_contingent_value(*corner) - precommit_value(*corner)
        if smallest is None or gap < smallest:
            smallest = gap
            witnesses = [corner]
        elif gap == smallest:
            witnesses.append(corner)
        positive_count += int(gap>0)
    assert smallest is not None
    return {
        'status': 'STRICTLY_POSITIVE_CONTINGENT_ADVANTAGE_CERTIFIED'
                  if smallest>0 else 'NO_UNIFORM_POSITIVITY_CERTIFICATE',
        'original_eight_worlds':True,
        'certificate_kind':'sharp fixed-policy vs all-precommit, multiaffine rectangle',
        'parameter_box':{k:[str(y) for y in region[k]] for k in ORDER},
        'corner_count':2**len(ORDER),
        'positive_corner_count_for_fixed_policy':positive_count,
        'fixed_policy':'if Z0 SKIP predict 0; if Z1 buy V and predict V readout; never buy U',
        'minimum_fixed_minus_optimal_precommit':str(smallest),
        'worst_corner':{k:str(x) for k,x in zip(ORDER,witnesses[0])},
        'number_of_tied_worst_corners':len(witnesses),
        'baseline_at_c_0point15':str(fixed_contingent_value(*BASE)-precommit_value(*BASE)),
        'sharpness':'Exact for the fixed policy, a lower bound for the optimal contingent policy',
        'logic':'For every deterministic precommitted strategy, its expected payoff and the chosen fixed contingent policy payoff are separately multiaffine in the eight coordinates: Bernoulli q and each class-channel probability, and linear paid cost c (each source once). Their difference therefore attains its minimum on the 8D rectangle at a vertex. Min over strategies commutes with min over the finite vertex set. The maximum precommitted value at each vertex is computed exactly by backward induction. Optimal contingent value is at least the fixed policy value at every interior point.',
        'no_live_bees':True,
        'no_animal_measurements':True,
        'not_an_empirical_confidence_region':True,
        'not_fitness_measurement':True
    }


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='stage24_source_free_outputs')
    folder=Path(p.parse_args().out);folder.mkdir(parents=True,exist_ok=True)
    result=certify()
    assert result['minimum_fixed_minus_optimal_precommit']=='63/6250'
    assert result['baseline_at_c_0point15']=='6/125'
    (folder/'stage24_8d_robust_cost_rectangle.json').write_text(
        json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in
          ('status','minimum_fixed_minus_optimal_precommit','corner_count','positive_corner_count_for_fixed_policy','no_live_bees')},sort_keys=True))
