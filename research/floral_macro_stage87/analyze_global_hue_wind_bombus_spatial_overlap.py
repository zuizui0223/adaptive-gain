"""Stage87E: worldwide source-native flower-hue geography × climate × observed Bombus.

Input is the immutable, checked GBIF Bombus source and NHM/WCVP/WorldClim
source-derived regional artifacts. We NEVER treat regions without Bombus
records as species absence. This is a descriptive spatial correspondence,
NOT sensory cue order, a Bombus preference, wind-at-flower, VOC plume,
pollinator learning, landing, selection, or biological trait prevalence.

Primary universe: accepted regionally native source flora, >=50 source
single-lexical-hue plant names, five climatological variables at >=12
source region samples, original TDWG geometry valid without repair.
A separate association within GBIF-positive regions additionally requires
>=1 Bombus species supported by >=3 occurrences in >=2 1-degree grid cells
and >=5 occupied grid cells. These eligibility cuts have no hue outcomes.

Eleven source lexical hue families, native species pooled AND genus-balanced
summary; regional climate and geographical geography controls, GBIF
sampling intensity proxies, 2 geographically blocked bootstrap scales,
and all-family multiplicity accounting. No zeros imputed for unrecorded bees.
"""
from __future__ import annotations
import argparse,hashlib,io,json,math,zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from scipy.stats import spearmanr

WCVP_CLIMATE_ZIP_SHA="4c0ab25596078be4b2aa35a254e42695fd260e1720864e173970aac8aa7db83a"
BOMBUS_ZIP_SHA="2fe7510fe8c08189d63151fe255a00baafb96c7acc87d3d0fedc970966ca1a43"
CLIMATE_MEMBER="stage87_original_global_TDWG3_NHM_WCVP_WorldClim_regions.csv"
BOMBUS_MEMBER="stage87D_original_GBIF_Bombus_TDWG3_recorded_richness.csv"
CLIMATE_RECEIPT="stage87C_real_worldclim_TDWG3_flower_spatial_receipt.json"
BOMBUS_RECEIPT="stage87D_original_GBIF_Bombus_source_spatial_receipt.json"
COLORS=("yellow","white","purple","blue","pink","red","orange","green","brown","black","gray")
OUTCOMES=tuple(("hue_"+c+"_"+suffix,c,level) for c in COLORS
    for level,suffix in (("pooled","fraction_of_exclusive_documented"),
                         ("genus_balanced","mean_of_genus_fractions")))
WIND="worldclim_baseline_wind_m_s"
TEMP="worldclim_baseline_mean_temperature_C"
PREC="worldclim_baseline_precip_mm_month"
SOLAR="worldclim_baseline_solar_kJ_m2_day"
VAPR="worldclim_baseline_vapour_kPa"
PRIMARY="GBIF_Bombus_3occ_2grid_recorded_species_primary"
STRICT="GBIF_Bombus_2grid_coord_uncertainty_le10km_sensitivity_species"
CELLS="GBIF_Bombus_unique_1degree_recorded_cells"
CLIMATE_COLS=("wind","temperature","logprec","solar","vapour",
              "source_coverage","log_plant_hues",
              "latitude","latitude_sq","sin_longitude","cos_longitude")
BEE_COLS=CLIMATE_COLS+("log_bombus_richness","log_gbif_cells","wind_x_bombus")

def verified_csv(archive,source_sha,member,receipt_name):
    raw=Path(archive).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=source_sha:
        raise ValueError("STAGE87E_AUTHENTIC_SOURCE_ARTIFACT_ZIP_SHA_CHANGED_"+member)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if member not in z.namelist() or receipt_name not in z.namelist():
            raise ValueError("STAGE87E_SOURCE_ARTIFACT_MEMBERS_MISSING")
        tab=pd.read_csv(io.BytesIO(z.read(member)))
        receipt=json.loads(z.read(receipt_name))
    if "TDWG_L3" not in tab or tab.TDWG_L3.duplicated().any():
        raise ValueError("STAGE87E_UNIQUE_TDWG3_SOURCE_SPATIAL_KEYS_REQUIRED")
    return tab,receipt

def source_join(climate_zip,bombus_zip):
    x,c=verified_csv(climate_zip,WCVP_CLIMATE_ZIP_SHA,
                      CLIMATE_MEMBER,CLIMATE_RECEIPT)
    b,r=verified_csv(bombus_zip,BOMBUS_ZIP_SHA,
                      BOMBUS_MEMBER,BOMBUS_RECEIPT)
    if len(x)!=367 or len(b)!=165 or c["source_original_global_native_region_input"]!=367:
        raise ValueError("STAGE87E_ORIGINAL_GLOBAL_367_165_SOURCE_COHORT_CHANGED")
    if r["original_source_archive"]["observed_original_full_source_count"]!=3958417:
        raise ValueError("STAGE87E_REAL_GBIF_ORIGINAL_3958417_CHANGED")
    merged=x.merge(b,on="TDWG_L3",how="left",validate="one_to_one",indicator=True)
    if (merged["_merge"]=="both").sum()!=165:
        raise ValueError("STAGE87E_UNEXPECTED_GBIF_SOURCE_POSITIVE_REGION_OVERLAP")
    merged["GBIF_observed_Bombus_source_coverage"]=merged["_merge"].eq("both")
    merged=merged.drop(columns=["_merge"])
    merged["latitude"]=pd.to_numeric(merged["region_sampling_latitude_mean"])
    merged["longitude"]=pd.to_numeric(merged["region_sampling_longitude_mean"])
    merged["latitude_sq"]=merged["latitude"]**2
    merged["sin_longitude"]=np.sin(np.radians(merged.longitude))
    merged["cos_longitude"]=np.cos(np.radians(merged.longitude))
    merged["wind"]=merged[WIND]
    merged["temperature"]=merged[TEMP]
    merged["logprec"]=np.log1p(merged[PREC])
    merged["solar"]=merged[SOLAR]
    merged["vapour"]=merged[VAPR]
    merged["source_coverage"]=merged.source_documented_colour_coverage_fraction
    merged["log_plant_hues"]=np.log1p(merged.n_source_single_explicit_hue)
    merged["log_bombus_richness"]=np.log1p(merged[PRIMARY])
    merged["log_bombus_strict"]=np.log1p(merged[STRICT])
    merged["log_gbif_cells"]=np.log1p(merged[CELLS])
    good=(merged.n_source_single_explicit_hue>=50)&(
          merged.source_all_5climate_variables_at_12_or_more_points==1)&(
          merged.source_original_TDWG_polygon_geometry_repaired_sensitivity==0)
    global_data=merged.loc[good].copy()
    positive=global_data.loc[global_data.GBIF_observed_Bombus_source_coverage &
         (global_data[PRIMARY]>0)&(global_data[CELLS]>=5)].copy()
    if len(global_data)!=274 or len(positive)!=139:
        raise ValueError("STAGE87E_SOURCE_274_GLOBAL_139_BOMBUS_POSITIVE_GATES_CHANGED")
    if not positive[CELLS].ge(5).all() or positive[PRIMARY].eq(0).any():
        raise ValueError("STAGE87E_FALSE_RECEIVER_ABSENCE_OR_EFFORT_ZERO")
    return merged,global_data,positive,{"original_flora_regions":len(x),
        "original_worldclim_complete_regions":int(
            (merged.source_all_5climate_variables_at_12_or_more_points==1).sum()),
        "original_Bombus_positive_regions":int(merged.GBIF_observed_Bombus_source_coverage.sum()),
        "global_source_hue_geographic_regression_regions":len(global_data),
        "recorded_Bombus_positive_eligible_geographic_regions":len(positive),
        "global_hue_source_minimum_n":50,
        "GBIF_occupied_1degree_cells_minimum":5,
        "number_of_original_TDWG_regions_with_repaired_geometry_excluded":
         int(merged.source_original_TDWG_polygon_geometry_repaired_sensitivity.sum()),
        "GBIF_missing_region_records_not_true_absence":True,
        "regions_are_not_independent_plant_evolutionary_origins":True}

def source_design(frame,include_bee):
    cols=list(CLIMATE_COLS)+(["log_bombus_richness","log_gbif_cells"] if include_bee else [])
    x=pd.DataFrame(index=frame.index)
    for col in cols:
        a=np.asarray(frame[col],float)
        if not np.isfinite(a).all() or a.std(ddof=0)<=1e-12:
            raise ValueError("STAGE87E_MISSING_OR_UNVARIABLE_CONTROLLING_SOURCE_PREDICTOR_"+col)
        x[col]=(a-a.mean())/a.std(ddof=0)
    if include_bee:x["wind_x_bombus"]=x["wind"]*x["log_bombus_richness"]
    return sm.add_constant(x,has_constant="add")

def source_blocks(frame,latitude_bin,longitude_bin):
    lat=np.floor((frame.latitude.to_numpy()+90)/latitude_bin).astype(int)
    lon=np.floor((frame.longitude.to_numpy()+180)/longitude_bin).astype(int)
    return np.stack((lat,lon),axis=1)

def all_outcomes(frame):
    y=frame[[z[0] for z in OUTCOMES]].copy()
    if (y.isna().to_numpy().any() or (~np.isfinite(y.to_numpy(dtype=float))).any() or
         (y.to_numpy(dtype=float)<0).any() or (y.to_numpy(dtype=float)>1).any()):
        raise ValueError("STAGE87E_SOURCE_HUE_FRACTION_UNRECORDED_IN_ELIGIBLE_REGIONS")
    return y

def spatial_bootstrap(frame,x,y,reps=1000,seed=20261118,latitude_bin=20,longitude_bin=45):
    b=source_blocks(frame,latitude_bin,longitude_bin)
    unique,inv=np.unique(b,axis=0,return_inverse=True)
    if len(unique)<10:raise ValueError("STAGE87E_FEWER_THAN_10_SPATIAL_BLOCKS")
    groups=[np.where(inv==i)[0] for i in range(len(unique))]
    rng=np.random.default_rng(seed)
    X=x.to_numpy(float);Y=y.to_numpy(float)
    result=[]
    for _ in range(reps):
        block_sel=rng.integers(0,len(unique),size=len(unique))
        ids=np.concatenate([groups[j] for j in block_sel])
        if len(ids)<X.shape[1]+3:continue
        # Refit source region model while respecting blocks; if a geographic
        # resample cannot identify all covariates, do not silently impute.
        try:
            beta,_,rank,_=np.linalg.lstsq(X[ids],Y[ids],rcond=None)
        except np.linalg.LinAlgError:continue
        if rank!=X.shape[1]:continue
        result.append(beta)
    if len(result)<int(reps*.7):
        raise ValueError("STAGE87E_SPATIAL_BOOTSTRAP_REPLICATION_RANK_TOO_LOW")
    out=np.asarray(result)
    return {"n_independent_approx_geographic_blocks":len(unique),
      "n_successful_geographic_resamples":len(result),
      "block_definition_degrees":[latitude_bin,longitude_bin],
      "intervals":np.quantile(out,[.025,.975],axis=0)}

def spatial_sector_loo(frame,x,y,term):
    lon=frame.longitude.to_numpy()
    ids=np.floor((lon+180)/120).astype(int)
    values=[]
    for sector in np.unique(ids):
        mask=ids!=sector
        if sum(mask)<x.shape[1]+15:continue
        if np.linalg.matrix_rank(x.to_numpy()[mask])!=x.shape[1]:continue
        beta=np.linalg.lstsq(x.to_numpy()[mask],y.to_numpy()[mask],rcond=None)[0]
        j=list(x.columns).index(term)
        values.append({"excluded_longitude_sector":int(sector),
             "regions_remaining":int(sum(mask)),
             "coefficients_by_hue":[float(z) for z in beta[j]]})
    return values

def bh_by_columns(rows,field):
    for category in ("pooled","genus_balanced"):
        for term in sorted({k for r in rows if r["averaging"]==category for k in r["coefficients"]}):
            idx=[i for i,r in enumerate(rows) if r["averaging"]==category and term in r["coefficients"]]
            p=[rows[i]["coefficients"][term]["HC3_exploratory_p"] for i in idx]
            vals=multipletests(p,method="fdr_bh")[1]
            for i,v in zip(idx,vals):rows[i]["coefficients"][term]["BH_q_in_11_original_hues"]=float(v)

def analyze_frame(frame,scope,include_bee,spatial_reps=1000):
    X=source_design(frame,include_bee)
    Y=all_outcomes(frame)
    names=list(X.columns)
    target=["wind"]+(["log_bombus_richness","wind_x_bombus"] if include_bee else [])
    # Same fixed source design, separately fitted source fractions.
    fits=[sm.OLS(Y.iloc[:,j].to_numpy(float),X).fit(cov_type="HC3")
          for j in range(Y.shape[1])]
    block_small=spatial_bootstrap(frame,X,Y,reps=spatial_reps,latitude_bin=20,longitude_bin=45)
    block_large=spatial_bootstrap(frame,X,Y,reps=spatial_reps,seed=20261119,latitude_bin=30,longitude_bin=60)
    loo={t:spatial_sector_loo(frame,X,Y,t) for t in target}
    rows=[]
    for j,(source_col,hue,level) in enumerate(OUTCOMES):
        f=fits[j]
        relation={}
        for t in target:
            k=names.index(t)
            relation[t]={
               "standardized_predictor_partial_Ols_fraction_point_slope":float(f.params.iloc[k]),
               "HC3_exploratory_p":float(f.pvalues.iloc[k]),
               "HC3_descriptive_95_interval":[float(q) for q in f.conf_int().iloc[k]],
               "spatial_20x45_degree_block_bootstrap_95":[float(q) for q in block_small["intervals"][:,k,j]],
               "spatial_30x60_degree_block_bootstrap_95":[float(q) for q in block_large["intervals"][:,k,j]],
               "longitude_sector_exclusions_coefficients":[{
                   "excluded_sector":q["excluded_longitude_sector"],
                   "slope":q["coefficients_by_hue"][j]} for q in loo[t]],
             }
        source_rho=spearmanr(frame[source_col].to_numpy(),frame.wind.to_numpy()).statistic
        row={"scope":scope,"hue":hue,"averaging":level,
          "n_regions":len(frame),
          "source_outcome_fraction":source_col,
          "source_mean_regional_hue_fraction":float(Y.iloc[:,j].mean()),
          "source_spearman_rho_hue_vs_climate_wind_unadjusted":float(source_rho),
          "model_r_squared_descriptive":float(f.rsquared),
          "coefficients":relation,
          "not_measured_receptor_guide_or_colour_discriminability":True}
        if include_bee:
            row["source_spearman_rho_hue_vs_observed_Bombus_richness_unadjusted"]=float(
                spearmanr(frame[source_col],frame[PRIMARY]).statistic)
        rows.append(row)
    bh_by_columns(rows,"coefficients")
    meta={"geographic_block_20x45_unique":block_small["n_independent_approx_geographic_blocks"],
      "geographic_block_30x60_unique":block_large["n_independent_approx_geographic_blocks"],
      "block_20x45_successful_resamples":block_small["n_successful_geographic_resamples"],
      "block_30x60_successful_resamples":block_large["n_successful_geographic_resamples"],
      "n_observed_regions":len(frame),"original_11_hue_families_and_2_genus_balance_responses":len(rows),
      "analytical_design":"OLS descriptively conditioned on regional WorldClim climate, botanical text coverage, geographic latitude/longitude, and recorded GBIF effort proxy if present",
      "latitude_longitude_block_bootstrap_not_phylogeny_or_exact_SAR_model":True}
    return rows,meta

def run(native_climate_zip,bombus_zip,out,spatial_reps=1000):
    frame,global_data,positive,support=source_join(native_climate_zip,bombus_zip)
    global_rows,global_meta=analyze_frame(global_data,"native_global_without_Bombus_selection",False,spatial_reps)
    bee_rows,bee_meta=analyze_frame(positive,"GBIF_positive_3continent_only_not_true_absence",True,spatial_reps)
    receipt={"schema":"stage87E_source_59k_botanical_TDWG_350_climate_165_observed_bombus_spatial_adjusted",
       "sources":{"global_WCVP_WorldClim_artifact_ZIP_sha256":WCVP_CLIMATE_ZIP_SHA,
          "GBIF_original_3958417_TDWG_artifact_ZIP_sha256":BOMBUS_ZIP_SHA},
       "cohort":support,
       "global_analysis":global_meta,
       "GBIF_observed_analysis":bee_meta,
       "source_hue_colour_descriptive_spatial_results":global_rows+bee_rows,
       "interpretation_gates":{
          "GBIF_no_record_regions_unknown_not_Bombus_absence":True,
          "GBIF_grid_cells_not_independent_target_group_observation_effort":True,
          "botanical_single_hue_words_not_spectrometer_far_near_signal":True,
          "original_bean_information_order_not_measured":True,
          "WorldClim_1970_2000_wind_at_2m_not_original_1950_2025_GBIF_bee_flight_wind":True,
          "regional_native_range_repeats_plant_taxa_and_spatial_autocorrelation_not_eliminated":True,
          "hue_fractions_are_compositional_not_independent_outcomes":True,
          "geographical_blocks_are_approximate_not_continental_phylogenetic_replication":True,
          "analysis_is_exploratory_spatial_correspondence_NOT_evolution_or_fitness_causal_claim":True}}
    out.mkdir(parents=True,exist_ok=True)
    (out/"stage87E_global_spatial_hue_wind_Bombus_full_original_analysis.json").write_text(
       json.dumps(receipt,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    tab=[]
    for row in global_rows+bee_rows:
        for term,r in row["coefficients"].items():
            tab.append({"scope":row["scope"],"hue":row["hue"],
                "averaging":row["averaging"],"source_regions":row["n_regions"],
                "term":term,"coef":r["standardized_predictor_partial_Ols_fraction_point_slope"],
                "HC3_p":r["HC3_exploratory_p"],"BH_q_11":r["BH_q_in_11_original_hues"],
                "spatial_20x45_lower":r["spatial_20x45_degree_block_bootstrap_95"][0],
                "spatial_20x45_upper":r["spatial_20x45_degree_block_bootstrap_95"][1],
                "spatial_30x60_lower":r["spatial_30x60_degree_block_bootstrap_95"][0],
                "spatial_30x60_upper":r["spatial_30x60_degree_block_bootstrap_95"][1]})
    pd.DataFrame(tab).to_csv(out/"stage87E_original_global_regions_colour_wind_Bombus_model_summary.csv",index=False)
    cols=["TDWG_L3","TDWG_level3_name","region_sampling_latitude_mean",
          "region_sampling_longitude_mean","n_source_single_explicit_hue",
          "source_documented_colour_coverage_fraction",WIND,TEMP,PREC,SOLAR,VAPR,
          "source_original_TDWG_polygon_geometry_repaired_sensitivity",
          "GBIF_observed_Bombus_source_coverage",PRIMARY,STRICT,CELLS]
    cols+=["hue_"+h+"_fraction_of_exclusive_documented" for h in COLORS]
    cols+=["hue_"+h+"_mean_of_genus_fractions" for h in COLORS]
    frame[cols].to_csv(out/"stage87E_original_full_TDWG_region_matched_data_with_NA_absence.csv",index=False)
    print("STAGE87E_REAL_350_GLOBAL_CLIMATE_165_BOMBUS_JOIN_SOURCE",json.dumps({
         "cohort":support,"global":global_meta,"bee":bee_meta,
         "summary":[{"scope":r["scope"],"hue":r["hue"],"averaging":r["averaging"],
           "coefficients":{k:{"estimate":v["standardized_predictor_partial_Ols_fraction_point_slope"],
                             "block_interval":v["spatial_20x45_degree_block_bootstrap_95"],
                             "BH_q":v["BH_q_in_11_original_hues"]}
                             for k,v in r["coefficients"].items()}}
            for r in global_rows+bee_rows if r["hue"] in ("yellow","purple","green","brown") and r["averaging"]=="genus_balanced"]},
         sort_keys=True),flush=True)
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage87C-global-native-climate-zip",required=True,type=Path)
    p.add_argument("--stage87D-original-GBIF-Bombus-zip",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    p.add_argument("--spatial-bootstrap-reps",type=int,default=1000)
    a=p.parse_args()
    run(a.stage87C_global_native_climate_zip,a.stage87D_original_GBIF_Bombus_zip,a.outdir,a.spatial_bootstrap_reps)
if __name__=="__main__":main()
