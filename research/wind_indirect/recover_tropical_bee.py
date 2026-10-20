"""Recover wind × orchid-bee species × forest-cover original source from Zenodo.

No unmeasured predator/biotic interaction is inferred from this archive.
"""
from __future__ import annotations
import csv,hashlib,io,json,os,urllib.request,zipfile
from pathlib import Path

URL="https://zenodo.org/records/3675327/files/CrallEtAl_OrchidBeeWindEcology.zip?download=1"
EXPECTED_MD5="42e53512e4bdad2701593a89d1c87dfd"
LIMIT=10_000_000

def archive_bytes():
    req=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-original-ecology-source/1.0"})
    with urllib.request.urlopen(req,timeout=85) as r:
        body=r.read(LIMIT+1)
        if len(body)>LIMIT:raise ValueError("SOURCE_TOO_LARGE")
        return body

def member_details(z,name):
    raw=z.read(name)
    detail={"name":name,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
    if name.lower().endswith(".csv") and len(raw)<3_000_000:
        try:s=raw.decode("utf-8-sig");encoding="utf-8"
        except UnicodeDecodeError:s=raw.decode("latin-1");encoding="latin-1"
        rdr=csv.reader(io.StringIO(s))
        try:cols=next(rdr)
        except StopIteration:raise ValueError("EMPTY_CSV_"+name)
        if len(cols)<2:raise ValueError("INVALID_SCHEMA_"+name)
        n=0
        for row in rdr:
            if len(row)!=len(cols):raise ValueError("RAGGED_CSV_"+name)
            n+=1
        detail.update({"encoding":encoding,"columns":cols,"rows":n})
    return detail

def main():
    dest=Path(os.environ.get("CRALL_OUT","wind_indirect_tropical"));dest.mkdir(parents=True,exist_ok=True)
    data=archive_bytes()
    if hashlib.md5(data).hexdigest()!=EXPECTED_MD5:raise ValueError("CRALL_ZENODO_MD5_MISMATCH")
    if not zipfile.is_zipfile(io.BytesIO(data)):raise ValueError("NOT_ZIP")
    archive=dest/"CrallEtAl_OrchidBeeWindEcology.zip";archive.write_bytes(data)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        files=[member_details(z,n) for n in z.namelist() if not n.endswith("/")]
    summary={"original_url":URL,"md5":EXPECTED_MD5,"sha256":hashlib.sha256(data).hexdigest(),
             "bytes":len(data),"source":"10.5281/zenodo.3675327","files":files}
    (dest/"receipt.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print("CRALL_ORIGINAL_SOURCE_VERIFIED",json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
