"""Stage53: official RBG Kew WCVP original bulk zip source metadata audit.

WCVP contains accepted plant names, synonyms and WGSRPD L3 native/
introduced botanical-country records (NOT political ISO countries).
Source: Royal Botanic Gardens Kew, official WCVP archive, read only at CI
runtime, original raw zip is neither rehosted nor committed.

This PROBE tests whether the true original source is accessible and
which columns and zip members are supplied. It does NOT infer native
range or species richness until schema and source identity verified.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

URL="https://sftp.kew.org/pub/data-repositories/WCVP/wcvp.zip"
MAX_BYTES=155_000_000


def audit():
    data={"status":"OFFICIAL_KEW_WCVP_SOURCE_META_PROBE",
          "source":URL,
          "original_bulk_source_not_persisted":True,
          "taxon_or_native_distribution_not_yet_verified":True,
          "original_archive_info":None}
    with tempfile.TemporaryDirectory() as temp:
        file=Path(temp)/"wcvp_original.zip"
        req=urllib.request.Request(URL,headers={
            "User-Agent":"adaptive-gain-native-floral-stage53-bulk-source-audit/2026",
            "Accept":"application/zip,*/*"})
        checksum=hashlib.sha256()
        total=0
        with urllib.request.urlopen(req,timeout=90) as resp, file.open("wb") as out:
            response_type=resp.headers.get("Content-Type","")
            while True:
                piece=resp.read(2*1024*1024)
                if not piece:break
                total+=len(piece)
                if total>MAX_BYTES:
                    raise ValueError("NO_GO_OFFICIAL_WCVP_SOURCE_TOO_BIG")
                checksum.update(piece)
                out.write(piece)
        if not zipfile.is_zipfile(file):
            raise ValueError("NO_GO_OFFICIAL_WCVP_SOURCE_NOT_ZIP")
        with zipfile.ZipFile(file) as z:
            members=[{"name":x.filename,"uncompressed_bytes":x.file_size}
                     for x in z.infolist() if not x.is_dir()]
            table_sources={}
            for target in ("wcvp_names.csv","wcvp_distribution.csv"):
                match=[x.filename for x in z.infolist()
                       if Path(x.filename).name.lower()==target.lower()]
                if len(match)!=1:
                    raise ValueError("NO_GO_WCVP_ORIGINAL_REQUIRED_TABLE_"+target)
                with z.open(match[0]) as fp:
                    text=io.TextIOWrapper(fp,encoding="utf-8-sig",newline="")
                    first=next(csv.reader(text,delimiter="|"))
                    # Peek one row for type/schema only, not biological data.
                    second=next(csv.reader(text,delimiter="|"))
                table_sources[target]={
                    "member":match[0],"header":first,
                    "n_columns":len(first),"first_row_field_lengths":[len(x) for x in second],
                    "first_row_field_nonempty":[bool(x) for x in second],
                    "zip_member_uncompressed_bytes":next(x.file_size for x in z.infolist()
                                                          if x.filename==match[0])}
        data["original_archive_info"]={
          "original_kew_zip_sha256":checksum.hexdigest(),
          "original_zip_bytes":total,
          "server_content_type":response_type,
          "member_manifest":members,
          "original_tables":table_sources
        }
    return data


def main():
    try:
        report=audit()
    except (ValueError,urllib.error.URLError,urllib.error.HTTPError,
            TimeoutError,zipfile.BadZipFile,StopIteration) as e:
        report={"status":"OFFICIAL_KEW_BULK_SOURCE_NOT_ACCESSIBLE_NO_NATIVE_CLAIM",
                "source":URL,"error_kind":type(e).__name__,
                "error_detail":str(e)[:220],
                "taxon_or_native_distribution_not_yet_verified":True}
    d=Path("stage53_kew_source_probe")
    d.mkdir(exist_ok=True)
    (d/"original_kew_WCVP_zip_schema_receipt.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",
        encoding="utf8")
    print("STAGE53_KEW_ORIGINAL_WCVP_SOURCE_SCHEMA",json.dumps(report,ensure_ascii=False))
    if report["status"]!="OFFICIAL_KEW_WCVP_SOURCE_META_PROBE":
        raise SystemExit("KEW_ORIGINAL_SOURCE_UNAVAILABLE_NOT_A_NEGATIVE_NATIVE_RESULT")


if __name__=="__main__":
    main()
