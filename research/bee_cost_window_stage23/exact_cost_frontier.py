"""Stage23: exact cost-phase certificate for a frozen Stage22 eight-world example.

SOURCE FREE. No bees or other animals were measured. All probabilities and
costs are hypothetical normalized decision-utility parameters.

Instead of fitting a cost grid, enumerate all relevant deterministic Bayesian
policies as rational (gross correctness, expected query-count) pairs. Every
policy has utility B - c*N, so the upper envelope proves each interval for
ALL c>=0, including endpoints and not only sampled costs.
"""
from fractions import Fraction as F
from itertools import product, combinations
import argparse
import json
from pathlib import Path

ZERO, ONE = F(0), F(1)
Q = F(1, 5)
R0, R1 = F(4, 5), F(3, 5)
U0, U1 = ONE, ONE
V0, V1 = ONE, F(9, 10)
WORLDS = tuple(product((0, 1), repeat=3))
PARAMS = {'Z': (0, R0, R1), 'U': (1, U0, U1), 'V': (2, V0, V1)}


def _world_prior():
    return {w: F(1, 4) * (Q if w[1] else 1-Q) for w in WORLDS}


def _observe(masses, source, reported):
    index, a0, a1 = PARAMS[source]
    return {w: m * ((a0 if reported == 0 else 1-a0) if w[index] == 0
                    else ((1-a1) if reported == 0 else a1))
            for w, m in masses.items()}


def _target(w):
    return w[1] if w[0] == 0 else w[2]


def _guess(masses):
    return max(sum((m for w,m in masses.items() if _target(w)==bit),ZERO)
               for bit in (0,1))


def _mass(masses):
    return sum(masses.values(), ZERO)


def _pareto(lines):
    """Retain nondominated (correct mass, query mass) for costs >=0."""
    by_n = {}
    for gross, n in lines:
        if n not in by_n or gross > by_n[n]:
            by_n[n] = gross
    best = F(-1)
    keep = []
    for n, gross in sorted(by_n.items()):
        if gross > best:
            keep.append((gross, n))
            best = gross
    return tuple(keep)


def _merge(option_groups):
    return _pareto((sum((p[0] for p in selected), ZERO),
                    sum((p[1] for p in selected), ZERO))
                   for selected in product(*option_groups))


def _one_first(masses, source):
    """Commit to first leaf, then optimally select SKIP/other leaf per bit."""
    other = 'V' if source == 'U' else 'U'
    choices = []
    for bit in (0,1):
        branch = _observe(masses, source, bit)
        stop = (_guess(branch), ZERO)
        second = (sum((_guess(_observe(branch, other, x)) for x in (0,1)),ZERO),
                  _mass(branch))
        choices.append(_pareto((stop, second)))
    return _pareto((correct, count + _mass(masses))
                   for correct, count in _merge(choices))


def policy_frontiers():
    root = {z: _observe(_world_prior(), 'Z', z) for z in (0,1)}
    local = {z: {'SKIP': ((_guess(root[z]), ZERO),),
                 'U': _one_first(root[z], 'U'),
                 'V': _one_first(root[z], 'V')}
             for z in (0,1)}
    contingent = _merge([_pareto(p for entries in local[z].values() for p in entries)
                         for z in (0,1)])
    precommitted = _pareto(p for action in ('SKIP','U','V')
                            for p in _merge([local[z][action] for z in (0,1)]))
    return contingent, precommitted


def _upper_envelope(lines):
    # Every possible change of the maximizing affine line is at an exact
    # pairwise intersection, so checking each open interval is exhaustive.
    cuts = {ZERO}
    for (b1,n1),(b2,n2) in combinations(lines,2):
        if n1 != n2:
            x = (b1-b2)/(n1-n2)
            if x > 0:
                cuts.add(x)
    xs=sorted(cuts)
    found=[]
    for k,lo in enumerate(xs):
        hi=xs[k+1] if k+1 < len(xs) else None
        sample=(lo+hi)/2 if hi is not None else lo+ONE
        best=max(lines,key=lambda line:line[0]-sample*line[1])
        if found and found[-1][2]==best:
            found[-1]=(found[-1][0],hi,best)
        else:
            found.append((lo,hi,best))
    return tuple(found)


def _value(lines,c):
    return max((b-c*n for b,n in lines))


def cost_window_certificate():
    contingent, precommitted=policy_frontiers()
    env_c=_upper_envelope(contingent)
    env_p=_upper_envelope(precommitted)
    expected_c=((ZERO,F(2,15),(F(419,500),ONE)),
                (F(2,15),F(27,100),(F(379,500),F(2,5))),
                (F(27,100),None,(F(13,20),ZERO)))
    expected_p=((ZERO,F(47,350),(F(419,500),F(7,5))),
                (F(47,350),None,(F(13,20),ZERO)))
    if env_c != expected_c or env_p != expected_p:
        raise AssertionError(f'NO_GO_EXACT_ENVELOPE: {env_c} != {expected_c}; {env_p} != {expected_p}')
    peak_c=F(47,350)
    peak=_value(contingent,peak_c)-_value(precommitted,peak_c)
    if peak!=F(19,350):
        raise AssertionError('NO_GO_PEAK_VALUE')
    if _value(contingent,F(1,4))-_value(precommitted,F(1,4))!=F(1,125):
        raise AssertionError('NO_GO_STAGE22_QUARTER_COST_REDUCTION')
    if _value(contingent,ZERO)!=_value(precommitted,ZERO):
        raise AssertionError('NO_GO_ZERO_COST_NEGATIVE_CONTROL')
    if _value(contingent,ONE)!=_value(precommitted,ONE):
        raise AssertionError('NO_GO_EXPENSIVE_COST_NEGATIVE_CONTROL')
    # Exact piecewise gain certificate: no interpolation or c-grid fitting.
    return {
        'status':'EXACT_SOURCE_FREE_COST_WINDOW_CERTIFICATE',
        'model':{'q':'1/5','s0':'4/5','s1':'3/5','u0':'1','u1':'1',
                 'v0':'1','v1':'9/10','each_leaf_at_most_once':True,
                 'second_distinct_leaf_optional':True,'cost_domain':'c>=0'},
        'contingent_envelope':_serialize(env_c),
        'precommit_envelope':_serialize(env_p),
        'gain_piecewise':[
          {'cost_range':'0 <= c <= 2/15','gain':'2*c/5'},
          {'cost_range':'2/15 <= c <= 47/350','gain':'c - 2/25'},
          {'cost_range':'47/350 <= c <= 27/100','gain':'27/250 - 2*c/5'},
          {'cost_range':'c >= 27/100','gain':'0'}],
        'peak_cost':'47/350','peak_gain':'19/350',
        'gain_at_stage22_cost_quarter':'1/125',
        'strict_positive_iff':'0<c<27/100',
        'proof':'All deterministic first/optional second query choices have utility B-cN. Exact rational Pareto frontiers and all pairwise affine intersections certify the upper envelopes for every c>=0.',
        'no_real_animals':True,'no_empirical_cost_estimate':True,
        'not_ecological_fitness':True
    }


def _serialize(pieces):
    return [{'start':str(lo),'end':str(hi) if hi is not None else None,
             'gross_correct':str(line[0]),'expected_queries':str(line[1])}
            for lo,hi,line in pieces]


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='stage23_exact_outputs')
    dest=Path(ap.parse_args().out);dest.mkdir(parents=True,exist_ok=True)
    result=cost_window_certificate()
    (dest/'stage23_cost_window_certificate.json').write_text(
        json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','peak_cost','peak_gain','strict_positive_iff','no_real_animals')},sort_keys=True))
