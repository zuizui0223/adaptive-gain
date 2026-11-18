"""Stage81E: receiver-model contrast source-admission on actual EuPP guild networks.

The unit-of-analysis is an observed source network-year, not an independent
plant evolutionary origin; Japan spectrometers and European visitors are not
co-located. This scores THREE PREDECLARED biological signal dimensions:
  far: late-vs-early achromatic (Apis green receptor), signed
  near: late-vs-early colour contrast to green background, signed
  change: bee honeybee hexagon early-to-late chromatic distance, magnitude
Plus a separately labelled sensitivity using a modeled hexagon 0.09 flag.
Each is a network-conditional zero-effect null-score/I descriptive association
(not a fitted logistic coefficient, actual sensory attention, or adaptation).
Unobserved bee channels are NEVER recoded as species true absence.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from source_ohashi_age_shift_vs_real_EuPP_guild import (
   SOURCE_ORIGINAL_EUPP_SHA,validated_source_csv,source_network_preguild,
   one_network_score,publication_bootstrap,group_ratio
)

ORIGINAL_28=28
ENDPOINTS={
  "late_minus_early_far_green_background_abs":"median_delta_far_green_abs",
  "late_minus_early_near_hex_background_chroma":"median_delta_near_hex_chroma",
  "early_to_late_hex_chromatic_distance":"median_age_colour_shift_hex",
}
SENSITIVITY="independent_model_any_visible_hex_shift"
MIN_PUBLICATIONS=10
EXPECTED_PRE_TOTAL=537
EXPECTED_SOURCE_CANDIDATE_NETWORKS=1040
EXPECTED_SOURCE_ROWS=1921

def genuine_receptor_source_metrics(receptor_path,declared_SHA):
    source=Path(receptor_path).read_bytes()
    digest=hashlib.sha256(source).hexdigest()
    if digest!=declared_SHA:
        raise ValueError("STAGE81E_ORIGINAL_RECEIVER_DERIVED_CSV_DIGEST_CHANGED")
    x=pd.read_csv(receptor_path)
    if x.source_species.nunique()!=ORIGINAL_28 or len(x)!=ORIGINAL_28:
        raise ValueError("STAGE81E_NOT_ORIGINAL_28_INDEPENDENT_SPECIES")
    if x.source_species.duplicated().any():
        raise ValueError("STAGE81E_RECEIVER_SOURCE_SPECIES_REPEATED")
    if not x.source_species.astype(str).str.contains(" ").all():
        raise ValueError("STAGE81E_INVALID_AUTHOR_ACCEPTED_BINOMIAL")
    for col in [*ENDPOINTS.values(),SENSITIVITY]:
        if col not in x:raise ValueError("STAGE81E_REQUIRED_APIS_SIGNAL_FIELD_MISSING")
    for col in ENDPOINTS.values():
        if not np.isfinite(pd.to_numeric(x[col],errors="coerce")).all():
            raise ValueError("STAGE81E_NONFINITE_APIS_SIGNAL_SCORE")
    if not set(x[SENSITIVITY].astype(str).str.lower()).issubset({"true","false"}):
        raise ValueError("STAGE81E_INVALID_SOURCE_VERIFIED_RECEPTOR_DISCRIMINATION_FLAG")
    return x,digest

def mapping_scale_to_equal_species(traits,signal):
    t=traits[["source_species",signal]].copy()
    x=t[signal].to_numpy(dtype=float)
    scale=float(np.std(x,ddof=1))
    if scale<=0:raise ValueError("STAGE81E_ZERO_SIGNAL_BETWEEN_REAL_SPECIES_"+signal)
    t["source_original_accepted_species"]=t.source_species
    t["x_28species_equal_taxon_standardized_log1p_raw_age_RMS"]=(x-np.mean(x))/scale
    return t

def admitted_source_scores(floral,traits,field):
    t=mapping_scale_to_equal_species(traits,field)
    matching,eligible=source_network_preguild(floral,t)
    if (len(matching)!=EXPECTED_SOURCE_ROWS or
        matching.groupby(["Study_id","Network_id","Year_from_original_date"]).ngroups!=EXPECTED_SOURCE_CANDIDATE_NETWORKS or
        eligible.groupby(["Study_id","Network_id","Year_from_original_date"]).ngroups!=EXPECTED_PRE_TOTAL):
        raise ValueError("STAGE81E_SOURCE_FLORA_PRE_BEE_COHORT_CHANGED")
    scores=[]
    for _,group in eligible.groupby(["Study_id","Network_id","Year_from_original_date"],sort=True):
        z=one_network_score(group)
        if z:scores.append(z)
    if not scores:raise ValueError("STAGE81E_NO_SOURCE_INFORMATIVE_NETWORK")
    return pd.DataFrame(scores),matching,eligible

def describe(scores):
    info=scores.groupby("source_publication")["source_I_local_null_fisher_information"].sum()
    if len(info)<MIN_PUBLICATIONS:raise ValueError("STAGE81E_TOO_FEW_TRUE_PUBLISHED_SOURCE_STUDIES")
    mass=info/info.sum()
    output={
      "descriptive_score_per_equal_taxon_standard_deviation_not_a_fitted_beta":group_ratio(scores),
      "source_informative_networks":len(scores),
      "source_distinct_Study_ID":int(scores.Study_id.nunique()),
      "source_independent_published_studies":int(scores.source_publication.nunique()),
      "source_two_or_more_distinct_genera_informative":int((scores.n_original_distinct_measured_source_genera>=2).sum()),
      "source_largest_publication_original_null_information_fraction":float(mass.max()),
      "source_publication_effective_n_by_null_information":float(1/(mass*mass).sum()),
      "source_publication_cluster_bootstrap":publication_bootstrap(scores)
    }
    bypub=scores.groupby("source_publication",sort=True)[["source_U_local_score","source_I_local_null_fisher_information"]].sum()
    loo=[]
    for pub in bypub.index:
        rest=bypub.drop(pub)
        loo.append(float(rest.source_U_local_score.sum()/rest.source_I_local_null_fisher_information.sum()))
    output["source_published_study_leave_one_out_min_max"]=[float(min(loo)),float(max(loo))]
    output["source_published_study_leave_one_out_sign_flips"] =int(sum(v*output["descriptive_score_per_equal_taxon_standard_deviation_not_a_fitted_beta"]<0 for v in loo))
    return output

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-stage69-flora",type=Path,required=True)
    p.add_argument("--original-stage81d-receptor-species",type=Path,required=True)
    p.add_argument("--source-sha256-receptor-species",required=True)
    p.add_argument("--outdir",type=Path,required=True)
    x=p.parse_args()
    flor=validated_source_csv(x.original_stage69_flora,SOURCE_ORIGINAL_EUPP_SHA)
    traits,digest=genuine_receptor_source_metrics(x.original_stage81d_receptor_species,x.source_sha256_receptor_species)
    output={
      "schema":"stage81e_original_28_apis_d65_far_near_green_chromatic_vs_real_EuPP_Bombus_nullscore",
      "original_28_taxon_receptor_model_species_derived_sha256":digest,
      "original_EuPP_botanical_source_plant_guild_sha256":SOURCE_ORIGINAL_EUPP_SHA,
      "source_guild_original_publication_23_24_25_must_cluster_together":True,
      "not_original_emission_odor_or_gust_wind_landing_visited_flower_age":True,
      "not_a_discrimination_learning_or_dynamic_decision_order_measurement":True,
      "not_a_phylogenetic_contrast_or_evolutionary_selection":True,
      "original_Japan_blossom_spectrometer_vs_Europe_visit_spatial_mismatch":True,
      "source_receptor_distances_do_not_identify_true_distant_detection_range_or_actual_functional_guide":True,
      "source_predeclared_endpoint_results":{}
    }
    x.outdir.mkdir(exist_ok=True,parents=True)
    for label,field in ENDPOINTS.items():
        scores,matching,eligible=admitted_source_scores(flor,traits,field)
        desc=describe(scores)
        src=matching.source_original_accepted_species if "source_original_accepted_species" in matching else matching.Original_plant_accepted_name_literal
        c=matching.groupby(["Study_id","Network_id","Year_from_original_date"]).genus.nunique()
        cross=matching.loc[
           matching.set_index(["Study_id","Network_id","Year_from_original_date"]).index.isin(c.index[c>=2])
        ].copy()
        # This restricts to source communities where >=2 original genera exist,
        # but each scored network must still have 2 true bee-bearing taxa.
        alt=[]
        for _,g in cross.groupby(["Study_id","Network_id","Year_from_original_date"]):
            s=one_network_score(g)
            if s:alt.append(s)
        if alt:
            cdf=pd.DataFrame(alt)
            desc["cross_genus_preguild_original_stratum"]={
               "informative_networks":len(cdf),
               "source_publications":int(cdf.source_publication.nunique()),
               "descriptive_score":group_ratio(cdf)}
        non_trif=matching[matching.genus!="trifolium"]
        leave=[]
        for _,g in non_trif.groupby(["Study_id","Network_id","Year_from_original_date"]):
            s=one_network_score(g)
            if s:leave.append(s)
        if leave:
            q=pd.DataFrame(leave)
            desc["Trifolium_excluded_source_reconstructed"]={
               "informative_networks":len(q),
               "source_publications":int(q.source_publication.nunique()),
               "descriptive_score":group_ratio(q)}
        output["source_predeclared_endpoint_results"][label]=desc
        scores.to_csv(x.outdir/("stage81e_"+label+"_network_nullscores.csv"),index=False)
    # Flags: taxon dichotomy from author-independent receiver model only, not
    # a true classified absence of original 2015 stage colour changes.
    output["source_model_hex_visible_0_09_species_count"]=int((traits[SENSITIVITY].astype(str).str.lower()=="true").sum())
    (x.outdir/"stage81e_original_28_apis_far_near_guild_readout.json").write_text(
       json.dumps(output,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
    print("STAGE81E_TRUE_REAL_SPECTRA_RECEIVER_GUILD_SOURCE_MACRO",
          json.dumps({k:{a:b for a,b in v.items() if isinstance(b,(int,float))}
                      for k,v in output["source_predeclared_endpoint_results"].items()},
                     sort_keys=True),flush=True)
if __name__=="__main__":main()
