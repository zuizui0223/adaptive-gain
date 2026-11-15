"""Stage38: original-source landing audit + noncombinable wind stages.

Original sources:
  Chang/Crall/Combes 2016 doi:10.1242/jeb.137976; Zenodo #60234
  Goyal et al. 2024 doi:10.1242/jeb.245432; Mendeley mww9m8r3dk.v1
  Crall et al. 2020 doi:10.1098/rsbl.2020.0103; original Stage37.

Important: 19,421 Goyal trajectories were selected successful landings, NOT
all approached flowers; cannot calculate P(landing | discovered flower).
Goyal's reported landing frequency per HOUR is different from landing
success probability. Original files do not provide matched wind x scent
ON/OFF x plant pollen-deposition outcomes. Never invent a meta-effect.

The bounded provenance audit records filenames, format, and hashes only.
It does not redistribute original dataset bytes or trajectories.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import sys
import urllib.request
import urllib.error
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

ZENODO_RECORD=60234
ZENODO_API=f'https://zenodo.org/api/records/{ZENODO_RECORD}'
ZENODO_FILE='ChangCrallCombes_WindAltersLandingDynamicsInBumblebeeData.zip'
ZENODO_MD5='22bbc8286fecd2535d3f284679aed87b'
MENDELEY_ID='mww9m8r3dk'
MENDELEY_URL='https://api.data.mendeley.com/datasets/mww9m8r3dk?version=1'
MAX_ZIP=10_000_000
MAX_UNCOMPRESSED=180_000_000

def _fetch(url,max_bytes=MAX_ZIP):
    url_parts=urlsplit(url)
    if url_parts.scheme!='https' or url_parts.hostname not in (
       'zenodo.org','api.data.mendeley.com'):
        raise ValueError('NO_GO_UNTRUSTED_PUBLIC_ARCHIVE_HOST')
    req=urllib.request.Request(url,headers={
        'User-Agent':'adaptive-gain-stage38-landing-source-audit/2026',
        'Accept':'application/json,application/octet-stream,application/zip,*/*'})
    with urllib.request.urlopen(req,timeout=28) as response:
        data=response.read(max_bytes+1)
    if len(data)>max_bytes:
        raise ValueError('NO_GO_LARGE_ORIGINAL_ARCHIVE')
    return data

def _zip_inventory(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError('NO_GO_ZENODO_NOT_A_VALID_ZIP')
    with zipfile.ZipFile(io.BytesIO(blob)) as f:
        items=[x for x in f.infolist() if not x.is_dir()]
        if len(items)>1000:
            raise ValueError('NO_GO_TOO_MANY_ORIGINAL_SOURCE_ENTRIES')
        if sum(x.file_size for x in items)>MAX_UNCOMPRESSED:
            raise ValueError('NO_GO_ZIP_BOMB_OR_LARGE_UNCOMPRESSED_SOURCE')
        entries=[]
        for x in items:
            if ('..' in Path(x.filename).parts or
                x.filename.startswith('/')):
                raise ValueError('NO_GO_UNSAFE_ZIP_ENTRY_PATH')
            suffix=Path(x.filename).suffix.lower()
            entries.append({'name':x.filename,'size':x.file_size,
                'type':suffix or '<no_extension>'})
    return {
      'file_count':len(entries),
      'uncompressed_total_bytes':sum(x['size'] for x in entries),
      'entries':entries,
      'raw_data_rows_disclosed':0,
      'no_flight_or_person_data_redistributed':True
    }

def inspect_zenodo(metadata,source):
    if not isinstance(metadata,dict) or metadata.get('id')!=ZENODO_RECORD:
        raise ValueError('NO_GO_ZENODO_WRONG_SOURCE_VERSION')
    meta=metadata.get('metadata') or {}
    title=(meta.get('title') or '').lower()
    if 'wind alters landing dynamics' not in title:
        raise ValueError('NO_GO_ORIGINAL_LANDING_TITLE_MISMATCH')
    creators=meta.get('creators') or []
    if not any('Chang' in (u.get('name') or '') for u in creators):
        raise ValueError('NO_GO_ORIGINAL_CHANG_AUTHOR_MISSING')
    sources=metadata.get('files') or []
    matches=[x for x in sources if x.get('key')==ZENODO_FILE]
    if len(matches)!=1:
        raise ValueError('NO_GO_MISSING_LANDING_ZIP_NAME')
    expected=matches[0]
    chk=expected.get('checksum') or ''
    if chk!='md5:'+ZENODO_MD5:
        raise ValueError('NO_GO_LANDING_ZENODO_ORIGINAL_CHECKSUM_METADATA')
    if hashlib.md5(source).hexdigest()!=ZENODO_MD5:
        raise ValueError('NO_GO_LANDING_ZENODO_ZIP_CHECKSUM')
    if expected.get('size')!=len(source):
        raise ValueError('NO_GO_LANDING_ZENODO_SIZE_MISMATCH')
    return {
      'status':'REAL_ORIGINAL_CHANG_LANDING_ARCHIVE_VERIFIED',
      'record_id':ZENODO_RECORD,
      'source_doi':'10.1242/jeb.137976',
      'file':ZENODO_FILE,
      'source_md5':ZENODO_MD5,
      'source_sha256':hashlib.sha256(source).hexdigest(),
      'zip_source_structure':_zip_inventory(source),
      'behavioral_endpoint':'conditioned landing trajectory biomechanics',
      'no_unrecorded_failed_approaches_or_attempt_denominators_claimed':True,
      'not_a_pollination_or_plant_fitness_estimate':True
    }

def read_mendeley_metadata(payload):
    if not isinstance(payload,dict):
        raise ValueError('NO_GO_NOT_MENDELEY_METADATA')
    version=payload.get('version')
    name=payload.get('name','')
    id_=str(payload.get('short_id') or payload.get('id') or '')
    doi=payload.get('doi')
    doi_id=doi.get('id','') if isinstance(doi,dict) else ''
    # Do not assert source identity if the endpoint changes schema.
    if version!=1 or not (MENDELEY_ID in (id_,doi_id) or MENDELEY_ID in doi_id):
        raise ValueError('NO_GO_UNVERIFIED_MENDELEY_DATASET_ID')
    if 'landing' not in name.lower() or 'bumblebee' not in name.lower():
        raise ValueError('NO_GO_UNRELATED_MENDELEY_TITLE')
    return {
      'status':'MENDELEY_PUBLIC_METADATA_CONFIRMED',
      'id':MENDELEY_ID,'version':version,'doi':doi_id,
      'name':name,
      'source_identity_verified_with_metadata':True,
      'landing_track_count_reported_by_source_authors':19421,
      'landing_tracks_not_all_attempted_landing_events':True,
      'bee_individual_ID_not_usable_according_to_published_method':True,
      'no_original_mat_trajectory_rows_extracted':True,
    }

def author_published_landing_rate_benchmark():
    """Published fixed-rate figures, NOT newly calculated from original MAT."""
    free0=280.8
    free3=112.2
    take0=56.0
    take3=16.5
    return {
      'status':'PUBLISHED_PAPER_RATE_BENCHMARK_NOT_RAW_DATA_REFIT',
      'source_paper':'Goyal et al 2024 doi:10.1242/jeb.245432',
      'source_dataset':'10.17632/mww9m8r3dk.1',
      'wind_speeds_m_s':[0.,3.4],
      'free_flight_landing_frequency_hourly_paper_means':[free0,free3],
      'free_flight_landing_frequency_hourly_paper_sem':[28.3,27.8],
      'free_flight_high_vs_calm_rate_ratio':free3/free0,
      'free_flight_drop_fraction':1-free3/free0,
      'post_takeoff_landing_frequency_hourly_paper_means':[take0,take3],
      'post_takeoff_landing_frequency_hourly_paper_sem':[7.8,7.7],
      'post_takeoff_high_vs_calm_rate_ratio':take3/take0,
      'post_takeoff_drop_fraction':1-take3/take0,
      'published_tracked_successful_landings':19421,
      'published_free_flight_tracks':16374,
      'published_post_takeoff_tracks':3047,
      'cannot_infer_landing_success_probability':True,
      'original_raw_session_variance_and_effort_not_reestimated':True,
      'not_original_raw_reanalysis':True
    }

def separate_noncombinable_stages():
    return {
       'status':'NO_GO_CROSS_SYSTEM_STAGE_MULTIPLICATION',
       'Stage37_focal':'male Euglossini visits to odor bait within natural wind 0.02-0.73 m/s, nine forest sites',
       'Stage38_focal':'Bombus terrestris hourly landing rate in controlled sidewind 0 versus 3.4 m/s',
       'other_source_2016':'Bombus impatiens headwind 0 vs 3.5m/s landing kinematics',
       'different_species_and_wind_regimes':True,
       'no_same_bee_or_plant_or_site_cohort':True,
       'Crall_bait_landings_unmeasured':True,
       'Goyal_scent_transport_unmeasured':True,
       'wind_direction_and_turbulence_differ':True,
       'no_source_matched_pollen_deposition':True,
       'do_not_multiply_source_effects_into_plant_fitness':True,
       'no_wind_by_floral_odor_interaction_estimated':True
    }

def run():
    result={
      'status':'ORIGINAL_LANDING_SOURCE_DIAGNOSTIC_COMPLETE_OR_NO_GO',
      'zenodo2016':None,'mendeley2024':None,
      'paper_2024_benchmark':author_published_landing_rate_benchmark(),
      'cross_source_identifiability':separate_noncombinable_stages(),
      'no_new_pollinator_data_collected':True
    }
    try:
        m=json.loads(_fetch(ZENODO_API,max_bytes=900_000).decode('utf8'))
        a=[x for x in m.get('files',[]) if x.get('key')==ZENODO_FILE]
        if len(a)!=1:
            raise ValueError('NO_GO_SOURCE_ZIP_LINK_UNAVAILABLE')
        link=(a[0].get('links') or {}).get('self')
        if not isinstance(link,str):
            raise ValueError('NO_GO_SOURCE_ZIP_DOWNLOAD_LINK_UNAVAILABLE')
        original=_fetch(link,max_bytes=MAX_ZIP)
        result['zenodo2016']=inspect_zenodo(m,original)
    except (ValueError,urllib.error.URLError,TimeoutError,OSError,
            zipfile.BadZipFile) as e:
        result['zenodo2016']={
          'status':'NO_GO_ZENODO_ORIGINAL_ARCHIVE_NOT_VERIFIED',
          'error_type':type(e).__name__,'error':str(e)[:240],
          'http_status':getattr(e,'code',None),
          'no_original_landing_data_claim':True}
    try:
        blob=_fetch(MENDELEY_URL,max_bytes=900_000)
        m=json.loads(blob.decode('utf8'))
        result['mendeley2024']=read_mendeley_metadata(m)
    except (ValueError,urllib.error.URLError,TimeoutError,OSError,
            json.JSONDecodeError) as e:
        result['mendeley2024']={
          'status':'NO_GO_MENDELEY_PUBLIC_API_OR_IDENTITY',
          'error_type':type(e).__name__,'error':str(e)[:240],
          'http_status':getattr(e,'code',None),
          'no_original_mat_contents_claim':True}
    return result

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='stage38_landing_source_receipts')
    args=ap.parse_args(argv)
    result=run()
    directory=Path(args.out);directory.mkdir(parents=True,exist_ok=True)
    (directory/'stage38_wind_landing_source_provenance.json').write_text(
      json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps({
        'zenodo':result['zenodo2016']['status'],
        'zenodo_inventory':result['zenodo2016'].get('zip_source_structure'),
        'mendeley':result['mendeley2024']['status'],
        'mendeley_error':result['mendeley2024'].get('error'),
        'published_free_flight_wind_rate_ratio':
            result['paper_2024_benchmark']['free_flight_high_vs_calm_rate_ratio'],
        'no_mat_biological_refit':True
    },ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
