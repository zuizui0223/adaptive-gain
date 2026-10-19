"""Original FIT zero-count and crossed-exposure feasibility audit (no modeling).

Works from the official EIDC original ZIP and emits only aggregate diagnostics.
DO NOT interpret a zero in an unobserved target plant as a measured zero.
"""
from __future__ import annotations
import argparse, collections, hashlib, io, json, re, urllib.request, zipfile
from pathlib import Path
import numpy as np
import pandas as pd

URL="https://data-package.ceh.ac.uk/data/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip"
MEMBERS={
  "public":"data/ukpoms_publicfitcountdata_2017-2023.csv",
  "1km":"data/ukpoms_1kmfitcountdata_2017-2023.csv"
}
GUILDS=("bumblebees","honeybees","solitary_bees","wasps","hoverflies",
"other_flies","butterflies_moths","beetles","insects_small","insects_other")

def archive():
    req=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-poms-effort-audit/1.0"})
    with urllib.request.urlopen(req,timeout=80) as f:source=f.read()
    if not zipfile.is_zipfile(io.BytesIO(source)):raise RuntimeError("NOT_A_ZIP")
    return source,zipfile.ZipFile(io.BytesIO(source))

def clean_target(df):
    # Corrected value supersedes original only when actually recorded.
    a=df["target_flower_corrected"].astype("string").str.strip()
    b=df["target_flower"].astype("string").str.strip()
    a=a.mask(a.isin(["","nan","NA","None","<NA>"]))
    b=b.mask(b.isin(["","nan","NA","None","<NA>"]))
    return a.fillna(b)

def safe_top(series,n=15):
    a=series.dropna().astype(str).value_counts().head(n)
    return [{"value":str(k)[:130],"n":int(v)} for k,v in a.items()]

def intersections(df):
    # One site/month is not a full choice set. Crossed support requires >=2
    # target plants sampled in two or more months in the same place/year.
    group=df.groupby(["site","year"],dropna=False,sort=False)
    out={"site_years":int(group.ngroups),"site_year_ge2_dates":0,
         "site_year_ge2_months":0,"site_year_ge2_plants":0,
         "site_year_ge2_months_ge2_plants":0,"site_year_with_crossed_2plant_2month_support":0,
         "surveys_in_crossed_site_years":0, "site_month_with_ge2_targets":0,
         "site_month_total":0, "sampled_target_month_cells":0}
    count_by_site_month = df.groupby(["site","year","month"],dropna=False)
    out["site_month_total"]=int(count_by_site_month.ngroups)
    out["site_month_with_ge2_targets"]=int((count_by_site_month.target.nunique(dropna=True)>=2).sum())
    for _,g in group:
        dates=g.date.nunique(dropna=True)
        months=g.month.nunique(dropna=True)
        plants=g.target.nunique(dropna=True)
        if dates>=2:out["site_year_ge2_dates"]+=1
        if months>=2:out["site_year_ge2_months"]+=1
        if plants>=2:out["site_year_ge2_plants"]+=1
        if months>=2 and plants>=2:out["site_year_ge2_months_ge2_plants"]+=1
        wide=pd.crosstab(g.target,g.month)
        if int((wide.gt(0).sum(axis=1)>=2).sum())>=2:
            out["site_year_with_crossed_2plant_2month_support"]+=1
            out["surveys_in_crossed_site_years"]+=len(g)
    out["sampled_target_month_cells"]=int(df.groupby(["site","year","month","target"],dropna=False).ngroups)
    return out

def docx_dictionary(z):
    name="supporting-documents/ukpoms_fitcountdata_2017-2023_metadata.docx"
    b=z.read(name)
    with zipfile.ZipFile(io.BytesIO(b)) as w:
        xml=w.read("word/document.xml").decode("utf-8")
    import xml.etree.ElementTree as ET
    root=ET.fromstring(xml)
    ns={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    texts=[]
    for p in root.findall(".//w:p",ns):
        t="".join(x.text or "" for x in p.findall(".//w:t",ns)).strip()
        if t:texts.append(t)
    keys=["sample_id","target_flower_corrected","floral_unit_count","floral_unit",
          "flower_cover","recorder_type","all_insects_total","x1km_square","location_code"]
    matches=[]
    for i,s in enumerate(texts):
        if any(k.lower() in s.lower() for k in keys):
            matches.append({"row":i,"text":s[:350],
                            "next":texts[i+1][:350] if i+1<len(texts) else ""})
    return {"paragraph_count":len(texts),"key_matches":matches[:60]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",default="poms_fit_audit");args=ap.parse_args()
    out=Path(args.out);out.mkdir(exist_ok=True,parents=True)
    original,z=archive()
    result={"source":URL,"sha256":hashlib.sha256(original).hexdigest(),"bytes":len(original),
            "status":"SCHEMA_ONLY_NOT_ECOLOGICAL_RESULT","files":{},"metadata":docx_dictionary(z)}
    for key,member in MEMBERS.items():
        raw=z.read(member)
        try:raw.decode("utf-8");codec="utf-8"
        except UnicodeDecodeError:codec="latin-1"
        df=pd.read_csv(io.BytesIO(raw),encoding=codec,low_memory=False)
        expected=set(GUILDS)|{"sample_id","date","year","target_flower","target_flower_corrected","floral_unit_count","all_insects_total","x1km_square"}
        if not expected<=set(df):raise RuntimeError("MISSING_FIELD_"+str(sorted(expected-set(df))))
        for g in GUILDS+("all_insects_total",):
            df[g]=pd.to_numeric(df[g],errors="coerce")
        fcounts=pd.to_numeric(df.floral_unit_count,errors="coerce")
        dates=pd.to_datetime(df.date,errors="coerce",dayfirst=True)
        df=df.assign(date=dates,month=dates.dt.month,target=clean_target(df),
                     site=df["location_code"].astype("string") if key=="1km" else df["x1km_square"].astype("string"))
        nonneg=df[list(GUILDS)].ge(0).all(axis=1)
        complete=df[list(GUILDS)].notna().all(axis=1)
        guild_total=df[list(GUILDS)].sum(axis=1,min_count=len(GUILDS))
        matching=np.isclose(guild_total,df.all_insects_total)
        profile={"rows":len(df),"sha256_csv":hashlib.sha256(raw).hexdigest(),"encoding":codec,
            "years":safe_top(df.year,n=20),"months":safe_top(df.month,n=15),
            "unique_samples":int(df.sample_id.nunique(dropna=True)),
            "missing_sample_id":int(df.sample_id.isna().sum()),
            "site_count":int(df.site.nunique(dropna=True)),
            "unique_target_labels":int(df.target.nunique(dropna=True)),
            "target_counts_top":safe_top(df.target,n=25),
            "flower_unit_count_nonmissing":int(fcounts.notna().sum()),
            "flower_unit_positive":int(fcounts.gt(0).sum()),
            "flower_unit_min":float(fcounts.min()),"flower_unit_median":float(fcounts.median()),
            "flower_unit_types":safe_top(df.floral_unit,n=15),
            "flower_cover":safe_top(df.flower_cover,n=12),
            "flower_context":safe_top(df.flower_context,n=12),
            "guild_nonnegative_complete":int((nonneg&complete).sum()),
            "guild_sum_matches_all_total":int(matching.sum()),
            "guild_sum_different":int((~matching).sum()),
            "zero_all_insects":int(df.all_insects_total.eq(0).sum()),
            "guild_zero":{g:int(df[g].eq(0).sum()) for g in GUILDS},
            "guild_missing":{g:int(df[g].isna().sum()) for g in GUILDS},
            "valid_date":int(df.date.notna().sum()),
            "has_complete_10min_guild_observation":int((complete&nonneg&matching&df.date.notna()&df.target.notna()&fcounts.gt(0)).sum()),
            "recording_types":safe_top(df.recorder_type,n=12)}
        profile["exposure_support"]=intersections(df.loc[df.date.notna()&df.target.notna()&fcounts.gt(0)])
        result["files"][key]=profile
        print("FIT_PROFILE",key,json.dumps(profile,ensure_ascii=False),flush=True)
    (out/"profile.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print("FIT_SCHEMA_AUDIT_COMPLETE",flush=True)
    # Prohibits using this as a modeled ecological finding.
if __name__=="__main__":main()
