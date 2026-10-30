"""Stage13 independent original Smolla2016 social-cue landing data source gate.

No biological effect fit. No original per-bee rows committed to Git.
"""
from __future__ import annotations
import csv
import hashlib
import io
import zipfile
import json
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

DOI="10.5061/dryad.3jb68"
ORIGIN="https://datadryad.org"
EXPECTED={"beeLandings.csv","code_figures_statistics.r"}

def verify(data,digest,kind):
    canonical=kind.lower().replace("-","")
    if canonical not in {"sha256","md5"}:raise ValueError("NO_GO_UNKNOWN_ORIGINAL_DIGEST_TYPE")
    actual=hashlib.new(canonical,data).hexdigest()
    if actual!=digest.lower():raise ValueError("NO_GO_ORIGINAL_PROVIDER_DIGEST_MISMATCH")
    return actual

def fetch(url,limit=3_000_000):
    request=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-source-first-biological-audit/1.0",
        "Accept":"application/json,application/octet-stream,*/*"})
    with urllib.request.urlopen(request,timeout=60) as response:
        if response.status!=200:raise ValueError("NO_GO_ORIGINAL_SOURCE_HTTP")
        data=response.read(limit+1)
    if len(data)>limit:raise ValueError("NO_GO_ORIGINAL_SOURCE_SIZE")
    return data

def api_link(data,key):
    v=data.get("_links",{}).get(key)
    if isinstance(v,list):
        if len(v)!=1:raise ValueError("NO_GO_AMBIGUOUS_"+key)
        v=v[0]
    if not isinstance(v,dict) or not v.get("href"):
        raise ValueError("NO_GO_MISSING_PROVIDER_LINK_"+key)
    return urllib.parse.urljoin(ORIGIN,v["href"])

def select_member(z,name):
    found=[n for n in z.namelist() if n.split("/")[-1]==name
           and "__MACOSX" not in n and "/._" not in n and not n.endswith("/")]
    if len(found)!=1:raise ValueError("NO_GO_AMBIGUOUS_ORIGINAL_FILE "+name)
    return found[0]

def original_table_schema(raw):
    try:text=raw.decode("utf-8-sig")
    except UnicodeDecodeError:text=raw.decode("latin-1")
    reader=csv.DictReader(io.StringIO(text))
    columns=reader.fieldnames or []
    if not columns:raise ValueError("NO_GO_EMPTY_ORIGINAL_BEE_LANDINGS")
    if len(set(columns))!=len(columns):
        raise ValueError("NO_GO_REPEATED_CSV_COLUMN_NAMES")
    rows=list(reader)
    if any(None in r for r in rows):raise ValueError("NO_GO_SOURCE_CSV_WIDTH")
    if not rows:raise ValueError("NO_GO_NO_NATIVE_LANDING_ROWS")
    group=next((c for c in columns if c.strip().lower()=="group"),None)
    missing={c:sum(v.get(c) is None or str(v[c]).strip().lower() in
                       ("","na","nan","null") for v in rows) for c in columns}
    candidates=[c for c in columns if
          any(t in c.lower() for t in ("bee","id","land","cue","reward","sequence","time"))]
    identity=[c for c in columns if
          any(k==c.strip().lower() for k in
              ("bee","beeid","bee_id","individual","id","animalid","subject"))]
    report={"original_source_rows":len(rows),
            "native_columns":columns,
            "empty_cell_count_by_column":missing,
            "group_counts":dict(sorted(Counter(r.get(group) for r in rows).items())) if group else None,
            "columns_might_contain_sequence_or_exposure":candidates,
            "native_individual_id_candidate_counts":{
                c:len({r[c] for r in rows}) for c in identity},
            "first_values_FOR_FORMAT_ONLY":{
                c:[str(r.get(c,""))[:120] for r in rows[:2]] for c in candidates},
            "no_biological_hypothesis_scored":True}
    return report

def run(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    out=root/"smolla2016_original_source_receipt.json"
    report={"doi":DOI,"status":"NO_GO_SOURCE_UNVERIFIED","no_biological_effect_fit":True}
    try:
        doi=urllib.parse.quote("doi:"+DOI,safe="")
        dataset=json.loads(fetch(ORIGIN+"/api/v2/datasets/"+doi))
        version_url=api_link(dataset,"stash:version")
        version=json.loads(fetch(version_url))
        listing=json.loads(fetch(api_link(version,"stash:files")))
        files=listing.get("_embedded",{}).get("stash:files",[])
        names=[f.get("path","").split("/")[-1] for f in files]
        if len(set(names))!=len(names):
            raise ValueError("NO_GO_AMBIGUOUS_PROVIDER_FILENAME")
        if not EXPECTED.issubset(names):
            raise ValueError("NO_GO_MISSING_AUTHOR_ORIGINAL_BEE_LANDINGS")
        report.update({"provider_version":version_url.rsplit("/",1)[-1],
                       "provider_files_available":names})
        # Old Dryad versions may reject public individual-file API links
        # with 401 although the complete original published version ZIP
        # remains publicly downloadable. Use only the provider's version
        # download, then hash every selected member against file metadata.
        full_zip=fetch(version_url+"/download",limit=20_000_000)
        if not zipfile.is_zipfile(io.BytesIO(full_zip)):
            raise ValueError("NO_GO_ORIGINAL_PROVIDER_VERSION_NOT_ZIP")
        source_rows={}
        with zipfile.ZipFile(io.BytesIO(full_zip)) as z:
            if z.testzip() is not None:
                raise ValueError("NO_GO_ORIGINAL_VERSION_ZIP_CRC")
            for f in files:
                name=f.get("path","").split("/")[-1]
                if name not in EXPECTED:continue
                raw=z.read(select_member(z,name))
                expected=f.get("digest");kind=f.get("digestType")
                if not expected or not kind:raise ValueError("NO_GO_PROVIDER_CHECKSUM_MISSING")
                verify(raw,expected,kind)
                # Ephemeral original data are available to the source QA job;
                # Git/CI artifacts retain ONLY metadata and derived checks.
                (root/name).write_bytes(raw)
                if f.get("size") is not None and len(raw)!=int(f["size"]):
                    raise ValueError("NO_GO_ORIGINAL_FILE_BYTES_CHANGED")
                receipt={"name":name,"bytes":len(raw),
                         "provider_digest":expected,"digest_type":kind,
                         "actual_sha256":hashlib.sha256(raw).hexdigest()}
                if name=="beeLandings.csv":
                    receipt["source_schema"]=original_table_schema(raw)
                else:
                    try:code=raw.decode("utf-8-sig")
                    except UnicodeDecodeError:code=raw.decode("latin-1")
                    receipt["original_R_script_headings"]=[s.strip()[:160] for s in code.splitlines()
                        if ("read.csv" in s or "subset(" in s or "firstLanding" in s or
                            "Landed" in s or "dummy_last" in s)][:35]
                source_rows[name]=receipt
        report.update({"status":"SOURCE_VERIFIED_NATIVE_SMOLLA2016_SCHEMAS",
                       "author_original_sources":source_rows})
    except Exception as e:
        report.update({"status":"NO_GO_ORIGINAL_SOURCE_GRANULARITY",
                       "reason":type(e).__name__+": "+str(e)})
        raise
    finally:
        out.write_text(json.dumps(report,indent=2,ensure_ascii=False))
        preview={"doi":DOI,"status":report["status"],
            "provider_version":report.get("provider_version"),
            "sources":report.get("author_original_sources"),
            "reason":report.get("reason")}
        print("STAGE13_ORIGINAL_SOCIAL_SOURCE "+json.dumps(preview,ensure_ascii=False),flush=True)
    return report

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--out",default="stage13_original")
    run(p.parse_args().out)
