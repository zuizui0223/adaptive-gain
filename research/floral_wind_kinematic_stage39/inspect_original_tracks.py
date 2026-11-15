"""Stage39: physically honest profiling of original 2016 bee landing tracks.

DO NOT report a new aerodynamic rate until author source selection, camera
timing/units, flower origin and body-point composition have been checked.
This code reads the original checksum-verified public Zenodo #60234 archive,
not a fabricated landing CSV. It saves aggregate provenance and profile
data only, never republished flight rows or authors' complete MATLAB files.

2016 paper 10.1242/jeb.137976: 1000-Hz video, DLT 3-D positions, fifth-order
Butterworth 100-Hz cutoff, approach 5–7cm, landing 1.5–3cm, 112 selected
tracks from 28 bees across 4 principal conditions (N=31,27,29,25).
The source ZIP contains 157 filename-marked xyz tracks, not blindly 112
paper-selected trials; at most the overlapping subset can reproduce results.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
import sys
import zipfile

HERE=Path(__file__).resolve().parent
EARLIER=HERE.parent/'floral_wind_landing_stage38'
sys.path.insert(0,str(EARLIER))
from landing_original_sources import (  # noqa: E402
    _fetch,inspect_zenodo,ZENODO_API,ZENODO_FILE,ZENODO_MD5,
)

EXPECTED_TRACK_FILE_COUNT=157
EXPECTED_B_LABEL_COUNT=28
EXPECTED_W_COUNTS={'W0':56,'W1':101}
PAPER_SELECTED_TRACKS=112
PAPER_TRACK_W_GROUPS={'W0':60,'W1':52}
PAPER_N_BEE=28
PAPER_FPS=1000
MEASURED_HEADER=tuple(
    f'pt{i}_{axis}' for i in range(1,8) for axis in 'XYZ'
)
FILENAME_PATTERN=re.compile(
 r'^B(?P<B>[0-9]+)_BC(?P<BC>[0-9]+)_F(?P<F>[0-9]+)_S(?P<S>[0-9]+)_'
 r'P(?P<P>[0-9]+)_T(?P<T>[0-9]+)_W(?P<W>[01])_.*xyzpts[.]csv$',
 re.I
)
MAX_ROWS_PER_TRACK=50000


def source_original_archive():
    meta=json.loads(_fetch(ZENODO_API,max_bytes=900_000).decode('utf-8'))
    f=[x for x in meta.get('files',[]) if x.get('key')==ZENODO_FILE]
    if len(f)!=1:
        raise ValueError('NO_GO_ARCHIVE_IDENTIFIER_CHANGED')
    url=(f[0].get('links') or {}).get('self')
    if not isinstance(url,str):
        raise ValueError('NO_GO_SOURCE_FILE_DOWNLOAD_LINK_MISSING')
    blob=_fetch(url,max_bytes=10_000_000)
    receipt=inspect_zenodo(meta,blob)
    if receipt['status']!='REAL_ORIGINAL_CHANG_LANDING_ARCHIVE_VERIFIED':
        raise ValueError('NO_GO_ORIGINAL_ARCHIVE_HASH_NOT_VERIFIED')
    return blob,receipt


def _read_numeric(value):
    text=value.strip()
    if not text or text.lower() in ('na','nan','none','null','inf','-inf'):
        return None
    try:
        v=float(text)
    except ValueError:
        raise ValueError('NO_GO_NON_NUMERIC_SOURCE_COORDINATE')
    return v if math.isfinite(v) else None


def profile_track(raw):
    """Profile expected source column names and geometry, never infer m/s."""
    if not isinstance(raw,bytes):
        raise ValueError('NO_GO_TRACK_INPUT_NOT_BYTES')
    try:
        text=raw.decode('utf-8-sig')
    except UnicodeDecodeError as err:
        raise ValueError('NO_GO_SOURCE_TRACK_UNEXPECTED_ENCODING') from err
    source=csv.reader(io.StringIO(text))
    header=tuple(next(source,[]))
    if header!=MEASURED_HEADER:
        raise ValueError('NO_GO_TRACK_MARKER_HEADER_NOT_VALIDATED')
    n=0
    valid_coord=0
    full_frame=0
    any_frame=0
    valid_triplets=[0]*7
    min_xyz=[None]*3
    max_xyz=[None]*3
    marker1_positions=[]
    for row in source:
        if not row or all(not c.strip() for c in row):
            continue
        if len(row)!=len(header):
            raise ValueError('NO_GO_TRACK_COORDINATE_ROW_ARITY')
        n+=1
        if n>MAX_ROWS_PER_TRACK:
            raise ValueError('NO_GO_TRACK_EXCEEDS_FRAME_SAFETY_LIMIT')
        vals=[_read_numeric(v) for v in row]
        valid_coord+=sum(v is not None for v in vals)
        triples=[all(v is not None for v in vals[i*3:(i+1)*3])
                 for i in range(7)]
        for i,yes in enumerate(triples):
            valid_triplets[i]+=int(yes)
        full_frame+=int(all(triples))
        any_frame+=int(any(triples))
        for j,axis in enumerate('XYZ'):
            axisvals=[vals[i] for i in range(j,len(vals),3) if vals[i] is not None]
            if not axisvals:
                continue
            low=min(axisvals);high=max(axisvals)
            min_xyz[j]=low if min_xyz[j] is None else min(low,min_xyz[j])
            max_xyz[j]=high if max_xyz[j] is None else max(high,max_xyz[j])
        if triples[0]:
            marker1_positions.append((vals[0],vals[1],vals[2]))
    if n==0:
        raise ValueError('NO_GO_EMPTY_SOURCE_TRACK')
    return {
      'frames':n,'marker_3d_complete_per_point':valid_triplets,
      'complete_7_marker_frames':full_frame,
      'at_least_one_complete_marker_frames':any_frame,
      'all_coordinates_valid_fraction':valid_coord/(n*21),
      'per_axis_native_min':min_xyz,
      'per_axis_native_max':max_xyz,
      'marker1_valid_frames':len(marker1_positions),
      'marker1_first_last_displacement_native_units':(
          math.dist(marker1_positions[0],marker1_positions[-1])
          if len(marker1_positions)>=2 else None),
      'source_header_21_marker_coordinates_verified':True,
      'no_assumed_physical_coordinate_units':True,
      'no_assumed_seconds_between_retained_rows':True
    }


def _distribution(values):
    if not values:
        return None
    return {
      'n':len(values),
      'min':min(values),'median':statistics.median(values),
      'max':max(values),'mean':statistics.mean(values)
    }


def profile_original_kinematic_archive(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError('NO_GO_ORIGINAL_LANDING_ZIP_INVALID')
    combos=Counter()
    wind=Counter()
    labels=defaultdict(set)
    file_bee_counts=Counter()
    tracks=[]
    structural_errors=[]
    matlab_files=[]
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        names=archive.namelist()
        for filename in names:
            basename=Path(filename).name
            if (filename.startswith('__MACOSX/') or basename.startswith('._') or
                basename=='.DS_Store'):
                continue
            if basename.lower().endswith('.m'):
                matlab_files.append(filename)
            if not basename.lower().endswith('xyzpts.csv'):
                continue
            match=FILENAME_PATTERN.fullmatch(basename)
            if not match:
                structural_errors.append(basename[:100])
                continue
            labels_src=match.groupdict()
            p=profile_track(archive.read(filename))
            w='W'+labels_src['W']
            wind[w]+=1
            combos[f"S{labels_src['S']}_P{labels_src['P']}_W{labels_src['W']}"]+=1
            file_bee_counts[labels_src['B']]+=1
            for name in ('F','BC','T','S','P','W'):
                labels[name].add(labels_src[name])
            p.update({
                'wind_source_filename_code':w,
                'source_B_label':labels_src['B'],
                'source_S_code':labels_src['S'],
                'source_P_code':labels_src['P'],
                'source_F_code':labels_src['F'],
            })
            tracks.append(p)
        # Code inspection is strictly token presence and filename counts,
        # not source-code redistribution or physically measured results.
        authored=[f for f in matlab_files if '/lib/' not in f.lower() and
                  '/matlabtoolbox/' not in f.lower()]
        tokens=('1000','100 Hz','butter','xyzpts','fps','frame rate',
                'cutoff','timepoint','flower','landing','DLT','dt','pt1')
        code_token_counts={}
        for token in tokens:
            matches=[]
            for filename in authored:
                code=archive.read(filename).decode('latin1',errors='replace')
                if token.lower() in code.lower():
                    matches.append(Path(filename).name)
            code_token_counts[token]={
               'files_matching':len(matches),
               'some_file_names':sorted(set(matches))[:8]
            }
    if structural_errors:
        raise ValueError('NO_GO_UNRECOGNIZED_SOURCE_TRACK_FILENAME')
    if len(tracks)!=EXPECTED_TRACK_FILE_COUNT or len(file_bee_counts)!=EXPECTED_B_LABEL_COUNT:
        raise ValueError('NO_GO_ORIGINAL_157_FILES_28_LABELS_CHANGED')
    if dict(sorted(wind.items()))!=EXPECTED_W_COUNTS:
        raise ValueError('NO_GO_ORIGINAL_SOURCE_W0_W1_CHANGED')
    return {
       'status':'ORIGINAL_157_CHANG_TRACKS_PROFILED_SOURCE_GRAIN_ONLY',
       'source_trial_file_count':len(tracks),
       'source_filename_B_labels':len(file_bee_counts),
       'source_filename_W0_W1_file_count':dict(sorted(wind.items())),
       'source_label_cross_counts':dict(sorted(combos.items())),
       'source_per_B_file_count_distribution':_distribution(list(file_bee_counts.values())),
       'source_label_cardinalities':{k:len(v) for k,v in labels.items()},
       'total_original_frame_rows':sum(x['frames'] for x in tracks),
       'frame_count_per_record':_distribution([x['frames'] for x in tracks]),
       'full_7_marker_fraction_across_frames':
         sum(x['complete_7_marker_frames'] for x in tracks)/sum(x['frames'] for x in tracks),
       'at_least_1_marker_fraction_across_frames':
         sum(x['at_least_one_complete_marker_frames'] for x in tracks)/sum(x['frames'] for x in tracks),
       'marker_3d_completeness_overall':[
         sum(x['marker_3d_complete_per_point'][i] for x in tracks)/
         sum(x['frames'] for x in tracks) for i in range(7)],
       'coordinate_native_value_axis_range':{
          axis:{'min':min(x['per_axis_native_min'][i] for x in tracks if x['per_axis_native_min'][i] is not None),
                'max':max(x['per_axis_native_max'][i] for x in tracks if x['per_axis_native_max'][i] is not None)}
          for i,axis in enumerate('XYZ')
       },
       'per_track_marker1_first_last_displacement_native_units':
          _distribution([x['marker1_first_last_displacement_native_units']
                         for x in tracks if x['marker1_first_last_displacement_native_units'] is not None]),
       'authored_nonlibrary_matlab_code_files':len(authored),
       'author_matlab_source_token_inventory':code_token_counts,
       'published_camera_frames_per_second':PAPER_FPS,
       'paper_original_independent_B_bees':PAPER_N_BEE,
       'paper_selected_tracks_primary_conditions':PAPER_SELECTED_TRACKS,
       'paper_selected_W0_W1':PAPER_TRACK_W_GROUPS,
       'published_112_selected_not_equal_157_original_files':True,
       'file_W0_W1_codes_not_yet_independently_mapped_to_actual_m_s':True,
       'source_B_label_is_a_filename_ID_not_independently_verified_animal_identity':True,
       'all_original_csv_rows_are_NOT_independent_kinematic_replicates':True,
       'physical_speed_or_deceleration_measured_m_s':False,
       'approach_5_7_cm_landing_1p5_3_cm_not_reconstructed':True,
       'no_plant_fitness_or_scent_by_wind_claim':True,
       'no_original_track_rows_or_matlab_code_redistributed':True
    }


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='stage39_kinematic_source_receipts')
    opts=parser.parse_args(argv)
    data,source=source_original_archive()
    receipt=profile_original_kinematic_archive(data)
    receipt['original_zenodo_record']=60234
    receipt['original_file_md5']=ZENODO_MD5
    receipt['original_zip_sha256']=source['source_sha256']
    folder=Path(opts.out);folder.mkdir(parents=True,exist_ok=True)
    path=folder/'stage39_original_track_grain_profile.json'
    path.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps({
      'status':receipt['status'],
      'source_trial_file_count':receipt['source_trial_file_count'],
      'original_source_B_labels':receipt['source_filename_B_labels'],
      'file_wind_counts':receipt['source_filename_W0_W1_file_count'],
      'source_label_cross_counts':receipt['source_label_cross_counts'],
      'source_label_cardinalities':receipt['source_label_cardinalities'],
      'frame_count_per_record':receipt['frame_count_per_record'],
      'total_original_frame_rows':receipt['total_original_frame_rows'],
      'full_7_marker_fraction_across_frames':receipt['full_7_marker_fraction_across_frames'],
      'marker_3d_completeness_overall':receipt['marker_3d_completeness_overall'],
      'coordinate_native_value_axis_range':receipt['coordinate_native_value_axis_range'],
      'source_code_calibration_tokens':{
         k:v for k,v in receipt['author_matlab_source_token_inventory'].items()
         if k in ('1000','butter','xyzpts','fps','DLT','cutoff')
      },
      'no_new_kinematic_physical_effect_claim':True
    },sort_keys=True,allow_nan=False))


if __name__=='__main__':
    main()
