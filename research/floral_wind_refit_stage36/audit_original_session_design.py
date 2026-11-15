"""Stage36 source-locked diagnostic: inspect original Crall session semantics.

Original study DOI:10.1098/rsbl.2020.0103; Zenodo author-published record
3743898. Neither the original ZIP nor row-level records are committed or
uploaded. Only source hashes, denominators, categorical values, missingness,
site-level aggregated ranges and original model formula identifiers.

This script intentionally DOES NOT estimate a wind effect until the
original "keep" policy, relative TKE transformation, bait exposure and
session-vs-bee count agreement are checked.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
import zipfile

EARLIER=Path(__file__).resolve().parents[1] / 'floral_wind_author_stage35'
sys.path.insert(0,str(EARLIER))
from zenodo_crall_original_source import (  # noqa: E402
    _fetch, _candidate_download_urls, assess_api_metadata, _verify_md5_if_declared
)

PINNED_RECORD=3743898
DATA_FILES=(
 'Zenodo/collectionMetadata.csv',
 'Zenodo/integratedSpatialWindData.csv',
 'Zenodo/beedata.csv',
 'Zenodo/GenerateFiguresAndAnalyses_CrallEtAl_OrchidBeeWindEcology.R',
)
ALLOWED_COLUMNS={
  'collectionMetadata.csv':('site','date','start.time','scent','count','wind.mean','rel.wind.KE'),
  'integratedSpatialWindData.csv':('coll.id','date','site','start.time','scent','wind.file','keep',
   'count','cover','cover200m','rel.bee.count','wind.mean','wind.mean.3d','wind.KE',
   'wind.mean.direction','turbInt','turbInt.3d'),
}

def _read_rows(raw):
    text=raw.decode('utf-8-sig')
    source=csv.reader(io.StringIO(text))
    header=next(source,None)
    if header is None:raise ValueError('NO_GO_EMPTY_CSV')
    if not header[0].strip():
        header[0]='_original_row_index'
    if len(set(header))!=len(header):
        raise ValueError('NO_GO_DUPLICATE_HEADER')
    rows=[]
    for values in source:
        if len(values)!=len(header):
            raise ValueError('NO_GO_ROW_FIELD_COUNT')
        rows.append(dict(zip(header,values)))
    return header,rows

def _finite_number(value):
    if not isinstance(value,str) or value.strip().lower() in ('','na','nan','null'):
        return None
    try:return float(value)
    except ValueError:return None

def _range_by(rows,column):
    data=[_finite_number(r.get(column,'')) for r in rows]
    present=[x for x in data if x is not None]
    return {'n_total':len(data),'n_numeric':len(present),
            'n_missing':len(data)-len(present),
            'min':min(present) if present else None,
            'max':max(present) if present else None,
            'mean':sum(present)/len(present) if present else None}

def _categories(rows,column):
    counter=Counter((x.get(column) or '').strip() for x in rows)
    return dict(sorted(counter.items()))

def _source_r_analysis_markers(code):
    """Short original-model diagnostics, not a reproduction of author script."""
    lines=code.decode('utf-8-sig',errors='replace').splitlines()
    terms=('glmer(', 'glm(', 'lmer(', 'rel.bee.count','rel.wind.KE',
           'wind.mean','keep', 'offset(', 'scale(', 'scent', 'forest.cover')
    # A short set of identifiers for auditing downstream model specification.
    counts={q:sum(q in line for line in lines) for q in terms}
    formula_candidates=[]
    for line in lines:
        if re.search(r'\b(glmer|glm|glmmTMB|lmer)\s*\(',line) and len(line)<250:
            # Names/formulas may span several lines; do not infer complete model.
            formula_candidates.append(line.strip()[:220])
    return {'line_count':len(lines),
            'source_code_sha256':hashlib.sha256(code).hexdigest(),
            'selected_identifier_counts':counts,
            'model_call_openers':formula_candidates[:12],
            'complete_original_model_formula_verified':False}

def audit_archive(blob, metadata, source_file='CrallEtAl_OrchidBeeWindEcology.zip'):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError('NO_GO_BAD_AUTHOR_ZIP')
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names=set(z.namelist())
        if any(x not in names for x in DATA_FILES):
            raise ValueError('NO_GO_EXPECTED_ORIGINAL_SESSION_SOURCE_MISSING')
        byfile={}
        raw={}
        for name in DATA_FILES:
            raw[name]=z.read(name)
        for name in DATA_FILES[:3]:
            header,rows=_read_rows(raw[name])
            key=Path(name).name
            if key in ALLOWED_COLUMNS:
                missing=set(ALLOWED_COLUMNS[key])-set(header)
                if missing:raise ValueError('NO_GO_MISSING_REQUIRED_SOURCE_COLUMNS_'+str(sorted(missing)))
            byfile[key]={
              'n_rows':len(rows),'n_header_cols':len(header),
              'original_columns':header,
              'raw_sha256':hashlib.sha256(raw[name]).hexdigest(),
            }
            if key!='beedata.csv':
                for col in ('count','wind.mean','rel.wind.KE','wind.KE','rel.bee.count','cover200m'):
                    if col in header:
                        byfile[key][col+'_profile']=_range_by(rows,col)
                for col in ('site','scent','keep'):
                    if col in header:
                        byfile[key][col+'_values']=_categories(rows,col)
                byfile[key]['observed_unique_dates']=len(set(r.get('date') for r in rows))
                byfile[key]['unique_site_date_scent_combinations']=len(set(
                    (r.get('site'),r.get('date'),r.get('scent')) for r in rows))
        # Aggregates only — inspect mismatch rather than silently forcing 409.
        h,collection=_read_rows(raw[DATA_FILES[0]])
        h,integrated=_read_rows(raw[DATA_FILES[1]])
        h,bees=_read_rows(raw[DATA_FILES[2]])
        summed={
         'all_collection_count':sum(_finite_number(r['count']) or 0 for r in collection),
         'all_integrated_count':sum(_finite_number(r['count']) or 0 for r in integrated),
         'bee_table_rows':len(bees),
         'bee_table_unique_original_numeric_ids':len(set(x.get('number') for x in bees)),
         'bee_species_values_present':len(set(
             (x.get('genus'),x.get('species')) for x in bees)),
         'source_site_labels_consistent':set(x.get('site') for x in collection)==
                                         set(x.get('site') for x in integrated),
         'record_410_vs_450_reconciliation_not_assumed':True
        }
        rmarkers=_source_r_analysis_markers(raw[DATA_FILES[3]])
    return {
      'status':'ORIGINAL_AUTHOR_SESSION_DESIGN_AUDITED_NOT_STATISTICAL_REFIT',
      'author_record_id':PINNED_RECORD,
      'source_paper_doi':'10.1098/rsbl.2020.0103',
      'author_archive_name':source_file,
      'author_archive_sha256':hashlib.sha256(blob).hexdigest(),
      'source_metadata_doi':metadata.get('doi'),
      'files':byfile,
      'cross_source_denominator_checks':summed,
      'author_R_script':rmarkers,
      'visitation_effect_estimated':False,
      'scent_on_off_randomized_in_this_experiment':False,
      'plant_pollen_transfer_measured':False,
      'session_is_primary_analysis_unit_not_bee_row':True,
      'no_raw_author_rows_or_code_uploaded':True,
    }

def run():
    meta=json.loads(_fetch(f'https://zenodo.org/api/records/{PINNED_RECORD}').decode('utf8'))
    check=assess_api_metadata(meta,PINNED_RECORD)
    if meta.get('id')!=PINNED_RECORD:
        raise ValueError('NO_GO_AUTHOR_SOURCE_VERSION_MISMATCH')
    links=_candidate_download_urls(meta)
    if len(links)!=1:
        raise ValueError('NO_GO_AMBIGUOUS_OR_MISSING_AUTHOR_ZIP')
    filename,url,checksum,size=links[0]
    raw=_fetch(url)
    if len(raw)!=size:
        raise ValueError('NO_GO_AUTHOR_ARCHIVE_SIZE_CHANGED')
    _verify_md5_if_declared(raw,checksum)
    return audit_archive(raw,meta,source_file=filename)

if __name__=='__main__':
    try:
        receipt=run()
    except Exception as exc:
        receipt={'status':'NO_GO_ORIGINAL_AUTHOR_SOURCE_NOT_ANALYZABLE',
                 'error_type':type(exc).__name__,
                 'message':str(exc)[:250],
                 'visitation_effect_estimated':False,
                 'no_raw_author_rows_or_code_uploaded':True}
    folder=Path('stage36_original_receipts')
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'stage36_crall_original_session_design.json').write_text(
      json.dumps(receipt,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps(receipt,ensure_ascii=False,sort_keys=True,allow_nan=False))
    if receipt['status']!='ORIGINAL_AUTHOR_SESSION_DESIGN_AUDITED_NOT_STATISTICAL_REFIT':
        raise SystemExit(1)
