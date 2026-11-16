"""Stage49: join two source-authenticated 2016 and 2020/2021 literature artifacts.

This code consumes only successful immutable GitHub Actions artifacts:
- real 2016 177 UV trait rows, 164 mapped source records/159 accepted taxa
- real 2020/2021 121 literature records, 111 accepted taxa
Never add the denominators: merge by independently GBIF accepted taxon key.
Only directly measured UV spatial-pattern statuses enter the primary
binary response. 2020 historical UVP slope has NO binary guide status.
Any cross-study conflict is explicitly excluded from pooled binary labels.
"""
from __future__ import annotations

from collections import defaultdict,Counter
import argparse
import csv
import json
from pathlib import Path

NPH2016="10.1111/nph.13921"
TUNES2021="10.3389/fpls.2021.618028"
KOSKI2020="10.1016/j.cub.2020.08.077"

def rows_from_csv(filename):
    with Path(filename).open(encoding="utf8",newline="") as f:
        return list(csv.DictReader(f))

def union_source_records(nph,other):
    if len(nph)!=177 or len(other)!=121:
        raise ValueError("NO_GO_SOURCE_ARCHIVED_TAXON_DENOMINATORS_NOT_VALIDATED")
    accepted=defaultdict(list)
    for row in nph:
        key=row.get("accepted_GBIF_taxon_key_or_empty","")
        if row.get("accepted_GBIF_species_match_status")!="EXACT_CONFIDENT_SPECIES_MAPPED":
            continue
        if not key.isdigit():
            raise ValueError("NO_GO_NPH_ACCEPTED_KEY_NON_NUMERIC")
        label=row.get("source_measured_UV_pattern_present")
        if label not in ("0","1"):
            raise ValueError("NO_GO_NPH_SOURCE_BINARY_UV_LABEL")
        accepted[key].append({
           "article":NPH2016,"trait_kind":"SOURCE_MEASURED_UV_SPATIAL_PATTERN",
           "original_name":row["original_taxon_code"],
           "taxon_name":row["original_S1_author_full_binomial_candidate"],
           "pattern":int(label)
        })
    for row in other:
        key=row.get("gbif_accepted_species_key","")
        if row.get("gbif_match_status")!="EXACT_CONFIDENT_SPECIES_MAPPED":
            continue
        if not key.isdigit():
            raise ValueError("NO_GO_OTHER_PAPERS_ACCEPTED_KEY_NON_NUMERIC")
        article=row["original_study_doi"]
        if article==TUNES2021:
            original=row["UV_spatial_guide_pattern_source_status"]
            if original not in ("SOURCE_MEASURED_PATTERNED","SOURCE_MEASURED_UNIFORM"):
                raise ValueError("NO_GO_TUNES_DIRECT_MEASURED_UV_SOURCE_CATEGORY")
            accepted[key].append({
               "article":article,"trait_kind":"SOURCE_MEASURED_UV_SPATIAL_PATTERN",
               "original_name":row["published_taxon_string"],
               "taxon_name":row["canonical_binomial_candidate_unreconciled"],
               "pattern":int(original=="SOURCE_MEASURED_PATTERNED")
            })
        elif article==KOSKI2020:
            if row["UV_spatial_guide_pattern_source_status"]!="NOT_CLASSIFIED_BY_TABLE_S1":
                raise ValueError("NO_GO_HISTORICAL_UVP_TREATED_AS_GUIDE")
            accepted[key].append({
               "article":article,"trait_kind":"UVP_TEMPORAL_SLOPE_ONLY_NOT_GUIDE",
               "original_name":row["published_taxon_string"],
               "taxon_name":row["canonical_binomial_candidate_unreconciled"],
               "pattern":None
            })
        else:
            raise ValueError("NO_GO_UNKNOWN_ORIGINAL_LITERATURE_STUDY")
    merged=[]
    for key,records in sorted(accepted.items(),key=lambda p:int(p[0])):
        claims=[x for x in records if x["pattern"] is not None]
        values={x["pattern"] for x in claims}
        status=("NO_SOURCE_MEASURED_SPATIAL_PATTERN" if not claims
                else "CONFLICTING_DIRECT_SOURCE_UV_PATTERN_STATES_DO_NOT_POOL"
                   if len(values)>1
                else "CONSISTENT_SOURCE_MEASURED_SPATIAL_UV_PATTERN")
        pooled=next(iter(values)) if len(values)==1 else None
        merged.append({
            "gbif_accepted_species_key":key,
            "source_study_count":len({x["article"] for x in records}),
            "source_study_DOIs":"|".join(sorted({x["article"] for x in records})),
            "source_taxon_aliases":"|".join(sorted({x["taxon_name"] for x in records})),
            "n_original_published_taxon_units":len(records),
            "UV_binary_phenotype_evidence_status":status,
            "source_measured_UV_spatial_pattern_or_missing":(
                pooled if pooled is not None else ""),
            "n_direct_measured_UV_pattern_source_units":len(claims),
            "n_2020_temporal_UVP_source_units":sum(
                r["article"]==KOSKI2020 for r in records),
            "UV_plant_record_coverage_NOT_site_specific":True,
            "Bee_suitability_at_source_species_range":"NOT_MODELLED",
            "No_species_fitness_or_visual_learning_measured":True
        })
    assert len({x["gbif_accepted_species_key"] for x in merged})==len(merged)
    labels=Counter(x["UV_binary_phenotype_evidence_status"] for x in merged)
    source_n=Counter(x["article"] for rows in accepted.values() for x in rows)
    return merged,{
      "status":"AUTHENTIC_PUBLISHED_VISUAL_TAXONOMY_DEDUPLICATED_BY_ACCEPTED_GBIF_SPECIES",
      "source_2016_UV_mapped_taxon_units":source_n[NPH2016],
      "source_2021_UV_mapped_taxon_units":source_n[TUNES2021],
      "source_2020_historical_UVP_mapped_taxon_units":source_n[KOSKI2020],
      "source_specific_mapped_taxon_units_total":sum(source_n.values()),
      "n_unique_accepted_species_across_three_study_sources":len(merged),
      "source_accepted_species_evidence_statuses":dict(sorted(labels.items())),
      "n_unique_species_with_consistent_directly_measured_UV_spatial_pattern":labels[
          "CONSISTENT_SOURCE_MEASURED_SPATIAL_UV_PATTERN"],
      "n_unique_species_with_temporal_UVP_only_no_direct_binary":labels[
          "NO_SOURCE_MEASURED_SPATIAL_PATTERN"],
      "n_conflicting_direct_spatial_pattern_accepted_species":labels[
          "CONFLICTING_DIRECT_SOURCE_UV_PATTERN_STATES_DO_NOT_POOL"],
      "never_sum_overlapping_published_species_denominators":True,
      "source_taxon_subspecies_are_not_independent_accepted_species":True,
      "no_suitability_by_UV_pattern_spatial_coefficient_yet":True,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original-2016",required=True)
    ap.add_argument("--other-2020-2021",required=True)
    args=ap.parse_args()
    nph=rows_from_csv(args.original_2016)
    other=rows_from_csv(args.other_2020_2021)
    out,receipt=union_source_records(nph,other)
    dest=Path("stage49_unified_published_visual_species")
    dest.mkdir(exist_ok=True)
    with (dest/"literature_directly_measured_UV_species_GBIF_unique_accepted_registry.csv").open(
        "w",encoding="utf8",newline="") as h:
        writer=csv.DictWriter(h,fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    (dest/"source_unique_accepted_species_overlap_receipt.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=False)+"\n",
        encoding="utf8")
    print("STAGE49_UNIQUE_ACCEPTED_LITERATURE_VISUAL_SPECIES_UNION",
          json.dumps(receipt,sort_keys=True))
    print("NO_RAW_BEE_COUNT_VS_UV_PATTERN_FIT")

if __name__=="__main__":
    main()
