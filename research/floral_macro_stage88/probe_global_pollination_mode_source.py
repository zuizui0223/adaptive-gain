"""Stage88A: audit original 2025 global 179,263 species pollination-mode data.

Original independent Wang, Luo et al. New Phytologist (2025), Dryad
10.5061/dryad.73n5tb35w, archived dataset 2.72MB .Rdata and README.
Author reports 194,476 species with inflorescence types and 179,263
with animal/wind pollination-mode labels (not user dataset overlap).
This code verifies original API, version and file identity and downloads
original, never synthesizes anemophily for unreported NHM taxa.
"""
from __future__ import annotations
import argparse,hashlib,json,urllib.request,urllib.parse
from pathlib import Path

DOI="10.5061/dryad.73n5tb35w"
BASE="https://datadryad.org/api/v2"
CANON=BASE+"/datasets/doi%3A"+urllib.parse.quote(DOI,safe="")
EXPECTED_FILE="Combine_data_uploaded_Final_20250411.Rdata"
LIMIT=8_000_000

def http(url,limit=LIMIT):
    p=urllib.parse.urlparse(url)
    if p.scheme!="https" or p.hostname not in ("datadryad.org","www.datadryad.org"):
        raise ValueError("STAGE88_API_FOREIGN_HOST_BLOCKED_"+p.hostname.__str__())
    req=urllib.request.Request(url,headers={"Accept":"application/json",
        "User-Agent":"floral-macro-source-reproducibility-audit/1.0"})
    with urllib.request.urlopen(req,timeout=95) as r:
        data=r.read(limit+1)
        if len(data)>limit:raise ValueError("STAGE88_DRYAD_METADATA_TOO_LARGE")
        return data,r.status,r.geturl()

def link_path(obj, key):
    raw=obj.get("_links",{}).get(key,{})
    if isinstance(raw,list):raw=raw[0] if raw else {}
    if isinstance(raw,dict):
        return raw.get("href","")
    return ""

def resolve(relative):
    return urllib.parse.urljoin("https://datadryad.org",relative)

def run():
    data,status,_=http(CANON)
    if status!=200:raise ValueError("STAGE88_REAL_GLOBAL_MODE_ORIGINAL_DATASET_HTTP")
    d=json.loads(data)
    if DOI not in json.dumps(d) or "inflorescence" not in json.dumps(d).casefold():
        raise ValueError("STAGE88_DRYAD_DOI_NOT_REQUIRED_GLOBAL_DATASET")
    versionurl=link_path(d,"stash:version") or link_path(d,"version")
    verslist=link_path(d,"stash:versions")
    versions=[]
    if versionurl:
        b,_,_=http(resolve(versionurl));versions=[json.loads(b)]
    elif verslist:
        b,_,_=http(resolve(verslist));raw=json.loads(b)
        versions=raw.get("_embedded",{}).get("stash:versions",[])
    vid=0
    if versions:
        vd=versions[0]
        vid=vd.get("id") or vd.get("versionId") or vd.get("version")
    if not vid:
        vid=d.get("versionId") or d.get("currentVersion",{}).get("id")
    if not vid and versionurl:
        import re
        m=re.search(r"/versions/(\d+)(?:[/?#]|$)",versionurl)
        if m:vid=int(m.group(1))
    if not vid:
        print("STAGE88_DRYAD_API_METADATA_SHAPE",json.dumps({
            "root_keys":sorted(d),
            "embedded_links":d.get("_links",{}),
            "version_url_resolved":versionurl,
            "version_object_sample":versions[:1],
            "known_version_ID_candidates":{k:d.get(k) for k in ("versionId","version","currentVersion","versionNumber")}},
             ensure_ascii=False,default=str),flush=True)
        raise ValueError("STAGE88_DRYAD_ORIGINAL_VERSION_ID_UNAVAILABLE")
    file_data,_,_=http(f"{BASE}/versions/{int(vid)}/files")
    files=json.loads(file_data)
    if isinstance(files,dict):
        candidates=files.get("_embedded",{}).get("stash:files",[]) or files.get("_embedded",{}).get("files",[]) or files.get("files",[])
    elif isinstance(files,list):candidates=files
    else:candidates=[]
    if not candidates:raise ValueError("STAGE88_REAL_AUTHOR_FILE_LIST_EMPTY")
    file_info=[]
    for f in candidates:
        link=link_path(f,"stash:download") or link_path(f,"download") or link_path(f,"self")
        file_info.append({"id":f.get("id"),"path":f.get("path") or f.get("name") or f.get("filename"),
            "size":f.get("size"),"digest":f.get("digest") or f.get("checksum"),
            "link":link})
    keys=json.dumps(file_info)
    if EXPECTED_FILE not in keys:
        raise ValueError("STAGE88_REAL_AUTHOR_RDATA_FILE_NOT_IN_RELEASE")
    return {"schema":"stage88_original_Dryad_global_pollination_mode_database_probe",
       "author_DOI":DOI,"original_Dryad_API":CANON,
       "source_metadata_sha256":hashlib.sha256(data).hexdigest(),
       "original_version_id":int(vid),"original_files":file_info,
       "author_paper_global_pollination_mode_species_declared":179263,
       "author_paper_global_inflorescence_species_declared":194476,
       "source_author_taxon_coverage_not_still_our_WCVP_overlap":True,
       "source_not_assumed_independently_wild_pollinator_observed_mode":True,
       "we_will_not_classify_unknown_source_pollination_as_wind":True}

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True,type=Path)
    z=p.parse_args();d=run();z.out.parent.mkdir(exist_ok=True,parents=True)
    z.out.write_text(json.dumps(d,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE88A_REAL_WANG2025_DRYAD_POLLINATION_MODE",json.dumps(d,sort_keys=True))
if __name__=="__main__":main()
