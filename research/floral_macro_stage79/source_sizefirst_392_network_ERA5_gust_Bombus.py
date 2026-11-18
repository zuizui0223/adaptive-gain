"""Stage79I: prospective SIZE-FIRST macro strong-gust field source analysis.

Start from ALL 392 original NHM botanical-description petal-width
contrasting EuPPPollNet networks, NOT the earlier 152 hue-diversity-selected
networks. Sample at most 5 per original source study before inspecting bee
outcomes or future gust values, preferring source year/month/location
diversity rather than fitted sign. Region: Europe, no island hypotheses.

ERA5 daily max 10m gust 15 m/s exceedance, source study-year visited months,
time/coordinates not actual bee landing instant. True original species-ranked
Bombus/other bee visits reconstructed after source frame frozen.
Re-use prior validated null-information, study-FE WLS gate (not causal SEM).
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage78"))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from source_era5_strong_gust_visual_Bombus_macro import (
    build_requests,retrieve_strong_gusts,aggregate_exposure
)
from petal_width_vs_era5_strong_gust_real_Bombus_network_gate import (
    csv_records,strict_bee_records,within_network_null_score,
    descriptive_size_gust_relationship
)

SOURCE_FIELD_SHA="948ac0ecbcfc9b8a2e810753748a5436d998cd586574ea185c6da5db08cbce53"
MAX_PER_STUDY=5
EXPECTED_PRE_WIDTH_NET=392
MIN_PRE_SOURCE_STUDIES=30
EXCLUDE_UNRESOLVED_JANUARY=True

def verified_site(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_FIELD_SHA:
        raise ValueError("STAGE79I_ORIGINAL_FIELD_NETWORK_SOURCE_SHA_CHANGED")
    result=csv_records(path)
    if len(result)!=1864 or len({r["Study_id"] for r in result})!=54:
        raise ValueError("STAGE79I_ORIGINAL_NETWORK_DENOMINATOR_CHANGED")
    return result

def study_grid_signature(r):
    # Used ONLY for source site selection independent of bee outcome and
    # unobserved strong gust. This is a coarse objective heuristic, NOT
    # the actual ERA5 returned grid provenance.
    return (r["Year"],round(float(r["lat"])*4)/4,
            round(float(r["lon"])*4)/4,
            tuple(r["original_visited_months"]))

def build_size_first_frame(traitrows,site):
    sites={(r["Study_id"],r["Network_id"],r["Year"]):r for r in site}
    visits=defaultdict(list)
    for r in traitrows:
        key=(r["Study_id"],r["Network_id"],r["Year"])
        val=str(r.get("source_petal_max_width_cm") or "")
        if not val:continue
        size=float(val)
        if not math.isfinite(size) or not 0<size<150:
            raise ValueError("STAGE79I_ORIGINAL_SIZE_FIELD_INVALID")
        visits[key].append((r["original_plant_literal_accepted_name"].casefold().strip(),size))
    original={
        k:plants for k,plants in visits.items()
        if len({name for name,w in plants})>=2 and len({w for name,w in plants})>=2}
    if len(original)!=EXPECTED_PRE_WIDTH_NET:
        raise ValueError("STAGE79I_SOURCE_392_SIZE_CONTRAST_NETWORKS_CHANGED_"+str(len(original)))
    excluded=Counter()
    pre=[]
    for k,plants in sorted(original.items()):
        source=sites.get(k)
        if source is None:
            excluded["SOURCE_SITE_WITHOUT_VISIT_NETWORK"]+=1
            continue
        if not source["Latitude_original"] or not source["Longitude_original"]:
            excluded["SOURCE_MULTI_COORDINATE_UNRESOLVED"]+=1
            continue
        try:
            year=int(k[2])
            lat=float(source["Latitude_original"])
            lon=float(source["Longitude_original"])
            months=sorted({int(x) for x in source["source_observed_visit_months"].split(",") if x})
        except ValueError:
            excluded["SOURCE_YEAR_MONTH_OR_COORDINATE_INVALID"]+=1;continue
        if not 1950<=year<=2025 or not months or any(m<1 or m>12 for m in months):
            excluded["ORIGINAL_DATE_YEAR_OR_MONTH_INVALID"]+=1;continue
        if EXCLUDE_UNRESOLVED_JANUARY:
            before=len(months)
            months=[m for m in months if m!=1]
            if len(months)<before:excluded["SOURCE_JANUARY_MONTH_UNRESOLVED_REMOVED"]+=1
            if not months:
                excluded["SOURCE_JANUARY_ONLY_CALENDAR_MAY_BE_PLACEHOLDER"]+=1;continue
        distinct_genera=len({s.split()[0] for s,w in plants})
        pre.append({
          "Study_id":k[0],"Network_id":k[1],"Year":k[2],
          "lat":lat,"lon":lon,
          "original_visited_months":months,
          "original_source_petal_width_species":len(plants),
          "original_source_petal_width_genera":distinct_genera,
          "original_source_distinct_width_values":len({w for s,w in plants}),
          "pre_selected_without_original_Bombus_or_ERA5_gust_outcome":True,
        })
    bystudy=defaultdict(list)
    for row in sorted(pre,key=lambda z:(z["Study_id"],z["Year"],z["Network_id"])):
        bystudy[row["Study_id"]].append(row)
    selected=[]
    for study,rows in sorted(bystudy.items()):
        selected_study=[]
        seen=set()
        for row in rows:
            key=study_grid_signature(row)
            if key in seen:continue
            selected_study.append(row);seen.add(key)
            if len(selected_study)>=MAX_PER_STUDY:break
        if len(selected_study)<MAX_PER_STUDY:
            used={(x["Study_id"],x["Network_id"],x["Year"]) for x in selected_study}
            for row in rows:
                k=(row["Study_id"],row["Network_id"],row["Year"])
                if k in used:continue
                selected_study.append(row);used.add(k)
                if len(selected_study)>=MAX_PER_STUDY:break
        selected.extend(selected_study)
    if len(bystudy)<MIN_PRE_SOURCE_STUDIES or len(selected)<90:
        raise ValueError("STAGE79I_FULL_SIZE_BASE_NOT_ENOUGH_SOURCE_STUDIES_OR_NETWORKS")
    return selected,{
       "original_all_networks_with_two_distinct_botanical_petal_widths":len(original),
       "original_number_of_studies_before_gust_or_bee_exposure":len(bystudy),
       "original_before_weather_verified_coordinates_months":len(pre),
       "pre_source_exclusions":dict(excluded),
       "max_source_networks_per_study_outcome_blind":MAX_PER_STUDY,
       "frozen_source_site_networks":len(selected),
       "frozen_source_studies":len({r["Study_id"] for r in selected}),
       "selection_prefer_distinct_geographic_climate_cells_from_original_coords_NOT_outcome":True,
       "excluded_unverified_January_weather_placeholder_month":EXCLUDE_UNRESOLVED_JANUARY,
       "not_original_complete_392_study_networks":True,
       "source_plant_width_not_true_visual_display":True,
       "source_visiting_bee_outcome_not_used_in_selection":True,
    }

def run(traits,sites,out):
    frozen,selection=build_size_first_frame(traits,sites)
    requests=build_requests(frozen)
    print("STAGE79I_SIZE_FIRST_FROZEN_ORIGINAL_NETWORKS",
          json.dumps(selection,sort_keys=True),
          "ERA5_requested_batches",len(requests),flush=True)
    cache=out/"original_ERA5_source_year_month_batches"
    weather,receipts=retrieve_strong_gusts(requests,cache)
    exposure=aggregate_exposure(frozen,weather)
    # Only after botanical traits and source meteorology are frozen do
    # we read the original 623,476 true recorded visitor taxon rows.
    chosen={(r["Study_id"],r["Network_id"],r["Year"]) for r in exposure}
    widths=defaultdict(list)
    for r in traits:
        k=(r["Study_id"],r["Network_id"],r["Year"])
        if k not in chosen:continue
        val=r.get("source_petal_max_width_cm","")
        if val:
            widths[k].append((r["original_plant_literal_accepted_name"].casefold().strip(),float(val)))
    recorded=strict_bee_records(chosen)
    source_scores=[];statuses=Counter()
    for r in exposure:
        k=(r["Study_id"],r["Network_id"],r["Year"])
        one,reason=within_network_null_score(k,widths[k],recorded,r)
        statuses[reason]+=1
        if one:source_scores.append(one)
    support=descriptive_size_gust_relationship(source_scores)
    return {
       "schema":"stage79i_europe_original_size_first_gust15_Bombus_macro_conditional_network_score",
       "source_original_PRE_ERA5_392_width_network_selection":selection,
       "source_original_ERA5_request_batches":len(receipts),
       "original_ERA5_source_API_provenance":receipts,
       "source_real_ERA5_full_network_exposures":exposure,
       "source_actual_Bombus_conditioning_status":dict(statuses),
       "source_study_cluster_strong_gust_width_inference_gate":support,
       "source_original_ERA5_network_null_score_rows":source_scores,
       "source_unknown_markings_and_FCC_NOT_used_as_negative":True,
       "source_no_independently_measured_same_field_UV_or_scent":True,
       "source_plant_shape_selection_outcome_blind":True,
       "original_ERA5_gust15_not_actual_bee_visit_hour_or_VOC_plume":True,
       "no_plant_evolutionary_selection_or_causal_Cue_order_claim":True,
    }

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--source-original-plant-width",type=Path,required=True)
    a.add_argument("--source-original-1864-climate-sites",type=Path,required=True)
    a.add_argument("--outdir",type=Path,required=True)
    q=a.parse_args();q.outdir.mkdir(parents=True,exist_ok=True)
    data=run(csv_records(q.source_original_plant_width),verified_site(q.source_original_1864_climate_sites),q.outdir)
    def save(name,rows):
        if not rows:return
        with (q.outdir/name).open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    save("source_original_sizefirst_ERA5_gust15_exposures.csv",data.pop("source_real_ERA5_full_network_exposures"))
    save("source_original_sizefirst_Bombus_width_nullscores.csv",data.pop("source_original_ERA5_network_null_score_rows"))
    (q.outdir/"source_original_sizefirst_ERA5_gust_vs_Bombus_width_preguild_receipt.json").write_text(
        json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE79I_ORIGINAL_SIZE_FIRST_GUST_BOMBUS_SOURCE_MACRO",
          json.dumps({k:v for k,v in data.items() if k!="original_ERA5_source_API_provenance"},
                     sort_keys=True),flush=True)
if __name__=="__main__":main()
