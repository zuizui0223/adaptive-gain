"""Stage57 original 2025 UV reflectance × bee/bird syndrome family/area audit.

Pre-defined purely descriptive contrasts:
 (a) source 245 rows before taxon dedup,
 (b) 243 strictly GBIF-accepted unique species (one repeated species source
     with distinct UV reflectance values is aggregated, preserving range),
 (c) source-family and source-family×broad-area equal-stratum within-group
     bee minus bird UV-reflectance means,
 (d) original hue UV+/UV- frequency and source broad area imbalance.

This is NOT Bombus spatial distribution, a floral UV pattern, site-level
environment, phylogenetic PGLS, randomization, nor a causal path model.
Published guild labels are study's literature-based syndrome classifications.
No p-values; family and area strata are unbalanced and not independent.
"""
from __future__ import annotations
import argparse,csv,json,math,statistics
from collections import Counter,defaultdict
from pathlib import Path

N_ROWS=245
N_ACCEPTED_ROWS=244
N_ACCEPTED_SPECIES=243
REQUIRED=("source_original_docx_tableS1_row_1_based",
    "GBIF_accepted_species_key_or_unknown",
    "GBIF_strict_match_status",
    "source_average_UV_reflection_proportion_or_unknown",
    "source_pollination_system_literal",
    "source_colour_hue_category_literal",
    "source_family_literal",
    "source_geographic_area_category_literal")
HUE_PREFIXES=("UV+","UV-")

def read(path):
    with Path(path).open(encoding="utf8",newline="") as fp:
        return list(csv.DictReader(fp))

def collapse_species(rows,expected_source_n=N_ROWS,strict=True):
    if len(rows)!=expected_source_n:
        raise ValueError("NO_GO_245_SOURCE_ORIGINAL_TABLE_ROWS")
    if any(any(x not in r for x in REQUIRED) for r in rows):
        raise ValueError("NO_GO_SOURCE_ORIGINAL_245_COLUMNS")
    out=[]
    byid=defaultdict(list)
    for r in rows:
        try:
            reflectance=float(r["source_average_UV_reflection_proportion_or_unknown"])
        except (TypeError,ValueError) as exc:
            raise ValueError("NO_GO_SOURCE_245_NUMERIC_UV_REFLECTANCE") from exc
        if not (math.isfinite(reflectance) and 0<=reflectance<=1):
            raise ValueError("NO_GO_SOURCE_245_REFLECTION_RANGE")
        if r["source_pollination_system_literal"] not in ("bee","bird"):
            raise ValueError("NO_GO_UNEXPECTED_SOURCE_GUILD_LABEL")
        if not r["source_colour_hue_category_literal"].startswith(HUE_PREFIXES):
            raise ValueError("NO_GO_SOURCE_HUE_NOT_ORIGINAL_UV_CLASS")
        status=r["GBIF_strict_match_status"]
        key=r["GBIF_accepted_species_key_or_unknown"]
        if status=="EXACT_CONFIDENT_SPECIES_MAPPED":
            if not key.isdigit():
                raise ValueError("NO_GO_SOURCE_ACCEPTED_KEY_INVALID")
            byid[key].append(r)
        elif status=="SOURCE_TAXON_NOT_LEXICAL_BINOMIAL":
            if key:
                raise ValueError("NO_GO_SOURCE_UNRESOLVED_TAXON_HAS_ACCEPTED_KEY")
        else:
            if strict:
                raise ValueError("NO_GO_SOURCE_UNEXPECTED_GBIF_TAXON_STATUS")
    if strict and (len(byid)!=N_ACCEPTED_SPECIES or
                   sum(map(len,byid.values()))!=N_ACCEPTED_ROWS):
        raise ValueError("NO_GO_SOURCE_245_ACCEPTED_SPECIES_DENOMINATORS")
    for key,rs in sorted(byid.items(),key=lambda x:int(x[0])):
        # A taxon's true source internal variation must not be treated as
        # independent phylogenetic species. Do not merge opposite guilds.
        consistency=("source_family_literal",
                     "source_geographic_area_category_literal",
                     "source_pollination_system_literal")
        for c in consistency:
            if len({r[c] for r in rs})!=1:
                raise ValueError("NO_GO_SOURCE_MULTIPLE_ROW_FAMILY_AREA_GUILD_CONFLICT")
        vals=[float(r["source_average_UV_reflection_proportion_or_unknown"]) for r in rs]
        row=rs[0]
        out.append({
           "accepted_GBIF_species_key":key,
           "source_family":row["source_family_literal"],
           "source_broad_area":row["source_geographic_area_category_literal"],
           "source_literature_primary_pollination_system":row["source_pollination_system_literal"],
           "mean_original_source_UV_reflectance":statistics.mean(vals),
           "source_original_reflectance_range":[min(vals),max(vals)],
           "number_original_source_measurement_rows":len(vals),
           "original_hue_UV_positive_any":any(r["source_colour_hue_category_literal"].startswith("UV+") for r in rs),
           "original_hue_UV_positive_all":all(r["source_colour_hue_category_literal"].startswith("UV+") for r in rs),
           "NOT_spatial_UV_pattern":True,
           "NOT_measured_Bombus_or_bird_visits":True,
        })
    return out

def _stats(values):
    return {"n":len(values),"mean":statistics.mean(values) if values else None,
            "median":statistics.median(values) if values else None}

def _difference(rows):
    bee=[x["mean_original_source_UV_reflectance"] for x in rows
         if x["source_literature_primary_pollination_system"]=="bee"]
    bird=[x["mean_original_source_UV_reflectance"] for x in rows
          if x["source_literature_primary_pollination_system"]=="bird"]
    return statistics.mean(bee)-statistics.mean(bird) if bee and bird else None

def contrasts(rows):
    if not rows:
        raise ValueError("NO_GO_EMPTY_ACCEPTED_SPECIES")
    group=[x["source_literature_primary_pollination_system"] for x in rows]
    out={
      "total_accepted_distinct_taxa":len(rows),
      "n_source_family":len({r["source_family"] for r in rows}),
      "n_broad_source_area_categories":len({r["source_broad_area"] for r in rows}),
      "unique_species_per_guild":dict(sorted(Counter(group).items())),
      "one_species_with_two_different_UV_source_rows_not_independent_taxa":sum(
          r["number_original_source_measurement_rows"]>1 for r in rows),
      "observed_source_uv_reflectance_by_guild":{
          k:_stats([r["mean_original_source_UV_reflectance"] for r in rows if r[
              "source_literature_primary_pollination_system"]==k])
          for k in ("bee","bird")},
      "all_unique_species_unadjusted_bee_minus_bird":_difference(rows),
      "broad_area_by_guild_counts":{
          k:dict(sorted(Counter(r["source_literature_primary_pollination_system"]
                for r in rows if r["source_broad_area"]==k).items()))
          for k in sorted({r["source_broad_area"] for r in rows})},
      "source_original_hue_UVplus_by_guild":{
          k:{"n_UVplus_any_original_hue":sum(
              r["original_hue_UV_positive_any"] for r in rows if r[
                 "source_literature_primary_pollination_system"]==k),
            "n_total":sum(r["source_literature_primary_pollination_system"]==k for r in rows)}
          for k in ("bee","bird")},
    }
    for granule,cols in (
       ("broad_area",("source_broad_area",)),
       ("source_family",("source_family",)),
       ("family_by_area",("source_family","source_broad_area"))
    ):
        groups=defaultdict(list)
        for r in rows:
            groups[tuple(r[c] for c in cols)].append(r)
        viable=[{"stratum":list(key),"bee_minus_bird_UV_reflection":_difference(rs),
                 "n_guild_bee":sum(r["source_literature_primary_pollination_system"]=="bee" for r in rs),
                 "n_guild_bird":sum(r["source_literature_primary_pollination_system"]=="bird" for r in rs)}
                for key,rs in sorted(groups.items()) if _difference(rs) is not None]
        diffs=[x["bee_minus_bird_UV_reflection"] for x in viable]
        out[granule+"_source_within_strata"]={
          "n_source_strata":len(groups),
          "n_with_both_guilds":len(viable),
          "n_no_within_stratum_guild_contrast":len(groups)-len(viable),
          "equal_observed_stratum_weight_bee_minus_bird_mean_or_unknown":(
              statistics.mean(diffs) if diffs else None),
          "equal_observed_stratum_weight_median_or_unknown":(
              statistics.median(diffs) if diffs else None),
          "positive_negative_zero_strata":{
              "positive":sum(x>0 for x in diffs),
              "negative":sum(x<0 for x in diffs),
              "zero":sum(x==0 for x in diffs),
          },
          "leave_one_stratum_out_equal_stratum_mean_range_or_unknown":(
              [min(statistics.mean(diffs[:i]+diffs[i+1:]) for i in range(len(diffs))),
               max(statistics.mean(diffs[:i]+diffs[i+1:]) for i in range(len(diffs)))]
              if len(diffs)>1 else None),
          "no_shared_stratum_not_treated_as_zero":True,
          "not_an_environment_or_phylogenetic_causal_control":True,
        }
    return out

def report(rows,source):
    outcomes=contrasts(rows)
    original_guild=Counter(x["source_pollination_system_literal"] for x in source)
    if len(source)==N_ROWS and original_guild!=Counter({"bee":136,"bird":109}):
        raise ValueError("NO_GO_AUTHOR_SOURCE_245_GUILD_COUNTS_DRIFT")
    return {"status":"ORIGINAL_2025_NUMERIC_UV_BEE_BIRD_FAMILY_AREA_NONCAUSAL_COMPARISON",
        "source_authored_table_rows":len(source),
        "source_primary_guild_label_counts_original":dict(sorted(original_guild.items())),
        "accepted_distinct_taxon_descriptive_statistics":outcomes,
        "sampled_source_family_and_country_are_NOT_local_site_climate":True,
        "not_Bombus_species_distribution_at_sampling_sites":True,
        "not_a_visual_guide_or_reward_information_claim":True,
        "not_phylopath_or_causal_SEM_or_independent_evolutionary_transitions":True,
        "no_inferential_pvalue_from_nonrandom_opportunistic_species_list":True,
        "no_hue_category_recoded_as_actual_UV_pattern":True,
        "source_245_rows_and_243_accepted_species_not_two_independent_studies":True,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--Oliveira2025-original-245",required=True)
    args=ap.parse_args()
    source=read(args.Oliveira2025_original_245)
    individual=collapse_species(source)
    result=report(individual,source)
    folder=Path("stage57_Oliveira245_family_area_audit")
    folder.mkdir(exist_ok=True)
    (folder/"original_UV_reflectance_bee_bird_family_area_confound_receipt.json").write_text(
        json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    with (folder/"original_2025_accepted_species_243_collapsed_UV_reflectance.csv").open(
        "w",encoding="utf8",newline="") as fp:
        flat=[{k:json.dumps(v) if isinstance(v,list) else v for k,v in r.items()} for r in individual]
        w=csv.DictWriter(fp,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    print("STAGE57_2025_SOURCE_BEE_BIRD_UV_REFLECTANCE_FAMILY_AREA_AUDIT",
          json.dumps(result,ensure_ascii=False,sort_keys=True,allow_nan=False))
    print("NO_GUILD_CAUSAL_SELECTION_OR_UV_GUIDE_EVOLUTION_INFERRED")

if __name__=="__main__":
    main()
