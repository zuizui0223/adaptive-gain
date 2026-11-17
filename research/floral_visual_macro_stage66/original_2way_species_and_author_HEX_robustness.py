"""Stage66 real original-source 2-way cluster robustness, exploratory after model fit.

Input is the signed genuine original species×HEX 92,010-row artifact from
Stage66 Actions 44025370724. No artificial photos and no cross-study estimates.
Two-way source plant species and source author HEX cluster-robust sandwich
variance with species×HEX intersection correction. Not a phylogenetic model.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np,pandas as pd
SOURCE_RUN=44025370724
SOURCE_CSV_SHA="90cb8620b4c007e3a04b06121c0b75550fb3c176f17794b21b8295031d669da4"
SOURCE_JSON_SHA="18e755be03e776f7f2da12cb6c904815669a3d1b603bfe632bab58211de6bf65"
COLORS=("white","yellow_orange","red_pink","blue_purple")

def check(ok,why):
    if not ok:raise ValueError("STAGE66_TWO_WAY_SOURCE_NO_GO_"+why)

def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(2**20),b""):h.update(block)
    return h.hexdigest()

def authenticated_source(csv_path,receipt_path):
    check(digest(csv_path)==SOURCE_CSV_SHA,"SOURCE_92010_SPECIES_HEX_SHA")
    check(digest(receipt_path)==SOURCE_JSON_SHA,"SOURCE_STAGE66_RECEIPT_SHA")
    d=json.loads(Path(receipt_path).read_text())
    t=pd.read_csv(csv_path)
    check(d["schema"]=="stage66_447500_actual_photo_4475species_x_original2695_beeHEX_macro",
          "SOURCE_SCHEMA")
    check(len(t)==d["species_HEX_coverage"]["species_x_hex_units"]==92010,
          "SOURCE_SPECIES_HEX_DENOMINATOR")
    check(t.inat_taxon_id.nunique()==4475 and t.source_hex_id.nunique()==1618,
          "SOURCE_SPECIES_OR_AUTHORIZED_HEX_CHANGED")
    check(t[["inat_taxon_id","source_hex_id"]].drop_duplicates().shape[0]==len(t),
          "DUPLICATE_SPECIES_HEX")
    return t,d

def two_way_species_hex(cell,min_photos):
    t=cell.loc[(cell.n_photos>=min_photos)&cell.BIO5.notna()&cell.BIO12.notna()].copy()
    t=t.loc[t.groupby("inat_taxon_id").source_hex_id.transform("size")>=2].reset_index(drop=True)
    if len(t)<300 or t.inat_taxon_id.nunique()<50:
        return {"status":"NO_COMPARABLE_SAME_SPECIES_HEX","n_species_hex":len(t)}
    groups=t.inat_taxon_id
    w=1/t.groupby("inat_taxon_id").source_hex_id.transform("size").to_numpy(float)
    la=t.lat.to_numpy(float);lo=t.lon.to_numpy(float)
    X=np.column_stack([t.Bombus_fraction.to_numpy(float)/.1,
        t.log_bees.to_numpy(float),la/30,np.abs(la)/30,
        np.sin(np.deg2rad(lo)),np.cos(np.deg2rad(lo)),
        t.BIO5.to_numpy(float)/20,np.log1p(t.BIO12.to_numpy(float))/5])
    for j in range(X.shape[1]):
        X[:,j]-=pd.Series(X[:,j]).groupby(groups).transform("mean").to_numpy(float)
    check(np.linalg.matrix_rank(X*np.sqrt(w)[:,None])==8,"DESIGN_NOT_FULL_RANK")
    bread=np.linalg.inv(X.T@(w[:,None]*X))
    bvar=t.groupby("inat_taxon_id").Bombus_fraction.transform("std").fillna(0).gt(1e-9)
    result={"status":"POSTHOC_CLUSTER_ROBUST_SOURCE_SPECIES_AND_AUTHOR_HEX",
            "species":int(t.inat_taxon_id.nunique()),
            "source_author_hex":int(t.source_hex_id.nunique()),"species_hex":len(t),
            "n_species_with_Bombus_model_exposure_difference":int(t.loc[bvar,"inat_taxon_id"].nunique()),
            "min_photo_per_species_hex":min_photos,"effects":{},
            "source_species_hex_intersection_cluster_corrected":True,
            "not_an_independent_provider_phylogeny_or_spatial_block_prediction":True}
    for colour in COLORS:
        y=t["fraction_"+colour].to_numpy(float)
        y-=pd.Series(y).groupby(groups).transform("mean").to_numpy(float)
        beta=bread@(X.T@(w*y))
        scores=(w*(y-X@beta))[:,None]*X
        s=pd.DataFrame(scores,columns=[f"x{j}" for j in range(8)])
        s["species"]=groups.to_numpy();s["source_hex_id"]=t.source_hex_id.to_numpy()
        cols=[f"x{j}" for j in range(8)]
        by_species=s.groupby("species",sort=False)[cols].sum().to_numpy()
        by_hex=s.groupby("source_hex_id",sort=False)[cols].sum().to_numpy()
        meat=by_species.T@by_species+by_hex.T@by_hex-scores.T@scores
        covariance=bread@meat@bread
        variance=float(covariance[0,0]);se=float(np.sqrt(variance)) if variance>0 else None
        result["effects"][colour]={
            "beta_fraction_per_10pp_modeled_Bombus_share":float(beta[0]),
            "two_way_cluster_se":se,
            "two_way_cluster_normal95_posthoc":(
                [float(beta[0]-1.96*se),float(beta[0]+1.96*se)]
                if se is not None else [None,None]),
            "extra_phylogeny_and_native_range_control_not_performed":True}
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage66-authentic-species-hex",type=Path,required=True)
    p.add_argument("--stage66-authentic-receipt",type=Path,required=True)
    p.add_argument("--outdir",type=Path,default=Path("stage66_global_macro_two_way_robustness"))
    a=p.parse_args()
    data,receipt=authenticated_source(a.stage66_authentic_species_hex,
                                      a.stage66_authentic_receipt)
    output={"source_actions_run":SOURCE_RUN,"source_stage66_species_x_hex_SHA256":SOURCE_CSV_SHA,
            "source_stage66_receipt_SHA256":SOURCE_JSON_SHA,
            "n_photo_source_species":4475,"n_photo_source_author_hex":1618,
            "min_1":two_way_species_hex(data,1),
            "min_3":two_way_species_hex(data,3),
            "posthoc_not_predeclared_and_no_floral_UV_scent_or_wind_trait":True}
    # Assert that the new 2-way cluster audit EXACTLY regenerates the earlier
    # genuine photographic OLS effects; do not accidentally change the data.
    for n,k in ((1,"min_1_original_classified_photo_per_cell"),
                (3,"min_3_original_classified_photos_per_cell")):
        frozen=receipt["macro_"+k]
        for colour,z in output[f"min_{n}"]["effects"].items():
            expected=frozen["outcomes"][colour][
                "species_equal_fraction_change_per_10pp_Bombus_modelled_share"]
            check(abs(z["beta_fraction_per_10pp_modeled_Bombus_share"]-expected)<1e-10,
                  "CANNOT_REPRODUCE_ORIGINAL_STAGE66_POINT_"+colour)
    a.outdir.mkdir(parents=True,exist_ok=True)
    (a.outdir/"original_species_and_hex_two_way_cluster_real_macro.json").write_text(
        json.dumps(output,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("STAGE66_GENUINE_ORIGINAL_SPATIAL_AND_PLANT_CLUSTER_AUDIT",
          json.dumps({k:{"species":output[k]["species"],"hex":output[k]["source_author_hex"],
                          "effects":{c:{"beta":round(v["beta_fraction_per_10pp_modeled_Bombus_share"],6),
                                        "CI":v["two_way_cluster_normal95_posthoc"]}
                                     for c,v in output[k]["effects"].items()}}
                           for k in ("min_1","min_3")},sort_keys=True))
    print("STAGE66_STRONG_CLAIM_NO_GO_NON_NATIVE_AND_NO_UV_GUIDE")
if __name__=="__main__":main()
