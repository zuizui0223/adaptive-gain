"""Stage41: independent sensitivity of Chang et al. 2016 wind-landing speeds.

Read exact checksum-verified Zenodo 60234 only at runtime. Vary the
precommitted Butterworth cutoff 50/100/150 Hz and moving-body speed as
mean of all three tag markers versus point2 alone. Keep the original
5–7 cm / 1.5–3 cm distance bands and match W0/W1 by B x S x P.
Data are already published; no 112-trial manuscript selection is known.
Never infer failed landings, scent effects, pollination, or plant fitness.
"""
from __future__ import annotations

import csv
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import statistics
import sys
import zipfile

import numpy as np
from scipy.signal import butter, sosfiltfilt

FPS=1000
CUTOFFS=(50,100,150)
SPEED_METHODS=('three_tag_mean','point2_only')
EXPECTED_W={'W0':56,'W1':101}
MIN_FRAMES=5


def _number(value):
    if value is None or value.strip().lower() in ('','nan','na','none','null'):
        return math.nan
    try:
        out=float(value)
    except ValueError as exc:
        raise ValueError('NO_GO_NONNUMERIC_SOURCE_COORDINATE') from exc
    return out if math.isfinite(out) else math.nan


def reconstruct_all_filters(blob, *, header):
    """Physical 3-D velocity with independently chosen stable SOS filtering."""
    rd=csv.DictReader(io.StringIO(blob.decode('utf-8-sig'), newline=''))
    if tuple(rd.fieldnames or ())!=header:
        raise ValueError('NO_GO_UNEXPECTED_21_COLUMN_SCHEMA')
    tags=[]
    flowers=[]
    for row in rd:
        a=np.array([_number(row[k]) for k in header],dtype=float).reshape(7,3)
        tags.append(a[:3])
        if np.isfinite(a[6]).all():
            flowers.append(a[6].copy())
    if len(flowers)!=1 or len(tags)<30:
        raise ValueError('NO_GO_NO_SINGLE_STATIC_FLOWER_OR_SHORT_TRACK')
    x=np.array(tags)
    valid=np.flatnonzero(np.isfinite(x).all(axis=(1,2)))
    if valid.size<30 or valid.size!=valid[-1]-valid[0]+1:
        raise ValueError('NO_GO_NO_CONTIGUOUS_THREE_TAG_FRAMES')
    x=x[valid]
    flower=flowers[0]
    out={}
    for cutoff in CUTOFFS:
        sos=butter(5,cutoff,fs=FPS,btype='low',output='sos')
        xf=sosfiltfilt(sos,x,axis=0)
        if not np.isfinite(xf).all():
            raise ValueError('NO_GO_FILTER_NONFINITE')
        distance=np.linalg.norm(xf[:,1,:]-flower[None,:],axis=1)
        displacement=np.diff(xf,axis=0)*FPS
        approach=(distance[:-1]>.05)&(distance[:-1]<.07)
        landing=(distance[:-1]>.015)&(distance[:-1]<.03)
        eligible=int(approach.sum())>=MIN_FRAMES and int(landing.sum())>=MIN_FRAMES
        for method in SPEED_METHODS:
            speed=(np.linalg.norm(displacement,axis=2).mean(axis=1)
                   if method=='three_tag_mean'
                   else np.linalg.norm(displacement[:,1,:],axis=1))
            if not np.isfinite(speed).all():
                raise ValueError('NO_GO_VELOCITY_NONFINITE')
            if eligible:
                a=float(speed[approach].mean())
                l=float(speed[landing].mean())
                out[(cutoff,method)]=(a,l,l-a)
            else:
                out[(cutoff,method)]=None
    return out


def matched_by_bee(tracks,method,cutoff,endpoint):
    """Exactly one matched W1-W0 contribution per original B bee label."""
    cells=defaultdict(lambda:defaultdict(list))
    for row in tracks:
        values=row['values'][(cutoff,method)]
        if values is not None:
            cells[(row['B'],row['S'],row['P'])][row['W']].append(values[endpoint])
    bees=defaultdict(list)
    for (bee,_,_),bywind in cells.items():
        if bywind.get('W0') and bywind.get('W1'):
            bees[bee].append(statistics.mean(bywind['W1'])-
                             statistics.mean(bywind['W0']))
    return [statistics.mean(d) for _,d in sorted(bees.items())]


def summarize(tracks):
    counts=Counter(r['W'] for r in tracks)
    if len(tracks)!=157 or dict(sorted(counts.items()))!=EXPECTED_W:
        raise ValueError('NO_GO_ORIGINAL_ARCHIVE_GRAIN')
    specs=[]
    for cutoff in CUTOFFS:
      for method in SPEED_METHODS:
        subsets={w:[r['values'][(cutoff,method)] for r in tracks
                    if r['W']==w and r['values'][(cutoff,method)] is not None]
                 for w in ('W0','W1')}
        stage={}
        for w,vals in subsets.items():
            if not vals:raise ValueError('NO_GO_WIND_CONDITION_WITH_NO_STAGE_TRACKS')
            stage[w]={
              'n_eligible_tracks':len(vals),
              'approach_mean_m_s':statistics.mean(v[0] for v in vals),
              'near_flower_mean_m_s':statistics.mean(v[1] for v in vals),
              'landing_minus_approach_mean_m_s':statistics.mean(v[2] for v in vals)
            }
        paired={}
        for label,idx in (('near_flower',1),('landing_minus_approach',2)):
            d=matched_by_bee(tracks,method,cutoff,idx)
            if len(d)<2:raise ValueError('NO_GO_FEWER_THAN_TWO_PAIRED_B_LABELS')
            jack=[statistics.mean(d[:i]+d[i+1:]) for i in range(len(d))]
            paired[label]={
              'n_paired_B_labels':len(d),
              'equal_B_mean_W1_minus_W0_m_s':statistics.mean(d),
              'positive_B_labels':sum(v>0 for v in d),
              'negative_B_labels':sum(v<0 for v in d),
              'leave_one_B_out_min_m_s':min(jack),
              'leave_one_B_out_max_m_s':max(jack)
            }
        specs.append({'filter_hz':cutoff,'speed_method':method,
                      'wind_group_track_means':stage,'B_S_P_matched':paired})
    return {
      'status':'ORIGINAL_157_ARCHIVED_TRACKS_SIX_METHOD_SENSITIVITY',
      'original_source':'Chang et al 2016 Zenodo 60234',
      'source_W0_W1_filename_counts':dict(sorted(counts.items())),
      'published_primary_112':{'calm':60,'wind':52},
      'source_W0_less_than_paper_calm_60':counts['W0']<60,
      'original_112_file_selection_not_recovered':True,
      'filters_hz_prespecified':list(CUTOFFS),
      'speed_methods_prespecified':list(SPEED_METHODS),
      'specifications':specs,
      'not_original_published_mixed_model':True,
      'not_independent_colony_level_inference':True,
      'not_failures_or_pollen_or_seeds_or_fitness':True,
      'no_raw_track_rows_or_author_code_redistributed':True
    }


def main():
    stage39=Path(__file__).resolve().parents[1]/'floral_wind_kinematic_stage39'
    sys.path.insert(0,str(stage39))
    from inspect_original_tracks import (
        source_original_archive,FILENAME_PATTERN,MEASURED_HEADER
    )
    raw,_=source_original_archive()
    tracks=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for filename in sorted(archive.namelist()):
            name=Path(filename).name
            if filename.startswith('__MACOSX/') or name.startswith('._') or not name.endswith('xyzpts.csv'):
                continue
            match=FILENAME_PATTERN.fullmatch(name)
            if not match:raise ValueError('NO_GO_SOURCE_FILENAME_NOT_RECOGNIZED')
            code=match.groupdict()
            tracks.append({
              'B':code['B'],'S':code['S'],'P':code['P'],'W':'W'+code['W'],
              'values':reconstruct_all_filters(archive.read(filename),
                                               header=MEASURED_HEADER)
            })
    receipt=summarize(tracks)
    baseline=next(x for x in receipt['specifications']
                  if x['filter_hz']==100 and x['speed_method']=='three_tag_mean')
    for wind,expected in (('W0',.10151403),('W1',.22636598)):
        if abs(baseline['wind_group_track_means'][wind]['near_flower_mean_m_s']-expected)>1e-5:
            raise ValueError('NO_GO_INDEPENDENT_100HZ_STAGE40_REPRODUCTION')
    if abs(baseline['B_S_P_matched']['near_flower']['equal_B_mean_W1_minus_W0_m_s']-.121429)>1e-5:
        raise ValueError('NO_GO_INDEPENDENT_MATCHED_STAGE40_REPRODUCTION')
    output=Path('stage41_aggregate_receipts')
    output.mkdir(exist_ok=True)
    (output/'six_source_specifications.json').write_text(
        json.dumps(receipt,indent=2,allow_nan=False)+'\n',encoding='utf8'
    )
    print(json.dumps(receipt,sort_keys=True,allow_nan=False))


if __name__=='__main__':
    main()
