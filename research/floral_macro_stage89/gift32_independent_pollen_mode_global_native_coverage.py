"""Stage89A: 5,771 original GIFT v3.2 species pollination modes × global floras.

True original public GIFT v3.2 API source, retrieved and taxonomically audited
on 2026-09-14 by independent source-replay in zuizui0223/island:
 GitHub Actions run 34803493307, artifact ID 10332810251, artifact SHA256
 074a52323ba835201043a3a5980cc2b2d0ff79878e83bc9be19511ae83a1c0e8.
 The artifact contains ORIGINAL-SOURCE-DERIVED accepted species mode assignments
 after exclusion of mismatched taxonomy, bias-derived/derived traits,
 restricted references, mixed and conflicting pollination labels.
 GIFT raw 14,122 public source rows, 23 reference × trait pairs; original
 GIFT 3.2 version stable; 5,771 unambiguous species modes biotic=4538 wind=1233.

No interpolation of source modes from taxonomic genus/family, flower colour,
local community, lack of visits, nectar guides or bee cognition. GIFT mode
may be literature compiled, not direct field ecology; no source original
habitat/population adaptive cue-order claim is made.

Scientific goal: test if independently classified source pollination modes
have enough geographic/support overlap with original NHM 59,369 floral
description species and the 55,775 WCVP accepted native species across
367 TDWG level-3 regions. Controls for source mode ascertainment needed
before any animal-vs-wind regional effect is attempted.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,gzip,zipfile,sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage87"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage88"))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions,strict_name
from global_native_pollination_mode_tdwg3 import recompute_global,write_csv

SOURCE_ARTIFACT_SHA="074a52323ba835201043a3a5980cc2b2d0ff79878e83bc9be19511ae83a1c0e8"
ORIGINAL_GIFT_RUN=34803493307
ORIGINAL_GIFT_ARTIFACT=10332810251
MEMBER="h5c-qualification/h5c_independent_pollination_mode_species.csv.gz"
MANIFEST="h5c-gift/gift_fetch_manifest.json"
EXPECTED="2026-09-14"
SOURCE_MODE={"biotic":"animal","abiotic_wind":"wind"}

def original_gift_species(source_zip):
    raw=Path(source_zip).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_ARTIFACT_SHA:
        raise ValueError("STAGE89_ORIGINAL_GIFT32_INDEPENDENT_ARCHIVE_SHA_CHANGED")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if MEMBER not in z.namelist() or MANIFEST not in z.namelist():
            raise ValueError("STAGE89_GIFT32_ORIGINAL_H5C_SOURCE_MEMBERS_MISSING")
        metadata=json.loads(z.read(MANIFEST))
        table=gzip.decompress(z.read(MEMBER)).decode("utf-8-sig")
    if (metadata.get("gift_version")!="3.2" or
        metadata.get("n_raw_api_rows")!=14122 or
        metadata.get("n_public_unbiased_reference_trait_pairs_fetched")!=23 or
        metadata.get("prepared_species_by_trait",{}).get("pollen_vector_mode")!=5875):
        raise ValueError("STAGE89_ORIGINAL_GIFT32_API_PROVENANCE_NOT_FROZEN")
    counts=Counter();out={};unknown=[];bad_name=0
    for row in csv.DictReader(io.StringIO(table)):
        counts["source_original_gift_qualified_rows"]+=1
        name=strict_name(row.get("accepted_species"))
        code=str(row.get("pollen_vector_mode") or "").strip()
        mode=SOURCE_MODE.get(code)
        if not name:
            bad_name+=1;continue
        if mode is None:unknown.append((name,code));continue
        if name in out:raise ValueError("STAGE89_SOURCE_GIFT_QUALIFIED_DUPLICATE_SPECIES")
        out[name]=mode
        counts["source_mode_"+mode]+=1
    if counts["source_original_gift_qualified_rows"]!=5771 or
        counts["source_mode_animal"]!=4538 or counts["source_mode_wind"]!=1233 or
        len(out)!=5771 or bad_name or unknown:
        raise ValueError("STAGE89_GIFT32_TRUE_4538_1233_SOURCE_MODE_SCOPE_DRIFT")
    if metadata.get("n_prepared_species")!=8635:
        raise ValueError("STAGE89_GIFT32_REAL_SOURCE_NUMBER_OF_TAXA_CHANGED")
    return out,{
      "archive_sha256":SOURCE_ARTIFACT_SHA,
      "original_source_repo":"zuizui0223/island",
      "original_actions_run_id":ORIGINAL_GIFT_RUN,
      "original_derived_artifact_id":ORIGINAL_GIFT_ARTIFACT,
      "original_source_retrieved_at_utc":metadata.get("retrieved_at_utc"),
      "source_original_GIFT_version":metadata.get("gift_version"),
      "original_raw_api_source_rows":metadata["n_raw_api_rows"],
      "original_gift_public_reference_trait_pairs":metadata["n_public_unbiased_reference_trait_pairs_fetched"],
      "original_species_modes_declared":dict(counts),
      "original_source_conflicts_mixed_and_taxonomy_filtered_by_island_h5c":True,
      "source_original_compilation_not_direct_mode_local_field_observation":True,
      "source_missing_modes_remain_UNKNOWN_not_wind":True,
    }

def run(gift_zip,nhm_file,wcvp_zip,outdir):
    modes,source=original_gift_species(gift_zip)
    traits,source_nhm=load_nhm(nhm_file)
    native,source_wcvp=wcvp_regions(wcvp_zip,traits)
    rows,original=recompute_global(traits,native,modes,{s:"GIFT_original_direct_reference" for s in modes})
    original["schema"]="stage89_original_GIFT3_2_5771_plant_pollination_modes_WCVP_global_TDWG3"
    original["source_original_Wang2025_source_mode_strict_matched_species_gift_external"] = original.pop(
        "source_original_Wang2025_source_mode_strict_matched_species")
    original["source_original_Wang2025_exact_species_animal_vs_wind_counts_gift_external"] = original.pop(
        "source_original_Wang2025_exact_species_animal_vs_wind_counts")
    original["source_GIFT_public_only_original_source_mapping_not_Wang2025"]=True
    original["source_original_no_5771_true_local_pollination_modes_at_WCVP_sites"]=True
    native_species=set().union(*native.values())
    confirmed_mode=set(modes)&native_species
    source_regional_wind_support={
        "wind_exact_matched_native_taxa":sum(modes[s]=="wind" for s in confirmed_mode),
        "animal_exact_matched_native_taxa":sum(modes[s]=="animal" for s in confirmed_mode),
        "unknown_native_taxa":len(native_species)-len(confirmed_mode),
        "n_gift_qualified_taxa_not_exact_WCVP_NHM":len(modes)-len(confirmed_mode)}
    if len(native)!=367 or len(native_species)!=55775:
        raise ValueError("STAGE89_WCVP_ORIGINAL_GLOBAL_NATIVE_FLORA_CHANGED")
    outdir.mkdir(parents=True,exist_ok=True)
    write_csv(outdir/"stage89_original_GIFT32_native_animal_wind_unknown_367_TDWG3_hues.csv",rows)
    receipt={"schema":"stage89_original_GIFT3_2_global_pollen_mode_source_admission",
       "source_original_GIFT32":source,
       "source_original_WCVP":source_wcvp,
       "source_original_NHM":source_nhm,
       "source_global_GIFT_pollination_mode_native_join":original,
       "source_mapped_original_species_coverage":source_regional_wind_support,
       "source_not_confirmatory_pollinator_information_order_selection":True,
       "source_not_a_global_random_angiosperm_sample":True,
       "source_compiled_modes_without_true_field_population_observation":True,
       "source_origin_region_membership_not_actual_plant_at_GBIF_site":True,
       "source_unrecorded_pollinator_absence_and_pollination_mode_are_unknown":True}
    (outdir/"stage89_original_GIFT32_NHM_WCVP_global_plant_mode_spatial_support.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE89_TRUE_INDEPENDENT_GIFT_POLLEN_MODE_WCVP_NATIVE_SOURCE",
        json.dumps({"actual_matched_modes":source_regional_wind_support,
        "source_mode_region_coverage":original["source_spatial_mode_composition_coverage"]},sort_keys=True))
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-GIFT32-island-original-artifact",type=Path,required=True)
    p.add_argument("--source-original-NHM",type=Path,required=True)
    p.add_argument("--source-original-Kew-WCVP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.source_GIFT32_island_original_artifact,
        a.source_original_NHM,a.source_original_Kew_WCVP,a.outdir)
if __name__=="__main__":main()
