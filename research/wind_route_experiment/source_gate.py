"""Checksum-locked public Dryad v2 version-download original experimental CSV."""
from __future__ import annotations
import csv,hashlib,io,json,os,urllib.request,zipfile
from pathlib import Path
URL="https://datadryad.org/api/v2/versions/171277/download"
SHA256="2361dccb523b97f1e5e542fc492d302a5e7c290cdde72eb2dfb2ce021153d6f7"
NBYTES=22602
REQUIRED=["Bee ID","Canopy height (mm)","Wind Presence","Flight Direction Label",
"Median altitude (mm)","Altitudinal range (mm)","Median ground speed (m/s)","Lateral excursion (mm)"]
def main():
    out=Path(os.environ.get("WIND_ROUTE_OUT","wind_route_original"));out.mkdir(parents=True,exist_ok=True)
    req=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-open-data-wind-route/1.0","Accept":"application/zip,application/octet-stream"})
    with urllib.request.urlopen(req,timeout=100) as r:
        raw=r.read(3_000_000)
        if len(raw)>2_000_000:raise ValueError("RAW_SOURCE_TOO_BIG")
        final=r.geturl()
    if not zipfile.is_zipfile(io.BytesIO(raw)):raise ValueError("DRYAD_VERSION_NOT_ZIP")
    (out/"original_version.zip").write_bytes(raw)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=[n for n in z.namelist() if n.endswith("Bee_route_choice_in_wind.csv")]
        if len(names)!=1:raise ValueError("MISSING_OR_AMBIGUOUS_ORIGINAL_MEMBER")
        body=z.read(names[0])
    actual=hashlib.sha256(body).hexdigest()
    if len(body)!=NBYTES or actual!=SHA256:raise ValueError("ORIGINAL_SHA256_OR_LENGTH_CHANGED")
    s=body.decode("utf-8-sig")
    rows=list(csv.DictReader(io.StringIO(s)))
    if not rows:raise ValueError("NO_FLIGHT_ROWS")
    headers=list(rows[0])
    if set(REQUIRED)-set(headers):raise ValueError("MISSING_FLIGHT_SCHEMA:"+str(sorted(set(REQUIRED)-set(headers))))
    (out/"Bee_route_choice_in_wind.csv").write_bytes(body)
    vals={h:{} for h in ("Canopy height (mm)","Wind Presence","Flight Direction Label")}
    for h in vals:
        for row in rows: vals[h][str(row[h])]=vals[h].get(str(row[h]),0)+1
    receipt={"doi":"10.25338/B8Z34Q","version":171277,"url":URL,"final_host":final.split("/")[2],
             "sha256":actual,"original_bytes":len(body),"archive_sha256":hashlib.sha256(raw).hexdigest(),
             "rows":len(rows),"columns":headers,"n_bees":len({r["Bee ID"] for r in rows}),
             "experiment_margins":vals,"status":"ORIGINAL_CSV_VERIFIED"}
    (out/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    print("ORIGINAL_BEES_WIND_VERIFIED",json.dumps(receipt,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
