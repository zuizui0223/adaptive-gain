"""Stage25: source-traceable class-wise recognition CI gate (NO biological result).

Original individual animals, not video frames or repeated trials, are the
nominal independent sampling units for each colony x cue x true-class rate.
Intervals are equal-tailed exact binomial (Clopper-Pearson) intervals with
Bonferroni simultaneous error budget 0.05 over SIX classes times all colonies.

This conditional statistical statement assumes sampled bees are independent
and identically distributed within each original colony and source class.
Neither this assumption nor the authenticity of a declared-original source
is established by a self-reported JSON flag. q/c intervals are supplied
EXTERNALLY, not inferred from choice/sucrose records in this stage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

STAGE24 = Path(__file__).resolve().parents[1] / 'bee_robust_stage24'
sys.path.insert(0, str(STAGE24))
from exact_rectangle_certificate import certify  # noqa: E402

SOURCE_CLASSES = ('s0','s1','u0','u1','v0','v1')
SOURCE_TO_KEY = {('Z',0):'s0',('Z',1):'s1',
                 ('U',0):'u0',('U',1):'u1',
                 ('V',0):'v0',('V',1):'v1'}
STUDY_FLAGS = ('independent_bee_sampling_by_class',
               'randomized_and_blinded_true_classes',
               'source_specific_isolation_verified',
               'recorded_before_correctness_feedback')
JOINT_ALPHA = 0.05
CI_DECIMALS = 6
MAX_ROWS = 500000
MAX_COLONIES = 20


def _upper_binomial_tail(n,k,p):
    """P[Binomial(n,p)>=k], using a log first term and a recurrence."""
    if k<=0:return 1.
    if p<=0:return 0.
    if p>=1:return 1.
    t=math.exp(math.lgamma(n+1)-math.lgamma(k+1)-
               math.lgamma(n-k+1)+k*math.log(p)+(n-k)*math.log1p(-p))
    result=t
    ratio=p/(1-p)
    for i in range(k,n):
        t*=((n-i)/(i+1))*ratio
        result+=t
    return max(0.,min(1.,result))


def _invert_upper_tail(n,k,target):
    """Increasing binomial-tail inversion (bracketing, 65 iterations)."""
    a,b=0.,1.
    for _ in range(65):
        mid=(a+b)/2
        if _upper_binomial_tail(n,k,mid)<target:a=mid
        else:b=mid
    return b


def cp_interval(k,n,individual_alpha):
    """Outward-rounded conservative exact 1-alpha class-rate interval.

    Only valid for independent Bernoulli sampling units; do not supply
    multiple frames or repeat trials from the same bee in one class.
    """
    if not(type(k) is int and type(n) is int and 0<=k<=n and n>=1):
        raise ValueError('NO_GO_INVALID_CLASS_COUNTS')
    if not 0<individual_alpha<1:
        raise ValueError('NO_GO_ALPHA')
    tail=individual_alpha/2
    lo=0. if k==0 else _invert_upper_tail(n,k,tail)
    hi=1. if k==n else 1.-_invert_upper_tail(n,n-k,tail)
    # Directed OUTWARD rounding with guard > numerical bisection error.
    scale=10**CI_DECIMALS
    lo_floor=max(0,math.floor((lo-1e-11)*scale))/scale
    hi_ceil=min(scale,math.ceil((hi+1e-11)*scale))/scale
    return (f'{lo_floor:.{CI_DECIMALS}f}',f'{hi_ceil:.{CI_DECIMALS}f}')


def _timestamp(raw):
    if not isinstance(raw,str):
        raise ValueError('NO_GO_MISSING_TIMESTAMP')
    try:
        val=datetime.fromisoformat(raw.replace('Z','+00:00'))
    except ValueError as err:
        raise ValueError('NO_GO_BAD_TIMESTAMP') from err
    if val.tzinfo is None or val.utcoffset() is None:
        raise ValueError('NO_GO_NAIVE_TIMESTAMP')
    return val


def _string(x,label):
    if not isinstance(x,str) or not x or len(x)>250:
        raise ValueError('NO_GO_BAD_'+label)
    return x


def _study_and_raw_rows(payload):
    if not isinstance(payload,dict) or not isinstance(payload.get('manifest'),dict):
        raise ValueError('NO_GO_MISSING_SOURCE_MANIFEST')
    manifest=payload['manifest']
    rows=payload.get('trials')
    if not isinstance(rows,list) or not rows:
        return manifest,[],{},{}
    if len(rows)>MAX_ROWS:raise ValueError('NO_GO_TOO_MANY_ROWS')
    if manifest.get('source_kind') not in ('mock','declared_original_unverified'):
        raise ValueError('NO_GO_BAD_SOURCE_KIND')
    if any(manifest.get(k) is not True for k in STUDY_FLAGS):
        raise ValueError('NO_GO_SOURCE_DESIGN_MISSING')
    given=manifest.get('trial_data_sha256')
    digest=hashlib.sha256(json.dumps(rows,sort_keys=True,
        separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()
    if not isinstance(given,str) or not re.fullmatch(r'[0-9a-f]{64}',given) or given!=digest:
        raise ValueError('NO_GO_TRIAL_DIGEST_MISMATCH')
    if manifest['source_kind']=='declared_original_unverified':
        _string(manifest.get('ethics_reference'),'ETHICS_REFERENCE')
        _string(manifest.get('original_source_uri'),'ORIGINAL_SOURCE_URI')
    counts=defaultdict(lambda:{k:[0,0] for k in SOURCE_CLASSES})
    seen_trials=set()
    seen_units=set()
    bee_home={}
    for row in rows:
        if not isinstance(row,dict):raise ValueError('NO_GO_NON_RECORD')
        trial=_string(row.get('trial_id'),'TRIAL_ID')
        bee=_string(row.get('bee_id'),'BEE_ID')
        colony=_string(row.get('colony_id'),'COLONY_ID')
        source=row.get('cue')
        true_bit=row.get('true_bit')
        reported=row.get('reported_bit')
        if source not in ('Z','U','V') or type(true_bit)is not int or \
           type(reported)is not int or true_bit not in (0,1) or reported not in (0,1):
            raise ValueError('NO_GO_INVALID_SOURCE_CLASS')
        if row.get('original_response_blinded') is not True or \
           row.get('other_sources_hidden') is not True or \
           row.get('reward_hidden') is not True:
            raise ValueError('NO_GO_RESPONSE_LEAKAGE')
        cue_time=_timestamp(row.get('cue_time_utc'))
        response_time=_timestamp(row.get('response_time_utc'))
        feedback_time=_timestamp(row.get('feedback_time_utc'))
        if not cue_time < response_time < feedback_time:
            raise ValueError('NO_GO_FEEDBACK_BEFORE_RESPONSE')
        key=SOURCE_TO_KEY[(source,true_bit)]
        unit=(colony,bee,key)
        if trial in seen_trials or unit in seen_units:
            raise ValueError('NO_GO_PSEUDO_REPLICATED_TRIAL')
        if bee in bee_home and bee_home[bee]!=colony:
            raise ValueError('NO_GO_BEE_IN_MULTIPLE_COLONIES')
        seen_trials.add(trial)
        seen_units.add(unit)
        bee_home[bee]=colony
        counts[colony][key][1]+=1
        counts[colony][key][0]+=int(reported==true_bit)
    if len(counts)>MAX_COLONIES:raise ValueError('NO_GO_EXCESS_COLONIES')
    return manifest,rows,counts,bee_home


def _bound_q_cost(manifest):
    bounds={}
    for param in ('q','c'):
        raw=manifest.get(param+'_interval')
        if not isinstance(raw,(list,tuple)) or len(raw)!=2:
            return None
        try:
            lo,hi=(F(x) for x in raw)
        except (TypeError,ValueError,ZeroDivisionError) as err:
            raise ValueError('NO_GO_NONRATIONAL_Q_OR_COST') from err
        if lo<0 or hi<lo or (param=='q' and hi>F(1,2)):
            raise ValueError('NO_GO_INVALID_Q_OR_COST')
        bounds[param]=[str(lo),str(hi)]
    return bounds


def _recognition_results(counts,extra_bounds):
    colonies=sorted(counts)
    assert colonies
    indiv_alpha=JOINT_ALPHA/(len(colonies)*len(SOURCE_CLASSES))
    out={}
    for colony in colonies:
        rates={}
        for k in SOURCE_CLASSES:
            correct,total=counts[colony][k]
            if total==0:
                rates[k]={'status':'NO_GO_MISSING_TRUE_CLASS','n_bees':0}
            else:
                lo,hi=cp_interval(correct,total,indiv_alpha)
                rates[k]={'status':'SOURCE_RATE_CI_ONLY',
                          'correct':correct,'n_bees':total,
                          'class_correct_fraction':correct/total,
                          'cp_interval_outward':[lo,hi]}
        missing=[k for k in SOURCE_CLASSES if counts[colony][k][1]==0]
        if missing:
            bound={'status':'NO_GO_CLASS_MISSING','missing_classes':missing}
        elif extra_bounds is None:
            bound={'status':'NO_GO_Q_OR_COST_CALIBRATION_UNAVAILABLE'}
        else:
            box={k:rates[k]['cp_interval_outward'] for k in SOURCE_CLASSES}
            box.update(extra_bounds)
            if any(F(box[k][0])<F(1,2) for k in SOURCE_CLASSES):
                bound={'status':'NO_GO_SENSORY_INTERVAL_OUTSIDE_STAGE24_DOMAIN',
                       'note':'Do not truncate an empirical CI to [0.5,1]'}
            else:
                cert=certify(box)
                bound={'status':'CONDITIONAL_MODEL_'+cert['status'],
                       'fixed_policy_gap_lower':cert['minimum_fixed_minus_optimal_precommit'],
                       'corner_count':cert['corner_count'],
                       'no_empirical_certification':True}
        out[colony]={'recognition_rates':rates,'conditional_model':bound}
    return out


def audit(payload):
    manifest,rows,counts,bee_home=_study_and_raw_rows(payload)
    if not rows:
        return {
          'status':'NO_GO_NO_ORIGINAL_TRIALS',
          'n_original_animals_verified':0,
          'biological_positive_claim':False,
          'no_fabricated_observations':True,
          'next_required_input':'independent original bee-by-source-class trials plus authenticated q/c calibration'}
    bounds=_bound_q_cost(manifest)
    groups=_recognition_results(counts,bounds)
    return {
      'status':'MOCK_ONLY_NO_BIOLOGICAL_INFERENCE' if manifest['source_kind']=='mock'
        else 'SOURCE_DECLARED_ORIGINAL_BUT_UNAUTHENTICATED',
      'n_rows':len(rows),'n_colonies':len(counts),'unique_bee_ids':len(bee_home),
      'trials_sha256':manifest['trial_data_sha256'],
      'nominal_joint_recognition_coverage':0.95,
      'covered_parameters':'six source-class rates PER COLONY, under independent bees and stationary Bernoulli outcomes; Bonferroni over colonies/classes',
      'q_and_c_interval_status':'EXTERNALLY_ASSUMED_NOT_COVERED_BY_THIS_CI' if bounds
                              else 'NO_GO_MISSING_CALIBRATION',
      'per_colony':groups,
      'independence_source_proof_verified':False,
      'joint_source_noise_dependence_tested':False,
      'animal_policy_choices_measured':False,
      'precommit_vs_contingent_reward_RCT_completed':False,
      'biological_positive_claim':False,
      'why_not_biological':'Internal raw-table consistency and CIs do not prove original data authenticity, independence, learned priors, full 8D coverage, voluntary paid queries, or actual payoff.',
    }


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--input',default=None,help='Original or mock manifest+trials JSON; if omitted refuse')
    p.add_argument('--out',default='stage25_source_gate_outputs')
    opts=p.parse_args(argv)
    if opts.input:
        payload=json.loads(Path(opts.input).read_text(encoding='utf-8'))
    else:
        payload={'manifest':{'source_kind':'missing'},'trials':[]}
    receipt=audit(payload)
    folder=Path(opts.out);folder.mkdir(parents=True,exist_ok=True)
    (folder/'stage25_recognition_source_gate.json').write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':receipt['status'],
                      'biological_positive_claim':receipt['biological_positive_claim'],
                      'n_original_animals_verified':receipt.get('n_original_animals_verified',0)},
                     sort_keys=True))


if __name__=='__main__':
    main()
