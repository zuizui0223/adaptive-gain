"""Stage52 exploratory AFTER initial results: pair source-UV plants by genus, latitude, UV-B, temperature.

Consumes source-authenticated 60-species 2016 UV/bombus-share original
study table from Stage52. Pair selection ONLY uses original author
genus+latitude+UVB+mean annual temperature, never modelled bees/UV outcome
beyond selecting opposite measured classes. No source study field visits,
GBIF native range, pollen, seed or bee information use. Two fixed
sensitivity tiers tested; not preregistered or population inference.
"""
from __future__ import annotations
import argparse,csv,json,math,statistics
from pathlib import Path
from collections import Counter

ENDPOINTS=("source_modelled_Bombus_share_proxy_N",
           "source_modelled_Bombus_taxa_N",
           "source_modelled_all_bee_taxa_N")
MATCH_SPECS=(("strict",5.0,700.0,4.0),
             ("relaxed",8.0,1000.0,6.0))

def source_rows(filename):
    with Path(filename).open(encoding="utf8",newline="") as h:
        rows=list(csv.DictReader(h))
    if len(rows)!=60 or len({r["gbif_accepted_species_key"] for r in rows})!=60:
        raise ValueError("NO_GO_SOURCE_60_PRESPECIFIED_SPECIES")
    processed=[]
    for r in rows:
        if r["original_UV_pattern_binary"] not in ("0","1"):
            raise ValueError("NO_GO_UV_PATTERN_SOURCE_STATE")
        viable=r["viable_N_5records_2hex"]=="True"
        q={**r,"source_UV_binary":int(r["original_UV_pattern_binary"]),
           "source_lat":float(r["source_mean_latitude_N"]),
           "source_uvb":float(r["source_mean_UVB"]),
           "source_temp":float(r["source_mean_temperature"]),
           "eligible":viable}
        for m in ENDPOINTS:
            q[m]=float(r[m]) if viable else None
            if q[m] is not None and not math.isfinite(q[m]):
                raise ValueError("NO_GO_SOURCE_BEE_METRIC_NONFINITE")
        processed.append(q)
    return processed

def match_covariates(rows,latlim,uvblim,templim):
    if not (latlim>0 and uvblim>0 and templim>0):
        raise ValueError("NO_GO_INVALID_COVARIATE_TOLERANCES")
    patterned=[r for r in rows if r["eligible"] and r["source_UV_binary"]==1]
    uniform=[r for r in rows if r["eligible"] and r["source_UV_binary"]==0]
    candidates=[]
    for a in patterned:
        for b in uniform:
            if not a["original_author_genus"] or a["original_author_genus"]!=b["original_author_genus"]:
                continue
            lat=abs(a["source_lat"]-b["source_lat"])
            uvb=abs(a["source_uvb"]-b["source_uvb"])
            temp=abs(a["source_temp"]-b["source_temp"])
            if lat>latlim or uvb>uvblim or temp>templim:
                continue
            # All matching decisions independent of bee exposure outcome.
            score=lat/latlim+uvb/uvblim+temp/templim
            candidates.append((score,lat,uvb,temp,a,b))
    candidates.sort(key=lambda x:(x[0],x[4]["gbif_accepted_species_key"],
                                  x[5]["gbif_accepted_species_key"]))
    used_a=set();used_b=set();pairs=[]
    for score,lat,uvb,temp,a,b in candidates:
        ak=a["gbif_accepted_species_key"];bk=b["gbif_accepted_species_key"]
        if ak in used_a or bk in used_b:continue
        used_a.add(ak);used_b.add(bk)
        row={
          "pattern_GBIF_accepted_species_key":ak,
          "uniform_GBIF_accepted_species_key":bk,
          "original_author_genus":a["original_author_genus"],
          "source_abs_latitude_difference_degrees":lat,
          "source_UVB_difference":uvb,
          "source_temperature_difference_C":temp,
          "matching_score_covariate_only":score,
        }
        for m in ENDPOINTS:
            row[m+"_pattern_minus_uniform"]=a[m]-b[m]
        pairs.append(row)
    return pairs

def report(rows):
    records=[]
    for name,lat,uvb,temp in MATCH_SPECS:
        pairs=match_covariates(rows,lat,uvb,temp)
        effects={}
        for m in ENDPOINTS:
            values=[x[m+"_pattern_minus_uniform"] for x in pairs]
            loo=[statistics.mean(values[:i]+values[i+1:]) for i in range(len(values))]
                if len(values)>1 else []
            effects[m]={
              "n_pairs":len(values),
              "mean_pattern_minus_uniform":statistics.mean(values) if values else None,
              "median_pattern_minus_uniform":statistics.median(values) if values else None,
              "positive_pairs":sum(x>0 for x in values),
              "negative_pairs":sum(x<0 for x in values),
              "leave_one_pair_out_mean_min_max":(
                 [min(loo),max(loo)] if loo else None)
            }
        records.append({
           "tolerance_tier":name,
           "maximum_original_latitude_gap_degrees":lat,
           "maximum_original_UVB_gap":uvb,
           "maximum_original_temperature_gap_C":temp,
           "n_disjoint_original_genus_environment_matched_pairs":len(pairs),
           "pairs":pairs,
           "outcome_diagnostics":effects,
           "source_pairing_uses_no_modelled_bee_data":True,
           "not_a_climate_controlled_population_inference":True
        })
    return {
      "status":"ORIGINAL_UV_2016_GENUS_LATITUDE_UVB_TEMPERATURE_MATCHED_DESCRIPTIVE",
      "n_original_published_2016_source_taxa_pilot":len(rows),
      "n_eligible_source_records":sum(x["eligible"] for x in rows),
      "source_matching_posthoc_after_initial_descriptives":True,
      "fixed_source_covariate_only_match_specs":records,
      "no_randomized_species_trait_or_independent_native_ranges":True,
      "no_valid_pollinator_guide_use_or_fitness_effect":True
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original-60-UV-source-guild",required=True)
    args=ap.parse_args()
    rows=source_rows(args.original_60_UV_source_guild)
    receipt=report(rows)
    folder=Path("stage52_species_climate_matched_sensitivity")
    folder.mkdir(exist_ok=True)
    (folder/"published_UV_genus_lat_UVB_temp_matched_pairs.json").write_text(
        json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE52_REAL_UV_GENUS_LATITUDE_CLIMATE_MATCHED_SOURCE_PAIRS",
          json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    print("NO_CAUSAL_OR_POLLINATOR_INFORMATION_USE_TEST")

if __name__=="__main__":
    main()
