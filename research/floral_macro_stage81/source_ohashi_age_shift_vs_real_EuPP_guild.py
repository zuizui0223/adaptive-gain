"""Stage81C: authentic 28-source-age-spectral traits x corrected EuPP visited bees.

FIRST ORDER network-conditional null-score screen ONLY. This is not a fitted
binomial model, bee perceptual model, causal selection, actual wind interaction,
flower age observed by visitors, or phylogenetically independent result.

Original source ages: Ohashi et al. 2015 spectra measured in Japan.
Original visitor guilds: EuPPollNet 2025, observed in Europe. Country/site/age
and plant individual are NOT paired. Study_id 23/24/25 are same original
publication as the publisher explicitly states.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,math
from pathlib import Path
import numpy as np
import pandas as pd

SOURCE_ORIGINAL_EUPP_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
SOURCE_OHASHI_DERIVED_28_SHA="bb8c7d497bf2e0fcea267aa88c685fdd87f475fd25b9d062b2011556819aa804"
ORIGINAL_EUPP_N=18798
ORIGINAL_SPECIES=28
N_PERMUTATION_PARTS=53
EXPECTED_PRECOHORT=537
EXPECTED_SOURCE_STRICT_INFORMATION=194

def publication(study):
    if str(study).split("_",1)[0] in {"23","24","25"}:
        return "23_24_25_ONE_PUBLISHED_STUDY"
    return str(study)

def validated_source_csv(path,sha):
    b=Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=sha:
        raise ValueError("STAGE81C_REPRODUCIBLE_SOURCE_SHA_CHANGED")
    return pd.read_csv(path,keep_default_na=False)

def bh_fdr(pvalues):
    p=np.asarray(pvalues,dtype=float)
    if len(p)==0 or np.any(p<0) or np.any(p>1) or not np.isfinite(p).all():
        raise ValueError("INVALID_SOURCE_PERMUTATION_P_VALUES")
    perm=np.argsort(p,kind="stable")
    q=(p[perm]*len(p))/(np.arange(len(p))+1)
    q=np.minimum.accumulate(q[::-1])[::-1]
    output=np.empty_like(q)
    output[perm]=np.minimum(q,1.)
    return output

def build_taxon_traits(ages):
    ages=ages.copy()
    if ages.source_original_accepted_species.nunique()!=ORIGINAL_SPECIES or len(ages)!=N_PERMUTATION_PARTS:
        raise ValueError("STAGE81C_ORIGINAL_28_SPECIES_53_FLORAL_PARTS_CHANGED")
    for t in ("source_early_samples","source_late_samples"):
        if not (pd.to_numeric(ages[t])==10).all():
            raise ValueError("STAGE81C_TRUE_10_EARLY_LATE_MEASUREMENTS_MISSING")
    ages["q_raw_spectral_part_BH_53"]=bh_fdr(ages["raw_spectrum_permutation_p_999_not_bee_colour"])
    trait=ages.groupby("source_original_accepted_species",sort=True).agg(
       source_original_age_parts=("original_flower_part_literal","nunique"),
       raw_source_median_age_RMS_percent_points=("raw_reflectance_early_late_RMS_percent_points","median"),
       source_min_part_q_raw_spectral=("q_raw_spectral_part_BH_53","min"),
    ).reset_index()
    log=np.log1p(trait["raw_source_median_age_RMS_percent_points"].to_numpy())
    std=float(log.std(ddof=1))
    if std<=0:raise ValueError("SOURCE_28_TRUE_AGE_TRAITS_HAVE_NO_VARIATION")
    trait["x_28species_equal_taxon_standardized_log1p_raw_age_RMS"]=(log-log.mean())/std
    return trait,ages

def source_network_preguild(flora,trait):
    xs={r.source_original_accepted_species:float(r.x_28species_equal_taxon_standardized_log1p_raw_age_RMS)
        for r in trait.itertuples()}
    key=("Study_id","Network_id","Year_from_original_date")
    f=flora[flora["Original_plant_accepted_name_literal"].isin(xs)].copy()
    if len(flora)!=ORIGINAL_EUPP_N or len(f)!=1921:
        raise ValueError("STAGE81C_SOURCE_PLANT_NETWORK_ROW_GRAIN_CHANGED")
    if f.duplicated(list(key)+["Original_plant_accepted_name_literal"]).any():
        raise ValueError("STAGE81C_DUPLICATE_SOURCE_PLANT_NETWORK")
    if f.groupby(list(key)).ngroups!=1040:
        raise ValueError("STAGE81C_SOURCE_28_SPECIES_NETWORK_COUNT_CHANGED")
    f["source_age_trait_std"]=f["Original_plant_accepted_name_literal"].map(xs)
    f["genus"]=f["Original_plant_accepted_name_literal"].str.split().str[0]
    for col in ("n_observed_Bombus","n_observed_other_bee"):
        f[col]=pd.to_numeric(f[col],errors="raise")
        if (f[col]<0).any():raise ValueError("STAGE81C_INVALID_RECORDED_BEE_COUNTS")
    g=f.groupby(list(key),sort=True)
    eligible=g.filter(lambda y:y.Original_plant_accepted_name_literal.nunique()>=2)
    if eligible.groupby(list(key)).ngroups!=EXPECTED_PRECOHORT:
        raise ValueError("STAGE81C_SOURCE_COHORT_NOT_DEFINED_BEFORE_VISITOR_OUTCOMES")
    return f,eligible

def one_network_score(group):
    if len(group)<2 or group.Original_plant_accepted_name_literal.nunique()<2:
        return None
    b=group.n_observed_Bombus.to_numpy(dtype=float)
    o=group.n_observed_other_bee.to_numpy(dtype=float)
    n=b+o
    if int(np.sum(n>0))<2 or sum(b)==0 or sum(o)==0:return None
    p=float(sum(b)/sum(n))
    x=group.source_age_trait_std.to_numpy(dtype=float)
    centered=x-float(np.sum(n*x)/sum(n))
    u=float(np.sum((b-n*p)*centered))
    information=float(p*(1-p)*np.sum(n*centered*centered))
    if not np.isfinite(information) or information<=1e-8:return None
    return {
      "Study_id":str(group.Study_id.iloc[0]),
      "source_publication":publication(group.Study_id.iloc[0]),
      "Network_id":str(group.Network_id.iloc[0]),
      "Year_from_original_date":str(group.Year_from_original_date.iloc[0]),
      "n_original_distinct_measured_source_species":int(group.Original_plant_accepted_name_literal.nunique()),
      "n_original_distinct_measured_source_genera":int(group.genus.nunique()),
      "source_strict_observed_Bombus":int(sum(b)),
      "source_strict_observed_other_bee":int(sum(o)),
      "source_original_bee_species_with_events":int(np.sum(n>0)),
      "source_U_local_score":u,
      "source_I_local_null_fisher_information":information,
      "source_null_ratio_U_over_I_not_fitted_beta":u/information,
    }

def informative_scores(eligible):
    rows=[]
    for _,g in eligible.groupby(["Study_id","Network_id","Year_from_original_date"],sort=True):
        val=one_network_score(g)
        if val:rows.append(val)
    return pd.DataFrame(rows)

def group_ratio(scores):
    return float(scores.source_U_local_score.sum()/scores.source_I_local_null_fisher_information.sum())

def publication_bootstrap(scores,reps=4000,seed=20261118):
    pubs=scores.groupby("source_publication",sort=True)[["source_U_local_score",
      "source_I_local_null_fisher_information"]].sum().to_numpy(dtype=float)
    if len(pubs)<10:raise ValueError("STAGE81C_NOT_ENOUGH_PUBLICATION_CLUSTERS")
    n=len(pubs)
    rng=np.random.default_rng(seed)
    idx=rng.integers(0,n,(reps,n))
    b=pubs[idx]
    q=b[:,:,0].sum(axis=1)/b[:,:,1].sum(axis=1)
    return {"source_publications":n,
      "original_publication_bootstrap_replicates":reps,
      "descriptive_publication_bootstrap_95_interval_NOT_causal":[float(x) for x in np.quantile(q,[.025,.975])],
      "source_fraction_bootstraps_negative":float(np.mean(q<0)),
      "does_not_represent_taxon_or_individual_independence":True}

def analyze(flora,ages):
    trait,part=build_taxon_traits(ages)
    matched,eligible=source_network_preguild(flora,trait)
    scores=informative_scores(eligible)
    if len(scores)!=EXPECTED_SOURCE_STRICT_INFORMATION or scores.Study_id.nunique()!=31 or scores.source_publication.nunique()!=30:
        raise ValueError("STAGE81C_TRUE_SOURCE_GUILD_NETWORK_SUPPORT_CHANGED")
    bypub=scores.groupby("source_publication")["source_I_local_null_fisher_information"].sum()
    weight=bypub/bypub.sum()
    genus_presence=(eligible.groupby(["Study_id","Network_id","Year_from_original_date"])["genus"].nunique())
    out={
      "schema":"stage81c_original_28_age_source_mean_spectra_vs_2019_2025_EuPP_real_guild_nullscore",
      "original_source_flora_all_source_plant_network_year_rows":len(flora),
      "original_source_species_measured_early_late":28,
      "original_source_species_part_measurements":len(part),
      "original_raw_spectral_part_BH_q_lt_0_05":int((part.q_raw_spectral_part_BH_53<.05).sum()),
      "original_raw_spectral_species_with_any_part_BH_q_lt_0_05":int(part.loc[part.q_raw_spectral_part_BH_53<.05,
          "source_original_accepted_species"].nunique()),
      "original_source_pre_bee_trait_plant_network_rows":len(matched),
      "original_source_pre_bee_trait_networks_one_28_species":matched.groupby(["Study_id","Network_id","Year_from_original_date"]).ngroups,
      "original_source_outcome_blind_2_species_networks":eligible.groupby(["Study_id","Network_id","Year_from_original_date"]).ngroups,
      "original_source_outcome_blind_2_species_networks_2_genera":int((genus_presence>=2).sum()),
      "original_source_true_two_strict_bee_guild_informative_networks":len(scores),
      "original_source_informative_unique_study_ID":int(scores.Study_id.nunique()),
      "original_source_informative_distinct_publications":int(scores.source_publication.nunique()),
      "source_networks_with_at_least_2_distinct_measured_genera":int((scores.n_original_distinct_measured_source_genera>=2).sum()),
      "source_networks_with_at_least_3_distinct_measured_genera":int((scores.n_original_distinct_measured_source_genera>=3).sum()),
      "original_null_score_ratio_per_taxon_equal_standardized_log1p_raw_age_RMS_not_fitted_beta":group_ratio(scores),
      "original_study_info_largest_fraction":float(weight.max()),
      "original_study_info_effective_number":float(1/(weight*weight).sum()),
      "source_guild_original_publication_bootstrap":publication_bootstrap(scores),
      "source_same_genus_Trifolium_is_one_evolutionary_comparison_NOT_118_independent_origins":True,
      "source_Apis_photoreceptor_0_09_colour_discrimination_NOT_MEASURED_HERE":True,
      "source_flower_visitor_source_Europe_vs_spectral_source_Japan_not_same_site_or_plant_individual":True,
      "source_phenology_flower_counts_clade_environment_and_survey_effort_not_yet_adjusted":True,
      "source_not_behavioral_early_visual_route_or_wind_scent_plume_landing_test":True,
      "source_not_new_positive_claim_due_to_taxon_and_study_dominance":True,
    }
    # Study/guild and genus leave-out are sensitivity analyses, not a search for sign.
    out["source_leave_one_genus_recomputed"]=[]
    source_most_used=matched.genus.value_counts().index.tolist()
    for genus in source_most_used:
        sub=matched.loc[matched.genus!=genus].copy()
        parts=[]
        for _,g in sub.groupby(["Study_id","Network_id","Year_from_original_date"]):
            x=one_network_score(g)
            if x:parts.append(x)
        if not parts:continue
        fit=pd.DataFrame(parts)
        out["source_leave_one_genus_recomputed"].append({
          "excluded_genus":genus,
          "valid_source_networks":len(fit),
          "source_publications":int(fit.source_publication.nunique()),
          "original_null_score_ratio":group_ratio(fit),
        })
    out["source_species_visit_concentration"]={
      "top_three_source_species":matched["Original_plant_accepted_name_literal"].value_counts().head(3).to_dict(),
      "top_three_original_taxon_plant_network_row_fraction":float(
       matched["Original_plant_accepted_name_literal"].value_counts().head(3).sum()/len(matched))}
    return out,trait,part,scores

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-stage69-flora",required=True,type=Path)
    p.add_argument("--original-stage81b-ages",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    opt=p.parse_args()
    flora=validated_source_csv(opt.original_stage69_flora,SOURCE_ORIGINAL_EUPP_SHA)
    ages=validated_source_csv(opt.original_stage81b_ages,SOURCE_OHASHI_DERIVED_28_SHA)
    result,traits,parts,scores=analyze(flora,ages)
    opt.outdir.mkdir(parents=True,exist_ok=True)
    (opt.outdir/"stage81c_source_original_macro_guild_age_nullscore.json").write_text(
      json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    traits.to_csv(opt.outdir/"stage81c_28_species_trait_age_rms_crosswalk.csv",index=False)
    scores.to_csv(opt.outdir/"stage81c_194_true_source_network_null_scores.csv",index=False)
    print("STAGE81C_REAL_OHASHI_AGE_SPECTRA_28_X_EUPP_PUBLISHED_GUILD_SOURCE",
      json.dumps({k:v for k,v in result.items()
       if isinstance(v,(int,float))},sort_keys=True),flush=True)
if __name__=="__main__":main()
