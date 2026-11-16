"""Stage54: accepted-key evidence matrix combining ORIGINAL UV, Ohashi spectra and 2025 review.

Input is three separate source-authenticated CI artifacts. The original
2025 literature review extraction is PARTIAL: 136 font-identified
columns, 124 accepted species (published study says 151), not a complete
catalogue. Original Ohashi 2015 219 folders map to 207 accepted species,
but not per-species bee/fruit-fly/butterfly age-colour discriminability.
Original 2016/2021 direct measured UV pattern outcomes from 262 accepted
plants provide binary information for 230 (101 pattern,129 uniform).
Avoid sum of overlapping species and avoid fake biological zeros.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse,csv,json
from pathlib import Path

SOURCE_UV=262
SOURCE_OHASHI=219
SOURCE_REVIEW=136


def _read(path):
    with Path(path).open(encoding="utf8",newline="") as f:
        return list(csv.DictReader(f))


def combine(uv,ohashi,review):
    if (len(uv),len(ohashi),len(review))!=(SOURCE_UV,SOURCE_OHASHI,SOURCE_REVIEW):
        raise ValueError("NO_GO_ORIGINAL_MODALITY_SOURCE_DENOMINATOR_CHANGED")
    byid={}
    for row in uv:
        key=row.get("gbif_accepted_species_key","")
        if not key.isdigit() or key in byid:
            raise ValueError("NO_GO_AUTHENTIC_UV262_GBIF_KEY_DUPLICATE")
        state=row.get("source_measured_UV_spatial_pattern_or_missing")
        if state not in ("0","1",""):
            raise ValueError("NO_GO_DIRECT_UV_STATE_OUTSIDE_MEASURED_OR_UNKNOWN")
        byid[key]={
           "gbif_accepted_species_key":key,
           "direct_UV_2016_2021_pattern_or_missing":state,
           "source_original_direct_UV_studies":row.get("source_study_DOIs",""),
           "original_Ohashi_2015_age_reflectance_archive":False,
           "n_original_Ohashi_taxon_variety_directories":0,
           "original_2025_colour_change_literature_reviewed":False,
           "n_original_2025_review_taxon_columns":0,
           "Ohashi_bee_perceptible_age_colour_change":"NOT_CLASSIFIED_FROM_ORIGINAL_SPECTRA_DIRECTORY",
           "review_colour_change_not_original_direct_functional_measurement":True,
           "phenotyped_locality_and_native_receiver_cooccurrence":"NOT_VERIFIED",
           "no_all_modality_signal_absence_inferred":True,
        }
    seen_Ohashi=set()
    for row in ohashi:
        key=row.get("gbif_accepted_species_key_or_missing","")
        if not key:continue
        if not key.isdigit() or row.get("gbif_name_taxonomic_mapping_status")!="EXACT_CONFIDENT_SPECIES_MAPPED":
            raise ValueError("NO_GO_OHASHI_SOURCE_ACCEPTED_SPECIES_KEY_MISMATCH")
        seen_Ohashi.add(key)
        if key not in byid:
            byid[key]={
                "gbif_accepted_species_key":key,
                "direct_UV_2016_2021_pattern_or_missing":"",
                "source_original_direct_UV_studies":"",
                "original_Ohashi_2015_age_reflectance_archive":False,
                "n_original_Ohashi_taxon_variety_directories":0,
                "original_2025_colour_change_literature_reviewed":False,
                "n_original_2025_review_taxon_columns":0,
                "Ohashi_bee_perceptible_age_colour_change":"NOT_CLASSIFIED_FROM_ORIGINAL_SPECTRA_DIRECTORY",
                "review_colour_change_not_original_direct_functional_measurement":True,
                "phenotyped_locality_and_native_receiver_cooccurrence":"NOT_VERIFIED",
                "no_all_modality_signal_absence_inferred":True,
            }
        byid[key]["original_Ohashi_2015_age_reflectance_archive"]=True
        byid[key]["n_original_Ohashi_taxon_variety_directories"]+=1
    seen_review=set()
    for row in review:
        key=row.get("gbif_accepted_key_or_unresolved","")
        if not key:continue
        if not key.isdigit() or row.get("gbif_exact_species_match_status")!="EXACT_CONFIDENT_SPECIES_MAPPED":
            raise ValueError("NO_GO_REVIEW_ACCEPTED_SPECIES_KEY_STATUS")
        seen_review.add(key)
        if key not in byid:
            byid[key]={
                "gbif_accepted_species_key":key,
                "direct_UV_2016_2021_pattern_or_missing":"",
                "source_original_direct_UV_studies":"",
                "original_Ohashi_2015_age_reflectance_archive":False,
                "n_original_Ohashi_taxon_variety_directories":0,
                "original_2025_colour_change_literature_reviewed":False,
                "n_original_2025_review_taxon_columns":0,
                "Ohashi_bee_perceptible_age_colour_change":"NOT_CLASSIFIED_FROM_ORIGINAL_SPECTRA_DIRECTORY",
                "review_colour_change_not_original_direct_functional_measurement":True,
                "phenotyped_locality_and_native_receiver_cooccurrence":"NOT_VERIFIED",
                "no_all_modality_signal_absence_inferred":True,
            }
        byid[key]["original_2025_colour_change_literature_reviewed"]=True
        byid[key]["n_original_2025_review_taxon_columns"]+=1
    out=sorted(byid.values(),key=lambda x:int(x["gbif_accepted_species_key"]))
    u=set(k for k in byid if byid[k]["source_original_direct_UV_studies"])
    if len(u)!=SOURCE_UV:
        raise ValueError("NO_GO_UV_SOURCE_ACCEPTED_KEY_LOST")
    if len(seen_Ohashi)!=207 or len(seen_review)!=124:
        raise ValueError("NO_GO_AUTHENTIC_OHASHI_OR_REVIEW_ACCEPTED_COUNT_CHANGED")
    if sum(x["direct_UV_2016_2021_pattern_or_missing"]=="1" for x in out)!=101 or (
       sum(x["direct_UV_2016_2021_pattern_or_missing"]=="0" for x in out)!=129):
        raise ValueError("NO_GO_AUTHENTIC_DIRECT_UV_PATTERN_COUNTS_LOST")
    return out,{
      "status":"SOURCE_VERIFIED_GBIF_ACCEPTED_MULTIMODAL_FLORAL_VISUAL_INFORMATION_ATLAS",
      "original_direct_UV_2016_2021_plus_temporal_only_accepted_species":len(u),
      "direct_original_measured_UV_spatial_patterned_species":101,
      "direct_original_measured_UV_uniform_species":129,
      "original_Ohashi_2015_spectral_taxon_variety_directories":len(ohashi),
      "original_Ohashi_2015_spectral_unique_accepted_species":len(seen_Ohashi),
      "original_2025_review_source_extracted_taxon_columns_partial":len(review),
      "original_2025_review_unique_accepted_species_partial":len(seen_review),
      "n_total_unique_accepted_species_all_3_modalities":len(out),
      "n_accepted_species_in_all_3_sources":len(u&seen_Ohashi&seen_review),
      "overlap_UV_Ohashi":len(u&seen_Ohashi),
      "overlap_UV_review":len(u&seen_review),
      "overlap_Ohashi_review":len(seen_Ohashi&seen_review),
      "n_UV_only":len(u-seen_Ohashi-seen_review),
      "n_Ohashi_only":len(seen_Ohashi-u-seen_review),
      "n_review_only":len(seen_review-u-seen_Ohashi),
      "n_source_review_151_not_exhaustively_recovered":151-len(review),
      "original_review_positive_only_no_nonchanging_negative_comparators":True,
      "source_spectra_directory_not_2015_pollinator_perceptible_positive_status":True,
      "original_2016_UV_uniform_not_entire_visual_signal_absence":True,
      "no_native_local_Bombus_contrast_or_wind_biology_fitted":True,
    }


def main():
    ap=argparse.ArgumentParser()
    for name in ("UV262","Ohashi219","review2025"):
        ap.add_argument("--"+name,required=True)
    opts=ap.parse_args()
    out,report=combine(_read(opts.UV262),_read(opts.Ohashi219),_read(opts.review2025))
    dest=Path("stage54_multimodal_accepted_species")
    dest.mkdir(exist_ok=True)
    with (dest/"original_UV_Ohashi_age_spectra_2025_review_GBIF_accepted_species.csv").open(
          "w",encoding="utf8",newline="") as fp:
        w=csv.DictWriter(fp,fieldnames=list(out[0]))
        w.writeheader();w.writerows(out)
    (dest/"source_multimodal_accepted_species_count_receipt.json").write_text(
         json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("STAGE54_ACTUAL_ACCEPTED_SPECIES_TOTAL_ALL_VISUAL_MODALITIES",json.dumps(report,sort_keys=True))
    print("NO_ILLUSORY_ABSENT_SIGNAL_OR_BOMBUS_WIND_FIT")

if __name__=="__main__":
    main()
