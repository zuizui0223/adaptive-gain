"""Stage79H: study-balanced 2026 continental REAL gust × botanical petal width × Bombus.

Original response: corrected v1.3.0 EuPPPollNet 623,476 observed insect visits.
Original antecedent: source botanical NHM petal max width in cm, source positive
floral phenotype measured in taxon descriptions, NOT same-field petal size,
actual flower display nor bee receptor contrast.
Original climate: source SHA verified ERA5 10m daily MAX gust study-matched
month (Stage78B) for 152 outcome-blind selected 43-study field networks.
All inclusion based on source positive WIDTH and the preselected ERA5 cohort
before opening original Bombus/other-bee outcomes.

Use network-intercept null logistic score U and information I for log-width
within each real source network. This is NOT a fitted maximum-likelihood
binomial size effect. Optional study-FE WLS of U/I ~ gust + ERA5 T/P is a
FIRST-ORDER descriptive null-score tendency, only if ≥25 source networks,
≥10 independent studies and ≥5 studies have within-study strong gust
variation. Otherwise output NO-GO, never manufacture a causal coefficient.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,sys
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_literature_macro_stage69"))
from ingest_original_corrected_EuPPollNet_network_NHM_spectra import (
    fetch_original,dict_rows,year_of,guild_of,is_species,EXPECTED_INTERACTIONS
)

STAGE79_TRAIT_SHA=None  # Versioned original Stage79B artifact checked by workflow.
STAGE78_GUST_SHA=None   # Versioned original Stage78B artifact checked by workflow.
PETAL_WIDTH_NAME="source_petal_max_width_cm"
GUST15="original_ERA5_fraction_days_10m_gust_ge_15_ms"
MIN_NETWORKS=25
MIN_STUDIES=10
MIN_WITHIN_GUST_STUDIES=5

def csv_records(path):
    with Path(path).open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def site_key(r):
    return (r["Study_id"],r["Network_id"],r["Year"])

def source_preguild_frame(traits,gust):
    # Scientific cohort selection explicitly sees neither B nor O outcomes.
    original={}
    for r in gust:
        k=site_key(r)
        if k in original:raise ValueError("STAGE79H_DUPLICATE_ORIGINAL_ERA5_NETWORK")
        original[k]=r
    if len(original)!=152:
        raise ValueError("STAGE79H_SOURCE_152_GUST_NETWORKS_CHANGED")
    plant=defaultdict(list)
    for r in traits:
        k=site_key(r)
        if k not in original:continue
        value=str(r.get(PETAL_WIDTH_NAME) or "").strip()
        if not value:continue
        w=float(value)
        if not .001<=w<=150:
            raise ValueError("STAGE79H_ORIGINAL_PETAL_WIDTH_OUT_OF_RANGE")
        plant[k].append((r["original_plant_literal_accepted_name"].strip().casefold(),w))
    cohorts={k:v for k,v in plant.items() if len({s for s,w in v})>=2
             and len({w for s,w in v})>=2}
    if not all(r.get("reanalysis_gust_is_not_visited_hour_actual_wind")=="True"
               for r in gust):
        raise ValueError("STAGE79H_REANALYSIS_GUST_MISLABELLED_AS_VISIT_HOUR")
    return original,cohorts,{
       "original_ERA5_outcome_blind_field_networks":len(original),
       "source_networks_with_at_least_two_distinct_petal_widths_pre_guild":len(cohorts),
       "source_studies_with_at_least_two_petal_widths_pre_guild":len({k[0] for k in cohorts}),
       "source_petal_width_species_in_selected_networks":len({s for sites in cohorts.values() for s,w in sites}),
       "source_size_selected_without_Bombus_response":True,
       "source_only_152_hue_balanced_networks_not_universal_size_panel":True,
    }

def strict_bee_records(selected):
    groups=defaultdict(Counter)
    source_rows=0
    for row in dict_rows(fetch_original("Interaction_data.csv.gz"),compressed=True):
        source_rows+=1
        k=(row["Study_id"].strip(),row["Network_id"].strip(),year_of(row["Date"]))
        if k not in selected:continue
        if not is_species(row):continue
        if row.get("Pollinator_rank","").strip().casefold()!="species":continue
        if row.get("Pollinator_unsure_id","").strip().casefold() in {"yes","true","1","y"}:continue
        guild=guild_of(row)
        plant=row["Plant_accepted_name"].strip().casefold()
        if guild=="Bombus":groups[(k,plant)]["B"]+=1
        elif guild=="other_bee":groups[(k,plant)]["O"]+=1
    if source_rows!=EXPECTED_INTERACTIONS:
        raise ValueError("STAGE79H_ORIGINAL_CORRECTED_VISIT_623476_ROWS_CHANGED")
    return groups

def within_network_null_score(k,plants,source_counts,clim):
    records=[]
    seen=set()
    for s,w in plants:
        if s in seen:raise ValueError("STAGE79H_DUPLICATE_PETAL_WIDTH_PLANT_IN_NETWORK")
        seen.add(s)
        counts=source_counts.get((k,s),Counter())
        B=counts["B"];O=counts["O"]
        if B+O:records.append((s,math.log(w),B,O))
    if len(records)<2 or len({x for _,x,_,_ in records})<2:
        return None,"FEWER_THAN_TWO_SOURCE_WIDTHS_WITH_IDENTIFIED_BEE_VISITS"
    N=sum(b+o for _,_,b,o in records);Btot=sum(b for _,_,b,o in records)
    if Btot==0 or Btot==N:
        return None,"ONLY_ONE_IDENTIFIED_BEE_GUILD_IN_NETWORK"
    p=Btot/N
    mx=sum((b+o)*x for _,x,b,o in records)/N
    U=sum((b-(b+o)*p)*(x-mx) for _,x,b,o in records)
    I=p*(1-p)*sum((b+o)*(x-mx)**2 for _,x,b,o in records)
    if I<=0:return None,"ZERO_WITHIN_NETWORK_SOURCE_WIDTH_INFORMATION"
    return {
       "Study_id":k[0],"Network_id":k[1],"Year":k[2],
       "source_identified_species_with_distinct_width_and_bees":len(records),
       "original_source_visitor_events_bee_denom":N,
       "original_source_Bombus_visitors":Btot,
       "original_source_width_local_null_score":U,
       "original_source_width_local_null_information":I,
       "original_source_width_null_score_ratio":U/I,
       "original_source_strong_gust_day_fraction15":float(clim[GUST15]),
       "original_source_strong_gust_per10pp":10*float(clim[GUST15]),
       "original_source_ERA5_temperature_C":float(clim["original_ERA5_period_daily_T_mean_C"]),
       "original_source_ERA5_precip_mm_day":float(clim["original_ERA5_period_precip_mm_per_day"]),
       "original_source_petal_width_not_same_field_flower_population":True,
       "original_source_gust_not_bee_visit_hour":True,
       "source_source_actual_Bee_composition_not_pollination_fitness":True,
    },"INFORMATIVE"

def descriptive_size_gust_relationship(rows):
    report={"original_source_size_gust_informative_networks":len(rows),
            "original_source_size_gust_informative_studies":len({x["Study_id"] for x in rows}),
            "source_gust15_nonzero_exposure_networks":sum(x["original_source_strong_gust_day_fraction15"]>0 for x in rows),
            "within_study_gust15_variation_groups":0,
            "source_original_null_score_primary_logwidth_over_study_network":None,
            "nullscore_not_binomial_mle":True}
    if not rows:return {"status":"NO_GUILD_INFORMATIVE_SIZE_NETWORKS",**report}
    df=pd.DataFrame(rows)
    ratio=(df.original_source_width_local_null_score.sum()/
           df.original_source_width_local_null_information.sum())
    report["source_original_null_score_primary_logwidth_over_study_network"]=float(ratio)
    vars=df.groupby("Study_id")["original_source_strong_gust_per10pp"].agg(["size","std"])
    nvary=int(((vars["size"]>=2)&(vars["std"].fillna(0)>1e-7)).sum())
    report["within_study_gust15_variation_groups"]=nvary
    if len(rows)<MIN_NETWORKS or df.Study_id.nunique()<MIN_STUDIES or nvary<MIN_WITHIN_GUST_STUDIES:
        return {"status":"NO_GO_INSUFFICIENT_WITHIN_STUDY_STRONG_GUST_OR_SOURCE_WIDTH_BEE_OVERLAP",**report}
    import statsmodels.formula.api as smf
    df["z_temp"]=(df.original_source_ERA5_temperature_C-
                  df.original_source_ERA5_temperature_C.mean())/df.original_source_ERA5_temperature_C.std()
    df["z_prec"]=(df.original_source_ERA5_precip_mm_day-
                  df.original_source_ERA5_precip_mm_day.mean())/df.original_source_ERA5_precip_mm_day.std()
    formula="original_source_width_null_score_ratio ~ original_source_strong_gust_per10pp + z_temp + z_prec + C(Study_id)"
    fit=smf.wls(formula,df,weights=df.original_source_width_local_null_information).fit()
    if int(np.linalg.matrix_rank(fit.model.exog))!=len(fit.params):
        return {"status":"NO_GO_SINGULAR_STUDY_FE_SOURCE_GUST_DESIGN",**report}
    robust=fit.get_robustcov_results(cov_type="cluster",groups=df["Study_id"])
    term="original_source_strong_gust_per10pp"
    idx=list(fit.params.index).index(term)
    return {"status":"SOURCE_OBSERVATIONAL_NETWORK_NULL_SCORE_GUST_TENDENCY",
       **report,"source_formula":formula,
       "original_source_gust15_x_width_nullscore_tendency_per_10pp":float(robust.params[idx]),
       "source_study_cluster_95_sampling_interval_not_causal":[float(x) for x in robust.conf_int()[idx]],
       "no_independent_species_phylogeny_or_survey_effort_control":True,
       "not_measured_flower_display_or_true_UV_guider":True}

def analyze(traits,gust):
    indexed,plant,design=source_preguild_frame(traits,gust)
    counts=strict_bee_records(set(plant))
    success=[];gates=Counter()
    for k,items in sorted(plant.items()):
        info,reason=within_network_null_score(k,items,counts,indexed[k])
        gates[reason]+=1
        if info:success.append(info)
    inference=descriptive_size_gust_relationship(success)
    return {"schema":"stage79h_original_EuPP_nhm_petal_width_vs_ERA5_gust15_Bombus_site_network_source",
       "source_original_preguild_size_network_gates":design,
       "source_original_accepted_bee_width_network_reason_counts":dict(gates),
       "source_size_gust_estimand_eligibility":inference,
       "original_flower_size_proxy_source":"NHM botanical petal maximum width (cm), not total display",
       "recorded_Bombus_not_true_pollinator_absence_or_real_gust_behavior":True,
       "source_signal_stage_not_confirmed_sensory_cue_use":True,
       "source_near_FCC_and_pattern_negative_controls_NOT_MEASURED":True,
       "original_ERA5_gust15_measured_source_months_not_instantaneous":True,
       "no_general_causal_Bombus_strong_wind_visual_order_claim":True,
       "source_network_null_scores":success}

def save(path,rows):
    if not rows:return
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-original-plant-width",type=Path,required=True)
    p.add_argument("--source-original-ERA5-strong-gust",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    data=analyze(csv_records(a.source_original_plant_width),
                 csv_records(a.source_original_ERA5_strong_gust))
    a.outdir.mkdir(parents=True,exist_ok=True)
    save(a.outdir/"source_original_within_network_size_Bombus_null_scores.csv",
         data.pop("source_network_null_scores"))
    (a.outdir/"source_original_size_vs_gust15_Bombus_macro_eligibility.json").write_text(
        json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE79H_REAL_SOURCE_PETAL_WIDTH_STRONG_GUST_BOMBUS_NETWORK_GATE",
         json.dumps(data,sort_keys=True))
    print("NO_MEASURED_MARKING_ABSENCE_OR_CAUSAL_WIND_CUE_ORDER")
if __name__=="__main__":main()
