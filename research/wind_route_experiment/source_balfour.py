"""Public original Balfour-Ratnieks 2025/2026 wind and flower transfer source gate.

No inference here; verifies nested ZIP exactly and full row/file headers.
"""
from __future__ import annotations
import csv,hashlib,io,json,os,urllib.request,zipfile
from pathlib import Path
URL="https://datadryad.org/api/v2/versions/442436/download"
SHA256="79d9ed20ccaa0370d31cd454eb6b293efbf2d18525443a3ae16ae3154a43fa38"
SIZE=7338
REQUIRED=["Balfouretal_Surveys_DataDryad.csv","Balfouretal_Foraging_Rate_DataDryad.csv",
          "Balfouretal_Inflorescence_Switch_Rate_DataDryad.csv"]
def main():
    root=Path(os.environ.get("BALFOUR_OUT","balfour_original"));root.mkdir(parents=True,exist_ok=True)
    req=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-public-wind-flower/1.0",
                                             "Accept":"application/zip,application/octet-stream"})
    with urllib.request.urlopen(req,timeout=90) as response:
        raw=response.read(4_000_000)
    if not zipfile.is_zipfile(io.BytesIO(raw)):raise ValueError("PUBLIC_VERSION_NOT_ZIP")
    (root/"published_version.zip").write_bytes(raw)
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        names=[n for n in outer.namelist() if n.endswith("Balfouretal_Wind_Pollinators_DataDryad.zip")]
        if len(names)!=1:raise ValueError("NO_UNIQUE_ORIGINAL_NESTED_ZIP")
        original=outer.read(names[0])
    if hashlib.sha256(original).hexdigest()!=SHA256 or len(original)!=SIZE:
        raise ValueError("SOURCE_ORIGINAL_ZIP_DIGEST_CHANGED")
    (root/"original_nested.zip").write_bytes(original)
    report={"source_doi":"10.5061/dryad.4qrfj6qpf","source_version":442436,
        "original_zip_sha256":SHA256,"original_bytes":len(original),"tables":{}}
    with zipfile.ZipFile(io.BytesIO(original)) as nested:
        for target in REQUIRED:
            candidates=[n for n in nested.namelist() if n.endswith(target) and "__MACOSX" not in n and "/._" not in n]
            if len(candidates)!=1:raise ValueError("AMBIGUOUS_DATA_TABLE:"+target+":"+str(candidates))
            raw_table=nested.read(candidates[0])
            try:text=raw_table.decode("utf-8-sig");enc="utf-8"
            except UnicodeDecodeError:text=raw_table.decode("latin-1");enc="latin-1"
            reader=csv.reader(io.StringIO(text))
            header=next(reader);n=0;bad=0
            for row in reader:
                n+=1
                if len(row)!=len(header):bad+=1
            if bad:raise ValueError("CSV_WIDTH_MISMATCH:"+target)
            (root/target).write_bytes(raw_table)
            report["tables"][target]={"rows":n,"columns":header,
                "sha256":hashlib.sha256(raw_table).hexdigest(),"encoding":enc}
            print("BALFOUR_ORIGINAL_TABLE",target,json.dumps(report["tables"][target]),flush=True)
    report["status"]="SOURCE_VERIFIED_NO_INFERENCE"
    (root/"receipt.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print("BALFOUR_SOURCE_VERIFIED",json.dumps(report,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
