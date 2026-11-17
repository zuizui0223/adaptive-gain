"""Stage74: original same-island Kent flower spectra and observed insect visitors.

Only public author-linked Dryad streams, separately validated against official
Dryad version-file SHA256. This is not use of authenticated/private endpoints.
Dryad API v2 file downloads returned HTTP 401 in Stage73; a webpage has
actual public links with different stream IDs. Never guess other stream IDs.

Jones et al. 2025 (Biology Letters): DOI 10.1098/rsbl.2025.0044
Data DOI 10.5061/dryad.9p8cz8wtm, 2019/2022/2023 Kent Island records.
Source reports 90 measured flowers; 74 visited, 3718 observations, 145 visitor
types. These counts are PUBLISHED, not verified until raw bytes are obtained.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import html
import io
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_original_field_stage73"))
from resolve_original_Dryad_versions_files import list_versions, list_file_metadata

HOST="https://datadryad.org"
DOI="10.5061/dryad.9p8cz8wtm"
PUB="10.1098/rsbl.2025.0044"
UA="adaptive-gain-original-author-public-Dryad-stage74/2026-11-17"
FILES={
    "Floral_Reflectance_Kent_Island_Plants.csv":4074180,
    "2019_2023_Kent_Island_Plant_Pollinator_Network.csv":4074184,
}
PUBLISHED={
    "spectral_plant_species":90,
    "visited_plant_species":74,
    "individual_visitor_observations":3718,
    "visitor_identification_types":145,
}
MAX_RAW=1200000
STREAM_RE=re.compile(r"^/downloads/file_stream/([0-9]+)(?:[/?#].*)?$")

def fetch(url,cap=MAX_RAW):
    if not url.startswith(HOST+"/"):
        raise ValueError("STAGE74_ONLY_OFFICIAL_PUBLIC_DRYAD_WEB_URL")
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=55) as r:
        raw=r.read(cap+1)
        final=r.geturl()
        content_type=r.headers.get("Content-Type","")
    if len(raw)>cap:raise ValueError("STAGE74_DOWNLOADED_FILE_OVER_BUDGET")
    return raw,final,content_type

def failed(e):
    code=getattr(e,"code",None)
    return {"status":"ORIGINAL_PUBLIC_BYTES_UNAVAILABLE",
            "error_type":type(e).__name__,
            "http_code":code,
            "NOT_biological_absence":True}

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out=[]
        self.current=None
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            d=dict(attrs)
            self.current={"href":html.unescape(d.get("href","")),
                          "title":d.get("title",""),"text":""}
    def handle_data(self,txt):
        if self.current is not None:self.current["text"]+=txt
    def handle_endtag(self,tag):
        if tag=="a" and self.current is not None:
            self.out.append(self.current)
            self.current=None

def author_page_links(raw):
    parser=LinkParser()
    parser.feed(raw.decode("utf-8",errors="replace"))
    matching=[]
    for a in parser.out:
        href=a["href"]
        if href.startswith(HOST+"/"):href=href[len(HOST):]
        m=STREAM_RE.fullmatch(href)
        if not m:continue
        matching.append({"stream_id":int(m.group(1)),"href":href,
                         "original_anchor_text":a["text"].strip(),
                         "original_anchor_title":a["title"]})
    return matching

def author_metadata():
    versions,meta=list_versions(DOI)
    if not versions:
        raise ValueError("STAGE74_ORIGINAL_PUBLIC_DRYAD_HAS_NO_VERSIONS")
    records,receipt=list_file_metadata(versions[-1])
    metadata={str(row["path"]).rsplit("/",1)[-1]:row for row in records}
    return metadata,{"version_ids":versions,"version":versions[-1],
                     "list_record":receipt,"version_records":meta}

def is_actual_utf8_csv(raw):
    try:
        string=raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return False
    if string.lstrip().lower().startswith(("<!doctype","<html")):
        return False
    return len(string.splitlines())>=2 and "," in string.splitlines()[0]

def verify_original(raw,meta):
    digest=hashlib.sha256(raw).hexdigest()
    official=str(meta.get("digest") or "")
    if len(official)!=64:
        return False,{"source_sha256":digest,"source_official_digest":official,
                     "status":"OFFICIAL_FILE_SHA256_NOT_DECLARED"}
    if digest!=official:
        return False,{"source_sha256":digest,"source_official_digest":official,
                     "status":"ORIGINAL_FILE_SHA256_MISMATCH"}
    if not is_actual_utf8_csv(raw):
        return False,{"source_sha256":digest,"source_official_digest":official,
                     "status":"AUTHOR_HASH_VALID_BUT_NOT_UTF8_CSV"}
    return True,{"source_sha256":digest,"source_official_digest":official,
                 "status":"ORIGINAL_AUTHOR_SHA256_AND_CSV_VERIFIED"}

def read_csv_bytes(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline="")))

def audit_join(raw_spectra,raw_visits):
    spectra=read_csv_bytes(raw_spectra)
    visits=read_csv_bytes(raw_visits)
    if not spectra or not visits:raise ValueError("STAGE74_AUTHENTIC_CSV_EMPTY")
    scols=list(spectra[0])
    vcols=list(visits[0])
    source_plant_col=next((k for k in vcols if k.strip().casefold()=="plant"),None)
    if not source_plant_col:
        raise ValueError("STAGE74_SOURCE_NO_ORIGINAL_PLANT_COLUMN")
    plant_names={v[source_plant_col].strip().casefold() for v in visits
                 if v[source_plant_col] and v[source_plant_col].strip()}
    # Per source README first spectral column is wavelength and remaining
    # columns include flower species AND original lab-paper stimuli.
    # Exclude only names without genus-species binomial: no invented synonyms.
    candidate_spectral_names={
        n.strip().casefold() for n in scols[1:]
        if len(n.strip().split())>=2 and all(x.isalpha() or "-" in x for x in n.strip().split()[:2])
    }
    share=plant_names & candidate_spectral_names
    years=Counter(v.get("Year","UNKNOWN") for v in visits)
    guilds=Counter(v.get("Taxonomic_Group","UNKNOWN") for v in visits)
    return {
      "original_visitation_rows":len(visits),
      "original_visit_csv_columns":vcols,
      "original_spectral_wavelength_rows":len(spectra),
      "original_spectra_csv_columns_first15":scols[:15],
      "original_nonwavelength_spectral_columns":len(scols)-1,
      "strict_source_plant_names_in_visit_csv":len(plant_names),
      "strict_source_candidate_binomial_spectral_columns":len(candidate_spectral_names),
      "strict_literal_plant_overlap":len(share),
      "original_date_year_count":dict(years),
      "original_author_taxonomic_visitor_categories":dict(guilds),
      "original_measured_spectral_plant_and_field_visitor_same_island":True,
      "original_no_visitor_record_not_verified_absence":True,
      "strict_binomial_no_taxonomic_synonym_inferred":True,
      "spectra_2019_field_visits_temporally_identical":False,
      "published_source_90_74_3718_145_is_not_automatically_recomputed":True,
    }

def run(outdir):
    metadata,inventory=author_metadata()
    report={"schema":"stage74_original_Kent_Jones2025_public_Dryad_site_spectra_network",
            "original_dataset_DOI":DOI,"article_DOI":PUB,
            "actual_author_version_file_inventory":inventory,
            "published_paper_reference_counts_NOT_raw_verified":PUBLISHED,
            "original_Author_file_metadata":{
                name:{k:v for k,v in row.items() if k in
                      ("file_id","path","size","digest","digest_type")}
                for name,row in metadata.items()},
            "author_public_dataset_page_status":"NOT_DOWNLOADED",
            "file_receipts":[]}
    url=HOST+"/dataset/doi%3A"+urllib.parse.quote(DOI,safe="")
    try:
        html_data,final,mime=fetch(url,2500000)
        report["author_public_dataset_page_status"]="FETCHED"
        report["author_public_dataset_page_sha256"]=hashlib.sha256(html_data).hexdigest()
        links=author_page_links(html_data)
        report["actual_author_webpage_file_stream_links"]=links[:40]
    except Exception as e:
        report["author_public_dataset_page_error"]=failed(e)
        links=[]
    # Exact literal stream IDs surfaced through source WEB page by web
    # retrieval. They are NOT Dryad API version file IDs. Validate both
    # requested named files against the independent original API SHA.
    source_files={}
    for name,stream_id in FILES.items():
        meta=metadata.get(name)
        if meta is None:
            report["file_receipts"].append({"filename":name,"status":"ORIGINAL_VERSION_FILE_NOT_FOUND"})
            continue
        explicit=[a for a in links if a["stream_id"]==stream_id and name.lower() in
                  (a["original_anchor_text"]+" "+a["original_anchor_title"]).lower()]
        uri=HOST+"/downloads/file_stream/"+str(stream_id)
        try:
            raw,final,mime=fetch(uri)
            good,record=verify_original(raw,meta)
            status="REAL_ORIGINAL_PUBLIC_STREAM_ADMITTED" if good else record["status"]
            report["file_receipts"].append({
              "filename":name,"source_public_stream_id":stream_id,
              "source_public_page_link_exact":bool(explicit),
              "source_official_v2_file_id":meta.get("file_id"),
              "original_author_version":inventory["version"],
              "downloaded_bytes":len(raw),"content_type":mime,
              "status":status,**record})
            if good:
                source_files[name]=raw
        except Exception as e:
            report["file_receipts"].append({
             "filename":name,"source_public_stream_id":stream_id,
             "source_public_page_link_exact":bool(explicit),
             "source_official_v2_file_id":meta.get("file_id"),**failed(e)})
    if len(source_files)==2:
        report["source_both_real_spectra_and_visitors_admitted"]=True
        report["source_real_join_result"]=audit_join(
             source_files["Floral_Reflectance_Kent_Island_Plants.csv"],
             source_files["2019_2023_Kent_Island_Plant_Pollinator_Network.csv"])
    else:
        report["source_both_real_spectra_and_visitors_admitted"]=False
        report["source_real_join_result"]=None
    report.update({
      "independent_geographic_study_systems_this_source":1,
      "field_spectra_are_from_same_individuals_as_2019_visits":False,
      "published_2025_original_analysis_precedes_our_comparison":True,
      "new_confirmatory_UV_guild_effect_estimated":False,
      "photo_derived_flower_traits":False,
      "private_authentication_bypassed":False,
    })
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"kent_2025_original_author_web_stream_and_SHA_join_receipt.json").write_text(
        json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE74_SOURCE_KENT_ISLAND_FIELD_SPECTRA_VISITS_AUDIT",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("SOURCE_REAL_CSV_SHA_GATE_OR_ACCESS_FAILURE_NOT_SOURCE_ABSENCE")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",required=True,type=Path)
    args=p.parse_args()
    run(args.outdir)
if __name__=="__main__":
    main()
