"""Stage43: *partial identification*, not a publication-selected wind-effect refit.

Source 1: Chang/Crall/Combes 2016, JEB doi:10.1242/jeb.137976,
pages 2820-2821 (original author PDF reviewed manually).
Source 2: checksum-pinned original Zenodo 60234 xyz trajectories and
author example MATLAB script. No author-selected trial roster is present.

Questions:
 (1) Are the paper main text, Fig. 1 caption and speed-statistic
     denominators mutually identifiable as one study population?
 (2) Can deleting a strategically chosen set of whole original bee-ID
     contrasts reverse the archived-data W1-W0 mean? Exact finite-list
     minimax, not a p-value, randomization or empirical population CI.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import sys
import zipfile
from collections import Counter,defaultdict

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'floral_wind_kinematic_stage39'))
sys.path.insert(0,str(BASE/'floral_landing_sensitivity_stage41'))
sys.path.insert(0,str(BASE/'floral_original_selection_stage42'))
from inspect_original_tracks import source_original_archive,FILENAME_PATTERN,MEASURED_HEADER
from preprocessing_sensitivity import reconstruct_all_filters,CUTOFFS,SPEED_METHODS
from author_archive_condition_audit import (
    SOURCE_SHA256,author_script_semantics,publication_compatibility
)

# Literal manual transcription of two mutually inconsistent constructions
# in 2016 paper, p2820. No PDF is downloaded/parsed in this source CI.
PUB_PROSE={'P0_W0':31,'P1_W0':29,'P0_W1':27,'P1_W1':25}
PUB_FIG1_CAPTION_FIRST_CLAUSE={'P0_W0':31,'P1_W0':27,'P0_W1':29,'P1_W1':25}
PUB_SPEED_FIG2={'W0':60,'W1':52}
PUB_TTEST_DF={'W0':54,'W1':54}
PUB_STUDY_PRIMARY_TOTAL=112


def publication_denominator_audit(source_pw,source_w):
    """Conditional source subset lower bounds, never invented missing files."""
    if set(source_pw)!=set(PUB_PROSE) or set(source_w)!=set(PUB_SPEED_FIG2):
        raise ValueError('NO_GO_SOURCE_CONDITION_CELL_SCHEMA')
    if sum(source_pw.values())!=sum(source_w.values()):
        raise ValueError('NO_GO_SOURCE_PW_W_GRAIN_MISMATCH')
    def one_to_one(paper):
        if sum(paper.values())!=PUB_STUDY_PRIMARY_TOTAL:
            raise ValueError('NO_GO_WRONG_PAPER_TRAJECTORY_TOTAL')
        lower={k:max(0,paper[k]-source_pw[k]) for k in paper}
        return {'paper_counts':dict(sorted(paper.items())),
                'source_counts':dict(sorted(source_pw.items())),
                'conditional_minimum_unavailable_paper_paths':sum(lower.values()),
                'conditional_shortfall_by_cell':lower,
                'cannot_1_to_1_embed_all_paper_paths':any(v>0 for v in lower.values())}
    main=one_to_one(PUB_PROSE)
    caption=one_to_one(PUB_FIG1_CAPTION_FIRST_CLAUSE)
    if sum(PUB_SPEED_FIG2.values())!=112:
        raise ValueError('NO_GO_SPEED_FIGURE_TOT')
    implied={w:PUB_TTEST_DF[w]+1 for w in PUB_TTEST_DF}
    return {
      'publication_DOI':'10.1242/jeb.137976',
      'publication_Fig1_main_prose_P_W':main,
      'publication_Fig1_caption_first_clause_P_W':caption,
      'paper_fig1_first_clause_and_main_prose_differ':PUB_PROSE!=PUB_FIG1_CAPTION_FIRST_CLAUSE,
      'publication_Fig2_plot_all_still_wind':PUB_SPEED_FIG2,
      'publication_speed_paired_t_reported_df':PUB_TTEST_DF,
      'sample_n_if_ordinary_one_sample_or_paired_t':implied,
      'standard_t_implied_n_differs_from_main_W_n':implied!=PUB_SPEED_FIG2,
      'paper_fig2_wind_n_52_less_than_t_implied_n_55':PUB_SPEED_FIG2['W1']<implied['W1'],
      'no_assumption_that_fig1_fig2_and_ttests_are_same_trial_subset':True,
      'paper_numbers_manually_checked_not_machine_extracted_in_this_CI':True,
      'paper_notes_are_an_identification_warning_not_proof_author_mistake':True
    }


def robust_adversarial_removals(d):
    """Exact minimum of retained mean after deleting k whole B labels.

    At fixed retained count, the smallest achievable mean is the mean of
    the smallest n-k individual differences; exchanging a larger retained
    element with a smaller deleted element never increases the sum.
    """
    if not d:
        return {'status':'NO_GO_NO_PAIRED_B'}
    nums=sorted(float(x) for x in d)
    if not all(math.isfinite(x) for x in nums):
        raise ValueError('NO_GO_NONFINITE_INDIVIDUAL_CONTRAST')
    n=len(nums)
    worst=[statistics.mean(nums[:n-k]) for k in range(n)]
    best=[statistics.mean(nums[k:]) for k in range(n)]
    first_nonpositive=next((k for k,x in enumerate(worst) if x<=0),None)
    return {
      'status':'EXACT_FINITE_OBSERVED_B_LABEL_DELETION_BOUND',
      'n_unique_matched_B_codes':n,
      'positive_B':sum(x>0 for x in nums),
      'negative_B':sum(x<0 for x in nums),
      'zero_B':sum(x==0 for x in nums),
      'original_equal_B_mean_m_s':statistics.mean(nums),
      'worst_mean_delete_1_m_s':worst[1] if n>1 else None,
      'worst_mean_delete_2_m_s':worst[2] if n>2 else None,
      'worst_mean_delete_3_m_s':worst[3] if n>3 else None,
      'best_mean_delete_1_m_s':best[1] if n>1 else None,
      'minimum_adversarial_whole_B_deletions_to_nonpositive_mean':first_nonpositive,
      'largest_k_all_k_deletions_preserve_positive_mean':(
          n-1 if first_nonpositive is None else first_nonpositive-1),
      'worst_remaining_B_mean_at_half_sample_drop_m_s':worst[n//2],
      'all_drop_one_mean_positive':n>1 and worst[1]>0,
      'proof':'At fixed n-k, retaining the n-k smallest paired contrasts minimizes mean.',
      'not_a_colony_or_animal_population_confidence_interval':True,
      'not_authentication_of_original_112_selection':True,
      'not_a_causal_wind_or_plant_fitness_effect':True
    }


def source_paired_differences(rows,filter_hz=100,speed_method='three_tag_mean',
                              endpoint=1,subset=None):
    """Within the SAME original B×S×P; return one contrast per B code."""
    if subset is None:subset={}
    if set(subset)-{'S','P'}:
        raise ValueError('NO_GO_SUBSET_INVALID_FIELDS')
    cells=defaultdict(lambda:defaultdict(list))
    for row in rows:
        if any(row.get(k)!=v for k,v in subset.items()):
            continue
        val=row['values'][(filter_hz,speed_method)]
        if val is not None:
            cells[(row['B'],row['S'],row['P'])][row['W']].append(val[endpoint])
    per_bee=defaultdict(list)
    for (bee,_,_),both in cells.items():
        if both.get('W0') and both.get('W1'):
            per_bee[bee].append(statistics.mean(both['W1'])-
                                statistics.mean(both['W0']))
    return [statistics.mean(per_bee[bee]) for bee in sorted(per_bee)]


def audit_source(archive):
    if hashlib.sha256(archive).hexdigest()!=SOURCE_SHA256:
        raise ValueError('NO_GO_ORIGINAL_CHANG_ZIP_DIGEST')
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        mats=[name for name in z.namelist()
              if Path(name).name=='analyzeTrackingData.m'
              and not name.startswith('__MACOSX/')]
        if len(mats)!=1:
            raise ValueError('NO_GO_ORIGINAL_AUTHOR_SCRIPT_MISSING_OR_AMBIGUOUS')
        author=author_script_semantics(z.read(mats[0]))
        matlab=z.read(mats[0]).decode('latin1')
        if not all(text in matlab for text in (
            "floralApproachBeeData.mat",
            "flowerApproachDataForStats.csv"
        )):
            raise ValueError('NO_GO_AUTHOR_OUTPUT_NAMES_NOT_PRESENT')
        contents=[Path(name).name for name in z.namelist()
                  if not name.startswith('__MACOSX/')
                  and not Path(name).name.startswith('._')]
        if any(x in contents for x in (
            "floralApproachBeeData.mat","flowerApproachDataForStats.csv"
        )):
            raise ValueError('NO_GO_AUTHOR_DERIVED_STATS_ALREADY_PRESENT_REAUDIT')
        rows=[]
        for name in sorted(z.namelist()):
            f=Path(name).name
            if name.startswith('__MACOSX/') or f.startswith('._') or not f.endswith('xyzpts.csv'):
                continue
            m=FILENAME_PATTERN.fullmatch(f)
            if m is None:
                raise ValueError('NO_GO_ORIGINAL_CODED_FILENAME_MISMATCH')
            c=m.groupdict()
            rows.append({'B':c['B'],'P':c['P'],'S':c['S'],'W':'W'+c['W'],
                         'values':reconstruct_all_filters(z.read(name),
                                                           header=MEASURED_HEADER)})
    source_w=Counter(r['W'] for r in rows)
    source_pw=Counter('P'+r['P']+'_'+r['W'] for r in rows)
    if len(rows)!=157 or len({r['B'] for r in rows})!=28 or dict(source_w)!={'W0':56,'W1':101}:
        raise ValueError('NO_GO_CHANGED_ARCHIVAL_TRAJECTORY_GRAIN')
    paper=publication_denominator_audit(source_pw,source_w)
    specs=[]
    subsets=[('all',{}),('S0',{'S':'0'}),('S1',{'S':'1'}),
             ('P0',{'P':'0'}),('P1',{'P':'1'}),
             ('S0_P0',{'S':'0','P':'0'}),('S0_P1',{'S':'0','P':'1'}),
             ('S1_P0',{'S':'1','P':'0'}),('S1_P1',{'S':'1','P':'1'})]
    for hz in CUTOFFS:
        for method in SPEED_METHODS:
            for label,subset in subsets:
                for endpoint_name,endpoint in (
                    ('near_flower_speed',1),('landing_minus_approach_speed',2)
                ):
                    d=source_paired_differences(rows,hz,method,endpoint,subset)
                    specs.append({
                      'cutoff_hz':hz,'method':method,'subset':label,'endpoint':endpoint_name,
                      'selection_robustness':robust_adversarial_removals(d)
                    })
    base=next(x['selection_robustness'] for x in specs
              if x['cutoff_hz']==100 and x['method']=='three_tag_mean'
              and x['subset']=='all' and x['endpoint']=='near_flower_speed')
    if base['n_unique_matched_B_codes']!=23 or abs(
        base['original_equal_B_mean_m_s']-.12142936338922392)>1e-5:
        raise ValueError('NO_GO_REFERENCE_STAGE41_B_CONTRAST_NOT_REPRODUCED')
    return {
      'status':'ORIGINAL_SOURCE_TRIAL_DENOMINATOR_AND_WHOLE_B_DELETION_AUDIT',
      'original_source_sha256':SOURCE_SHA256,
      'source_157_xyz_files':len(rows),
      'source_W0_W1_file_counts':dict(sorted(source_w.items())),
      'original_author_filename_semantics_SHA_locked':author['status'],
      'original_author_stats_files_named_but_not_in_source_zip':True,
      'original_published_112_trial_list_not_authenticated':True,
      'publication_denominator_evidence':paper,
      'exact_finite_B_label_selection_sensitivities':specs,
      'no_source_raw_xyz_or_original_author_matlab_redistributed':True,
      'no_plant_fitness_or_odor_factorial_or_failed_landings_measured':True,
      'not_proof_published_error_or_animal_population_significance':True,
    }


def main():
    source,_=source_original_archive()
    receipt=audit_source(source)
    folder=Path('stage43_aggregate_receipts')
    folder.mkdir(exist_ok=True)
    (folder/'paper_denominators_and_whole_bee_deletion.json').write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2,allow_nan=False)+'\n',
        encoding='utf8')
    compact=[r for r in receipt['exact_finite_B_label_selection_sensitivities']
             if r['subset']=='all' and r['endpoint']=='near_flower_speed']
    print('STAGE43_PUBLICATION_DENOMINATORS',json.dumps(receipt['publication_denominator_evidence'],sort_keys=True))
    print('STAGE43_WHOLE_B_ADVERSARIAL_EXCLUSIONS',json.dumps(compact,sort_keys=True))
    print('STAGE43_ALL_SOURCE_SUBGROUPS_JSON',json.dumps(receipt['exact_finite_B_label_selection_sensitivities'],sort_keys=True))
    print('STAGE43_DONE_ORIGINAL_157_NOT_PAPER_112_OR_REAL_POLLINATION')


if __name__=='__main__':
    main()
