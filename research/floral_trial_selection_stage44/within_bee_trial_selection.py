"""Stage44: EXACT within-bee original-trajectory selection envelopes.

Original archived 2016 Chang/Crall/Combes bee flight files, Zenodo #60234.
Reuses authenticated source parser and Stage41 independent 3-D filtering.
Compared with Stage43, whole original B identifiers remain FIXED.
Instead choose ONE of the eligible original 3-D flight trajectories in each
observed matched (B, S, P, W) cell. The worst and best contrasts are
analytically exact by independent cellwise minimization/maximization:
    lower(B,S,P) = min_W1(speed) - max_W0(speed);
    upper(B,S,P) = max_W1(speed) - min_W0(speed).
Cells and original B numbers are equal-weighted as in Stages41–43.
An explicitly *different* second bound picks a single matched S/P cell
per B instead of all matching cells. These are conditional observed-file
extrema, NOT intervals for missing 112 manuscript-selected trajectories,
population CIs, causal effects, or plant fitness.
"""
from __future__ import annotations

from collections import Counter,defaultdict
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
for sub in ('floral_wind_kinematic_stage39','floral_landing_sensitivity_stage41',
            'floral_original_selection_stage42'):
    sys.path.insert(0,str(ROOT/sub))
from inspect_original_tracks import source_original_archive,FILENAME_PATTERN,MEASURED_HEADER
from preprocessing_sensitivity import reconstruct_all_filters,CUTOFFS,SPEED_METHODS
from author_archive_condition_audit import SOURCE_SHA256,author_script_semantics

EXPECTED_W={'W0':56,'W1':101}
METHOD_KEYS=tuple((hz,method) for hz in CUTOFFS for method in SPEED_METHODS)
SUBSETS=(('all',{}),('S0',{'S':'0'}),('S1',{'S':'1'}),
         ('P0',{'P':'0'}),('P1',{'P':'1'}),
         ('S0_P0',{'S':'0','P':'0'}),('S0_P1',{'S':'0','P':'1'}),
         ('S1_P0',{'S':'1','P':'0'}),('S1_P1',{'S':'1','P':'1'}))
ENDPOINTS=(('near_flower_speed',1),('landing_minus_approach_speed',2))


def finite_cells(records,method_key,endpoint,subset=None):
    """Original unmodified eligible file measurements grouped by B/S/P/W."""
    if method_key not in METHOD_KEYS or endpoint not in (1,2):
        raise ValueError('NO_GO_UNREGISTERED_PREPROCESSING_OR_ENDPOINT')
    if subset is None:
        subset={}
    if set(subset)-{'S','P'}:
        raise ValueError('NO_GO_UNKNOWN_SUBSET_DIMENSION')
    cells=defaultdict(lambda:defaultdict(list))
    for row in records:
        if any(row.get(k)!=v for k,v in subset.items()):
            continue
        if any(k not in row for k in ('B','S','P','W','values')):
            raise ValueError('NO_GO_INCOMPLETE_SOURCE_TRAJECTORY_KEY')
        if row['W'] not in EXPECTED_W:
            raise ValueError('NO_GO_NONBINARY_SOURCE_WIND')
        val=row['values'].get(method_key)
        if val is None:
            continue
        if len(val)!=3 or not all(math.isfinite(float(x)) for x in val):
            raise ValueError('NO_GO_NAN_OR_MALFORMED_SOURCE_SPEED')
        cells[(row['B'],row['S'],row['P'])][row['W']].append(float(val[endpoint]))
    return {k:v for k,v in cells.items() if v.get('W0') and v.get('W1')}


def selection_envelope(records,method_key=(100,'three_tag_mean'),
                       endpoint=1,subset=None):
    """Sharp conditional envelopes, retaining original source B ID cohort.

    Regime A: fixed observed matched S/P cells, one eligible trajectory per
    wind arm of each cell, every matched cell given equal within-B weight.
    Regime B: per B freely choose one matched S/P cell, then one trajectory
    from each arm. This is deliberately more permissive, NOT publication
    source selection.
    """
    cells=finite_cells(records,method_key,endpoint,subset)
    per_B=defaultdict(list)
    flexible_cells=0
    fixed_cells=0
    total_eligible_source_files_in_matched_cells=0
    for (B,S,P),wind in sorted(cells.items()):
        a=wind['W0'];b=wind['W1']
        fixed_cells+=1
        total_eligible_source_files_in_matched_cells+=len(a)+len(b)
        flexible_cells+=int(len(a)>1 or len(b)>1)
        baseline=statistics.mean(b)-statistics.mean(a)
        lower=min(b)-max(a)
        upper=max(b)-min(a)
        if not (lower-1e-12<=baseline<=upper+1e-12):
            raise ValueError('NO_GO_MEAN_OUTSIDE_SOURCE_TRIAL_EXTREMA')
        per_B[B].append((baseline,lower,upper,len(a),len(b)))
    if not per_B:
        return {'status':'NO_GO_NO_MATCHED_ORIGINAL_B_IDENTIFIERS',
                'subset':subset or {},'not_a_biological_inference':True}
    original=[];fixed_low=[];fixed_high=[];one_low=[];one_high=[]
    ambiguous_B=0
    for bee,values in sorted(per_B.items()):
        original.append(statistics.mean(v[0] for v in values))
        fixed_low.append(statistics.mean(v[1] for v in values))
        fixed_high.append(statistics.mean(v[2] for v in values))
        one_low.append(min(v[1] for v in values))
        one_high.append(max(v[2] for v in values))
        ambiguous_B+=int(len(values)>1 or any(a>1 or b>1 for _,_,_,a,b in values))
    main=statistics.mean(original)
    result={
      'status':'EXACT_ARCHIVED_TRIAL_SELECTION_ENVELOPES_FIXED_OR_ONE_CELL_PER_B',
      'n_original_B_identifiers':len(per_B),
      'n_source_B_with_at_least_one_optional_cell_or_trial':ambiguous_B,
      'n_original_matched_B_S_P_cells':fixed_cells,
      'n_cells_with_multiple_eligible_original_trajectories_in_either_wind_arm':flexible_cells,
      'n_eligible_source_file_appearances_in_matched_cells':total_eligible_source_files_in_matched_cells,
      'original_within_B_S_P_all_trial_mean_m_s':main,
      'fixed_matched_cells_one_original_trial_per_arm_exact_lower_m_s':statistics.mean(fixed_low),
      'fixed_matched_cells_one_original_trial_per_arm_exact_upper_m_s':statistics.mean(fixed_high),
      'any_one_matched_cell_per_B_one_original_trial_per_arm_exact_lower_m_s':statistics.mean(one_low),
      'any_one_matched_cell_per_B_one_original_trial_per_arm_exact_upper_m_s':statistics.mean(one_high),
      'B_with_positive_fixed_cell_worst_case':sum(x>0 for x in fixed_low),
      'B_with_nonpositive_fixed_cell_worst_case':sum(x<=0 for x in fixed_low),
      'B_with_positive_one_cell_worst_case':sum(x>0 for x in one_low),
      'B_with_nonpositive_one_cell_worst_case':sum(x<=0 for x in one_low),
      'all_matched_B_retained_no_B_deletion':True,
      'selection_rule_replaces_all_original_eligible_replicates_in_a_cell_with_one_each':True,
      'exactness':'Separable linear equal-B and equal-cell averages; each paired-cell difference reaches extrema at minimum windy and maximum still speed, or vice versa.',
      'not_matching_original_author_112_trial_roster':True,
      'does_not_protect_against_unarchived_paths_or_B_subsets':True,
      'not_a_colony_population_CI_or_randomized_wind_effect':True,
      'not_landing_success_or_pollen_or_seeds_or_fitness':True
    }
    if (result['fixed_matched_cells_one_original_trial_per_arm_exact_lower_m_s']>main+1e-9
        or result['fixed_matched_cells_one_original_trial_per_arm_exact_upper_m_s']<main-1e-9
        or result['any_one_matched_cell_per_B_one_original_trial_per_arm_exact_lower_m_s']>result['fixed_matched_cells_one_original_trial_per_arm_exact_lower_m_s']+1e-9
        or result['any_one_matched_cell_per_B_one_original_trial_per_arm_exact_upper_m_s']<result['fixed_matched_cells_one_original_trial_per_arm_exact_upper_m_s']-1e-9):
        raise ValueError('NO_GO_MATHEMATICAL_EXTREMA_ORDER')
    return result


def audit_source(archive):
    if hashlib.sha256(archive).hexdigest()!=SOURCE_SHA256:
        raise ValueError('NO_GO_ORIGINAL_157_SHA256_MISMATCH')
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        mats=[name for name in z.namelist()
              if Path(name).name=='analyzeTrackingData.m'
              and not name.startswith('__MACOSX/')]
        if len(mats)!=1:
            raise ValueError('NO_GO_MATLAB_SOURCE_SCRIPT_NOT_UNIQUE')
        author=author_script_semantics(z.read(mats[0]))
        records=[]
        for name in sorted(z.namelist()):
            filename=Path(name).name
            if name.startswith('__MACOSX/') or filename.startswith('._') or not filename.endswith('xyzpts.csv'):
                continue
            match=FILENAME_PATTERN.fullmatch(filename)
            if match is None:
                raise ValueError('NO_GO_ORIGINAL_FILENAME_CODE_MISSING')
            c=match.groupdict()
            records.append({
               'B':c['B'],'S':c['S'],'P':c['P'],'W':'W'+c['W'],
               'values':reconstruct_all_filters(z.read(name),header=MEASURED_HEADER)
            })
    counts=dict(sorted(Counter(r['W'] for r in records).items()))
    if len(records)!=157 or counts!=EXPECTED_W or len({r['B'] for r in records})!=28:
        raise ValueError('NO_GO_ORIGINAL_SOURCE_STRUCTURE_CHANGED')
    summaries=[]
    for method_key in METHOD_KEYS:
        for subset_name,selection in SUBSETS:
            for end_name,endpoint in ENDPOINTS:
                summaries.append({
                    'cutoff_hz':method_key[0],
                    'speed_method':method_key[1],
                    'subset':subset_name,
                    'endpoint':end_name,
                    'bounds':selection_envelope(records,method_key,endpoint,selection)
                })
    if len(summaries)!=len(METHOD_KEYS)*len(SUBSETS)*len(ENDPOINTS):
        raise ValueError('NO_GO_SPECIFICATION_GRID_NOT_EXHAUSTIVE')
    ref=next(x['bounds'] for x in summaries
             if x['cutoff_hz']==100 and x['speed_method']=='three_tag_mean'
             and x['subset']=='all' and x['endpoint']=='near_flower_speed')
    if ref['n_original_B_identifiers']!=23 or abs(
        ref['original_within_B_S_P_all_trial_mean_m_s']-.12142936338922392)>1e-5:
        raise ValueError('NO_GO_STAGE41_43_ORIGINAL_REFERENCE_NOT_REPRODUCED')
    return {
       'status':'ORIGINAL_ARCHIVE_2016_WITHIN_B_TRIAL_SELECTION_INTERVALS',
       'original_archive_sha256':SOURCE_SHA256,
       'source_original_trajectories':len(records),
       'source_original_B_labels':28,
       'original_W0_W1_counts':counts,
       'original_MATLAB_source_sha_verified':author['status']=='AUTHOR_FILENAME_INDEX_SEMANTICS_SHA_VERIFIED',
       'methods':len(METHOD_KEYS),
       'subsets':len(SUBSETS),
       'endpoints':len(ENDPOINTS),
       'summaries':summaries,
       'original_112_publication_path_membership_unrecovered':True,
       'not_full_author_112_R_model_replication':True,
       'no_original_3d_frames_or_MATLAB_script_redistributed':True,
       'no_wind_olfaction_interaction_or_pollen_fitness':True
    }


def main():
    original,_=source_original_archive()
    receipt=audit_source(original)
    output=Path('stage44_aggregate_receipts')
    output.mkdir(exist_ok=True)
    (output/'source_within_bee_trial_selection_extrema.json').write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf8')
    subset=[x for x in receipt['summaries']
            if x['subset']=='all' and x['endpoint']=='near_flower_speed']
    print('STAGE44_REAL_ORIGINAL_MAIN_SIX_SPECIFICATIONS',json.dumps(subset,sort_keys=True))
    print('STAGE44_REAL_ALL_SUBSET_INTERVALS',json.dumps(receipt['summaries'],sort_keys=True))
    print('STAGE44_SOURCE_ONLY_NOT_AUTHOR_SELECTED_112_OR_PLANT_FITNESS')


if __name__=='__main__':
    main()
