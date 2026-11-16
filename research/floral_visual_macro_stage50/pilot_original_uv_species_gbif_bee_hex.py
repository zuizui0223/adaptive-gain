"""Stage50: real GBIF plant-occurrence -> author-authenticated global bee HEX pilot.

Input botanical phenotype: independently verified original published UV
pattern categories, 262 accepted species / 230 direct UV-pattern labels.
A *predeclared, source/study/phenotype-balanced 60-species PILOT* is chosen
by deterministic GBIF accepted-key hash BEFORE observing occurrence data.

Sampling from GBIF's occurrence/search is bounded: 2 separated 150-row
pages per species, strictly NOT a complete native species distribution.
Results are coverage/measurement diagnostics; *no ecological UV×bee
coefficient or adaptation claim*. The original source HEX shapefile and
3,370-bee author filter from Stages46–47 are independently reproduced.
All original GBIF points are consumed transiently, not redistributed.

Important: a species-wide UV state observed in one study population is
not a validated phenotype for every GBIF occurrence of the species.
"""
from __future__ import annotations

from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE=Path(__file__).resolve()
ROOT=HERE.parents[1]
for folder in ("floral_visual_macro_stage46","floral_visual_macro_stage47"):
    sys.path.insert(0,str(ROOT/folder))

from align_uv_study_sites_to_bee_hex import (
    load_authenticated_shape_sources,
    polygons_from_original_shapefile,
    matching_original_hex
)
from author_tree_filtered_bombus import (
    fetch_author_small_sources,source_parameter_and_taxa,
    trim_original_bee_matrix,materialize_join
)
from derive_bombus_hex_prediction import _get_model_source

SOURCE_UV_STATES={"0","1"}
PILOT_PER_STUDY_PATTERN=15
PILOT_TOTAL=60
PAGE_LIMIT=150
MAX_GBIF_SEARCH_WINDOW=100000
START_YEAR=2000
END_YEAR=2026
MAX_ACCEPTED_UNCERTAINTY_METERS=10000
SOURCE_STUDIES={
    "2016":"10.1111/nph.13921",
    "2021":"10.3389/fpls.2021.618028",
}
GBIF_URL="https://api.gbif.org/v1/occurrence/search"
MAX_RESPONSE_BYTES=2_400_000
MAX_WORKERS=3
# Planned before source query: do not select using ecological outcomes.
SELECTION_SALT="stage50-fixed-preoccurrence-20261116-UV-geography"


def read_verified_source_species(path):
    with Path(path).open(encoding="utf8",newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=262:
        raise ValueError("NO_GO_EXPECTED_ORIGINAL_262_GBIF_SOURCE_SPECIES")
    keys=[r.get("gbif_accepted_species_key","") for r in rows]
    if len(set(keys))!=262 or not all(k.isdigit() for k in keys):
        raise ValueError("NO_GO_SOURCE_262_TAXONOMY_NOT_UNIQUE_ACCEPTED")
    state=Counter(r.get("source_measured_UV_spatial_pattern_or_missing","")
                  for r in rows)
    if state!={"0":129,"1":101,"":32}:
        raise ValueError("NO_GO_262_ORIGINAL_UV_STATUS_COUNTS")
    if not all(r.get("Bee_suitability_at_source_species_range")=="NOT_MODELLED"
               for r in rows):
        raise ValueError("NO_GO_ALREADY_MODELED_SOURCE_INPUT_DIFFERENT")
    return rows


def balanced_preoccurrence_sample(rows,n=PILOT_PER_STUDY_PATTERN):
    """One target per author study × UV phenotype; stable GBIF-key hash."""
    output=[]
    for study,doi in sorted(SOURCE_STUDIES.items()):
        for state in sorted(SOURCE_UV_STATES):
            elig=[r for r in rows
                  if state==r["source_measured_UV_spatial_pattern_or_missing"]
                  and doi in r["source_study_DOIs"].split("|")
                  # Each accepted key has a single prior study assignment
                  # in this two-primary-UV-source frame.
                  ]
            ranked=sorted(elig,key=lambda r:(
                hashlib.sha256(
                    (SELECTION_SALT+"|"+r["gbif_accepted_species_key"]).encode()
                ).hexdigest(),r["gbif_accepted_species_key"]))
            if len(ranked)<n:
                raise ValueError("NO_GO_FEWER_AUTHENTIC_SOURCE_SPECIES_THAN_PILOT")
            output.extend({
                "taxon_key":int(r["gbif_accepted_species_key"]),
                "source_primary_study":study,
                "UV_pattern_source_binary":int(state),
                "source_study_DOIs":r["source_study_DOIs"],
                "source_taxon_name":r["source_taxon_aliases"],
                "selection_rank_in_study_pattern":i+1,
            } for i,r in enumerate(ranked[:n]))
    if len(output)!=4*n or len({r["taxon_key"] for r in output})!=4*n:
        raise ValueError("NO_GO_PILOT_SOURCE_STUDY_TAXON_COLLISION")
    return output


def _request_json(args):
    url=GBIF_URL+"?"+urllib.parse.urlencode(args)
    if not url.startswith("https://api.gbif.org/v1/occurrence/search?"):
        raise ValueError("NO_GO_WRONG_GBIF_SOURCE_ENDPOINT")
    last=None
    for attempt in range(4):
        req=urllib.request.Request(url,headers={
            "User-Agent":"adaptive-gain-stage50-published-UV-source-bee-grid-pilot/2026",
            "Accept":"application/json"
        })
        try:
            with urllib.request.urlopen(req,timeout=35) as response:
                body=response.read(MAX_RESPONSE_BYTES+1)
            if len(body)>MAX_RESPONSE_BYTES:
                raise ValueError("NO_GO_GBIF_SOURCE_RESPONSE_OVERSIZED")
            data=json.loads(body.decode("utf8"))
            if not isinstance(data,dict) or not isinstance(data.get("count"),int) or (
                not isinstance(data.get("results"),list)):
                raise ValueError("NO_GO_GBIF_SOURCE_JSON_RESPONSE_INCOMPLETE")
            return data
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as e:
            last=e
            code=e.code if isinstance(e,urllib.error.HTTPError) else 0
            if (code not in (0,429,500,502,503,504) or attempt==3):
                raise
            time.sleep(1.2*(attempt+1))
    raise ValueError("NO_GO_GBIF_SOURCE_REQUEST_UNAVAILABLE "+str(last))


def fixed_page_offsets(count,limit=PAGE_LIMIT):
    """At most two non-overlapping fixed API windows; not a random sample."""
    if not isinstance(count,int) or count<0:
        raise ValueError("NO_GO_GBIF_TOTAL_COUNT_NOT_NONNEGATIVE_INTEGER")
    if limit<1 or limit>300:
        raise ValueError("NO_GO_GBIF_PAGE_LIMIT_NOT_ALLOWED")
    available=min(count,MAX_GBIF_SEARCH_WINDOW)
    if available<=limit:
        return [0] if available else []
    # select original first and distant index-window page; no false full-range
    # assertion when total>100,000 GBIF search max.
    nextoffset=available-limit
    return sorted({0,nextoffset})


def retrieve_plant_occurrence_pilot(taxon):
    key=taxon["taxon_key"]
    q={
       "taxonKey":key,
       "year":f"{START_YEAR},{END_YEAR}",
       "occurrenceStatus":"PRESENT",
       "hasCoordinate":"true",
       "hasGeospatialIssue":"false",
       "limit":PAGE_LIMIT,
    }
    base=_request_json({**q,"offset":0})
    count=base["count"]
    offsets=fixed_page_offsets(count)
    records=base["results"] if count else []
    for offset in offsets[1:]:
        nextpayload=_request_json({**q,"offset":offset})
        if nextpayload["count"]!=count:
            raise ValueError("NO_GO_GBIF_OCCURRENCE_TOTAL_DRIFT_ACROSS_PAGES")
        records+=nextpayload["results"]
    observations={}
    counts=Counter()
    for rec in records:
        rid=rec.get("key")
        if not isinstance(rid,int):
            counts["no_GBIF_record_id"]+=1
            continue
        if rid in observations:
            counts["duplicate_page_record_ids"]+=1
            continue
        observations[rid]=rec
    # No original records in persistable output: return transient dicts
    return {
      "source_gbif_accepted_species_key":key,
      "source_gbif_index_count_after_query_filters":count,
      "gbif_query_limit":PAGE_LIMIT,
      "gbif_requested_offsets":offsets,
      "source_search_100000_cap_truncated":count>MAX_GBIF_SEARCH_WINDOW,
      "n_source_records_fetched_deduplicated":len(observations),
      "records":list(observations.values()),
      "fetch_duplicate_or_id_issues":dict(counts),
      "not_random_sample_or_complete_native_range":True,
      "query_period":f"{START_YEAR}-{END_YEAR}",
      "query_filters":"hasCoordinate=true;hasGeospatialIssue=false;occurrenceStatus=PRESENT",
    }


def _is_introduction(text):
    return any(word in str(text or "").upper() for word in (
       "INTRODUCED","NATURALISED","NATURALIZED","INVASIVE","CULTIVATED","MANAGED"
    ))


def aggregate_plant_bee_exposure(taxon,gbif_source,names,tree,transform,bee_cells):
    """Record-only coverage diagnostics, equal-weight unique eligible cells."""
    records=gbif_source["records"]
    counts=Counter()
    cells=Counter()
    countries=set()
    all_lat=[]
    used_lat=[]
    examined=Counter()
    n_source_records=len(records)
    for r in records:
        lat=r.get("decimalLatitude");lon=r.get("decimalLongitude")
        if not isinstance(lat,(int,float)) or not isinstance(lon,(int,float)):
            counts["missing_coordinate"]+=1;continue
        lat=float(lat);lon=float(lon)
        if not (-90<=lat<=90 and -180<=lon<=180) or (
           not math.isfinite(lat) or not math.isfinite(lon)):
            counts["invalid_coordinates"]+=1;continue
        all_lat.append(lat)
        # Must match *species-level* key in GBIF taxonomy, not genus-only.
        if r.get("speciesKey")!=taxon["taxon_key"]:
            counts["gbif_species_key_mismatch"]+=1;continue
        if _is_introduction(r.get("establishmentMeans")):
            counts["explicitly_introduced_or_managed"]+=1;continue
        uncertainty=r.get("coordinateUncertaintyInMeters")
        if uncertainty is None:
            counts["missing_uncertainty_not_quality_verified"]+=1;continue
        if not isinstance(uncertainty,(int,float)) or not math.isfinite(float(uncertainty)):
            counts["nonfinite_uncertainty"]+=1;continue
        if uncertainty<0 or uncertainty>MAX_ACCEPTED_UNCERTAINTY_METERS:
            counts["uncertainty_outside_10km"]+=1;continue
        matches=matching_original_hex(lon,lat,names,tree,transform)
        if len(matches)!=1:
            counts["outside_or_on_source_hex_boundary"]+=1;continue
        cell=matches[0]
        row=bee_cells.get(cell)
        if row is None:
            raise ValueError("NO_GO_PLANT_POINT_HEX_NOT_IN_AUTHENTIC_SOURCE_BEE_GRID")
        counts["quality_qualified_and_assigned"]+=1
        if r.get("country"):
            countries.add(str(r["country"]))
        if row["eligibility"]!="AUTHOR_TREE_AND_PA_CELL_CUTOFF":
            counts["outside_original_bee_model_eligibility_UNKNOWN"]+=1
            continue
        richness=row["n_source_tree_and_pa_cutoff_Bombus_taxa"]
        allbee=row["n_source_tree_and_pa_cutoff_all_bee_taxa"]
        if not isinstance(richness,int) or not isinstance(allbee,int):
            raise ValueError("NO_GO_MODEL_ELIGIBLE_HEX_HAS_NULL_BEE_MODEL")
        cells[cell]+=1
        used_lat.append(lat)
        counts["eligible_bee_model_plant_records"]+=1
        examined[cell]=(richness,allbee)
    retained=[examined[k] for k in sorted(cells)]
    # Two estimands carefully distinguished:
    #   a cell-equal survey proxy; a sampled-GBIF-record-weighted proxy.
    # Both are descriptive sample exposures, not native range suitability.
    exposure_b=(sum(x[0] for x in retained)/len(retained)) if retained else None
    exposure_all=(sum(x[1] for x in retained)/len(retained)) if retained else None
    n_eligible=sum(cells.values())
    exposure_record=(sum(cells[k]*examined[k][0] for k in cells)/n_eligible
                     if n_eligible else None)
    return {
       "gbif_accepted_species_key":taxon["taxon_key"],
       "primary_original_UV_study":taxon["source_primary_study"],
       "UV_pattern_direct_source_binary":taxon["UV_pattern_source_binary"],
       "source_literal_taxon_alias":taxon["source_taxon_name"],
       "precommitted_pilot_selection_rank":taxon["selection_rank_in_study_pattern"],
       "original_gbif_filtered_index_count":gbif_source[
           "source_gbif_index_count_after_query_filters"],
       "source_records_retrieved_unique":n_source_records,
       "source_search_offset_pages":gbif_source["gbif_requested_offsets"],
       "source_search_100k_limit_truncated":gbif_source["source_search_100000_cap_truncated"],
       "n_eligible_model_source_occurrence_records":n_eligible,
       "n_eligible_source_model_cells_with_GBIF_plant_points":len(cells),
       "modelled_Bombus_taxa_equal_visited_HEX_cell_mean_or_null":exposure_b,
       "modelled_all_bee_taxa_equal_visited_HEX_cell_mean_or_null":exposure_all,
       "modelled_Bombus_taxa_record_weighted_mean_or_null":exposure_record,
       "source_record_quality_counts":dict(sorted(counts.items())),
       "n_source_record_countries_retained":len(countries),
       "source_record_country_codes":sorted(countries),
       "sampled_GBIF_latitude_min_max":(
           [min(all_lat),max(all_lat)] if all_lat else None),
       "n_no_true_native_range_classification":n_eligible,
       "not_a_taxon_rangewide_nativity_or_pollination_service":True,
       "not_a_Bombus_versus_UV_inferential_model":True,
    }


def summary(rows):
    if len(rows)!=PILOT_TOTAL:
        raise ValueError("NO_GO_PILOT_NOT_60_PRECOMMITTED_SPECIES")
    group=Counter((r["primary_original_UV_study"],
                   r["UV_pattern_direct_source_binary"]) for r in rows)
    if set(group.values())!={PILOT_PER_STUDY_PATTERN} or len(group)!=4:
        raise ValueError("NO_GO_UNBALANCED_ORIGINAL_STUDY_PATTERN_SAMPLE")
    viable=[r for r in rows if r["n_eligible_model_source_occurrence_records"]>=15
            and r["n_eligible_source_model_cells_with_GBIF_plant_points"]>=3]
    descriptives=[]
    for study in sorted(SOURCE_STUDIES):
      for pattern in (0,1):
        sub=[r for r in viable if r["primary_original_UV_study"]==study
             and r["UV_pattern_direct_source_binary"]==pattern]
        descriptives.append({
          "source_article_year":study,
          "source_pattern_binary":pattern,
          "n_species_with_at_least_15_quality_records_and_3_model_cells":len(sub),
          "pilot_species_equal_mean_source_modelled_Bombus_taxa":(
              sum(r["modelled_Bombus_taxa_equal_visited_HEX_cell_mean_or_null"]
                  for r in sub)/len(sub) if sub else None),
          "pilot_species_equal_mean_source_modelled_all_bee_taxa":(
              sum(r["modelled_all_bee_taxa_equal_visited_HEX_cell_mean_or_null"]
                  for r in sub)/len(sub) if sub else None),
          "not_spatially_blocked_climate_phylogeny_or_effort_controlled":True
        })
    return {
      "status":"SOURCE_AUTHENTIC_60_LITERATURE_UV_SPECIES_GBIF_TO_BEE_HEX_FEASIBILITY",
      "precommitted_species_balance":{
         f"{k[0]}_UVpattern{k[1]}":v for k,v in sorted(group.items())
      },
      "number_original_published_UV_species_pilot":len(rows),
      "n_pilot_species_with_any_source_model_eligible_records":sum(
         r["n_eligible_model_source_occurrence_records"]>0 for r in rows),
      "n_pilot_species_with_at_least_3_covered_cells_and_15_records":len(viable),
      "n_species_1990_2026_GBIF_zero_result":sum(
         r["original_gbif_filtered_index_count"]==0 for r in rows),
      "n_records_retrieved_total":sum(r["source_records_retrieved_unique"] for r in rows),
      "n_model_eligible_plant_records_after_quality":sum(
         r["n_eligible_model_source_occurrence_records"] for r in rows),
      "n_species_wide_GBIF_100k_cap_exceeded":sum(
         r["source_search_100k_limit_truncated"] for r in rows),
      "descriptive_study_by_source_pattern":descriptives,
      "source_interpretation":"GBIF bounded-page indexed observed records sampled at two offsets, not true native range or independent random species occurrence sampling.",
      "source_bee_model":"Laborieux et al 2026 original 3370-taxon author tree/pa_cutoff=5 model",
      "no_source_study_taxon_measured_site_inferred_from_GBIF":True,
      "no_null_bee_grid_as_true_zero":True,
      "no_globally_valid_UV_Bombus_statistical_significance_claim":True,
      "no_direct_visual_information_use_or_plant_seed_fitness":True,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--accepted-source-csv",required=True)
    args=ap.parse_args()
    source=read_verified_source_species(args.accepted_source_csv)
    chosen=balanced_preoccurrence_sample(source)
    # Read original source grid and 3370-bee source R/phylogeny controls.
    members,centroids,source_hex=load_authenticated_shape_sources()
    names,tree,transform,geo_info=polygons_from_original_shapefile(members,centroids)
    script,author_tree=fetch_author_small_sources()
    param,names_phylo=source_parameter_and_taxa(script,author_tree)
    matrix=_get_model_source()
    filtered,retained,shared=trim_original_bee_matrix(
        matrix,names_phylo,param["pa_cutoff"])
    if filtered["source_taxa_after_tree_and_cell_cutoff"]!=3370:
        raise ValueError("NO_GO_PUBLISHED_3370_ORIGINAL_AUTHOR_SOURCE_FILTER")
    if filtered["source_Bombus_species_after_tree_cell_cutoff"]!=133:
        raise ValueError("NO_GO_PUBLISHED_BOMBUS_SOURCE_FILTER")
    model_rows=materialize_join(retained,centroids)
    model={x["source_siteid"]:x for x in model_rows}
    if len(model)!=10242:
        raise ValueError("NO_GO_BEE_SOURCE_POLYGON_COUNT")
    # API requests can finish in any order, but output keeps frozen sample order.
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        gbif_sources=list(pool.map(retrieve_plant_occurrence_pilot,chosen))
    results=[
        aggregate_plant_bee_exposure(taxon,observed,names,tree,transform,model)
        for taxon,observed in zip(chosen,gbif_sources)
    ]
    receipt=summary(results)
    receipt["source_original_bee_hex_count"]=len(model)
    receipt["source_author_eligible_bee_hex_count"]=len(retained)
    receipt["source_original_bee_model_Bombus_names"]=133
    receipt["source_original_bee_model_total_names"]=3370
    receipt["source_original_262_species_count"]=len(source)
    receipt["sampled_GBIF_occurrence_search_limit"]=PAGE_LIMIT
    receipt["sampled_GBIF_occurrence_search_year_start"]=START_YEAR
    receipt["sampled_GBIF_occurrence_search_year_end"]=END_YEAR
    receipt["registered_selection_salt"]=SELECTION_SALT
    folder=Path("stage50_original_plant_bee_hex_pilot")
    folder.mkdir(exist_ok=True)
    with (folder/"60_source_UV_plants_GBIF_record_sampling_x_original_Bombus_hex.csv").open(
        "w",encoding="utf8",newline="") as h:
        flat=[]
        for q in results:
            r={key:(json.dumps(v,ensure_ascii=False,sort_keys=True)
                    if isinstance(v,(list,dict)) else v) for key,v in q.items()}
            flat.append(r)
        w=csv.DictWriter(h,fieldnames=list(flat[0]))
        w.writeheader();w.writerows(flat)
    (folder/"precommitted_pilot_source_exposure_receipt.json").write_text(
        json.dumps(receipt,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE50_REAL_GBIF_OCCURRENCES_TO_ORIGINAL_BEE_HEX",json.dumps(
        receipt,ensure_ascii=False,sort_keys=True,allow_nan=False))
    print("STAGE50_NO_NATIVE_SPECIES_DISTRIBUTION_OR_UV_BOMBUS_CAUSAL_FIT")

if __name__=="__main__":
    main()
