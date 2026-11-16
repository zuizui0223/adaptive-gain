"""Stage45: source-granularity and API-availability probe for a floral visual-signal macro atlas.

This is intentionally a NON-INFERENTIAL inventory. Query original public
NHM CKAN floral trait table and GBIF Bombus taxonomy / occurrence index;
report source schema, counts and page identifiers only. No remote raw
records or protected photo content are redistributed.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

NHM_RESOURCE="2552d157-9519-476c-995d-906e2433cc19"
NHM_DATASET_DOI="10.5519/p3dm31kc"
GBIF_API="https://api.gbif.org/v1"
ALLOWLIST={"data.nhm.ac.uk","api.gbif.org"}
MAX_JSON_BYTES=2_000_000
FLORAL_PATTERN=re.compile(
    r"flowe?r|floral|corolla|petal|perianth|spur|pattern|mark|colo[u]?r|nectar|pollinat|uv|ultraviolet|stamen|anther",
    re.IGNORECASE
)

def _safe_url(url):
    parsed=urllib.parse.urlsplit(url)
    if parsed.scheme!="https" or parsed.hostname not in ALLOWLIST:
        raise ValueError("NO_GO_UNTRUSTED_SOURCE_HOST")
    return url

def _get_json(url):
    request=urllib.request.Request(_safe_url(url),headers={
      "User-Agent":"adaptive-gain-stage45-floral-macro-source-probe/2026",
      "Accept":"application/json"
    })
    with urllib.request.urlopen(request,timeout=35) as response:
        data=response.read(MAX_JSON_BYTES+1)
    if len(data)>MAX_JSON_BYTES:
        raise ValueError("NO_GO_API_RESPONSE_OVERSIZED")
    parsed=json.loads(data.decode("utf-8-sig"))
    if not isinstance(parsed,dict):
        raise ValueError("NO_GO_INVALID_PUBLIC_API_JSON")
    return parsed

def _ckan(action,params):
    q=urllib.parse.urlencode(params)
    obj=_get_json("https://data.nhm.ac.uk/api/3/action/"+action+"?"+q)
    if obj.get("success") is not True or not isinstance(obj.get("result"),dict):
        raise ValueError("NO_GO_NHM_CKAN_UNSUCCESSFUL_"+action)
    return obj["result"]

def _resource_schema():
    resource=_ckan("resource_show",{"id":NHM_RESOURCE})
    if resource.get("id")!=NHM_RESOURCE:
        raise ValueError("NO_GO_NHM_RESOURCE_UUID_CHANGED")
    found=_ckan("datastore_search",{
       "resource_id":NHM_RESOURCE,"limit":2,"offset":0
    })
    fields=found.get("fields")
    records=found.get("records")
    if not isinstance(fields,list) or not fields or not isinstance(records,list):
        raise ValueError("NO_GO_NHM_DATASTORE_SCHEMA_MISSING")
    columns=[x["id"] for x in fields if isinstance(x,dict) and isinstance(x.get("id"),str)]
    matching=[f for f in columns if FLORAL_PATTERN.search(f)]
    # Only data schema and category/shape labels, no plant rows in report.
    sampletypes={}
    for column in columns[:80]:
        if not records:break
        val=records[0].get(column)
        sampletypes[column]={"type":type(val).__name__}
        if isinstance(val,str):
            sampletypes[column]["first_value_length"]=len(val)
            # For 1/2 short label fields, emitted as probe only: not a trait truth.
            if (FLORAL_PATTERN.search(column) or column.lower() in ("traits","trait")):
                sampletypes[column]["first_value_preview"]=val[:180]
    direct=resource.get("url")
    if direct and not isinstance(direct,str):
        raise ValueError("NO_GO_NHM_RESOURCE_DOWNLOAD_URL_TYPE")
    return {
      "source":"Natural History Museum London 2026 angiosperm traits",
      "doi":NHM_DATASET_DOI,
      "resource_id":NHM_RESOURCE,
      "resource_name":resource.get("name"),
      "reported_size_bytes":resource.get("size"),
      "resource_url":direct,
      "datastore_total":found.get("total"),
      "n_fields":len(columns),
      "fields":columns,
      "potential_floral_columns_not_confirmed_trait_status":matching,
      "first_record_field_types":sampletypes,
      "only_source_schema_not_any_species_claim":True,
    }

def _gbif_registry():
    match=_get_json(GBIF_API+"/species/match?"+urllib.parse.urlencode({
        "name":"Bombus","rank":"GENUS","kingdom":"Animalia"
    }))
    taxon=match.get("usageKey")
    if not isinstance(taxon,int) or match.get("rank")!="GENUS" or (
         str(match.get("canonicalName","")).lower()!="bombus"):
        raise ValueError("NO_GO_GBIF_BOMBUS_GENUS_MATCH_NOT_CONFIRMED")
    occ=_get_json(GBIF_API+"/occurrence/search?"+urllib.parse.urlencode({
        "taxonKey":taxon,"hasCoordinate":"true","hasGeospatialIssue":"false",
        "limit":1
    }))
    taxa=_get_json(GBIF_API+"/species/search?"+urllib.parse.urlencode({
        "higherTaxonKey":taxon,"rank":"SPECIES","limit":100
    }))
    if not isinstance(occ.get("count"),int) or not isinstance(taxa.get("count"),int):
        raise ValueError("NO_GO_GBIF_RESPONSE_COUNTS_MISSING")
    names=taxa.get("results") or []
    return {
       "source":"GBIF API / backbone taxonomic index",
       "taxon_name":"Bombus",
       "genus_taxon_key":taxon,
       "taxon_match_type":match.get("matchType"),
       "taxon_status":match.get("status"),
       "taxon_index_species_query_total_raw":taxa["count"],
       "first_page_accepted_Bombus_species_names":[
          r.get("canonicalName") for r in names
          if r.get("rank")=="SPECIES"
          and r.get("status")=="ACCEPTED"
          and r.get("canonicalName")
       ][:20],
       "georeferenced_genus_occurrence_index_count_not_independent_bees":occ["count"],
       "not_native_distribution_not_habitat_suitability_or_realized_visit":True,
    }

def probe():
    results={"status":"SOURCE_METADATA_PROBE_NO_BIOLOGICAL_ASSOCIATION",
             "sources":{},"errors":{},"source_only":True}
    for name,fun in (("NHM_TRAIT",_resource_schema),
                     ("GBIF_BOMBUS",_gbif_registry)):
        try:
            results["sources"][name]=fun()
        except (ValueError,urllib.error.URLError,urllib.error.HTTPError,
                TimeoutError,KeyError,TypeError,json.JSONDecodeError) as err:
            results["errors"][name]={"kind":type(err).__name__,
                                      "message":str(err)[:220]}
    return results

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="stage45_source_probe")
    o=ap.parse_args()
    result=probe()
    folder=Path(o.out)
    folder.mkdir(parents=True,exist_ok=True)
    (folder/"public_source_schema_receipt.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,allow_nan=False))
    if result["errors"]:
        raise SystemExit("SOURCE_PROBE_INCOMPLETE_NO_ECOLOGICAL_INFERENCE")

if __name__=="__main__":
    main()
