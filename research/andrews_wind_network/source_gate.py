"""Source-locked DataONE copy of LTER SA026 original watch and flower surveys.

Stage 0 ONLY. Fail closed on data integrity or permissions. No ecology effect
is estimated here. Anonymous public DataONE resolves are used, not EDI key workarounds.
"""
from __future__ import annotations
import csv,hashlib,io,json,os,urllib.parse,urllib.request,urllib.error
from collections import Counter,defaultdict
from pathlib import Path

SRC={
"watch":{"entity":"a86814e421eca03a12001ffafe3763f2",
 "bytes":11823316,"sha1":"fcd28cf0c9623fbfbc5619136334265a65f13dc4",
 "md5":"7be658632075908343c5ab72c4de9c50","rows":74942},
"flowers":{"entity":"55544d327f32eeb7f29b77b275a8acd1",
 "bytes":2782356,"sha1":"c93b5496154245b9e94dc3362297ed354db3ebb6"}}
PACKAGE="knb-lter-and.5216.8"
MAX_BYTES=20_000_000

def original_public_url(entity):
    pid=f"https://pasta.lternet.edu/package/data/eml/knb-lter-and/5216/8/{entity}"
    return "https://cn.dataone.org/cn/v2/resolve/"+urllib.parse.quote(pid,safe="")

def acquire(name,cfg,dest):
    url=original_public_url(cfg["entity"])
    request=urllib.request.Request(url,headers={
      "Accept":"text/csv,application/octet-stream,*/*",
      "User-Agent":"adaptive-gain-source-locked-SA026-research/1.0"})
    with urllib.request.urlopen(request,timeout=110) as res:
        status=res.status;final=res.geturl()
        output=bytearray()
        while True:
            buf=res.read(1024*1024)
            if not buf:break
            output.extend(buf)
            if len(output)>MAX_BYTES:raise ValueError("SOURCE_SAFETY_SIZE_LIMIT")
    raw=bytes(output)
    receipt={"url":url,"final_url":final,"status":status,"content_type":res.headers.get("Content-Type"),
       "bytes":len(raw),"sha1":hashlib.sha1(raw).hexdigest(),
       "sha256":hashlib.sha256(raw).hexdigest(),"md5":hashlib.md5(raw).hexdigest()}
    if len(raw)!=cfg["bytes"] or receipt["sha1"]!=cfg["sha1"]:
        raise ValueError("PUBLIC_SOURCE_DIGEST_OR_SIZE_MISMATCH:"+name+":"+json.dumps(receipt))
    if "md5" in cfg and receipt["md5"]!=cfg["md5"]:
        raise ValueError("PUBLIC_SOURCE_MD5_MISMATCH:"+name)
    dest.write_bytes(raw)
    receipt["source_verified"]=True
    return receipt,raw

def profile(raw,name):
    try: decoded=raw.decode("utf-8-sig");codec="utf-8-sig"
    except UnicodeDecodeError:decoded=raw.decode("latin-1");codec="latin-1"
    reader=csv.DictReader(io.StringIO(decoded,newline=""))
    headers=reader.fieldnames or []
    if len(headers)<10:raise ValueError("WRONG_CSV_HEADER:"+name)
    count=0;values=defaultdict(Counter);nulls=Counter();duplicates=0
    seen=set()
    selections={"WIND","PPI_STATUS","SAMPLEDATE","YEAR","MEADOW","PLOT_ID","WATCH",
                "MINUTE","VISSP_NO","NO_INT","PLTSP_CODE"}
    for row in reader:
        count+=1
        if None in row:raise ValueError("CSV_EXTRA_FIELD:"+name+":"+str(count))
        for h in headers:
            val=(row.get(h) or "").strip()
            if not val or val.upper() in {"NA","NULL"}:nulls[h]+=1
            if h in selections:values[h][val]+=1
        if name=="watch":
            pk=tuple(row.get(s) for s in ("SAMPLEDATE","MINUTE","WATCH","PLOT_ID","VISSP_NO"))
            if pk in seen:duplicates+=1
            seen.add(pk)
    if name=="watch" and count!=SRC["watch"]["rows"]:
        raise ValueError("ROW_COUNT_MISMATCH_EXPECTED_74942:"+str(count))
    profile={"encoding":codec,"rows":count,"columns":headers,
      "missing_or_NA":dict(nulls),
      "duplicate_nominal_primary_keys":duplicates if name=="watch" else None,
      "frequency":{"WIND":values["WIND"].most_common(15),
          "PPI_STATUS":values["PPI_STATUS"].most_common(15),
          "YEAR":values["YEAR"].most_common(15),
          "MINUTE":values["MINUTE"].most_common(25),
          "WATCH":values["WATCH"].most_common(25),
          "NO_INT":values["NO_INT"].most_common(20)},
      "distinct":{"SAMPLEDATE":len(values["SAMPLEDATE"]),
          "MEADOW":len(values["MEADOW"]),"PLOT_ID":len(values["PLOT_ID"]),
          "VISSP_NO":len(values["VISSP_NO"]),"PLTSP_CODE":len(values["PLTSP_CODE"])}}
    return profile

def main():
    out=Path(os.environ.get("ANDREWS_SOURCE_OUT","andrews_original"));out.mkdir(parents=True,exist_ok=True)
    receipt={"package":PACKAGE,"doi":"10.6073/pasta/eec55cbc3dbfc56428629773737ab3e5",
      "scope":"ORIGINAL_DATA_AUDIT_NO_BIOLOGICAL_INFERENCE","entities":{}}
    for name,cfg in SRC.items():
        result,raw=acquire(name,cfg,out/f"{name}.csv")
        result["profile"]=profile(raw,name)
        receipt["entities"][name]=result
        print("ANDREWS_ORIGINAL_PROFILE",name,json.dumps(result,ensure_ascii=False),flush=True)
    (out/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False))
    print("ANDREWS_ORIGINAL_SOURCE_VERIFIED",flush=True)

if __name__=="__main__":main()
