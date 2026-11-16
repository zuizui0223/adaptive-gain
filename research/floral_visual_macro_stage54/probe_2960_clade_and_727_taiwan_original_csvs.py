"""Stage54: original Dryad broad visual-colour source 2,960 species and 727 Taiwan taxa.

These datasets are plain SOURCE-RECORDED HUMAN FLOWER COLOUR,
not UV nectary guides, reward-colour age shifts, visual learning or bee
visitation. Original public Dryad API metadata and attached checksums
validate any data bytes; HTTP 401/403 is reported as UNAVAILABLE rather
than invented species/negative traits.
"""
from __future__ import annotations
from collections import Counter
import csv,hashlib,io,json,time
from pathlib import Path
import urllib.error,urllib.parse,urllib.request

API="https://datadryad.org"
DOIS={
 "2025_51_clades_2960_species":"10.5061/dryad.r4xgxd2sc",
 "2021_Taiwan_727_species":"10.5061/dryad.63xsj3v08"
}
TARGETS={
 "2025_51_clades_2960_species":"final_dataset.csv",
 "2021_Taiwan_727_species":"Table_S2_The_list_727_flowering_species.csv"
}
EXPECTED_COUNTS={"2025_51_clades_2960_species":2960,"2021_Taiwan_727_species":727}
MAX_BYTES=1_100_000


def _get(url,maxbytes=MAX_BYTES):
    if not url.startswith(API+"/api/v2/") and not url.startswith(API+"/downloads/file_stream/"):
        raise ValueError("NO_GO_UNTRUSTED_ORIGINAL_DRYAD_HOST")
    request=urllib.request.Request(url,headers={
      "User-Agent":"adaptive-gain-stage54-original-broad-floral-colour-source/2026",
      "Accept":"text/csv,application/json,application/octet-stream,*/*"
    })
    with urllib.request.urlopen(request,timeout=36) as resp:
        body=resp.read(maxbytes+1)
    if len(body)>maxbytes:
        raise ValueError("NO_GO_ORIGINAL_DRYAD_DOWNLOAD_BYTES_LIMIT")
    return body


def _metadata(doi):
    uri=API+"/api/v2/datasets/doi%3A"+urllib.parse.quote(doi,safe="")
    x=json.loads(_get(uri))
    h=(x.get("_links") or {}).get("stash:version") or {}
    path=h.get("href")
    if not isinstance(path,str) or not path.startswith("/api/v2/versions/"):
        raise ValueError("NO_GO_OFFICIAL_DRYAD_VERSION_METADATA_NOT_PRESENT")
    version=json.loads(_get(API+path+"/files"))
    files=(version.get("_embedded") or {}).get("stash:files") or []
    return x,files


def _file_source(file):
    path=file.get("path") or file.get("filename")
    links=file.get("_links") or {}
    end=(links.get("stash:download") or {}).get("href")
    if not isinstance(path,str) or not isinstance(end,str) or not end.startswith("/api/v2/files/"):
        raise ValueError("NO_GO_DRYAD_SOURCE_FILE_NOT_EXACT")
    digest=file.get("digest")
    if not isinstance(digest,str) or len(digest)!=64:
        raise ValueError("NO_GO_DRYAD_SOURCE_SHA256_MISSING")
    errors=[]
    for url in (API+end, API+"/downloads/file_stream/"+end.split("/")[-2]):
        try:
            raw=_get(url)
            if hashlib.sha256(raw).hexdigest()!=digest:
                raise ValueError("NO_GO_DRYAD_SOURCE_CHECKSUM_MISMATCH")
            return raw,{"url":url,"sha256":digest,
                        "original_source_bytes":len(raw),
                        "original_source_file":path,"source_fetch_status":"SOURCE_BYTES_SHA256_VERIFIED"}
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,ValueError) as e:
            errors.append(type(e).__name__+":"+str(e)[:100])
    return None,{"original_source_file":path,
                 "sha256":digest,"source_fetch_status":"NOT_RETRIEVED_NOT_A_NEGATIVE_TRAIT",
                 "errors":errors}


def _summarize_rows(raw):
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
    names=reader.fieldnames or []
    if not names or len(set(names))!=len(names):
        raise ValueError("NO_GO_ORIGINAL_DRYAD_CSV_FIELD_SCHEMA")
    rows=list(reader)
    return rows,{
        "n_source_rows":len(rows),
        "source_columns":names,
        "column_nonblank_counts":{name:sum(bool((r.get(name) or "").strip()) for r in rows)
                                  for name in names},
        "source_first_row_field_previews":{name:(rows[0].get(name) or "")[:80]
                                          for name in names} if rows else {},
        "not_confirmed_UV_or_nectar_guide_traits":True,
        "not_current_climatic_nativity_or_bee_occurrence":True,
    }


def probe():
    out={"status":"ORIGINAL_DRYAD_BROAD_FLORAL_COLOUR_CLADES_AND_TAIWAN_METADATA",
         "sources":{},"no_biological_color_signal_inferred_from_missing_source":True}
    for kind,doi in DOIS.items():
        entry={"dataset_doi":doi,"expected_original_source_rows_in_paper":EXPECTED_COUNTS[kind]}
        try:
            dataset,files=_metadata(doi)
            entry["dataset_title"]=dataset.get("title")
            entry["source_file_manifests"]=[{
               "path":x.get("path"),"bytes":x.get("size"),
               "digest":x.get("digest"),
               "download_href":(x.get("_links") or {}).get("stash:download",{}).get("href")}
               for x in files]
            chosen=[x for x in files if (x.get("path") or x.get("filename"))==TARGETS[kind]]
            if len(chosen)!=1:raise ValueError("NO_GO_ORIGINAL_TARGET_CSV_NOT_UNIQUE")
            body,source=_file_source(chosen[0])
            entry["source_csv_authentication"]=source
            if body is not None:
                rows,stats=_summarize_rows(body)
                entry.update(stats)
                if len(rows)!=EXPECTED_COUNTS[kind]:
                    entry["original_paper_n_vs_csv_rows_discrepancy"]=True
                # Original source CSV retained only transiently; persistent
                # record contains count, source column and checksum.
        except (urllib.error.HTTPError,urllib.error.URLError,
                TimeoutError,ValueError,KeyError,json.JSONDecodeError) as e:
            entry["source_error_status"]="SOURCE_METADATA_UNAVAILABLE_NO_SPECIES_CLAIM"
            entry["error_kind"]=type(e).__name__
            entry["error_detail"]=str(e)[:200]
        out["sources"][kind]=entry
    return out


def main():
    out=probe()
    folder=Path("stage54_broad_original_colour_sources");folder.mkdir(exist_ok=True)
    (folder/"original_2960_flower_colour_727_Taiwan_source_manifest.json").write_text(
      json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
      encoding="utf8")
    print("STAGE54_ORIGINAL_2960_AND_727_SOURCE_MANIFEST",
          json.dumps(out,ensure_ascii=False,sort_keys=True))
    print("NO_UV_NEGATIVE_OR_POLLINATOR_AVAILABILITY_INFERRED")


if __name__=="__main__":
    main()
