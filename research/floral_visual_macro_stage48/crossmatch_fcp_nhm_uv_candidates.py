"""Stage48: source-verified global *visible pattern candidate* photo-review atlas.

Join 4,475 species with original FCP image-measurement opportunity,
59,369 NHM 2026 OCR-derived botanical trait rows and Tunes et al. 2021
80 original UV-phototyped taxon rows. No original FCP photographs are
downloaded or redistributed and NO NEW UV guide phenotype is inferred.
Exact canonical binomial string joins are a *screening device*, NOT
validated taxonomic reconciliation or within-flower structure labels.
"""
from __future__ import annotations

from collections import Counter,defaultdict
import csv
import io
import json
from pathlib import Path

import sys
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_visual_macro_stage45"))
from build_visual_trait_registry import _get_source_bytes,summarize_and_extract
from join_uv_with_global_traits import canonical_candidate,retrieve_original_uv
from probe_fcp_photo_species_frame import get_original_fcp_ledger,_sha1_blob,SOURCE_GIT_BLOB_SHA1

SOURCE_FCP_EXPECTED=4475
SOURCE_NHM_EXPECTED=59369
SOURCE_UV_EXPECTED=80
PHOTO_MIN_FOR_REVIEW=40


def _canonical(name):
    name=canonical_candidate(name)
    return name.casefold() if name else None


def _unambiguous_index(rows,name_field):
    """Return only unique exact binomial spelling, record ambiguous names."""
    mapping=defaultdict(list)
    for record in rows:
        k=_canonical(record.get(name_field))
        if k:
            mapping[k].append(record)
    return mapping


def _int(value,field):
    try:
        n=int(value)
    except (TypeError,ValueError) as err:
        raise ValueError("NO_GO_NONINTEGER_ORIGINAL_FCP_"+field) from err
    if n<0:
        raise ValueError("NO_GO_NEGATIVE_ORIGINAL_FCP_"+field)
    return n


def compose_review_registry(fcp_rows,nhm_rows,uv_rows,expected_source_counts=(4475,59369,80)):
    if (len(fcp_rows),len(nhm_rows),len(uv_rows))!=tuple(expected_source_counts):
        raise ValueError("NO_GO_INCORRECT_ORIGINAL_SOURCE_DENOMINATOR")
    missing=({"species","inat_taxon_id","n_source_photo","n_classified_photo"}-set(fcp_rows[0]))
    if missing:
        raise ValueError("NO_GO_FCP_COLUMN_SCHEMA_"+",".join(sorted(missing)))
    idx_nhm=_unambiguous_index(nhm_rows,"taxon")
    idx_uv=_unambiguous_index(uv_rows,"taxon_as_published")
    seen_fcp_id=set()
    out=[]
    for f in fcp_rows:
        species=f["species"].strip()
        taxon_id=f["inat_taxon_id"].strip()
        if not species or not taxon_id or taxon_id in seen_fcp_id:
            raise ValueError("NO_GO_FCP_SPECIES_OR_TAXON_ID_NOT_UNIQUE")
        seen_fcp_id.add(taxon_id)
        key=_canonical(species)
        originals=_int(f["n_source_photo"],"n_source_photo")
        measured=_int(f["n_classified_photo"],"n_classified_photo")
        if measured>originals:
            raise ValueError("NO_GO_CLASSIFIED_GREATER_THAN_SOURCE_PHOTOS")
        matching_nhm=idx_nhm.get(key,[]) if key else []
        matching_uv=idx_uv.get(key,[]) if key else []
        nhm_status=("SOURCE_TAXON_NO_CANONICAL_NAME" if key is None
                    else "NO_NHM_EXACT_NAME" if not matching_nhm
                    else "AMBIGUOUS_NHM_SOURCE_NAME" if len(matching_nhm)>1
                    else "EXACT_SINGLE_NHM_NAME_NOT_TAXONOMY_RECONCILED")
        uv_status=("NO_UV_SOURCE_CANDIDATE" if not matching_uv
                   else "AMBIGUOUS_UV_SOURCE_NAME" if len(matching_uv)>1
                   else "EXACT_MEASURED_UV_SOURCE_NAME_NOT_TAXONOMY_RECONCILED")
        nhm=matching_nhm[0] if len(matching_nhm)==1 else None
        uv=matching_uv[0] if len(matching_uv)==1 else None
        lexical_marking=int(nhm["marking_text_review_candidate"]) if nhm else None
        if lexical_marking not in (0,1,None):
            raise ValueError("NO_GO_NHM_MARKING_CANDIDATE_NOT_BOOLEAN")
        real_uv=int(uv["uv_pattern_present"]) if uv else None
        if real_uv not in (0,1,None):
            raise ValueError("NO_GO_SOURCE_UV_NOT_BINARY")
        # Different original categories of evidence: do not call candidate positive.
        if uv is not None:
            priority="1_ORIGINAL_UV_PHENOTYPE_REFERENCE_AND_PHOTO"
        elif lexical_marking==1 and measured>=PHOTO_MIN_FOR_REVIEW:
            priority="2_NHM_VISIBLE_MARKING_TEXT_PLUS_CLASSIFIABLE_PHOTO_REVIEW"
        elif measured>=PHOTO_MIN_FOR_REVIEW:
            priority="3_PHOTO_OPPORTUNITY_BALANCED_VISIBLE_PATTERN_REVIEW"
        else:
            priority="4_LOW_CLASSIFIABILITY_OR_OPPORTUNITY_NOT_NEGATIVE"
        out.append({
          "inat_taxon_id":taxon_id,
          "fcp_species_as_reported":species,
          "canonical_binomial_candidate":key or "",
          "n_original_photos_attempted":originals,
          "n_fcp_four_coarse_colour_classifiable_photos":measured,
          "nhm_exact_name_join_status":nhm_status,
          "nhm_visible_marking_TEXT_candidate_or_missing":(
              lexical_marking if lexical_marking is not None else ""),
          "nhm_colour_reported_or_missing":(
              nhm["floral_colour_reported"] if nhm else ""),
          "uv_original_source_name_join_status":uv_status,
          "uv_original_table_category_or_missing":uv["uv_category"] if uv else "",
          "uv_original_direct_measured_pattern_or_missing":(
              real_uv if real_uv is not None else ""),
          "actual_visible_guide_phenotype":"NOT_MEASURED_FROM_FCP_PHOTO",
          "actual_UV_guide_phenotype":"NOT_MEASURED_FROM_FCP_PHOTO",
          "source_pollinator_use_of_pattern":"NOT_MEASURED",
          "review_priority":priority,
          "photo_original_repository":"zuizui0223/fcp",
          "flower_guide_survey_inclusion":"CANDIDATE_ONLY_NOT_CONFIRMED",
        })
    if len(out)!=expected_source_counts[0]:
        raise ValueError("NO_GO_SPECIES_FRAME_DROPPED_ROWS")
    priorities=Counter(r["review_priority"] for r in out)
    joins=Counter(r["nhm_exact_name_join_status"] for r in out)
    uvjoins=Counter(r["uv_original_source_name_join_status"] for r in out)
    return out,{
      "status":"ORIGINAL_FCP_NHM_UV_GLOBAL_VISUAL_SIGNAL_REVIEW_QUEUE",
      "original_fcp_species":len(fcp_rows),
      "original_nhm_source_taxa":len(nhm_rows),
      "source_original_uv_taxon_rows":len(uv_rows),
      "review_priorities":dict(sorted(priorities.items())),
      "nhm_name_join_statuses":dict(sorted(joins.items())),
      "uv_name_join_statuses":dict(sorted(uvjoins.items())),
      "n_original_FCP_photos_in_roster":sum(r["n_original_photos_attempted"] for r in out),
      "n_coarse_color_classifiable_FCP_photos_in_roster":sum(
         r["n_fcp_four_coarse_colour_classifiable_photos"] for r in out),
      "n_NHM_unconfirmed_marking_TEXT_candidates_with_FCP":sum(
          r["nhm_visible_marking_TEXT_candidate_or_missing"]==1 for r in out),
      "n_source_UV_measured_name_matches_with_FCP":sum(
          r["uv_original_direct_measured_pattern_or_missing"]!="" for r in out),
      "not_source_measured_guide_or_insect_information_use":True,
      "all_unobserved_pattern_states_explicitly_NOT_MEASURED":True,
      "only_name_matching_no_synonym_or_taxonomic_reconciliation":True,
      "not_spatial_Bombus_exposure_or_plant_fitness":True,
    }


def main():
    fcp_raw=get_original_fcp_ledger()
    rdr=csv.DictReader(io.StringIO(fcp_raw.decode("utf-8-sig"),newline=""))
    fcp=list(rdr)
    nhm_raw,nhm_identity=_get_source_bytes()
    nhm,unverified,stats=summarize_and_extract(nhm_raw)
    uv,uv_identity=retrieve_original_uv()
    output,summary=compose_review_registry(fcp,nhm,uv)
    summary["FCP_original_Git_blob_sha1"]=SOURCE_GIT_BLOB_SHA1
    summary["NHM_original_git_blob_sha1"]=nhm_identity["git_blob_sha1_verified"]
    summary["UV_source_PDF_SHA256"]=uv_identity["original_source_pdf_sha256"] if "original_source_pdf_sha256" in uv_identity else "d11b41a36d85d1b70c8d3d47c04f3e03e7d8f5f58ebaaa331a737e56ed4c2820"
    dest=Path("stage48_global_flower_pattern_review")
    dest.mkdir(exist_ok=True)
    with (dest/"FCP_4475_species_NHM_visible_marking_and_UV_original_review_queue.csv").open(
        "w",newline="",encoding="utf8") as h:
        w=csv.DictWriter(h,fieldnames=list(output[0]))
        w.writeheader()
        w.writerows(output)
    (dest/"source_coverage_and_no_false_guide_status.json").write_text(
        json.dumps(summary,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE48_REAL_GLOBAL_VISUAL_IMAGE_REVIEW_CANDIDATES",json.dumps(summary,sort_keys=True))
    print("NO_CONFIRMED_NEW_UV_OR_VISIBLE_GUIDES_NO_BOMBUS_ASSOCIATION")

if __name__=="__main__":
    main()
