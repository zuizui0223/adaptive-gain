"""Source-only original Harris2026 field archive; no biological effect estimates."""
from __future__ import annotations
import csv, hashlib, io, json, urllib.request, urllib.parse, zipfile
from collections import Counter
from pathlib import Path

DOI='10.5061/dryad.9kd51c608'
ORIGIN='https://datadryad.org'
REQUIRED=('forage.csv','nectar.csv','weather.csv','insect_surveys.csv','Harris_2026_FE_energetics.R','README.md')

def verify(data: bytes, digest: str, kind: str) -> str:
    name=kind.lower().replace('-','')
    if name not in ('sha256','md5'): raise ValueError('UNSUPPORTED_PROVIDER_DIGEST')
    actual=hashlib.new(name,data).hexdigest()
    if actual!=digest.lower(): raise ValueError('ORIGINAL_PROVIDER_DIGEST_MISMATCH')
    return actual

def decode(data):
    try: return data.decode('utf-8-sig')
    except UnicodeDecodeError: return data.decode('cp1252')

def csv_profile(data: bytes) -> dict:
    rows=list(csv.reader(io.StringIO(decode(data),newline='')))
    if not rows: raise ValueError('EMPTY_CSV')
    header=rows[0]
    if len(set(header))!=len(header): raise ValueError('DUPLICATE_COLUMN_NAME')
    records=[r for r in rows[1:] if r]
    if any(len(r)!=len(header) for r in records): raise ValueError('CSV_WIDTH_CHANGED')
    missing={h:sum(r[i].strip().lower() in ('','na','nan','null') for r in records) for i,h in enumerate(header)}
    survey=next((i for i,h in enumerate(header) if h.strip().lower()=='survey'),None)
    return {'rows':len(records),'columns':header,'missing':missing,
            'unique_surveys':len({r[survey] for r in records}) if survey is not None else None,
            'duplicate_complete_rows':sum(n-1 for n in Counter(tuple(r) for r in records).values()),
            'first_two_original_rows':records[:2]}

def select_member(z:zipfile.ZipFile,name:str)->str:
    found=[n for n in z.namelist() if n.rsplit('/',1)[-1]==name and '__MACOSX' not in n and not n.endswith('/')]
    if len(found)!=1: raise ValueError('NONUNIQUE_ARCHIVE_MEMBER:'+name)
    return found[0]

def get(url:str,limit:int=15_000_000)->bytes:
    req=urllib.request.Request(url,headers={'User-Agent':'adaptive-gain-scientific-source-audit/1.0','Accept':'application/json,application/zip,*/*'})
    with urllib.request.urlopen(req,timeout=60) as r:
        if r.status!=200: raise ValueError('SOURCE_HTTP_STATUS')
        b=r.read(limit+1)
    if len(b)>limit: raise ValueError('SOURCE_SIZE_LIMIT')
    return b

def link(obj,key):
    item=obj.get('_links',{}).get(key)
    if isinstance(item,list):
        if len(item)!=1: raise ValueError('AMBIGUOUS_API_LINK:'+key)
        item=item[0]
    if not isinstance(item,dict) or not item.get('href'): raise ValueError('MISSING_PROVIDER_LINK:'+key)
    return urllib.parse.urljoin(ORIGIN,item['href'])

def main(root:Path):
    root.mkdir(parents=True,exist_ok=True)
    report={'dataset_doi':DOI,'status':'SOURCE_PENDING','biological_outcome_fitted':False}
    out=root/'source_receipt.json'
    try:
        dataset=json.loads(get(ORIGIN+'/api/v2/datasets/doi:'+DOI))
        version_url=link(dataset,'stash:version')
        version=json.loads(get(version_url))
        files_url=link(version,'stash:files')
        files_doc=json.loads(get(files_url))
        files=files_doc.get('_embedded',{}).get('stash:files',[])
        report.update({'version_url':version_url,'version_id':version_url.rsplit('/',1)[-1],
                       'provider_files':[{k:f.get(k) for k in ('id','path','size','digest','digestType','_links')} for f in files]})
        out.write_text(json.dumps(report,indent=2))
        print('STAGE11_PROVIDER_METADATA '+json.dumps(report),flush=True)
        if not files: raise ValueError('EMPTY_PROVIDER_FILE_LIST')
        names={f['path'].rsplit('/',1)[-1]:f for f in files}
        if not set(REQUIRED).issubset(names): raise ValueError('MISSING_REQUIRED_ORIGINAL_FILES')
        raw=get(version_url+'/download')
        if not zipfile.is_zipfile(io.BytesIO(raw)): raise ValueError('VERSION_DOWNLOAD_NOT_ZIP')
        receipts={}
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            if z.testzip() is not None: raise ValueError('SOURCE_ZIP_CRC')
            for name in REQUIRED:
                member=select_member(z,name)
                content=z.read(member); meta=names[name]
                expected=meta.get('digest');kind=meta.get('digestType')
                if not expected or not kind: raise ValueError('NO_PROVIDER_CHECKSUM:'+name)
                verify(content,expected,kind)
                if meta.get('size') is not None and len(content)!=int(meta['size']): raise ValueError('SOURCE_FILE_SIZE_MISMATCH')
                (root/name).write_bytes(content)
                receipts[name]={'provider_digest':expected,'digest_type':kind,'bytes':len(content),
                                'sha256':hashlib.sha256(content).hexdigest()}
                if name.endswith('.csv'): receipts[name]['profile']=csv_profile(content)
                if name.endswith('.R') or name=='README.md': receipts[name]['source_text']=decode(content)
                print('STAGE11_ORIGINAL_FILE '+json.dumps({'name':name,**receipts[name]},ensure_ascii=False),flush=True)
        report.update(status='ORIGINAL_FILES_PROVIDER_VERIFIED_NO_MODEL',files=receipts)
    except Exception as e:
        report.update(status='NO_GO_ORIGINAL_SOURCE',error=type(e).__name__+': '+str(e))
        raise
    finally:
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False))
        print('STAGE11_SOURCE_STATUS '+json.dumps({k:v for k,v in report.items() if k not in ('files','provider_files')}),flush=True)
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',default='stage11_original')
    main(Path(p.parse_args().out))
