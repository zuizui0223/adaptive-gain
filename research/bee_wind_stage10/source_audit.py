"""Stage10 genuine original Zenodo trajectory source manifest; NO biological endpoint."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import re
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
import zipfile

RECORD="60234"
FILENAME="ChangCrallCombes_WindAltersLandingDynamicsInBumblebeeData.zip"
EXPECTED_MD5="22bbc8286fecd2535d3f284679aed87b"
URLS=(
    "https://zenodo.org/records/60234/files/"+FILENAME+"?download=1",
    "https://zenodo.org/api/records/60234/files/"+FILENAME+"/content",
)
MAX_COMPRESSED_BYTES=40_000_000
MAX_MEMBER_BYTES=200_000_000

def safe_manifest(data:bytes):
    if not zipfile.is_zipfile(io.BytesIO(data)):
        raise ValueError("NO_GO_ZENODO_ORIGINAL_NOT_ZIP")
    manifest=[]
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        bad=z.testzip()
        if bad is not None:
            raise ValueError("NO_GO_ZIP_CRC_"+str(bad))
        for m in z.infolist():
            parts=PurePosixPath(m.filename).parts
            if not parts or any(x in ("..","") for x in parts) or m.filename.startswith(("/", "\\")):
                raise ValueError("NO_GO_UNSAFE_ARCHIVE_MEMBER")
            if m.file_size>MAX_MEMBER_BYTES:
                raise ValueError("NO_GO_ABNORMAL_ARCHIVE_MEMBER_SIZE")
            row={"name":m.filename,"compressed_bytes":m.compress_size,
                 "original_bytes":m.file_size,
                 "is_dir":m.is_dir(),
                 "extension":PurePosixPath(m.filename).suffix.lower()}
            if not m.is_dir():
                with z.open(m) as member:
                    prefix=member.read(min(512,m.file_size))
                row["prefix_type"]=("MATLAB5" if prefix[:6]==b"MATLAB" else
                                    "HDF5" if prefix[:8]==b"\\x89HDF\\r\\n\\x1a\\n" else
                                    "ZIP" if prefix.startswith(b"PK\\x03\\x04") else
                                    "TEXT" if b"\\x00" not in prefix else "BINARY")
                if row["prefix_type"]=="TEXT":
                    row["source_header_excerpt"]=prefix[:250].decode("utf-8",errors="replace").replace("\r"," ").replace("\n"," | ")
            manifest.append(row)
    return manifest

def run(folder:Path):
    folder.mkdir(exist_ok=True,parents=True)
    out=folder/"zenodo60234_source_audit.json"
    report={"source":"ChangCrallCombes2016",
            "doi":"10.1242/jeb.137976",
            "zenodo_record":"https://zenodo.org/records/60234",
            "provider_file":FILENAME,
            "provider_published_md5":EXPECTED_MD5,
            "source_is_genuine_tracked_flight_only_if_downloaded_verified":True,
            "empirical_flight_conclusion":None}
    out.write_text(json.dumps(report,indent=2))
    errors=[]
    for url in URLS:
        try:
            req=Request(url,headers={"User-Agent":"ResearchSourceIntegrityAudit/1.0 (source-verified scientific analysis)",
                                     "Accept":"application/octet-stream,*/*"})
            with urlopen(req,timeout=45) as f:
                status=f.status
                actual_url=f.url
                raw=f.read(MAX_COMPRESSED_BYTES+1)
            if status!=200 or len(raw)>MAX_COMPRESSED_BYTES:
                raise ValueError("NO_GO_SOURCE_HTTP_OR_SIZE")
            checksum=hashlib.md5(raw).hexdigest()
            if checksum!=EXPECTED_MD5:
                raise ValueError("NO_GO_SOURCE_PROVIDER_MD5_MISMATCH "+checksum)
            manifest=safe_manifest(raw)
            if not manifest:
                raise ValueError("NO_GO_NO_NATIVE_SOURCE_ARCHIVE_MEMBERS")
            report.update({"status":"ZENODO2016_ORIGINAL_ARCHIVE_MD5_VERIFIED",
                           "successful_original_url":url,
                           "returned_url_final_host":actual_url.split("/")[2],
                           "http_status":status,
                           "byte_size":len(raw),
                           "actual_md5":checksum,
                           "actual_sha256":hashlib.sha256(raw).hexdigest(),
                           "native_member_count":len(manifest),
                           "original_zip_files":manifest,
                           "no_original_trajectory_data_committed":True})
            out.write_text(json.dumps(report,indent=2,ensure_ascii=False))
            print("STAGE10_SOURCE_ARCHIVE_VERIFIED "+json.dumps(report,ensure_ascii=False),flush=True)
            print("STAGE10_NATIVE_SCHEMA_AUDIT_COMPLETE",flush=True)
            (folder/FILENAME).write_bytes(raw)  # ephemeral CI only, not committed or uploaded
            return report
        except Exception as exc:
            errors.append({"attempt_url":url,"error_type":type(exc).__name__,
                           "failure":str(exc)[:400]})
    report["status"]="NO_GO_ORIGINAL_ZENODO_TRAJECTORY_ARCHIVE_ACCESS"
    report["attempts"]=errors
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print("STAGE10_ZENODO_SOURCE_NO_GO "+json.dumps(report,ensure_ascii=False),flush=True)
    raise RuntimeError(report["status"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage10_original")
    args=p.parse_args()
    run(Path(args.out))
