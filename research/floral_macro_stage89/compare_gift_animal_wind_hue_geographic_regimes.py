"""Stage89B: original GIFT3.2 biotic-vs-wind independently classified flora
and source-native NHM flower colour spatial correspondence with global wind
and 1950-2025 observed positive GBIF Bombus richness.

This is a two-mode within-*same-region* contrast. At source inclusion both
plant groups require >=10 independent explicit one-hue source taxon names.
The global unmodeled 52,603 original plant taxa with unreported source
pollen-vector mode are EXCLUDED from both arms; not coded "wind".

GIFT accepted pollination category is a literature-compiled species trait,
not direct local observed bee behavior. 367 TDWG-level3 regions repeat
species and phylogenetic origins, so geographic block bootstrap is
approximate and this is exploratory spatial correspondence only.

No observed pollinator preference for colour, no nest visit rates, no odor,
no learning, no wind at visit, no nectar guides, no landing/fitness or
causal evolutionary adaptation is inferred.
"""
from __future__ import annotations
import argparse,hashlib,io,json,zipfile
from pathlib import Path
import numpy as np,pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage87"))
from analyze_global_hue_wind_bombus_spatial_overlap import (
    source_join, source_blocks, COLORS,
    WCVP_CLIMATE_ZIP_SHA, BOMBUS_ZIP_SHA,PRIMARY,CELLS,
)
GIFT_SOURCE_SHA="26ffa12c78a583743735d89575b6b8d4c4066a01da5b2a7e54aea531915bb7a8"
GIFT_MEMBER="stage89_original_GIFT32_native_animal_wind_unknown_367_TDWG3_hues.csv"
GIFT_RECEIPT="stage89_original_GIFT32_NHM_WCVP_global_plant_mode_spatial_support.json"
SCOPES=("global","GBIF_positive_only")
COLORS_ALL=tuple(COLORS)
AGG=(("pooled","fraction_of_exclusive_documented"),
     ("genus_balanced","mean_of_genus_fractions"))
TERMS=("wind","log_bombus_richness","wind_x_bombus")
BASE_CONTROLS=("wind","temperature","logprec","solar","vapour",
    "animal_coverage","wind_coverage","animal_log_plant_hues",
    "wind_log_plant_hues","latitude","latitude_sq","sin_longitude","cos_longitude")
BEE_CONTROLS=BASE_CONTROLS+("log_bombus_richness","log_gbif_cells","wind_x_bombus")

def source_modes(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=GIFT_SOURCE_SHA:
        raise ValueError("STAGE89B_GIFT_SOURCE_ACCEPTED_5770_ZIP_SHA_CHANGED")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if GIFT_MEMBER not in z.namelist() or GIFT_RECEIPT not in z.namelist():
            raise ValueError("STAGE89B_SOURCE_GIFT_ARTIFACT_MEMBERS_MISSING")
        modes=pd.read_csv(io.BytesIO(z.read(GIFT_MEMBER)))
        receipt=json.loads(z.read(GIFT_RECEIPT))
    if len(modes)!=1101 or modes.duplicated(["TDWG_L3","pollination_mode"]).any():
        raise ValueError("STAGE89B_REAL_367_X_THREE_ORIGINAL_SOURCE_POLLINATION_MODES_CHANGED")
    if set(modes.pollination_mode)!={"animal","wind","unknown"}:
        raise ValueError("STAGE89B_ORIGINAL_SOURCE_MODE_NOT_EXACT_VALID")
    qa=receipt["source_mapped_original_species_coverage"]
    if qa["animal_exact_matched_native_taxa"]!=2560 or qa["wind_exact_matched_native_taxa"]!=612:
        raise ValueError("STAGE89B_REAL_SOURCE_2560_ANIMAL_612_WIND_CHANGED")
    return modes,receipt

def matched_native_mode_frames(gift_zip,climate_zip,bombus_zip):
    modes,gift_meta=source_modes(gift_zip)
    allclimate,global_source,bees,support=source_join(climate_zip,bombus_zip)
    source_map={m:modes.loc[modes.pollination_mode==m].set_index("TDWG_L3") for m in ("animal","wind","unknown")}
    merged=allclimate.copy()
    for m in ("animal","wind"):
        t=source_map[m].loc[list(merged.TDWG_L3)]
        merged[f"{m}_hue_n"]=t.source_explicit_single_hue_species.to_numpy()
        merged[f"{m}_coverage"]=t.source_colour_documentation_fraction.to_numpy()
        merged[f"{m}_log_plant_hues"]=np.log1p(merged[f"{m}_hue_n"])
        for hue in COLORS_ALL:
            for _,suffix in AGG:
                src=f"hue_{hue}_{suffix}"
                merged[f"{m}_{src}"]=t[src].to_numpy()
    allowed=(merged.animal_hue_n>=10)&(merged.wind_hue_n>=10)&(
        merged.source_all_5climate_variables_at_12_or_more_points.eq(1))&(
        merged.source_original_TDWG_polygon_geometry_repaired_sensitivity.eq(0))
    global_=merged.loc[allowed].sort_values("TDWG_L3").copy().reset_index(drop=True)
    bee=global_.loc[global_.GBIF_observed_Bombus_source_coverage&
         (global_[PRIMARY]>0)&(global_[CELLS]>=5)].copy().reset_index(drop=True)
    if len(global_)!=155 or len(bee)!=113:
        raise ValueError("STAGE89B_REAL_SOURCE_GLOBAL_155_BOMBUS_113_SAME_REGION_GATE_CHANGED")
    if not (global_.wind_hue_n>=10).all():
        raise ValueError("STAGE89B_WIND_FLORA_NOT_DOCU_FROZEN")
    return {"global":global_,"GBIF_positive_only":bee},gift_meta,support

def model_design(df,bee):
    columns=list(BASE_CONTROLS)+(["log_bombus_richness","log_gbif_cells","wind_x_bombus"] if bee else [])
    X=pd.DataFrame(index=df.index)
    for col in columns:
        a=np.asarray(df[col],float)
        if not np.isfinite(a).all() or np.std(a)<1e-12:
            raise ValueError("STAGE89B_GIFT_SOURCE_MISSING_OR_CONSTANT_CONTROL_"+col)
        X[col]=(a-a.mean())/a.std(ddof=0)
    if bee:X["wind_x_bombus"]=X["wind"]*X["log_bombus_richness"]
    X.insert(0,"const",1.)
    if np.linalg.matrix_rank(X.to_numpy(float))!=X.shape[1]:
        raise ValueError("STAGE89B_COLLINEAR_SOURCE_GIFT_GEO_DESIGN")
    return X

def full_hue_table(df):
    output=[];names=[]
    for aggregation,suffix in AGG:
        for hue in COLORS_ALL:
            an=np.asarray(df[f"animal_hue_{hue}_{suffix}"],float)
            wi=np.asarray(df[f"wind_hue_{hue}_{suffix}"],float)
            if not (np.isfinite(an).all() and np.isfinite(wi).all()):
                raise ValueError("STAGE89B_GIFT_WIND_ANIMAL_HUE_MISSING_NOT_ZERO")
            if not (np.all((0<=an)&(an<=1)) and np.all((0<=wi)&(wi<=1))):
                raise ValueError("STAGE89B_HUE_SOURCE_OUTSIDE_0_TO_1")
            output.extend((an,wi,an-wi))
            names.extend(((aggregation,hue,"animal"),
                          (aggregation,hue,"wind"),
                          (aggregation,hue,"animal_minus_wind")))
    Y=np.column_stack(output)
    if Y.shape!=(len(df),66):
        raise ValueError("STAGE89B_11_X_2_X_3_SOURCE_OUTCOMES_CHANGED")
    return Y,names

def geographically_blocked_beta(df,X,Y,latitude_bin,longitude_bin,reps,seed):
    b=source_blocks(df,latitude_bin,longitude_bin)
    _,inv=np.unique(b,axis=0,return_inverse=True)
    groups=[np.where(inv==i)[0] for i in np.unique(inv)]
    if len(groups)<10:
        raise ValueError("STAGE89B_NOT_10_GEO_BLOCKS_FOR_SOURCE_BOTANICAL_PAIRS")
    rng=np.random.default_rng(seed)
    x=X.to_numpy(float);out=[]
    for i in range(reps):
        sampled=rng.integers(0,len(groups),size=len(groups))
        idx=np.concatenate([groups[j] for j in sampled])
        if len(idx)<x.shape[1]+10:continue
        beta,_,rank,_=np.linalg.lstsq(x[idx],Y[idx],rcond=None)
        if rank==x.shape[1]:out.append(beta)
    if len(out)<reps*.7:
        raise ValueError("STAGE89B_TOO_FEW_IDENTIFIABLE_GEOGRAPHY_BLOCK_BOOTSTRAPS")
    return np.array(out),len(groups)

def analyze_case(df,scope,geoboot=999):
    bee=scope=="GBIF_positive_only"
    X=model_design(df,bee)
    Y,names=full_hue_table(df)
    original_beta=np.linalg.lstsq(X.to_numpy(float),Y,rcond=None)[0]
    # Original source support for each hue by pollen vector: at least
    # 10 single-hue species overall per pollination arm, not per colour.
    bootstrap1,b1=geographically_blocked_beta(df,X,Y,20,45,geoboot,20261119)
    bootstrap2,b2=geographically_blocked_beta(df,X,Y,30,60,geoboot,20261120)
    termset=("wind","log_bombus_richness","wind_x_bombus") if bee else ("wind",)
    rows=[]
    for j,(agg,hue,mode) in enumerate(names):
        for term in termset:
            ix=list(X.columns).index(term)
            # HC3 is only exploratory region-level variance; paired
            # geographical resampling is the primary uncertainty.
            fit=sm.OLS(Y[:,j],X).fit(cov_type="HC3")
            rows.append({"scope":scope,"mode":mode,"averaging":agg,"hue":hue,
                "predictor":term,"n_source_regions":len(df),
                "mean_source_hue_fraction":float(np.mean(Y[:,j])),
                "original_partial_slope_frac_points_per_1sd":float(original_beta[ix,j]),
                "exploratory_HC3_p":float(fit.pvalues.iloc[ix]),
                "geoblock_20x45_95":[float(v) for v in np.quantile(bootstrap1[:,ix,j],[.025,.975])],
                "geoblock_30x60_95":[float(v) for v in np.quantile(bootstrap2[:,ix,j],[.025,.975])],
                "mode_trait_not_same_local_population_as_source_bee_observation":True})
    # Multiplicity across predeclared hue families, separately by data scope,
    # aggregation, mode and predictor. Does not correct previous exploration.
    for (_,_,term),group in __import__("itertools").groupby([],lambda x:x):pass
    from collections import defaultdict
    buckets=defaultdict(list)
    for i,r in enumerate(rows):
        buckets[(r["averaging"],r["mode"],r["predictor"])].append(i)
    for keys,ii in buckets.items():
        p=[rows[i]["exploratory_HC3_p"] for i in ii]
        adj=multipletests(p,method="fdr_bh")[1]
        for i,v in zip(ii,adj):rows[i]["exploratory_BH_11_hues"]=float(v)
    summary={"scope":scope,"n_original_regions":len(df),
       "n_source_geoblocks_20x45":b1,"n_source_geoblocks_30x60":b2,
       "n_bootstrap20_success":len(bootstrap1),"n_bootstrap30_success":len(bootstrap2),
       "source_original_11_source_hues":len(COLORS_ALL),
       "source_outcomes_2_aggregations_3_modes":len(names),
       "note":"'animal_minus_wind' response is the within-region difference, not a phylogenetically replicated transition"}
    return rows,summary

def run(gift_zip,climate_zip,bombus_zip,outdir,bootstrap=999):
    frames,metadata,source=matched_native_mode_frames(gift_zip,climate_zip,bombus_zip)
    results=[];summaries=[]
    for scope,df in frames.items():
        r,s=analyze_case(df,scope,bootstrap)
        results.extend(r);summaries.append(s)
    if len(results)!=264:
        raise ValueError("STAGE89B_EXPECTED_66_WIND_AND_66_X3_BEE_MODE_SIGNAL_RESULTS")
    outdir.mkdir(parents=True,exist_ok=True)
    import csv
    with (outdir/"stage89B_original_155_global_113bee_GIFT_mode_hue_wind_Bombus_geoblocks.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]))
        w.writeheader()
        for r in results:w.writerow({k:json.dumps(v) if isinstance(v,list) else v for k,v in r.items()})
    report={"schema":"stage89B_global_GIFT32_animal_vs_wind_source_pollination_mode_geographic_correspondence",
      "original_GIFT_derived_artifact_sha256":GIFT_SOURCE_SHA,
      "original_Stage87C_source_climate_artifact_SHA256":WCVP_CLIMATE_ZIP_SHA,
      "original_Stage87D_Bombus_source_artifact_SHA256":BOMBUS_ZIP_SHA,
      "original_spectrometer_vs_plant_gene_comparison_not_performed":True,
      "actual_source_common_pollination_mode_regional_design":summaries,
      "source_controlled_original_global_TDWG_native":source,
      "source_GIFT_original_pollination_mode_n":metadata["source_mapped_original_species_coverage"],
      "source_Bombus_positive_region_not_source_confirmed_native_populations":True,
      "source_WorldClim1970_2000_not_true_flower_wind":True,
      "source_compiled_pollination_mode_not_local_field_plant_pollination":True,
      "source_region_repeated_species_not_independent_plant_phylogenetic_origins":True,
      "source_hue_words_not_honeybee_far_near_vision":True,
      "source_no_odor_learning_landing_pollen_fitness_measured":True}
    (outdir/"stage89B_GIFT_animal_wind_native_floral_global_spatial_receipt.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    for scope in SCOPES:
        out=[r for r in results if r["scope"]==scope and r["mode"] in ("animal","wind","animal_minus_wind")
                and r["averaging"]=="genus_balanced" and r["hue"] in ("yellow","purple","green","brown") and
                r["predictor"] in ("wind","log_bombus_richness")]
        print("STAGE89B_SOURCE_GIFT_MODE_REGION_SPATIAL",scope,json.dumps([
            {"mode":x["mode"],"hue":x["hue"],"term":x["predictor"],
            "beta":x["original_partial_slope_frac_points_per_1sd"],
            "block20":x["geoblock_20x45_95"],
            "BH_q":x["exploratory_BH_11_hues"]} for x in out],sort_keys=True),flush=True)
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-GIFT32-global-modes-zip",type=Path,required=True)
    p.add_argument("--source-Stage87C-climate-zip",type=Path,required=True)
    p.add_argument("--source-Stage87D-GBIF-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--bootstrap-reps",type=int,default=999)
    a=p.parse_args()
    run(a.source_GIFT32_global_modes_zip,a.source_Stage87C_climate_zip,
        a.source_Stage87D_GBIF_zip,a.outdir,a.bootstrap_reps)
if __name__=="__main__":main()
