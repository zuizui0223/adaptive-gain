"""Stage75: continental floral VISUAL-TEXT macro × independent field visitor networks.

THE MACRO MAIN LINE. Original source denominators:
- 59,369 taxon labels, 31,773 source colour record labels, NHM botanical TEXT;
- 1,864 networks across 54 independent European studies, original corrected
  EuPPollNet v1.3.0 and 623,476 visitor event rows, 1,408 species-ranked plants;
- 963 exact same-name species with original NHM source text.

Visual phenotype is ORIGINAL LEXICAL FLOWER COLOUR descriptor (not photographs,
not direct spectrometer wavelength, not UV bullseye or validated nectar guide).
Positive source spot/spotted tokens are EVIDENCE OF A TEXT REPORT ONLY.
An unreported token is UNKNOWN, not a measured trait negative.

Specifying the comparison BEFORE reading guild outcomes:
(1) explicitly YELLOW-only text vs explicitly WHITE-only text,
(2) explicitly YELLOW-only text vs explicitly PURPLE-only text.
"Only" means just one source hue family occurs in source text; it does NOT
prove flowers are biologically monochromatic or that a missing hue is absent.
Compare species only inside SAME original study×network×year field community.

After sample selection: strict recorded species-rank Bombus vs non-Bombus bees.
Use network-intercept null score and expected information; this is a LOCAL
zero-effect approximation, NOT a fitted logistic beta, p-value, genuine fitness,
phylogenetic causal effect or global climate-adjusted SEM. Report study-block
sign fragility and independent site/method/habitat metadata explicitly.

Main dependency is original Stage68→Stage69, NOT stages72–74 case studies.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_literature_macro_stage69"))
from ingest_original_corrected_EuPPollNet_network_NHM_spectra import (
    fetch_original,dict_rows,year_of,guild_of,is_species,EXPECTED_INTERACTIONS
)

NHM_SHA256="b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a"
NETWORK_SHA256="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
SOURCE_NHM=59369
SOURCE_NETWORK_UNITS=18798
SOURCE_GUILD_NETWORKS=1864
SOURCE_STUDY_IDS=54
SOURCE_NAME_OVERLAP=963
COLOUR=("flower colour","petal colour","corolla colour")
HUE_RULES={
  "yellow":r"yellow|yellowish|golden|gold",
  "white":r"white|whitish|cream|ivory",
  "purple":r"purple|purplish|violet|violaceous|lilac|lavender|mauve",
  "blue":r"blue|bluish|azure|cyan",
  "pink":r"pink|pinkish|rose|rosy|salmon",
  "red":r"red|reddish|scarlet|crimson|maroon|carmine",
  "orange":r"orange|orangish|copper",
  "green":r"green|greenish",
  "brown":r"brown|brownish",
  "black":r"black|blackish",
  "gray":r"grey|gray|greyish|grayish",
}
HUE_PATTERNS={key:re.compile(r"(?<![a-z])(?:"+value+r")(?![a-z])")
              for key,value in HUE_RULES.items()}
SPOT_PATTERN=re.compile(r"(?<![a-z])spot(?:ted)?(?![a-z])")
CONTRASTS=(("yellow","white"),("yellow","purple"))
BOOTSTRAPS=2000
SEED=20261118

def source_sha(path,expected):
    h=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if h!=expected:
        raise ValueError("STAGE75_ORIGINAL_SOURCE_DERIVED_ARTIFACT_SHA_CHANGED")
    return h

def csv_rows(path):
    with Path(path).open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def key(s):
    return " ".join(str(s or "").strip().casefold().split())

def source_text_trait(row):
    record={k:str(row.get(k) or "").strip() for k in COLOUR}
    raw=", ".join(v.lower() for v in record.values() if v)
    states=sorted(k for k,pat in HUE_PATTERNS.items() if pat.search(raw))
    return {
      "original_taxon":row["taxon"],
      "original_WFO_link":row.get("wfo",""),
      "source_colour_recorded":int(bool(raw)),
      "source_reported_hue_families":states,
      "n_explicit_source_hue_families":len(states),
      "source_exclusive_lexical_hue":states[0] if len(states)==1 else "",
      "source_colour_descriptor_spot_positive_report":int(bool(SPOT_PATTERN.search(raw))),
      "source_corolla_tube_min_length_text":row.get("corolla tube min. length [cm]",""),
      "source_corolla_tube_max_length_text":row.get("corolla tube max. length [cm]",""),
      "original_UV_spatial_guide_measured":"UNKNOWN",
      "source_lexical_single_hue_does_not_prove_monochromatic_biology":True,
      "source_spot_token_absent_is_NOT_negative":True
    }

def original_trait_map(nhm_rows):
    if len(nhm_rows)!=SOURCE_NHM:raise ValueError("STAGE75_ORIGINAL_NHM_59369_TAXA_CHANGED")
    out={}
    totals=Counter()
    for row in nhm_rows:
        name=key(row["taxon"])
        if not name or name in out:
            raise ValueError("STAGE75_ORIGINAL_NHM_SOURCE_DUPLICATE_LABEL")
        t=source_text_trait(row)
        out[name]=t
        totals["original_all_plant_taxon_labels"]+=1
        totals["original_source_flower_colour_recorded"]+=t["source_colour_recorded"]
        totals["original_source_spot_token_positive_only"]+=t["source_colour_descriptor_spot_positive_report"]
        totals["original_single_hue_word_family"]+=int(bool(t["source_exclusive_lexical_hue"]))
        if t["source_colour_recorded"] and not t["source_reported_hue_families"]:
            totals["original_colour_text_unparsed_or_no_hue_family"]+=1
    return out,dict(totals)

def load_joined_network(rows,traits):
    if len(rows)!=SOURCE_NETWORK_UNITS:
        raise ValueError("STAGE75_ORIGINAL_EUPPOLLNET_18798_SOURCE_UNITS_CHANGED")
    original=defaultdict(list)
    seen=set()
    matched=set();all_species=set()
    overlap_stats=Counter()
    mono_species={};motif=set()
    source_studies=set()
    for r in rows:
        study=r["Study_id"];network=r["Network_id"];year=r["Year_from_original_date"]
        tax=key(r["Original_plant_accepted_name_literal"])
        unique=(study,network,year,tax)
        if unique in seen:raise ValueError("STAGE75_ORIGINAL_SOURCE_DUPLICATE_SPECIES_NETWORK_UNIT")
        seen.add(unique)
        source_studies.add(study)
        all_species.add(tax)
        t=traits.get(tax)
        if t:
            matched.add(tax)
            overlap_stats["matched_source_NHM_plant_network_year_units"]+=1
            overlap_stats["matched_source_plant_network_colour_recorded"]+=t["source_colour_recorded"]
            overlap_stats["matched_source_plant_network_spot_token_positive"]+=t["source_colour_descriptor_spot_positive_report"]
            if t["source_colour_descriptor_spot_positive_report"]:motif.add(tax)
            if t["source_exclusive_lexical_hue"]:
                mono_species[tax]=t["source_exclusive_lexical_hue"]
                overlap_stats["source_lexically_one_hue_plant_network_units"]+=1
        if t and t["source_exclusive_lexical_hue"]:
            original[(study,network,year)].append({
              "Study_id":study,"Network_id":network,"Year":year,
              "species":tax,"genus":tax.split()[0],"hue":t["source_exclusive_lexical_hue"],
              "source_visible_text_single_hue_is_not_field_measured":1,
              "source_unobserved_other_hue_not_known_absent":1,
              "original_reported_pollinator_taxa_scope":r["Author_study_taxa_recorded"],
              "original_sampling_method":r["Author_study_sampling_method"],
              "original_all_rank_pollinator_observation_count":int(r["n_all_observed_visitor_records_this_plant_network"]),
              "source_observed_bombus_any_rank":int(r["n_observed_Bombus"]),
              "source_observed_fly_any_rank":int(r["n_observed_diptera"]),
              "source_observed_butterfly_any_rank":int(r["n_observed_lepidoptera"]),
            })
    if len(source_studies)!=SOURCE_STUDY_IDS:
        raise ValueError("STAGE75_ORIGINAL_54_SOURCE_STUDIES_CHANGED")
    if len(matched)!=SOURCE_NAME_OVERLAP:
        raise ValueError("STAGE75_ORIGINAL_NHM_963_SPECIES_OVERLAP_CHANGED")
    hue_counts=Counter(mono_species.values())
    networks_with_two_lexical_one_hue_species={
        k for k,v in original.items() if len(v)>=2
    }
    networks_with_at_least_two_distinct_hue_lexicons={
        k for k,v in original.items()
        if len({r["hue"] for r in v})>=2
    }
    overall={
      "source_networks_with_at_least_two_source_one_hue_species":len(networks_with_two_lexical_one_hue_species),
      "source_studies_with_at_least_two_source_one_hue_species":len({k[0] for k in networks_with_two_lexical_one_hue_species}),
      "source_networks_with_at_least_two_distinct_explicit_hue_families":len(networks_with_at_least_two_distinct_hue_lexicons),
      "source_studies_with_at_least_two_distinct_explicit_hue_families":len({k[0] for k in networks_with_at_least_two_distinct_hue_lexicons}),
      "source_euppollnet_original_species_ranked_names":len(all_species),
      "source_original_NHM_literal_matched_species":len(matched),
      "source_original_NHM_lexical_one_hue_species":len(mono_species),
      "source_original_NHM_marking_spot_positive_species":len(motif),
      "source_explicit_single_hue_family_species_counts":dict(hue_counts),
      "source_original_nonexclusive_hue_or_no_descriptor_species":
          len(matched)-len(mono_species),
      **dict(overlap_stats),
    }
    return original,overall

def original_context_and_guilds(eligible):
    # Read authentic original visitor records to restore sample spatial/habitat
    # context and enforce species-ranked observed BEE responses. Stage69 summary
    # counted all pollinator ranks; macro inference does NOT silently reuse them.
    contexts=defaultdict(lambda:defaultdict(set))
    bees=defaultdict(Counter)
    counts=Counter()
    for r in dict_rows(fetch_original("Interaction_data.csv.gz"),compressed=True):
        counts["source_original_corrected_visitation_record_rows"]+=1
        net=(r["Study_id"].strip(),r["Network_id"].strip(),year_of(r["Date"]))
        ctx=contexts[net]
        for field in ("Country","Bioregion","EuPPollNet_habitat","Authors_habitat",
                      "Sampling_method","Latitude","Longitude"):
            v=str(r.get(field) or "").strip()
            if v and v.casefold() not in {"na","nan","unknown"}:ctx[field].add(v)
        if net not in eligible:
            continue
        p=key(r["Plant_accepted_name"])
        if not is_species(r):
            continue
        if r.get("Pollinator_rank","").strip().casefold()!="species":
            counts["original_pollinator_not_species_rank_excluded"]+=1
            continue
        if r.get("Pollinator_unsure_id","").strip().casefold() in {"yes","true","1","y"}:
            counts["original_pollinator_unsure_rank_excluded"]+=1
            continue
        g=guild_of(r)
        if g=="Bombus":bees[(net,p)]["B"]+=1
        elif g=="other_bee":bees[(net,p)]["O"]+=1
    if counts["source_original_corrected_visitation_record_rows"]!=EXPECTED_INTERACTIONS:
        raise ValueError("STAGE75_NOT_CORRECTED_623476_VISITOR_ORIGINAL_ROWS")
    if len(contexts)!=SOURCE_GUILD_NETWORKS:
        raise ValueError("STAGE75_ORIGINAL_1864_FIELD_NETWORK_KEYS_CHANGED")
    def clean_context(v):
        if not v:return "SOURCE_NOT_RECORDED"
        return next(iter(v)) if len(v)==1 else "SOURCE_MULTI_VALUE_AMBIGUOUS"
    metadata={
       k:{f:clean_context(v.get(f)) for f in
           ("Country","Bioregion","EuPPollNet_habitat","Authors_habitat",
            "Sampling_method","Latitude","Longitude")}
       for k,v in contexts.items()
    }
    meta_stats={
      "original_field_network_keys":len(contexts),
      "field_network_multi_latitude":sum(len(v.get("Latitude",set()))>1 for v in contexts.values()),
      "field_network_multi_bioregion":sum(len(v.get("Bioregion",set()))>1 for v in contexts.values()),
      "field_network_multi_habitat":sum(len(v.get("EuPPollNet_habitat",set()))>1 for v in contexts.values()),
      "country_categories":dict(Counter(metadata[k]["Country"] for k in metadata)),
      "bioregion_categories":dict(Counter(metadata[k]["Bioregion"] for k in metadata)),
      "source_recorded_habitat_categories":dict(Counter(metadata[k]["EuPPollNet_habitat"] for k in metadata)),
      **dict(counts),
    }
    return bees,metadata,meta_stats

def predefine_color_pair_frames(original,contrasts=CONTRASTS):
    # NO guilds available or consulted while choosing which original field
    # networks contain explicitly documented contrasting flower-color states.
    frames={}
    for pair in contrasts:
        chosen={}
        for k,rows in original.items():
            if set(r["hue"] for r in rows).issuperset(pair):
                chosen[k]=[r for r in rows if r["hue"] in pair]
        frames[pair]=chosen
    return frames

def null_score_pair(plant_rows,bee_events,pair):
    # Network-specific nuisance Bombus rate p_k; null score of indicator
    # yellow vs comparator white/purple *conditional on original community*.
    subset=[]
    for r in plant_rows:
        B=bee_events.get(((r["Study_id"],r["Network_id"],r["Year"]),r["species"]),{}).get("B",0)
        O=bee_events.get(((r["Study_id"],r["Network_id"],r["Year"]),r["species"]),{}).get("O",0)
        N=B+O
        if N:
            subset.append((1 if r["hue"]==pair[0] else 0,B,N,r["species"],r["genus"]))
    if not subset:return None,"NO_STRICT_BEE_SOURCE_EVENTS"
    hues={r[0] for r in subset}
    if len(hues)<2:return None,"ONLY_ONE_HUE_HAS_STRICT_BEE_RECORDS"
    Btot=sum(r[1] for r in subset);Ntot=sum(r[2] for r in subset)
    if Btot==0 or Btot==Ntot:
        return None,"ONLY_ONE_BEE_GUILD_OBSERVED_IN_INFORMATIVE_SOURCE_NETWORK"
    xmean=sum(n*x for x,b,n,sp,g in subset)/Ntot
    p=Btot/Ntot
    score=sum((b-n*p)*(x-xmean) for x,b,n,sp,g in subset)
    info=p*(1-p)*sum(n*(x-xmean)**2 for x,b,n,sp,g in subset)
    if info<=0:return None,"NO_POSITIVE_NULL_INFORMATION"
    genera={x: {r[4] for r in subset if r[0]==x} for x in (0,1)}
    return {
       "Study_id":plant_rows[0]["Study_id"],
       "Network_id":plant_rows[0]["Network_id"],
       "Year":plant_rows[0]["Year"],
       "n_reported_positive_hue_plant_species_with_bee_visits":len(subset),
       "original_field_strict_species_rank_bee_event_count":Ntot,
       "original_field_Bombus_event_count":Btot,
       "original_null_score":score,"original_null_information":info,
       "has_two_colour_states_in_same_genus":int(bool(genera[0]&genera[1])),
       "original_plant_species_in_source":"|".join(sorted(r[3] for r in subset)),
       "original_hue_source_comparison":pair[0]+"_vs_"+pair[1],
       "source_independent_phylogenetic_species_contrasts":False,
    },"INFORMATIVE"

def study_block_summary(informative):
    studies=defaultdict(lambda:[0.,0.,0])
    for r in informative:
        x=studies[r["Study_id"]]
        x[0]+=r["original_null_score"]
        x[1]+=r["original_null_information"]
        x[2]+=1
    total_s=sum(x[0] for x in studies.values())
    total_i=sum(x[1] for x in studies.values())
    ratio=total_s/total_i if total_i>0 else None
    per_study=[{
      "Study_id":study,
      "original_informative_network_count":v[2],
      "original_source_null_score":v[0],
      "original_source_null_information":v[1],
      "source_study_local_null_ratio":v[0]/v[1] if v[1]>0 else None}
      for study,v in sorted(studies.items())]
    if not studies:
        return {
          "informative_networks":0,
          "informative_study_ids":0,
          "source_network_local_null_score_ratio":None,
          "descriptive_study_block_bootstrap_percentile_95":None},per_study
    loo=[(total_s-v[0])/(total_i-v[1]) for v in studies.values()
         if total_i>v[1]]
    study_ratios=[r["source_study_local_null_ratio"] for r in per_study
                  if r["source_study_local_null_ratio"] is not None]
    rng=random.Random(SEED)
    vals=list(studies.values())
    boot=[]
    for _ in range(BOOTSTRAPS):
        rs=[vals[rng.randrange(len(vals))] for _ in vals]
        denom=sum(v[1] for v in rs)
        if denom>0:boot.append(sum(v[0] for v in rs)/denom)
    boot.sort()
    range95=[boot[int(0.025*(len(boot)-1))],
             boot[int(0.975*(len(boot)-1))]] if boot else None
    return {
       "informative_networks":len(informative),
       "informative_study_ids":len(studies),
       "source_network_local_null_score_ratio":ratio,
       "source_original_source_null_score":total_s,
       "source_original_source_null_information":total_i,
       "source_study_block_sign_positive":sum(v[0]>0 for v in studies.values()),
       "source_study_block_sign_negative":sum(v[0]<0 for v in studies.values()),
       "source_study_equal_weight_mean_local_score_ratio":
           sum(study_ratios)/len(study_ratios) if study_ratios else None,
       "source_leave_one_study_out_score_ratio_min":min(loo) if loo else None,
       "source_leave_one_study_out_score_ratio_max":max(loo) if loo else None,
       "source_leave_one_study_out_sign_flip_count":sum((x>0)!=(ratio>0) for x in loo),
       "descriptive_study_block_bootstrap_percentile_95":range95,
       "source_strict_bee_visits_in_informative_networks":
           sum(r["original_field_strict_species_rank_bee_event_count"] for r in informative),
       "original_source_networks_with_both_reported_hues_same_genus":
           sum(r["has_two_colour_states_in_same_genus"] for r in informative),
       "null_score_not_glm_fitted_beta":True,
       "source_study_bootstrap_not_phylogenetic_confidence_interval":True,
       "field_biological_hue_absence_unknown":True,
    },per_study

def run(nhm_path,network_path):
    source_sha(nhm_path,NHM_SHA256)
    source_sha(network_path,NETWORK_SHA256)
    traits,large=original_trait_map(csv_rows(nhm_path))
    networks,overlap=load_joined_network(csv_rows(network_path),traits)
    frames=predefine_color_pair_frames(networks)
    eligible=set().union(*(set(x) for x in frames.values()))
    bee,metadata,context=original_context_and_guilds(eligible)
    unit_rows=[]
    results={}
    site_rows=[]
    study_rows=[]
    study_genera=Counter()
    for (a,b),frame in frames.items():
        base=(a+"_vs_"+b)
        reason=Counter()
        informative=[]
        all_genus_same=0
        for k,plant_rows in sorted(frame.items()):
            colors={x["hue"] for x in plant_rows}
            genus_pairs={x["genus"] for x in plant_rows if x["hue"]==a} & {
              x["genus"] for x in plant_rows if x["hue"]==b}
            all_genus_same+=bool(genus_pairs)
            record,why=null_score_pair(plant_rows,bee,(a,b))
            reason[why]+=1
            if record:
                record.update(metadata[k])
                informative.append(record)
            for r in plant_rows:
                events=bee.get((k,r["species"]),Counter())
                unit_rows.append({
                 "color_contrast":base,
                 **r,
                 "original_strict_Bombus_species_visit_records":events.get("B",0),
                 "original_strict_other_bee_species_visit_records":events.get("O",0),
                 "strict_species_bee_denominator":
                     events.get("B",0)+events.get("O",0),
                 "original_pollinator_absence_confirmed":0,
                 **metadata[k],
                })
        score,studies=study_block_summary(informative)
        unique_species={r["species"] for v in frame.values() for r in v}
        results[base]={
          "source_frozen_hue_contrast":base,
          "source_original_networks_with_two_source_positive_hue_groups_BEFORE_guild_outcomes":len(frame),
          "source_original_distinct_studies_with_eligible_hues":len({k[0] for k in frame}),
          "source_original_distinct_plant_species_with_two_groups":len(unique_species),
          "source_original_genus_matched_networks_before_guild_outcomes":all_genus_same,
          "source_observed_strict_bee_information_status":dict(reason),
          "source_explicit_lexical_hue_only_NOT_flower_monochromatic":True,
          **score,
          "true_nonobserved_guilds_are_unknown_not_zeros":True,
          "species_fully_fixed_effect_would_absorb_constant_hue":True,
          "source_hue_not_direct_bee_visual_color_or_UV":True,
          "source_wind_and_local_VOC_not_measured_in_EuPPollNet":True,
          "original_source_climate_adjusted_phenotype_selection_beta_estimated":False,
          "confirmatory_p_value":None
        }
        for r in informative:site_rows.append(r)
        for r in studies:study_rows.append({"color_contrast":base,**r})
    # Count motif POSITIVE plant names; never compare to 'motif absent'.
    positive_spot=sorted([n for n,t in traits.items()
        if t["source_colour_descriptor_spot_positive_report"]])
    match_plant={r["Original_plant_accepted_name_literal"].casefold()
                   for r in csv_rows(network_path)} & set(traits)
    spot_shared=sorted(set(positive_spot)&match_plant)
    source_summary={
      "schema":"stage75_real_continental_euppollnet_NHM_flower_visual_TEXT_macro",
      "scope":"continental_Europe_54_primary_studies_23_countries_not_global_causal",
      "source_NHM_original_compact_SHA256":NHM_SHA256,
      "source_corrected_EuPPollNet_plant_network_SHA256":NETWORK_SHA256,
      "source_original_NHM_all_taxon_label_counts":large,
      "source_NHM_x_original_recorded_visits":overlap,
      "original_EuPPollNet_source_field_context_and_guild_qc":context,
      "original_reported_spot_positive_all_NHM_taxon_labels":len(positive_spot),
      "original_spot_text_positive_plant_species_with_visits":len(spot_shared),
      "spot_token_nonreport_not_a_measured_negative":True,
      "source_lexical_color_multi_state_excluded_from_single_hue_comparison":True,
      "analysis_hue_pairs_defined_before_original_guild_outcomes":
          ["yellow_vs_white","yellow_vs_purple"],
      "all_field_networks_eligible_hue_group_selection_unconditioned_on_Bombus":True,
      "effect_test_output":results,
      "source_species_independent_evolutionary_origins_not_network_count":True,
      "climate_Bombus_native_range_scent_wind_joint_causal_model_identified":False,
      "no_photographs_no_source_inferred_UV_nectarguide_absence":True,
      "no_confirmatory_phylogenetic_or_global_effect_estimated":True,
    }
    return source_summary,unit_rows,site_rows,study_rows

def write_csv(path,rows):
    if not rows:return
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-NHM",type=Path,required=True)
    p.add_argument("--original-networks",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    a.outdir.mkdir(exist_ok=True,parents=True)
    summary,unit,site,study=run(a.original_NHM,a.original_networks)
    (a.outdir/"original_source_963_species_continental_macro_trait_guild_receipt.json").write_text(
      json.dumps(summary,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    write_csv(a.outdir/"original_source_hue_positive_species_in_network_environment.csv",unit)
    write_csv(a.outdir/"original_source_within_network_guild_conditional_null_scores.csv",site)
    write_csv(a.outdir/"original_source_study_block_null_score_sign_and_coverage.csv",study)
    print("STAGE75_REAL_MACRO_NHM59K_X_EUPPOLLNET54_STUDIES_SOURCE_TRAIT_GUILD",
          json.dumps(summary,sort_keys=True,ensure_ascii=False))
    print("NO_PHOTOS_NO_FAKE_NEGATIVE_UV_NO_CLAIMED_CAUSAL_POLLINATOR_PREFERENCE")

if __name__=="__main__":
    main()
