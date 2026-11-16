"""Stage49: taxonomic name-key bridge for ORIGINAL paper visual-trait taxa.

The union of the original Tunes 2021 and Koski/MacQueen/Ashman 2020
source study taxa is passed to GBIF species/match. Strict species rank,
Plantae kingdom, exact name and >=95 match confidence. No occurrence
counts or Bombus suitability queried in this file.

Source paper S1 UVP temporal slope is NOT labelled a visual nectar guide.
No source study's original taxon number is silently altered to make a
claimed 42 match its 41 source literal binomials.
"""
from __future__ import annotations
from collections import Counter
import concurrent.futures
import csv
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage45"))
from join_uv_with_global_traits import retrieve_original_uv
from gbif_taxon_occurrence_seed import _get_json
from assemble_literature_visual_species import (
    assemble,fetch_original_cb_table
)

MAX_WORKERS=4

def strict_match(name,response):
    if not name:
        return {"taxonomy_status":"UNRESOLVED_ORIGINAL_SOURCE_TAXON"}
    if not isinstance(response,dict):
        return {"taxonomy_status":"NO_GBIF_JSON"}
    # Every field is required; never infer accepted species from genus.
    if (response.get("kingdom")!="Plantae" or
        response.get("rank")!="SPECIES" or
        response.get("matchType")!="EXACT" or
        str(response.get("canonicalName","")).casefold()!=name.casefold() or
        not isinstance(response.get("confidence"),(int,float)) or
        response["confidence"]<95):
        return {"taxonomy_status":"NOT_EXACT_95_CONFIDENCE_PLANT_SPECIES",
                "source_reported_rank":str(response.get("rank","")),
                "source_reported_name":str(response.get("canonicalName",""))[:100],
                "source_reported_confidence":response.get("confidence")}
    status=response.get("status")
    if status=="ACCEPTED":
        key=response.get("usageKey")
    elif status=="SYNONYM":
        key=response.get("acceptedUsageKey")
    else:
        return {"taxonomy_status":"UNSUPPORTED_GBIF_TAXON_STATUS",
                "source_reported_status":str(status)}
    if not isinstance(key,int) or key<=0:
        return {"taxonomy_status":"NO_VALID_ACCEPTED_GBIF_KEY"}
    return {"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
            "gbif_matched_original_name":response.get("canonicalName"),
            "gbif_returned_taxon_status":status,
            "gbif_accepted_usage_key":key,
            "gbif_original_usage_key":response.get("usageKey"),
            "gbif_confidence":response.get("confidence")}

def lookup(name):
    try:
        obj=_get_json("species/match",{"name":name,"rank":"SPECIES","kingdom":"Plantae"})
        return strict_match(name,obj)
    except Exception as e:
        return {"taxonomy_status":"API_FAILURE_UNRESOLVED_NOT_ABSENT",
                "error_kind":type(e).__name__,
                "error_detail":str(e)[:160]}

def combine_taxonomy(source_rows,lookup_results):
    out=[]
    for original in source_rows:
        key=original["canonical_binomial_candidate_unreconciled"]
        tax=lookup_results.get(key,{
             "taxonomy_status":"UNRESOLVED_ORIGINAL_SOURCE_TAXON"})
        row=dict(original)
        row.update({
          "gbif_match_status":tax["taxonomy_status"],
          "gbif_accepted_species_key":tax.get("gbif_accepted_usage_key",""),
          "gbif_name_as_returned":tax.get("gbif_matched_original_name",
                                          tax.get("source_reported_name","")),
          "gbif_matched_confidence_or_missing":tax.get(
               "gbif_confidence",tax.get("source_reported_confidence","")),
          "gbif_taxon_status":tax.get("gbif_returned_taxon_status",""),
          "study_taxon_to_original_measured_site":"UNRESOLVED_UNLESS_ORIGINAL_SOURCE_LOCATED",
          "bee_model_cell_overlap":"NOT_YET_COMPUTED"
        })
        out.append(row)
    mapped=[r for r in out if r["gbif_match_status"]=="EXACT_CONFIDENT_SPECIES_MAPPED"]
    by_study=Counter(r["original_study_doi"] for r in mapped)
    return out,{
       "status":"ORIGINAL_PUBLISHED_VISUAL_TAXA_GBIF_TAXONOMIC_CROSSWALK",
       "n_original_study_taxon_records":len(out),
       "n_name_keys_queried":len(lookup_results),
       "n_exact_confident_species_records":len(mapped),
       "n_distinct_accepted_species_keys":len({r["gbif_accepted_species_key"] for r in mapped}),
       "n_unresolved_source_study_rows":len(out)-len(mapped),
       "match_status_counts":dict(sorted(Counter(r["gbif_match_status"] for r in out).items())),
       "by_original_article_exact_matched_counts":dict(sorted(by_study.items())),
       "spatial_UV_pattern_missing_for_2020_temporal_UVP_study":True,
       "no_origination_site_or_native_Bombus_inference":True,
       "no_formal_floral_visual_guide_Bombus_effect_estimated":True,
    }

def main():
    uv,_=retrieve_original_uv()
    cb=fetch_original_cb_table()
    original,summary=assemble(uv,cb)
    keys=sorted(set(x["canonical_binomial_candidate_unreconciled"]
                    for x in original if x["canonical_binomial_candidate_unreconciled"]))
    if len(original)!=121 or len(keys)!=114:
        raise ValueError("NO_GO_AUTHENTIC_SOURCE_KEY_UNIVERSE_CHANGED")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as p:
        results=list(p.map(lookup,keys))
    tax=dict(zip(keys,results))
    output,stats=combine_taxonomy(original,tax)
    p=Path("stage49_taxonomy_registry")
    p.mkdir(exist_ok=True)
    with (p/"original_121_source_visual_taxa_GBIF_species_keys.csv").open(
         "w",encoding="utf8",newline="") as f:
        columns=list(dict.fromkeys(k for row in output for k in row))
        w=csv.DictWriter(f,fieldnames=columns,extrasaction="raise")
        w.writeheader()
        w.writerows(output)
    (p/"original_paper_species_GBIF_match_receipt.json").write_text(
        json.dumps(stats,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf8")
    print("STAGE49_REAL_ORIGINAL_LITERATURE_SPECIES_TAXONOMY",
          json.dumps(stats,sort_keys=True,ensure_ascii=False))
    if stats["n_exact_confident_species_records"]<60:
        raise SystemExit("NO_GO_TOO_FEW_REAL_ORIGINAL_TAXONOMIC_MATCHES")
if __name__=="__main__":
    main()
