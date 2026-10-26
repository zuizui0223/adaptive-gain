"""Read-only UK PoMS 2017-2023 FIT Count package/schema audit.

This script does not estimate cue routeability. Its main job is to prevent
treating a targeted 10-minute flower survey as a whole-community choice record.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import time
import urllib.request
import zipfile

DATASET_DOI = '10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618'
DATA_URL = 'https://data-package.ceh.ac.uk/data/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip'
SUPPORT_URL = 'https://data-package.ceh.ac.uk/sd/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip'
MAX_COMPRESSED = 180 * 1024 * 1024
MAX_UNCOMPRESSED = 1_000 * 1024 * 1024

def download_verified(url, dest, max_bytes=MAX_COMPRESSED):
    """Read-and-hash bytes; never silently accept a human-readable error page."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        if not zipfile.is_zipfile(dest):
            raise ValueError('cached path is not a ZIP archive')
    else:
        last = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'adaptive-gain-poms-independent-macro-audit/1.0',
                    'Accept': 'application/zip,application/octet-stream,*/*'})
                with urllib.request.urlopen(req, timeout=120) as response, dest.open('wb') as out:
                    n = 0
                    while True:
                        part = response.read(1024 * 1024)
                        if not part: break
                        n += len(part)
                        if n > max_bytes: raise ValueError('archive exceeds download cap')
                        out.write(part)
                if not zipfile.is_zipfile(dest): raise ValueError('download not a valid ZIP')
                last = None
                break
            except Exception as ex:
                last = ex
                dest.unlink(missing_ok=True)
                time.sleep(3*(attempt+1))
        if last:
            raise RuntimeError(f'official archive retrieval failed after 3 attempts: {last}') from last
    h = hashlib.sha256()
    with dest.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''):h.update(b)
    return {'url':url, 'name':dest.name, 'bytes':dest.stat().st_size, 'sha256':h.hexdigest()}

def audit_archive(zip_path, *, max_uncompressed=MAX_UNCOMPRESSED):
    """Inventory original files without expanding paths onto the filesystem."""
    entries = []
    with zipfile.ZipFile(zip_path) as z:
        infos=z.infolist()
        total_size=sum(x.file_size for x in infos)
        if total_size > max_uncompressed:
            raise ValueError(f'archive expansion cap violated: {total_size}')
        for info in infos:
            member_hash = hashlib.sha256()
            if not info.is_dir():
                with z.open(info) as stream:
                    for piece in iter(lambda: stream.read(1024*1024), b''):
                        member_hash.update(piece)
            entries.append({'file':info.filename, 'bytes':info.file_size,
                            'sha256_uncompressed_member':member_hash.hexdigest(),
                            'compressed_bytes':info.compress_size,
                            'extension':Path(info.filename).suffix.lower(),
                            'crc32':f'{info.CRC:08x}'})
    return {'members':entries,'member_count':len(entries),'total_uncompressed_bytes':total_size}

def field_roles(columns):
    rules={
        'date':r'date|day|month|year',
        'target_flower':r'flower|plant|species|target|species_code',
        'observed_insect_group':r'insect|pollinator|visitor|bee|fly|wasp|beetle|butterfly|hover',
        'observation_effort':r'duration|minute|time|effort|seconds|survey',
        'location':r'site|square|latitude|longitude|grid|northing|easting|location',
        'flowering_quantity':r'flower_count|flowers|number.*flower|floral|abundance',
        'counts':r'count|abundance|frequency|visit|total|number',
        'weather':r'wind|rain|temperature|sun|cloud|weather',
        'record_key':r'^id$|_id$|unique|record|fit.?count'
    }
    return {r:[c for c in columns if re.search(p,c.lower().replace(' ','_'))] for r,p in rules.items()}

def inventory_csv(zip_path, member, sample_rows=300):
    import pandas as pd
    try:
        with zipfile.ZipFile(zip_path) as z:
            with z.open(member) as fh:
                # Read a small sample to enumerate columns; the full file is
                # inventoried in a later stage with explicit schema/keys.
                raw=fh.read(512*1024)
        encoding='utf-8'
        try:raw.decode(encoding)
        except UnicodeDecodeError:encoding='latin-1'
        text=raw.decode(encoding)
        reader=csv.reader(io.StringIO(text))
        header=next(reader)
        examples=[]
        for _,row in zip(range(sample_rows),reader):
            if len(row)==len(header): examples.append(row)
        df=pd.DataFrame(examples,columns=header)
        return {'filename':member,'encoding_sample':encoding,'columns':header,
                'sample_rows':len(df),
                'sample_null_or_empty_by_column':{c:int(df[c].isna().sum()+(df[c].astype(str).str.strip()=='').sum()) for c in header},
                'numeric_column_candidates':[
                    c for c in header if pd.to_numeric(df[c].replace('',pd.NA),errors='coerce').notna().mean()>.8
                ],'field_roles':field_roles(header)}
    except Exception as e:
        return {'filename':member,'read_error':str(e)}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='stage3_poms_audit')
    p.add_argument('--download-support',action='store_true')
    args=p.parse_args(argv)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    audit={'doi':DATASET_DOI,'source':'UK Pollinator Monitoring Scheme (2026), NERC EDS EIDC',
           'license':'Open Government Licence; original provider acknowledgement required',
           'interpretation':'FIT target-flower 10-min censuses, NOT simultaneous alternative-plant choice records'}
    data=out/'poms_fit_2017_2023_source.zip'
    audit['data_download']=download_verified(DATA_URL,data)
    inv=audit_archive(data)
    audit['archive']=inv
    all_csv=[]
    for x in inv['members']:
        if x['extension']=='.csv':
            all_csv.append(inventory_csv(data,x['file']))
    audit['csv_schema_audit']=all_csv
    if args.download_support:
        support=out/'poms_support.zip'
        try:
            audit['support_download']=download_verified(SUPPORT_URL,support)
            audit['support_inventory']=audit_archive(support)
        except Exception as exc:
            audit['support_error']=str(exc)
    (out/'source_schema_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False))
    # The short textual marker makes CI logs useful without publishing raw data.
    print('POMS_SOURCE_RECEIPT '+json.dumps(audit['data_download']),flush=True)
    print('POMS_ARCHIVE_INVENTORY '+json.dumps(inv),flush=True)
    for x in all_csv:print('POMS_SCHEMA '+json.dumps(x,ensure_ascii=False),flush=True)
    print('POMS_SCHEMA_AUDIT_COMPLETE',flush=True)
    if not all_csv:raise ValueError('no original CSV source data: fail closed')
    return audit

if __name__=='__main__':main()
