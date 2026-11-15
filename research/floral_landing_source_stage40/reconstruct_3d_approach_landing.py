"""Stage40: exploratory original-data 3D landing ground-speed reconstruction.

This uses the authentic Chang/Crall/Combes 2016 Zenodo #60234 archive.
Unlike previous Stage39, this module actually derives m/s from source
3-BEETag coordinates using the source MATLAB Butterworth 5th/100Hz
filtfilt and the unique per-track pt7 flower origin.

CRITICAL INFERENCE CEILING:
* all 157 original archived trajectories, not the published 112 selected;
* filename W0/W1, S/P and bee B labels parsed by original source script;
* missing initial/final frames retained in original time order; NO phantom
  movements across missing spans; source-valid tag frames are contiguous;
* stage windows are 5-7 cm approach and 1.5-3 cm near-flower landing;
* no attempt/failure denominator and no olfaction/fitness outcome;
* per-B descriptive estimates exploratory, not author GLMM replication.
"""
from __future__ import annotations

import csv
import io
import json
import math
import random
import statistics
from collections import defaultdict,Counter
from pathlib import Path
import sys
import zipfile

import numpy as np
from scipy.signal import butter,filtfilt

from inspect_original_tracks import (
 source_original_archive, FILENAME_PATTERN, MEASURED_HEADER
)

FPS=1000
CUTOFF_HZ=100
ORDER=5
FILTER_B,FILTER_A=butter(ORDER,CUTOFF_HZ,fs=FPS,btype='low')
EXPECTED_ARCHIVE_TRACKS=157
EXPECTED_SOURCE_W={'W0':56,'W1':101}
MIN_STAGE_DERIVS=5
BOOT_SEED=20261115
BOOT_REPLICATES=10000


def _parse_original(s):
    if s is None:
        raise ValueError('NO_GO_MALFORMED_3D_CSV')
    if s.strip().lower() in ('nan','na','null','none',''):
        return float('nan')
    try:r=float(s)
    except ValueError as e:raise ValueError('NO_GO_NONNUMERIC_SOURCE_XYZ') from e
    if not math.isfinite(r):
        return float('nan')
    return r


def inspect_track(raw, metadata):
    rd=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''))
    if tuple(rd.fieldnames or ())!=MEASURED_HEADER:
        raise ValueError('NO_GO_3D_TRACK_SCHEMA_MISMATCH')
    positions=[]
    flowers=[]
    for frame,row in enumerate(rd):
        v=[_parse_original(row[k]) for k in MEASURED_HEADER]
        tag=np.asarray(v[:9],dtype=float).reshape(3,3)
        flower=np.asarray(v[18:21],dtype=float)
        if np.all(np.isfinite(flower)):
            flowers.append((frame,flower))
        positions.append(tag)
    if len(positions)<25 or len(flowers)!=1:
        raise ValueError('NO_GO_TRACK_OR_FLOWER_STATIC_REFERENCE')
    tag=np.stack(positions,axis=0)
    good=np.all(np.isfinite(tag),axis=(1,2))
    fi=np.flatnonzero(good)
    if len(fi)<30:
        raise ValueError('NO_GO_TOO_FEW_VALID_3TAG_FRAMES')
    if len(fi)!=fi[-1]-fi[0]+1:
        raise ValueError('NO_GO_NONCONSECUTIVE_PHYSICAL_FRAMES')
    valid=tag[fi]
    corrected=filtfilt(FILTER_B,FILTER_A,valid,axis=0)
    if not np.all(np.isfinite(corrected)):
        raise ValueError('NO_GO_FILTER_PHYSICAL_COORDINATES_NONFINITE')
    flower=flowers[0][1]
    # Source MATLAB point2 relative to one STATIC reference pt7
    distance=np.linalg.norm(corrected[:,1,:]-flower[None,:],axis=1)
    speed_by_pt=np.linalg.norm(np.diff(corrected,axis=0),axis=2)*FPS
    speed=np.mean(speed_by_pt,axis=1)
    if not np.all(np.isfinite(speed)) or np.any(speed<0):
        raise ValueError('NO_GO_NONFINITE_RECONSTRUCTED_SPEED')
    approach=(distance[:-1]>.05)&(distance[:-1]<.07)
    landing=(distance[:-1]>.015)&(distance[:-1]<.03)
    min_required=(approach.sum()>=MIN_STAGE_DERIVS and
                  landing.sum()>=MIN_STAGE_DERIVS)
    if min_required:
        a=float(speed[approach].mean())
        l=float(speed[landing].mean())
        delta=l-a
    else:
        a=l=delta=None
    # Source MATLAB's last100ms maximum decel: exclude 10 edges,
    # then look for steepest signed speed change in final100 frames.
    # This is a source-style sensitivity rather than a publication
    # selected-track result; numerical differentiation amplifies noise.
    accel=np.diff(speed)*FPS
    trimmed=accel[10:-10] if len(accel)>25 else np.array([])
    min_last100=float(np.min(trimmed[-101:])) if len(trimmed)>=101 else None
    return {
      **metadata,
      'original_frames':len(positions),'valid_tag_frames':len(fi),
      'valid_tag_frame_contiguous':True,
      'one_static_flower_center':True,
      'min_frames_for_both_stage_estimates':min_required,
      'approach_original_speed_windows':int(approach.sum()),
      'landing_original_speed_windows':int(landing.sum()),
      'approach_m_per_s_exploratory':a,
      'near_flower_m_per_s_exploratory':l,
      'speed_change_landing_minus_approach_m_per_s':delta,
      'source_style_peak_deceleration_m_per_s2':min_last100,
      'no_source_track_coordinates_exported':True,
    }


def _moments(x):
    return {'n':len(x),'mean':statistics.mean(x) if x else None,
            'median':statistics.median(x) if x else None,
            'min':min(x) if x else None,
            'max':max(x) if x else None}


def _paired_by_bee(tracks,key):
    group=defaultdict(lambda:defaultdict(list))
    for row in tracks:
        v=row[key]
        if v is not None:
            group[row['B']][row['W']].append(v)
    paired=[]
    for bee,values in sorted(group.items()):
        if values.get('W0') and values.get('W1'):
            still=statistics.mean(values['W0'])
            windy=statistics.mean(values['W1'])
            paired.append((bee,still,windy,windy-still))
    return paired


def _matched_bee_stiffness_position(tracks,key):
    """Condition on B, original S(stiffness), P(flower position) BEFORE wind."""
    cells=defaultdict(lambda:defaultdict(list))
    for row in tracks:
        v=row.get(key)
        if v is not None:
            cells[(row['B'],row['S'],row['P'])][row['W']].append(v)
    matched=defaultdict(list)
    for (B,S,P),both in cells.items():
        if both.get('W0') and both.get('W1'):
            matched[B].append((statistics.mean(both['W0']),
                               statistics.mean(both['W1'])))
    # Each original B contributes ONCE; each matched S/P cell within B
    # receives equal weight, not one pseudoreplicate per trajectory.
    out=[]
    for B,values in sorted(matched.items()):
        calm=statistics.mean(x[0] for x in values)
        windy=statistics.mean(x[1] for x in values)
        out.append((B,calm,windy,windy-calm))
    return out


def _bootstrap_pairs(paired,replicates=BOOT_REPLICATES,seed=BOOT_SEED):
    if not paired:
        return None
    d=[p[3] for p in paired]
    rand=random.Random(seed)
    n=len(d)
    sample=[]
    for i in range(replicates):
        sample.append(sum(d[rand.randrange(n)] for _ in range(n))/n)
    sample.sort()
    def q(prob):
        point=(len(sample)-1)*prob
        lo=int(point);fraction=point-lo
        return sample[lo]*(1-fraction)+sample[min(lo+1,len(sample)-1)]*fraction
    return {
       'equal_bee_mean_W1_minus_W0':statistics.mean(d),
       'paired_bee_labels':n,
       'n_positive':sum(x>0 for x in d),
       'n_negative':sum(x<0 for x in d),
       'n_zero':sum(x==0 for x in d),
       'bee_resample_10k_percentile_95ci_descriptive':[q(.025),q(.975)],
       'random_seed':seed,'bootstrap_replicates':replicates,
       'not_author_selected_112_or_colony_robust':True,
       'not_a_causal_wind_effect':True
    }


def analyze_original_zip(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError('NO_GO_NO_AUTHENTIC_ORIGINAL_ZIP')
    tracks=[]
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for filename in sorted(z.namelist()):
            basename=Path(filename).name
            if filename.startswith('__MACOSX/') or basename.startswith('._'):
                continue
            if not basename.endswith('xyzpts.csv'):
                continue
            m=FILENAME_PATTERN.fullmatch(basename)
            if m is None:
                raise ValueError('NO_GO_ORIGINAL_FILENAME_CLASSIFICATION_FAILED')
            codes=m.groupdict()
            metadata={'B':codes['B'],'BC':codes['BC'],
                     'S':codes['S'],'P':codes['P'],'W':'W'+codes['W']}
            tracks.append(inspect_track(z.read(filename),metadata))
    if len(tracks)!=EXPECTED_ARCHIVE_TRACKS:
        raise ValueError('NO_GO_ORIGINAL_NUMBER_OF_TRAJECTORIES_CHANGED')
    w=Counter(row['W'] for row in tracks)
    if dict(sorted(w.items()))!=EXPECTED_SOURCE_W:
        raise ValueError('NO_GO_SOURCE_WIND_LABEL_COUNTS_CHANGED')

    valid=[x for x in tracks if x['min_frames_for_both_stage_estimates']]
    labels=sorted({r['B'] for r in tracks})
    by_W={}
    for W in ('W0','W1'):
        z=[x for x in valid if x['W']==W]
        by_W[W]={
           'valid_stage_tracks':len(z),
           'mean_approach_m_s_exploratory':_moments(
               [r['approach_m_per_s_exploratory'] for r in z]),
           'mean_near_flower_m_s_exploratory':_moments(
               [r['near_flower_m_per_s_exploratory'] for r in z]),
           'within_track_speed_change_m_s_exploratory':_moments(
               [r['speed_change_landing_minus_approach_m_per_s'] for r in z])
        }

    stage_keys=(
        ('approach_speed','approach_m_per_s_exploratory'),
        ('landing_speed','near_flower_m_per_s_exploratory'),
        ('landing_minus_approach_speed','speed_change_landing_minus_approach_m_per_s'),
        ('source_style_peak_decel','source_style_peak_deceleration_m_per_s2')
    )
    pairs={stage:_bootstrap_pairs(_paired_by_bee(valid,key))
           for stage,key in stage_keys}
    strictly_matched={stage:_bootstrap_pairs(_matched_bee_stiffness_position(valid,key))
                      for stage,key in stage_keys}
    cross=Counter(f"S{x['S']}_P{x['P']}_W{x['W'][-1]}" for x in valid)
    return {
       'status':'ORIGINAL_157_ARCHIVED_TRACKS_EXPLORATORY_KINEMATIC_REFIT',
       'original_frames_per_second_from_author_MATLAB':FPS,
       'author_MATLAB_Butterworth_order':ORDER,
       'author_MATLAB_Butterworth_cutoff_hz':CUTOFF_HZ,
       'original_archive_tracks':len(tracks),
       'original_filename_B_labels':len(labels),
       'original_W0_W1_counts':dict(sorted(w.items())),
       'original_tag3_and_static_flower_geometry_verified':True,
       'stage_eligible_tracks':len(valid),
       'stage_ineligible_tracks':len(tracks)-len(valid),
       'eligible_S_P_W_combinations':dict(sorted(cross.items())),
       'wind_stratified_descriptive':by_W,
       'within_original_B_label_paired_descriptive':pairs,
       'within_B_and_same_stiffness_position_matched_descriptive':strictly_matched,
       'matched_original_source_design_B_S_P_before_comparing_W':True,
       'published_112_selected_tracks_not_identified':True,
       'W0_W1_paper_selected_n_unreconciled':True,
       'source_stiffness_and_flower_position_not_matched_between_conditions':True,
       'not_author_published_GLMM_reproduction':True,
       'not_external_source_original_raw_data_redistributed':True,
       'no_attempted_landing_failure_denominator':True,
       'no_flow_to_pollen_or_seed_fitness_estimated':True,
       'no_wind_by_scent_on_off_interaction':True
    }


def main():
    original,_=source_original_archive()
    result=analyze_original_zip(original)
    folder=Path('stage40_kinematic_refit_receipts')
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'stage40_original_157_archived_exploratory_kinematics.json').write_text(
        json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps(result,sort_keys=True,allow_nan=False))


if __name__=='__main__':
    main()
