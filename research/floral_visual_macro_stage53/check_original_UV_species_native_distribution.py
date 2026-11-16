"""Stage53: audit native-vs-introduced country evidence for 159 source UV plants.

Original UV phenotype source: Koski & Ashman 2016, 177 Table S2 rows,
159 distinct accepted GBIF taxa from source-verified Stage49/52. This
stage queries GBIF ChecklistBank /species/{usageKey}/distributions. Each
distribution is a *checklist claim*, not a verified occurrence, plant
phenotype locality, contemporary source native-range polygon, or proof
of modelled bee visitation.

Use an ISO country only if a checklist explicitly supplies both that
country and a NATIVE status and no conflicting introduced status.
Unknown/missing status is NEVER native or absent. A taxon with no
published ChecklistBank distributions remains UNKNOWN, not non-native.
Each accepted species gets one and only one aggregate output row.
"""
from __future__ import annotations
import csv
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from collections import Counter,defaultdict
from pathlib import Path
import argparse

API="https://api.gbif.org/v1/species/"
MAX_SOURCE_ROWS=159
SOURCE_PATTERN_COUNTS={"0":81,"1":78}
PAGES_PER_TAXON_MAX=4
PAGE_SIZE=300
MAX_RESPONSE_BYTES=1_800_000
WORKERS=5
NATIVE_CODES={"NATIVE","NATIVE_REINTRODUCED","NATIVE_REINTRODUCTION"}
INTRO_CODES={"INTRODUCED","NATURALISED","NATURALIZED","INVASIVE",
             "INTRODUCED_ASSISTED_COLONISATION","MANAGED","CULTIVATED"}
UNKNOWN_CODES={"","UNKNOWN","UNCERTAIN","DOUBTFUL","VAGRANT","UNSPECIFIED"}


def read_source(filename,expected=MAX_SOURCE_ROWS):
    with Path(filename).open(encoding="utf8",newline="") as f:
        source=list(csv.DictReader(f))
    if len(source)!=expected:
        raise ValueError("NO_GO_ORIGINAL_2016_SOURCE_SPECIES_GRAIN")
    if len({r["gbif_accepted_species_key"] for r in source})!=len(source):
        raise ValueError("NO_GO_ORIGINAL_2016_ACCEPTED_TAXON_DUPLICATION")
    if expected==MAX_SOURCE_ROWS:
        count=Counter(r["source_2016_UV_pattern"] for r in source)
        if dict(count)!=SOURCE_PATTERN_COUNTS:
            raise ValueError("NO_GO_ORIGINAL_UV_BINARY_COUNTS_DRIFT")
    if not all(str(x["gbif_accepted_species_key"]).isdigit() for x in source):
        raise ValueError("NO_GO_NONNUMERIC_GBIF_ACCEPTED_SPECIES_KEY")
    return source


def fetch_json(url):
    if not url.startswith(API):
        raise ValueError("NO_GO_SOURCE_HOST_NOT_GBIF")
    for i in range(3):
        req=urllib.request.Request(url,headers={
            "User-Agent":"adaptive-gain-floral-native-source-stage53/2026",
            "Accept":"application/json"})
        try:
            with urllib.request.urlopen(req,timeout=30) as resp:
                data=resp.read(MAX_RESPONSE_BYTES+1)
            if len(data)>MAX_RESPONSE_BYTES:
                raise ValueError("NO_GO_GBIF_CHECKLIST_RESPONSE_TOO_LARGE")
            obj=json.loads(data)
            if not isinstance(obj,dict):
                raise ValueError("NO_GO_GBIF_CHECKLIST_INVALID_JSON")
            return obj
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError):
            if i==2:
                raise
            time.sleep(.7*(i+1))


def fetch_checklist_distribution(taxon_key):
    if not isinstance(taxon_key,int) or taxon_key<=0:
        raise ValueError("NO_GO_CHECKLIST_SPECIES_KEY")
    items=[]
    seen=set()
    n_pages=0
    end=False
    errors=[]
    while n_pages<PAGES_PER_TAXON_MAX and not end:
        params=urllib.parse.urlencode({"limit":PAGE_SIZE,"offset":len(items)})
        url=f"{API}{taxon_key}/distributions?{params}"
        try:
            result=fetch_json(url)
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as e:
            errors.append(type(e).__name__+":"+str(e)[:110])
            return {"status":"SOURCE_API_UNAVAILABLE_CHECKLIST_UNKNOWN",
                    "items":[],"pages":n_pages,"truncated":True,
                    "errors":errors}
        rows=result.get("results")
        end=result.get("endOfRecords")
        if not isinstance(rows,list) or not isinstance(end,bool):
            raise ValueError("NO_GO_GBIF_CHECKLIST_PAGINATION_SCHEMA_CHANGED")
        if len(rows)>PAGE_SIZE or (not end and not rows):
            raise ValueError("NO_GO_GBIF_CHECKLIST_PAGINATION_NONPROGRESS")
        for r in rows:
            if not isinstance(r,dict):
                raise ValueError("NO_GO_CHECKLIST_RECORD_NOT_OBJECT")
            # Page result duplication can happen in a mutable API index:
            # keep a ledger but do not interpret duplicate checklist claims
            key=json.dumps(r,sort_keys=True,ensure_ascii=False)
            if key not in seen:
                seen.add(key)
                items.append(r)
        n_pages+=1
    return {"status":"GBIF_CHECKLIST_DISTRIBUTIONS_RETURNED",
            "items":items,"pages":n_pages,"truncated":not end,
            "errors":errors}


def harmonize_country_claims(records):
    """Never infer complete nativity from missing checklist/source records."""
    stats=Counter()
    country_status=defaultdict(set)
    sources=Counter()
    for rec in records:
        country=str(rec.get("country") or "").strip().upper()
        status=str(rec.get("establishmentMeans") or "").strip().upper()
        source=str(rec.get("source") or "").strip()
        if source:sources[source[:100]]+=1
        if status in NATIVE_CODES:
            label="native"
        elif status in INTRO_CODES:
            label="introduced"
        elif status in UNKNOWN_CODES:
            label="unknown"
        else:
            label="unrecognized"
        stats["checklist_total"]+=1
        stats["status_"+label]+=1
        if not country or len(country)!=2 or not country.isalpha():
            stats["non_ISO_country_code_or_missing"]+=1
            continue
        country_status[country].add(label)
    safe_native=[]
    safe_intro=[]
    conflict=[]
    unknown=[]
    for country,labels in sorted(country_status.items()):
        if "native" in labels and "introduced" in labels:
            conflict.append(country)
        elif labels=={"native"}:
            safe_native.append(country)
        elif labels=={"introduced"}:
            safe_intro.append(country)
        else:
            unknown.append(country)
    return {
      "n_checklist_items":stats["checklist_total"],
      "n_explicit_native_claims":stats["status_native"],
      "n_explicit_introduced_claims":stats["status_introduced"],
      "n_unknown_or_unrecognized_status_claims":stats["status_unknown"]+stats["status_unrecognized"],
      "n_without_valid_country":stats["non_ISO_country_code_or_missing"],
      "explicit_native_nonconflicting_ISO_countries":safe_native,
      "explicit_introduced_nonconflicting_ISO_countries":safe_intro,
      "conflicting_native_vs_introduced_ISO_countries":conflict,
      "unresolved_ISO_countries":unknown,
      "n_distinct_checklist_sources_reported":len(sources),
      "native_status_only_if_explicit_and_not_conflicted":True,
      "no_checklist_country_listing_is_NOT_a_nativity_absence":True,
      "country_level_not_original_UV_phototyped_locality":True
    }


def one_species(source):
    key=int(source["gbif_accepted_species_key"])
    c=fetch_checklist_distribution(key)
    data=harmonize_country_claims(c["items"])
    return {
      "gbif_accepted_species_key":key,
      "original_source_2016_UV_pattern":int(source["source_2016_UV_pattern"]),
      "original_source_2016_genus_or_unknown":source.get("original_2016_source_genus_or_unknown",""),
      "source_2016_mean_latitude_degrees_N":float(source["published_latitude_mean"]),
      "source_2016_mean_UVB":float(source["published_uvb_mean"]),
      "GBIF_checklist_api_status":c["status"],
      "GBIF_distribution_pages_read":c["pages"],
      "GBIF_checklist_source_record_truncated":c["truncated"],
      "GBIF_checklist_error_type_or_empty":"|".join(c["errors"]),
      **data,
      "no_proven_current_native_species_range_polygon":True,
      "no_original_UV_measurement_individual_site_mapping":True,
      "no_Bombus_visitor_or_plant_fitness_inference":True
    }


def summary(rows):
    if len(rows)!=MAX_SOURCE_ROWS:
        raise ValueError("NO_GO_NOT_ALL_159_SOURCE_SPECIES")
    statuses=Counter(r["GBIF_checklist_api_status"] for r in rows)
    bytrait=[]
    for p in (0,1):
        sub=[r for r in rows if r["original_source_2016_UV_pattern"]==p]
        bytrait.append({
           "source_UV_pattern_binary":p,"n_original_accepted_species":len(sub),
           "n_species_with_any_unconflicted_explicit_native_ISO_countries":sum(
               bool(r["explicit_native_nonconflicting_ISO_countries"]) for r in sub),
           "n_species_with_any_checklist_distribution_items":sum(
               r["n_checklist_items"]>0 for r in sub),
           "n_species_with_native_introduced_country_conflict":sum(
               bool(r["conflicting_native_vs_introduced_ISO_countries"]) for r in sub)
        })
    return {
       "status":"2016_ORIGINAL_UV_PLANTS_GBIF_NATIVE_DISTRIBUTION_CHECKLIST_COVERAGE_AUDIT",
       "original_source_accepted_species":len(rows),
       "source_UV_pattern_state_counts":dict(sorted(
           Counter(r["original_source_2016_UV_pattern"] for r in rows).items())),
       "n_species_with_checklist_records":sum(r["n_checklist_items"]>0 for r in rows),
       "n_species_with_any_explicit_nonconflicted_native_ISO_country":sum(
            bool(r["explicit_native_nonconflicting_ISO_countries"]) for r in rows),
       "n_species_with_3_or_more_native_ISO_countries":sum(
            len(r["explicit_native_nonconflicting_ISO_countries"])>=3 for r in rows),
       "n_species_with_native_vs_introduced_country_conflict":sum(
            bool(r["conflicting_native_vs_introduced_ISO_countries"]) for r in rows),
       "n_species_pagination_truncated":sum(r["GBIF_checklist_source_record_truncated"]
                                            for r in rows),
       "source_api_status_counts":dict(sorted(statuses.items())),
       "taxon_UV_group_nativity_coverage":bytrait,
       "GBIF_checklist_country_claim_not_native_range_polygon":True,
       "unknown_status_is_never_true_absence_or_native":True,
       "no_original_plant_UV_specimen_location_recovered":True,
       "no_new_UV_pattern_by_Bombus_climate_phylogeny_adjusted_effect":True
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-159",required=True)
    args=p.parse_args()
    species=read_source(args.source_159)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results=list(pool.map(one_species,species))
    report=summary(results)
    dest=Path("stage53_nativity_checklist")
    dest.mkdir(exist_ok=True)
    flat=[]
    for q in results:
        flat.append({k:json.dumps(v,ensure_ascii=False,sort_keys=True)
                      if isinstance(v,(list,dict)) else v for k,v in q.items()})
    with (dest/"original_159_UV_plants_GBIF_checklist_native_country_evidence.csv").open(
         "w",encoding="utf8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(flat[0]))
        writer.writeheader();writer.writerows(flat)
    (dest/"native_country_source_availability_receipt.json").write_text(
       json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n",
       encoding="utf8")
    print("STAGE53_REAL_ORIGINAL_UV_SPECIES_CHECKLIST_NATIVITY_COVERAGE",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("NO_CHECKLIST_COUNTRY_IS_NATIVE_RANGE_POLYGON_OR_SOURCE_UV_MEASURED_LOCALITY")


if __name__=="__main__":
    main()
