"""Stage57: original, modality-preserving 817 accepted-species floral evidence atlas.

Inputs are TWO separately source-authenticated GitHub Actions artifacts:
 (1) 583 distinct accepted plants from original UV 2016/2021,
     Ohashi2015 spectral archive, and 2025 positive-only review;
 (2) 243 distinct GBIF accepted plants with original 2025 quantitative
     UV mean reflection, original floral hue, and literature bee/bird
     syndrome, collapsed from 245 original rows (Senecio 2 observations).

Join ONLY on strict accepted GBIF species key. Do not map
"not measured" to flower trait=0; a flower without UV spatial contrast may
have visible guides, scent, learned reward-age colour, or UV reflection.
No species-wide global positive visual-signal state; no direct native site
pollinator presence or causal SEM. The 2025 numeric UV mean is not a
measured UV nectar-guide binary label.
"""
from __future__ import annotations
import argparse,csv,json,math
from collections import Counter
from pathlib import Path

PRIOR_N=583
NEW_N=243
OVERLAP=9
UNION_N=817
PRIOR_UV_STUDY=262
PRIOR_SPATIAL_PATTERNED=101
PRIOR_SPATIAL_UNIFORM=129
PRIOR_OHASHI=207
PRIOR_REVIEW=124
LITERATURE_GUILD={"bee":134,"bird":109}

def read(path):
    with Path(path).open(encoding="utf8",newline="") as fp:
        return list(csv.DictReader(fp))

def from_source_bool(x):
    if x not in (True,False,"True","False"):
        raise ValueError("NO_GO_ORIGINAL_BOOLEAN_TRAIT_PROVENANCE")
    return x in (True,"True")

def combine(prior,source):
    if len(prior)!=PRIOR_N or len(source)!=NEW_N:
        raise ValueError("NO_GO_ORIGINAL_583_OR_243_SOURCE_DENOMINATOR")
    out={}
    prior_studies=set()
    for r in prior:
        key=r.get("gbif_accepted_species_key","")
        if not key.isdigit() or key in out:
            raise ValueError("NO_GO_PRIOR_583_GBIF_ACCEPTED_KEY_NONUNIQUE")
        uv=r["direct_UV_2016_2021_pattern_or_missing"]
        if uv not in ("0","1",""):
            raise ValueError("NO_GO_SOURCE_SPATIAL_UV_NOT_BINARY_OR_UNKNOWN")
        study=r["source_original_direct_UV_studies"]
        if study:
            prior_studies.add(key)
        ohashi=from_source_bool(r["original_Ohashi_2015_age_reflectance_archive"])
        review=from_source_bool(r["original_2025_colour_change_literature_reviewed"])
        out[key]={
            "gbif_accepted_species_key":key,
            "prior_source_UV2016_2021_or_2020_evidence":True,
            "source_UV_pattern_directly_measured_or_unknown":uv,
            "measured_UV_pattern_1_or_uniform_0_is_NOT_all_visual_signal_binary":True,
            "original_Ohashi2015_spectral_taxon_source":ohashi,
            "Ohashi2015_bee_age_colour_change_perceptible":"NOT_SPECIES_CLASSIFIED",
            "original_2025_literature_colour_change_reported":review,
            "review_positive_only_no_observed_negative":True,
            "original_Oliveira2025_UV_mean_source":False,
            "original_Oliveira2025_mean_UV_reflection_or_unknown":"",
            "original_Oliveira2025_source_broad_area_or_unknown":"",
            "original_Oliveira2025_source_family_or_unknown":"",
            "original_Oliveira2025_literature_primary_pollination_system_or_unknown":"",
            "original_Oliveira2025_any_UVplus_hue_or_unknown":"",
            "original_Oliveira2025_n_source_spectral_rows_or_zero":0,
            "no_unknown_visual_modality_inferred_as_absent":True,
            "native_source_phenotyped_site_and_local_pollinator_cooccurrence":"NOT_VERIFIED",
        }
    if len(prior_studies)!=PRIOR_UV_STUDY:
        raise ValueError("NO_GO_PRIOR_SOURCE_UV262_STUDY_KEYS")
    prior_all_keys=set(out)
    if (Counter(r["source_UV_pattern_directly_measured_or_unknown"] for r in out.values())
            !=Counter({"1":PRIOR_SPATIAL_PATTERNED,"0":PRIOR_SPATIAL_UNIFORM,"":353})):
        raise ValueError("NO_GO_PRIOR_DIRECT_UV_PATTERNED_UNIFORM_LABELS")
    if sum(r["original_Ohashi2015_spectral_taxon_source"] for r in out.values())!=PRIOR_OHASHI:
        raise ValueError("NO_GO_PRIOR_2015_SPECTRAL_UNION_COUNT")
    if sum(r["original_2025_literature_colour_change_reported"] for r in out.values())!=PRIOR_REVIEW:
        raise ValueError("NO_GO_PRIOR_REVIEW_COLOUR_CHANGE_UNION_COUNT")
    newkeys=set()
    primary=[]
    for r in source:
        key=r.get("accepted_GBIF_species_key","")
        if not key.isdigit() or key in newkeys:
            raise ValueError("NO_GO_NEW_SOURCE_243_ACCEPTED_NONUNIQUE")
        newkeys.add(key)
        guild=r["source_literature_primary_pollination_system"]
        if guild not in LITERATURE_GUILD:
            raise ValueError("NO_GO_ORIGINAL_2025_POLLINATION_GUILD_UNKNOWN")
        value=float(r["mean_original_source_UV_reflectance"])
        if not math.isfinite(value) or not 0<=value<=1:
            raise ValueError("NO_GO_NUMERIC_UV_REFLECTION_OUTSIDE_0_1")
        rows=int(r["number_original_source_measurement_rows"])
        if rows<1 or rows>2:
            raise ValueError("NO_GO_ORIGINAL_2025_REPEAT_ROW_GRAIN")
        if key not in out:
            out[key]={
                "gbif_accepted_species_key":key,
                "prior_source_UV2016_2021_or_2020_evidence":False,
                "source_UV_pattern_directly_measured_or_unknown":"",
                "measured_UV_pattern_1_or_uniform_0_is_NOT_all_visual_signal_binary":True,
                "original_Ohashi2015_spectral_taxon_source":False,
                "Ohashi2015_bee_age_colour_change_perceptible":"NOT_SPECIES_CLASSIFIED",
                "original_2025_literature_colour_change_reported":False,
                "review_positive_only_no_observed_negative":True,
                "original_Oliveira2025_UV_mean_source":False,
                "original_Oliveira2025_mean_UV_reflection_or_unknown":"",
                "original_Oliveira2025_source_broad_area_or_unknown":"",
                "original_Oliveira2025_source_family_or_unknown":"",
                "original_Oliveira2025_literature_primary_pollination_system_or_unknown":"",
                "original_Oliveira2025_any_UVplus_hue_or_unknown":"",
                "original_Oliveira2025_n_source_spectral_rows_or_zero":0,
                "no_unknown_visual_modality_inferred_as_absent":True,
                "native_source_phenotyped_site_and_local_pollinator_cooccurrence":"NOT_VERIFIED",
            }
        dest=out[key]
        dest["original_Oliveira2025_UV_mean_source"]=True
        dest["original_Oliveira2025_mean_UV_reflection_or_unknown"]=value
        dest["original_Oliveira2025_source_broad_area_or_unknown"]=r["source_broad_area"]
        dest["original_Oliveira2025_source_family_or_unknown"]=r["source_family"]
        dest["original_Oliveira2025_literature_primary_pollination_system_or_unknown"]=guild
        dest["original_Oliveira2025_any_UVplus_hue_or_unknown"]=from_source_bool(r["original_hue_UV_positive_any"])
        dest["original_Oliveira2025_n_source_spectral_rows_or_zero"]=rows
        primary.append(guild)
    if len(newkeys)!=NEW_N or Counter(primary)!=Counter(LITERATURE_GUILD):
        raise ValueError("NO_GO_ORIGINAL_NEW_ACCEPTED_2025_SOURCE_COUNT_GUILD")
    overlap=len(newkeys&prior_all_keys)
    if overlap!=OVERLAP or len(out)!=UNION_N:
        raise ValueError("NO_GO_ORIGINAL_ACCEPTED_KEY_OVERLAP_817_COUNT")
    rows=sorted(out.values(),key=lambda r:int(r["gbif_accepted_species_key"]))
    if sum(r["original_Oliveira2025_UV_mean_source"] for r in rows)!=NEW_N:
        raise ValueError("NO_GO_ORIGINAL_2025_NUMERIC_UV_NOT_243_ACCEPTED")
    return rows,{
        "status":"AUTHENTIC_ORIGINAL_SOURCE_MODALED_FLORAL_UV_COLOR_GUILD_EVIDENCE_817_ACCEPTED",
        "prior_original_UV_age_spectra_review_source_unique_accepted_species":PRIOR_N,
        "new_2025_UV_numeric_species_source_unique_accepted_species":NEW_N,
        "source_accepted_species_overlap":overlap,
        "new_2025_source_unique_accepteds_not_in_prior":len(newkeys-prior_all_keys),
        "combined_distinct_original_source_accepted_botanical_species":len(out),
        "source_original_directly_measured_UV_spatial_patterned":PRIOR_SPATIAL_PATTERNED,
        "source_original_directly_measured_UV_spatial_uniform":PRIOR_SPATIAL_UNIFORM,
        "source_original_Ohashi2015_age_spectra_botanical_species":PRIOR_OHASHI,
        "source_original_2025_colourchange_positive_review_species":PRIOR_REVIEW,
        "source_original_Oliveira_2025_numeric_mean_UV_species":NEW_N,
        "source_original_Oliveira_2025_primary_guild_labels":dict(sorted(Counter(primary).items())),
        "n_species_without_direct_UV_spatial_contrast_classification":sum(
            not r["source_UV_pattern_directly_measured_or_unknown"] for r in rows),
        "n_species_with_original_Oliveira2025_internal_two_measurement_rows":sum(
            r["original_Oliveira2025_n_source_spectral_rows_or_zero"]==2 for r in rows),
        "not_all_817_source_measured_visual_guides_or_positive_signallers":True,
        "source_2025_numeric_mean_UV_is_not_a_floral_pattern":True,
        "no_original_sample_site_native_bee_cooccurrence_or_causal_path":True,
        "review_has_no_negative_unobserved_colour_changes":True,
        "no_unknown_visual_state_encoded_as_false_zero":True
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-prior-583",required=True)
    p.add_argument("--source-2025-243",required=True)
    a=p.parse_args()
    rows,stats=combine(read(a.source_prior_583),read(a.source_2025_243))
    out=Path("stage57_multimodal_817_accepted_visual_species")
    out.mkdir(exist_ok=True)
    with (out/"original_817_accepted_visual_evidence_modality_guild_matrix.csv").open(
         "w",encoding="utf8",newline="") as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/"source_817_original_accepted_modalities_count_receipt.json").write_text(
        json.dumps(stats,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("STAGE57_ORIGINAL_ALL_817_MULTIMODAL_VISUAL_ACCEPTED_EVIDENCE",
          json.dumps(stats,sort_keys=True,ensure_ascii=False))
    print("NO_817_SPECIES_TOTAL_SIGNAL_PRESENCE_OR_NATIVE_BOMBUS_FIT")

if __name__=="__main__":
    main()
