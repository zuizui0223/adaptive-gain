#!/usr/bin/env python3
"""Stage113: close original 72 mainland EXPLORATORY source point-gust climate gaps.

Actual original first25+next25 ERA5 MODEL 1991–2020 daily climate at first50
lexical TDWG mainland regions already authenticated SHA. Exactly 33 overlap
the frozen Stage98B 72 contact-free exploration regions. Request ONLY the
remaining 39 original 72 train region representative points, grouped five
site, 3 source decades. Original 37 holdout floral outcomes not read.

This source-matched point gust is NOT full area-weighted region exposure
(Stage109/110/112 do physical sampling). Still useful for larger geographic
first-pass original source botanical reporting-bias diagnostics. NO floral
effects are fitted at this source-only stage. No CDS original hourly 10fg.
"""
from __future__ import annotations
import argparse,csv,io,json,math,sys,time,zipfile,statistics
from pathlib import Path
from collections import Counter,defaultdict

BASE=Path(__file__).resolve().parents[1]
for name in ("floral_macro_stage95","floral_macro_stage97","floral_macro_stage109","floral_macro_stage110"):
    sys.path.insert(0,str(BASE/name))
from original_ERA5_1991_2020_regional_25point_source_probe import (
    source_mainland_regions
)
from original_ERA5_1991_2020_gust_five_mainland_pilot import (
    api_url,parse_decade,climatology,YEARS)
from original_geogrid_public_ERA5_1991_2020_WDC_area_gust import (
    sha256,source_decade_with_bounded_provider_retries
)
from original_public_ERA5_model_34cells_DEL_CAB_landarea import normalize_source_era5_response

SHA_SOURCE_FIRST25="7c98421306466b589b1f80ec97d4ca32ba58e73ba7807f0c2330a7f082fe6b67"
SHA_SOURCE_NEXT25="5e5ee1c325cc85abfb3cfb98a85d9b3faecacd116db9d917eaebdd3a0c453d79"
SHA_MAINLAND72="8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7"
SOURCE_FIRST25_MEMBER="stage95C_true_source_first25_mainland_site_gust_30yr.json"
SOURCE_NEXT25_MEMBER="stage97_real_1991_2020_next25_original_mainland_ERA5_model_gust.json"
SOURCE_TRAIN_MEMBER="stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv"
SOURCE_HOLDOUT_MEMBER="stage98B_holdout_original_mainland_37_UNCHANGED.csv"
GEO_BLOCKS=17
ORIGINAL_MISSING_TRAIN_POINTS=39
ORIGINAL_PRIOR_TRAIN_POINTS=33
ORIGINAL_TOTAL_TRAIN_POINTS=72
BATCH_SITES=5
SOURCE_BATCH_SPACING_SECONDS=68
SOURCE_DECADE_SPACING_SECONDS=12

def exact_geo_and_source_first50(stage94,geo,stage98B,prior25,next25):
    # Stage95's previously independently authenticated Stage94 and original
    # TDWG geo source method refuses blob or region identity changes.
    allsites=source_mainland_regions(stage94,geo)
    if len(allsites)!=125 or len({x["TDWG_L3"] for x in allsites})!=125:
        raise ValueError("STAGE113_SOURCE_125_MAINLAND_ORIGINAL_GEO_CHANGED")
    if sha256(stage98B)!=SHA_MAINLAND72:
        raise ValueError("STAGE113_ORIGINAL_STAGE98B_72_37_SHA_DRIFT")
    with zipfile.ZipFile(stage98B) as z:
        if not {SOURCE_TRAIN_MEMBER,SOURCE_HOLDOUT_MEMBER}<=set(z.namelist()):
            raise ValueError("STAGE113_SOURCE_GEOGRAPHIC_72_37_MEMBER_MISSING")
        train=list(csv.DictReader(io.StringIO(z.read(SOURCE_TRAIN_MEMBER).decode("utf-8-sig"))))
        hold=list(csv.DictReader(io.StringIO(z.read(SOURCE_HOLDOUT_MEMBER).decode("utf-8-sig"))))
    if (len(train),len(hold))!=(72,37) or set(x["TDWG_L3"] for x in train)&set(x["TDWG_L3"] for x in hold):
        raise ValueError("STAGE113_SOURCE_GEOGRAPHIC_72_37_COUNTS_OR_OVERLAP_DRIFT")
    train={r["TDWG_L3"]:r for r in train}
    if len(train)!=72 or len({r["spatial_block_id"] for r in train.values()})!=GEO_BLOCKS:
        raise ValueError("STAGE113_NOT_17_BLOCK_CONTACT_FREE_SOURCE_EXPLORATION")
    by={r["TDWG_L3"]:r for r in allsites}
    for code,item in train.items():
        source=by.get(code)
        if not source or (source["shared_split"]!="exploration"
            or source["TDWG_source_polygon_SHA256"]!=item["polygon_sha256"]
            or source["spatial_block_id"]!=item["spatial_block_id"]
            or item["admission"]!="exploration_contact_free"
            or source["regional_strict_continent_connected_scope"]!="mainland"):
            raise ValueError("STAGE113_HOLDOUT_OR_NONMAINLAND_SOURCE_TAXON_GEO_ADMITTED")
    if sha256(prior25)!=SHA_SOURCE_FIRST25 or sha256(next25)!=SHA_SOURCE_NEXT25:
        raise ValueError("STAGE113_PRIOR_50_ORIGINAL_ERA5_SOURCE_ARTIFACT_SHA_DRIFT")
    with zipfile.ZipFile(prior25) as z:a=json.loads(z.read(SOURCE_FIRST25_MEMBER))
    with zipfile.ZipFile(next25) as z:b=json.loads(z.read(SOURCE_NEXT25_MEMBER))
    first=a["sites"];second=b["regions"]
    if (len(first),len(second))!=(25,25) or (
        [r["TDWG_L3"] for r in first+second]!=[r["TDWG_L3"] for r in allsites[:50]]):
        raise ValueError("STAGE113_ORIGINAL_FIRST50_SOURCE_REGION_ORDER_CHANGED")
    if b["source_prior25_exact_region_codes"]!=[s["TDWG_L3"] for s in first]:
        raise ValueError("STAGE113_SECOND25_SOURCE_PROVENANCE_DRIFT")
    previous={}
    for source in first+second:
        code=source["TDWG_L3"]
        if code in previous:raise ValueError("STAGE113_REPEATED_ORIGINAL_SOURCE_POINT")
        true=by[code]
        if (source["TDWG_source_polygon_SHA256"]!=true["TDWG_source_polygon_SHA256"]
            or abs(float(source["lat"])-true["lat"])>1e-5
            or abs(float(source["lon"])-true["lon"])>1e-5
            or source["source_ERA5_observed_30yr_days"]!=10958):
            raise ValueError("STAGE113_PRIOR_50_SOURCE_POINT_GEOMETRY_OR_CALENDAR_CHANGED")
        previous[code]=source
    matched={code:previous[code] for code in sorted(train) if code in previous}
    missing=[by[code] for code in sorted(set(train)-set(matched))]
    if (len(matched),len(missing))!=(ORIGINAL_PRIOR_TRAIN_POINTS,ORIGINAL_MISSING_TRAIN_POINTS):
        raise ValueError("STAGE113_ORIGINAL_TRAIN33_POINT_39_MISSING_SOURCE_COUNTS_CHANGED")
    if any(row["shared_split"]!="exploration" for row in missing):
        raise ValueError("STAGE113_ATTEMPT_TO_ACQUIRE_HOLDOUT_SOURCE_POINT")
    return matched,missing,train

def returned_source_model_point(requested,frame):
    if not isinstance(frame,dict):raise ValueError("STAGE113_PROVIDER_DAILY_SOURCE_NOT_OBJECT")
    try:
        lat=float(frame["latitude"]);lon=float(frame["longitude"])
    except (KeyError,TypeError,ValueError) as e:
        raise ValueError("STAGE113_SOURCE_RETURNED_COORD_NOT_REPORTED") from None
    if not math.isfinite(lat) or not math.isfinite(lon):
        raise ValueError("STAGE113_SOURCE_ERA5_MODEL_COORD_NOT_FINITE")
    delta_lon=abs((lon-requested["lon"]+180)%360-180)
    if abs(lat-requested["lat"])>.65 or delta_lon>.65:
        raise ValueError("STAGE113_TDWG_REP_POINT_ERA5_MODEL_CELL_TOO_FAR")
    return [lat,lon]

def execute(original_stage94,original_tdwg,original_stage98B,stage95C,stage97,out):
    prior,missing,train=exact_geo_and_source_first50(
        original_stage94,original_tdwg,original_stage98B,stage95C,stage97)
    out.mkdir(parents=True,exist_ok=True)
    results=dict(prior);queries=[];n=0
    for start in range(0,len(missing),BATCH_SITES):
        if start:time.sleep(SOURCE_BATCH_SPACING_SECONDS)
        group=missing[start:start+BATCH_SITES]
        series={r["TDWG_L3"]:[] for r in group}
        coordinates={}
        for i,(y1,y2) in enumerate(YEARS):
            if i:time.sleep(SOURCE_DECADE_SPACING_SECONDS)
            url=api_url(group,f"{y1}-01-01",f"{y2}-12-31")
            raw,source_sha,bytes_=source_decade_with_bounded_provider_retries(url)
            frames=normalize_source_era5_response(raw,len(group))
            if len(frames)!=len(group):
                raise ValueError("STAGE113_SOURCE_ADDITIONAL_TRAIN_BATCH_CARDINALITY_DRIFT")
            queries.append({"source_new_exploration_batch":start//BATCH_SITES,
                "source_original_region_codes":[r["TDWG_L3"] for r in group],
                "source_original_decade_years":f"{y1}-{y2}",
                "source_public_ERA5model_daily_archive_URL":url,
                "source_raw_provider_JSON_SHA256":source_sha,
                "source_raw_original_response_bytes":bytes_,
                "source_is_ERA5_model_daily_NOT_CDS_hourly":True})
            for site,frame in zip(group,frames):
                code=site["TDWG_L3"]
                coord=returned_source_model_point(site,frame)
                if code in coordinates and coordinates[code]!=coord:
                    raise ValueError("STAGE113_SOURCE_ERA5_GRID_POINT_CHANGED_ACROSS_DECADES_"+code)
                coordinates[code]=coord
                series[code].extend(parse_decade(frame,y1,y2))
        completed=[]
        for site in group:
            code=site["TDWG_L3"]
            climate=climatology(series[code])
            if climate["source_ERA5_observed_30yr_days"]!=10958:
                raise ValueError("STAGE113_INCOMPLETE_REAL_1991_2020_DAILY_ERA5_SOURCE")
            item={**site,**climate,"source_actual_model_returned_grid_latlon":coordinates[code],
                "source_ERA5_provider_location_is_original_TDWG_rep_point_NOT_exact_area_mean":True}
            results[code]=item;completed.append(item)
        # Persist independent 3-decade full source climates for each completed
        # batch. If a later transport/quota batch fails, this record is PARTIAL
        # and never called a 72-region complete source frame.
        (out/f"stage113_PARTIAL_NEW_TRAIN_POINT_BATCH_{start//BATCH_SITES:02d}_NOT_72_COMPLETE.json").write_text(
            json.dumps({"status":"PARTIAL_SOURCE_BATCH_NOT_ALL72",
                "fixed_source_original_72_train_region_codes":sorted(train),
                "source_verified_new_batch_30year_point_climates":completed,
                "source_current_batch_raw_JSON_SHA256":queries[-3:],
                "no_global_completed72_claim_from_partial":True},
                sort_keys=True,indent=2)+"\n")
        n+=len(completed)
        print("STAGE113_TRUE_ERA5_MODEL_ADDITIONAL_72_TRAIN_SOURCE_REGION_BATCH",{
              "new_points_complete":n,"original_new_points_required":ORIGINAL_MISSING_TRAIN_POINTS,
              "original_source_blocks":len({r["spatial_block_id"] for r in completed})},flush=True)
    if len(results)!=72 or n!=39 or len(queries)!=24:
        raise ValueError("STAGE113_NOT_COMPLETE_72_SOURCE_MAINLAND_EXPLORATION_DAILY")
    if set(results)!=set(train):
        raise ValueError("STAGE113_NON_EXPLORATION_REGION_ENTERED_SOURCE_72")
    source=[results[code] for code in sorted(results)]
    available=[r["source_primary_fraction_days_daily_gust_strict_above_15_ms"] for r in source
               if r["source_primary_fraction_days_daily_gust_strict_above_15_ms"] is not None]
    receipt={
        "schema":"stage113_exact_72_contactfree_exploration_ERA5_model_1991_2020_30year_POINT_exposures",
        "source_original_stage94_SHA256":"3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833",
        "source_original_stage98B_72_37_SHA256":SHA_MAINLAND72,
        "source_original_first25_archive_SHA256":SHA_SOURCE_FIRST25,
        "source_original_next25_archive_SHA256":SHA_SOURCE_NEXT25,
        "source_first50_existing_33_train_points_reused":len(prior),
        "source_new_39_original_train_points_ERA5_model_30years":n,
        "source_final_72_original_mainland_exploration_gust15_POINT_regions":len(source),
        "source_original17_geographic_blocks":len({r["spatial_block_id"] for r in source}),
        "source_original_37_holdout_floral_outcomes_NOT_read":True,
        "source_previous50_old_nontrain_weather_records_loaded_for_source_lineage_only":True,
        "source_37_holdout_weather_records_NOT_USED_OR_REPORTED":True,
        "source_alphabetic_previous50_source_selection_not_trait_sign_selected":True,
        "source_original_new39_selected_only_from_frozen_geographic_train72":True,
        "source_1991_2020_complete_days_per_site":10958,
        "source_original_API_request_sha256_ledger_for_new39":queries,
        "source_72_area_weighted_gust_NOT_obtained":True,
        "source_real_Public_OpenMeteo_ERA5model_daily_not_CDS_hourly_10fg":True,
        "source_NHM_WFO_AusTraits_Bombus_outcomes_NOT_read":True,
        "source_not_confirmatory_ecological_causal_wind_flower_effect":True,
        "source_72_true_original_model_ERA5_representative_points":source,
        "source_point_gust15_min_excluding_eligibility_NA":min(available) if available else None,
        "source_point_gust15_max_excluding_eligibility_NA":max(available) if available else None,
        "source_point_gust15_nonmissing_original_regions":len(available)}
    (out/"stage113_TRUE_72_original_mainland_ERA5model_1991_2020_point_climate_NO_floral.json").write_text(
          json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("STAGE113_TRUE_NEW_39_72_TRAIN_ERA5MODEL_ORIGINAL_SOURCE_POINT_GUST",json.dumps({
        "old_train_points":len(prior),"new_train_points":n,
        "all_original_source_train_points":len(source),
        "geo_blocks":receipt["source_original17_geographic_blocks"],
        "nonmissing_warmclimate_gust15":len(available),
        "range":[receipt["source_point_gust15_min_excluding_eligibility_NA"],
                 receipt["source_point_gust15_max_excluding_eligibility_NA"]]},
        sort_keys=True),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for arg in ("original-stage94-geo-ZIP","original-TDWG3-geojson",
                "original-stage98B-train72-ZIP","original-stage95C-first25-ZIP",
                "original-stage97-next25-ZIP"):
        p.add_argument("--"+arg,required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    execute(a.original_stage94_geo_ZIP,a.original_TDWG3_geojson,
      a.original_stage98B_train72_ZIP,a.original_stage95C_first25_ZIP,
      a.original_stage97_next25_ZIP,a.outdir)
