"""Stage75B: phylogeny (genus) and bioregion/study fragility of Stage75 MACRO.

Input is the SHA-verified original-derived Stage75 color×recorded-guild
source dataset, not human-annotated field photographs or the 2021 UV
one-species experiment. Does NOT claim genus equals full phylogenetic tree.

Recompute network null score after removing each genus. Audit genuinely
same-genus contrasting source hue state with actual bee visits. Bioregion is
original EuPPollNet field metadata (7 categories), NOT a measured wind,
altitude, UV-B, scent, native-status or site-year climate treatment.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from authentic_continental_text_signal_guild_macro import (
    null_score_pair,CONTRASTS,study_block_summary,key
)
SOURCE_UNIT_SHA="c55836c115b013ecbe41d00c20ac9348913ce4edbc23178ab3249de024314de5"
SOURCE_ORIGINAL_SITE_SCORE_SHA="17162e9bbc3036564a25f104ef2a211d00b8eaf992f9f7a2df93d5e3d4a39cde"
SOURCE_ORIGINAL_MACRO_RECEIPT_SHA="e63f97c8cafc9d649531b247e5f0559f8c399e0cb72dfa503178806854739d93"

def pinned_csv(path,expected):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected:
        raise ValueError("STAGE75B_ORIGINAL_DERIVED_SOURCE_SHA_CHANGED")
    import io
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))

def original_data_frame(unit):
    frame=defaultdict(list)
    bee={}
    for r in unit:
        k=(r["color_contrast"],r["Study_id"],r["Network_id"],r["Year"])
        base=(r["Study_id"],r["Network_id"],r["Year"])
        tax=key(r["species"])
        if tax!=r["species"]:
            raise ValueError("STAGE75B_ORIGINAL_SOURCE_ACCEPTED_NAME_NORMALIZATION_CHANGED")
        frame[k].append(r)
        if (base,tax) in bee:
            # Every species might appear once per two pre-specified contrasts:
            # the same actual real bee events must remain identical.
            old=bee[(base,tax)]
            if old!=(int(r["original_strict_Bombus_species_visit_records"]),
                      int(r["original_strict_other_bee_species_visit_records"])):
                raise ValueError("STAGE75B_SOURCE_BEE_COUNTS_INCONSISTENT_ACROSS_CONTRASTS")
        bee[(base,tax)]=(
            int(r["original_strict_Bombus_species_visit_records"]),
            int(r["original_strict_other_bee_species_visit_records"]))
    source_bees={k:{"B":v[0],"O":v[1]} for k,v in bee.items()}
    return frame,source_bees

def recalculated(frame,bees,pair):
    chosen=[]
    same_genus=[]
    for (_,study,net,year),rows in sorted(frame.items()):
        value,reason=null_score_pair(rows,bees,pair)
        if value:chosen.append(value)
        bygen=defaultdict(list)
        for row in rows:bygen[row["genus"]].append(row)
        for gen,subset in bygen.items():
            if len({row["hue"] for row in subset})<2:continue
            own,why=null_score_pair(subset,bees,pair)
            same_genus.append({
              "contrast":pair[0]+"_vs_"+pair[1],
              "source_Study_id":study,"source_Network_id":net,"source_Year":year,
              "genus":gen,
              "source_plant_names_in_same_genus": "|".join(sorted(x["species"] for x in subset)),
              "source_two_explicit_hue_states_within_same_genus":1,
              "source_strict_bee_visitor_comparison_informative":int(own is not None),
              "source_null_score":own["original_null_score"] if own else "",
              "source_null_information":own["original_null_information"] if own else "",
              "source_guild_uninformative_reason":"" if own else why,
            })
    return chosen,same_genus

def context_summary(source_network_site_scores):
    groups=defaultdict(list)
    for r in source_network_site_scores:
        for dimension in ("Bioregion","Country","EuPPollNet_habitat"):
            groups[(r["original_hue_source_comparison"],dimension,r[dimension])].append(r)
    out=[]
    for (contrast,dimension,value),rows in sorted(groups.items()):
        score=sum(float(r["original_null_score"]) for r in rows)
        inf=sum(float(r["original_null_information"]) for r in rows)
        out.append({
          "contrast":contrast,"original_field_context_dimension":dimension,
          "source_context_recorded_value":value,
          "original_informative_networks":len(rows),
          "original_distinct_study_ids":len({r["Study_id"] for r in rows}),
          "original_null_score":score,
          "original_null_information":inf,
          "source_null_local_score_ratio_if_information":
              score/inf if inf>0 else "",
          "source_field_context_not_direct_wind_or_climate_Bombus_model":1,
          "nonindependent_taxon_and_study_cluster_not_corrected":1,
        })
    return out

def analyze(unit,original_scores,macro_receipt):
    if not macro_receipt["all_field_networks_eligible_hue_group_selection_unconditioned_on_Bombus"]:
        raise ValueError("STAGE75B_HUE_FRAME_NOT_FROZEN_BEFORE_GUILD_OUTCOME")
    f,bee=original_data_frame(unit)
    answer={}
    same_genus_all=[]
    genus_rows=[]
    for pair in CONTRASTS:
        contrast=pair[0]+"_vs_"+pair[1]
        subset={k:v for k,v in f.items() if k[0]==contrast}
        original=macro_receipt["effect_test_output"][contrast]
        if len(subset)!=original["source_original_networks_with_two_source_positive_hue_groups_BEFORE_guild_outcomes"]:
            raise ValueError("STAGE75B_ORIGINAL_NETWORK_HUE_FRAME_DIFFERENT")
        source,within=recalculated(subset,bee,pair)
        if len(source)!=original["informative_networks"]:
            raise ValueError("STAGE75B_ORIGINAL_SOURCE_INFORMATIVE_NETWORK_COUNT_MISMATCH")
        score,study=study_block_summary(source)
        if abs(score["source_network_local_null_score_ratio"]-
               original["source_network_local_null_score_ratio"])>1e-10:
            raise ValueError("STAGE75B_ORIGINAL_MACRO_SCORE_NOT_REPRODUCED")
        if len(within)!=original["source_original_genus_matched_networks_before_guild_outcomes"]:
            raise ValueError("STAGE75B_ORIGINAL_SAME_GENUS_SOURCE_COUNTS_MISMATCH")
        taxa={r["species"] for rows in subset.values() for r in rows}
        genera=sorted({r["genus"] for rows in subset.values() for r in rows})
        leavegen=[]
        for genus in genera:
            removed={k:[r for r in rows if r["genus"]!=genus]
                     for k,rows in subset.items()}
            informative,_=recalculated(removed,bee,pair)
            if not informative:continue
            result,_=study_block_summary(informative)
            leavegen.append({
             "contrast":contrast,
             "omitted_source_genus":genus,
             "original_informative_networks_without_genus":len(informative),
             "source_null_local_score_ratio_without_genus":
                 result["source_network_local_null_score_ratio"],
             "source_same_site_design_preselected_before_guild":1,
             "not_a_phylogenetic_comparative_model":1,
            })
        prior=score["source_network_local_null_score_ratio"]
        values=[r["source_null_local_score_ratio_without_genus"] for r in leavegen]
        informative_within=[v for v in within if v["source_strict_bee_visitor_comparison_informative"]]
        sumU=sum(float(x["source_null_score"]) for x in informative_within)
        sumI=sum(float(x["source_null_information"]) for x in informative_within)
        answer[contrast]={
          "matched_source_hue_plant_species":len(taxa),
          "distinct_source_genera_in_hue_comparison":len(genera),
          "source_hue_eligible_networks":len(subset),
          "original_informative_strict_bee_source_networks":len(source),
          "source_independent_studies_in_informative_networks":score["informative_study_ids"],
          "original_macro_score_reproduced":prior,
          "leave_one_original_genus_out_source_ratio_min":min(values) if values else None,
          "leave_one_original_genus_out_source_ratio_max":max(values) if values else None,
          "leave_one_original_genus_out_sign_changes":
              sum((x>0)!=(prior>0) for x in values),
          "source_within_genus_lexical_color_contrast_networks":len(within),
          "source_within_genus_strict_bee_informative_networks":len(informative_within),
          "source_distinct_genera_with_informative_within_genus_comparison":
              len({x["genus"] for x in informative_within}),
          "source_within_genus_only_null_score_ratio_if_informative":
              sumU/sumI if sumI>0 else None,
          "source_within_genus_approximation_not_full_plant_phylogeny":True,
          "source_name_lexicon_cannot_establish_true_pollination_syndrome":True,
          "source_field_wind_VOC_climate_unmeasured_jointly":True,
          "new_significant_evolutionary_effect_estimated":False,
        }
        same_genus_all+=within
        genus_rows+=leavegen
    regions=context_summary(original_scores)
    return {
       "schema":"stage75b_continental_original_hue_guild_macro_phylogenetic_and_region_fragility",
       "real_source_59k_taxon_963_plant_54study_Europe_macro":True,
       "source_plant_biological_guide_absence_unknown":True,
       "original_source_genus_not_validated_full_phylogenetic_clade":True,
       "ecological_environment_source_category_not_continuous_microclimate":True,
       "source_original_cross_guild_Bombus_outcome_not_causal_preference":True,
       "source_macronetwork_results":answer,
       "source_context_stratification":regions,
       "source_within_genus_contrast_details":same_genus_all,
       "source_leave_genus_diagnostics":genus_rows,
       "original_UV_spatial_motif_not_measured_in_NHM":True,
       "confirmatory_phylogenetic_multiregion_pollination_result":False,
    }

def write_csv(path,rows):
    if not rows:return
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--Stage75-hue-source",required=True,type=Path)
    p.add_argument("--Stage75-original-network-scores",required=True,type=Path)
    p.add_argument("--Stage75-original-macro-receipt",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    unit=pinned_csv(a.Stage75_hue_source,SOURCE_UNIT_SHA)
    sites=pinned_csv(a.Stage75_original_network_scores,SOURCE_ORIGINAL_SITE_SCORE_SHA)
    if hashlib.sha256(a.Stage75_original_macro_receipt.read_bytes()).hexdigest()!=SOURCE_ORIGINAL_MACRO_RECEIPT_SHA:
        raise ValueError("STAGE75B_ORIGINAL_MAIN_MACRO_RECEIPT_SHA_CHANGED")
    original=json.loads(a.Stage75_original_macro_receipt.read_text())
    result=analyze(unit,sites,original)
    a.outdir.mkdir(parents=True,exist_ok=True)
    (a.outdir/"source_original_macro_genus_bioregion_study_robustness_receipt.json").write_text(
      json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    write_csv(a.outdir/"source_original_macro_reported_hue_within_genus_contrasts.csv",
              result["source_within_genus_contrast_details"])
    write_csv(a.outdir/"source_original_macro_leave_one_genus_out.csv",
              result["source_leave_genus_diagnostics"])
    write_csv(a.outdir/"source_original_macro_bioregion_habitat_stratification.csv",
              result["source_context_stratification"])
    print("STAGE75B_REAL_CONTINENTAL_MACRO_SOURCE_STUDY_GENUS_BIOREGION_DIAGNOSTICS",
          json.dumps({"results":result["source_macronetwork_results"],
                      "bioregion":[x for x in result["source_context_stratification"]
                                  if x["original_field_context_dimension"]=="Bioregion"]},sort_keys=True))
    print("GENUS_NOT_PHYLOGENETIC_TREE_NO_RECEPTOR_SPECIFIC_UV_OR_CAUSAL_MODEL")
if __name__=="__main__":
    main()
