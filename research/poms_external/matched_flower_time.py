"""PoMS 2-flower x 2-month exact site-block matched interaction screen.

EXPLORATORY post-schema analysis. An observed within-site/month difference in
guild visits is NOT the same as adaptive sensory routing, resource availability,
or individual pollinator choice. No flower NOT surveyed is coded as a zero.
"""
from __future__ import annotations
import argparse, hashlib, io, itertools, json, math, urllib.request, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import nchypergeom_fisher, chi2

URL="https://data-package.ceh.ac.uk/data/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip"
CSV={
 "public":"data/ukpoms_publicfitcountdata_2017-2023.csv",
 "1km":"data/ukpoms_1kmfitcountdata_2017-2023.csv"}
GUILDS=("bumblebees","honeybees","solitary_bees","wasps","hoverflies","other_flies",
"butterflies_moths","beetles","insects_small","insects_other")

def get_archive():
    req=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-poms-matched-original-data/1.0"})
    with urllib.request.urlopen(req,timeout=75) as f:b=f.read()
    if not zipfile.is_zipfile(io.BytesIO(b)):raise RuntimeError("EIDC_SOURCE_NOT_ZIP")
    return b,zipfile.ZipFile(io.BytesIO(b))

def load(z,design):
    data=z.read(CSV[design])
    try:data.decode("utf-8"); codec="utf-8"
    except UnicodeDecodeError:codec="latin-1"
    raw=pd.read_csv(io.BytesIO(data),encoding=codec,low_memory=False)
    df=raw.copy()
    corrected=df.target_flower_corrected.astype("string").str.strip()
    source=df.target_flower.astype("string").str.strip()
    corrected=corrected.mask(corrected.eq(""))
    source=source.mask(source.eq(""))
    target=corrected.fillna(source)
    # "Other" contains MANY unrelated species and is NOT a coherent plant.
    # Keep only 14 explicitly named categories in main matched analysis.
    is_other=target.str.contains("Other - please describe",case=False,na=True)
    date=pd.to_datetime(df.date,errors="coerce",dayfirst=True)
    floral=pd.to_numeric(df.floral_unit_count,errors="coerce")
    numeric=df[list(GUILDS)+["all_insects_total"]].apply(pd.to_numeric,errors="coerce")
    mask=((~is_other)&date.notna()&floral.gt(0)&target.notna()&
      numeric.notna().all(axis=1)&numeric.ge(0).all(axis=1)&
      np.isclose(numeric[list(GUILDS)].sum(axis=1),numeric.all_insects_total))
    site=(df.location_code if design=="1km" else df.x1km_square).astype("string")
    mask=mask&site.notna()
    w=pd.DataFrame({"sample_id":df.sample_id,"site":site,"year":date.dt.year,
       "month":date.dt.month,"date":date,"plant":target,"units":df.floral_unit.astype("string"),
       "flowers":floral})
    for c in GUILDS:w[c]=numeric[c]
    w=w.loc[mask].copy()
    w=w.loc[w.month.between(4,9)]
    return w,{"original_rows":len(df),"main_eligible_surveys":len(w),
     "rows_excluded":int(len(df)-len(w)), "other_or_unresolved_target":int(is_other.fillna(True).sum()),
     "site_counts":int(w.site.nunique()),"sha256_csv":hashlib.sha256(data).hexdigest()}

def select_strata(w):
    """One 2x2 from each site-year; select based ONLY on survey exposure.

    All four combinations are observed (not imputed), each species' floral unit
    measurement is homogeneous, and site-year selection is independent of counts.
    """
    result=[]
    for (site,year),g in w.groupby(["site","year"],sort=True):
        if len(g)<4 or g.month.nunique()<2 or g.plant.nunique()<2:continue
        cells={(int(m),str(p)):a for (m,p),a in g.groupby(["month","plant"],sort=True)}
        months=sorted(set(m for m,p in cells))
        best=None
        for ma,mb in itertools.combinations(months,2):
            pa={p for m,p in cells if m==ma}
            pb={p for m,p in cells if m==mb}
            for p,q in itertools.combinations(sorted(pa&pb),2):
                blocks=[cells[(ma,p)],cells[(ma,q)],cells[(mb,p)],cells[(mb,q)]]
                if any(len(a)==0 for a in blocks):continue
                # Count unlike flower units separately; never mix units for
                # the same species in a two-month flower-unit rate comparison.
                if len(set(str(u) for a in (blocks[0],blocks[2]) for u in a.units.dropna()))!=1:continue
                if len(set(str(u) for a in (blocks[1],blocks[3]) for u in a.units.dropna()))!=1:continue
                n=[len(a) for a in blocks]
                score=(min(n),sum(n),-abs(mb-ma),-ma,-mb)
                if best is None or score>best[0]:
                    best=(score,(int(ma),int(mb),str(p),str(q)),blocks)
        if best is None:continue
        score,(ma,mb,p,q),blocks=best
        ns=[len(a) for a in blocks]
        # Months are rows, flowers columns, cells in order ma/p,ma/q,mb/p,mb/q.
        exposure=np.array(ns,dtype=float).reshape(2,2)
        flow=np.array([float(a.flowers.sum()) for a in blocks]).reshape(2,2)
        def center_day(a):
            return float(np.median(a.date.values.astype("datetime64[D]").astype("int64")))
        offset=[abs(center_day(blocks[0])-center_day(blocks[1])),
                abs(center_day(blocks[2])-center_day(blocks[3]))]
        entry={"site":str(site),"year":int(year),"months":[ma,mb],"plants":[p,q],
           "cell_survey_counts":ns,"surveys":sum(ns),
           "flower_unit_exposures":flow.tolist(),"survey_exposures":exposure.tolist(),
           "within_month_day_gap":offset,"within_7_days_both_months":max(offset)<=7,
           "cell_values":{c:np.array([int(a[c].sum()) for a in blocks]).reshape(2,2).tolist()
                          for c in GUILDS}}
        result.append(entry)
    return result

def exact_conditional_2x2(y,exposure):
    """Fisher noncentral hypergeometric null with Poisson exposure offsets.

    Under mu_{month,plant} = exposure_{month,plant} * a_month * b_plant,
    conditioning on observed row and column visitor-count margins leaves
    X11 ~ FisherNoncentralHypergeom(M, col1, row1, odds=E11*E22/E12/E21).
    This conditions on BOTH guild activity by month and target-plant totals.
    """
    a=np.asarray(y,dtype=np.int64)
    e=np.asarray(exposure,dtype=float)
    if a.shape!=(2,2) or e.shape!=(2,2) or np.any(a<0) or np.any(e<=0):
        raise ValueError("2x2 nonnegative integer counts and positive exposures")
    if int(a.sum())<2:return None
    rows=a.sum(axis=1);cols=a.sum(axis=0)
    lo=max(0,int(rows[0]-cols[1]));hi=min(int(rows[0]),int(cols[0]))
    if lo>=hi:return None
    odds=float(e[0,0]*e[1,1]/(e[0,1]*e[1,0]))
    if not math.isfinite(odds) or odds<=0:raise ValueError("invalid offset odds")
    dist=nchypergeom_fisher(int(a.sum()),int(cols[0]),int(rows[0]),odds)
    support=np.arange(lo,hi+1,dtype=int)
    pmf=dist.pmf(support)
    if not np.isfinite(pmf).all():raise ValueError("nonfinite conditional pmf")
    p=float(min(1.0,pmf[pmf<=float(dist.pmf(int(a[0,0])))+1e-12].sum()))
    logor=math.log((a[0,0]+.5)*(a[1,1]+.5)/((a[0,1]+.5)*(a[1,0]+.5)))-math.log(odds)
    return {"p":p,"log_interaction_or":logor,"n_visits":int(a.sum())}

def bh(pvals):
    p=np.array(pvals,dtype=float);order=np.argsort(p);out=np.ones_like(p)
    n=len(p);prev=1.
    for j in range(n-1,-1,-1):
        idx=order[j];prev=min(prev,float(p[idx])*n/(j+1));out[idx]=prev
    return out

def analyze_panel(rows,mode,day_matched=False,only_one_site_year=True):
    filtered=[x for x in rows if (not day_matched or x["within_7_days_both_months"])]
    if only_one_site_year:
        # Treat spatial square as the independent replication unit.
        keep={}
        for x in filtered:
            k=x["site"];rank=(x["surveys"],min(x["cell_survey_counts"]),-x["year"])
            if k not in keep or rank>keep[k][0]:keep[k]=(rank,x)
        filtered=[x for rank,x in keep.values()]
    tests=[]
    for guild in GUILDS:
        obs=[]
        for row in filtered:
            exp=row["survey_exposures"] if mode=="surveys" else row["flower_unit_exposures"]
            r=exact_conditional_2x2(row["cell_values"][guild],exp)
            if r is not None:obs.append(r)
        if obs:
            stat=float(-2*np.log([max(p["p"],1e-300) for p in obs]).sum())
            combined=float(chi2.sf(stat,2*len(obs)))
            tests.append({"guild":guild,"tested_sites":len(obs),"combined_p_exploratory":combined,
                "median_log_interaction_or":float(np.median([p["log_interaction_or"] for p in obs])),
                "nominal_p_le_005":int(sum(p["p"]<=.05 for p in obs)),
                "total_guild_visits":int(sum(p["n_visits"] for p in obs))})
        else:tests.append({"guild":guild,"tested_sites":0,"combined_p_exploratory":None})
    valid=[x for x in tests if x["tested_sites"]>0]
    if valid:
        adj=bh([x["combined_p_exploratory"] for x in valid])
        for row,p in zip(valid,adj):row["BH_q_exploratory"]=float(p)
    return {"sampled_site_years":len(filtered),"independent_sites":len(set(x["site"] for x in filtered)),
        "survey_rows_in_selected_2x2":sum(x["surveys"] for x in filtered),
        "within7day_pair":day_matched,"one_year_per_site":only_one_site_year,
        "exposure":mode,"tests":tests}

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--out",default="poms_matched_results")
    args=parser.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    data,z=get_archive()
    report={"status":"EXPLORATORY_POST_SCHEMA_MATCHED_2X2",
      "source":URL,"sha256_zip":hashlib.sha256(data).hexdigest(),
      "inference":"guild-specific target-plant x month interaction in observed 10min FIT counts; NOT true resource availability, pollinator choice or sensory routeability",
      "limitations":["selected flowers per FIT count; unsurveyed flowers never coded zero",
                     "target flower sampling and phenology not randomized",
                     "flower-unit exposure proportional-rate model is an assumption",
                     "site-month weather may differ despite within7day restriction",
                     "public x1km_square may contain spatially different observer patches",
                     "archive field checks are not causal outcome validation",
                     "post-schema exploratory gate; no preregistered confirmatory p values"],"designs":{}}
    for design in ("1km","public"):
        w,q=load(z,design)
        rows=select_strata(w)
        # Main chosen exposure: single fully sampled 2x2 per independent site,
        # with comparisons sensitivity-matched to +/- 7 days per month.
        variants={}
        for daymatch in (False,True):
            for mode in ("surveys","flowers"):
                tag=("within7d" if daymatch else "all_crossed")+"_"+mode
                variants[tag]=analyze_panel(rows,mode,day_matched=daymatch,only_one_site_year=True)
        report["designs"][design]={"quality":q,
           "candidate_site_year_crosses":len(rows),
           "candidate_crosses_same7d":int(sum(x["within_7_days_both_months"] for x in rows)),
           "candidate_distinct_sites":len(set(x["site"] for x in rows)),
           "candidate_distinct_sites_same7d":len({x["site"] for x in rows if x["within_7_days_both_months"]}),
           "survey_rows_candidate":int(sum(x["surveys"] for x in rows)),
           "survey_rows_within7d":int(sum(x["surveys"] for x in rows if x["within_7_days_both_months"])),
           "median_min_cell_surveys":float(np.median([min(x["cell_survey_counts"]) for x in rows])) if rows else None,
           "variants":variants}
        print("MATCHED_FIT_RESULT",design,json.dumps(report["designs"][design],ensure_ascii=False),flush=True)
    (out/"summary.json").write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print("MATCHED_FIT_ANALYSIS_COMPLETE",flush=True)

if __name__=="__main__":main()
