"""Author-original Harris2026 wind/community/flight-vs-walk *source QA only*.

All data are archived, SHA-pinned source tables. Records are collapsed to
original survey before joining to insect counts and averaged weather.
No model is fitted and no association is inspected here.
"""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

HASHES = {
    "forage.csv":"c5bb7b67780b8749014cb645fa43fc35bc1ffe8a4b1c8edcb5637d07a5146f61",
    "weather.csv":"c7b09eaef978b4bc8bbd6bf093c2872130c8a6038ec206a4f36fa365896a9641",
    "insect_surveys.csv":"f0f899655d671f311f47100745790ae8618b57777a9cd8e5a35f0d0854619ee3",
}
INSECT_METADATA={"survey","date","time","site","plant","honeybees"}
MOVEMENT=("number of flights","number of walks","flowers probed")
OTHER_REQUIRED=("approx flower density (flowers / m2)",)

def _norm(value):
    return " ".join(str(value).strip().lower().split())

def prepare(table):
    df=table.copy()
    df.columns=[c.strip() for c in df.columns]
    if len(df.columns)!=len(set(df.columns)):
        raise ValueError("NO_GO_NORMALIZED_DUPLICATE_COLUMNS")
    for c in ("survey","date"):
        if c not in df: raise ValueError("NO_GO_SOURCE_LACKS_"+c)
    df["survey"]=df["survey"].astype(str).str.strip()
    if df["survey"].eq("").any(): raise ValueError("NO_GO_MISSING_SURVEY_ID")
    df["date"]=pd.to_datetime(df["date"].astype(str).str.strip(),
                                format="%d/%m/%Y",errors="raise")
    return df

def count_categories(insect):
    df=prepare(insect)
    taxa=[c for c in df.columns if c not in INSECT_METADATA]
    if not taxa or "honeybees" not in df.columns:
        raise ValueError("NO_GO_MISSING_ORIGINAL_INSECT_CATEGORIES")
    return taxa

def checked_numeric(source,fields,kind="COUNT"):
    cols=source[list(fields)].apply(pd.to_numeric,errors="raise")
    vals=cols.to_numpy(dtype=float)
    if not np.isfinite(vals).all():
        raise ValueError("NO_GO_MISSING_NONFINITE_"+kind)
    if kind=="COUNT":
        if np.any(vals<0) or np.any(vals!=np.floor(vals)):
            bad=np.argwhere((vals<0)|(vals!=np.floor(vals)))
            examples=[{"survey":str(source.iloc[int(i)]["survey"]),
                       "field":str(cols.columns[int(j)]),
                       "native_value":str(source.iloc[int(i)][cols.columns[int(j)]])}
                      for i,j in bad[:12]]
            raise ValueError("INVALID_SOURCE_BEHAVIOR_COUNT "+json.dumps(examples))
    return cols

def _one_value(df,column):
    v=df[column].map(_norm).unique()
    return len(v)==1

def assemble(forage,weather,insects):
    f,w,i=map(prepare,(forage,weather,insects))
    cats=count_categories(insects)
    excluded=[];raw_issues=[];rows=[]
    q={
       "source":"Harris2026 Dryad v456836",
       "status":"ORIGINAL_SOURCE_GRAIN_AUDIT_NOT_AN_EFFECT",
       "original_foraging_rows":len(f),
       "original_foraging_surveys":int(f.survey.nunique()),
       "original_weather_rows":len(w),
       "original_weather_surveys":int(w.survey.nunique()),
       "original_insect_rows":len(i),
       "original_insect_surveys":int(i.survey.nunique()),
       "original_nonhoneybee_taxon_categories":cats,
       "no_biological_effect_fitted":True,
       "excluded":excluded,
       "metadata_alerts":raw_issues,
       "nesting":"original behavior observations within survey, weather and insect counts joined only at survey-level",
    }
    if f.duplicated().any():
        q["exact_duplicate_original_foraging_rows"]=int(f.duplicated().sum())
        # Repeated biological behavior events may be identical; do not deduplicate.
    for survey,g in f.groupby("survey",sort=True):
        def drop(reason):
            excluded.append({"survey":survey,"foraging_rows":len(g),"reason":reason})
        if any(not _one_value(g,c) for c in ("date","site","location","plant")):
            drop("source_foraging_metadata_conflict")
            continue
        wg=w[w.survey==survey]
        ig=i[i.survey==survey]
        if wg.empty:
            drop("no_original_weather_survey")
            continue
        if len(ig)!=1:
            drop("nonunique_or_absent_insect_survey")
            continue
        city=str(g.site.iloc[0]).strip()
        location=str(g.location.iloc[0]).strip()
        plant=str(g.plant.iloc[0]).strip()
        day=g.date.iloc[0]
        bad_w=any(not _one_value(wg,c) for c in ("date","site","location"))
        bad_w=bad_w or any(
            not (_norm(wg[c].iloc[0])==_norm(value))
            for c,value in (("date",day),("site",city),("location",location)))
        if bad_w:
            drop("weather_source_metadata_mismatch")
            continue
        x=ig.iloc[0]
        if any(_norm(x[c])!=_norm(v) for c,v in
               (("date",day),("site",location),("plant",plant))):
            drop("insect_source_metadata_mismatch")
            raw_issues.append({"survey":survey,"forage_plant":plant,
                               "insect_plant":str(x["plant"]),
                               "forage_location":location,"insect_site":str(x["site"])})
            continue
        behavior=checked_numeric(g,MOVEMENT)
        extra=checked_numeric(g,OTHER_REQUIRED,kind="FEATURE")
        meteo=checked_numeric(wg,("temperature","blue_sky","beaufort"),kind="FEATURE")
        community=checked_numeric(ig,["honeybees"]+cats)
        if not (meteo["beaufort"].between(0,12).all() and
                meteo["blue_sky"].between(0,100).all() and
                extra.iloc[:,0].ge(0).all()):
            raise ValueError("NO_GO_SOURCE_METEOROLOGY_OR_DENSITY_RANGE")
        flights=int(behavior["number of flights"].sum())
        walks=int(behavior["number of walks"].sum())
        probes=int(behavior["flowers probed"].sum())
        total=flights+walks
        if total<=0:
            drop("no_recorded_flight_or_walk")
            continue
        impossible=int((behavior["number of flights"]+
                        behavior["number of walks"]>
                        behavior["flowers probed"]).sum())
        if impossible:
            raw_issues.append({"survey":survey,
                "source_rows_with_more_moves_than_probes":impossible,
                "mode_count_semantics_must_be_reviewed":True})
        apis=int(community["honeybees"].iloc[0])
        other=int(community[cats].iloc[0].sum())
        denom=apis+other
        if denom<=0:
            drop("empty_original_insect_census")
            continue
        rows.append({
            "survey":survey,"date":day.strftime("%Y-%m-%d"),"site":city,
            "location":location,"plant":plant,
            "behavior_rows":len(g),"weather_records":len(wg),
            "flights":flights,"walks":walks,"movement_events":total,
            "flowers_probed":probes,"moves_greater_than_probes_rows":impossible,
            "beaufort":float(meteo["beaufort"].mean()),
            "temperature":float(meteo["temperature"].mean()),
            "blue_sky":float(meteo["blue_sky"].mean()),
            "flower_density":float(extra.iloc[:,0].mean()),
            "honeybee_count":apis,"other_insect_count":other,
            "total_insects":denom,"other_share":float(other/denom),
            "other_nonzero_categories":int((community[cats].iloc[0]>0).sum()),
        })
    d=pd.DataFrame(rows)
    if not d.empty:
        if d.survey.duplicated().any():raise ValueError("NO_GO_SURVEY_JOIN_MULTIPLICATION")
        q.update({
           "survey_records_usable_for_mode":len(d),
           "raw_behavior_rows_in_usable_surveys":int(d.behavior_rows.sum()),
           "total_recorded_flights":int(d.flights.sum()),
           "total_recorded_walks":int(d.walks.sum()),
           "total_recorded_movement_events":int(d.movement_events.sum()),
           "surveys_more_moves_than_probes":int((d.moves_greater_than_probes_rows>0).sum()),
           "cities":sorted(d.site.unique().tolist()),
           "city_date_clusters":int((d.site+"|"+d.date).nunique()),
           "plants":int(d.plant.nunique()),
           "beaufort_counts_by_source_survey":{str(k):int(v) for k,v in
                  sorted(d.beaufort.value_counts().items())},
           "other_share_range":[float(d.other_share.min()),float(d.other_share.max())],
           "zero_other_insect_surveys":int((d.other_insect_count==0).sum()),
           "zero_walk_surveys":int((d.walks==0).sum()),
           "zero_flight_surveys":int((d.flights==0).sum()),
           "by_plant_support":[{
               "plant":name,"surveys":len(g),
               "wind_levels":int(g.beaufort.nunique()),
               "other_share_levels":int(g.other_share.nunique()),
               "movement_events":int(g.movement_events.sum()),
               "zero_walk_surveys":int((g.walks==0).sum()),
           } for name,g in d.groupby("plant",sort=True)]
        })
        q["source_support_gate"]="PASS_GRAIN_ONLY" if (
             len(d)>=80 and q["city_date_clusters"]>=30 and
             len(q["cities"])==2 and q["total_recorded_walks"]>0 and
             q["total_recorded_flights"]>0) else "NO_GO_SOURCE_MOVEMENT_SUPPORT"
    else:q["source_support_gate"]="NO_GO_NO_SOURCE_SURVEYS"
    return d,q

def run(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    raw={}
    for fname,sha in HASHES.items():
        data=(root/fname).read_bytes()
        if hashlib.sha256(data).hexdigest()!=sha:
            raise ValueError("NO_GO_ORIGINAL_SOURCE_SHA256_CHANGED "+fname)
        raw[fname]=pd.read_csv(root/fname)
    source=raw["forage.csv"].copy();source.columns=[c.strip() for c in source.columns]
    issue_rows=[]
    for fld in MOVEMENT:
        v=pd.to_numeric(source[fld],errors="coerce")
        invalid=v.isna() | ~np.isfinite(v.to_numpy(dtype=float)) | (v<0) | (v!=np.floor(v))
        for idx in np.flatnonzero(invalid.to_numpy()):
            issue_rows.append({"survey":str(source.iloc[idx]["survey"]),
                               "column":fld,"original":str(source.iloc[idx][fld]),
                               "source_row_index":int(idx)})
    m=(pd.to_numeric(source["number of flights"],errors="coerce")+
       pd.to_numeric(source["number of walks"],errors="coerce"))
    p=pd.to_numeric(source["flowers probed"],errors="coerce")
    diag={"noninteger_negative_missing_original_counts":issue_rows,
          "native_episodes_more_transfers_than_probes":int((m>p).sum()),
          "original_total_behavior_rows":len(source),
          "only_source_contract_QA_no_biological_effect":True}
    (root/"original_count_diagnostics.json").write_text(json.dumps(diag,indent=2))
    print("STAGE12_RAW_COUNT_DIAGNOSTICS "+json.dumps(diag),flush=True)
    d,q=assemble(raw["forage.csv"],raw["weather.csv"],raw["insect_surveys.csv"])
    # Derived selected survey counts only: raw original insect rows not committed.
    (root/"source_grain_qa.json").write_text(json.dumps(q,indent=2,ensure_ascii=False))
    print("STAGE12_SOURCE_GRAIN_AUDIT "+json.dumps(q,ensure_ascii=False),flush=True)
    print("STAGE12_SOURCE_GRAIN_AUDIT_COMPLETE",flush=True)
    return d,q

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--out",default="stage12_original")
    run(p.parse_args().out)
