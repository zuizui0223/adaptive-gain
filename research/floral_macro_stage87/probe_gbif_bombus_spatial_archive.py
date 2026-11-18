"""Probe archived original multi-million GBIF Bombus download for spatial use.

Target: GBIF DOI 10.15468/dl.jbewdc, original occurrence download ID
0003256-260226173443078. Publication notes 3,958,417 records 1950–2025
in Asia/Europe/North America, 1,964 constituent data sets. This is not a
current 2026 snapshot, but it is citable, source-frozen and re-usable.
No observed Bombus record is interpreted as a biologically absent bee.
"""
from __future__ import annotations
import argparse,json,urllib.request,urllib.parse
from pathlib import Path

KEY="0003256-260226173443078"
DOI="10.15468/dl.jbewdc"
URL="https://api.gbif.org/v1/occurrence/download/"+KEY
ALLOWED={"api.gbif.org","download.gbif.org","downloads.gbif.org",
         "occurrence-downloads.gbif.org","gbif.org","www.gbif.org"}

def source_info():
    request=urllib.request.Request(URL,headers={"Accept":"application/json",
      "User-Agent":"source-archived-2026-global-bumblebee-floral-macro"})
    with urllib.request.urlopen(request,timeout=75) as resp:
        b=resp.read(1000000)
    j=json.loads(b)
    status=str(j.get("status") or "")
    if status.upper()!="SUCCEEDED":
        raise ValueError("STAGE87_ORIGINAL_BOMBUS_DOWNLOAD_NOT_SUCCEEDED_"+status)
    rawlink=j.get("downloadLink") or ""
    u=urllib.parse.urlparse(rawlink)
    if u.scheme!="https" or u.hostname not in ALLOWED:
        raise ValueError("STAGE87_GBIF_DOWNLOAD_LINK_HOST_UNKNOWN")
    return {"schema":"stage87B_archive_GBIF_original_Bombus_download_metadata",
      "download_key":KEY,"download_doi_expected":DOI,
      "download_status":status,
      "download_format":j.get("format"),
      "archive_record_count":j.get("totalRecords"),
      "declared_download_link":rawlink,
      "archive_source_request_created":j.get("created"),
      "archive_source_request_completed":j.get("finished"),
      "original_source_2025_max_year":2025,
      "original_source_region_scope":"Asia Europe North America",
      "original_database_no_species_absence_inferred":True,
      "gbif_occurrence_sampling_effort_is_geographically_biased":True}

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",type=Path,required=True)
    x=p.parse_args();r=source_info();x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n")
    print("STAGE87_BOMBUS_GLOBAL_ARCHIVE_METADATA",json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
