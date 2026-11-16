"""One bounded diagnosis of original 126 MB bee-model source GET 406.

No large binary downloaded. Test three fixed direct source endpoints with
HTTP Range and report original response status/header/errors. If unavailable,
declare blocked and do NOT replace with synthetic bee predictions.
"""
from __future__ import annotations
import json
from pathlib import Path
import urllib.error
import urllib.request

URLS=[
 "https://zenodo.org/api/records/20525240/files/data.zip/content",
 "https://zenodo.org/records/20525240/files/data.zip?download=1",
 "https://zenodo.org/api/records/20525240/files/data.zip/content?download=1",
 "https://zenodo.org/api/records/20525240/files/readme.txt/content"
]
def diagnostic():
    results=[]
    for u in URLS:
        r={"url":u}
        req=urllib.request.Request(u,headers={
            "User-Agent":"adaptive-gain-stage46-zip-range-diagnostic/2026",
            "Range":"bytes=0-1023"})
        try:
            with urllib.request.urlopen(req,timeout=40) as resp:
                b=resp.read(1024)
                r.update({"http_status":resp.status,
                  "received_first_bytes":len(b),
                  "content_range":resp.headers.get("Content-Range"),
                  "accept_ranges":resp.headers.get("Accept-Ranges"),
                  "declared_length":resp.headers.get("Content-Length"),
                  "content_type":resp.headers.get("Content-Type")})
        except urllib.error.HTTPError as err:
            r.update({"http_status":err.code,
                 "error_excerpt":err.read(500).decode("utf-8",errors="replace")[:500]})
        except Exception as err:
            r.update({"error_kind":type(err).__name__,
                      "error_excerpt":str(err)[:200]})
        results.append(r)
    return {"status":"BOUND_ORIGINAL_ZENODO_ZIP_RANGE_ACCESS_DIAGNOSIS",
            "cases":results,
            "no_full_source_or_model_prediction_acquired":True}

if __name__=="__main__":
    o=diagnostic()
    folder=Path("stage46_zip_diag");folder.mkdir(exist_ok=True)
    (folder/"zenodo_data_zip_http_status.json").write_text(
       json.dumps(o,indent=2,sort_keys=True)+"\n")
    print("STAGE46_ZENODO_RANGE_DIAGNOSIS",json.dumps(o,sort_keys=True))
