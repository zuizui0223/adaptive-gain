"""Stage31 observed pilot: read pinned FReD sample spectrum (ONE flower record).

A verified independent R-package copy of FReD flowerID_157 from the
photobiologyInOut CRAN mirror is used as an ingestion QA fixture.
It is NOT a multi-sample population estimate, not within-flower UV
nectar-guide presence, not a pollinator photoreceptor model, and
not a replicated macroecological result.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

SOURCE_REPO='cran/photobiologyInOut'
SOURCE_COMMIT='ae409a941e58b302ac714b4f5abc656dd9249c6b'
SOURCE_PATH='inst/extdata/FReDflowerID_157.csv'
GIT_BLOB_SHA='0f9dace9d812cd0c0affc68b58cd7972d86b7f01'
URL=('https://raw.githubusercontent.com/'+SOURCE_REPO+'/'+
     SOURCE_COMMIT+'/'+SOURCE_PATH)
SOURCE_FLOWER_ID=157


def _git_blob_sha(source):
    return hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()


def audit_spectrum(raw,verify_source=True):
    if not isinstance(raw,bytes):
        raise ValueError('NO_GO_SPECTRUM_REQUIRES_RAW_BYTES')
    sha=_git_blob_sha(raw)
    if verify_source and sha!=GIT_BLOB_SHA:
        raise ValueError('NO_GO_FRED_MIRROR_SOURCE_HASH_CHANGED')
    try:
        rd=csv.reader(io.StringIO(raw.decode('utf-8-sig')))
        rows=[r for r in rd if r]
    except UnicodeDecodeError as exc:
        raise ValueError('NO_GO_INVALID_SPECTRUM_ENCODING') from exc
    values={}
    ids=set()
    for r in rows:
        if len(r)!=3:
            raise ValueError('NO_GO_WRONG_FRED_SPECTRUM_GRAIN')
        try:
            sid=int(r[0].strip());w=float(r[1].strip());y=float(r[2].strip())
        except (ValueError,TypeError) as exc:
            raise ValueError('NO_GO_NONNUMERIC_SPECTRAL_ROW') from exc
        if not math.isfinite(y) or y<0 or y>1 or not math.isfinite(w) or w!=int(w):
            raise ValueError('NO_GO_OUT_OF_RANGE_WAVELENGTH_OR_REFLECTANCE')
        w=int(w)
        if w in values:
            raise ValueError('NO_GO_DUPLICATED_WAVELENGTH')
        ids.add(sid)
        values[w]=y
    if verify_source and (ids!={SOURCE_FLOWER_ID} or set(values)!=set(range(300,701))):
        raise ValueError('NO_GO_FRED_SINGLE_SOURCE_WAVELENGTH_COVERAGE')
    if not values:
        raise ValueError('NO_GO_SPECTRUM_EMPTY')
    uv=[v for w,v in values.items() if 300<=w<400]
    vis=[v for w,v in values.items() if 400<=w<=700]
    if not uv or not vis:
        raise ValueError('NO_GO_MISSING_UV_OR_VISIBLE_BAND')
    uvmean=sum(uv)/len(uv)
    vismean=sum(vis)/len(vis)
    return {
      'status':'ONE_SOURCE_SPECTRUM_QA_NOT_A_MACRO_INFERENCE'
                if verify_source else 'SYNTHETIC_SPECTRAL_SOURCE_QA_ONLY',
      'source_repo':SOURCE_REPO,'source_commit':SOURCE_COMMIT,
      'source_path':SOURCE_PATH,
      'source_git_blob_sha1':sha,
      'fred_original_flower_id':SOURCE_FLOWER_ID if verify_source else list(sorted(ids)),
      'source_specimen_record_count':len(ids),
      'spectral_rows':len(values),
      'wavelength_min_nm':min(values),'wavelength_max_nm':max(values),
      'UV_300_399_n':len(uv),'visible_400_700_n':len(vis),
      'UV_300_399_arithmetic_mean_reflectance':uvmean,
      'visible_400_700_arithmetic_mean_reflectance':vismean,
      'UV_to_visible_reflectance_mean_ratio':uvmean/vismean if vismean else None,
      'physical_bee_cone_catches_computed':False,
      'UV_guide_presence_inferred':False,
      'floral_age_or_pollination_state_known':False,
      'within_flower_spatial_contrast_measured':False,
      'scent_from_this_record_measured':False,
      'no_original_pollinator_visitation_observed':True,
      'no_species_level_macro_effect_estimated':True,
      'no_raw_source_copied_to_artifact':True,
    }


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',default=None)
    ap.add_argument('--out',default='stage31_spectral_pilot_receipts')
    args=ap.parse_args(argv)
    if args.input:
        record=audit_spectrum(Path(args.input).read_bytes())
    else:
        record={
          'status':'NO_GO_NO_PINNED_FRED_ORIGINAL_EXAMPLE',
          'UV_guide_presence_inferred':False,
          'no_species_level_macro_effect_estimated':True,
        }
    folder=Path(args.out);folder.mkdir(parents=True,exist_ok=True)
    (folder/'stage31_one_FReD_spectrum_QA.json').write_text(
       json.dumps(record,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':record['status'],
                      'spectral_rows':record.get('spectral_rows',0),
                      'UV_guide_presence_inferred':False},sort_keys=True))


if __name__=='__main__':
    main()
