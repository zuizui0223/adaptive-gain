"""Diagnose NHM CKAN large-page HTTP 409 without repeated blind retries."""
from __future__ import annotations
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

RESOURCE="2552d157-9519-476c-995d-906e2433cc19"
CASES=((2,0),(50,0),(100,0),(500,0),(800,0),(2,2),(50,50))
def diagnostics():
    ret=[]
    for limit,offset in CASES:
        url="https://data.nhm.ac.uk/api/3/action/datastore_search?"+urllib.parse.urlencode({
          "resource_id":RESOURCE,"limit":limit,"offset":offset})
        request=urllib.request.Request(url,headers={
          "Accept":"application/json",
          "User-Agent":"adaptive-gain-stage45-CKAN-pagination-diagnostic/2026"})
        result={"limit":limit,"offset":offset}
        try:
            with urllib.request.urlopen(request,timeout=25) as stream:
                data=stream.read(2_000_000)
                result["http_status"]=stream.status
            obj=json.loads(data)
            payload=obj.get("result") or {}
            result["api_success"]=obj.get("success")
            result["returned_records"]=len(payload.get("records") or [])
            result["total"]=payload.get("total")
            result["error_excerpt"]=str(obj.get("error",""))[:200]
        except urllib.error.HTTPError as exc:
            result["http_status"]=exc.code
            result["error_excerpt"]=exc.read(700).decode("utf-8",errors="replace")[:500]
        except Exception as exc:
            result["error_kind"]=type(exc).__name__
            result["error_excerpt"]=str(exc)[:200]
        ret.append(result)
        time.sleep(.4)
    return {"status":"DIAGNOSTIC_ONLY_NO_BIOLOGICAL_INFERENCE",
            "source_resource_id":RESOURCE,"cases":ret}

if __name__=="__main__":
    data=diagnostics()
    d=Path("stage45_diagnostic");d.mkdir(parents=True,exist_ok=True)
    (d/"nhm_api_page_sizes.json").write_text(
       json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    print("NHM_PAGE_SIZE_DIAGNOSTIC",json.dumps(data,ensure_ascii=False,sort_keys=True))
