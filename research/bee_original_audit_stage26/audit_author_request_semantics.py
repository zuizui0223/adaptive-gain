"""Stage26: immutable public-author trial CSV semantics audit, not new bees.

Author-public source: Cuixiaojian21/bee_metacognition, 2026, data/4_active...
Pin both commit and byte-level Git SHA1 blob ID. Never vendor trial CSV into
adaptive-gain: license is not specified by the source GitHub repository.

Most importantly: the source variable Info_Requested is ALWAYS 1 in
Random_Free_Cue trials even when the animal never actually lands. It must
NOT be read as an animal-initiated paid request across the whole dataset.
Regular-trial platform landings are the operational paid-request action.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path

AUTHOR_REPO = 'Cuixiaojian21/bee_metacognition'
AUTHOR_COMMIT = '7f886394b4de872ecdb19ca4ea214ec321d5dce9'
SOURCE_PATH = 'data/4_active_information_seeking_trials.csv'
SOURCE_BLOB_SHA1 = '26259c9071c6d73141d56b9bedd396cab1a04491'
AUTHOR_PINNED_URL = (
    f'https://raw.githubusercontent.com/{AUTHOR_REPO}/{AUTHOR_COMMIT}/{SOURCE_PATH}'
)
COLUMNS = (
  'Trial_ID', 'Bee_ID', 'Trial_Number', 'Difficulty', 'Trial_Type',
  'Info_Requested', 'Actually_Landed_On_Platform',
  'Post_Request_Accuracy', 'Is_Post_Request_Correct',
  'Non_Request_Accuracy', 'Is_Post_Non_Request_Correct'
)
DIFFICULTY=('Easy','Hard','Impossible')
TYPES=('Regular','Random_Free_Cue')
EXPECTED_COUNTS={
  ('Regular','Easy'):(6140,591,591),
  ('Regular','Hard'):(6108,2866,2866),
  ('Regular','Impossible'):(3112,2229,2229),
  ('Random_Free_Cue','Easy'):(1540,1540,950),
  ('Random_Free_Cue','Hard'):(1572,1572,925),
  ('Random_Free_Cue','Impossible'):(728,728,153),
}


def _blob_sha1(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def _count_as_int(value,name):
    if value not in ('0','1'):
        raise ValueError('NO_GO_NONBINARY_'+name.upper())
    return int(value)


def _correctness_as_binary(value,name):
    # The author CSV encodes outcome indicators as decimal 0.0/1.0,
    # unlike actual request and platform landing flags (integer 0/1).
    if value not in ('0','1','0.0','1.0'):
        raise ValueError('NO_GO_NONBINARY_'+name.upper())
    return int(float(value))


def _new_stats():
    return {'trials':0,'info_requested':0,'actual_landing':0,
            'flagged_without_landing':0,'landed_without_flag':0,
            'post_request_correct':0,'post_request_trials':0,
            'post_non_request_correct':0,'post_non_request_trials':0}


def audit_csv_bytes(source_bytes,verify_source=True):
    if not isinstance(source_bytes,bytes):
        raise ValueError('NO_GO_SOURCE_NOT_BYTES')
    digest=_blob_sha1(source_bytes)
    if verify_source and digest!=SOURCE_BLOB_SHA1:
        raise ValueError('NO_GO_AUTHOR_SOURCE_BLOB_SHA_MISMATCH')
    try:
        text=source_bytes.decode('utf-8-sig')
    except UnicodeDecodeError as err:
        raise ValueError('NO_GO_INVALID_SOURCE_ENCODING') from err
    reader=csv.DictReader(io.StringIO(text))
    if tuple(reader.fieldnames or ())!=COLUMNS:
        raise ValueError('NO_GO_AUTHOR_SOURCE_SCHEMA_MISMATCH')
    groups=defaultdict(_new_stats)
    per_bee=defaultdict(lambda:defaultdict(lambda:[0,0]))
    seen=set()
    bee_trials=defaultdict(set)
    rows=0
    for row in reader:
        if None in row or any(row.get(k) is None for k in COLUMNS):
            raise ValueError('NO_GO_CORRUPTED_CSV_ROW')
        try:
            tid=int(row['Trial_ID'])
            number=int(row['Trial_Number'])
        except ValueError as err:
            raise ValueError('NO_GO_INVALID_TRIAL_INDEX') from err
        bee=row['Bee_ID']
        if not bee or tid in seen or number in bee_trials[bee]:
            raise ValueError('NO_GO_DUPLICATED_TRIAL_OR_BEE_SESSION')
        if row['Difficulty'] not in DIFFICULTY or row['Trial_Type'] not in TYPES:
            raise ValueError('NO_GO_INVALID_SOURCE_TREATMENT')
        seen.add(tid)
        bee_trials[bee].add(number)
        req=_count_as_int(row['Info_Requested'],'info_requested')
        land=_count_as_int(row['Actually_Landed_On_Platform'],'actual_landing')
        typ=row['Trial_Type']
        difficulty=row['Difficulty']
        if typ=='Regular' and req!=land:
            raise ValueError('NO_GO_REGULAR_REQUEST_NOT_ACTUAL_LANDING')
        if typ=='Random_Free_Cue' and req!=1:
            raise ValueError('NO_GO_FREE_CUE_FLAG_NOT_EXPOSURE_INDICATOR')
        if req==1:
            if row['Is_Post_Non_Request_Correct']!='':
                raise ValueError('NO_GO_OUTCOME_BRANCH_LEAKAGE')
            post=_correctness_as_binary(row['Is_Post_Request_Correct'],'post_request_correct')
        else:
            if row['Is_Post_Request_Correct']!='':
                raise ValueError('NO_GO_OUTCOME_BRANCH_LEAKAGE')
            post=_correctness_as_binary(row['Is_Post_Non_Request_Correct'],'non_request_correct')
        g=groups[(typ,difficulty)]
        g['trials']+=1
        g['info_requested']+=req
        g['actual_landing']+=land
        g['flagged_without_landing']+=int(req==1 and land==0)
        g['landed_without_flag']+=int(req==0 and land==1)
        outcome='post_request' if req else 'post_non_request'
        g[outcome+'_trials']+=1
        g[outcome+'_correct']+=post
        counts=per_bee[bee][(typ,difficulty)]
        counts[0]+=1
        counts[1]+=land
        rows+=1

    if verify_source:
        if rows!=19200 or len(bee_trials)!=192 or set(seen)!=set(range(1,19201)):
            raise ValueError('NO_GO_PUBLISHED_SOURCE_CARDINALITY_CHANGED')
        if any(nums!=set(range(1,101)) for nums in bee_trials.values()):
            raise ValueError('NO_GO_100_TRIALS_PER_BEE_NOT_REPRODUCED')
        for name, expected in EXPECTED_COUNTS.items():
            got=groups[name]
            if (got['trials'],got['info_requested'],got['actual_landing'])!=expected:
                raise ValueError('NO_GO_LOCKED_AUTHOR_SOURCE_COUNTS_DIFFER')

    outputs=[]
    for name in sorted(groups):
        g=groups[name]
        n=g['trials']
        outputs.append({
           'trial_type':name[0], 'difficulty':name[1],**g,
           'info_request_flag_fraction':g['info_requested']/n,
           'platform_landing_fraction':g['actual_landing']/n,
           'exposure_flag_without_landing_fraction':g['flagged_without_landing']/n
        })
    descriptive=[]
    for d in DIFFICULTY:
        diffs=[]
        for bee,counters in per_bee.items():
            a=counters.get(('Regular',d))
            b=counters.get(('Random_Free_Cue',d))
            if a and b:
                diffs.append(b[1]/b[0]-a[1]/a[0])
        descriptive.append({
            'difficulty':d,
            'paired_bee_count':len(diffs),
            'mean_bee_level_landing_change_free_minus_regular':(
                sum(diffs)/len(diffs) if diffs else None),
            'positive_bees':sum(x>0 for x in diffs),
            'negative_bees':sum(x<0 for x in diffs),
            'tied_bees':sum(x==0 for x in diffs),
            'not_colony_independent_statistical_test':True
        })
    group_total={typ:{k:sum(g[k] for (t,d),g in groups.items() if t==typ)
                      for k in ('trials','info_requested','actual_landing','flagged_without_landing')}
                 for typ in TYPES}
    return {
        'status':'PUBLIC_AUTHOR_TRIAL_TABLE_SEMANTICS_REPRODUCED' if verify_source
                  else 'SYNTHETIC_INTERNAL_QA_ONLY',
        'author_repo':AUTHOR_REPO, 'pinned_commit':AUTHOR_COMMIT,
        'source_path':SOURCE_PATH, 'source_git_blob_sha1_expected':SOURCE_BLOB_SHA1,
        'source_git_blob_sha1_observed':digest,
        'source_trial_rows':rows,'unique_bee_ids':len(bee_trials),
        'trial_type_totals':group_total,
        'difficulty_strata':outputs,
        'within_bee_descriptive_contrasts':descriptive,
        'naive_cross_treatment_request_flag_total':sum(g['info_requested'] for g in groups.values()),
        'all_platform_landings_total':sum(g['actual_landing'] for g in groups.values()),
        'free_cue_flag_without_landing_total':group_total.get('Random_Free_Cue',{}).get('flagged_without_landing',0),
        'strict_regular_paid_animal_initiated_landings':group_total.get('Regular',{}).get('actual_landing',0),
        'strict_paid_request_rule':'Regular AND Actually_Landed_On_Platform==1; Free_Cue info flag=exposure, NOT self-chosen paid information',
        'free_cue_landing_not_paid_request':True,
        'source_original_instrumentation_and_colony_ids_not_independently_verified':True,
        'not_equivalent_to_stage24_six_class_confusion':True,
        'stage25_eight_parameter_empirical_ci_ready':False,
        'missing_stage25_inputs':['independent original colony IDs','Z/U/V true0/true1 recognition outcomes','learned branch prior q','calibrated c','randomized precommit/contingent net rewards'],
        'no_new_animals':True,'not_evolved_cognition_or_fitness_inference':True,
        'no_trial_data_redistributed':True,
        'raw_data_license_not_specified_in_source_repository':True
    }


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',default=None)
    ap.add_argument('--out',default='stage26_author_source_receipts')
    args=ap.parse_args(argv)
    if args.input is None:
        result={'status':'NO_GO_PUBLIC_AUTHOR_CSV_NOT_PROVIDED',
                'source_trial_rows':0,'no_new_animals':True,
                'not_equivalent_to_stage24_six_class_confusion':True}
    else:
        result=audit_csv_bytes(Path(args.input).read_bytes())
    folder=Path(args.out);folder.mkdir(parents=True,exist_ok=True)
    (folder/'stage26_request_semantics_audit.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',
        encoding='utf-8')
    print(json.dumps({'status':result['status'],
                      'source_trial_rows':result['source_trial_rows'],
                      'no_new_animals':True},sort_keys=True))


if __name__=='__main__':
    main()
