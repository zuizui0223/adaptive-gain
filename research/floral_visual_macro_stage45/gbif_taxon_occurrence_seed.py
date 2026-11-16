"""Stage45: GBIF accepted-taxonomy and georeferenced occurrence coverage audit
for all 80 original UV-measured Neotropical savanna plant taxa.

Original UV source: Tunes et al. 2021 DOI 10.3389/fpls.2021.618028.
All specimen/occurrence counts are opportunistic, are NOT native ranges,
absences, species distribution model predictions or visitation/pollination.
Taxonomy is accepted only at exact, high-confidence species-level match.
"""
from __future__ import annotations
import concurrent.futures
from collections import Counter
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
import csv

from join_uv_with_global_traits import retrieve_original_uv,canonical_candidate

ROOT="https://api.gbif.org/v1"
MAX_BYTES=2_000_000
MAX_WORKERS=4
USER_AGENT="adaptive-gain-stage45-original-UV-GBIF-80-taxonomy-probe/2026"


def _get_json(endpoint,params):
    if endpoint not in ("species/match","occurrence/search"):
        raise ValueError("NO_GO_UNREGISTERED_GBIF_API_ENDPOINT")
    q=urllib.parse.urlencode(params)
    url=ROOT+"/"+endpoint+"?"+q
    request=urllib.request.Request(url,headers={
       "User-Agent":USER_AGENT,"Accept":"application/json"
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request,timeout=32) as resp:
                data=resp.read(MAX_BYTES+1)
            if len(data)>MAX_BYTES:
                raise ValueError("NO_GO_GBIF_RESPONSE_OVERSIZED")
            obj=json.loads(data.decode("utf-8"))
            if not isinstance(obj,dict):
                raise ValueError("NO_GO_GBIF_RESPONSE_NOT_OBJECT")
            return obj
        except urllib.error.HTTPError as err:
            if err.code in (429,500,502,503) and attempt<2:
                time.sleep(1.5*(attempt+1))
                continue
            raise


def validate_taxon_match(name,response):
    """Never accept a fuzzy, doubtful, genus-only or wrong-canonical match."""
    if not name:
        return {"status":"NON_SPECIES_OR_UNCERTAIN_ORIGINAL_NAME"}
    if not isinstance(response,dict) or not response:
        return {"status":"NO_GBIF_MATCH_RESPONSE"}
    rank=response.get("rank")
    canonical=response.get("canonicalName","")
    confidence=response.get("confidence")
    match_type=response.get("matchType")
    taxonomy=response.get("status")
    accepted=(isinstance(confidence,(float,int)) and confidence>=95
              and rank=="SPECIES" and match_type=="EXACT"
              and canonical.casefold()==name.casefold())
    if not accepted:
        return {"status":"NOT_EXACT_HIGH_CONFIDENCE_SPECIES",
                "returned_rank":rank,"returned_match_type":match_type,
                "reported_confidence":confidence,
                "reported_canonical":canonical}
    raw_key=response.get("usageKey")
    if taxonomy=="ACCEPTED":
        accepted_key=raw_key
    elif taxonomy=="SYNONYM":
        accepted_key=response.get("acceptedUsageKey")
    else:
        return {"status":"UNSUPPORTED_TAXONOMIC_STATUS",
                "reported_status":taxonomy}
    if not isinstance(accepted_key,int) or accepted_key<=0:
        return {"status":"NO_ACCEPTED_SPECIES_KEY"}
    return {
       "status":"EXACT_HIGH_CONFIDENCE_SPECIES_MAPPED",
       "source_taxon":name,
       "reported_kingdom":response.get("kingdom"),
       "match_type":match_type,
       "taxonomic_status":taxonomy,
       "gbif_original_usage_key":raw_key,
       "gbif_accepted_species_key":accepted_key,
       "gbif_matched_canonical_name":canonical,
       "gbif_match_confidence":confidence,
    }


def resolve_original_taxon(original):
    name=canonical_candidate(original["taxon_as_published"])
    out={"original_taxon":original["taxon_as_published"],
         "canonical_binomial_candidate":name or "",
         "source_uv_category":original["uv_category"],
         "uv_pattern_measured":original["uv_pattern_present"],
         "source_pollination_syndrome_only":original["pollination_system_reported"],
         "gbif_taxonomy_status":"NOT_QUERIED",
         "gbif_accepted_taxon_key":"",
         "gbif_match_confidence":"",
         "georeferenced_occurrence_count":"",
         "occurrence_response_status":"NOT_QUERIED",
         "not_native_distribution_or_predicted_suitability":True}
    if name is None:
        out["gbif_taxonomy_status"]="UNRESOLVED_SOURCE_NAME"
        return out
    try:
        resp=_get_json("species/match",{
            "name":name,"rank":"SPECIES","kingdom":"Plantae"
        })
        m=validate_taxon_match(name,resp)
        out["gbif_taxonomy_status"]=m["status"]
        out["gbif_match_confidence"]=m.get("gbif_match_confidence","")
        out["gbif_taxonomic_status"]=m.get("taxonomic_status","")
        out["gbif_returned_name"]=m.get("gbif_matched_canonical_name",
                                        m.get("reported_canonical",""))
        if m["status"]!="EXACT_HIGH_CONFIDENCE_SPECIES_MAPPED":
            return out
        key=m["gbif_accepted_species_key"]
        out["gbif_accepted_taxon_key"]=key
        occurrence=_get_json("occurrence/search",{
            "taxonKey":key,"hasCoordinate":"true",
            "hasGeospatialIssue":"false","limit":0
        })
        n=occurrence.get("count")
        if not isinstance(n,int) or n<0:
            out["occurrence_response_status"]="NO_GO_BAD_OCCURRENCE_COUNT"
        else:
            out["georeferenced_occurrence_count"]=n
            out["occurrence_response_status"]="ORIGINAL_GBIF_INDEX_COUNT_NOT_INDEPENDENT_LOCALITIES"
    except (urllib.error.HTTPError,urllib.error.URLError,
            TimeoutError,ValueError,KeyError) as err:
        out["occurrence_response_status"]="API_UNAVAILABLE_OR_LIMITED_NOT_ZERO"
        out["error_kind"]=type(err).__name__
        out["error_summary"]=str(err)[:120]
    return out


def summarize(rows):
    if len(rows)!=80:
        raise ValueError("NO_GO_NOT_ALL_80_SOURCE_TAXA")
    statuses=Counter(x["gbif_taxonomy_status"] for x in rows)
    observed=[r for r in rows if isinstance(r.get("georeferenced_occurrence_count"),int)]
    return {
       "status":"ORIGINAL_UV_80_GBIF_TAXONOMY_AND_OCCURRENCE_COVERAGE_AUDIT",
       "original_uv_taxa":len(rows),
       "taxonomy_statuses":dict(sorted(statuses.items())),
       "matched_exact_species":statuses.get("EXACT_HIGH_CONFIDENCE_SPECIES_MAPPED",0),
       "taxa_with_returned_georeferenced_occurrence_counts":len(observed),
       "taxa_with_positive_georeferenced_index_counts":sum(
           r["georeferenced_occurrence_count"]>0 for r in observed),
       "uv_patterned_taxa_in_source":sum(x["uv_pattern_measured"] for x in rows),
       "unresolved_taxa_never_encoded_as_absences":True,
       "GBIF_counts_not_species_distribution_predictions":True,
       "GBIF_counts_not_native_occurrence_not_visitation_not_independent_individuals":True,
       "source_doi":"10.3389/fpls.2021.618028",
       "gbif_api_prefix":ROOT,
       "no_Bombus_joint_distribution_sdm_test_yet":True
    }


def main():
    original,metadata=retrieve_original_uv()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        rows=list(pool.map(resolve_original_taxon,original))
    summary=summarize(rows)
    dest=Path("stage45_gbif_uv_taxa")
    dest.mkdir(exist_ok=True)
    keys=sorted(set().union(*(r.keys() for r in rows)))
    with (dest/"GBIF_matched_original_80_UV_taxa.csv").open(
        "w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    (dest/"source_GBIF_taxonomic_coverage.json").write_text(
       json.dumps(summary,indent=2,ensure_ascii=False,sort_keys=True)+"\n",
       encoding="utf8")
    print("STAGE45_REAL_GBIF_UV_TAXONOMY",json.dumps(summary,sort_keys=True))
    print("STAGE45_UV_SOURCE_PATTERNS_NOT_BOMBUS_SDM")
    if summary["matched_exact_species"]<10:
        raise SystemExit("NO_GO_TOO_FEW_AUTHENTIC_GBIF_TAXONOMIC_MATCHES")


if __name__=="__main__":
    main()
