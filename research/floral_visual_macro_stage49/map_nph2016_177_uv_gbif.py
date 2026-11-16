"""Stage49: original 177 UV-patterned Potentilleae taxa → accepted GBIF species IDs.

Only source S1-verified genus/binomial candidate names are queried, with
the exact original 2016 Table S2 UVP and binary source status preserved.
Unresolved nine paper source codes remain UNKNOWN, not missing biology.
Infraspecific source rows are NEVER silently counted as independent
accepted species or collapsed to a potentially conflicting single
UV guide state.

This creates a taxon-key list for later native-range and bee-model GIS,
not a UV pattern × Bombus association or pollinator cognition result.
"""
from __future__ import annotations

from collections import Counter,defaultdict
import concurrent.futures
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage45"))
from gbif_taxon_occurrence_seed import _get_json
from match_literature_visual_taxa_gbif import strict_match
from probe_nph2016_177_europepmc_supplement import _fetch,API
from extract_nph2016_original_uv_177 import (
 parse_source_rows,summarize,PAGES,MEMBER,ORIGINAL_TABLE_PDF_SHA256
)
from map_nph2016_tableS1_author_names import s1_author_name_index,source_match_rows

MAX_WORKERS=4
ARTICLE="10.1111/nph.13921"

def query_exact_original_name(name):
    try:
        j=_get_json("species/match",{
           "name":name,"rank":"SPECIES","kingdom":"Plantae"
        })
        return strict_match(name,j)
    except Exception as err:
        return {"taxonomy_status":"GBIF_API_ERROR_UNRESOLVED_NOT_ABSENCE",
                "error_type":type(err).__name__,
                "error_detail":str(err)[:130]}

def attach_taxonomy(source_rows,resolved):
    out=[]
    for original in source_rows:
        name=original["original_S1_author_full_binomial_candidate"]
        result=resolved.get(name,{"taxonomy_status":"ORIGINAL_S1_NAME_UNRESOLVED"})
        r=dict(original)
        r["accepted_GBIF_species_match_status"]=result["taxonomy_status"]
        r["accepted_GBIF_taxon_key_or_empty"]=result.get("gbif_accepted_usage_key","")
        r["accepted_GBIF_name_or_empty"]=result.get("gbif_matched_original_name","")
        r["source_original_taxon_unit"]="2016_original_table_S2_taxon_variety_not_guaranteed_independent_species"
        r["UV_pattern_distribution_model_join"]="NOT_COMPUTED"
        out.append(r)
    matches=[x for x in out if x["accepted_GBIF_species_match_status"]=="EXACT_CONFIDENT_SPECIES_MAPPED"]
    eligible_keys=defaultdict(list)
    for r in matches:
        eligible_keys[r["accepted_GBIF_taxon_key_or_empty"]].append(r)
    conflicts=[]
    for key,records in eligible_keys.items():
        if len({int(r["source_measured_UV_pattern_present"]) for r in records})>1:
            conflicts.append({
               "source_accepted_GBIF_key":key,
               "original_source_S2_codes":[r["original_taxon_code"] for r in records],
               "source_UV_patterns":[int(r["source_measured_UV_pattern_present"])
                                     for r in records],
               "status":"INFRASPECIFIC_SOURCE_UV_DISAGREEMENT_NO_COLLAPSE"
            })
    source_counter=Counter(x["accepted_GBIF_species_match_status"] for x in out)
    return out,{
       "status":"ORIGINAL_NPH2016_177_UV_TRAITS_WITH_GBIF_SPECIES_CROSSWALK",
       "original_UV_measured_taxon_rows":len(out),
       "original_UV_pattern_present_source_rows":sum(
           r["source_measured_UV_pattern_present"] for r in out),
       "original_UV_uniform_source_rows":sum(
           1-r["source_measured_UV_pattern_present"] for r in out),
       "S1_verified_source_binomial_rows":sum(
           bool(x["original_S1_author_full_binomial_candidate"]) for x in out),
       "high_confidence_GBIF_mapped_original_UV_source_rows":len(matches),
       "distinct_GBIF_accepted_species_keys":len(eligible_keys),
       "GBIF_match_status_counts":dict(sorted(source_counter.items())),
       "accepted_species_key_with_conflicting_infraspecific_UV_states":conflicts,
       "species_trait_conflicts_never_resolved_by_majority_or_averaging":True,
       "unmatched_source_taxa_not_absence":True,
       "no_native_Bombus_pollinator_or_plant_fitness_claim":True,
       "no_novel_UV_Bombus_sdm_association":True
    }

def source_names():
    import fitz
    blob,_=_fetch(API)
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        file=z.read(MEMBER)
    if hashlib.sha256(file).hexdigest()!=ORIGINAL_TABLE_PDF_SHA256:
        raise ValueError("NO_GO_NPH2016_SOURCE_PDF_SHA256")
    with fitz.open(stream=file,filetype="pdf") as pdf:
        s1={i:pdf[i].get_text("text") for i in range(3,17)}
        s2={i:pdf[i].get_text("text") for i in PAGES}
    traits=parse_source_rows(s2)
    contract=summarize(traits)
    names,_=s1_author_name_index(s1)
    expanded,report=source_match_rows(traits,names)
    if len(expanded)!=177 or report["n_full_author_binomial_lexical_candidates"]!=168:
        raise ValueError("NO_GO_NPH2016_AUTHOR_NAMES_CROSSCHECK")
    return expanded,report

def main():
    original,coverage=source_names()
    names=sorted({x["original_S1_author_full_binomial_candidate"] for x in original
                  if x["original_S1_author_full_binomial_candidate"]})
    if len(names)!=164:
        raise ValueError("NO_GO_2016_SOURCE_UNIQUE_BINOMIALS_CHANGED")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as p:
        response=list(p.map(query_exact_original_name,names))
    tax=dict(zip(names,response))
    rows,receipt=attach_taxonomy(original,tax)
    p=Path("stage49_2016_UV_accepted_taxonomy")
    p.mkdir(exist_ok=True)
    fields=list(rows[0])
    with (p/"nph2016_original_177_UV_trait_GBIF_accepted_taxon_key.csv").open(
         "w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (p/"original_177_UV_accepted_taxon_key_receipt.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("STAGE49_ORIGINAL_177_UV_SPECIES_GBIF_KEYS",
          json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    if receipt["high_confidence_GBIF_mapped_original_UV_source_rows"]<90:
        raise SystemExit("NO_GO_SOURCE_177_TAXONOMY_TOO_FEW_REAL_EXACT_SPECIES_MATCHES")

if __name__=="__main__":
    main()
