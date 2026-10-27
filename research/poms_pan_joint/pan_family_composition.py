"""Stage 3g original Pan flowering family-composition control for FIT wind-guild odds.

The surrounding Pan station plant assemblage is a measured *site-day context*,
NOT an FIT bee's feasible or perceived resource choice set. Outcome is the
same grouped bumblebee vs other-fly conditional visit count as Stage 3f.
"""
from __future__ import annotations
import argparse, hashlib, json, warnings, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm

from site_date_join import (
    safe_source_csv, build_pan_environment, taxon_id, PAN_PARTS, FIT_MEMBER, FIT_HASH, KEYS
)
from pan_richness_model import prepare_matched_context, _fit_one, stage3d_formula

NA_FAMILY = "__SOURCE_UNKNOWN_FAMILY__"
REJECT_NAMES = {"", "nan", "<na>", "none", "null", "unknown", "not recorded", "n/a", "na"}
N_FAMILIES = 3
FEATURES = ("pan_family1_fraction", "pan_family2_fraction", "pan_family3_fraction")


def _normalized_family(series):
    raw=series.astype("string").str.strip()
    norm=raw.str.casefold()
    norm=norm.mask(norm.isna() | norm.isin(REJECT_NAMES), NA_FAMILY)
    return norm.astype(str)


def build_pan_family_context(samples:pd.DataFrame, flowers:pd.DataFrame):
    """Choose 3 source-frequency families, never consulting FIT insect counts.

    Source foreign-key reconciliation, 5-station site-days, and distinct Pan
    flowering taxon identity preserve the source hierarchy and observation
    grain. Missing family remains a declared category in the denominator.
    """
    pan_daily,pan_source,stations=build_pan_environment(samples,flowers)
    if "family" not in flowers:
        raise ValueError("source Pan flowering 'family' field absent")
    f=flowers.copy()
    f["sample_id"]=f.sample_id.astype("string").str.strip()
    original=len(f)
    f=f.loc[f.sample_id.isin(stations.sample_id)].copy()
    f["source_taxon_id"]=[taxon_id(row)[0] for _,row in f.iterrows()]
    if f.source_taxon_id.isna().any():
        raise ValueError("unlabeled source flower taxon, cannot assign family")
    f["native_family"]= _normalized_family(f.family)
    f=f[["sample_id","source_taxon_id","native_family"]].merge(
        stations[["sample_id",*KEYS]],on="sample_id",how="left",validate="many_to_one")
    if f[KEYS].isna().any().any():
        raise ValueError("taxon occurrence gained missing Pan site/date")
    # Within one site-day and source taxon identity, distinct known family
    # labels must agree. Explicitly do NOT convert an unknown to a new taxon.
    taxoncols=[*KEYS,"source_taxon_id"]
    known=f[f.native_family.ne(NA_FAMILY)]
    known_card=known.groupby("source_taxon_id",observed=True).native_family.nunique()
    bad=known_card[known_card>1]
    if len(bad):
        raise ValueError(f"source Pan taxa map to conflicting known families: {len(bad)}")
    known_mapping=known.drop_duplicates(taxoncols)[taxoncols+["native_family"]].rename(
        columns={"native_family":"known_family"})
    taxa=f[taxoncols].drop_duplicates().merge(
        known_mapping,on=taxoncols,how="left",validate="one_to_one")
    taxa["family"]=taxa.known_family.fillna(NA_FAMILY).astype(str)
    pan_valid=pan_daily.loc[
        pan_daily.stations.eq(5) &
        pan_daily.station_types.eq(5) &
        pan_daily.pan_recorded_flowering_taxa.notna(),KEYS+["stations","station_types",
            "pan_recorded_flowering_taxa"]].copy()
    taxa=taxa.merge(pan_valid[KEYS],on=KEYS,how="inner",validate="many_to_one")
    if taxa.empty:
        raise ValueError("no 5-station Pan site-days with original flower taxon identities")
    daily_sizes=taxa.groupby(KEYS,observed=True).source_taxon_id.nunique().rename("taxon_count")
    # A station found with repeated occurrences of the same taxon must be
    # counted only once for richness and family composition.
    by_family=taxa.groupby([*KEYS,"family"],observed=True).size().rename("taxa").reset_index()
    frequency=by_family.groupby("family",observed=True).agg(
        unique_site_days=("date","size"),
        across_site_day_taxa=("taxa","sum")
    ).reset_index().sort_values(
        ["unique_site_days","family"],ascending=[False,True],kind="mergesort")
    eligible_top=frequency.loc[frequency.family.ne(NA_FAMILY)].head(N_FAMILIES)
    if len(eligible_top)!=N_FAMILIES:
        raise ValueError("fewer than three source-known Pan flowering plant families")
    selected=eligible_top.family.tolist()
    # Source-only source audit: the list below is fixed before FIT responses.
    day_family=by_family.pivot_table(
        index=KEYS,columns="family",values="taxa",
        aggfunc="sum",fill_value=0,observed=True)
    for col in selected:
        if col not in day_family:raise ValueError("family missing from source pivot")
    day_family=day_family[selected].reset_index()
    day_family.columns=[*KEYS,*FEATURES]
    day_family=day_family.merge(
        daily_sizes.reset_index(),on=KEYS,validate="one_to_one")
    reconcile=day_family.merge(
        pan_valid[KEYS+["pan_recorded_flowering_taxa"]],
        on=KEYS,validate="one_to_one")
    if not np.array_equal(reconcile.taxon_count.to_numpy(dtype=int),
                          reconcile.pan_recorded_flowering_taxa.to_numpy(dtype=int)):
        raise ValueError("Pan distinct flowering taxa differ from Stage3f provenance")
    for field in FEATURES:
        day_family[field]=day_family[field].astype(float)/day_family.taxon_count
    if (day_family[list(FEATURES)].lt(0)|day_family[list(FEATURES)].gt(1)).any().any():
        raise ValueError("Pan family fractions not in [0,1]")
    if (day_family[list(FEATURES)].sum(axis=1)>1.0+1e-12).any():
        raise ValueError("family fractions greater than 1: source identity inflation")
    pan_full=pan_daily.merge(day_family[KEYS+list(FEATURES)],on=KEYS,
                             how="left",validate="one_to_one")
    full_checks=pan_valid[KEYS].merge(day_family[KEYS],on=KEYS,
                                     how="left",indicator=True,validate="one_to_one")
    if not full_checks["_merge"].eq("both").all():
        raise ValueError("Pan 5-station flower site-day lost in family mapping")
    family_source=[]
    for name,_,count in zip(selected,FEATURES,eligible_top.unique_site_days.tolist()):
        group=taxa.loc[taxa.family.eq(name)]
        family_source.append({
            "name":name,
            "unique_original_pan_site_days":int(count),
            "unique_pan_sites":int(group.location_code.nunique()),
            "source_taxon_labels":int(group.source_taxon_id.nunique())})
    meta={
        "source_pan_station_and_flower_foreign_key_receipt":pan_source,
        "original_pan_flower_occurrence_rows":original,
        "source_orphan_flower_occurrences_quarantined":int(pan_source["orphan_flower_occurrence_rows"]),
        "five_station_site_days_with_named_taxa":len(pan_valid),
        "taxon_families_in_source":int(frequency.family.nunique()),
        "unknown_family_site_day_taxa":int(taxa.family.eq(NA_FAMILY).sum()),
        "unknown_family_site_days":int(taxa.loc[taxa.family.eq(NA_FAMILY),KEYS].drop_duplicates().shape[0]),
        "families_selected_source_only":family_source,
        "top_source_family_site_day_coverage":[
            {"family":str(r.family),"unique_pan_days":int(r.unique_site_days)}
            for r in frequency.head(12).itertuples(index=False)],
        "features":list(FEATURES),
        "family_selection_rule":"top three known original family labels by distinct five-station Pan site-day coverage, lexicographic tie, independent of FIT outcomes",
        "family_fraction_rule":"distinct original Pan taxon version identities in that family / distinct identities from ALL families including unknown, not flowers or visits",
        "pan_flower_unit_counts_not_aggregated":True,
    }
    return pan_full,meta


def make_matched_family_data(fit:pd.DataFrame,pan_full:pd.DataFrame,metadata,
                             expected_stage3f=(2210,95)):
    d,support=prepare_matched_context(fit,pan_full)
    support["families_selected_source_only"]=metadata["families_selected_source_only"]
    support["matched_family_missing_columns"]={
        c:int(d[c].isna().sum()) for c in FEATURES}
    if any(support["matched_family_missing_columns"].values()):
        support["family_composition_gate"]="NO_GO_MISSING_PAN_FAMILY_COMPOSITION"
        return d,support
    fail=[]
    site_n=d.location_code.nunique()
    if expected_stage3f is not None and (len(d),site_n)!=tuple(expected_stage3f):
        # Stage 3f source set is frozen. Changing FIT coverage is a real
        # data-lineage regression, not a license to fit another population.
        fail.append(f"Stage3f count/site reconciliation changed: n={len(d)}, sites={site_n}")
    for k,info in enumerate(metadata["families_selected_source_only"]):
        c=FEATURES[k]
        if info["unique_original_pan_site_days"]<50:fail.append(f"{c} <50 source days")
        if info["unique_pan_sites"]<10:fail.append(f"{c} <10 source sites")
        varying=int((d.groupby("location_code",observed=True)[c].nunique()>1).sum())
        support.setdefault("families_within_site_fraction_variation",{})[c]=varying
        support.setdefault("family_fraction_summary",{})[c]={
            "selected_original_family":info["name"],
            "min":float(d[c].min()),"q25":float(d[c].quantile(.25)),
            "median":float(d[c].median()),"q75":float(d[c].quantile(.75)),
            "max":float(d[c].max()),
            "fraction_of_pair_surveys_with_family_present":float(d[c].gt(0).mean())}
        if varying<10:fail.append(f"{c} varies at <10 FIT sites")
    support["family_composition_gate"]="PASS" if not fail else "NO_GO"
    support["family_composition_gate_failures"]=fail
    return d,support


def fit_family_control(d:pd.DataFrame):
    """Site-clustered grouped binomial model, same source sample as Stage 3f."""
    rhs=stage3d_formula("one_km")+" + pan_rich_center + "+" + "+".join(FEATURES)
    result={"status":"not_run","n":len(d),"sites":int(d.location_code.nunique()),
            "rhs":rhs,"covariance":"cluster site location_code",
            "outcome":"paired bumblebee, other_flies recorded visits, conditional >=1"}
    try:
        X=patsy.dmatrix(rhs,d,return_type="dataframe")
        if len(X)!=len(d):raise ValueError("design drops source matched FIT surveys")
        rank=int(np.linalg.matrix_rank(X.to_numpy()))
        result["design_columns"]=len(X.columns)
        result["design_rank"]=rank
        if rank!=len(X.columns):
            result["status"]="NO_GO_RANK_DEFICIENT";return result
        y=np.column_stack([d.bumblebees.astype(int).to_numpy(),
                           d.other_flies.astype(int).to_numpy()])
        with warnings.catch_warnings(record=True) as cautions:
            warnings.simplefilter("always")
            fit=sm.GLM(y,X,family=sm.families.Binomial()).fit(
                maxiter=180,cov_type="cluster",
                cov_kwds={"groups":d.location_code.astype(str).to_numpy()})
        result["warnings"]=[str(c.message) for c in cautions][-10:]
        result["converged"]=bool(fit.converged)
        result["pearson_dispersion_over_df"]=float(fit.pearson_chi2/fit.df_resid)
        if not fit.converged:
            result["status"]="NO_GO_NOT_CONVERGED";return result
        windstrong=[n for n in fit.params.index if n.startswith("C(wind_speed") and
                    "Leaves moving strongly" in n]
        if len(windstrong)!=1:
            result["status"]="NO_GO_STRONG_WIND_TERM";return result
        target=windstrong[0]
        req=[target,"pan_rich_center",*FEATURES]
        cov=fit.cov_params().loc[req,req].to_numpy()
        ci=fit.conf_int().loc[req].to_numpy()
        result["all_nuisance_nonfinite_ci_cells"]=int(
            (~np.isfinite(fit.conf_int().to_numpy())).sum()-
            (~np.isfinite(ci)).sum())
        if not np.isfinite(cov).all() or not np.isfinite(ci).all() or np.max(np.abs(ci))>100:
            result["status"]="NO_GO_NONFINITE_STUDY_CONTRAST";return result
        beta=fit.params[target]
        se=np.sqrt(fit.cov_params().loc[target,target])
        result["strong_wind_OR"]={
            "OR":float(np.exp(beta)),
            "ci95_low":float(np.exp(beta-1.95996398454*se)),
            "ci95_high":float(np.exp(beta+1.95996398454*se)),
            "p":float(fit.pvalues[target])}
        mat=np.zeros((len(FEATURES),len(fit.params)))
        for i,feature in enumerate(FEATURES):
            mat[i,fit.params.index.get_loc(feature)]=1
        wald=fit.wald_test(mat,scalar=True)
        result["family_composition_joint_wald"]={
            "df":3,"chi2":float(wald.statistic),"p":float(wald.pvalue)}
        result["family_fraction_contrasts"]={}
        for feature in FEATURES:
            b=fit.params[feature]
            s=np.sqrt(fit.cov_params().loc[feature,feature])
            result["family_fraction_contrasts"][feature]={
                "OR_per_0p25_fraction":float(np.exp(.25*b)),
                "CI95_low":float(np.exp(.25*(b-1.95996398454*s))),
                "CI95_high":float(np.exp(.25*(b+1.95996398454*s))),
                "cluster_p_unadjusted_exploratory":float(fit.pvalues[feature])}
        result["status"]="FITTED"
    except Exception as e:
        result["status"]="MODEL_FAILED"
        result["error"]=str(e)
    return result


def analyze(root:Path):
    with zipfile.ZipFile(root/"pan_original_provider.zip") as z:
        samples,_,sha_samples=safe_source_csv(z,*PAN_PARTS["samples"])
        flowers,_,sha_flower=safe_source_csv(z,*PAN_PARTS["flowers"])
    with zipfile.ZipFile(root/"fit_original_provider.zip") as z:
        fit,_,sha_fit=safe_source_csv(z,FIT_MEMBER,FIT_HASH)
    pan,source=build_pan_family_context(samples,flowers)
    data,support=make_matched_family_data(fit,pan,source)
    result={"status":"exploratory_posthoc_same_PoMS_programme",
            "member_sha256":{
                "Pan_station":sha_samples,"Pan_flower":sha_flower,"FIT_1km":sha_fit},
            "Pan_flower_family_source_audit":source,
            "exact_join_support":support,
            "baseline_with_richness":None,"model_with_source_selected_families":None,
            "no_causal_flower_resource_availability_or_wind_choice_inference":True}
    if support["family_composition_gate"]=="PASS":
        result["baseline_with_richness"]=_fit_one(data,"richness_main")
        result["model_with_source_selected_families"]=fit_family_control(data)
    else:
        result["status"]="NO_GO_FAMILY_ADMISSION"
    root.mkdir(parents=True,exist_ok=True)
    (root/"pan_family_composition_model.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("POMS_PAN_FAMILY_RESULT "+json.dumps(result,ensure_ascii=False,allow_nan=False),flush=True)
    print("POMS_PAN_FAMILY_MODEL_COMPLETE",flush=True)
    return result


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="poms_pan_joint_output")
    a=p.parse_args(argv)
    analyze(Path(a.out))


if __name__=="__main__":
    main()
