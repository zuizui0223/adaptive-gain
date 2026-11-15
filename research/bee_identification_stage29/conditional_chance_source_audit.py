"""Stage29: source-locked, assumption-gated chance-control identification audit.

The author-published (2026) information-seeking CSV does NOT report Zone2
true target side, the bee's Zone2 chosen side, assignment schedules, or
original colony identifiers. This tool proves a CONDITIONAL mathematical
incompatibility, not biological maladaptation or publication misconduct.

Two different diagnostics must not be conflated:
  1. Binomial lower tail only under IID Bernoulli(.5) outcomes for the
     selectively retained no-cue trials (including noninformative selection).
  2. A fixed-lambda test-martingale e-value: IF before each selected trial,
     fair correct-side randomization remains unpredictable conditional on
     behavior and previous trials, then predictable selection can be allowed.
The calculation is RETROSPECTIVE; lambda=1 was NOT prospectively registered
by the source authors, and no recorded randomization log verifies the null.
Neither statistic should be advertised as a confirmatory animal p-value.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

EARLIER=Path(__file__).resolve().parents[1] / 'bee_original_audit_stage26'
sys.path.insert(0,str(EARLIER))
from audit_author_request_semantics import (  # noqa: E402
    audit_csv_bytes, AUTHOR_REPO, AUTHOR_COMMIT,
    SOURCE_PATH, SOURCE_BLOB_SHA1,
)

FIELDS_REQUIRING_ORIGINAL_SOURCE=(
    'true_correct_target_side',
    'actual_bee_chosen_side',
    'target_side_randomization_schedule_and_seed',
    'event_time_of_target_assignment',
    'individual_original_colony_id',
    'raw_video_or_blinded_scorer_identity',
)
SUGGESTED_SCHEMA_CANDIDATES={
  'target_side':('Correct_Target_Side','Target_Side','Correct_Answer','Target_Position'),
  'chosen_side':('Chosen_Target_Side','Choice_Side','Bee_Choice','Zone2_Choice'),
  'colony_id':('Colony_ID','Colony','Original_Colony_ID'),
  'randomization':('Target_Assignment_Seed','Assignment_Block','Randomization_ID'),
}


def exact_binom_lower_tail(n,k):
    """Integer-exact numerator and denominator; presentation may be float."""
    if type(n) is not int or type(k) is not int or n<1 or k<0 or k>n:
        raise ValueError('NO_GO_INVALID_BINOMIAL_COUNTS')
    choose=1
    total=1
    for i in range(1,k+1):
        choose=choose*(n-i+1)//i
        total+=choose
    denominator=1<<n
    return {
      'n':n, 'correct_at_most':k, 'assumed_success_rate':0.5,
      'lower_tail_probability':total/denominator,
      'probability_expression':f'sum(comb({n},i) for i=0..{k}) / 2**{n}',
      'exact_integer_numerator':str(total),
      'exact_integer_denominator':str(denominator),
      'ASSUMPTION':'fixed or non-informatively selected n Bernoulli(1/2) correct labels, independent across trials',
      'not_a_confirmatory_inference':True,
    }


def fixed_lambda_martingale(n,k,lam=1.0):
    """Diagnostics under predictable selection and conditional fair outcomes.

    M_n=exp(lam*(n/2-k)) / cosh(lam/2)**n is a fair-null test
    martingale when selected Bernoulli success outcomes are conditionally
    fair and the trial-selection rule is predictable. Ville bound for
    a *fixed, preregistered* lambda: P(sup_t M_t >= M_obs)<=1/M_obs.
    Data inspected before Stage29; do NOT assert preregistration here.
    """
    if type(n) is not int or type(k) is not int or not 0<=k<=n or n<1:
        raise ValueError('NO_GO_INVALID_MARTINGALE_COUNTS')
    if type(lam) not in (int,float) or not math.isfinite(lam) or lam<=0:
        raise ValueError('NO_GO_INVALID_FIXED_LAMBDA')
    log_e=lam*(n/2-k)-n*math.log(math.cosh(lam/2))
    return {
      'fixed_lambda_demonstration':lam,
      'log_e_value':log_e,
      'e_value':math.exp(log_e) if log_e<700 else None,
      'ville_inverse_bound_if_lambda_fixed_a_priori':math.exp(-log_e) if log_e<700 else None,
      'ASSUMPTION':'each selected no-cue correct response is conditionally fair Bernoulli(1/2) given prior decisions; selection predictable before unobservable random correct side',
      'SOURCE_RANDOMIZATION_NOT_VERIFIED':True,
      'RETROSPECTIVE_CALCULATION_NOT_PREREGISTERED':True,
      'NOT_EMPIRICAL_ANIMAL_P_VALUE':True
    }


def source_schema_audit(source, crossmodal=None, memory=None):
    prior=audit_csv_bytes(source,verify_source=True)
    header=tuple(next(csv.reader(io.StringIO(source.decode('utf-8-sig')))))
    found={k:[name for name in options if name in header]
           for k,options in SUGGESTED_SCHEMA_CANDIDATES.items()}
    experiments={}
    other=[('cross_modal',crossmodal,
            'a5d895061565c06b7d2045bc128773000d2778e5'),
           ('memory',memory,
            '355e3cc6a5908e33671ea18ffd6f1bf8edd31cd3')]
    for label,blob,sha in other:
        if blob is None:
            experiments[label]={'status':'NOT_SUPPLIED_FOR_SCHEMA_COMPARISON'}
            continue
        if not isinstance(blob,bytes):
            raise ValueError('NO_GO_OTHER_SOURCE_NOT_BYTES')
        digest=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()
        if digest!=sha:
            raise ValueError('NO_GO_OTHER_PUBLIC_SOURCE_BLOB_MISMATCH')
        cols=tuple(next(csv.reader(io.StringIO(blob.decode('utf-8-sig')))))
        experiments[label]={
          'status':'AUTHOR_OTHER_EXPERIMENT_SCHEMA_VERIFIED',
          'expected_blob_sha1':sha, 'actual_blob_sha1':digest,
          'has_correct_answer':('Correct_Answer' in cols),
          'has_bee_choice':('Bee_Choice' in cols),
          'these_records_are_NOT_linkable_as_zone2_truth':True
        }
    return prior,header,found,experiments


def source_no_cue_outcomes(source):
    prior=audit_csv_bytes(source,verify_source=True)
    rd=csv.DictReader(io.StringIO(source.decode('utf-8-sig')))
    units=defaultdict(lambda:[0,0])
    period=defaultdict(lambda:[0,0])
    counts=[0,0]
    for row in rd:
        if (row['Trial_Type'],row['Difficulty'],row['Info_Requested'],
                row['Actually_Landed_On_Platform']) != ('Regular','Impossible','0','0'):
            continue
        correct=row['Is_Post_Non_Request_Correct']
        if correct not in ('0.0','1.0','0','1'):
            raise ValueError('NO_GO_MISSING_BINARY_NO_CUE_OUTCOME')
        y=int(float(correct))
        bee=row['Bee_ID']
        idx=int(row['Trial_Number'])
        group='Early' if idx<=50 else 'Late'
        for v in (units[bee],period[group],counts):
            v[0]+=1;v[1]+=y
    if not units:
        raise ValueError('NO_GO_MISSING_IMPOSSIBLE_NO_CUE')
    if prior['source_trial_rows'] != 19200 or len(units)!=192:
        raise ValueError('NO_GO_SOURCE_GRAIN_MISMATCH')
    if counts != [883,183] or period['Early'] != [442,81] or period['Late'] != [441,102]:
        raise ValueError('NO_GO_FROZEN_NO_CUE_COUNTS_DIFFER')
    per_bee={
      'n_bees':len(units),
      'below_half':sum(2*v[1]<v[0] for v in units.values()),
      'equal_half':sum(2*v[1]==v[0] for v in units.values()),
      'above_half':sum(2*v[1]>v[0] for v in units.values()),
      'mean_equal_bee_accuracy':sum(v[1]/v[0] for v in units.values())/len(units),
      'n_trials_per_bee_min':min(v[0] for v in units.values()),
      'n_trials_per_bee_max':max(v[0] for v in units.values()),
    }
    if (per_bee['below_half'],per_bee['equal_half'],per_bee['above_half'])!=(170,12,10):
        raise ValueError('NO_GO_PER_BEE_NEGATIVE_CONTROL_DIFFERENT')
    return {
      'n':counts[0], 'correct':counts[1], 'accuracy':counts[1]/counts[0],
      'early_late':{name:{'n':v[0],'correct':v[1],'accuracy':v[1]/v[0]}
                    for name,v in sorted(period.items())},
      'per_bee':per_bee
    }


def source_identification_receipt(source,crossmodal=None,memory=None):
    _,header,found,comparison=source_schema_audit(source,crossmodal,memory)
    outcomes=source_no_cue_outcomes(source)
    n,k=outcomes['n'],outcomes['correct']
    # If target side is independent of a bee's selected answer and has
    # frequency t on side L, then P(correct)=t*pchooseL+(1-t)*(1-pchooseL)
    # so min possible agreement over arbitrary choice bias is min(t,1-t).
    # Achieving observed p<.5 requires t<=p or t>=1-p. That is a
    # NECESSARY condition under this intentionally simplified model, not
    # evidence of an actual target-side bias in the experiment.
    min_bias=.5-k/n
    receipt={
      'status':'STRICT_HYPOTHETICAL_FAIR_ASSIGNMENT_NULL_REJECTED_BUT_SOURCE_IDENTIFICATION_NO_GO',
      'source_repo':AUTHOR_REPO,'author_commit':AUTHOR_COMMIT,
      'source_path':SOURCE_PATH,'source_blob_sha1':SOURCE_BLOB_SHA1,
      'source_rows':19200,'bee_ids':192,
      'source_header':list(header),
      'source_column_presence':{name:len(cols)>0 for name,cols in found.items()},
      'other_author_experiment_schema':comparison,
      'impossible_regular_nocue':outcomes,
      'ideal_IID_fair_label_conditional_tail':exact_binom_lower_tail(n,k),
      'predictable_selection_fixed_lambda_diagnostic':fixed_lambda_martingale(n,k,1.0),
      'side_balance_sensitivity_IF_target_side_independent_of_choice':{
          'minimum_absolute_imbalance_from_half':min_bias,
          'minimum_required_more_common_side_fraction':1-k/n,
          'logic':'For target-left rate t independent of chosen side and chosen-left rate a, correctness=t*a+(1-t)*(1-a), which is >=min(t,1-t). With observed correctness below 1/2, reproducing it by side imbalance ALONE requires t<=observed rate or t>=1-observed rate.',
          'not_a_measured_randomization_imbalance':True
      },
      'nonidentification_counterexamples':{
          'A_no_information_but_target_side_imbalanced':'Hypothetically always choose L; correct target assigned to L with probability 183/883. Then observed correctness is 183/883 although bee receives no target signal.',
          'B_fair_target_but_anti_correlated_scoring_or_leak':'Hypothetically target side fair yet chosen/scored side matches true target with probability 183/883 through an unobserved correlated signal or coding rule. Same observable Bernoulli correct rate; mechanism differs.',
          'not_claimed_to_represent_real_bees':True
      },
      'irrecoverable_from_this_csv':list(FIELDS_REQUIRING_ORIGINAL_SOURCE),
      'requirements_to_identify_chance_null':[
          'Prespecified target assignment probabilities conditional on trial, bee, request decision, and history',
          'Original correct target left/right, actual bee chosen left/right before feedback',
          'Cue timing and hidden allocation logs, including seed or independently auditable assignment protocol',
          'Original colony identifiers to quantify between-colony uncertainty'
      ],
      'not_confirmatory_p_value':True,
      'not_proof_of_animal_maladaptation':True,
      'not_allegation_of_publication_misconduct':True,
      'no_new_live_animals':True,
      'no_original_csv_redistributed':True,
      'stage24_optimal_information_fitness_empirically_validated':False
    }
    if all(receipt['source_column_presence'].values()):
        raise ValueError('NO_GO_SCHEMA_CHANGED_ALL_SOURCE_FIELDS_AVAILABLE')
    if n!=883 or k!=183:
        raise ValueError('NO_GO_ORIGINAL_CONTRAST_CHANGED')
    return receipt


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--input')
    ap.add_argument('--crossmodal')
    ap.add_argument('--memory')
    ap.add_argument('--out',default='stage29_source_diagnostic_receipts')
    args=ap.parse_args(argv)
    if not args.input:
        value={'status':'NO_GO_ORIGINAL_AUTHOR_TRIAL_FILE_UNAVAILABLE',
               'original_source_animals_verified':0,
               'no_empirical_adaptation_claim':True}
    else:
        value=source_identification_receipt(
          Path(args.input).read_bytes(),
          Path(args.crossmodal).read_bytes() if args.crossmodal else None,
          Path(args.memory).read_bytes() if args.memory else None
        )
    root=Path(args.out);root.mkdir(parents=True,exist_ok=True)
    (root/'stage29_conditional_chance_source_no_go.json').write_text(
        json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf-8')
    print(json.dumps({
      'status':value['status'],
      'observed_unqueried_impossible_success':value.get('impossible_regular_nocue'),
      'no_new_live_animals':True
    },sort_keys=True,ensure_ascii=False))


if __name__=='__main__':
    main()
