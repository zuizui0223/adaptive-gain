"""Stage 3f: site-date Pan floral-richness context of selected FIT wind/guild effect.

All original data from one monitoring PROGRAMME, two spatially distinct
surveys: Pan 2m around each station, FIT 10-min visits to a chosen target.
This does NOT reconstruct insects' experienced alternatives or choice routing.
Analyses exploratory/post-hoc relative to prior observed wind signal.
"""
from __future__ import annotations
import argparse, hashlib, io, json, sys, warnings, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm

# Reuse exactly the prior registered FIT model/eligibility, not a re-invented
# regression that could change original censoring or source count semantics.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"poms_fit"))
from fit_associations import prepare, WIND
from clock_observer_sensitivity import (
    audit_clock, label_clock, CLOCK_BINS,
    augmented_pair, formula as stage3d_formula
)
from site_date_join import (
    safe_source_csv, build_pan_environment, clean_keys,
    PAN_PARTS, FIT_MEMBER, FIT_HASH, KEYS, parse_original_dates
)

def prepare_matched_context(fit_original, pan_daily):
    """One FIT per row: exact site/date and exactly five nearby Pan stations."""
    # The pre-existing FIT parser supplies dayfirst=True, which can be
    # ambiguous for ISO YYYY-MM-DD strings if inferred from one row.
    # Decode the source's actual date format first, while keeping every
    # original observation and all earlier eligibility rules intact.
    source_fit=fit_original.copy()
    source_fit["date"]=parse_original_dates(source_fit["date"])
    if source_fit["date"].isna().any():
        raise ValueError("unparseable FIT source dates, cannot infer calendar")
    fit,fit_flow=prepare(source_fit,"one_km",outcome="all_insects_total")
    fit=clean_keys(fit)
    if fit.sample_id.duplicated().any():raise ValueError("duplicate FIT sample_id")
    if fit[KEYS].isna().any().any():raise ValueError("unidentified 1km FIT key/date")
    if pan_daily.duplicated(KEYS).any():raise ValueError("pan site/date duplicate")
    joined=fit.merge(pan_daily,on=KEYS,how="left",validate="many_to_one",indicator=True)
    if len(joined)!=len(fit) or joined.sample_id.nunique()!=fit.sample_id.nunique():
        raise ValueError("FIT multiplied during Pan join")
    exact=joined["_merge"].eq("both")
    complete=(joined.stations.eq(5)&joined.station_types.eq(5)).fillna(False)
    flowers=joined.pan_recorded_flowering_taxa.notna()
    # A pan site-date with absent occurrence rows is NOT zero flowers.
    matched=joined.loc[exact&complete&flowers].copy()
    count_labels=matched.pan_recorded_flowering_taxa.astype(float)
    if (count_labels<=0).any():raise ValueError("matched richness <=0: unresolved flower completeness")
    time,audit=audit_clock(matched)
    if audit["parsed_fraction"]<0.95:
        raise ValueError("source recorded start time parse coverage <95%")
    matched["clock_bin"]=pd.Categorical(
        [label_clock(None if pd.isna(x) else x) for x in time],
        categories=list(CLOCK_BINS))
    missing_clock=int(matched.clock_bin.isna().sum())
    matched=matched.loc[matched.clock_bin.notna()].copy()
    matched["clock_bin"]=matched["clock_bin"].cat.remove_unused_categories()
    # Patsy/statsmodels cannot interpret pandas StringDtype ("string[python]")
    # as a categorical design factor. Coerce valid, already-audited site labels
    # to native Python object strings only AFTER strict geospatial matching.
    matched["location_code"]=matched["location_code"].astype(object)
    matched["recorder_type_audited"]=matched.recorder_type.fillna("__SOURCE_MISSING__").astype(str)
    matched["flower_cover_audited"]=matched.flower_cover.fillna("__SOURCE_MISSING__").astype(str)
    matched["pan_logrich"]=np.log1p(matched.pan_recorded_flowering_taxa.astype(float))
    pair=(matched.bumblebees+matched.other_flies)>0
    eligible=matched.loc[pair].copy()
    if not len(eligible):raise ValueError("no paired guild observations in matched context")
    richness_median=float(eligible.pan_logrich.median())
    eligible["pan_rich_center"]=eligible.pan_logrich-richness_median
    eligible["pan_gentle_x_rich"]=(
        (eligible.wind_speed==WIND[1]).astype(int)*eligible.pan_rich_center)
    eligible["pan_strong_x_rich"]=(
        (eligible.wind_speed==WIND[2]).astype(int)*eligible.pan_rich_center)
    bysite=eligible.groupby("location_code").pan_recorded_flowering_taxa.nunique()
    sizes=eligible.wind_speed.value_counts()
    support={
        "original_fit_surveys":len(fit_original),
        "stage3d_covariate_eligible_fit":len(fit),
        "exact_site_grid_date_context_surveys":int(exact.sum()),
        "exact_five_unique_pan_station_context_surveys":int((exact&complete).sum()),
        "exact_five_pan_stations_with_flower_taxa":int((exact&complete&flowers).sum()),
        "matched_clock_parse_rate":audit["parsed_fraction"],
        "matched_clock_excluded":missing_clock,
        "matched_pair_positive_fit_surveys":len(eligible),
        "matched_pair_absent_fit_surveys":int((~pair).sum()),
        "matched_unique_sites":int(eligible.location_code.nunique()),
        "sites_with_multiple_recorded_pan_richness_values":int((bysite>1).sum()),
        "recorded_pan_taxa_distinct_values":int(eligible.pan_recorded_flowering_taxa.nunique()),
        "recorded_pan_richness_min":int(eligible.pan_recorded_flowering_taxa.min()),
        "recorded_pan_richness_q25":float(eligible.pan_recorded_flowering_taxa.quantile(.25)),
        "recorded_pan_richness_median":float(eligible.pan_recorded_flowering_taxa.median()),
        "recorded_pan_richness_q75":float(eligible.pan_recorded_flowering_taxa.quantile(.75)),
        "recorded_pan_richness_max":int(eligible.pan_recorded_flowering_taxa.max()),
        "centering_log1p_richness_median":richness_median,
        "wind_surveys_in_paired_context":{str(k):int(v) for k,v in sizes.items()},
        "nearby_pan_five_station_complete_sample_not_same_fit_quadrat":True,
        "fit_row_multiplication":0
    }
    failures=[]
    if len(eligible)<100:failures.append("<100 paired surveys")
    if eligible.location_code.nunique()<10:failures.append("<10 source sites")
    if eligible.pan_recorded_flowering_taxa.nunique()<4:failures.append("<4 Pan richness levels")
    if (bysite>1).sum()<10:failures.append("<10 sites with richness variation")
    if any(sizes.get(w,0)<30 for w in [WIND[0],WIND[2]]):
        failures.append("<30 surveys in one wind reference/extreme level")
    support["model_gate"]="PASS_CONTEXTUAL_OVERLAP" if not failures else "NO_GO_CONTEXTUAL_MODEL_INADEQUATE"
    support["gate_failures"]=failures
    return eligible,support

def _estimate(m, names, weights):
    beta=np.zeros(len(m.params))
    for name,w in zip(names,weights):
        if name not in m.params:raise ValueError("required coefficient missing "+name)
        beta[m.params.index.get_loc(name)]+=w
    effect=float(beta@m.params.to_numpy())
    variance=float(beta@m.cov_params().to_numpy()@beta)
    if variance<0 or not np.isfinite([effect,variance]).all():
        raise ValueError("nonfinite or negative covariance in requested contrast")
    se=float(np.sqrt(variance))
    return {
        "OR":float(np.exp(effect)),
        "ci95_low":float(np.exp(effect-1.95996398454*se)),
        "ci95_high":float(np.exp(effect+1.95996398454*se)),
        "logOR":effect,
        "site_cluster_se":se}

def _fit_one(d, mode):
    if mode not in ("richness_main","wind_by_richness"):
        raise ValueError("undeclared model mode")
    rhs=stage3d_formula("one_km")+" + pan_rich_center"
    if mode=="wind_by_richness":
        rhs+=" + pan_gentle_x_rich + pan_strong_x_rich"
    result={"mode":mode,"rhs":rhs,"n_surveys":len(d),
            "source_site_clusters":int(d.location_code.nunique())}
    try:
        X=patsy.dmatrix(rhs,d,return_type="dataframe")
        if len(X)!=len(d):
            raise ValueError("model matrix silently changed original FIT survey grain")
        rank=int(np.linalg.matrix_rank(X.to_numpy()))
        result["design_columns"]=len(X.columns)
        result["design_rank"]=rank
        if rank!=len(X.columns):
            result["status"]="NO_GO_DESIGN_RANK_DEFICIENT";return result
        y=np.column_stack([d.bumblebees.to_numpy(dtype=int),
                           d.other_flies.to_numpy(dtype=int)])
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter("always")
            m=sm.GLM(y,X,family=sm.families.Binomial()).fit(
                maxiter=180,cov_type="cluster",
                cov_kwds={"groups":d.location_code.astype(str).to_numpy()})
        result["model_warnings"]=[str(w.message) for w in seen][-8:]
        result["converged"]=bool(m.converged)
        result["pearson_dispersion_per_residual_df"]=float(m.pearson_chi2/m.df_resid)
        if not m.converged:
            result["status"]="NO_GO_NONCONVERGED";return result
        terms=[n for n in m.params.index if n.startswith("C(wind_speed")]
        strong=[n for n in terms if "Leaves moving strongly" in n]
        required=[*terms,"pan_rich_center"]
        if mode=="wind_by_richness":
            required.extend(["pan_gentle_x_rich","pan_strong_x_rich"])
        ci=m.conf_int()
        result["all_parameter_nonfinite_ci_cells"]=int(
            (~np.isfinite(ci.to_numpy())).sum())
        result["required_contrast_coefficients"]=required
        if len(terms)!=2 or len(strong)!=1 or not set(required)<=set(ci.index):
            result["status"]="NO_GO_MISSING_WIND_OR_CONTEXT_COEFFICIENT";return result
        target_ci=ci.loc[required].to_numpy()
        target_cov=m.cov_params().loc[required,required].to_numpy()
        result["required_contrast_nonfinite_ci_cells"]=int(
            (~np.isfinite(target_ci)).sum())
        result["required_contrast_nonfinite_cov_cells"]=int(
            (~np.isfinite(target_cov)).sum())
        # Nuisance fixed-effect coefficients may be poorly identified; the
        # study estimand is the declared wind/richness contrast. Never claim
        # a finite or meaningful interaction unless ALL needed coefficient
        # intervals and the COMPLETE small contrast covariance are finite.
        if not np.isfinite(target_ci).all() or not np.isfinite(target_cov).all():
            result["status"]="NO_GO_NONFINITE_DECLARED_CONTRAST";return result
        if np.max(np.abs(target_ci))>100:
            result["status"]="NO_GO_EXTREME_DECLARED_CONTRAST_CI";return result
        strong=strong[0]
        result["status"]="FITTED"
        result["strong_vs_calm_at_median_richness"]=_estimate(m,[strong],[1])
        result["pan_richness_main_coefficient"]=_estimate(m,["pan_rich_center"],[1])
        if mode=="wind_by_richness":
            names=["pan_gentle_x_rich","pan_strong_x_rich"]
            row=np.zeros((2,len(m.params)))
            for i,name in enumerate(names):
                row[i,m.params.index.get_loc(name)]=1
            wald=m.wald_test(row,scalar=True)
            result["joint_wind_by_richness"]={
                "chi2":float(wald.statistic),"df":2,"p":float(wald.pvalue)}
            result["strong_wind_by_richness_log_slope"]=_estimate(
                m,["pan_strong_x_rich"],[1])
            center=float(d.pan_logrich.median())
            for q,label in [(0.25,"q25"),(0.75,"q75")]:
                value=float(d.pan_recorded_flowering_taxa.quantile(q))
                delta=float(np.log1p(value)-center)
                result["strong_wind_OR_at_pan_richness_"+label]={
                    "pan_recorded_taxa":value,
                    **_estimate(m,[strong,"pan_strong_x_rich"],[1,delta])}
    except Exception as exc:
        result["status"]="MODEL_FAILURE"
        result["error"]=str(exc)
    return result

def analyze(root:Path):
    with zipfile.ZipFile(root/"pan_original_provider.zip") as z:
        samples,enc_s,sha_s=safe_source_csv(z,*PAN_PARTS["samples"])
        flowers,enc_f,sha_f=safe_source_csv(z,*PAN_PARTS["flowers"])
    with zipfile.ZipFile(root/"fit_original_provider.zip") as z:
        fit,enc_fit,sha_fit=safe_source_csv(z,FIT_MEMBER,FIT_HASH)
    pan_daily,pan_receipt,station=build_pan_environment(samples,flowers)
    data,support=prepare_matched_context(fit,pan_daily)
    result={
        "status":"exploratory_posthoc_same_PoMS_programme",
        "source_member_hashes":{
            "pan_samples":sha_s,"pan_flowers":sha_f,"FIT_1km":sha_fit},
        "source_original_rows":{
            "pan_stations":len(samples),"pan_flowers":len(flowers),
            "fit_1km":len(fit)},
        "support":support,
        "pan_data_quality":pan_receipt,
        "claim_boundary":"Pan flora within 2m of five trap stations is only an administratively linked square-day environmental proxy; not measured alternative flowers at focal FIT or an individual decision",
        "baseline_on_matched_sample":None,
        "model_with_pan_richness":None,
        "model_wind_by_pan_richness":None
    }
    if support["model_gate"]=="PASS_CONTEXTUAL_OVERLAP":
        result["baseline_on_matched_sample"]=augmented_pair(data,"one_km")
        result["model_with_pan_richness"]=_fit_one(data,"richness_main")
        result["model_wind_by_pan_richness"]=_fit_one(data,"wind_by_richness")
    else:
        result["status"]="NO_GO_SUPPORT_BEFORE_CONTEXTUAL_MODELS"
    root.mkdir(parents=True,exist_ok=True)
    (root/"pan_richness_contextual_models.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    print("POMS_PAN_CONTEXTUAL_MODEL "+json.dumps(result,ensure_ascii=False,allow_nan=False),flush=True)
    print("POMS_PAN_CONTEXTUAL_MODEL_COMPLETE",flush=True)
    return result

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="poms_pan_joint_output")
    a=p.parse_args(argv)
    analyze(Path(a.out))

if __name__=="__main__":
    main()
