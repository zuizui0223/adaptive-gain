"""Stage90C: Is the apparent wind-pollinated floral hue gradient spread
across independent source botanical lineages, or is its source support
concentrated in Poaceae, Cyperaceae and Juncaceae?

All true source data are author-verified:
 GIFT3.2 independently classified source species 5770 qualified
 NHM 59369 original botanical floral text labels
 Kew WCVP 55775 accepted source native species×367 TDWG regions
 Stage87C 1970–2000 WorldClim source 367 regions climate + GIS.
The source 55,775 native-species universe and Stage89 155 common animal/
wind source-hue regions are held fixed. Original species without a
documented hue are not assigned a negative floral colour. Without 10
source one-hue wind-mode plants in an original region after a family
exclusion, the source region cannot support the previous comparison.

Excluding families is a lineage/sampling sensitivity, not asserting that
all members have the same ecological pollination mechanism. No true
phylogenetic independent transitions, field pollination fitness, landing,
odor plume, gust, or sensor learning is inferred.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,sys,zipfile
from pathlib import Path
from collections import Counter,defaultdict

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage87"))
sys.path.insert(0,str(BASE/"floral_macro_stage88"))
sys.path.insert(0,str(BASE/"floral_macro_stage89"))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions
from source_taxonomic_family_exclusion_native_flora import (
    source_families,GRAMINOID,OTHER_WIND_ENRICHED
)
from gift32_independent_pollen_mode_global_native_coverage import original_gift_species

CLIMATE_SOURCE_SHA="4c0ab25596078be4b2aa35a254e42695fd260e1720864e173970aac8aa7db83a"
CLIMATE_MEMBER="stage87_original_global_TDWG3_NHM_WCVP_WorldClim_regions.csv"
CONDITIONS={
 "all_source_wind_mode":set(),
 "exclude_Poaceae":set(("Poaceae",)),
 "exclude_Cyperaceae":set(("Cyperaceae",)),
 "exclude_Juncaceae":set(("Juncaceae",)),
 "exclude_all_three_graminoid_families":GRAMINOID,
 "exclude_graminoid_and_nine_wind_enriched_families":
    GRAMINOID|OTHER_WIND_ENRICHED,
}

def verified_climate_regions(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=CLIMATE_SOURCE_SHA:
        raise ValueError("STAGE90C_ORIGINAL_WORLDCLIM_NATIVE_367_SOURCE_SHA_MISMATCH")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        rows=list(csv.DictReader(io.StringIO(z.read(CLIMATE_MEMBER).decode("utf-8-sig"))))
    if len(rows)!=367 or len(set(x["TDWG_L3"] for x in rows))!=367:
        raise ValueError("STAGE90C_WORLDCLIM_NATIVE_367_TDWG_FRAME_CHANGED")
    return {r["TDWG_L3"]:r for r in rows}

def source_analysis(gift_zip,nhm_path,wcvp_zip,climate_zip,outdir):
    mode,_=original_gift_species(gift_zip)
    trait,nhm_qc=load_nhm(nhm_path)
    regions,wcvp_qc=wcvp_regions(wcvp_zip,trait)
    family,family_qc=source_families(wcvp_zip,trait)
    climate=verified_climate_regions(climate_zip)
    mode_matched={s for reg in regions.values() for s in reg if s in mode}
    if len(mode_matched)!=3172:raise ValueError("STAGE90C_REAL_SOURCE_GIFT_NATIVE_3172_CHANGED")
    all_wind_hue={s for s in mode_matched if mode[s]=="wind" and
                  trait[s]["explicit_single_hue"] is not None}
    all_animal_hue={s for s in mode_matched if mode[s]=="animal" and
                    trait[s]["explicit_single_hue"] is not None}
    if len(all_wind_hue)!=57 or len(all_animal_hue)!=598:
        raise ValueError("STAGE90C_SOURCE_57_WIND_598_ANIMAL_TRUE_HUE_CHANGED")
    family_wind=Counter(family.get(s,"SOURCE_FAMILY_UNAVAILABLE") for s in all_wind_hue)
    family_animal=Counter(family.get(s,"SOURCE_FAMILY_UNAVAILABLE") for s in all_animal_hue)
    wind_by_hue=defaultdict(Counter)
    genera_by_family=defaultdict(set)
    for s in all_wind_hue:
        ff=family.get(s,"SOURCE_FAMILY_UNAVAILABLE")
        wind_by_hue[ff][trait[s]["explicit_single_hue"]]+=1
        genera_by_family[ff].add(s.split()[0])
    rows=[]
    base_regions=[]
    for code,source_plants in sorted(regions.items()):
        animal={s for s in source_plants if s in all_animal_hue}
        wind={s for s in source_plants if s in all_wind_hue}
        cl=climate.get(code)
        if not cl:raise ValueError("STAGE90C_Kew_NATIVE_REGION_NOT_WORLDCLIM")
        complete=(cl["source_all_5climate_variables_at_12_or_more_points"]=="1" and
              cl["source_original_TDWG_polygon_geometry_repaired_sensitivity"]=="0")
        common=complete and len(animal)>=10 and len(wind)>=10
        if common:base_regions.append(code)
        for cond,excluded in CONDITIONS.items():
            kept={s for s in wind if family.get(s) not in excluded}
            rows.append({
             "TDWG_L3":code,
             "source_condition":cond,
             "original_same_155_region_eligible_before_lineage_exclusion":int(common),
             "source_original_GIFT_animal_one_hue_taxa":len(animal),
             "source_original_GIFT_wind_one_hue_taxa":len(wind),
             "source_remaining_wind_one_hue_taxa":len(kept),
             "source_remaining_wind_one_hue_genera":len({s.split()[0] for s in kept}),
             "source_remaining_wind_one_hue_families":len({family.get(s) for s in kept}),
             "source_animal_and_wind_mode_minimum10_after_exclusion":int(
                 complete and len(animal)>=10 and len(kept)>=10),
             "source_original_source_anemophily_at_site_NOT_directly_measured":True})
    if len(base_regions)!=155:
        raise ValueError("STAGE90C_ORIGINAL_SAME_155_REGION_SOURCE_COHORT_DRIFT_"+str(len(base_regions)))
    if len(rows)!=367*len(CONDITIONS):
        raise ValueError("STAGE90C_MISSING_ORIGINAL_SOURCE_FAMILY_ABLATION_ROWS")
    summary={}
    for cond in CONDITIONS:
        one=[x for x in rows if x["source_condition"]==cond]
        first=[x for x in one if x["original_same_155_region_eligible_before_lineage_exclusion"]==1]
        retained={s for s in all_wind_hue if family.get(s) not in CONDITIONS[cond]}
        summary[cond]={
           "original_all_367_TDWG_regions_wind_ge10":sum(x["source_remaining_wind_one_hue_taxa"]>=10 for x in one),
           "original_common_155_TDWG_regions_still_wind_ge10":sum(x["source_remaining_wind_one_hue_taxa"]>=10 for x in first),
           "original_common_155_TDWG_regions_still_both_mode_ge10":sum(x["source_animal_and_wind_mode_minimum10_after_exclusion"] for x in first),
           "remaining_unique_source_wind_one_hue_species":len(retained),
           "remaining_source_wind_one_hue_unique_genera":len({s.split()[0] for s in retained}),
           "remaining_source_wind_one_hue_unique_families":len({family.get(s) for s in retained}),
           "source_unqualified_regions_not_biological_absence":True}
    outdir.mkdir(exist_ok=True,parents=True)
    with (outdir/"stage90_original_wind_flora_family_155_common_region_source_support.csv").open(
         "w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    receipt={
      "schema":"stage90C_original_GIFT_native_WCVP_WIND_mode_floral_lineage_family_spatial_support",
      "original_source_GIFT_modes_qualifying_NHM_WCVP_native":len(mode_matched),
      "original_source_55775_plant_native_WCVP_species":len(set().union(*regions.values())),
      "source_native_TDWG3_all_regions":len(regions),
      "source_exact_same_Stage89_original_global_common_regions":len(base_regions),
      "source_unique_animal_one_hue_taxa":len(all_animal_hue),
      "source_unique_wind_one_hue_taxa":len(all_wind_hue),
      "source_unique_wind_one_hue_taxa_by_family":dict(family_wind),
      "source_unique_animal_one_hue_taxa_by_family":dict(family_animal),
      "source_unique_wind_one_hue_genera_by_family":{
          f:len(genera_by_family[f]) for f in sorted(genera_by_family)},
      "source_unique_wind_one_hue_lexical_hue_by_family":{
          f:dict(v) for f,v in wind_by_hue.items()},
      "source_original_lineage_source_coverage_per_family_exclusion":summary,
      "source_original_sources_sha_verified_by_imported_handlers":True,
      "source_mode_classification_not_local_observation_of_pollen_vector":True,
      "source_family_exclusion_not_actual_trait_mode_intervention":True,
      "source_zero_documented_hue_not_truly_zero_plant_occurrences":True,
      "source_worldclim_1970_2000_not_actual_field_wind_gust":True,
      "source_this_does_not_prove_evolutionary_phylogenetic_nonindependence_corrected":True,
      "source_no_original_Bombus_choice_learning_visual_olfaction_landing_measurement":True}
    (outdir/"stage90_original_GIFT_wind_flora_family_support_receipt.json").write_text(
        json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("STAGE90C_TRUE_NATIVE_GIFT_57_WIND_ONE_HUE_TAXA_LINEAGE_SUPPORT",json.dumps({
      "source_unique_57_wind_taxa_by_family":dict(family_wind),
      "source_conditions":summary},sort_keys=True),flush=True)
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--GIFT-original-artifact",type=Path,required=True)
    p.add_argument("--NHM-original",type=Path,required=True)
    p.add_argument("--WCVP-original",type=Path,required=True)
    p.add_argument("--WorldClim-source-artifact",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();source_analysis(a.GIFT_original_artifact,a.NHM_original,
        a.WCVP_original,a.WorldClim_source_artifact,a.outdir)
if __name__=="__main__":main()
