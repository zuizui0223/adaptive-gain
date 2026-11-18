"""Stage88E: ORIGINAL native-flora family leave-outs with PAIRED geo-blocks.

All three conditions use the SAME real 268 global or 138 observed-Bombus
regions and frozen baseline covariates. The analyzed variable is NHM
lexically described hue composition, not sensory use, wind pollination mode,
biological zero visits, nectar guides, odor dispersion, or plant fitness.

This is taxonomy exclusion sensitivity, NOT species' directly measured
animal-versus-wind pollen vector mode. Source raw 55,775 native taxa,
WCVP official family names, original WorldClim and GBIF archived species.
"""
from __future__ import annotations
import argparse,hashlib,io,json,zipfile,sys
from pathlib import Path
import numpy as np,pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage87"))
from analyze_global_hue_wind_bombus_spatial_overlap import (
    source_join,source_design,source_blocks,COLORS,PRIMARY,CELLS,
    WCVP_CLIMATE_ZIP_SHA,BOMBUS_ZIP_SHA,
)
SOURCE_FAMILY_SHA="4451986d53f653cb96966d0595765d2c7806fb81057177be65ccfb3d2519e7d2"
SOURCE_MEMBER="stage88D_global_TDWG3_native_flora_hue_three_family_exclusion_designs.csv"
DESIGNS=("all_original_source_taxa","exclude_three_graminoid_families",
         "exclude_graminoid_plus_nine_wind_enriched_families")
AGG=("fraction_of_exclusive_documented","mean_of_genus_fractions")
TERMS_BASE=("wind",)
TERMS_BEE=("wind","log_bombus_richness","wind_x_bombus")

def source_family(path):
    b=Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=SOURCE_FAMILY_SHA:
        raise ValueError("STAGE88E_FROZEN_REAL_WCVP_FAMILY_ARTIFACT_SHA_DRIFT")
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        df=pd.read_csv(io.BytesIO(z.read(SOURCE_MEMBER)))
    if len(df)!=1101 or set(df.source_exclusion_sensitivity)!=set(DESIGNS):
        raise ValueError("STAGE88E_SOURCE_367_X_THREE_FAMILY_MODES_CHANGED")
    if df.duplicated(["TDWG_L3","source_exclusion_sensitivity"]).any():
        raise ValueError("STAGE88E_DUPLICATE_SOURCE_REGION_FAMILY_MODE")
    return df

def matched_frames(native_zip,bee_zip,family):
    merged,glob,bees,orig=source_join(native_zip,bee_zip)
    local={}
    for d in DESIGNS:
        t=family.loc[family.source_exclusion_sensitivity==d].set_index("TDWG_L3")
        local[d]=t
    allowed=set(glob.TDWG_L3)
    for t in local.values():
        allowed&=set(t.index[t.n_source_single_explicit_hue>=50])
    global_f=glob[glob.TDWG_L3.isin(allowed)].sort_values("TDWG_L3").reset_index(drop=True)
    bee_f=bees[bees.TDWG_L3.isin(allowed)].sort_values("TDWG_L3").reset_index(drop=True)
    if len(global_f)!=268 or len(bee_f)!=138:
        raise ValueError("STAGE88E_REAL_COMMON_SOURCE_268_138_DOMAIN_CHANGED")
    return {"global":global_f,"bee_record_positive_only":bee_f},local,orig

def responses(frame,family):
    cols=[f"hue_{h}_{s}" for s in AGG for h in COLORS]
    out={}
    for key in DESIGNS:
        q=family[key].loc[list(frame.TDWG_L3)]
        a=q[cols].to_numpy(float)
        if a.shape!=(len(frame),22) or not np.isfinite(a).all() or a.min()<0 or a.max()>1:
            raise ValueError("STAGE88E_SOURCE_LEXICAL_COLOUR_UNOBSERVED_NOT_ZERO")
        out[key]=(a,q)
    return out,cols

def paired_region_bootstrap(frame,X,y,n_rep,lat_size,lon_size,seed):
    part=source_blocks(frame,lat_size,lon_size)
    _,index=np.unique(part,axis=0,return_inverse=True)
    groups=[np.where(index==k)[0] for k in sorted(set(index))]
    if len(groups)<12:raise ValueError("STAGE88E_TOO_FEW_GEOGRAPHIC_BLOCKS")
    rng=np.random.default_rng(seed)
    Y=np.concatenate([y[k][0] for k in DESIGNS],axis=1)
    raw=[]
    for i in range(n_rep):
        chosen=rng.integers(0,len(groups),size=len(groups))
        ids=np.concatenate([groups[j] for j in chosen])
        if len(ids)<=X.shape[1]+10:continue
        beta,_,rank,_=np.linalg.lstsq(X[ids],Y[ids],rcond=None)
        if rank==X.shape[1]:raw.append(beta)
    if len(raw)<.8*n_rep:raise ValueError("STAGE88E_SOURCE_GEO_RESAMPLING_RANK_LOST")
    return np.stack(raw).reshape(len(raw),X.shape[1],3,22),len(groups)

def analyze(family_zip,native_zip,bee_zip,out,boot=999):
    family=source_family(family_zip)
    frames,maps,orig=matched_frames(native_zip,bee_zip,family)
    result=[];meta=[]
    for frame_name,frame in frames.items():
        with_bees=frame_name!="global"
        X=source_design(frame,with_bees)
        matrix=X.to_numpy(float)
        y,columns=responses(frame,maps)
        fitted={k:np.linalg.lstsq(matrix,y[k][0],rcond=None)[0] for k in DESIGNS}
        # Outcome-only ablation is the PRIMARY estimand. In another
        # sensitivity, restandardize source metadata coverage per exclusion.
        controls={}
        for k in DESIGNS:
            altered=frame.copy()
            vals=y[k][1]
            altered["source_coverage"]=vals.source_documented_colour_coverage_fraction.to_numpy(float)
            altered["log_plant_hues"]=np.log1p(vals.n_source_single_explicit_hue.to_numpy(float))
            xx=source_design(altered,with_bees)
            controls[k]=np.linalg.lstsq(xx.to_numpy(float),y[k][0],rcond=None)[0]
        small,bs=paired_region_bootstrap(frame,matrix,y,boot,20,45,20261118)
        large,bl=paired_region_bootstrap(frame,matrix,y,boot,30,60,20261119)
        terms=TERMS_BEE if with_bees else TERMS_BASE
        for j,field in enumerate(columns):
            hue=next(h for h in COLORS if field.startswith("hue_"+h+"_"))
            aggregation="genus_balanced" if field.endswith("mean_of_genus_fractions") else "species_pooled"
            for term in terms:
                ti=list(X.columns).index(term)
                baseline=fitted[DESIGNS[0]][ti,j]
                for i,cond in enumerate(DESIGNS):
                    beta=fitted[cond][ti,j]
                    a=small[:,ti,i,j];b=large[:,ti,i,j]
                    da=a-small[:,ti,0,j];db=b-large[:,ti,0,j]
                    result.append({
                      "scope":frame_name,"hue":hue,"aggregation":aggregation,
                      "term":term,"family_exclusion":cond,"original_regions":len(frame),
                      "beta_fixed_covariates":float(beta),
                      "beta_recomputed_coverage_covariates":float(controls[cond][ti,j]),
                      "delta_to_all_native_species":float(beta-baseline),
                      "geoblock20x45_beta_95":[float(v) for v in np.quantile(a,[.025,.975])],
                      "geoblock30x60_beta_95":[float(v) for v in np.quantile(b,[.025,.975])],
                      "geoblock20x45_paired_delta_95":[float(v) for v in np.quantile(da,[.025,.975])],
                      "geoblock30x60_paired_delta_95":[float(v) for v in np.quantile(db,[.025,.975])]})
        meta.append({"scope":frame_name,"n_source_common_original_regions":len(frame),
            "n_geographic_blocks_20x45":bs,"n_geographic_blocks_30x60":bl,
            "n_valid_bootstrap20":len(small),"n_valid_bootstrap30":len(large),
            "covariate_columns":list(X.columns)})
    if len(result)!=264:raise ValueError("STAGE88E_NOT_264_FROZEN_SOURCE_FAMILY_COMPARISONS")
    out.mkdir(parents=True,exist_ok=True)
    import csv
    with (out/"stage88E_268global_138bee_source_family_spatial_comparison.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(result[0]))
        writer.writeheader()
        for row in result:
            writer.writerow({k:json.dumps(v) if isinstance(v,list) else v for k,v in row.items()})
    receipt={"schema":"stage88E_original_NHM_Kew_WCVP_family_leaveout_real_paired_geographical_bootstrap",
       "source_file_SHA256":{"family_source":SOURCE_FAMILY_SHA,
         "Stage87C_climate_source":WCVP_CLIMATE_ZIP_SHA,
         "Stage87D_bombus_source":BOMBUS_ZIP_SHA},
       "original_source_region_gates":orig,
       "source_global_and_bee_scope":meta,
       "source_original_family_conditions":list(DESIGNS),
       "source_source_species_wind_pollination_mode_NOT_verified":True,
       "source_GBIF_nonrecorded_regions_not_true_absence":True,
       "source_macro_flora_range_repetition_not_independent_evolution":True,
       "no_wind_odor_plume_learning_near_guide_landing_fitness_measured":True}
    (out/"stage88E_original_paired_global_flora_family_spatial_receipt.json").write_text(
       json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    for frame_name in frames:
        rows=[r for r in result if r["scope"]==frame_name and r["aggregation"]=="genus_balanced"
              and r["hue"] in ("yellow","purple","green","brown") and
              r["term"] in ("wind","log_bombus_richness")]
        print("STAGE88E_SOURCE_VERIFIED_PAIRED_ABLATION",frame_name,json.dumps(
           [{"hue":r["hue"],"term":r["term"],"family":r["family_exclusion"],
             "beta":r["beta_fixed_covariates"],"delta":r["delta_to_all_native_species"],
             "delta_block_95":r["geoblock20x45_paired_delta_95"]} for r in rows],sort_keys=True),flush=True)
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage88D-family-zip",type=Path,required=True)
    p.add_argument("--stage87C-climate-zip",type=Path,required=True)
    p.add_argument("--stage87D-GBIF-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--geoblock-reps",type=int,default=999)
    a=p.parse_args()
    analyze(a.stage88D_family_zip,a.stage87C_climate_zip,
            a.stage87D_GBIF_zip,a.outdir,a.geoblock_reps)
if __name__=="__main__":main()
