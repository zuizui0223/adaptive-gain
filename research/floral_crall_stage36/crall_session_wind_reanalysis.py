"""Stage36: independent session-grain reanalysis of actual Crall 2020 data.

Not an invented wind x floral-scent 2x2. The 70 collection sessions are
reobservations at nine locations (perfume bait stations) with a weather
record per collection; source-bee records are NOT 450 independent wind units.

Primary exploratory estimand: within-site coefficient of mean wind speed
for log(1 + recorded scent-bait visitation count), after demeaning by site.
Sensitivity: relative turbulence, leave-one-site-out, scent-bait strata,
site-cluster bootstrap, within-site shuffled-wind null. Different from the
authors' R lme4 Poisson GLMM with site+date random effects; not a numerical
replication of that GLMM. No measured flower landing or pollen transfer.
"""
from __future__ import annotations

import csv
import io
import json
import math
import random
import statistics
import sys
import zipfile
from collections import Counter,defaultdict
from pathlib import Path

PARENT=Path(__file__).resolve().parents[1]/"floral_wind_author_stage35"
sys.path.insert(0,str(PARENT))
from zenodo_crall_original_source import (  # noqa: E402
    _fetch, _candidate_download_urls, _verify_md5_if_declared,
    assess_api_metadata,_sha
)

AUTHOR_RECORD_ID=3743898
SESSION_FILE="Zenodo/collectionMetadata.csv"
INTEGRATED_FILE="Zenodo/integratedSpatialWindData.csv"
BEES_FILE="Zenodo/beedata.csv"
AUTHOR_SCRIPT="Zenodo/GenerateFiguresAndAnalyses_CrallEtAl_OrchidBeeWindEcology.R"
EXPECTED_SESSION_COLUMNS={"site","date","start.time","scent","count",
                          "wind.mean","rel.wind.KE"}


def _rows(raw):
    try:
        text=raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        # Some early source archives encode non-ASCII metadata notes
        # in Latin-1. Preserve source bytes/hash and record no edits.
        text=raw.decode("latin-1")
    rd=csv.reader(io.StringIO(text,newline=""))
    head=next(rd)
    if head and not head[0].strip():
        head[0]="_original_R_row_index"
    if len(set(head))!=len(head):
        raise ValueError("NO_GO_DUPLICATED_SOURCE_HEADER")
    rows=[]
    for row in rd:
        if len(row)!=len(head):
            raise ValueError("NO_GO_ORIGINAL_CSV_RAGGED")
        rows.append(dict(zip(head,row)))
    return rows


def extract_source_tables(archive_blob):
    if not zipfile.is_zipfile(io.BytesIO(archive_blob)):
        raise ValueError("NO_GO_NOT_ZENODO_ZIP")
    with zipfile.ZipFile(io.BytesIO(archive_blob)) as z:
        names=set(z.namelist())
        expected={SESSION_FILE,INTEGRATED_FILE,BEES_FILE,AUTHOR_SCRIPT}
        if not expected.issubset(names):
            raise ValueError("NO_GO_MISSING_AUTHOR_INPUTS")
        sessions=_rows(z.read(SESSION_FILE))
        integration=_rows(z.read(INTEGRATED_FILE))
        bees=_rows(z.read(BEES_FILE))
        script=z.read(AUTHOR_SCRIPT).decode("utf-8-sig",errors="replace")
        hashes={x:_sha(z.read(x)) for x in expected}
    if not sessions or not integration or not bees:
        raise ValueError("NO_GO_EMPTY_AUTHOR_SOURCE")
    if not EXPECTED_SESSION_COLUMNS.issubset(sessions[0]):
        raise ValueError("NO_GO_SESSION_SOURCE_SCHEMA")
    if not {"site","wind.mean","count","keep"}.issubset(integration[0]):
        raise ValueError("NO_GO_INTEGRATED_SOURCE_SCHEMA")
    import re
    tokens={pat:bool(re.search(pat,script,re.I)) for pat in (
       r"glmer\s*\(",r"glm\s*\(",r"wind\.mean",r"rel\.wind\.KE",
       r"keep\s*==",r"count\s*~")}
    return {
        "sessions":sessions,"integrated":integration,"bees":bees,
        "original_source_file_sha256":hashes,
        "original_R_model_tokens_detected":tokens,
        "original_R_full_content_not_redistributed":True
    }


def _float(v,name):
    try:val=float(str(v).strip())
    except (ValueError,TypeError) as err:
        raise ValueError("NO_GO_INVALID_SOURCE_NUMERIC_"+name.upper()) from err
    if not math.isfinite(val):
        raise ValueError("NO_GO_NONFINITE_SOURCE_"+name.upper())
    return val


def prepare_sessions(rows, require_70=True):
    accepted=[];skipped=Counter()
    for row in rows:
        site=(row.get("site") or "").strip()
        date=(row.get("date") or "").strip()
        scent=(row.get("scent") or "").strip()
        if not site or not date:
            skipped["missing_site_or_date"]+=1
            continue
        count_s=(row.get("count") or "").strip()
        wind_s=(row.get("wind.mean") or "").strip()
        if not count_s or not wind_s or count_s.lower()=="na" or wind_s.lower()=="na":
            skipped["missing_wind_or_count"]+=1
            continue
        count=_float(count_s,"count")
        wind=_float(wind_s,"wind")
        if count<0 or int(count)!=count or wind<0:
            raise ValueError("NO_GO_NEGATIVE_COUNT_OR_WIND")
        turbulence_s=(row.get("rel.wind.KE") or "").strip()
        turbulence=None
        if turbulence_s and turbulence_s.lower()!="na":
            turbulence=_float(turbulence_s,"turbulence")
        accepted.append({
          "site":site,"date":date,"scent":scent,
          "count":int(count),"wind":wind,"turbulence":turbulence,
          "y":math.log1p(count)})
    if require_70 and (len(rows)!=70 or len(accepted)<45):
        raise ValueError("NO_GO_ORIGINAL_SESSION_GRAIN_OR_MISSINGNESS")
    nsites=len({r["site"] for r in accepted})
    if require_70 and nsites!=9:
        raise ValueError("NO_GO_PUBLISHED_NINE_SITE_GRAIN")
    return accepted,dict(skipped)


def _groups(rows):
    g=defaultdict(list)
    for x in rows:g[x["site"]].append(x)
    return g


def slope_site_demeaned(rows,key="wind",ykey="y"):
    groups=_groups(rows)
    swy=sww=0.
    n=0
    for site,v in groups.items():
        v=[x for x in v if x.get(key) is not None and x.get(ykey) is not None]
        if len(v)<2:
            continue
        w0=sum(x[key] for x in v)/len(v)
        y0=sum(x[ykey] for x in v)/len(v)
        for x in v:
            dw=x[key]-w0
            swy+=dw*(x[ykey]-y0)
            sww+=dw**2
        n+=len(v)
    if sww<=1e-15:
        raise ValueError("NO_GO_NO_WITHIN_SITE_WIND_CONTRAST")
    return {"slope_per_wind_m_s":swy/sww,
            "slope_for_0p1_m_s":swy/sww*.1,
            "within_slope_exponential_log1p_percent_for_0p1_m_s":
                (math.exp((swy/sww)*.1)-1)*100,
            "raw_source_session_rows_used":n,
            "original_distinct_sites":len(groups),
            "log1p_count_NOT_original_Poisson_effect":True}


def slope_between_site_means(rows):
    groups=_groups(rows)
    means=[(sum(x["wind"] for x in v)/len(v),
            sum(x["y"] for x in v)/len(v)) for v in groups.values()]
    if len(means)<3:
        raise ValueError("NO_GO_NOT_ENOUGH_SITES")
    meanw=sum(x for x,y in means)/len(means)
    meany=sum(y for x,y in means)/len(means)
    cov=sum((x-meanw)*(y-meany) for x,y in means)
    var=sum((x-meanw)**2 for x,y in means)
    yvar=sum((y-meany)**2 for x,y in means)
    return {
       "site_n":len(means),
       "between_site_slope_per_0p1_m_s":(cov/var*.1 if var else None),
       "between_site_pearson_r":cov/math.sqrt(var*yvar) if var and yvar else None,
       "not_independent_causal_between_site_comparison":True}


def slope_partial_turbulence(rows):
    vv=[x for x in rows if x["turbulence"] is not None]
    groups=_groups(vv)
    sww=stt=swt=swy=sty=0.
    n=0
    for group in groups.values():
        if len(group)<2:continue
        w=sum(x["wind"] for x in group)/len(group)
        t=sum(x["turbulence"] for x in group)/len(group)
        y=sum(x["y"] for x in group)/len(group)
        for x in group:
            dw=x["wind"]-w
            dt=x["turbulence"]-t
            dy=x["y"]-y
            sww+=dw*dw
            stt+=dt*dt
            swt+=dw*dt
            swy+=dw*dy
            sty+=dt*dy
        n+=len(group)
    denom=sww*stt-swt*swt
    if denom<=1e-15:
        return {"status":"NO_GO_SINGULAR_WIND_TURBULENCE",
                "source_rows_available":n}
    return {
      "status":"WITHIN_SITE_LOG1P_SLOPE_CONTROLLING_TURBULENCE",
      "wind_beta_per_0p1_m_s":.1*(swy*stt-sty*swt)/denom,
      "turbulence_beta_per_unit":(sty*sww-swy*swt)/denom,
      "n_source_sessions":n,
      "not_a_reproduced_Poisson_mixed_model":True}


def _quantile(v,p):
    v=sorted(v)
    loc=(len(v)-1)*p
    i=int(loc)
    return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(loc-i)


def cluster_bootstrap_sites(rows,replicates=4000,seed=20261115):
    if type(replicates) is not int or not 100<=replicates<=100000:
        raise ValueError("NO_GO_BOOTSTRAP_SETTINGS")
    groups=list(_groups(rows).values())
    rng=random.Random(seed)
    vals=[]
    for _ in range(replicates):
        sampled=[]
        for j in range(len(groups)):
            chosen=groups[rng.randrange(len(groups))]
            # Treat each resampled site as a distinct sampled cluster,
            # even if the same physical source site was selected twice.
            sampled.extend(dict(r,site="bootstrap_site_"+str(j)) for r in chosen)
        try:
            vals.append(slope_site_demeaned(sampled)["slope_for_0p1_m_s"])
        except ValueError:
            continue
    if len(vals)<.95*replicates:
        raise ValueError("NO_GO_BOOTSTRAP_TOO_FEW_VALID_RESAMPLES")
    return {
      "site_cluster_bootstrap_draws":replicates,
      "valid_draws":len(vals),
      "bootstrap_site_count":len(groups),
      "wind_slope_0p1_m_s_percentile95":
          [_quantile(vals,.025),_quantile(vals,.975)],
      "original_site_spatial_independence_not_verified":True,
      "not_an_assigned_wind_causal_CI":True}


def permutation_within_sites(rows,replicates=4000,seed=20261115):
    if type(replicates) is not int or replicates<100:
        raise ValueError("NO_GO_PERMUTATION_SETTINGS")
    bysite=list(_groups(rows).values())
    observed=slope_site_demeaned(rows)["slope_for_0p1_m_s"]
    rng=random.Random(seed)
    greater=0
    for _ in range(replicates):
        shuffled=[]
        for group in bysite:
            winds=[v["wind"] for v in group]
            rng.shuffle(winds)
            shuffled.extend(dict(record,wind=w) for record,w in zip(group,winds))
        estimate=slope_site_demeaned(shuffled)["slope_for_0p1_m_s"]
        if abs(estimate)>=abs(observed):
            greater+=1
    return {"observed_log1p_beta_per_0p1_m_s":observed,
            "site_stratified_permutations":replicates,
            "two_sided_permutation_fraction":(greater+1)/(replicates+1),
            "assumption_of_exchangeable_wind_within_site_unverified":True,
            "time_of_day_and_date_possible_confounders":True,
            "not_randomized_wind_assignment":True}


def slope_site_and_date_fixed_effects(rows):
    """Two-way categorical fixed effects by alternating group demeaning.

    This is an OLS Frisch-Waugh-Lovell calculation on log(1+count),
    NOT the authors' Poisson mixed model. Fixed date blocks might
    absorb much temporal variation and can leave little identified wind
    contrast. Return a NO_GO, never an arbitrary zero slope, if the
    residualized wind has negligible variance.
    """
    if len(rows)<5:
        raise ValueError("NO_GO_DATE_FE_TOO_FEW_SESSIONS")
    def residualize(key):
        values=[float(r[key]) for r in rows]
        groups=[]
        for term in ("site","date"):
            index=defaultdict(list)
            for i,r in enumerate(rows):
                index[r[term]].append(i)
            groups.append(list(index.values()))
        converged=False
        for _ in range(2000):
            before=values[:]
            for group_set in groups:
                for idx in group_set:
                    mu=sum(values[i] for i in idx)/len(idx)
                    for i in idx:
                        values[i]-=mu
            if max(abs(a-b) for a,b in zip(before,values))<1e-11:
                converged=True
                break
        if not converged:
            raise ValueError("NO_GO_SITE_DATE_RESIDUALIZATION_NOT_CONVERGED")
        return values
    w=residualize("wind")
    y=residualize("y")
    sww=sum(v*v for v in w)
    if sww<1e-12:
        return {
            "status":"NO_GO_WIND_COLLINEAR_WITH_SITE_AND_DATE",
            "source_sessions":len(rows),
            "date_groups":len(set(r["date"] for r in rows)),
            "not_original_mixed_model":True}
    return {
        "status":"SITE_AND_DATE_FIXED_EFFECT_LOG1P_ASSOCIATION",
        "slope_per_0p1_m_s":.1*sum(a*b for a,b in zip(w,y))/sww,
        "site_groups":len(set(r["site"] for r in rows)),
        "date_groups":len(set(r["date"] for r in rows)),
        "n_sessions":len(rows),
        "not_original_mixed_model":True,
        "not_causal":True
    }


def _summary(rows):
    sites=_groups(rows)
    scent_counts=dict(Counter(r["scent"] for r in rows))
    return {
       "n_sessions_used":len(rows),
       "n_sites":len(sites),
       "sum_source_bee_visits_across_sessions":sum(x["count"] for x in rows),
       "count_min":min(x["count"] for x in rows),
       "count_max":max(x["count"] for x in rows),
       "sessions_with_zero_visitors":sum(x["count"]==0 for x in rows),
       "wind_min_m_s":min(x["wind"] for x in rows),
       "wind_max_m_s":max(x["wind"] for x in rows),
       "wind_median_m_s":statistics.median(x["wind"] for x in rows),
       "per_site_n_sessions_min":min(len(x) for x in sites.values()),
       "per_site_n_sessions_max":max(len(x) for x in sites.values()),
       "distinct_recorded_dates":len(set(x["date"] for x in rows)),
       "source_scent_types_sessions":scent_counts,
       "no_individual_original_session_rows_in_receipt":True}


def analyze_original_archive(archive_blob,permutations=4000,bootstrap=4000):
    tables=extract_source_tables(archive_blob)
    rows,skips=prepare_sessions(tables["sessions"])
    within=slope_site_demeaned(rows)
    between=slope_between_site_means(rows)
    part=slope_partial_turbulence(rows)
    date_fe=slope_site_and_date_fixed_effects(rows)
    cineole=[r for r in rows if r["scent"]=="cin"]
    cineole_only=(slope_site_demeaned(cineole)
                  if len(cineole)>=45 else
                  {"status":"NO_GO_TOO_FEW_CINEOLE_SESSIONS"})
    loo=[]
    sites=sorted(_groups(rows))
    for one in sites:
        reduced=[x for x in rows if x["site"]!=one]
        loo.append(slope_site_demeaned(reduced)["slope_for_0p1_m_s"])
    # Author R source inclusion semantics are NOT inferred by this expression.
    integ=tables["integrated"]
    keep=Counter((x.get("keep") or "<missing>").strip() for x in integ)
    return {
      "status":"PUBLIC_AUTHOR_70_SESSION_WIND_ASSOCIATION_REANALYZED",
      "paper_doi":"10.1098/rsbl.2020.0103",
      "source_record_id":AUTHOR_RECORD_ID,
      "source_file_sha256":tables["original_source_file_sha256"],
      "original_R_model_tokens_detected":tables["original_R_model_tokens_detected"],
      "study_grain":_summary(rows),
      "input_collectionMetadata_original_rows":len(tables["sessions"]),
      "input_integratedSpatialWindData_original_rows":len(integ),
      "input_beedata_original_rows":len(tables["bees"]),
      "integrated_keep_flag_distribution":dict(keep),
      "session_missingness_exclusions":skips,
      "wind_within_site_association_log1p":within,
      "wind_between_site_association_log1p":between,
      "wind_within_site_turbulence_sensitivity":part,
      "wind_within_site_and_date_fixed_effect_sensitivity":date_fe,
      "cineole_only_within_site_sensitivity":cineole_only,
      "leave_one_original_site_out_wind_beta_0p1_range":[min(loo),max(loo)],
      "site_cluster_bootstrap":cluster_bootstrap_sites(rows,bootstrap),
      "site_stratified_permutation":permutation_within_sites(rows,permutations),
      "authors_original_R_GLM_MIXED_MODEL_REPLICATED":False,
      "not_odor_on_vs_off":True,
      "not_flower_or_pollen_transfer":True,
      "not_a_causal_wind_effect":True,
      "not_an_empirical_wind_by_scent_2x2":True,
      "no_original_raw_csv_or_R_script_redistributed":True
    }


def get_paper_zenodo_archive():
    meta=json.loads(_fetch(f"https://zenodo.org/api/records/{AUTHOR_RECORD_ID}"))
    _=assess_api_metadata(meta,AUTHOR_RECORD_ID)
    candidates=_candidate_download_urls(meta)
    for filename,url,checksum,size in candidates:
        if filename!="CrallEtAl_OrchidBeeWindEcology.zip":
            continue
        data=_fetch(url)
        if size is not None and len(data)!=int(size):
            raise ValueError("NO_GO_AUTHOR_ZIP_SIZE_MISMATCH")
        _verify_md5_if_declared(data,checksum)
        return data
    raise ValueError("NO_GO_ORIGINAL_AUTHOR_ARCHIVE_NOT_RETRIEVED")


def main():
    output=Path("stage36_original_wind_receipts")
    output.mkdir(exist_ok=True)
    try:
        blob=get_paper_zenodo_archive()
        result=analyze_original_archive(blob)
    except (OSError,ValueError,zipfile.BadZipFile) as err:
        result={
          "status":"NO_GO_AUTHOR_SOURCE_OR_ANALYSIS",
          "error_kind":type(err).__name__,
          "diagnostic":str(err)[:500],
          "original_session_model_estimated":False,
          "ecological_result_claimed":False
        }
    (output/"stage36_within_between_site_wind.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    preview={k:result.get(k) for k in (
       "status","study_grain","wind_within_site_association_log1p",
       "wind_between_site_association_log1p",
       "wind_within_site_turbulence_sensitivity",
       "wind_within_site_and_date_fixed_effect_sensitivity",
       "cineole_only_within_site_sensitivity",
       "leave_one_original_site_out_wind_beta_0p1_range",
       "site_cluster_bootstrap","site_stratified_permutation",
       "integrated_keep_flag_distribution",
       "error_kind","diagnostic")}
    print(json.dumps(preview,sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
