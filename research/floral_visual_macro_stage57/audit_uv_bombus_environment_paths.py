"""Stage57 environmental confounding gate: original measured UV + modelled bee guild.

This is NOT a causal SEM: contemporary bounded GBIF occurrence indexed-page
pollinator predictions cannot identify historical selection on UV signal.
Two-equation observational dependence audit only:
 (1) source modelled Bombus/all-bee fraction ~ author species mean UVB+T+P;
 (2) binary original measured UV spatial pattern ~ source environment (+ genus)
     (+ current source-modelled Bombus/all-bee fraction).

No indirect causal effect, p-value inference, phenotyped site assignment, UV
pollinator cognition, actual bee visits, or pollen/seed fitness is estimated.
Source input groups:
 - stage52 159 original Koski & Ashman 2016 accepted species climate
 - stage55 exactly the same 159 source acceptance keys + bounded bee HEX
Both inputs required with taxon unique and UV-label audit. Enforce coverage
precommitted Stage55 (>=5 quality points and >=2 eligible original HEX).
"""
from __future__ import annotations

import argparse,csv,json,math,statistics
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

N_SOURCE=159
N_SOURCE_CLASS={"0":81,"1":78}
MIN_RECORDS=5
MIN_CELLS=2
E_ENV=("published_uvb_mean","published_annual_temp_mean","published_precip_mean")
E_ALT=("published_latitude_mean","published_annual_temp_mean","published_precip_mean")
TARGET="modelled_Bombus_share_ratio_of_means_or_unknown"

def load_verified_inputs(src,exposure):
    original=pd.read_csv(src,dtype={"gbif_accepted_species_key":"string"})
    occupied=pd.read_csv(exposure,dtype={"gbif_accepted_species_key":"string"})
    if len(original)!=N_SOURCE or len(occupied)!=N_SOURCE:
        raise ValueError("NO_GO_ORIGINAL_SOURCE_159_2016_UV_TAXA_FRAME")
    key="gbif_accepted_species_key"
    if original[key].isna().any() or occupied[key].isna().any() or (
      original[key].duplicated().any() or occupied[key].duplicated().any()
    ):
        raise ValueError("NO_GO_NONUNIQUE_2016_ACCEPTED_SPECIES_KEY")
    if set(original[key])!=set(occupied[key]):
        raise ValueError("NO_GO_ORIGINAL_UV_EXPOSURE_NOT_SAME_159_ACCEPTED_KEYS")
    ct=Counter(original["source_2016_UV_pattern"].astype(str))
    if ct!=Counter(N_SOURCE_CLASS):
        raise ValueError("NO_GO_SOURCE_DIRECT_UV_POSITIVE_NEGATIVE_DENOMINATOR")
    if not occupied["GBIF_sample_not_native_range"].eq(True).all():
        raise ValueError("NO_GO_SOURCE_GBIF_RECORD_NATIVE_PROVENANCE_LOST")
    d=original.merge(occupied,on=key,validate="one_to_one")
    if d.empty or not d["original_2016_source_genus_or_unknown"].notna().all():
        raise ValueError("NO_GO_ORIGINAL_STUDY_GENUS_MISSING")
    for name in (*E_ENV,"published_altitude_mean","published_latitude_mean"):
        if not np.isfinite(pd.to_numeric(d[name],errors="coerce")).all():
            raise ValueError("NO_GO_SOURCE_AUTHOR_CLIMATE_MISSING_OR_NONFINITE_"+name)
    for name in ("source_qualified_records","source_eligible_bee_hex_cells"):
        if not np.isfinite(pd.to_numeric(d[name],errors="coerce")).all():
            raise ValueError("NO_GO_SOURCE_GBIF_COVERAGE_INVALID")
    d=d[(d["source_qualified_records"]>=MIN_RECORDS)&
        (d["source_eligible_bee_hex_cells"]>=MIN_CELLS)].copy()
    if d.empty:raise ValueError("NO_GO_NO_QUALIFIED_BEE_GUILD_COVERAGE")
    cols=[TARGET,"modelled_Bombus_names_mean","modelled_all_bee_names_mean"]
    if not all(np.isfinite(pd.to_numeric(d[c],errors="coerce")).all() for c in cols):
        raise ValueError("NO_GO_SOURCE_BEE_RICHNESS_UNKNOWN_NOT_ZERO")
    if (d["modelled_all_bee_names_mean"]<=0).any() or (
      d["modelled_Bombus_names_mean"]>d["modelled_all_bee_names_mean"]
    ).any():
        raise ValueError("NO_GO_MODELLED_GUILD_FRACTION_DENOMINATOR_BAD")
    expected=d["modelled_Bombus_names_mean"]/d["modelled_all_bee_names_mean"]
    if not np.allclose(expected,d[TARGET],rtol=0,atol=1e-10):
        raise ValueError("NO_GO_BOMBUS_GUILD_FRACTION_SOURCE_RECOMPUTE_MISMATCH")
    d["measured_UV_spatial_pattern"]=d["source_2016_UV_pattern"].astype(int)
    d["original_author_genus"]=d["original_2016_source_genus_or_unknown"]
    return d

def zscore(data,fields):
    r=pd.DataFrame(index=data.index)
    for col in fields:
        x=data[col].astype(float)
        sd=x.std(ddof=0)
        if not np.isfinite(sd) or sd<=0:
            raise ValueError("NO_GO_ZERO_SOURCE_ENVIRONMENT_VARIANCE_"+col)
        r[col+"_z"]=(x-x.mean())/sd
    return r

def fit_binomial(y,X):
    x=sm.add_constant(X.astype(float),has_constant="add")
    fit=sm.GLM(y.astype(float),x,family=sm.families.Binomial()).fit()
    values=fit.params.replace([np.inf,-np.inf],np.nan)
    if not np.isfinite(values).all() or not np.isfinite(fit.aic):
        raise ValueError("NO_GO_UNSTABLE_OR_SEPARATED_GLM")
    # Under mixed small genera, complete/semi separation can yield finite
    # numerical AIC while intercept/dummy standard errors explode (~13000).
    # Such AIC must NOT be interpreted as a reliable genus-adjusted test.
    if float(fit.bse.abs().max())>50 or float(fit.params.abs().max())>15:
        return {"status":"QUASI_SEPARATION_DO_NOT_COMPARE_AIC",
                "AIC":None,
                "largest_coefficient_standard_error":float(fit.bse.abs().max()),
                "n_coefficients":int(len(fit.params)),
                "no_genus_adjusted_effect_or_AIC_claim":True}
    return {"status":"ESTIMABLE_EXPLORATORY_ASSOCIATION_NOT_CAUSAL",
            "AIC":float(fit.aic),"deviance":float(fit.deviance),
            "coefficients":{k:float(v) for k,v in fit.params.items()},
            "coefficient_standard_errors":{k:float(v) for k,v in fit.bse.items()},
            "no_significance_or_causal_indirect_effect_claimed":True}

def report(eligible):
    n=len(eligible)
    genus=eligible["original_author_genus"]
    outcome=eligible["measured_UV_spatial_pattern"]
    columns=(*E_ENV,"published_latitude_mean","published_altitude_mean",TARGET)
    z=zscore(eligible,columns)
    env=[c+"_z" for c in E_ENV]
    other=[c+"_z" for c in E_ALT]
    poll=TARGET+"_z"
    # A source-genus with fewer than 3 source-covered plants is pooled into
    # 'Other' for nuisance adjustment, NOT phylogenetic ancestry modelling.
    group=genus.where(genus.map(genus.value_counts())>=3,"Other")
    genus_dummies=pd.get_dummies(group,prefix="genus",drop_first=True,dtype=float)
    reg={}
    for name,X in (
        ("pollinator_only",z[[poll]]),
        ("environment_only",z[env]),
        ("environment_plus_pollinator",z[env+[poll]]),
        ("environment_plus_grouped_genus",z[env].join(genus_dummies)),
        ("environment_plus_grouped_genus_plus_pollinator",
          z[env+[poll]].join(genus_dummies)),
        ("latitude_for_UVB_environment_only",z[other]),
        ("latitude_for_UVB_environment_plus_pollinator",z[other+[poll]]),
    ):
        reg[name]=fit_binomial(outcome,X)
    linear=sm.OLS(z[poll],sm.add_constant(z[env],has_constant="add")).fit()
    # Source-based descriptives, no p values and no pseudo-'indirect effects'.
    x=z[env].values
    pairwise=np.corrcoef(z[["published_uvb_mean_z",
                           "published_latitude_mean_z"]].to_numpy().T)[0,1]
    # Climate + predicted guild share are not replicated measured at same sites.
    quality={
      "n_source_species":N_SOURCE,
      "n_qualified_species_5points_2hex":n,
      "measured_original_UV_pattern_0_1":dict(sorted(
          (str(k),int(v)) for k,v in Counter(outcome).items())),
      "qualified_original_study_genera":{str(k):int(v) for k,v in genus.value_counts().items()},
      "n_genus_original_source":genus.nunique(),
      "original_genus_by_UV_state":{
        str(k):{"n":int(len(s)),"patterned":int(sum(s==1)),"uniform":int(sum(s==0))}
        for k,s in eligible.groupby("original_author_genus")["measured_UV_spatial_pattern"]},
      "genus_fixed_effect_complete_separation_is_a_numerical_hard_stop":True,
      "fraction_source_taxa_qualified":n/N_SOURCE,
      "author_UVB_vs_author_mean_latitude_correlation":float(pairwise),
      "modelled_Bombus_fraction_environment_R2":float(linear.rsquared),
      "modelled_Bombus_fraction_environment_standardized_coefficients":{
         k:float(v) for k,v in linear.params.items()},
      "environment_climate_fields":list(E_ENV),
      "original_UV_pattern_source":"Koski & Ashman 2016 original accepted source UV binary; 1=patterned, 0=uniform",
      "separate_time_grain_prevents_evolutionary_causal_path":True,
      "no_genus_random_effect_stable_with_eight_skewed_genera":True,
      "not_a_plant_phenotyped_native_point_model":True,
      "source_modelled_2026_Bombus_fraction_not_pollinator_abundance_or_visits":True,
      "no_p_values_or_indirect_causal_effects":True,
    }
    return {"status":"SOURCE_AUTHENTIC_2016_UV_159_ENVIRONMENT_BOMBUS_DUAL_EQUATION_CONFOUND_AUDIT",
            "source_coverage":quality,
            "observational_UV_binary_regressions":reg,
            "model_comparison_AIC_improvement_positive_is_better":{
              "add_pollinator_to_environment":
                reg["environment_only"]["AIC"]-reg["environment_plus_pollinator"]["AIC"],
              "add_pollinator_to_environment_plus_grouped_genus":(
                reg["environment_plus_grouped_genus"]["AIC"]
                -reg["environment_plus_grouped_genus_plus_pollinator"]["AIC"]
                if reg["environment_plus_grouped_genus"]["AIC"] is not None
                and reg["environment_plus_grouped_genus_plus_pollinator"]["AIC"] is not None
                else None),
            },
            "model_is_not_causal_SEM_or_an_indirect_effect":True,
            "need_sample_site_coincident_phenotype_native_pollinators_and_phylogeny":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-2016-climate",required=True)
    p.add_argument("--source-159-bee-coverage",required=True)
    args=p.parse_args()
    rows=load_verified_inputs(args.original_2016_climate,args.source_159_bee_coverage)
    receipt=report(rows)
    out=Path("stage57_source_uv_bee_environment_confounds")
    out.mkdir(exist_ok=True)
    (out/"source_original_159_environment_pollinator_two_equation_noncausal_audit.json").write_text(
       json.dumps(receipt,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+"\n",
       encoding="utf8")
    print("STAGE57_SOURCE_ORIGINAL_159_UV_E_B_NONCAUSAL_AUDIT",
          json.dumps(receipt,sort_keys=True,ensure_ascii=False,allow_nan=False))
    print("NO_HISTORICAL_BOMBUS_SELECTION_OR_LOCAL_POLLINATOR_PATH_IDENTIFIED")

if __name__=="__main__":
    main()
