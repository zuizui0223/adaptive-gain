"""Stage66 source-measured global floral-colour × source-modelled bee guild HEX macro.

NEVER equate coarse human-visible ROI colour with spatial UV/nectar guides.
Use original FCP 447,500 photo rows/4,475 taxa, original source 2,695
eligible bee HEX, WorldClim BIO5/BIO12, exact author source HEX polygons.
No present-day range model is evidence of visited pollinators, evolved
visual information use or historic native plant-pollinator co-occurrence.
"""
from __future__ import annotations
import argparse,hashlib,io,json,zipfile
from pathlib import Path
import numpy as np
import pandas as pd

PHOTO_SHA="8e7f10f0427927208485b2da6fa9c46bb681d6f3611e53b8dfdc606cfc8dabe6"
BEES_SHA="d260b18be05a2ceac87a49fddd0645734d56c6246f80321c1c577f261dd5cee4"
BIO_SHA="00513224583665ec0f2f955a4ec252730c4deb2004cce9e793492a3f26df4dcf"
COLORS=("white","yellow_orange","red_pink","blue_purple")

def check(cond,why):
    if not cond:raise ValueError("STAGE66_NO_GO_"+why)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(2**20),b""):h.update(b)
    return h.hexdigest()

def source_photos(path):
    check(sha(path)==PHOTO_SHA,"ORIGINAL_FCP_GZIP_SHA")
    needed=["photo_id","inat_taxon_id","species","latitude","longitude",
            "positional_accuracy_m","morph","global_classifiable","fcp_source_cohort"]
    d=pd.read_csv(path,usecols=needed,low_memory=False)
    check(len(d)==447500 and d.inat_taxon_id.nunique()==4475
          and d.photo_id.nunique()==447500,"ORIGINAL_FCP_DENOMINATORS")
    check(d.groupby("inat_taxon_id").size().eq(100).all(),
          "ORIGINAL_FCP_EACH_SOURCE_SPECIES_100")
    check(d[["inat_taxon_id","species"]].drop_duplicates().shape[0]==4475,
          "TAXON_ID_NAME_NOT_ONE_TO_ONE")
    selected=d.global_classifiable.fillna(False).astype(str).str.lower().isin(["1","true","yes"])
    check(int(selected.sum())==227107,"ORIGINAL_CLASSIFIABLE_COUNT")
    d=d.loc[selected].copy()
    check(d.morph.isin(COLORS).all(),"ORIGINAL_FOUR_COLOUR_STATE")
    for name in ("latitude","longitude","positional_accuracy_m"):
        d[name]=pd.to_numeric(d[name],errors="coerce")
    d["coordinate_qualified"]=(d.latitude.between(-90,90)&d.longitude.between(-180,180)
           &d.positional_accuracy_m.between(0,5000))
    return d,{"source_photos":447500,"source_species":4475,
              "four_state_classified":227107,
              "qualified_photo_coordinates_accuracy_max5000m":int(d.coordinate_qualified.sum()),
              "ineligible_photo_coordinate_or_accuracy":int((~d.coordinate_qualified).sum()),
              "original_FCP_SHA256":PHOTO_SHA}

def source_bee_model(path):
    check(sha(path)==BEES_SHA,"ORIGINAL_FILTERED_BEE_CSV_SHA")
    b=pd.read_csv(path)
    check(len(b)==10242 and b.source_siteid.is_unique,"AUTHOR_HEX10242_IDS")
    ok=b.eligibility.eq("AUTHOR_TREE_AND_PA_CELL_CUTOFF")
    check(int(ok.sum())==2695,"AUTHOR_PHYLOGENY_CUTOFF_HEX2695")
    b0="n_source_tree_and_pa_cutoff_Bombus_taxa"
    allb="n_source_tree_and_pa_cutoff_all_bee_taxa"
    check(b.loc[~ok,b0].isna().all() and b.loc[~ok,allb].isna().all(),
          "SOURCE_INELIGIBLE_MUST_REMAIN_UNKNOWN_NOT_BEE_ZERO")
    x=b.loc[ok,["source_siteid",b0,allb]].copy()
    x=x.rename(columns={b0:"n_Bombus",allb:"n_all_bee"})
    check((x.n_all_bee>=5).all() and (x.n_Bombus>=0).all()
          and (x.n_Bombus<=x.n_all_bee).all(),"MODELLED_SOURCE_COUNTS_INVALID")
    x["Bombus_fraction"]=x.n_Bombus/x.n_all_bee
    x["log_bees"]=np.log1p(x.n_all_bee)
    return x,{"original_hex":10242,"author_eligible_hex":2695,
              "uncovered_hex_NOT_TRUE_ABSENCE":7547,
              "author_eligible_Bombus_positive_hex":int((x.n_Bombus>0).sum()),
              "author_eligible_Bombus_model_zero_hex":int((x.n_Bombus==0).sum()),
              "original_author_bee_table_SHA256":BEES_SHA}

def climate_at_photos(d,path):
    """Use exact FCP publication's source-locked WorldClim10m pixel geometry."""
    from PIL import Image
    check(sha(path)==BIO_SHA,"FCP_WORLDCLIM_2_1_BIO_ARCHIVE_SHA")
    valid=d.coordinate_qualified.to_numpy(bool)
    la=d.latitude.to_numpy(float);lo=d.longitude.to_numpy(float)
    rr=np.zeros(len(d),int);cc=np.zeros(len(d),int)
    rr[valid]=np.floor((90-la[valid])*6).astype(int)
    cc[valid]=np.floor((lo[valid]+180)*6).astype(int)
    valid &= (rr>=0)&(rr<1080)&(cc>=0)&(cc<2160)
    d=d.copy()
    with zipfile.ZipFile(path) as z:
        for bi in (5,12):
            name=f"wc2.1_10m_bio_{bi}.tif"
            check(name in z.namelist(),"NO_WORLDCLIM_BIO_"+str(bi))
            with Image.open(io.BytesIO(z.read(name))) as im:
                check(im.size==(2160,1080),"WORLDCLIM_RESOLUTION_DRIFT")
                tag=im.tag_v2
                check(np.allclose(tag.get(33550,()),(1/6,1/6,0),rtol=0,atol=1e-14),
                      "WORLDCLIM_PIXEL_SCALE")
                check(np.allclose(tag.get(33922,()),(0,0,0,-180,90,0),rtol=0,atol=1e-14),
                      "WORLDCLIM_PIXEL_ORIGIN")
                check(42113 in tag,"WORLDCLIM_MISSING_NODATA")
                a=np.asarray(im)
                nodata=np.asarray(float(str(tag[42113]).strip("\x00")),dtype=a.dtype).item()
            vals=np.full(len(d),np.nan)
            src=a[rr[valid],cc[valid]]
            vals[valid]=np.where((src!=nodata)&np.isfinite(src),src.astype(float),np.nan)
            if bi==5:check(not np.any(np.isfinite(vals)&((vals< -100)|(vals>100))),
                          "WORLDCLIM_BIO5_OUT_OF_RANGE")
            else:check(not np.any(np.isfinite(vals)&((vals<0)|(vals>20000))),
                       "WORLDCLIM_BIO12_OUT_OF_RANGE")
            d[f"BIO{bi}"]=vals
    return d,{"original_WorldClim_SHA256":BIO_SHA,
              "qualified_photos_with_BIO5_BIO12":int((d.BIO5.notna()&d.BIO12.notna()).sum()),
              "not_contemporaneous_pollinator_climate_cohort":True}

def original_polygon_match(d):
    """Existing source-MD5 verified Stage47 SHP+SHX+DBF+PRJ, no centroid shortcut."""
    from research.floral_visual_macro_stage47.align_uv_study_sites_to_bee_hex import (
       load_authenticated_shape_sources,polygons_from_original_shapefile)
    from shapely import points
    members,centroids,shas=load_authenticated_shape_sources()
    names,tree,transform,projection=polygons_from_original_shapefile(members,centroids)
    check(len(names)==10242 and len(set(names))==10242,"SOURCE_POLYGON_NAMES")
    valid=d.coordinate_qualified.to_numpy(bool)
    idxs=np.flatnonzero(valid)
    la=d.latitude.to_numpy(float);lo=d.longitude.to_numpy(float)
    ids=np.full(len(d),None,dtype=object)
    ambiguous=0
    for start in range(0,len(idxs),12000):
        ix=idxs[start:start+12000]
        xx,yy=transform.transform(lo[ix],la[ix])
        hits=tree.query(points(xx,yy),predicate="intersects")
        n=np.bincount(hits[0],minlength=len(ix))
        ambiguous+=int((n>1).sum())
        for k,j in zip(hits[0],hits[1]):
            if n[k]==1:ids[ix[k]]=names[int(j)]
    result=d.copy();result["source_hex_id"]=ids
    return result,{"original_10242_geometries_MDs":shas,
                   "geometry_reprojection":projection,
                   "n_photos_exactly_assigned_source_hex":int(pd.notna(ids).sum()),
                   "n_original_polygon_boundary_ambiguous_held_unknown":ambiguous,
                   "unassigned_qualified_points":int(valid.sum()-pd.notna(ids).sum()-ambiguous)}

def species_hex(d,bees):
    """Species×source grid sufficient statistics only; photo IDs not exported."""
    q=d.loc[d.source_hex_id.notna()].merge(bees,left_on="source_hex_id",
          right_on="source_siteid",how="inner",validate="many_to_one")
    check(not q.empty,"NO_SOURCE_PHOTOS_IN_AUTHORIZED_BEE_MODEL")
    grp=["inat_taxon_id","source_hex_id"]
    g=q.groupby(grp,observed=True,sort=True)
    cell=g.agg(species=("species","first"),cohort=("fcp_source_cohort","first"),
       n_photos=("photo_id","size"),lat=("latitude","mean"),lon=("longitude","mean"),
       BIO5=("BIO5","mean"),BIO12=("BIO12","mean"),
       n_Bombus=("n_Bombus","first"),n_all_bee=("n_all_bee","first"),
       Bombus_fraction=("Bombus_fraction","first"),log_bees=("log_bees","first")).reset_index()
    for colour in COLORS:
        fractions=q.morph.eq(colour).groupby([q.inat_taxon_id,q.source_hex_id],
                    sort=True,observed=True).mean().reset_index(name="frac")
        cell=cell.merge(fractions,on=grp,validate="one_to_one")
        cell=cell.rename(columns={"frac":"fraction_"+colour})
    cell["n_eligible_hex_this_plant_species"]=cell.groupby("inat_taxon_id").source_hex_id.transform("size")
    check(np.allclose(cell[["fraction_"+c for c in COLORS]].sum(axis=1),1),
          "MORPH_FRACTIONS_DO_NOT_SUM_ONE")
    return cell,{"classified_photos_in_eligible_model":len(q),
       "eligible_species":int(cell.inat_taxon_id.nunique()),
       "species_with_2plus_eligible_hex":int(cell.loc[cell.n_eligible_hex_this_plant_species>=2,"inat_taxon_id"].nunique()),
       "species_x_hex_units":len(cell),"eligible_hex_with_photos":int(cell.source_hex_id.nunique()),
       "classified_photos_outside_source_model_or_unassigned":int(len(d)-len(q)),
       "not_species_native_range_plant_presence_probability":True}

def covariates(f):
    la=f.lat.to_numpy(float);lo=f.lon.to_numpy(float)
    return np.column_stack([f.Bombus_fraction.to_numpy(float)/0.1,
       f.log_bees.to_numpy(float),la/30,np.abs(la)/30,
       np.sin(np.deg2rad(lo)),np.cos(np.deg2rad(lo)),
       f.BIO5.to_numpy(float)/20,
       np.log1p(f.BIO12.to_numpy(float))/5])

def model_fit(X,y,w):
    xx=X*np.sqrt(w)[:,None];yy=y*np.sqrt(w)
    if np.linalg.matrix_rank(xx)<X.shape[1]:return None
    beta=np.linalg.lstsq(xx,yy,rcond=None)[0]
    return beta,float(np.sum(w*(y-X@beta)**2)),float(np.sum(w*y*y))

def macro_within_species(cell,min_photos_per_cell=1,boot=499):
    f=cell.loc[(cell.n_photos>=min_photos_per_cell)&cell.BIO5.notna()
               &cell.BIO12.notna()].copy()
    f=f.loc[f.groupby("inat_taxon_id").source_hex_id.transform("size")>=2].reset_index(drop=True)
    n_species=int(f.inat_taxon_id.nunique())
    if len(f)<120 or n_species<35:
        return {"status":"NOT_ENOUGH_WITHIN_SPECIES_HEX_EXPOSURE",
                "n_species":n_species,"n_species_hex":len(f)}
    bvar=f.groupby("inat_taxon_id").Bombus_fraction.transform("std").fillna(0)
    variable=int(f.loc[bvar>1e-9,"inat_taxon_id"].nunique())
    if variable<25:
        return {"status":"NOT_ENOUGH_WITHIN_SPECIES_BOMBUS_CONTRAST",
                "n_species":n_species,"n_species_with_Bombus_exposure_difference":variable}
    X=covariates(f)
    groups=f.inat_taxon_id
    W=(1/f.groupby("inat_taxon_id").source_hex_id.transform("size")).to_numpy(float)
    for i in range(X.shape[1]):
        X[:,i]-=pd.Series(X[:,i]).groupby(groups).transform("mean").to_numpy(float)
    labels=f.species.str.split().str[0].to_numpy(str)
    uniq,inv=np.unique(labels,return_inverse=True)
    outcomes={}
    controls=["Bombus_share_10pp","log_all_bee_species","lat_30deg",
              "abs_lat_30deg","sin_longitude","cos_longitude",
              "BIO5_20degC","log1p_BIO12_div5"]
    for j,colour in enumerate(COLORS):
        y=f["fraction_"+colour].to_numpy(float)
        y=y-pd.Series(y).groupby(groups).transform("mean").to_numpy(float)
        fit=model_fit(X,y,W);base=model_fit(X[:,1:],y,W)
        if fit is None or base is None:
            outcomes[colour]={"status":"COLLINEAR_SPATIAL_CLIMATE_MODEL_UNIDENTIFIED"}
            continue
        coef,rss,tss=fit;_,rss0,_=base
        a=np.zeros((len(uniq),len(coef),len(coef)))
        b=np.zeros((len(uniq),len(coef)))
        for i in range(len(uniq)):
            m=inv==i;z=X[m];v=W[m]
            a[i]=(z*v[:,None]).T@z;b[i]=(z*v[:,None]).T@y[m]
        rng=np.random.default_rng(20261117+j+100*min_photos_per_cell)
        samples=[]
        for _ in range(boot):
            ix=rng.integers(0,len(uniq),size=len(uniq))
            xx=a[ix].sum(0);yy=b[ix].sum(0)
            try:
                if np.linalg.cond(xx)>1e12:continue
                samples.append(float(np.linalg.solve(xx,yy)[0]))
            except np.linalg.LinAlgError:continue
        ci=np.quantile(samples,[.025,.975]).tolist() if len(samples)>=.9*boot else [None,None]
        outcomes[colour]={
           "status":"OBSERVATIONAL_PHOTO_COARSE_COLOUR_ONLY_NOT_GUIDE",
           "species_equal_fraction_change_per_10pp_Bombus_modelled_share":float(coef[0]),
           "genus_resampled95_fixed_original_source_photo_sample":ci,
           "accepted_bootstrap_draws":len(samples),"genera":len(uniq),
           "incremental_within_species_R2_Bombus_added_vs_geo_climate_bees":(
               float((rss0-rss)/tss) if tss>1e-12 else None),
           "adjusted_covariate_coefficients":{k:float(v) for k,v in zip(controls,coef)},
           "no_causal_or_phylogenetic_selection_claim":True}
    return {"status":"EXPLORATORY_ORIGINAL_FCP4475_X_AUTHOR_BEE_HEX_WITHIN_SPECIES",
            "n_species":n_species,"n_species_with_Bombus_exposure_difference":variable,
            "n_species_hex":len(f),"n_distinct_hex":int(f.source_hex_id.nunique()),
            "n_genera":len(uniq),"min_photos_per_species_hex":min_photos_per_cell,
            "species_equal_total_weight":True,"covariate_adjustments":controls,
            "outcomes":outcomes,
            "native_species_occurrence_pollinator_contact_and_study_temporality_NOT_identified":True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--fcp-photos",required=True,type=Path)
    ap.add_argument("--source-author-bee-hex",required=True,type=Path)
    ap.add_argument("--worldclim-bio",required=True,type=Path)
    ap.add_argument("--outdir",default=Path("stage66_global_macro_original_source"),type=Path)
    args=ap.parse_args()
    p,photo=source_photos(args.fcp_photos)
    b,bees=source_bee_model(args.source_author_bee_hex)
    p,clim=climate_at_photos(p,args.worldclim_bio)
    p,geom=original_polygon_match(p)
    cells,coverage=species_hex(p,b)
    result={"schema":"stage66_447500_actual_photo_4475species_x_original2695_beeHEX_macro",
       "source_original_FCP":photo,"source_original_bee":bees,
       "source_original_WorldClim":clim,"exact_original_polygon":geom,
       "species_HEX_coverage":coverage,
       "macro_min_1_original_classified_photo_per_cell":macro_within_species(cells,1),
       "macro_min_3_original_classified_photos_per_cell":macro_within_species(cells,3),
       "human_visible_coarse_photo_colour_not_UV_spatial_pattern_or_guide":True,
       "modelled_Bombus_range_overlaps_not_native_realized_pollination":True,
       "no_flower_scent_wind_fitness_or_causal_E_guild_colour_path":True}
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"source_based_global_FCP_Bombus_colour_macro_receipt.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False,sort_keys=True)+"\n")
    # Includes species and source HEX (broad biogeographical cells), no
    # protected precise photographed location, observer or source photo ID.
    cells.to_csv(args.outdir/"original_species_by_eligible_model_HEX_colour_fractions.csv",index=False)
    summary={"status":result["macro_min_1_original_classified_photo_per_cell"]["status"],
       "species_in_model":coverage["eligible_species"],
       "matched_authentic_photo_records":coverage["classified_photos_in_eligible_model"],
       "species_hex_units":coverage["species_x_hex_units"],
       "source_model_hex_with_photos":coverage["eligible_hex_with_photos"],
       "within_species_comparable":result["macro_min_1_original_classified_photo_per_cell"].get("n_species"),
       "minimum_3_photos_sensitivity_species":result["macro_min_3_original_classified_photos_per_cell"].get("n_species")}
    print("STAGE66_REAL_ORIGINAL_GLOBAL_FCP_BEE_MACRO",json.dumps(summary,sort_keys=True))
    print("NO_UV_NECTAR_GUIDE_OR_HISTORICAL_POLLINATOR_SELECTION")
if __name__=="__main__":main()
