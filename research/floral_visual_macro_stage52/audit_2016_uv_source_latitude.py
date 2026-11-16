"""Stage52: original 2016 temperate UV study latitude/UV-B source audit.

Consumes source-authenticated Stage49 original Koski & Ashman 2016
177 original taxon/variety records, of which 164 source units map to
159 distinct GBIF accepted species. This is a source-domain audit,
NOT a native range estimate or a modeled UV×Bombus association.

We first establish whether the published 'mean latitude' is signed,
absolute or contains values needing author clarification before using
it as an occurrence geo-window. No GBIF plant occurrence is fetched.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv
import json
import math
from pathlib import Path
import statistics
import argparse

EXPECTED_SOURCE_ROWS=177
EXPECTED_ACCEPTED_TAXA=159
EXPECTED_ACCEPTED_ROWS=164


def numeric(value,label):
    if value is None or str(value).strip() in ("","NA","nan","None"):
        return None
    try:
        v=float(value)
    except (TypeError,ValueError) as e:
        raise ValueError("NO_GO_SOURCE_PUBLISHED_FIELD_NONNUMERIC_"+label) from e
    if not math.isfinite(v):
        raise ValueError("NO_GO_SOURCE_PUBLISHED_FIELD_NONFINITE_"+label)
    return v


def binstats(values):
    vals=[float(v) for v in values if v is not None]
    if not vals:
        return {"n":0,"min":None,"max":None,"mean":None,"median":None}
    return {"n":len(vals),"min":min(vals),"max":max(vals),
            "mean":statistics.mean(vals),"median":statistics.median(vals)}


def audit(rows):
    if len(rows)!=EXPECTED_SOURCE_ROWS:
        raise ValueError("NO_GO_PUBLISHED_177_ORIGINAL_SOURCE_ROWS")
    matched=defaultdict(list)
    excluded=Counter()
    for row in rows:
        if row.get("source_measured_UV_pattern_present") not in ("0","1"):
            raise ValueError("NO_GO_AUTHOR_PUBLISHED_UV_PATTERN_NOT_BINARY")
        status=row.get("accepted_GBIF_species_match_status")
        key=row.get("accepted_GBIF_taxon_key_or_empty","")
        if status!="EXACT_CONFIDENT_SPECIES_MAPPED":
            excluded[status or "UNKNOWN"]=excluded[status or "UNKNOWN"]+1
            continue
        if not key.isdigit():
            raise ValueError("NO_GO_SOURCE_GBIF_ACCEPTED_SPECIES_KEY")
        matched[key].append(row)
    if len(matched)!=EXPECTED_ACCEPTED_TAXA or sum(map(len,matched.values()))!=EXPECTED_ACCEPTED_ROWS:
        raise ValueError("NO_GO_ACCEPTED_SOURCE_159_OR_164_DRIFT")
    result=[]
    for key,rs in sorted(matched.items(),key=lambda x:int(x[0])):
        pattern={r["source_measured_UV_pattern_present"] for r in rs}
        if len(pattern)!=1:
            raise ValueError("NO_GO_SOURCE_INFRASPECIFIC_UV_STATE_CONFLICT")
        genus={
            r.get("original_S1_author_full_binomial_candidate","").split(" ")[0]
            for r in rs if r.get("original_S1_author_full_binomial_candidate","")
        }
        if len(genus)>1:
            raise ValueError("NO_GO_ORIGINAL_AUTHOR_CROSS_GENUS_SYNONYMY_NOT_RESOLVED")
        metrics={}
        for label,field in (
           ("latitude","source_mean_latitude_deg"),
           ("uvb","source_mean_UVB_J_per_m2_per_day"),
           ("temp","source_mean_annual_temp_C"),
           ("precip","source_mean_annual_precip_mm"),
           ("alt","source_mean_altitude_m"),
        ):
            vals=[numeric(r.get(field),field) for r in rs]
            metrics[label]=binstats(vals)
        result.append({
            "gbif_accepted_species_key":key,
            "source_2016_UV_pattern":int(next(iter(pattern))),
            "original_2016_source_genus_or_unknown":next(iter(genus),""),
            "number_original_infraspecific_source_rows":len(rs),
            "published_latitude_mean":metrics["latitude"]["mean"],
            "published_latitude_min_original_source_rows":metrics["latitude"]["min"],
            "published_latitude_max_original_source_rows":metrics["latitude"]["max"],
            "published_uvb_mean":metrics["uvb"]["mean"],
            "published_annual_temp_mean":metrics["temp"]["mean"],
            "published_precip_mean":metrics["precip"]["mean"],
            "published_altitude_mean":metrics["alt"]["mean"],
            "original_geographic_source_type":"one_species_average_not_GBIF_occurrence_or_phototyped_locality",
            "native_range_verified":False,
            "published_latitude_hemisphere_interpretation":"UNCHECKED_ORIGINAL_PAPER_CONVENTION"
        })
    pattern_counts=Counter(r["source_2016_UV_pattern"] for r in result)
    signed=Counter(
        "negative" if r["published_latitude_mean"]<0 else
        "zero" if r["published_latitude_mean"]==0 else "positive"
        for r in result if r["published_latitude_mean"] is not None
    )
    coverage=[]
    for p in (0,1):
        group=[r for r in result if r["source_2016_UV_pattern"]==p]
        coverage.append({
          "UV_pattern_2016":p,
          "n_accepted_source_species":len(group),
          "published_latitude":binstats([r["published_latitude_mean"] for r in group]),
          "source_abs_latitude":binstats([
              abs(r["published_latitude_mean"])
              if r["published_latitude_mean"] is not None else None for r in group]),
          "UVB":binstats([r["published_uvb_mean"] for r in group]),
          "annual_temperature":binstats([r["published_annual_temp_mean"] for r in group]),
          "annual_precipitation":binstats([r["published_precip_mean"] for r in group]),
        })
    report={
       "status":"AUTHENTIC_2016_UV_SPECIES_SOURCE_LATITUDE_UVB_FEASIBILITY_GATE",
       "source_original_taxon_rows":len(rows),
       "accepted_source_taxon_rows":sum(map(len,matched.values())),
       "accepted_distinct_GBIF_species":len(matched),
       "accepted_species_UV_pattern_counts":dict(sorted(pattern_counts.items())),
       "source_latitude_sign_counts":dict(sorted(signed.items())),
       "published_latitude_source_geometry_known_to_be_actual_occurrence":False,
       "published_latitude_as_signed_or_unsigned_still_requires_author_source_interpretation":True,
       "species_source_variation":coverage,
       "unresolved_original_taxon_rows":dict(sorted(excluded.items())),
       "no_direct_UV_phenotype_observed_at_2026_GBIF_species_occurrence":True,
       "no_Bombus_or_other_pollinator_fitness_or_richness_effect":True
    }
    return result,report


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-2016-csv",required=True)
    args=p.parse_args()
    with Path(args.original_2016_csv).open(encoding="utf8",newline="") as f:
        source=list(csv.DictReader(f))
    rows,report=audit(source)
    out=Path("stage52_source_latitude")
    out.mkdir(exist_ok=True)
    with (out/"KoskiAshman2016_159_accepted_UV_source_latitude_UVB.csv").open("w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    (out/"source_2016_latitude_UVB_hemisphere_gate.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True,allow_nan=False)+"\n",encoding="utf8")
    print("STAGE52_2016_UV_SOURCE_LATITUDE_AND_UVB_GRAIN",json.dumps(report,ensure_ascii=False,sort_keys=True))
    print("NO_NATIVE_RANGES_OR_UV_BOMBUS_ASSOCIATION_ESTIMATED")

if __name__=="__main__":
    main()
