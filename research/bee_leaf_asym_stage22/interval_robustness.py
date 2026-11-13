"""Exact interval robustness for fixed Stage22 q=1/5, c=1/4 theorem.

Any parameter rectangles passed here are ASSUMED. Unless each interval
has independently justified simultaneous statistical coverage based on
real original bees/colonies, the returned range is NOT a confidence
interval and does not establish biological adaptation.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json,math

KEYS=('s0','s1','v0','v1')
HALF=F(1,2);ONE=F(1)

def _as_fraction(x):
    if type(x) not in (float,int,F) or not math.isfinite(float(x)):
        raise ValueError('NO_GO_NONFINITE_PARAMETER_INTERVAL')
    return x if isinstance(x,F) else F(str(x))

def _signed_gain(s0,s1,v0,v1):
    # The one fixed theorem from Stage22, BEFORE taking positive part.
    return s1*(v0+v1-F(3,2))/4 + (ONE-s0)*(
           F(3,20)*v0-F(3,20)*v1-F(11,40))

def bound_value(box):
    """Sharp extrema on a 4D rectangle by multiaffine-corner property."""
    if not isinstance(box,dict) or set(box)!=set(KEYS):
        raise ValueError('NO_GO_MISSING_CLASS_SPECIFIC_INTERVAL')
    ranges={}
    for k in KEYS:
        raw=box[k]
        if not isinstance(raw,(list,tuple)) or len(raw)!=2:
            raise ValueError('NO_GO_MISSING_INTERVAL_ENDPOINT')
        a,b=(_as_fraction(x) for x in raw)
        if a<HALF or b>ONE or b<a:
            raise ValueError('NO_GO_INTERVAL_OUTSIDE_THEOREM_DOMAIN')
        ranges[k]=(a,b)
    corners=[]
    for vals in product(*(ranges[k] for k in KEYS)):
        signed=_signed_gain(*vals)
        corners.append((signed,vals))
    minimum=min(corners,key=lambda x:x[0])
    maximum=max(corners,key=lambda x:x[0])
    lower=max(F(0),minimum[0])
    upper=max(F(0),maximum[0])
    return {
      'status':'POSITIVE_FOR_ALL_ASSUMED_PARAMETERS' if minimum[0]>0 else
               'INCONCLUSIVE_FOR_SOME_ASSUMED_PARAMETERS' if maximum[0]>0 else
               'NO_POSITIVE_GAIN_ANYWHERE_IN_ASSUMED_PARAMETERS',
      'fixed_q_fraction':'1/5','fixed_leaf_cost_fraction':'1/4',
      'input_parameter_rectangle':{k:[float(x) for x in ranges[k]] for k in KEYS},
      'minimum_signed_margin':float(minimum[0]),
      'maximum_signed_margin':float(maximum[0]),
      'smallest_possible_gain':float(lower),
      'largest_possible_gain':float(upper),
      'exact_corner_count':len(corners),
      'worst_corner':dict(zip(KEYS,map(float,minimum[1]))),
      'best_corner':dict(zip(KEYS,map(float,maximum[1]))),
      'proof':'The signed gain is multi-affine in four variables, so extrema over any rectangular domain occur at vertices; positive part is monotone.',
      'not_a_confidence_interval_without_source_coverage':True,
      'no_animal_confusion_matrices_measured':True,
      'no_biological_inference':True
    }

def main(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    cases={
      'observed_point_but_uncertain_example':{
        's0':(.79,.81),'s1':(.59,.61),'v0':(.92,1.),'v1':(.85,.95)},
      'narrow_assumed_positive_region':{
        's0':(.8,.8),'s1':(.6,.6),'v0':(.99,1.),'v1':(.96,1.)},
      'exact_point_example':{
        's0':(.8,.8),'s1':(.6,.6),'v0':(1.,1.),'v1':(.9,.9)}
    }
    result={'status':'EXACT_PARAMETER_INTERVAL_ROBUSTNESS_NO_ANIMALS',
            'results':{k:bound_value(v) for k,v in cases.items()},
            'all_ranges_illustrative_not_statistical_CIs':True}
    (root/'stage22_assumed_parameter_rectangle_bounds.json').write_text(
        json.dumps(result,indent=2,allow_nan=False))
    print('STAGE22_ASSUMED_INTERVAL_ROBUSTNESS '+json.dumps({
      'status':result['status'],
      'robust_case_statuses':{k:v['status'] for k,v in result['results'].items()},
      'real_bees':0},allow_nan=False),flush=True)
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='stage22_exact_outputs')
    main(ap.parse_args().out)
