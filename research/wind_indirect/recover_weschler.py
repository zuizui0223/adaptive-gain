"""Public original source and schema gate, not a new ecological result."""
import csv,hashlib,io,json,os,urllib.request
from pathlib import Path
URL="https://zenodo.org/records/15447016/files/WindPollinatorData110823.csv?download=1"
MD5="9bcab4765c4fe5a9edaaf096867caf5b"
def run():
    out=Path(os.environ.get("WESCHLER_OUT","weschler_original"));out.mkdir(parents=True,exist_ok=True)
    req=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-original-data-research/1.0"})
    with urllib.request.urlopen(req,timeout=80) as r:
        data=r.read(2_000_000)
    if hashlib.md5(data).hexdigest()!=MD5:raise ValueError("MD5_MISMATCH_SOURCE_BYTES")
    try:s=data.decode("utf-8-sig");encoding="utf-8-sig"
    except UnicodeDecodeError:s=data.decode("latin-1");encoding="latin-1"
    reader=csv.reader(io.StringIO(s))
    header=next(reader);rows=list(reader)
    if len(header)<3 or any(len(x)!=len(header) for x in rows):
        raise ValueError("NON_TABULAR_OR_RAGGED_DATA")
    (out/"WindPollinatorData110823.csv").write_bytes(data)
    receipt={"source":URL,"md5":MD5,"sha256":hashlib.sha256(data).hexdigest(),
       "bytes":len(data),"encoding":encoding,"rows":len(rows),"columns":header,
       "status":"ORIGINAL_SOURCE_VERIFIED_NOT_YET_ANALYZED"}
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False))
    print("WESCHLER_SOURCE_VERIFIED",json.dumps(receipt,ensure_ascii=False),flush=True)
if __name__=="__main__":run()
