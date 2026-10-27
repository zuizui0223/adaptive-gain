"""Stage 3f: exact administrative PoMS pan-flower/FIT context join.

Pan floral checks at five stations in a 1km square are NOT simultaneous
alternative flowers perceived by insects in FIT 10-minute focal-flower counts.
This file audits join coverage, no causal behavior/competition/routeability.
"""
from __future__ import annotations
import argparse, hashlib, io, json, zipfile
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
from source_inventory import PAN_URL, FIT_URL, download, zip_guard

PAN_PARTS = {
    "samples":("data/ukpoms_1kmpantrapdata_2017-2023_samples.csv",
               "70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277"),
    "flowers":("data/ukpoms_1kmpantrapdata_2017-2023_flowers.csv",
               "53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba"),
}
FIT_MEMBER="data/ukpoms_1kmfitcountdata_2017-2023.csv"
FIT_HASH="29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52"
KEYS=["location_code","x1km_square","date"]
MISSING={"", "nan", "NA", "N/A", "null", "None", "<NA>"}

def safe_source_csv(z:zipfile.ZipFile,name,expected_hash:str):
    raw=z.read(name)
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=expected_hash:
        raise ValueError("source member SHA256 mismatch "+name)
    for enc in ["utf-8","cp1252","latin-1"]:
        try:
            text=raw.decode(enc,errors="strict")
            frame=pd.read_csv(io.StringIO(text),low_memory=False,
                              dtype={"sample_id":"string","location_code":"string",
                                     "x1km_square":"string","pan_trap_station":"string",
                                     "source_taxon_version_key":"string"})
            return frame,enc,digest
        except UnicodeDecodeError:continue
    raise ValueError("original CSV not decodable")

def parse_original_dates(series):
    """Do not accidentally reinterpret ISO yyyy-mm-dd as mm/dd under dayfirst."""
    raw=series.astype("string").str.strip()
    iso=raw.str.match(r"^\d{4}-\d{2}-\d{2}(?:[ T].*)?$",na=False)
    out=pd.Series(pd.NaT,index=series.index,dtype="datetime64[ns]")
    if iso.any():
        out.loc[iso]=pd.to_datetime(raw.loc[iso],errors="coerce",format="ISO8601")
    if (~iso).any():
        out.loc[~iso]=pd.to_datetime(raw.loc[~iso],errors="coerce",format="mixed",dayfirst=True)
    return out.dt.normalize()

def clean_keys(df,site_columns=KEYS):
    x=df.copy()
    for key in ["location_code","x1km_square"]:
        if key not in x:raise ValueError("missing native 1km key "+key)
        x[key]=x[key].astype("string").str.strip()
        x.loc[x[key].isin(MISSING),key]=pd.NA
    if "date" not in x:raise ValueError("source date is missing")
    x["date"]=parse_original_dates(x["date"])
    x["year_from_date"]=x["date"].dt.year
    if "sample_id" not in x:raise ValueError("missing native sample identifier")
    x["sample_id"]=x["sample_id"].astype("string").str.strip()
    if x["sample_id"].isna().any() or x["sample_id"].isin(MISSING).any():
        raise ValueError("source sample IDs missing")
    return x

def taxon_id(row):
    """Exact version key when possible; declared weaker source-name fallback."""
    key=str(row.get("source_taxon_version_key","")).strip()
    if key not in MISSING and key.lower() not in {"na","none","not recorded","unknown"}:
        return "key:"+key,"version_key"
    source=str(row.get("taxon_source","")).strip()
    if source not in MISSING and source.lower() not in {"na","none","not recorded","unknown","no flowers"}:
        return "source:"+source.casefold(),"taxon_source_fallback"
    return None,"missing_taxon_label"

def build_pan_environment(samples,flowers):
    required={"sample_id","pan_trap_station","date","location_code","x1km_square"}
    if not required <= set(samples):raise ValueError("Pan station source lacks join fields")
    if not {"sample_id","source_taxon_version_key","taxon_source"}<=set(flowers):
        raise ValueError("flower occurrence source lacks native keys/names")
    s=clean_keys(samples)
    f=flowers.copy()
    f["sample_id"]=f["sample_id"].astype("string").str.strip()
    s_dups=int(s.sample_id.duplicated().sum())
    if s_dups:raise ValueError("Pan sample_id is not unique: "+str(s_dups))
    keys_notnull=s[KEYS].notna().all(axis=1)
    invalid=s.loc[~keys_notnull]
    if len(invalid):
        raise ValueError(f"Pan sample locations/dates missing: {len(invalid)}")
    unmatched=f.loc[~f.sample_id.isin(s.sample_id)]
    if len(unmatched):raise ValueError(f"orphan flowering occurrences: {len(unmatched)}")
    labelled=[taxon_id(r) for _,r in f.iterrows()]
    f["taxon_identity"]=[v[0] for v in labelled]
    f["identity_rule"]=[v[1] for v in labelled]
    floral=pd.to_numeric(f["total_floral_units"],errors="coerce")
    invalid_floral=int((floral.notna() & ((floral<0)|(~np.isfinite(floral)))).sum())
    if invalid_floral:raise ValueError("invalid negative/nonfinite source floral-unit values")
    if f["occurrence_id"].notna().any() and f["occurrence_id"].dropna().duplicated().any():
        raise ValueError("duplicate Pan flower occurrence_id")
    label_summary={
        "floral_occurrence_rows":len(f),
        "with_version_key":int(f.identity_rule.eq("version_key").sum()),
        "with_fallback_name":int(f.identity_rule.eq("taxon_source_fallback").sum()),
        "without_plant_name":int(f.identity_rule.eq("missing_taxon_label").sum()),
        "missing_source_floral_units":int(floral.isna().sum()),
        "zero_source_floral_units":int(floral.eq(0).sum()),
        "plant_identity_count":int(f.taxon_identity.nunique(dropna=True)),
        "floral_units_heterogeneous_not_aggregated":True
    }
    # Each original pan station is represented once; a station may have
    # zero flower occurrences recorded, which is NOT assumed a surveyed zero.
    perstation=f.groupby("sample_id",observed=True,dropna=False).agg(
        recorded_flower_occurrences=("taxon_identity","size"),
        labelled_flower_occurrences=("taxon_identity","count"),
        recorded_plant_types=("taxon_identity","nunique")).reset_index()
    station=s.merge(perstation,on="sample_id",how="left",validate="one_to_one")
    station["recorded_flower_occurrences"]=station["recorded_flower_occurrences"].fillna(0).astype(int)
    station["labelled_flower_occurrences"]=station["labelled_flower_occurrences"].fillna(0).astype(int)
    station["recorded_plant_types"]=station["recorded_plant_types"].fillna(0).astype(int)
    pan_station_summary={
        "unique_pan_station_sample_ids":len(station),
        "distinct_pan_station_ids":int(station.pan_trap_station.nunique(dropna=True)),
        "station_rows_with_no_flower_occurrence":int((station.recorded_flower_occurrences==0).sum()),
        "date_min":str(station.date.min().date()),
        "date_max":str(station.date.max().date()),
        "unique_location_codes":int(station.location_code.nunique()),
        "unique_1km_squares":int(station.x1km_square.nunique()),
        "location_code_to_multiple_grid_codes":int(
            (station.groupby("location_code").x1km_square.nunique()>1).sum()),
        "site_years":int(station[["location_code","year_from_date"]].drop_duplicates().shape[0])
    }
    pan_per_day=station.groupby(KEYS,observed=True,dropna=False).agg(
        stations=("sample_id","size"),
        station_types=("pan_trap_station","nunique"),
        stations_with_flower_occurrences=("recorded_flower_occurrences",lambda x:int((x>0).sum())),
        raw_flower_occurrence_rows=("recorded_flower_occurrences","sum")).reset_index()
    # Occurrence rows link ONLY to their own Pan station sample_id first.
    linked=f[f.taxon_identity.notna()][["sample_id","taxon_identity"]].merge(
        station[["sample_id",*KEYS]],on="sample_id",how="left",validate="many_to_one")
    richness=linked.groupby(KEYS,observed=True,dropna=False).agg(
        pan_recorded_flowering_taxa=("taxon_identity","nunique")).reset_index()
    pan_per_day=pan_per_day.merge(richness,on=KEYS,how="left",validate="one_to_one")
    pan_per_day["pan_recorded_flowering_taxa"]=pan_per_day["pan_recorded_flowering_taxa"].astype("Int64")
    if pan_per_day.duplicated(KEYS).any():raise ValueError("source Pan day not unique after aggregation")
    pan_report={
        **pan_station_summary,
        **label_summary,
        "pan_station_days":len(pan_per_day),
        "pan_site_days_with_5_stations":int(pan_per_day.stations.eq(5).sum()),
        "pan_site_days_with_gt5_stations":int(pan_per_day.stations.gt(5).sum()),
        "pan_site_days_without_named_flower_taxa":int(pan_per_day.pan_recorded_flowering_taxa.isna().sum()),
        "median_taxa_where_documented":float(pan_per_day.pan_recorded_flowering_taxa.dropna().median()) if pan_per_day.pan_recorded_flowering_taxa.notna().any() else None,
        "survey_grain":"Pan trap station × date; station may have multiple flowering plant presence rows; five stations per square-visit generally expected"
    }
    return pan_per_day,pan_report,station

def nearest_site_date(fit:pd.DataFrame,pan:pd.DataFrame,window_days=7):
    """One closest pan context for each FIT row in exact same (site,grid,year).
    Earlier Pan date wins ties; do not interpolate missing flowering.
    """
    if fit.sample_id.duplicated().any():raise ValueError("duplicate FIT sample IDs")
    groups={}
    for (site,grid,year),g in pan.groupby(
        ["location_code","x1km_square","year_from_date"],observed=True,dropna=False):
        groups[(site,grid,int(year))]=g.sort_values("date")
    out=[]
    for _,row in fit.iterrows():
        key=(row.location_code,row.x1km_square,int(row.year_from_date))
        g=groups.get(key)
        if g is None or len(g)==0:
            out.append((None,None,None));continue
        dates=g.date.to_numpy(dtype="datetime64[ns]")
        delta=((dates-np.datetime64(row.date))/np.timedelta64(1,"D")).astype(int)
        candidates=np.flatnonzero(np.abs(delta)<=window_days)
        if len(candidates)==0:out.append((None,None,None));continue
        chosen=min(candidates,key=lambda i:(abs(delta[i]),int(delta[i]>0),int(i)))
        a=g.iloc[chosen]
        out.append((str(a.date.date()),int(delta[chosen]),
                    None if pd.isna(a.pan_recorded_flowering_taxa) else int(a.pan_recorded_flowering_taxa)))
    return pd.DataFrame(out,columns=["near_pan_date","near_day_difference","near_pan_flower_richness"],
                        index=fit.index)

def match_pan_fit(fit_original,pan_daily,pan_station_report):
    fit=clean_keys(fit_original)
    if fit.sample_id.duplicated().any():raise ValueError("FIT sample_id duplicates")
    if fit[KEYS].isna().any().any():
        raise ValueError("FIT site/grid/date missing: cannot silently drop")
    if pan_daily.duplicated(KEYS).any():raise ValueError("pan site date duplicate")
    fit["pair_positive"]=(pd.to_numeric(fit.bumblebees,errors="raise")+
                          pd.to_numeric(fit.other_flies,errors="raise"))>0
    # Reconcile source dates & years to avoid assuming formatted year is correct.
    fyear=pd.to_numeric(fit.year,errors="coerce")
    if int((fyear!=fit.year_from_date).sum()):
        raise ValueError("FIT year/date inconsistent")
    pan=pan_daily.copy()
    pan["year_from_date"]=pan.date.dt.year
    if pan["pan_recorded_flowering_taxa"].dtype!="Int64":
        pan["pan_recorded_flowering_taxa"]=pan.pan_recorded_flowering_taxa.astype("Int64")
    matched=fit.merge(pan,on=KEYS,how="left",validate="many_to_one",indicator=True,
                      suffixes=("","_pan"))
    if len(matched)!=len(fit) or matched.sample_id.nunique()!=fit.sample_id.nunique():
        raise ValueError("FIT census row inflation on Pan join")
    exact=matched["_merge"].eq("both")
    exact_and_flower=exact&matched["pan_recorded_flowering_taxa"].notna()
    near=nearest_site_date(fit,pan)
    if len(near)!=len(fit):raise ValueError("nearest sensitivity changed census grain")
    nearby=near.near_day_difference.notna()
    gridonly=fit[["sample_id","x1km_square","date"]].merge(
        pan[["x1km_square","date"]].drop_duplicates(),
        on=["x1km_square","date"],how="left",indicator=True,validate="many_to_one")
    grid_match=gridonly["_merge"].eq("both")
    evidence={
        "original_fit_surveys":len(fit),
        "original_fit_pair_positive":int(fit.pair_positive.sum()),
        "original_fit_site_codes":int(fit.location_code.nunique()),
        "original_fit_grid_squares":int(fit.x1km_square.nunique()),
        "exact_site_grid_date_fit_surveys":int(exact.sum()),
        "exact_site_grid_date_pair_positive_fit":int((exact&matched.pair_positive).sum()),
        "exact_with_recorded_flower_taxa_fit":int(exact_and_flower.sum()),
        "exact_with_recorded_flower_taxa_pair_positive_fit":int((exact_and_flower&matched.pair_positive).sum()),
        "exact_unique_sites":int(matched.loc[exact,"location_code"].nunique()),
        "exact_unique_site_dates":int(matched.loc[exact,KEYS].drop_duplicates().shape[0]),
        "exact_5_station_fit":int((exact&matched.stations.eq(5)).sum()),
        "exact_5_station_and_flowers_fit":int((exact_and_flower&matched.stations.eq(5)).sum()),
        "grid_date_only_matches":int(grid_match.sum()),
        "grid_date_only_unmatched_by_full_three_keys":int(grid_match.sum()-int((exact&grid_match.to_numpy()).sum())),
        "same_site_grid_within_7_days_fit":int(nearby.sum()),
        "near_date_abs_delta_day_counts":{str(k):int(v) for k,v in
             near.near_day_difference.dropna().abs().value_counts().sort_index().items()},
        "joined_record_type":"1 row per FIT sample_id; Pan station and floral occurrences aggregated at exact site-date",
        "explicit_not_available_choice_set":True,
        "pan_station_summary":pan_station_report
    }
    byyear=[]
    for year,g in matched.groupby("year_from_date",dropna=False):
        byyear.append({"year":str(year),
                       "fit_surveys":len(g),
                       "pair_positive_surveys":int(g.pair_positive.sum()),
                       "exact_matched_fit_surveys":int(g["_merge"].eq("both").sum()),
                       "matched_with_flower_labels":int(
                           (g["_merge"].eq("both")&g.pan_recorded_flowering_taxa.notna()).sum())})
    evidence["year_coverage"]=byyear
    if (evidence["exact_unique_sites"]>=10 and
        evidence["exact_with_recorded_flower_taxa_pair_positive_fit"]>=100):
        evidence["next_model_gate"]="PASS_CONTEXTUAL_JOIN_COVERAGE_NOT_CAUSAL"
    else:evidence["next_model_gate"]="NO_GO_INSUFFICIENT_EXACT_MATCHED_FLOWER_CONTEXT"
    return evidence

def run(folder:Path):
    pan_zip=folder/"pan_original_provider.zip"
    fit_zip=folder/"fit_original_provider.zip"
    source_receipts={}
    for name,url,path in [("pan",PAN_URL,pan_zip),("fit",FIT_URL,fit_zip)]:
        source_receipts[name]=download(url,path)
    with zipfile.ZipFile(pan_zip) as z:
        zip_guard(z)
        pan_samples,code_s,sha_s=safe_source_csv(z,*PAN_PARTS["samples"])
        pan_flowers,code_f,sha_f=safe_source_csv(z,*PAN_PARTS["flowers"])
    with zipfile.ZipFile(fit_zip) as z:
        zip_guard(z)
        fit,code_fit,sha_fit=safe_source_csv(z,FIT_MEMBER,FIT_HASH)
    pan_daily,pan_report,stations=build_pan_environment(pan_samples,pan_flowers)
    join=match_pan_fit(fit,pan_daily,pan_report)
    report={"status":"original_data_cross_source_join_audit",
            "sources":{"pan_doi":"10.5285/5841bfae-471b-498c-af89-c30e5140d6c5",
                       "fit_doi":"10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618",
                       "pan_station_csv_sha256":sha_s,
                       "pan_flower_csv_sha256":sha_f,
                       "fit_1km_csv_sha256":sha_fit,
                       "source_encodings":{"pan_stations":code_s,"pan_flowers":code_f,"fit":code_fit}},
            "original_pan_source_rows":{"stations":len(pan_samples),"flowers":len(pan_flowers)},
            "linkage":join,
            "scientific_boundary":"Same-day same 1km square Pan trap flowering is only nearby ecological context, not the FIT individual's contemporaneous flower-choice set."}
    folder.mkdir(exist_ok=True,parents=True)
    (folder/"site_date_flower_linkage_audit.json").write_text(
         json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))
    print("POMS_PAN_JOIN_RESULT "+json.dumps(report,ensure_ascii=False,allow_nan=False),flush=True)
    print("POMS_PAN_JOIN_AUDIT_COMPLETE",flush=True)
    return report

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="poms_pan_joint_output")
    args=p.parse_args(argv)
    run(Path(args.out))

if __name__=="__main__":main()
