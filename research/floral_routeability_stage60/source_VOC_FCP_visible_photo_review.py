"""Stage60: original FCP 4475 photo opportunities × authored 305 VOC species.

Inputs independently source-verified:
Stage48 PR #128: original FCP 4475 species + licensed photo-attempt counts,
four-state broad color classifiability; NHM marking text leads NOT confirmed.
Stage59 original Farré-Armengol 305 scent species × GBIF accepted 817 source.
This exact original-binomial match is a REVIEW QUEUE, NOT observed visible
nectar-guide phenotype nor same-plant/same-locality VOC emission. No image
bytes or wildlife photography are rehosted and no unseen photos are labeled.
Wind source field still means pollination mode, NOT wind velocity.

A species-level discovery/audit split is frozen without looking at future
visual label; it is same-source FCP, NOT an independent external replication.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse,csv,hashlib,json
from pathlib import Path

FCP_EXPECTED=4475
VOC_EXPECTED=305
FCP_CLASSIFIABLE_MIN=40
SALT="stage60-original-VOC305-visible-photo-annotation-20261117"
FCP_COLUMNS=("inat_taxon_id","canonical_binomial_candidate",
             "n_original_photos_attempted",
             "n_fcp_four_coarse_colour_classifiable_photos",
             "actual_visible_guide_phenotype","actual_UV_guide_phenotype",
             "nhm_visible_marking_TEXT_candidate_or_missing")

def source_rows(path):
    with Path(path).open(newline="",encoding="utf8") as f:
        return list(csv.DictReader(f))

def planned_split(name):
    v=int(hashlib.sha256((SALT+"|"+name).encode("utf8")).hexdigest()[:12],16)
    return ("A_DISCOVERY_INTERNAL_ANNOTATION" if v%5<3
            else "B_INTERNAL_BLIND_CHECK_NOT_EXTERNAL_REPLICATION")

def join(fcp,voc):
    if len(fcp)!=FCP_EXPECTED or len(voc)!=VOC_EXPECTED:
        raise ValueError("NO_GO_SOURCE_FCP4475_OR_VOC305_DENOMINATOR")
    if any(not set(FCP_COLUMNS).issubset(x) for x in fcp):
        raise ValueError("NO_GO_SOURCE_FCP_COLUMN_SCHEMA_CHANGED")
    grouped=defaultdict(list)
    ids=set()
    for row in fcp:
        key=str(row["canonical_binomial_candidate"] or "").strip().casefold()
        if not row["inat_taxon_id"] or row["inat_taxon_id"] in ids:
            raise ValueError("NO_GO_ORIGINAL_FCP_TAXON_ID_DUPLICATED")
        ids.add(row["inat_taxon_id"])
        if key: grouped[key].append(row)
        if (row["actual_visible_guide_phenotype"]!="NOT_MEASURED_FROM_FCP_PHOTO" or
            row["actual_UV_guide_phenotype"]!="NOT_MEASURED_FROM_FCP_PHOTO"):
            raise ValueError("NO_GO_FCP_UNMEASURED_VISUAL_PHOTO_AS_TRUE_GUIDE")
    source_names=set()
    matches=[]
    ambiguous=Counter()
    for r in voc:
        original=r["source_species_canonical_binomial_if_valid"].strip()
        k=original.casefold()
        if original in source_names:
            raise ValueError("NO_GO_SOURCE_VOC_DUPLICATED_ORIGINAL_BINOMIAL")
        if original:source_names.add(original)
        if not original or k not in grouped:
            continue
        if len(grouped[k])!=1:
            ambiguous[k]=len(grouped[k])
            continue
        f=grouped[k][0]
        n=int(f["n_fcp_four_coarse_colour_classifiable_photos"])
        total=int(f["n_original_photos_attempted"])
        if not 0<=n<=total:
            raise ValueError("NO_GO_CLASSIFIABLE_GREATER_THAN_ORIGINAL_ATTEMPTS")
        has_mark=f["nhm_visible_marking_TEXT_candidate_or_missing"]
        if has_mark not in ("0","1",""):
            raise ValueError("NO_GO_TEXT_REVIEW_MARKING_STATUS")
        if r["GBIF_strict_taxonomy_status"]!="EXACT_CONFIDENT_SPECIES_MAPPED":
            original_tax="SOURCE_VOC_TAXON_NOT_STRICT_GBIF_ACCEPTED"
        else:
            original_tax="ACCEPTED_VOC_TAXON_ONLY_NOT_A_PHOTO_CLASSIFICATION"
        rank=("A_TEXT_MARKING_PLUS_40_OR_MORE_CLASSIFIABLE"
              if has_mark=="1" and n>=FCP_CLASSIFIABLE_MIN else
              "B_40_OR_MORE_CLASSIFIABLE"
              if n>=FCP_CLASSIFIABLE_MIN else
              "C_LOW_PHOTO_CLASSIFIABILITY_UNMEASURED_NOT_NEGATIVE")
        matches.append({
            "source_original_VOC_binomial":original,
            "source_original_VOC_GBIF_accepted_species_key":r["GBIF_strict_accepted_species_key_or_unknown"],
            "source_original_VOC_GBIF_match_status":original_tax,
            "source_original_VOC_positive_analyte_cells":r["source_VOC_positive_presence_columns_in_original_full_bouquet"],
            "source_original_VOC_wind_pollination_mode_1_else_unknown":r["source_wind_pollination_flag_yes_if_1_else_unknown"],
            "original_FCP_name_binomial":f["fcp_species_as_reported"],
            "original_FCP_inat_taxon_id":f["inat_taxon_id"],
            "original_FCP_photo_attempts":total,
            "original_FCP_coarse_colour_classifiable_photos":n,
            "NHM_unverified_visible_marking_text_candidate":has_mark,
            "precommitted_review_tier":rank,
            "source_level_internal_split_no_new_signal_labels":planned_split(original),
            "visible_intrapetal_guide_status":"NOT_YET_MEASURED_ON_AUTHENTIC_SOURCE_PHOTO",
            "UV_pattern_status_from_FCP_photo":"NOT_MEASURED_UV_WITH_RGB_PHOTO",
            "local_plant_VOC_and_photo_same_individual":"NOT_ESTABLISHED",
            "flower_wind_speed_from_VOC_pollination_mode":"NOT_MEASURED",
            "n_original_source_photo_bytes_rehosted":0,
        })
    matches.sort(key=lambda r:(r["precommitted_review_tier"],
                               -r["original_FCP_coarse_colour_classifiable_photos"],
                               r["source_original_VOC_binomial"]))
    original_uids={r["source_original_VOC_GBIF_accepted_species_key"] for r in matches if r["source_original_VOC_GBIF_accepted_species_key"]}
    return matches,{
      "status":"ORIGINAL_305_VOC_4475_FCP_VISUAL_PATTERN_REVIEW_OPPORTUNITY",
      "n_original_2020_VOC_species_source":len(voc),
      "n_original_FCP_image_opportunity_species":len(fcp),
      "n_exact_verbatim_binomial_VOC_FCP_join_candidates":len(matches),
      "n_ambiguous_FCP_canonical_join_keys_heldout":len(ambiguous),
      "n_unique_strict_accepted_VOC_species_in_FCP_review":len(original_uids),
      "n_species_classifiable_photo_ge_40":sum(x["original_FCP_coarse_colour_classifiable_photos"]>=FCP_CLASSIFIABLE_MIN for x in matches),
      "n_original_attempted_photos_for_matched_species":sum(x["original_FCP_photo_attempts"] for x in matches),
      "n_coarse_classifiable_photos_for_matched_species":sum(x["original_FCP_coarse_colour_classifiable_photos"] for x in matches),
      "n_unverified_NHM_marking_text_candidates":sum(x["NHM_unverified_visible_marking_text_candidate"]=="1" for x in matches),
      "n_NHM_text_candidates_with_40_photos":sum(x["NHM_unverified_visible_marking_text_candidate"]=="1" and x["original_FCP_coarse_colour_classifiable_photos"]>=40 for x in matches),
      "n_wind_pollinated_source_VOC_photo_matches_NOT_wind_speed":sum(x["source_original_VOC_wind_pollination_mode_1_else_unknown"]=="1" for x in matches),
      "review_priority_counts":dict(sorted(Counter(x["precommitted_review_tier"] for x in matches).items())),
      "internal_annotation_split_counts":dict(sorted(Counter(x["source_level_internal_split_no_new_signal_labels"] for x in matches).items())),
      "source_original_photo_species_exact_spelling_not_accepted_taxonomy_reconciliation":True,
      "all_visible_UV_pattern_status_unknown_not_negative":True,
      "no_original_RGB_UV_spectroscopy_inferred":True,
      "no_VOC_and_RBG_source_same_individual_inference":True,
      "source_wind_is_pollination_not_wind_m_s":True,
      "this_is_a_frozen_review_target_not_morphology_measured":True,
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--original-fcp4475-queue",required=True)
    parser.add_argument("--original-voc305-accepted",required=True)
    a=parser.parse_args()
    rows,receipt=join(source_rows(a.original_fcp4475_queue),
                      source_rows(a.original_voc305_accepted))
    p=Path("stage60_source_VOC305_FCP4475_visible_review")
    p.mkdir(exist_ok=True)
    with (p/"80_original_VOC_flower_photo_species_visible_guide_source_review_queue.csv").open(
         "w",newline="",encoding="utf8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    (p/"source_VOC_FCP_photo_review_80_receipt.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf8")
    print("STAGE60_ORIGINAL_VOC305_FCP4475_JOINT_PHOTO_REVIEW_FEASIBILITY",
          json.dumps(receipt,sort_keys=True,ensure_ascii=False))
    print("NO_UNREAD_IMAGES_OR_UV_GUIDES_LABELED_NO_CAUSAL_WIND_SENSORY_GUILD_EFFECT")

if __name__=="__main__":
    main()
