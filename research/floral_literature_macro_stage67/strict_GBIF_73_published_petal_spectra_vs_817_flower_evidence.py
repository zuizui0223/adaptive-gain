"""Stage67 ORIGINAL published 2024 flower-petal UV/visible spectra × 817 accepted evidence.

This pipeline reads only:
 - original 73 measured spectrometer petal columns Figshare 2024 (authenticated
   Stage67 Actions 44037008730), not color photographs;
 - original 817 unique strict accepted-key source evidence from Stage57
   Actions 44008957910 (mix of UV spatial 230, spectral 2015 207,
   quantitative 2025 243, positive-only colour-change literature).
Original names are matched via strict GBIF Plantae SPECIES EXACT >=95 only;
unresolved names remain unknown, not added. Spectrometer units from
2024 are % reflectance and are not comparable to 2025 0..1 proportions
without explicit /100 conversion. No native sampling cooccurrence.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,sys
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage49"))
from match_literature_visual_taxa_gbif import lookup

FIGSHARE_DOI="10.6084/m9.figshare.21081025.v2"
FIGSHARE_ORIGINAL_SHA="fa72932776f965115d789fa2b3dc5117491d03b6c2decf01aedfd625373cee96"
N_SPECTRA=73
N_ATLAS=817
N_ATLAS_DIRECT_UV=230

def check(x,reason):
    if not x:raise ValueError("STAGE67_ORIGINAL_PUBLIC_SPECTRA_CROSSWALK_NO_GO_"+reason)

def read(path):
    with Path(path).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def source_records(spectra,visual,source_receipt):
    check(len(spectra)==N_SPECTRA,"NOT_SEVENTY_THREE_ORIGINAL_FLORAL_SPECTRA")
    check(len(visual)==N_ATLAS,"NOT_EIGHT_HUNDRED_SEVENTEEN_ACCEPTED_SOURCE_KEYS")
    check(source_receipt.get("source_data_DOI")==FIGSHARE_DOI,
          "ORIGINAL_FIGSHARE_VERSION_DOI_WRONG")
    check(source_receipt["original_figshare"]["original_source_sha256"]==FIGSHARE_ORIGINAL_SHA,
          "FIGSHARE_SOURCE_ZIP_AUTHENTICITY")
    check(source_receipt["actual_source_petal_columns"]["n_source_columns_with_complete_UV_and_visible"]==73,
          "ORIGINAL_73_SOURCE_BOTH_BANDS_INCOMPLETE")
    names=[x["source_literal_species_candidate"] for x in spectra]
    check(len(set(names))==73,"DUPLICATE_ORIGINAL_SOURCE_SPECIES_COLUMN_LABEL")
    prior={x["gbif_accepted_species_key"]:x for x in visual}
    check(len(prior)==817 and all(k.isdigit() for k in prior),
          "VISUAL_ATLAS_817_ACCEPTED_NONUNIQUE")
    direct=sum(r["source_UV_pattern_directly_measured_or_unknown"] in ("0","1")
               for r in visual)
    check(direct==230,"ORIGINAL_DIRECT_UV_POSITIVE_NEGATIVE_GATE")
    clean=[]
    for s in spectra:
        check(s["flower_part"]=="petal" and
              s["UV_spatial_guide_status"]==
                 "NOT_OBSERVABLE_FROM_ONE_PETAL_MEAN_SPECTRUM",
              "MEASURED_PETAL_SPECTRUM_IS_NOT_GUIDE")
        check(s["source_measured_spectrum_status"]=="SPECTRUM_MEASURED_WITH_UV_AND_VIS",
              "ORIGINAL_SOURCE_SPECTRUM_NOT_COMPLETE")
        # Validate physical scale as originally published percentages.
        for col in ("UV_mean_reflectance_300_399_or_unknown",
                    "visible_mean_reflectance_400_700_or_unknown"):
            v=float(s[col])
            check(math.isfinite(v) and 0<=v<=100,"SOURCE_PERCENT_NOT_0_TO_100")
        check(s["source_literal_species_candidate"].count(" ")==1,
              "UNCERTAIN_SOURCE_SPECIES_NAME")
        clean.append(s)
    return names,prior

def attach(spectra,visual,source_receipt,taxonomy):
    names,prior=source_records(spectra,visual,source_receipt)
    check(set(taxonomy)==set(names),"GBIF_SOURCE_73_KEY_UNIVERSE_CHANGED")
    result=[]
    seen_keys=set()
    for s in spectra:
        name=s["source_literal_species_candidate"]
        t=taxonomy[name]
        status=t["taxonomy_status"]
        key=str(t.get("gbif_accepted_usage_key") or "")
        if status!="EXACT_CONFIDENT_SPECIES_MAPPED":
            key=""
        else:
            check(key.isdigit(),"GBIF_STRICT_ACCEPTED_KEY_INVALID")
        result.append({
           "original_2024_species_name":name,
           "original_2024_Figshare_DOI":FIGSHARE_DOI,
           "original_flower_organ":"petal",
           "source_2024_spectral_column":s["original_spectral_column_name"],
           "source_2024_spectral_file":s["original_source_spectral_member"],
           "gbif_accepted_species_key_or_unknown":key,
           "strict_taxonomic_status":status,
           "source_UV_300_399_mean_reflectance_original_percent":s[
                "UV_mean_reflectance_300_399_or_unknown"],
           "source_visible_400_700_mean_reflectance_original_percent":s[
                "visible_mean_reflectance_400_700_or_unknown"],
           "source_UV_300_399_mean_reflectance_fraction_if_needed":float(
               s["UV_mean_reflectance_300_399_or_unknown"])/100,
           "source_visible_400_700_mean_reflectance_fraction_if_needed":float(
               s["visible_mean_reflectance_400_700_or_unknown"])/100,
           "prior_817_atlas_accepted_taxon_overlap":bool(key and key in prior),
           "prior_direct_measured_spatial_UV_class_if_any":(
              prior[key]["source_UV_pattern_directly_measured_or_unknown"]
              if key in prior else ""),
           "UV_spatial_guide_present_or_absent":"NOT_MEASURED_IN_THIS_PETAL_SPECTRA_SOURCE",
           "same_source_native_occurrence_and_receiver_visits":"NOT_MEASURED",
           "same_study_evolved_VOC_scent_and_wind":"NOT_MEASURED"})
        if key:seen_keys.add(key)
    check(len(result)==73,"ORIGINAL_SOURCE_TAXON_ROWS_LOST")
    return result,{
      "schema":"published_shrestha2024_true73_petal_spectra_crosswalk_prior817_original_modalities",
      "source_2024_DOI":FIGSHARE_DOI,
      "original_2024_zip_sha256":FIGSHARE_ORIGINAL_SHA,
      "original_2024_spectrometer_measured_taxon_columns":73,
      "prior_817_accepted_source_modalities_union":817,
      "prior_230_directly_measured_UV_spatial_states":230,
      "matched_strict_accepted_species_rows":sum(bool(r["gbif_accepted_species_key_or_unknown"]) for r in result),
      "unique_matched_accepted_species":len(seen_keys),
      "not_strictly_resolved_source_names":sum(not r["gbif_accepted_species_key_or_unknown"] for r in result),
      "strict_cross_study_accepted_species_overlap":len(seen_keys&set(prior)),
      "new_2024_strict_accepted_species_not_in_prior":len(seen_keys-set(prior)),
      "union_accepted_evidence_species_not_all_guide_positive":len(seen_keys|set(prior)),
      "2024_spectral_sample_also_measured_UV_pattern_in_prior":sum(
           r["prior_direct_measured_spatial_UV_class_if_any"] in ("0","1") for r in result),
      "original_2024_accepted_taxonomy_status_counts":dict(sorted(
           Counter(r["strict_taxonomic_status"] for r in result).items())),
      "source_2024_spectral_average_units_percent_not_fraction":True,
      "source_2025_Oliveira_UV_average_units_proportion_0_to_1":True,
      "native_study_location_is_bayreuth_botanical_garden":True,
      "no_site_native_bee_bird_or_scent_spatial_guide_macro_effect":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-73-spectral-columns",required=True,type=Path)
    p.add_argument("--original-73-spectral-receipt",required=True,type=Path)
    p.add_argument("--prior-817-source-atlas",required=True,type=Path)
    p.add_argument("--outdir",type=Path,default=Path("stage67_source_73spectra_817atlas_species_taxonomy"))
    a=p.parse_args()
    spectra=read(a.original_73_spectral_columns)
    prior=read(a.prior_817_source_atlas)
    receipt=json.loads(a.original_73_spectral_receipt.read_text())
    names,_=source_records(spectra,prior,receipt)
    with ThreadPoolExecutor(max_workers=4) as pool:
        taxa=list(pool.map(lookup,names))
    result,summary=attach(spectra,prior,receipt,dict(zip(names,taxa)))
    a.outdir.mkdir(exist_ok=True,parents=True)
    with (a.outdir/"original_2024_73_petal_spectra_taxonomic_source_match_and_UV_modes.csv").open(
          "w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
    (a.outdir/"source_verified_73spectra_vs_817accepted_taxonomic_union.json").write_text(
       json.dumps(summary,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print("STAGE67_ORIGINAL_FIGSHARE73_VS_817_ACCEPTED_FLORAL_MODALITY_MATCH",
          json.dumps(summary,sort_keys=True))
    print("NO_FALSE_UV_PATTERN_NEGATIVE_NO_VOC_SCENT_OR_PHOTO_IN_SOURCE")
if __name__=="__main__":main()
