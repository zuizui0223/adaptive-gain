"""Stage40: validate the original flower LANDMARK encoding and data selection.

Source: exact checksum-verified Chang et al 2016 Zenodo #60234 ZIP, not a
photographed flower or recreated raw record. No original time series saved.

Crucial: the original MATLAB analysis explicitly selects the single
nonmissing pt7 (columns 19:21) as the origin, then subtracts it from every
3D tag point. Thus apparent pt4..7 "missingness" may be deliberate static
landmark encoding, not tracking failure. Verify this in *every* source file.

Original DOI 10.1242/jeb.137976, 1000fps camera; source filename original
MATLAB wind=filename(27), P=position, S=stiffness, B=beeNumber.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import statistics
from collections import Counter,defaultdict
from pathlib import Path

from inspect_original_tracks import (
    source_original_archive,FILENAME_PATTERN,MEASURED_HEADER
)

EXPECTED_SOURCE_W={'W0':56,'W1':101}
EXPECTED_SOURCE_N=157
EXPECTED_PAPER_TRACKS=112
PAPER_CALM_TRACKS=31+29
PAPER_WIND_TRACKS=27+25


def _real(s):
    if s.strip().lower() in ('','nan','na','null','none','inf','-inf'):
        return None
    try:val=float(s)
    except ValueError as exc:raise ValueError('NO_GO_BAD_ORIGINAL_COORDINATE') from exc
    return val if math.isfinite(val) else None


def _profile(raw):
    text=raw.decode('utf-8-sig')
    reader=csv.DictReader(io.StringIO(text,newline=''))
    if tuple(reader.fieldnames or ())!=MEASURED_HEADER:
        raise ValueError('NO_GO_SOURCE_7_POINT_HEADER_CHANGED')
    static=[0]*4
    tag_complete=0
    tag_consecutive=0
    landmark_ix=[]
    roi1=0
    roi2=0
    prev_good=False
    frames=0
    pt2_cache=[]
    for row in reader:
        if not any(v.strip() for v in row.values()):continue
        frames+=1
        points=[tuple(_real(row[f'pt{j}_{axis}']) for axis in 'XYZ')
                for j in range(1,8)]
        ok=[all(v is not None for v in pt) for pt in points]
        yes=all(ok[:3])
        tag_complete+=int(yes)
        tag_consecutive+=int(prev_good and yes)
        prev_good=yes
        for j in range(3,7):
            static[j-3]+=int(ok[j])
        if ok[6]:
            landmark_ix.append((frames,points[6]))
        if ok[1]:
            pt2_cache.append(points[1])
    if frames<3:
        raise ValueError('NO_GO_ORIGINAL_TRACK_TOO_SHORT')
    if len(landmark_ix)!=1:
        return {'status':'NO_GO_NO_UNIQUE_FLOWER_LANDMARK',
                'frames':frames,'landmark_pt7_records':len(landmark_ix),
                'pt4_7_presence':static,'complete_3tag_frames':tag_complete,
                'valid_consecutive_3tag_pairs':tag_consecutive,
                'approach_pt2_count':None,'landing_pt2_count':None}
    center=landmark_ix[0][1]
    approach=sum(.05<math.dist(pt,center)<.07 for pt in pt2_cache)
    landing=sum(.015<math.dist(pt,center)<.03 for pt in pt2_cache)
    return {'status':'ORIGINAL_ONE_LANDMARK_PER_TRACK',
            'frames':frames,'landmark_pt7_records':1,
            'pt4_7_presence':static,'complete_3tag_frames':tag_complete,
            'valid_consecutive_3tag_pairs':tag_consecutive,
            'approach_pt2_count':approach,'landing_pt2_count':landing,
            'flower_landmark_recorded_as_static_not_animal_tracking':True,
            'no_raw_flower_center_coordinates_saved':True}


def assess_original_archive(blob):
    import zipfile
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError('NO_GO_ORIGINAL_DATA_NOT_A_ZIP')
    results=[]
    groups=defaultdict(list)
    site_codes=Counter()
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        for name in archive.namelist():
            file=Path(name).name
            if name.startswith('__MACOSX/') or not file.endswith('xyzpts.csv'):
                continue
            m=FILENAME_PATTERN.fullmatch(file)
            if not m:
                raise ValueError('NO_GO_ORIGINAL_FILENAME_NOT_AUTHENTIC')
            codes=m.groupdict()
            audit=_profile(archive.read(name))
            audit['B']=codes['B']
            audit['P']=codes['P']
            audit['S']=codes['S']
            audit['W']='W'+codes['W']
            results.append(audit)
            groups[audit['W']].append(audit)
            site_codes[f"S{codes['S']}_P{codes['P']}_W{codes['W']}"]+=1
    if len(results)!=EXPECTED_SOURCE_N:
        raise ValueError('NO_GO_ORIGINAL_TRACK_FILE_COUNT_CHANGED')
    winds={k:len(v) for k,v in sorted(groups.items())}
    if winds!=EXPECTED_SOURCE_W:
        raise ValueError('NO_GO_ORIGINAL_WIND_FILENAME_COUNTS_CHANGED')
    statuses=Counter(r['status'] for r in results)
    landmark_counts=Counter(r['landmark_pt7_records'] for r in results)
    pt4_7=Counter()
    for r in results:
        for j,x in enumerate(r['pt4_7_presence'],4):
            pt4_7[f'pt{j}_nonmissing_frame_total']+=x
    successful=[r for r in results if r['status']=='ORIGINAL_ONE_LANDMARK_PER_TRACK']
    def rate(k):
        return sum(r[k] for r in successful)
    n=rate('frames')
    complete=rate('complete_3tag_frames')
    k=rate('valid_consecutive_3tag_pairs')
    def distribution(key):
        v=[r[key] for r in successful]
        return {'n_tracks':len(v),'min':min(v),'median':statistics.median(v),
                'max':max(v),'mean':statistics.mean(v)}
    windgroup={}
    for w,subset in sorted(groups.items()):
        wgood=[r for r in subset if r['status']=='ORIGINAL_ONE_LANDMARK_PER_TRACK']
        windgroup[w]={
          'files':len(subset),
          'valid_static_flower_landmarks':len(wgood),
          'total_complete_3tag_frames':sum(r['complete_3tag_frames'] for r in wgood),
          'total_consecutive_3tag_pairs':sum(r['valid_consecutive_3tag_pairs'] for r in wgood),
          'tracks_with_approach_window':sum(r['approach_pt2_count']>0 for r in wgood),
          'tracks_with_landing_window':sum(r['landing_pt2_count']>0 for r in wgood),
          'tracks_with_both_windows':sum(
            r['approach_pt2_count']>0 and r['landing_pt2_count']>0 for r in wgood)
        }
    return {
      'status':'ORIGINAL_STATIC_FLOWER_LANDMARK_ENCODING_CONFIRMED'
        if len(successful)==len(results) and landmark_counts=={1:EXPECTED_SOURCE_N}
        else 'NO_GO_PARTIAL_STATIC_REFERENCE_ENCODING',
      'source_archive_file_count':len(results),
      'wind_file_codes':winds,
      'source_S_P_W_cross_counts':dict(sorted(site_codes.items())),
      'original_7point_table_not_seven_moving_body_markers':True,
      'original_MATLAB_uses_pt7_as_single_flower_origin':True,
      'pt7_records_per_original_trajectory_distribution':dict(landmark_counts),
      'status_counts':dict(statuses),
      'pt4_7_record_totals':dict(pt4_7),
      'original_track_frames_counted':n,
      'valid_3moving_tag_frames_counted':complete,
      'consecutive_valid_frame_pairs_for_1000fps_speed':k,
      'valid_3moving_tag_frame_fraction':complete/n,
      'valid_consecutive_frame_pair_fraction':k/max(1,n-len(successful)),
      'approach_5_to_7_cm_pt2_frame_count':rate('approach_pt2_count'),
      'landing_1p5_to_3_cm_pt2_frame_count':rate('landing_pt2_count'),
      'pt2_approach_per_track':distribution('approach_pt2_count'),
      'pt2_landing_per_track':distribution('landing_pt2_count'),
      'wind_group_eligibility':windgroup,
      'published_primary_tracks':EXPECTED_PAPER_TRACKS,
      'published_calm_tracks_if_W0_means_no_wind':PAPER_CALM_TRACKS,
      'original_W0_file_count':winds['W0'],
      'published_calm_tracks_exceed_archived_W0_if_one_file_per_path':
            PAPER_CALM_TRACKS>winds['W0'],
      'no_verified_original_112_track_selection':True,
      'no_raw_coordinate_or_original_reference_point_copied':True,
      'physical_wind_effect_not_fit_by_this_audit':True
    }


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='stage40_static_landmark_receipts')
    opts=ap.parse_args(argv)
    blob,provenance=source_original_archive()
    a=assess_original_archive(blob)
    a['original_source_archive_sha256']=provenance['source_sha256']
    a['original_source_archive_md5']=provenance['source_md5']
    d=Path(opts.out);d.mkdir(parents=True,exist_ok=True)
    (d/'stage40_static_flower_landmark_source_audit.json').write_text(
       json.dumps(a,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps(a,sort_keys=True,allow_nan=False))
    if a['status']!='ORIGINAL_STATIC_FLOWER_LANDMARK_ENCODING_CONFIRMED':
        raise SystemExit(1)


if __name__=='__main__':
    main()
