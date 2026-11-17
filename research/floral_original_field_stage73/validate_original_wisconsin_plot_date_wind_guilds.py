"""Stage73C original Wisconsin author field-wind × recorded visitors matching.

Source original workbook author bytes Git blob d456ddae... checked upstream.
Analyse SOURCE DATA GRAIN and join fidelity only; NO regression or significance.
Author README advertises "summer 2022", but original Excel date serials suggest
summer 2021 under Excel 1900 date system. Report this unresolved conflict, NEVER
silently attach 2022 day-level weather to the source.

Color is source literature categorical petal_color, NOT spectrometric UV.
Wind is ordinal source Beaufort category, NOT measured continuous wind velocity.
Visitor records are floral visitation events/inflorescences, not known pollen
transfer fitness. Survey missing visits must NOT be imputed as biological zero.
"""
from __future__ import annotations
import argparse,csv,datetime,json
from collections import Counter,defaultdict
from pathlib import Path

from audit_original_wisconsin_wind_visits import (
    download_original_excel,read_xlsx_sparse,table_from_sheet,normalize_key,
    SOURCE_GIT_BLOB_SHA1,SOURCE_BYTES
)

def excel_date_1900(num):
    s=str(num or "").strip()
    try:n=float(s)
    except ValueError:return None
    if n<20000 or n>60000 or int(n)!=n:
        return None
    return (datetime.datetime(1899,12,30)+datetime.timedelta(days=int(n))).date().isoformat()

def join_key(row):
    return tuple(str(row.get(field,"")).strip() for field in ("site","date","plot"))

def strict_nonnegative_number(s):
    try:x=float(str(s).strip())
    except (ValueError,TypeError):return None
    if x<0 or x!=x:return None
    return x

def summarize_field():
    books=read_xlsx_sparse(download_original_excel())
    sheets={name:table_from_sheet(books[name])[1] for name in
            ("plots","plants","visitors","plant_spp_traits","visitor_spp_traits")}
    pts=sheets["plots"];pl=sheets["plants"];vi=sheets["visitors"];traits=sheets["plant_spp_traits"];it=sheets["visitor_spp_traits"]
    pkeys=defaultdict(list)
    for row in pts:pkeys[join_key(row)].append(row)
    duplicate=[k for k,v in pkeys.items() if len(v)>1]
    unique_plots={k:v[0] for k,v in pkeys.items() if len(v)==1 and all(k)}
    sources={"plots":pts,"plants":pl,"visitors":vi}
    diagnostics={}
    for name,rows in sources.items():
        keys=[join_key(r) for r in rows]
        matched=sum(k in unique_plots for k in keys)
        diagnostics[name]={
            "source_rows":len(rows),
            "n_distinct_site_date_plot_key":len(set(keys)),
            "rows_matched_to_unique_original_plot_key":matched,
            "unmatched_or_ambiguous_source_rows":len(rows)-matched,
            "source_empty_site_date_plot":sum(not all(k) for k in keys),
        }
    source_trait_names={normalize_key(r["flower_sp"]) for r in traits if r.get("flower_sp","")}
    source_visitor_trait_names={normalize_key(r["visitor_sp"]) for r in it if r.get("visitor_sp","")}
    visit_status=Counter()
    bees_by_wind=defaultdict(Counter)
    wind_by_site_date=defaultdict(Counter)
    observed_plant_names=set();visited_plant_names=set();observed_visitor_names=set()
    plant_plot_set=defaultdict(set)
    visitor_plot_set=defaultdict(set)
    for k,rec in unique_plots.items():
        w=rec.get("wind","").strip()
        wind_by_site_date[k[:2]][w]+=1
    for r in pl:
        tax=normalize_key(r.get("flower_sp",""))
        observed_plant_names.add(tax)
        if join_key(r) in unique_plots:
            plant_plot_set[join_key(r)].add(tax)
    for r in vi:
        key=join_key(r)
        visitor=normalize_key(r.get("visitor_sp",""))
        target=normalize_key(r.get("flower_sp",""))
        visited_plant_names.add(target);observed_visitor_names.add(visitor)
        if key not in unique_plots:
            visit_status["visitor_rows_without_unique_original_plot_key"]+=1
            continue
        visitor_plot_set[key].add(visitor)
        wind=unique_plots[key].get("wind","").strip()
        if not wind:wind="UNKNOWN"
        count=strict_nonnegative_number(r.get("flower_visits",""))
        if count is None:
            visit_status["visitor_rows_with_missing_or_invalid_inflorescence_visits"]+=1
        else:
            visit_status["visitor_rows_with_numeric_inflorescence_visits"]+=1
            bees_by_wind[wind]["source_inflorescences_visited_reported"]+=count
        c=strict_nonnegative_number(r.get("visitor_no",""))
        if c is None:
            visit_status["visitor_rows_without_numeric_pollinator_individuals"]+=1
        else:
            bees_by_wind[wind]["source_reported_visitor_individuals_sum"]+=c
        bees_by_wind[wind]["source_visitor_rows_with_original_unique_plot"]+=1
        if visitor.startswith("bombus "):
            bees_by_wind[wind]["source_literal_Bombus_genus_name_rows"]+=1
            if c is not None:
                bees_by_wind[wind]["source_literal_Bombus_genus_individuals"]+=c
        if target not in plant_plot_set.get(key,set()):
            visit_status["source_visited_plant_name_not_in_plant_plot_source_list"]+=1
        if target not in source_trait_names:
            visit_status["source_visited_plant_name_not_in_25_literature_trait_names"]+=1
        if visitor not in source_visitor_trait_names:
            visit_status["source_visitor_name_not_in_36_insect_trait_names"]+=1
        if normalize_key(r.get("flower_sp_2","")):
            visit_status["visitor_rows_with_second_visited_flower_name"]+=1
    site_date_wind={f"{k[0]}:{excel_date_1900(k[1]) or k[1]}":
       dict(c) for k,c in sorted(wind_by_site_date.items())}
    n_within_site_date_multiwind=sum(len([w for w,n in c.items() if w and n>0])>=2 for c in wind_by_site_date.values())
    wind_counts=Counter(r.get("wind","") for r in unique_plots.values())
    source_dates=sorted({r.get("date","") for r in pts if r.get("date","")})
    interpreted=[excel_date_1900(x) for x in source_dates]
    year_count=Counter((x or "UNKNOWN")[:4] for x in interpreted)
    original_plants_plot_covered=sum(bool(plant_plot_set.get(k)) for k in unique_plots)
    original_visitors_plot_covered=sum(bool(visitor_plot_set.get(k)) for k in unique_plots)
    report={
        "schema":"stage73c_original_Wisconsin_site_date_plot_wind_visitor_field_gates",
        "original_source_Git_blob_SHA1":SOURCE_GIT_BLOB_SHA1,
        "author_README_says_sampling_2022":True,
        "Excel_1900_date_system_assumed_for_interpretation":True,
        "source_original_distinct_dates_serial":source_dates,
        "original_dates_under_Excel1900":interpreted,
        "original_interpreted_year_counts":dict(year_count),
        "author_README_vs_original_Excel_date_conflict_UNRESOLVED":bool(year_count and set(year_count)!={"2022"}),
        "original_author_visitation_study_geography":"4 Wisconsin sites, same study region",
        "original_source_plots":len(pts),
        "original_source_plant_rows":len(pl),
        "original_source_visitor_rows":len(vi),
        "original_source_plant_trait_species":len(source_trait_names),
        "original_source_insect_trait_labels":len(source_visitor_trait_names),
        "original_duplicate_plot_keys":len(duplicate),
        "original_distinct_plot_keys":len(pkeys),
        "original_unique_complete_site_date_plot_keys":len(unique_plots),
        "source_table_plot_key_join_diagnostics":diagnostics,
        "source_unique_plots_with_any_recorded_flowering_species":original_plants_plot_covered,
        "source_unique_plots_with_any_original_visitor_event":original_visitors_plot_covered,
        "plots_without_source_visitor_rows_are_UNOBSERVED_NOT_TRUE_ZERO":len(unique_plots)-original_visitors_plot_covered,
        "field_plots_by_original_Beaufort_category":dict(wind_counts),
        "source_unique_site_date_groups":len(wind_by_site_date),
        "source_site_date_groups_with_at_least_2_wind_categories":n_within_site_date_multiwind,
        "source_site_date_wind_class_counts":site_date_wind,
        "observed_flowering_plant_name_unique":len(observed_plant_names),
        "visited_flower_plant_name_unique":len(visited_plant_names),
        "visited_plant_name_matched_author_literature_trait_species":len(visited_plant_names & source_trait_names),
        "source_visitor_taxon_names_in_visitor_rows":len(observed_visitor_names),
        "source_visitor_names_matched_original_insect_trait":len(observed_visitor_names & source_visitor_trait_names),
        "source_visitor_join_taxon_coverage_issues":dict(visit_status),
        "source_wind_class_recorded_visitation_counts":{k:dict(v) for k,v in sorted(bees_by_wind.items())},
        "source_literature_categorical_flower_colour_is_UV_reflectance":False,
        "original_visits_are_pollen_effectiveness_or_fitness":False,
        "source_flower_wind_guild_model_fitted":False,
        "source_weather_year_alignment_allowed":False,
        "source_wind_is_observational_not_manipulated":True,
        "independent_study_regions_from_focal_2018_Lesvos":1,
    }
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    a.outdir.mkdir(exist_ok=True,parents=True)
    report=summarize_field()
    (a.outdir/"source_wisconsin_original_plot_visitor_wind_and_date_semantics.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE73C_AUTHOR_SOURCE_WIND_VISITS_ORIGINAL_PLOT_JOIN_DATE_AUDIT",
          json.dumps(report,ensure_ascii=False,sort_keys=True))
    print("SOURCE_DATE_2021_VS_README_2022_UNRESOLVED_NO_EXTERNAL_CLIMATE_NO_EFFECT")
if __name__=="__main__":main()
