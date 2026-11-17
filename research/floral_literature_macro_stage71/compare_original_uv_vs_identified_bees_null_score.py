"""Stage71C: exploratory within-network *null-score* optical vs recorded bee composition.

This is a source-authenticated DESCRIPTIVE covariance/score audit, not a
maximised logistic MLE, conditional likelihood CI, p-value or proof of visual
cue-use, adaptation, effective pollination or wild-site measured phenotype.
The frozen analytical cohort is Stage71B (685 pre-guild native-site candidates),
NOT Stage69B's response-conditioned 156 or Stage70's 73/135.

Study-level and taxon-level repeated use is never treated as independent n.
"""
from __future__ import annotations
import argparse,csv,json,math
from collections import defaultdict,Counter
from pathlib import Path

UV="petal_UV_300_399nm_mean_reflectance_percent_original_garden"
VISIBLE="petal_visible_400_700nm_mean_reflectance_percent_original_garden"
Y_B="source_bumblebee_species_rank_records"
Y_O="source_other_bee_species_rank_records"
Y_N="source_total_accepted_species_rank_bee_records"
SPECIES="original_plant_species"

MODES={
  "conservative_original_valid_TDWG":{
      "network_eligibility":"primary_original_geometry_study_eligible",
      "species_native":"cohort_primary_WCVP_regional_native_eligible",
      "required_networks":452},
  "old_TDWG_repaired_GIS_sensitivity":{
      "network_eligibility":"geo_repair_geometry_study_eligible",
      "species_native":"cohort_geo_repair_WCVP_regional_native_eligible",
      "required_networks":625}
}
MIN_BEES=[1,3]


def read(path):
    with Path(path).open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))


def network_score(native_source_rows,min_bees):
    # Analytically exact null score and Fisher information of a binomial
    # network-intercept logit p(Bombus | identified bees, plant, network).
    # No network selection by Bombus/other-bee availability.
    keep=[]
    for r in native_source_rows:
        B=int(r[Y_B]);O=int(r[Y_O]);N=int(r[Y_N])
        if B<0 or O<0 or B+O!=N:
            raise ValueError("STAGE71C_INVALID_OR_UNDERREPORTED_BEES")
        if N>=min_bees:
            keep.append((r,B,N,float(r[UV])/10.0,float(r[VISIBLE])/10.0))
    if len(keep)<2:
        return None,"FEWER_THAN_TWO_BEE_OBSERVED_PLANTS"
    b=sum(o[1] for o in keep); n=sum(o[2] for o in keep)
    if b==0 or b==n:
        return None,"SINGLE_RECORDED_BEE_GUILD"
    xb=sum(o[2]*o[3] for o in keep)/n
    xv=sum(o[2]*o[4] for o in keep)/n
    if len({o[3] for o in keep})<2:
        return None,"NO_ORIGINAL_UV_VARIATION_AMONG_BEE_RECORDED_PLANTS"
    q=b/n
    Su=sum((B-N*q)*(u-xb) for _,B,N,u,v in keep)
    Sv=sum((B-N*q)*(v-xv) for _,B,N,u,v in keep)
    Iuu=q*(1-q)*sum(N*(u-xb)**2 for _,B,N,u,v in keep)
    Ivv=q*(1-q)*sum(N*(v-xv)**2 for _,B,N,u,v in keep)
    Iuv=q*(1-q)*sum(N*(u-xb)*(v-xv) for _,B,N,u,v in keep)
    if Iuu<=0:return None,"ZERO_INFORMATION"
    return {
      "Study_id":keep[0][0]["Study_id"],"Network_id":keep[0][0]["Network_id"],
      "Year":keep[0][0]["Year"],
      "n_species_with_identified_bee_records":len(keep),
      "observed_strict_Bombus_bee_event_rows":b,
      "observed_strict_all_bee_event_rows":n,
      "null_score_UV_per_10pct_points":Su,
      "null_information_UV_per_10pct_points":Iuu,
      "null_score_visible_per_10pct_points":Sv,
      "null_information_visible_per_10pct_points":Ivv,
      "null_cross_information_UV_by_visible":Iuv,
      "source_species_names_joined":"|".join(sorted(o[0][SPECIES] for o in keep)),
      "author_source_sampling_method":keep[0][0]["source_sampling_method"],
      "all_birds_unobserved_in_EuPPollNet":1,
      "source_plant_spectra_is_German_garden_not_this_field":"NOT_MATCHED",
    },"INFORMATIVE_NULL_SCORE"


def null_score_summary(informative):
    if not informative:
        return {"informative_networks":0,"informative_studies":0,
                "null_score_slope_approx_UV_per_10pct_points":None}
    study=defaultdict(lambda:[0.0,0.0,0.0,0.0,0.0,0,0])
    for r in informative:
        s=study[r["Study_id"]]
        s[0]+=r["null_score_UV_per_10pct_points"]
        s[1]+=r["null_information_UV_per_10pct_points"]
        s[2]+=r["null_score_visible_per_10pct_points"]
        s[3]+=r["null_information_visible_per_10pct_points"]
        s[4]+=r["null_cross_information_UV_by_visible"]
        s[5]+=1
        s[6]+=r["observed_strict_all_bee_event_rows"]
    S=sum(v[0] for v in study.values());I=sum(v[1] for v in study.values())
    V_S=sum(v[2] for v in study.values());V_I=sum(v[3] for v in study.values())
    CI=sum(v[4] for v in study.values())
    if I<=0 or V_I<=0:
        raise ValueError("STAGE71C_BAD_BIOMODAL_SOURCE_INFORMATION")
    # Exact score/expected-information ratio at β=0. This is a LOCAL linear
    # approximation; do not exponentiate to 'fitted odds ratio'.
    uv=S/I;vis=V_S/V_I
    jointdet=I*V_I-CI**2
    UVadj=(S*V_I-V_S*CI)/jointdet if jointdet>1e-12 else None
    VISadj=(V_S*I-S*CI)/jointdet if jointdet>1e-12 else None
    leave_studies=[]
    for name,s in sorted(study.items()):
        out=(S-s[0])/(I-s[1]) if I-s[1]>0 else None
        leave_studies.append({
          "Study_id":name,"n_informative_networks":s[5],
          "observed_bee_event_rows":s[6],
          "within_study_uv_null_score":s[0],
          "within_study_uv_null_information":s[1],
          "within_study_local_uv_score_ratio":s[0]/s[1] if s[1]>0 else "",
          "after_leave_one_study_out_uv_score_ratio":out if out is not None else "",
          "study_source_sign_positive":int(s[0]>0),
        })
    nonmissing_loo=[r["after_leave_one_study_out_uv_score_ratio"] for r in leave_studies
                     if r["after_leave_one_study_out_uv_score_ratio"]!=""]
    return {
      "informative_networks":len(informative),
      "informative_studies":len(study),
      "original_identified_bee_event_rows_in_informative_networks":sum(v[6] for v in study.values()),
      "study_uv_null_scores_positive":sum(v[0]>0 for v in study.values()),
      "study_uv_null_scores_negative":sum(v[0]<0 for v in study.values()),
      "null_uv_score":S,"null_uv_information":I,
      "null_visible_score":V_S,"null_visible_information":V_I,
      "null_uv_visible_cross_information":CI,
      "null_score_slope_approx_UV_per_10pct_points":uv,
      "null_score_slope_approx_visible_per_10pct_points":vis,
      "null_joint_score_uv_adjusted_for_visible_per_10pct_points":UVadj,
      "null_joint_score_visible_adjusted_for_uv_per_10pct_points":VISadj,
      "null_joint_information_determinant":jointdet,
      "study_leave_one_out_local_uv_score_ratio_min":min(nonmissing_loo) if nonmissing_loo else None,
      "study_leave_one_out_local_uv_score_ratio_max":max(nonmissing_loo) if nonmissing_loo else None,
      "study_leave_one_out_flipped_sign":sum((v>0)!=(uv>0) for v in nonmissing_loo),
    },leave_studies


def analyze(panel,network_frame,mode,min_bees):
    contract=MODES[mode]
    valid={(r["Study_id"],r["Network_id"],r["Year"])
           for r in network_frame if r[contract["network_eligibility"]]=="1"}
    if len(valid)!=contract["required_networks"]:
        raise ValueError(f"STAGE71C_FROZEN_NATIVE_UNSELECTED_NETWORKS_CHANGED_{mode}_{len(valid)}")
    original=defaultdict(list)
    for r in panel:
        k=(r["Study_id"],r["Network_id"],r["Year"])
        if k in valid and r[contract["species_native"]]=="1":
            original[k].append(r)
    if set(original)!=valid:
        raise ValueError(f"STAGE71C_SOURCE_NATIVE_COHORT_HAS_UNFILLED_NETWORK_{mode}")
    vals=[]; reasons=Counter()
    for k in sorted(valid):
        v,reason=network_score(original[k],min_bees)
        reasons[reason]+=1
        if v:vals.append(v)
    all_result,studies=null_score_summary(vals) if vals else (
      {"informative_networks":0,"informative_studies":0},[])
    if sum(reasons.values())!=len(valid):
        raise ValueError("STAGE71C_STUDY_NETWORK_QUALIFICATION_NOT_ONE_TO_ONE")
    # Adversarial taxon-block fragility: recompute *within network* after
    # removing each source optical plant species; do not merely subtract its
    # original network score.
    taxa=sorted({r[SPECIES] for rows in original.values() for r in rows})
    species_loo=[]
    for excluded in taxa:
        rem=[]
        for k in sorted(valid):
            usable=[r for r in original[k] if r[SPECIES]!=excluded]
            one,_=network_score(usable,min_bees)
            if one:rem.append(one)
        if rem:
            report,_=null_score_summary(rem)
            beta=report["null_score_slope_approx_UV_per_10pct_points"]
        else:beta=None
        species_loo.append({
            "omitted_source_spectrometer_taxon":excluded,
            "informative_source_networks_remaining":len(rem),
            "null_local_uv_score_ratio_without_taxon":beta if beta is not None else "",
            "source_spectra_only_one_species_level_measurement":1,
        })
    n_taxa=len(taxa)
    loo=[r["null_local_uv_score_ratio_without_taxon"] for r in species_loo
         if r["null_local_uv_score_ratio_without_taxon"]!=""]
    original_beta=all_result.get("null_score_slope_approx_UV_per_10pct_points")
    summary={
      "analysis_mode":mode,"min_source_accepted_species_bee_records_per_plant":min_bees,
      "frozen_source_original_networks_not_selected_by_Bombus":len(valid),
      "frozen_source_original_spectrometer_taxa":n_taxa,
      "source_qualifiability_after_opening_bee_record_counts":dict(reasons),
      **all_result,
      "taxon_leave_one_out_local_uv_score_ratio_min":min(loo) if loo else None,
      "taxon_leave_one_out_local_uv_score_ratio_max":max(loo) if loo else None,
      "taxon_leave_one_out_sign_flips":sum((v>0)!=(original_beta>0) for v in loo)
          if original_beta is not None else None,
      "event_count_variance_not_plant_count_adjusted":True,
      "score_is_one_step_null_linear_approximation_not_fitted_mle":True,
      "study_networks_and_species_not_independent_replicates":True,
      "source_taxon_fixed_effect_would_absorb_species_constant_spectrum":True,
      "source_same_field_spectrum_receptor_response_fitness_unknown":True,
      "association_is_descriptive_not_causal_or_phylogenetically_controlled":True,
      "formal_confirmatory_statistical_pvalue_or_confidence_interval":None,
    }
    return summary,vals,studies,species_loo


def save_csv(out,rows):
    with Path(out).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-guild-after-freeze",required=True,type=Path)
    p.add_argument("--original-native-network-frame",required=True,type=Path)
    p.add_argument("--original-source-receipt",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    source=json.loads(a.original_source_receipt.read_text())
    if (source["networks_with_at_least_two_original_spectrometer_species_before_outcomes"]!=685 or
        source["source_guild_information_used_in_cohort_selection"] or
        source["original_strict_bee_record_audit"]["source_actual_corrected_visit_rows"]!=623476):
        raise ValueError("STAGE71C_ORIGINAL_UNSELECTED_REAL_SOURCE_NOT_FROZEN")
    panel=read(a.original_guild_after_freeze)
    frame=read(a.original_native_network_frame)
    a.outdir.mkdir(exist_ok=True,parents=True)
    results={}
    for mode in MODES:
        for min_bees in MIN_BEES:
            stamp=mode+"__min_bee_"+str(min_bees)
            s,net,study,taxon=analyze(panel,frame,mode,min_bees)
            results[stamp]=s
            if net:save_csv(a.outdir/(stamp+"__informative_network_null_scores.csv"),net)
            if study:save_csv(a.outdir/(stamp+"__study_block_leaveout.csv"),study)
            if taxon:save_csv(a.outdir/(stamp+"__original_spectrometer_species_leaveout.csv"),taxon)
    response={
      "schema":"stage71c_correction_aware_outcome_blind_uv_vs_visitor_guild_null_score_20261117",
      "original_plant_spectra_source":"2024 botanical garden spectrometer true 300-399 nm mean petal",
      "original_real_visits_source":"corrected EuPPollNet v1.3.0 actual species-rank bee visits",
      "previous_stage69_156_and_stage70_73_or_135_guild_outcome_conditioned_samples_rejected":True,
      "primary_and_repaired_geometry_independent_pre_outcome_cohorts":True,
      "testing_one_prespecified_uv_predictor_and_visible_control":True,
      "scores_not_fitted_logit_regression_or_causal_selection":True,
      "source_field_flower_abundance_exposure_not_harmonized":True,
      "source_species_and_study_nonindependence_explicit":True,
      "phylogeny_genus_and_source_population_trait_persistence_unidentified":True,
      "result_cells":results,
    }
    (a.outdir/"null_score_guild_composition_source_and_sensitivity_receipt.json").write_text(
       json.dumps(response,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("STAGE71C_SOURCE_REAL_UV_VS_OBSERVED_BEE_GUILD_NULL_SCORE",
          json.dumps(response,sort_keys=True))
    print("NO_FALSE_OR_CAUSAL_BETA_NO_PSEUDOREPLICATED_P_NO_GLOBAL_GUILD_ADAPTATION")
if __name__=="__main__":main()
