"""Fetch and verify the public EuPollTrait original trait archive.

This stage is only source acquisition/schema discovery, not a biological result.
"""
from __future__ import annotations
import hashlib, json, os, sys, urllib.request, zipfile
from pathlib import Path

RECORD="https://zenodo.org/records/18032357"
NAME="pollinator_traits_bees_hoverflies_repository.zip"
URL=f"{RECORD}/files/{NAME}?download=1"
EXPECTED_MD5="7a50cc03e2c5a287e663dc5d029f8026"
LIMIT=100_000_000

def main():
    out=Path(os.environ.get("EUPOLL_OUT","eupoll_source"));out.mkdir(parents=True,exist_ok=True)
    path=out/NAME
    headers={"User-Agent":"adaptive-gain-research/1.0 (public biodiversity source audit)"}
    req=urllib.request.Request(URL,headers=headers)
    with urllib.request.urlopen(req,timeout=100) as r:
        if r.status!=200:raise RuntimeError(f"Unexpected HTTP status: {r.status}")
        actual=0
        with path.open("wb") as f:
            while True:
                chunk=r.read(1_048_576)
                if not chunk:break
                actual+=len(chunk)
                if actual>LIMIT:raise ValueError("SOURCE_EXCEEDS_LIMIT")
                f.write(chunk)
    raw=path.read_bytes()
    md5=hashlib.md5(raw).hexdigest()
    if md5!=EXPECTED_MD5:raise ValueError(f"ORIGINAL_MD5_MISMATCH: {md5}")
    if not zipfile.is_zipfile(path):raise ValueError("ORIGINAL_NOT_ZIP")
    info=[]
    with zipfile.ZipFile(path) as z:
        if sum(i.file_size for i in z.infolist())>250_000_000:raise ValueError("SOURCE_INFLATED_TOO_LARGE")
        for i in z.infolist():
            if i.is_dir():continue
            info.append({"path":i.filename,"bytes":i.file_size,"crc":hex(i.CRC)})
    receipt={"source":URL,"doi":"10.5281/zenodo.18032357","md5":md5,
             "sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),
             "n_files":len(info),"files":info,"status":"ORIGINAL_SOURCE_VERIFIED"}
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
    print("EUPOLL_SOURCE_VERIFIED",json.dumps(receipt),flush=True)

if __name__=="__main__":main()
