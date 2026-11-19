"""Stage90B: SAME global regions, same covariates and same geo-block draws,
two source floral-mode composition weights: original and inverse species
native-TDWG-range breadth. Recompute conditional WIND-hue and recorded
Bombus-richness associations in 155 common-mode global regions and 113
GBIF positive regions, subject to original eligibility and visual-source
documentation.

Sources: Stage90A author NHM/GIFT/Kew re-derived native range species weights;
Stage89 original GIFT mode source; Stage87 original WorldClim 1970-2000 and
GBIF 3,958,417 archived positive bumblebee occurrences. All SHA verified.
An original species repeated in several TDWG regions remains a single
biological species; inverse native range is only sensitivity, not phylogeny.

No falsely observed absence, no sensory order from visual floral prose,
no tested VOC wind plume, learning, bee behaviour, pollen transfer, landing
or fitness. Do not promote inferential p from retrospective spatial checks.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,sys,zipfile
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage87"))
sys.path.insert(0,str(BASE/"floral_macro_stage89"))
from compare_gift_animal_wind_hue_geographic_regimes import (
    matched_native_mode_frames,model_design,full_hue_table,
    COLORS_ALL,AGG,SCOPES
)
from analyze_global_hue_wind_bombus_spatial_overlap import source_blocks

STAGE90A_SHA="523c0369483af34f702157021066174ed503c77c322fb1fa3ca88dcc2dbbe2fa"
STAGE90A_MEMBER="stage90_original_367_TDWG_GIFT_modes_inverse_native_range_hues.csv"
STAGE90A_RECEIPT="stage90_source_native_range_breadth_genus_support_receipt.json"
GIFT_ZIP_SHA="26ffa12c78a583743735d89575b6b8d4c4066a01da5b2a7e54aea531915bb7a8"
CLIMATE_ZIP_SHA="4c0ab25596078be4b2aa35a254e42695fd260e1720864e173970aac8aa7db83a"
BOMBUS_ZIP_SHA="2fe7510fe8c08189d63151fe255a00baafb96c7acc87d3d0fedc970966ca1a43"

def input_range_table(path):
    b=Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=STAGE90A_SHA:
        raise ValueError("STAGE90B_STAGE90A_NATIVE_RANGE_COMPOSITION_SHA_CHANGED")
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        src=pd.read_csv(io.BytesIO(z.read(STAGE90A_MEMBER)))
        audit=json.loads(z.read(STAGE90A_RECEIPT))
    if len(src)!=734 or src.duplicated(["TDWG_L3","pollination_mode"]).any() or (
         set(src.pollination_mode)!={"animal","wind"}):
        raise ValueError("STAGE90B_REAL_367_TDWG_X_2_ORIGINAL_MODES_CHANGED")
    if not audit["source_original_prior_367x3_GIFT_hue_fractions_all_reproduced"]:
        raise ValueError("STAGE90B_ORIGINAL_STAGE89_MODE_HUE_REGRESSION_FAILED")
    return src,audit

def adjusted_mode_outcomes(frame,range_table):
    source={m:range_table.loc[range_table.pollination_mode==m].set_index("TDWG_L3")
            for m in ("animal","wind")}
    sample_ids=list(frame.TDWG_L3)
    if not (set(sample_ids)<=set(source["animal"].index) and
            set(sample_ids)<=set(source["wind"].index)):
        raise ValueError("STAGE90B_SOURCE_INVERSE_BREADTH_UNMATCHED_TDWG_REGION")
    out=[]
    names=[]
    diagnostics={}
    for aggregation,suffix in AGG:
        for h in COLORS_ALL:
            values=[]
            for mode in ("animal","wind"):
                source_col=f"hue_{h}_{'genus_equal' if aggregation=='genus_balanced' else 'pooled'}_inverse_native_range"
                vals=source[mode].loc[sample_ids,source_col].to_numpy(float)
                if not np.isfinite(vals).all() or np.any((vals<0)|(vals>1)):
                    raise ValueError("STAGE90B_SOURCE_INVERSE_WEIGHT_HUE_NA_OR_INVALID_"+mode+"_"+h)
                values.append(vals)
            out.extend((values[0],values[1],values[0]-values[1]))
            names.extend(((aggregation,h,"animal"),(aggregation,h,"wind"),
                          (aggregation,h,"animal_minus_wind")))
    mat=np.column_stack(out)
    if mat.shape!=(len(frame),66):raise ValueError("STAGE90B_MODE_HUE_66_OUTCOMES_CHANGED")
    return mat,names

def paired_geo_bootstrap(frame,X,Y0,Y1,size_lat,size_lon,reps,seed):
    block=source_blocks(frame,size_lat,size_lon)
    _,inv=np.unique(block,axis=0,return_inverse=True)
    groups=[np.where(inv==i)[0] for i in sorted(set(inv))]
    if len(groups)<10:raise ValueError("STAGE90B_INDEPENDENT_GEO_BLOCKS_LESS_THAN10")
    rng=np.random.default_rng(seed)
    x=X.to_numpy(float)
    concat=np.column_stack([Y0,Y1])
    samples=[]
    for _ in range(reps):
        selected=rng.integers(0,len(groups),size=len(groups))
        ii=np.concatenate([groups[k] for k in selected])
        if len(ii)<x.shape[1]+10:continue
        betas,_,rank,_=np.linalg.lstsq(x[ii],concat[ii],rcond=None)
        if rank!=x.shape[1]:continue
        samples.append(betas.reshape(x.shape[1],2,66))
    if len(samples)<.75*reps:
        raise ValueError("STAGE90B_TOO_FEW_GEO_BLOCK_SAMPLES_WITH_FULL_DESIGN_RANK")
    return np.asarray(samples),len(groups)

def analyze_case(frame,scope,weighted,georeps=999):
    include_bee=scope=="GBIF_positive_only"
    X=model_design(frame,include_bee)
    Y0,names=full_hue_table(frame)
    Y1,weighted_names=adjusted_mode_outcomes(frame,weighted)
    if names!=weighted_names or Y0.shape!=Y1.shape:
        raise ValueError("STAGE90B_ORIGINAL_AND_WEIGHTED_SOURCE_SAME_MODE_HUE_ORDER_CHANGED")
    concat=np.column_stack((Y0,Y1))
    beta=np.linalg.lstsq(X.to_numpy(float),concat,rcond=None)[0].reshape(X.shape[1],2,66)
    bootfine,nf=paired_geo_bootstrap(frame,X,Y0,Y1,20,45,georeps,20261119)
    bootcoarse,nc=paired_geo_bootstrap(frame,X,Y0,Y1,30,60,georeps,20261120)
    terms=["wind"]+(["log_bombus_richness","wind_x_bombus"] if include_bee else [])
    results=[];nonidentified=[]
    for j,(agg,hue,mode) in enumerate(names):
        # For source animal-minus-wind DIFFERENCE a negative value is
        # informative, not a lack of documented flower hue. Separate the
        # denominators to avoid counting only positive differences.
        source_hue0=int((Y0[:,j]>0).sum()) if mode!="animal_minus_wind" else None
        source_hue1=int((Y1[:,j]>0).sum()) if mode!="animal_minus_wind" else None
        source_diff0=int((np.abs(Y0[:,j])>1e-12).sum()) if mode=="animal_minus_wind" else None
        source_diff1=int((np.abs(Y1[:,j])>1e-12).sum()) if mode=="animal_minus_wind" else None
        estimable=(np.std(Y0[:,j])>1e-12 and np.std(Y1[:,j])>1e-12)
        if not estimable:nonidentified.append({"aggregation":agg,"hue":hue,"mode":mode,
            "source_hue_positive_unweighted":source_hue0,
            "source_hue_positive_inverse_range":source_hue1,
            "original_mode_difference_nonzero":source_diff0,
            "inverse_range_mode_difference_nonzero":source_diff1})
        for term in terms:
            k=list(X.columns).index(term)
            if estimable:
                val0=float(beta[k,0,j]);val1=float(beta[k,1,j])
                bf0=bootfine[:,k,0,j];bf1=bootfine[:,k,1,j]
                bc0=bootcoarse[:,k,0,j];bc1=bootcoarse[:,k,1,j]
                def interval(v):return [float(x) for x in np.quantile(v,[.025,.975])]
            else:val0=val1=None
            results.append({
                "region_scope":scope,"aggregation":agg,"hue":hue,
                "mode":mode,"source_wind_or_Bombus_term":term,
                "original_source_region_count":len(frame),
                "original_source_hue_positive_regions":source_hue0,
                "range_weighted_source_hue_positive_regions":source_hue1,
                "original_source_mode_difference_nonzero_regions":source_diff0,
                "inverse_range_source_mode_difference_nonzero_regions":source_diff1,
                "source_status":"DESCRIPTIVE_ESTIMABLE" if estimable else "SOURCE_UNINFORMATIVE_NO_HUE_VARIATION",
                "unweighted_source_beta":val0,
                "inverse_native_range_breadth_source_beta":val1,
                "inverse_range_minus_unweighted_source_beta":(
                    val1-val0 if estimable else None),
                "original_fine_geo_20x45_source_beta_95":interval(bf0) if estimable else None,
                "inverse_range_fine_geo_20x45_source_beta_95":interval(bf1) if estimable else None,
                "source_paired_range_weight_change_fine_geo_20x45_95":interval(bf1-bf0) if estimable else None,
                "original_coarse_geo_30x60_source_beta_95":interval(bc0) if estimable else None,
                "inverse_range_coarse_geo_30x60_source_beta_95":interval(bc1) if estimable else None,
                "source_paired_range_weight_change_coarse_geo_30x60_95":interval(bc1-bc0) if estimable else None,
                "source_original_not_independent_phylogenetic_contrasts":True})
    return results,{"scope":scope,"original_regions":len(frame),
      "source_geoblocks_20x45":nf,"source_geoblocks_30x60":nc,
      "successful_paired_geo_bootstrap_20x45":len(bootfine),
      "successful_paired_geo_bootstrap_30x60":len(bootcoarse),
      "source_uninformative_original_hue_mode_series":nonidentified,
      "sample_geography_and_climate_predictors_unchanged_between_two_weighting_schemes":True}

def run(range_zip,gift_zip,climate_zip,bombus_zip,outdir,reps=999):
    range_matrix,range_qc=input_range_table(range_zip)
    frames,gift_qc,source=matched_native_mode_frames(gift_zip,climate_zip,bombus_zip)
    if len(frames["global"])!=155 or len(frames["GBIF_positive_only"])!=113:
        raise ValueError("STAGE90B_PRIOR_GIFT_ANIMAL_WIND_REGION_FRAME_CHANGED")
    allrows=[];scopes=[]
    for scope,frame in frames.items():
        rows,meta=analyze_case(frame,scope,range_matrix,reps)
        allrows.extend(rows);scopes.append(meta)
    if len(allrows)!=264:
        raise ValueError("STAGE90B_PREDECLARED_264_SOURCE_REGIONAL_PAIR_COMPARISONS_CHANGED")
    outdir.mkdir(exist_ok=True,parents=True)
    with (outdir/"stage90_original_global_range_breadth_weighted_hue_spatial_paired.csv").open(
         "w",encoding="utf-8",newline="") as h:
        names=sorted({k for r in allrows for k in r})
        w=csv.DictWriter(h,fieldnames=names);w.writeheader()
        w.writerows([{k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v
            for k,v in r.items()} for r in allrows])
    keyout=[]
    for scope,hue,term in [
      ("global","brown","wind"),("global","green","wind"),
      ("GBIF_positive_only","yellow","log_bombus_richness"),
      ("GBIF_positive_only","purple","log_bombus_richness"),
      ("GBIF_positive_only","white","wind_x_bombus")]:
        for mode in ("animal","wind","animal_minus_wind"):
            xs=[r for r in allrows if r["region_scope"]==scope and
                r["aggregation"]=="genus_balanced" and r["hue"]==hue and
                r["mode"]==mode and r["source_wind_or_Bombus_term"]==term]
            if len(xs)!=1:raise ValueError("STAGE90B_PREDECLARED_FIVE_MAJOR_SOURCE_COMPARISONS_MISSING")
            keyout.append(xs[0])
    r={"schema":"stage90B_true_WCVP_GIFT_native_55k_inverse_species_breadth_spatial_falsification",
      "source_original_stage90A_SHA":STAGE90A_SHA,
      "source_original_Stage89_GIFT_SHA":GIFT_ZIP_SHA,
      "source_original_Stage87_WorldClim_SHA":CLIMATE_ZIP_SHA,
      "source_original_Stage87_GBIF_Bombus_SHA":BOMBUS_ZIP_SHA,
      "source_native_plant_range_breadth_support":{k:v for k,v in range_qc.items()
          if k in ("source_mode_arm_range_and_hue_support",
             "source_genera_with_both_animal_and_wind_modes",
             "source_genera_with_both_modes_and_explicit_hue_in_both",
             "original_regions_with_any_both_mode_hue_genus")},
      "original_scope_counts_and_geoblock_quality":scopes,
      "source_frozen_six_main_sensitivity_contrasts":keyout,
      "source_original_all_hue_families":len(COLORS_ALL),
      "source_one_species_in_many_TDWG_regions_not_independent_evolution":True,
      "inverse_range_reweighting_NOT_phylogenetic_GLS_or_independent_transitions":True,
      "source_GBIF_absence_not_imputed_nor_target_group_effort_measured":True,
      "source_Floral_hue_text_not_actual_recognition_distance_nectar_guide_or_odour":True,
      "source_real_wind_on_flower_landings_cognitive_cost_fitness_NOT_measured":True,
      "no_confirmatory_causal_wind_x_pollinator_hierarchy_estimated":True}
    (outdir/"stage90_source_range_reweighted_global_spatial_receipt.json").write_text(
        json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("STAGE90_SOURCE_GLOBAL_RANGE_REWEIGHT_SPATIAL_RESULTS",json.dumps({
      "source_genera_with_both_modes":r["source_native_plant_range_breadth_support"]["source_genera_with_both_animal_and_wind_modes"],
      "scopes":scopes,"key_contrasts":[{"scope":x["region_scope"],"mode":x["mode"],
        "hue":x["hue"],"term":x["source_wind_or_Bombus_term"],
        "original_beta":x["unweighted_source_beta"],
        "rangeweighted_beta":x["inverse_native_range_breadth_source_beta"],
        "rangeweighted_coarse_geo95":x["inverse_range_coarse_geo_30x60_source_beta_95"],
        "paired_delta_coarse95":x["source_paired_range_weight_change_coarse_geo_30x60_95"]}
        for x in keyout]},sort_keys=True),flush=True)
    return r

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage90A-source-range-zip",type=Path,required=True)
    p.add_argument("--stage89-source-mode-zip",type=Path,required=True)
    p.add_argument("--stage87C-source-climate-zip",type=Path,required=True)
    p.add_argument("--stage87D-source-Bombus-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--geographic-bootstrap-reps",type=int,default=999)
    z=p.parse_args();run(z.stage90A_source_range_zip,z.stage89_source_mode_zip,
        z.stage87C_source_climate_zip,z.stage87D_source_Bombus_zip,z.outdir,z.geographic_bootstrap_reps)
if __name__=="__main__":main()
