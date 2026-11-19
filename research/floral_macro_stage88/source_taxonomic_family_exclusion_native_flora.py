"""Stage88D: Source-verified global native floral trait family exclusion tests.

Original pre-2026 NHM 59,369 botanical flower-text labels; official WCVP
taxon NAME family and region-specific native distributions. This source
can check whether global WIND x green/brown botanical colour geography
depends on graminoid and some potentially anemophilous plant families.

IMPORTANT: membership of a family is NOT observed species pollination mode.
A Poaceae/Cyperaceae/Juncaceae *lineage exclusion* is not equivalent to
independent Wang2025 179263 plant animal-vs-wind labels. Mixed families
are explicitly labelled exploratory. No genotype or phylogenetic distance.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,zipfile
from pathlib import Path
from collections import Counter,defaultdict

from global_native_pollination_mode_tdwg3 import summarize_one_region
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage87"))
from global_native_floral_signal_tdwg3 import (
    load_nhm,wcvp_regions,strict_name,HUES,WCVP_SHA
)

GRAMINOID=set(("Poaceae","Cyperaceae","Juncaceae"))
OTHER_WIND_ENRICHED=set(("Betulaceae","Fagaceae","Juglandaceae",
   "Myricaceae","Casuarinaceae","Platanaceae","Ulmaceae","Urticaceae",
   "Salicaceae"))
# Extra family set is a LEAVE-OUT design, never labels every species as wind.
SCOPES={
 "all_original_source_taxa":set(),
 "exclude_three_graminoid_families":GRAMINOID,
 "exclude_graminoid_plus_nine_wind_enriched_families":GRAMINOID|OTHER_WIND_ENRICHED,
}

def source_families(path,target):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=WCVP_SHA:
        raise ValueError("STAGE88D_Kew_OFFICIAL_ARCHIVE_SHA_NOT_MATCHING_2026")
    resolved=defaultdict(set);cats=Counter();schema=[]
    with zipfile.ZipFile(path) as z:
        with io.TextIOWrapper(z.open("wcvp_names.csv"),encoding="utf-8",
                              errors="replace",newline="") as f:
            reader=csv.DictReader(f,delimiter="|")
            schema=list(reader.fieldnames or [])
            candidates=[k for k in schema if k.casefold() in {"family","family_name"}]
            if len(candidates)!=1:
                raise ValueError("STAGE88D_WCVP_FAMILY_COLUMN_NOT_PROVEN_"+str(schema[:30]))
            col=candidates[0]
            for row in reader:
                cats["all_WCVP_original_name_rows"]+=1
                if row.get("taxon_rank","").strip().casefold()!="species":continue
                if row.get("taxon_status","").strip().casefold()!="accepted":continue
                sp=strict_name(row.get("taxon_name"))
                if sp not in target:continue
                family=str(row[col] or "").strip()
                if family:resolved[sp].add(family.title().replace(" ", ""))
    out={}
    conflict=set()
    for sp,vals in resolved.items():
        if len(vals)==1:out[sp]=next(iter(vals))
        else:conflict.add(sp)
    cats["original_strict_NHM_plant_species_target"]=len(target)
    cats["WCVP_family_exact_unambiguous_source_species"]=len(out)
    cats["WCVP_family_conflicted_species_not_classified"]=len(conflict)
    cats["WCVP_family_no_source_or_ambiguous"]=len(target)-len(out)
    cats["WCVP_taxonomic_original_header"]=schema
    if len(out)<50000:raise ValueError("STAGE88D_Kew_FAMILY_COVERAGE_TOO_LOW")
    return out,dict(cats)

def mode_agnostic_summary(code,taxa,traits):
    # In this helper "mode" is purely a subset marker: force a local
    # all-source mode in the tested family-exclusion cohort.
    subset=summarize_one_region(code,taxa,{},traits)["unknown"]
    # Copy to source schema compatible with Stage87E's original fractions.
    rec={
        "TDWG_L3":code,
        "n_source_single_explicit_hue":subset["source_explicit_single_hue_species"],
        "n_source_colour_documented":subset["source_NHM_flower_colour_documented_species"],
        "n_source_native_NHM_species":subset["source_WCVP_native_NHM_species_count"],
        "n_source_native_genera":subset["source_native_unique_genera"],
        "source_documented_colour_coverage_fraction":
            subset["source_colour_documentation_fraction"],
        "source_pollination_mode_NOT_claimed":"TRUE",
        "source_family_exclusion_not_direct_anemophily_label":"TRUE",
    }
    for h in HUES:
        rec["hue_"+h+"_count"]=subset["hue_"+h+"_count"]
        rec["hue_"+h+"_fraction_of_exclusive_documented"]=subset[
           "hue_"+h+"_fraction_of_exclusive_documented"]
        rec["hue_"+h+"_mean_of_genus_fractions"]=subset[
           "hue_"+h+"_mean_of_genus_fractions"]
    return rec

def reconstruct(nhm_path,wcvp_path,outdir):
    traits,tmeta=load_nhm(nhm_path)
    ranges,rmeta=wcvp_regions(wcvp_path,traits)
    fam,fmeta=source_families(wcvp_path,traits)
    names=set().union(*ranges.values())
    missing={sp for sp in names if sp not in fam}
    if len(names)!=55775:
        raise ValueError("STAGE88D_ORIGINAL_GLOBAL_WCVP_55775_NATIVE_SPECIES_CHANGED")
    output=[];coverage={};comparisons={}
    for label,excluded_families in SCOPES.items():
        local=[]
        for code,plants in sorted(ranges.items()):
            if label=="all_original_source_taxa":select=plants
            else:select={sp for sp in plants if sp in fam and fam[sp] not in excluded_families}
            record=mode_agnostic_summary(code,select,traits)
            record["source_exclusion_sensitivity"]=label
            local.append(record)
        if len(local)!=367:
            raise ValueError("STAGE88D_ORIGINAL_NATIVE_GEOGRAPHIC_UNIVERSE_CHANGED")
        output.extend(local)
        coverage[label]={
          "original_source_regions":len(local),
          "unique_original_native_WCVP_species_retained":len(set().union(*(
              plants if label=="all_original_source_taxa" else {
                  sp for sp in plants if sp in fam and fam[sp] not in excluded_families}
              for plants in ranges.values()))),
          "regions_with_25_explicit_hue_species":
             sum(row["n_source_single_explicit_hue"]>=25 for row in local),
          "regions_with_50_explicit_hue_species":
             sum(row["n_source_single_explicit_hue"]>=50 for row in local),
          "regional_native_taxon_incidence":sum(row["n_source_native_NHM_species"] for row in local),
          "original_named_families_excluded":sorted(excluded_families),
          "family_exclusion_NOT_source_verified_pollination_mode":True}
    # A family leaveout must have a smaller denominator in at least one
    # region. This is a meaningful source-data sensitivity, not a tautology.
    primary={row["TDWG_L3"]:row for row in output if row["source_exclusion_sensitivity"]=="all_original_source_taxa"}
    for label in list(SCOPES)[1:]:
        rows=[r for r in output if r["source_exclusion_sensitivity"]==label]
        if not any(row["n_source_native_NHM_species"]<primary[row["TDWG_L3"]]["n_source_native_NHM_species"] for row in rows):
            raise ValueError("STAGE88D_SOURCE_FAMILY_EXCLUSION_DID_NOT_REMOVE_ANY_PLANTS")
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage88D_global_TDWG3_native_flora_hue_three_family_exclusion_designs.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]))
        w.writeheader();w.writerows(output)
    report={"schema":"stage88D_global_WCVP_NHM_explicit_taxonomic_family_leaveout",
      "source_original_NHM":tmeta,
      "source_original_Kew_WCVP_native":rmeta,
      "source_original_Kew_WCVP_family":fmeta,
      "source_global_original_55775_species":len(names),
      "source_taxa_with_no_verified_family":len(missing),
      "source_frozen_family_exclusion_sensitivity":coverage,
      "source_not_species_animal_wind_pollination_classification":True,
      "source_original_TDWG3_regional_memberships_not_physical_flower_populations":True,
      "source_no_source_pollinator_VISUAL_learning_or_wind_VOC_landings":True}
    (outdir/"stage88D_original_global_family_exclusion_source_receipt.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE88D_SOURCE_GLOBAL_FAMILY_EXCLUSION_REGIONAL_COVERAGE",
          json.dumps(coverage,sort_keys=True))
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-NHM",type=Path,required=True)
    p.add_argument("--original-WCVP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    x=p.parse_args();reconstruct(x.original_NHM,x.original_WCVP,x.outdir)
if __name__=="__main__":main()
