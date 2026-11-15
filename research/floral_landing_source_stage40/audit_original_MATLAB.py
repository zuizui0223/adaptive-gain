"""Stage40: original 2016 landing-trial MATLAB source selection/calibration audit.

This step uses the EXACT checksum-verified original Zenodo #60234 ZIP through
Stage39 helpers. It publishes only source-file hashes, file-name/line-number
pointers, and small debugging hints (stdout only) about the ORIGINAL analysis
software. It NEVER treats 157 xyzpts files as published 112 selected tracks
or asserts a physical speed without calibrated unit and timing.

Original source and paper 10.1242/jeb.137976, CC-BY original Zenodo source.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent

TARGET_BASENAMES=(
 'analyzeTrackingData.m','trackBEEtagForDLT.m','trackTriangleForDLT.m',
 'datarotate.m','rpyout.m','rpyoutJC.m',
)
PATTERNS={
 'sampling_frequency':r'\b(1000|1000hz|fps|framerate|frameRate|samplingRate|dt|dT)\b',
 'filtering':r'\b(butter|filtfilt|cutoff|lowpass|low.pass|filter)\b',
 'xyz_input':r'xyzpts|readtable|csvread|dlmread|textscan|xlsread|load\(',
 'trajectory_identity':r'(file[name]?|track|trial|wind|parallel|perpen|fixed|orientation|condition|stem)',
 'spatial_units':r'(dlt|cm|mm|meter|metre|unit|scale|cent[er]{1,2}|origin|flower|dist)',
 'selection':r'(exclude|reject|select|nan|isnan|valid|keep|threshold|quality)',
 'velocity':r'(accel|velocity|speed|diff\(|gradient|derivat)',
}
MAX_HINTS_PER_SCRIPT=55
MAX_SOURCE_BLOB=600_000
MAX_CODE_LINES=10000


def _sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()


def source_script_inventory(archive_bytes:bytes, include_excerpt=False):
    if not isinstance(archive_bytes,bytes) or not zipfile.is_zipfile(io.BytesIO(archive_bytes)):
        raise ValueError('NO_GO_SOURCE_NOT_VERIFIED_ZIP_BYTES')
    source_hashes={}
    hints=[]
    parse_warnings=[]
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as z:
        names=z.namelist()
        selected=[n for n in names if Path(n).name in TARGET_BASENAMES
                  and not n.startswith('__MACOSX/') and not Path(n).name.startswith('._')]
        if not any(Path(n).name=='analyzeTrackingData.m' for n in selected):
            raise ValueError('NO_GO_ORIGINAL_PRIMARY_ANALYSIS_SCRIPT_MISSING')
        if len({Path(n).name for n in selected})!=len(selected):
            raise ValueError('NO_GO_AMBIGUOUS_AUTHOR_SCRIPT_PATH')
        for name in sorted(selected):
            info=z.getinfo(name)
            if info.file_size>MAX_SOURCE_BLOB:
                raise ValueError('NO_GO_ORIGINAL_SCRIPT_OVERSIZED')
            raw=z.read(name)
            file=Path(name).name
            lines=raw.decode('latin1',errors='replace').splitlines()
            if len(lines)>MAX_CODE_LINES:
                raise ValueError('NO_GO_AUTHOR_SOURCE_TOO_MANY_LINES')
            lex=Counter()
            matches=[]
            for i,line in enumerate(lines,1):
                if line.lstrip().startswith('%'):continue
                tags=[k for k,pat in PATTERNS.items() if re.search(pat,line,re.I)]
                for k in tags:lex[k]+=1
                # Keep only location and *small* source excerpt; output at
                # most 55 short source rows per script. User-facing result
                # will ONLY state a semantic summary and original file IDs.
                if tags and len(matches)<MAX_HINTS_PER_SCRIPT:
                    matches.append({
                        'line_number':i,
                        'tags':tags,
                        'excerpt_debug_ONLY':line.strip()[:190]
                    })
            source_hashes[file]={
              'original_zip_member':name,
              'source_blob_sha256':_sha(raw),
              'original_lines':len(lines),
              'source_id_tags_count':dict(lex),
              'matched_source_line_numbers':[z['line_number'] for z in matches],
              'hints_limited':len(matches)>=MAX_HINTS_PER_SCRIPT
            }
            if include_excerpt:
                hints.extend({'source_file':file,**z} for z in matches)
    return {
        'status':'ORIGINAL_AUTHOR_MATLAB_SOURCE_POINTERS_ONLY',
        'primary_code_sha256_verified_from_zip_not_inferred_from_Web':True,
        'script_inventory':source_hashes,
        'source_code_debug_hints':hints if include_excerpt else [],
        'source_ZIP_member_count':len(names),
        'author_published_112_tracks_selection_recovered':False,
        'original_meter_per_native_unit_recovered':False,
        'original_frame_index_for_each_csv_row_verified':False,
        'physical_m_per_s_difference_estimated':False,
        'no_pseudoreplicate_frames':True,
        'no_source_MATLAB_code_or_raw_data_redistributed':True
    }


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='stage40_method_source_receipts')
    ap.add_argument('--debug-limited-excerpts',action='store_true')
    opts=ap.parse_args(argv)
    from inspect_original_tracks import source_original_archive
    source,original=source_original_archive()
    raw=source_script_inventory(source,include_excerpt=opts.debug_limited_excerpts)
    # The shipped JSON receipt has only pointers and hashes. Never package
    # author original text in artifacts, even when debug CLI prints excerpts.
    out={**raw,'source_code_debug_hints':[]}
    out['original_record_id']=60234
    out['original_public_archive_sha256']=original['source_sha256']
    out['original_public_archive_md5']=original['source_md5']
    dest=Path(opts.out)
    dest.mkdir(parents=True,exist_ok=True)
    (dest/'stage40_original_MATLAB_calibration_pointers.json').write_text(
        json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print('STAGE40_ORIGINAL_MATLAB_SOURCE_POINTERS_AUDITED')
    print(json.dumps({'source_files':{
      k:{'sha256':v['source_blob_sha256'],
         'lines':v['original_lines'],
         'tags':v['source_id_tags_count']}
      for k,v in raw['script_inventory'].items()},
      'source_archive':original['source_sha256'],
      'not_kinematic_calibration_or_m_s_claim':True},sort_keys=True))
    if opts.debug_limited_excerpts:
        for item in raw['source_code_debug_hints']:
            print('ORIGINAL_DEBUG_HINT',item['source_file'],item['line_number'],
                  ','.join(item['tags']),item['excerpt_debug_ONLY'])


if __name__=='__main__':
    main()
