"""Stage42: source-verified publication-vs-archive trial ledger and S/P contrasts.

Chang, Crall & Combes (2016), doi:10.1242/jeb.137976; Zenodo 60234.
The paper's 112 primary trajectories are 31 (P0,W0), 29 (P1,W0),
27 (P0,W1), 25 (P1,W1), but 157 available filename-coded xyz tracks
contain only 56 W0 files. The primary file-by-file selection is missing.

Every published-archive mismatch must remain visible. No invented missing
tracks, no pseudoreplication of 1000-Hz frames, no physical fitness claims.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import io
import json
import math
from pathlib import Path
import re
import statistics
import sys
import zipfile

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'floral_wind_kinematic_stage39'))
sys.path.insert(0,str(BASE/'floral_landing_sensitivity_stage41'))
from inspect_original_tracks import source_original_archive,FILENAME_PATTERN,MEASURED_HEADER
from preprocessing_sensitivity import reconstruct_all_filters,matched_by_bee

PAPER_PRIMARY_BY_P_W={
    'P0_W0':31,'P1_W0':29,'P0_W1':27,'P1_W1':25
}
PAPER_PRIMARY_N=112
SOURCE_EXPECTED_BY_S_P_W={
    'S0_P0_W0':25,'S0_P0_W1':29,
    'S0_P1_W0':13,'S0_P1_W1':27,
    'S1_P0_W0':6,'S1_P0_W1':23,
    'S1_P1_W0':12,'S1_P1_W1':22,
}
SOURCE_SHA256='9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec'
SOURCE_MATLAB_SHA256='e05e565c13e70b043017fa5e88cfcd1789d81a4de0fd932fed1e6985b82475ce'


def publication_compatibility(cells):
    """Minimum unarchived primary paths under W/P one-to-one mapping."""
    if set(cells)!=set(PAPER_PRIMARY_BY_P_W):
        raise ValueError('NO_GO_P_W_CELLS_INCOMPLETE')
    if not all(isinstance(v,int) and v>=0 for v in cells.values()):
        raise ValueError('NO_GO_INVALID_SOURCE_COUNTS')
    gaps={k:max(0,PAPER_PRIMARY_BY_P_W[k]-cells[k]) for k in cells}
    extras={k:max(0,cells[k]-PAPER_PRIMARY_BY_P_W[k]) for k in cells}
    return {
        'paper_primary_by_P_W':dict(PAPER_PRIMARY_BY_P_W),
        'original_archive_by_P_W':dict(sorted(cells.items())),
        'minimum_missing_primary_files_if_one_to_one_and_labels_correct':sum(gaps.values()),
        'missing_primary_lower_bound_by_cell':gaps,
        'at_least_one_paper_condition_more_than_source':any(v>0 for v in gaps.values()),
        'strict_source_subset_of_published_112_possible':not any(gaps.values()),
        'source_surplus_by_cell_not_proof_of_exclusion':extras,
        'does_not_prove_original_author_error':True,
    }


def author_script_semantics(original_script):
    actual_hash=hashlib.sha256(original_script).hexdigest()
    if actual_hash!=SOURCE_MATLAB_SHA256:
        raise ValueError('NO_GO_AUTHOR_MATLAB_ORIGINAL_HASH_CHANGED')
    source=original_script.decode('latin1')
    required=(
       r'beeNumber\s*=\s*str2num\s*\(\s*filename\(2:3\)\s*\)',
       r'flowerNumber\s*=\s*str2num\s*\(\s*filename\(13:14\)\s*\)',
       r'stiffness\s*=\s*str2num\s*\(\s*filename\(17\)\s*\)',
       r'position\s*=\s*str2num\s*\(\s*filename\(20\)\s*\)',
       r'trialNumber\s*=\s*str2num\s*\(\s*filename\(23:24\)\s*\)',
       r'wind\s*=\s*str2num\s*\(\s*filename\(27\)\s*\)',
       r'\bif\s+stiffness\s*==\s*0\s*&\s*position\s*==\s*0\s*&\s*wind\s*==\s*0',
    )
    if not all(re.search(p,source) for p in required):
        raise ValueError('NO_GO_MATLAB_FILENAME_CODE_SEMANTICS_UNKNOWN')
    return {
        'status':'AUTHOR_FILENAME_INDEX_SEMANTICS_SHA_VERIFIED',
        'author_matlab_sha256':actual_hash,
        'wind_code_from_source_filename_character_27':True,
        'P_flower_position_code_from_source_filename_character_20':True,
        'S_stem_stiffness_code_from_source_filename_character_17':True,
        'B_bee_number_from_source_filename_characters_2_3':True,
        'F_flower_number_from_source_filename_characters_13_14':True,
        'T_trial_number_from_source_filename_characters_23_24':True,
        'no_independent_mapping_S0_S1_to_flexible_fixed_arms':True,
        'this_script_does_not_authenticate_paper_112_trial_membership':True
    }


def _difference_stats(rows,*,name):
    """One original B code per S/P-matched wind contrast, not every track."""
    selected=[r for r in rows if all(r[k]==v for k,v in name.items())]
    bywind=Counter(r['W'] for r in selected)
    eligible=Counter(r['W'] for r in selected
                     if r['values'][(100,'three_tag_mean')] is not None)
    ans={
      'condition':name,
      'source_tracks':len(selected),
      'source_tracks_by_W':dict(sorted(bywind.items())),
      'eligible_track_counts_by_W':dict(sorted(eligible.items())),
      'n_source_B_codes':len({r['B'] for r in selected}),
    }
    effects={}
    for endkey,idx in (('near_flower_speed',1),('landing_minus_approach_speed',2)):
        paired=matched_by_bee(selected,'three_tag_mean',100,idx)
        if not paired:
            effects[endkey]={'status':'NO_GO_NO_MATCHED_B'}
            continue
        leave_one=([statistics.mean(paired[:i]+paired[i+1:])
                    for i in range(len(paired))] if len(paired)>1 else [])
        effects[endkey]={
          'status':'DESCRIPTIVE_MATCHED_B_CODES',
          'mean_W1_minus_W0_m_s':statistics.mean(paired),
          'number_matched_B_codes':len(paired),
          'positive_B_codes':sum(d>0 for d in paired),
          'negative_B_codes':sum(d<0 for d in paired),
          'zero_B_codes':sum(d==0 for d in paired),
          'leave_one_B_out_mean_min_max_m_s':(
              [min(leave_one),max(leave_one)] if leave_one else None),
          'not_independent_colony_or_fitness_inference':True
        }
    ans['matched_B_effects']=effects
    return ans


def audit_trajectory_archive(raw_archive):
    with zipfile.ZipFile(io.BytesIO(raw_archive)) as z:
        source_names=z.namelist()
        script_names=[n for n in source_names
                      if Path(n).name=='analyzeTrackingData.m' and
                      not n.startswith('__MACOSX/')]
        if len(script_names)!=1:
            raise ValueError('NO_GO_AUTHOR_ANALYSIS_SCRIPT_ID_AMBIGUOUS')
        author=author_script_semantics(z.read(script_names[0]))
        source_rows=[]
        supplemental=Counter()
        nontrajectory_candidates=[]
        for fname in sorted(source_names):
            base=Path(fname).name
            if fname.startswith('__MACOSX/') or base.startswith('._') or base=='.DS_Store':
                continue
            if not base.endswith('xyzpts.csv'):
                if base and not fname.endswith('/'):
                    supplemental[Path(base).suffix.lower() or '<no_suffix>']+=1
                    if Path(base).suffix.lower() in ('.csv','.mat','.xlsx','.r','.rds'):
                        nontrajectory_candidates.append(base)
                continue
            m=FILENAME_PATTERN.fullmatch(base)
            if m is None:
                raise ValueError('NO_GO_ORIGINAL_FILENAME_PATTERN_MISMATCH')
            tags=m.groupdict()
            source_rows.append({
                'B':tags['B'],'F':tags['F'],'T':tags['T'],
                'BC':tags['BC'],'S':tags['S'],'P':tags['P'],'W':'W'+tags['W'],
                'values':reconstruct_all_filters(z.read(fname),header=MEASURED_HEADER)
            })
    counts=Counter('S'+r['S']+'_P'+r['P']+'_'+r['W'] for r in source_rows)
    if len(source_rows)!=157 or dict(sorted(counts.items()))!=SOURCE_EXPECTED_BY_S_P_W:
        raise ValueError('NO_GO_UNEXPECTED_ORIGINAL_S_P_W_COUNTS')
    if len({x['B'] for x in source_rows})!=28:
        raise ValueError('NO_GO_SOURCE_B_IDENTITY_CHANGED')
    archive_by_P_W=Counter('P'+r['P']+'_'+r['W'] for r in source_rows)
    compatibility=publication_compatibility(archive_by_P_W)
    if compatibility['strict_source_subset_of_published_112_possible']:
        raise ValueError('NO_GO_EXPECTED_PRIMARY_SOURCE_GAP_DISAPPEARED')
    analyses=[]
    for tag in ({}, {'S':'0'}, {'S':'1'}, {'P':'0'}, {'P':'1'},
                {'S':'0','P':'0'}, {'S':'0','P':'1'},
                {'S':'1','P':'0'}, {'S':'1','P':'1'}):
        analyses.append(_difference_stats(source_rows,name=tag))
    original=analyses[0]['matched_B_effects']['near_flower_speed']
    if original['number_matched_B_codes']!=23 or abs(
       original['mean_W1_minus_W0_m_s']-.12142936338922392)>1e-5:
        raise ValueError('NO_GO_STAGE41_REFERENCE_EFFECT_NOT_REPRODUCED')
    return {
       'status':'SOURCE_ARCHIVE_VS_PAPER_CONDITION_CENSUS_AND_STRATIFIED_KINEMATICS',
       'source_sha256_verified':SOURCE_SHA256,
       'source_file_count_original_xyz_tracks':len(source_rows),
       'source_filename_B_identifiers':28,
       'archive_by_S_P_W':dict(sorted(counts.items())),
       'author_matlab_semantics':author,
       'publication_compatibility':compatibility,
       'original_nontrajectory_extension_counts':dict(sorted(supplemental.items())),
       'potential_author_stats_or_trial_selection_file_basenames':sorted(set(nontrajectory_candidates))[:60],
       'stratified_100hz_three_tag_matched_results':analyses,
       'no_confirmed_author_original_112_list':True,
       'no_original_raw_trajectory_or_script_redistributed':True,
       'no_wind_by_scent_or_pollen_or_seed_or_fitness_estimate':True,
       'explicit_S0_S1_legends_not_inferred_from_paper':True
    }


def main():
    original,meta=source_original_archive()
    if hashlib.sha256(original).hexdigest()!=SOURCE_SHA256:
        raise ValueError('NO_GO_ORIGINAL_SOURCE_ARCHIVE_SHA_CHANGED')
    receipt=audit_trajectory_archive(original)
    folder=Path('stage42_aggregate_receipts')
    folder.mkdir(exist_ok=True)
    (folder/'original_stiffness_position_census.json').write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf8'
    )
    print(json.dumps(receipt,sort_keys=True,ensure_ascii=False,allow_nan=False))


if __name__=='__main__':
    main()
