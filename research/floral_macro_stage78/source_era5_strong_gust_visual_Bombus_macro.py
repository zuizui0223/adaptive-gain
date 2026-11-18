"""Stage78B: MACRO original strong-GUST extremes × floral visual × Bombus.

Retain original NHM59k botanical TEXT × corrected EuPPollNet 54 study × 1864
field networks, NO islands, NO photos and NO pseudo UV patterns. Freeze the
424 networks with contrasting explicitly reported floral hue states BEFORE
examining guild outcome. Study-balanced source subsample up to four networks
per original study, chosen solely by source field study/network identifiers.

For 2010-2021 etc original *study years* retrieve original ERA5 reanalysis
daily maximum 10m GUST via public Open-Meteo historical archive. Model strictly
ERA5, GMT, m/s, and no downscaling. Match survey-month windows, NOT actual
bee visitation hours. User's STRONG WIND modification:
 primary: fraction of observed-visit-calendar-month DAYS with ERA5 daily
         max gust >=15 m/s
 sensitivity: >=10, >=20, upper 5th percentile daily gust, daily max
             sustained >=8 m/s.
All thresholds pre-specified before opening Bombus outcome, NONE chosen for
statistical significance. ERA5 grid is coarse 0.25 degree and gust is
parameterized, not a flower-local wind/microturbulence or odor plume.

Conditional model is OBSERVATIONAL, not a causal path SEM. Source visual
metric is positive reported hue-family composition of visited plants,
not measured receptor-specific visual signal or guide geometry.
"""
from __future__ import annotations
import argparse,csv,datetime,hashlib,json,math,sys,time,urllib.parse
from collections import Counter,defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage77"))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from source_observational_visual_wind_climate_Bombus_piecewise import (
    build_original_positive_visual_networks,CLIM
)
from probe_original_era5_strong_gusts import (
    API,original_api,STAGE77_SHA
)

PIN={
 "nhm":"b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a",
 "plant_network":"475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617",
 "sites":STAGE77_SHA,
}
MAX_NETWORKS_PER_STUDY=4
MAX_SOURCE_LOCATIONS_PER_REQUEST=7
MAX_SOURCE_REQUESTS=280
GUST_THRESHOLDS=(10,15,20)
GUST_MAIN_THRESHOLD=15
SECONDARY_SUSTAINED_THRESHOLD=8
DAILY_VARS=("wind_gusts_10m_max","wind_speed_10m_max",
            "temperature_2m_mean","precipitation_sum","shortwave_radiation_sum")
MIN_MODEL_STUDIES=15
MIN_MODEL_NETWORKS=70

def verified_csv(path,want):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=want:
        raise ValueError("STAGE78B_PREVIOUS_SOURCE_ARTIFACT_SHA_MISMATCH")
    with Path(path).open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def pre_bombus_strong_gust_sample(nhm,plant,site):
    visual,meta=build_original_positive_visual_networks(nhm,plant)
    if meta["original_network_keys_with_two_DISTINCT_reported_hue_states"]!=424:
        raise ValueError("STAGE78B_PREOUTCOME_424_SOURCE_VISUAL_FRAME_CHANGED")
    site_by_key={(r["Study_id"],r["Network_id"],r["Year"]):r for r in site}
    eligible=visual.loc[visual.n_distinct_reported_hue_families>=2].copy()
    if len(eligible)!=424 or eligible.Study_id.nunique()!=43:
        raise ValueError("STAGE78B_PREOUTCOME_424_NETWORKS_43_STUDIES_CHANGED")
    frozen=[]
    excluded=Counter()
    for _,r in eligible.iterrows():
        k=(str(r.Study_id),str(r.Network_id),str(r.Year))
        original=site_by_key.get(k)
        if original is None:
            raise ValueError("STAGE78B_ORIGINAL_VISUAL_NETWORK_MISSING_TRUE_FIELD_STUDY")
        la=original.get("Latitude_original","")
        lo=original.get("Longitude_original","")
        months=original.get("source_observed_visit_months","")
        if not la or not lo:
            excluded["ORIGINAL_NON_UNIQUE_SITE_COORDINATE"]+=1
            continue
        try:
            y=int(r.Year)
            lat=float(la);lon=float(lo)
            mos=sorted(set(int(z) for z in months.split(",") if z))
        except (ValueError,TypeError):
            excluded["ORIGINAL_SOURCE_SITE_YEAR_OR_MONTH_INVALID"]+=1
            continue
        if y<1940 or y>2025 or not mos or any(not 1<=m<=12 for m in mos):
            excluded["ORIGINAL_SOURCE_YEAR_MONTH_OUT_OF_ERA5_RANGE"]+=1
            continue
        frozen.append({
          "Study_id":str(r.Study_id),"Network_id":str(r.Network_id),
          "Year":str(r.Year),"lat":lat,"lon":lon,
          "original_visited_months":mos,
          "source_original_explicit_reported_hue_family_count":int(r.n_distinct_reported_hue_families),
          "source_original_hue_species_count":int(r.n_reported_hue_species),
          "source_original_yellow_hue_species_count":int(r.n_yellow_reported_species),
          "selection_independent_of_Bombus_and_wind_outcomes":True,
        })
    if len(frozen)!=422:
        raise ValueError("STAGE78B_ORIGINAL_422_UNIQUE_GEO_COLOUR_NETWORKS_CHANGED")
    bystudy=defaultdict(list)
    for record in sorted(frozen,key=lambda r:(r["Study_id"],r["Year"],r["Network_id"])):
        bystudy[record["Study_id"]].append(record)
    selected=[]
    for study,records in sorted(bystudy.items()):
        selected+=records[:MAX_NETWORKS_PER_STUDY]
    if len({r["Study_id"] for r in selected})<35 or len(selected)<95:
        raise ValueError("STAGE78B_NOT_CONTINENTAL_STUDY_BALANCED_SUBFRAME")
    return selected,{
      "original_source_visual_networks":424,
      "source_unique_coordinate_visual_networks":len(frozen),
      "source_source_original_studies_after_location_gate":len(bystudy),
      "source_ineligible_network_reasons":dict(excluded),
      "sampling_rule":"earliest year and network ID, at most 4 per original study",
      "study_balanced_frozen_networks":len(selected),
      "study_balanced_frozen_studies":len({r["Study_id"] for r in selected}),
      "source_Bombus_visitation_ignored_during_selection":True,
      "source_climate_exposure_ignored_during_selection":True,
    }

def build_requests(selected):
    tasks=defaultdict(lambda:defaultdict(list))
    key_map={(r["Study_id"],r["Network_id"],r["Year"]):r for r in selected}
    for item in selected:
        for m in item["original_visited_months"]:
            source_id=(item["Year"],m)
            coord=(round(item["lat"],5),round(item["lon"],5))
            tasks[source_id][coord].append(
                (item["Study_id"],item["Network_id"],item["Year"]))
    out=[]
    for (year,month),locations in sorted(tasks.items()):
        coords=sorted(locations)
        for i in range(0,len(coords),MAX_SOURCE_LOCATIONS_PER_REQUEST):
            cohort=coords[i:i+MAX_SOURCE_LOCATIONS_PER_REQUEST]
            begin=datetime.date(int(year),month,1)
            end=(datetime.date(int(year)+(month==12),1 if month==12 else month+1,1)
                 -datetime.timedelta(days=1))
            pars={
               "latitude":",".join(str(p[0]) for p in cohort),
               "longitude":",".join(str(p[1]) for p in cohort),
               "start_date":begin.isoformat(),"end_date":end.isoformat(),
               "daily":",".join(DAILY_VARS),
               "models":"era5","timezone":"GMT","wind_speed_unit":"ms",
               "elevation":",".join("nan" for _ in cohort),
               "cell_selection":"nearest",
            }
            out.append({"year":year,"month":month,
               "begin":begin,"end":end,
               "coordinates":cohort,
               "keys_by_coord":{coord:locations[coord] for coord in cohort},
               "original_API_URL":API+"?"+urllib.parse.urlencode(pars)})
    if len(out)>MAX_SOURCE_REQUESTS:
        raise ValueError("STAGE78B_PROSPECTIVE_API_BUDGET_EXCEEDS_CAP")
    return out

def source_days(frame,begin,end):
    raw=frame.get("daily") or {}
    units=frame.get("daily_units") or {}
    if units.get("wind_gusts_10m_max")!="m/s" or units.get("wind_speed_10m_max")!="m/s":
        raise ValueError("STAGE78B_SOURCE_GUST_AND_SUSTAINED_NOT_METRES_PER_SECOND")
    if frame.get("utc_offset_seconds")!=0:
        raise ValueError("STAGE78B_SOURCE_NOT_GMT")
    n=(end-begin).days+1
    expected=[(begin+datetime.timedelta(days=k)).isoformat() for k in range(n)]
    if raw.get("time")!=expected:
        raise ValueError("STAGE78B_SOURCE_ORIGINAL_ERA5_MONTH_DATES_MISMATCH")
    values={}
    for var in DAILY_VARS:
        x=raw.get(var)
        if not isinstance(x,list) or len(x)!=n:
            raise ValueError("STAGE78B_SOURCE_ERA5_VARIABLE_MISSING_"+var)
        if any(v is None or not isinstance(v,(int,float)) or not math.isfinite(v) for v in x):
            raise ValueError("STAGE78B_ERA5_MISSING_DAILY_VALUE_NO_ZERO_IMPUTE_"+var)
        if var in ("wind_gusts_10m_max","wind_speed_10m_max") and any(v<0 for v in x):
            raise ValueError("STAGE78B_SOURCE_NEGATIVE_WIND")
        values[var]=x
    return values

def retrieve_strong_gusts(pages):
    daily=defaultdict(lambda:defaultdict(lambda:defaultdict(list)))
    evidence=[]
    for i,job in enumerate(pages):
        result,sha,count=original_api(job["original_API_URL"])
        if isinstance(result,dict):result=[result]
        if not isinstance(result,list) or len(result)!=len(job["coordinates"]):
            raise ValueError("STAGE78B_ERA5_MULTI_SOURCE_RESPONSE_LENGTH_CHANGED")
        for coord,source in zip(job["coordinates"],result):
            if abs(float(source.get("latitude",999))-coord[0])>.35 or abs(float(source.get("longitude",999))-coord[1])>.35:
                raise ValueError("STAGE78B_SOURCE_REANALYSIS_GRID_TOO_FAR")
            values=source_days(source,job["begin"],job["end"])
            for network in job["keys_by_coord"][coord]:
                if job["month"] in daily[network]:
                    raise ValueError("STAGE78B_DUPLICATED_SOURCE_STUDY_MONTH_WEATHER_JOIN")
                daily[network][job["month"]]=values
        evidence.append({
          "original_ERA5_model":"era5",
          "original_ERA5_GMT_month":str(job["year"])+"-"+str(job["month"]).zfill(2),
          "n_original_sites_in_batch":len(job["coordinates"]),
          "source_original_response_SHA256":sha,"source_raw_JSON_bytes":count,
          "original_source_openmeteo_URL":job["original_API_URL"],
          "source_same_field_visit_hour_gust_observed":False})
        # Protect provider rate quotas; no concurrent calls or implicit retry
        if i+1<len(pages):time.sleep(.18)
    return daily,evidence

def aggregate_exposure(frozen,weather):
    result=[]
    for r in frozen:
        key=(r["Study_id"],r["Network_id"],r["Year"])
        got=weather.get(key,{})
        if set(got)!=set(r["original_visited_months"]):
            raise ValueError("STAGE78B_ORIGINAL_OBSERVED_MONTHS_EXPOSURE_INCOMPLETE")
        variables={v:[] for v in DAILY_VARS}
        for month in sorted(got):
            for v in variables:variables[v]+=got[month][v]
        gust=variables["wind_gusts_10m_max"]
        if len(gust)<28:
            raise ValueError("STAGE78B_ERA5_TOO_FEW_MONTH_DAYS")
        out={**r,
            "original_ERA5_exposure_days_source_observed_visit_months":len(gust),
            "source_strong_gust_is_ERA5_daily_max_not_mean_wind":True,
            "original_source_visit_months_selection_may_depend_on_observation":True,
            "reanalysis_gust_is_not_visited_hour_actual_wind":True,
            "actual_flower_scent_plume_not_observed":True}
        for threshold in GUST_THRESHOLDS:
            p=sum(x>=threshold for x in gust)/len(gust)
            out[f"original_ERA5_fraction_days_10m_gust_ge_{threshold}_ms"]=p
        ordered=sorted(gust)
        out["original_ERA5_daily_max_gust_p95_m_s"]=ordered[math.ceil(.95*len(ordered))-1]
        out["original_ERA5_max_gust_m_s"]=max(gust)
        out["original_ERA5_fraction_days_daily_sustained_max_ge_8_ms"]=(
            sum(x>=SECONDARY_SUSTAINED_THRESHOLD for x in variables["wind_speed_10m_max"])/len(gust))
        out["original_ERA5_period_average_daily_max_sustained_wind_m_s"]=(
            sum(variables["wind_speed_10m_max"])/len(gust))
        out["original_ERA5_period_daily_T_mean_C"]=sum(variables["temperature_2m_mean"])/len(gust)
        out["original_ERA5_period_precip_total_mm"]=sum(variables["precipitation_sum"])
        out["original_ERA5_period_precip_mm_per_day"]=sum(variables["precipitation_sum"])/len(gust)
        out["original_ERA5_period_radiation_MJ_m2_day"]=sum(variables["shortwave_radiation_sum"])/len(gust)
        result.append(out)
    return result

def fit_source_study_frame(exposures,site_records):
    look={(r["Study_id"],r["Network_id"],r["Year"]):r for r in site_records}
    allrows=[]
    for r in exposures:
        v=look[(r["Study_id"],r["Network_id"],r["Year"])]
        B=int(v["source_actual_strict_species_rank_Bombus_records"])
        O=int(v["source_actual_strict_species_rank_other_bees_records"])
        tot=B+O
        visual=math.log((r["source_original_yellow_hue_species_count"]+.5)/
           (r["source_original_hue_species_count"]-r["source_original_yellow_hue_species_count"]+.5))
        allrows.append({
           "Study_id":r["Study_id"],
           "original_study_ERA5_gust_grid_site_year_month":r["Network_id"]+"|"+r["Year"],
           "reported_visual_hue_logit":visual,
           "original_strict_Bombus":B,"original_strict_other_bees":O,
           "n_observed_strict_bees":tot,
           "Bombus_observed_bee_logodds":math.log((B+.5)/(O+.5)),
           "wind_extreme15_10pct":r["original_ERA5_fraction_days_10m_gust_ge_15_ms"]*10,
           "wind_extreme10_10pct":r["original_ERA5_fraction_days_10m_gust_ge_10_ms"]*10,
           "wind_extreme20_10pct":r["original_ERA5_fraction_days_10m_gust_ge_20_ms"]*10,
           "wind_p95_gust_m_s":r["original_ERA5_daily_max_gust_p95_m_s"],
           "temp":r["original_ERA5_period_daily_T_mean_C"],
           "prec":r["original_ERA5_period_precip_mm_per_day"],
           "radiation":r["original_ERA5_period_radiation_MJ_m2_day"],
        })
    df=pd.DataFrame(allrows)
    pre=df.copy()
    for name in ("temp","prec","radiation"):
        st=float(pre[name].std())
        if st<=0:raise ValueError("STAGE78B_NO_ENVIRONMENTAL_VARIABILITY_"+name)
        df["z_"+name]=(df[name]-pre[name].mean())/st
    withbee=df.loc[df.n_observed_strict_bees>0].copy()
    criteria={
      "source_outcome_blind_exposure_sites":len(pre),
      "source_outcome_blind_study_ids":pre.Study_id.nunique(),
      "source_after_observed_identified_bees":len(withbee),
      "source_after_observed_identified_bees_studies":withbee.Study_id.nunique(),
      "study_wind15_within_study_nonzero_sd_count":
        int((pre.groupby("Study_id")["wind_extreme15_10pct"].std().fillna(0)>1e-9).sum()),
      "source_extreme15_zero_site_count":
        int((pre.wind_extreme15_10pct==0).sum()),
      "source_extreme20_zero_site_count":
        int((pre.wind_extreme20_10pct==0).sum()),
      "source_surveyed_months_are_conditioned_on_positive_visit_records":True,
      "no_original_instantaneous_wind_or_scent_plume_measured":True,
    }
    if len(withbee)<MIN_MODEL_NETWORKS or withbee.Study_id.nunique()<MIN_MODEL_STUDIES:
        return criteria,{"status":"NO_MODEL_INSUFFICIENT_SOURCE_STUDY_SUPPORT"}
    outputs={}
    for tag,windcol in (
      ("PRIMARY_extreme15","wind_extreme15_10pct"),
      ("SENS_extreme10","wind_extreme10_10pct"),
      ("SENS_extreme20","wind_extreme20_10pct"),
      ("SENS_gust95","wind_p95_gust_m_s")):
        formula=("Bombus_observed_bee_logodds ~ reported_visual_hue_logit * "
          +windcol+" + z_temp + z_prec + C(Study_id)")
        try:
            fit=smf.ols(formula,data=withbee).fit()
            rank=int(np.linalg.matrix_rank(fit.model.exog))
            if rank<len(fit.params):
                outputs[tag]={"status":"UNIDENTIFIED_DESIGN_MATRIX_SINGULAR",
                     "source_design_rank":rank,"source_design_columns":len(fit.params)}
                continue
            robust=fit.get_robustcov_results(cov_type="cluster",
                groups=withbee["Study_id"],use_correction=True)
            out=[]
            for term,coef,interval in zip(fit.params.index,robust.params,robust.conf_int()):
                if term.startswith("C(Study_id)"):continue
                out.append({"term":term,"exploratory_linear_composition_coefficient":float(coef),
                  "study_cluster_sampling_interval_95_not_causal":[float(x) for x in interval]})
            interaction="reported_visual_hue_logit:"+windcol
            loo=[]
            for st in sorted(withbee.Study_id.unique()):
                a=withbee.loc[withbee.Study_id!=st]
                if a.Study_id.nunique()<MIN_MODEL_STUDIES:continue
                model=smf.ols(formula,data=a).fit()
                loo.append(float(model.params.get(interaction,float("nan"))))
            estimate=float(fit.params[interaction])
            outputs[tag]={
              "status":"DESCRIPTIVE_SOURCE_STUDY_CLUSTER_SCREEN_ONLY",
              "original_observational_source_networks":len(withbee),
              "original_source_study_groups":withbee.Study_id.nunique(),
              "source_pseudoreplication_phylogeny_not_controlled":True,
              "source_formula":formula,
              "source_R2_not_causal_explanatory_fraction":float(fit.rsquared),
              "source_predictors":out,
              "interaction_leave_one_source_study_out_n":len(loo),
              "interaction_leave_one_source_study_out_range":
                 [min(loo),max(loo)] if loo else None,
              "interaction_leave_one_study_out_sign_flips":
                 sum((v>0)!=(estimate>0) for v in loo),
              "no_inferred_pollinator_absences":True,
              "no_species_fixed_effect_color_identifiability":True,
              "NO_validated_wind_gust_odor_plume_mediation":True,
              "NOT_binomial_visitation_or_phylogenetic_causal_estimator":True,
            }
        except Exception as exc:
            outputs[tag]={"status":"MODEL_NOT_FITTED_EXPLICIT_SOURCE_ERROR",
              "error_type":type(exc).__name__}
    return criteria,outputs

def save_csv(path,rows):
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def run(nhm,plant,site):
    frozen,frame=pre_bombus_strong_gust_sample(nhm,plant,site)
    req=build_requests(frozen)
    original_weather,source_receipts=retrieve_strong_gusts(req)
    exposure=aggregate_exposure(frozen,original_weather)
    diagnostic,fits=fit_source_study_frame(exposure,site)
    return exposure,{
       "schema":"stage78b_original_2026_54study_euppollnet_visual_Bombus_ERA5_strong_gust_macro",
       "source_original_network_plant_site_SHA":PIN,
       "source_visual_network_frame_and_study_balance":frame,
       "source_actual_ERA5_requests_recorded":len(source_receipts),
       "source_ERA5_real_API_source_provenance":source_receipts,
       "source_ERA5_reanalysis_gust_not_original_anemometer":True,
       "primary_gust_threshold_m_s":15,
       "sensitivity_gust_threshold_m_s":[10,20],
       "source_original_month_days_not_only_true_visited_days":True,
       "source_study_original_ERA5_analysis_cohort":diagnostic,
       "strong_gust_x_visual_x_realized_Bombus_exploratory_models":fits,
       "no_new_global_phylogenetic_sem_or_scent_mediation":True,
       "user_request_extreme_wind_not_mean_wind_addressed":True,
    }

def scientific_json(obj):
    if isinstance(obj,np.integer):return int(obj)
    if isinstance(obj,np.floating):return float(obj)
    if isinstance(obj,np.bool_):return bool(obj)
    raise TypeError("Non-numeric unsupported scientific JSON source")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-NHM",type=Path,required=True)
    p.add_argument("--source-plant-network",type=Path,required=True)
    p.add_argument("--source-original-field-climate",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    for name,path in (("nhm",a.source_NHM),("plant_network",a.source_plant_network),
       ("sites",a.source_original_field_climate)):
        verified_csv(path,PIN[name])
    x,report=run(verified_csv(a.source_NHM,PIN["nhm"]),
        verified_csv(a.source_plant_network,PIN["plant_network"]),
        verified_csv(a.source_original_field_climate,PIN["sites"]))
    a.outdir.mkdir(exist_ok=True,parents=True)
    save_csv(a.outdir/"source_ERA5_true_strong_gust_study_balanced_424_frame.csv",x)
    (a.outdir/"source_ERA5_actual_gust_bombus_visual_macro_and_audit.json").write_text(
        json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False,default=scientific_json)+"\n",encoding="utf-8")
    concise={k:v for k,v in report.items() if k!="source_ERA5_real_API_source_provenance"}
    print("STAGE78B_REAL_EUROPE_MACRO_STRONG_GUST_NOT_MEAN_WIND",
          json.dumps(concise,sort_keys=True,default=scientific_json))
    print("ERA5_SURVEY_MONTH_MAX_GUST_NOT_INSTANTANEOUS_BEHAVIOR_NO_CAUSAL_SCENT")
if __name__=="__main__":main()
