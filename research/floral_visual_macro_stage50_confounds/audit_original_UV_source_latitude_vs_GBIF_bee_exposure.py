"""Stage50 independent confounding/representativeness audit.

Join the SOURCE-MEASURED original 2016 published Potentilleae latitude,
annual climate and UV-B with source-verified GBIF-first-page records in the
60-species Stage50 pilot. This tests whether apparent bee-richness contrast
could simply track native-biome/study/latitude and nonrepresentative GBIF
sampling, rather than creating a post-hoc positive hypothesis.

No model-based P values, no assumption that GBIF source points are the
published botanical phenotype measurement locations, and no native-range
or realized pollination claims.
"""
from __future__ import annotations

from collections import Counter,defaultdict
import argparse
import csv
import json
import math
from pathlib import Path
import statistics

PAPER2016="10.1111/nph.13921"
LAT_PAIR_MAX_DEGREES=5.0
MIN_USEFUL_GEO_RECORDS=15
MIN_USEFUL_GEO_CELLS=3


def _number(r,k):
    x=r.get(k)
    if x is None or str(x).strip() in ("","NA","None","nan"):
        return None
    try:
        a=float(x)
    except ValueError as err:
        raise ValueError("NO_GO_ORIGINAL_SOURCE_CLIMATE_NONNUMERIC_"+k) from err
    if not math.isfinite(a):
        raise ValueError("NO_GO_ORIGINAL_SOURCE_CLIMATE_NONFINITE_"+k)
    return a


def _int(r,k):
    try:
        n=int(r[k])
    except (KeyError,ValueError,TypeError) as err:
        raise ValueError("NO_GO_PILOT_N_NONINTEGER_"+k) from err
    if n<0:
        raise ValueError("NO_GO_PILOT_N_NEGATIVE_"+k)
    return n


def _json_list(r,k):
    if r.get(k) in ("",None):
        return []
    try:
        z=json.loads(r[k])
    except (ValueError,TypeError,KeyError) as err:
        raise ValueError("NO_GO_PILOT_SOURCE_JSON_LIST_"+k) from err
    if not isinstance(z,list):
        raise ValueError("NO_GO_PILOT_SOURCE_NOT_JSON_LIST_"+k)
    return z


def _mean(values):
    x=[a for a in values if a is not None]
    return statistics.mean(x) if x else None


def prepare(pilot_rows,nph_rows,expected_pilot=60,expected_nph=177):
    if len(pilot_rows)!=expected_pilot or len(nph_rows)!=expected_nph:
        raise ValueError("NO_GO_ORIGINAL_PILOT_OR_NPH_SOURCE_DENOMINATOR")
    original=defaultdict(list)
    for row in nph_rows:
        if row.get("accepted_GBIF_species_match_status")=="EXACT_CONFIDENT_SPECIES_MAPPED":
            key=row.get("accepted_GBIF_taxon_key_or_empty","")
            if not str(key).isdigit():
                raise ValueError("NO_GO_NPH_ACCEPTED_GBIF_KEY")
            original[str(key)].append(row)
    out=[]
    for p in pilot_rows:
        key=p.get("gbif_accepted_species_key","")
        study=p.get("primary_original_UV_study")
        state=p.get("UV_pattern_direct_source_binary")
        if not key.isdigit() or study not in ("2016","2021") or state not in ("0","1"):
            raise ValueError("NO_GO_PILOT_SOURCE_SPECIES_KEY_OR_UV_STATE")
        source=original.get(key,[])
        if study=="2016" and not source:
            raise ValueError("NO_GO_2016_PILOT_GBIF_KEY_NOT_IN_AUTHENTIC_PAPER")
        if study=="2021" and source:
            # A cross-source overlap is allowed in general, but Stage49
            # here found no original 2016+2021 accepted key intersections.
            raise ValueError("NO_GO_CURRENT_PILOT_2021_OVERLAPS_2016_SOURCE")
        if source and len({str(s["source_measured_UV_pattern_present"]) for s in source})>1:
            raise ValueError("NO_GO_DIRECT_SOURCE_UV_CONFLICT_WITHIN_SPECIES")
        if source and str(source[0]["source_measured_UV_pattern_present"])!=state:
            raise ValueError("NO_GO_PUBLISHED_SOURCE_UV_VERSUS_PILOT_STATUS")
        lat=[_number(s,"source_mean_latitude_deg") for s in source]
        uvb=[_number(s,"source_mean_UVB_J_per_m2_per_day") for s in source]
        temp=[_number(s,"source_mean_annual_temp_C") for s in source]
        precip=[_number(s,"source_mean_annual_precip_mm") for s in source]
        genus={s.get("original_S1_author_full_binomial_candidate","").split(" ")[0]
               for s in source if s.get("original_S1_author_full_binomial_candidate")}
        if len(genus)>1:
            raise ValueError("NO_GO_ONE_ACCEPTED_SPECIES_MULTIPLE_ORIGINAL_GENERA")
        coords=_json_list(p,"sampled_GBIF_latitude_min_max")
        if coords and (len(coords)!=2 or not all(isinstance(v,(int,float)) for v in coords)):
            raise ValueError("NO_GO_GBIF_SAMPLED_LAT_RANGE")
        country=_json_list(p,"source_record_country_codes")
        nrecords=_int(p,"n_eligible_model_source_occurrence_records")
        ncells=_int(p,"n_eligible_source_model_cells_with_GBIF_plant_points")
        if (nrecords==0)!=(ncells==0):
            raise ValueError("NO_GO_ORIGINAL_PILOT_CELL_COVERAGE_GRAIN")
        mean_b=_number(p,"modelled_Bombus_taxa_equal_visited_HEX_cell_mean_or_null")
        mean_all=_number(p,"modelled_all_bee_taxa_equal_visited_HEX_cell_mean_or_null")
        if nrecords==0 and (mean_b is not None or mean_all is not None):
            raise ValueError("NO_GO_OUTSIDE_MODELLED_BEE_SUPPORT_TREATED_AS_ZERO")
        source_mean_lat=_mean(lat)
        in_gbif_sample_range=(coords[0]<=source_mean_lat<=coords[1]
                              if coords and source_mean_lat is not None else None)
        out.append({
          "gbif_accepted_species_key":key,
          "original_study":study,
          "source_direct_UV_pattern_binary":int(state),
          "original_2016_Genus_or_unknown":next(iter(genus),""),
          "original_2016_source_S2_record_count":len(source),
          "original_2016_mean_source_latitude_or_null":source_mean_lat,
          "original_2016_mean_source_abs_latitude_or_null":(
              abs(source_mean_lat) if source_mean_lat is not None else None),
          "original_2016_source_mean_UVB_or_null":_mean(uvb),
          "original_2016_source_mean_annual_temp_or_null":_mean(temp),
          "original_2016_source_mean_annual_precip_or_null":_mean(precip),
          "original_2016_source_mean_latitude_within_bounded_GBIF_index_page_range_or_unknown":in_gbif_sample_range,
          "original_2021_Cerrado_study_Brazil_in_sampled_eligible_GBIF_country_codes_or_unknown":(
              "BR" in country if study=="2021" else None),
          "eligible_bee_model_hex_count":ncells,
          "qualified_GBIF_plant_occurrences":nrecords,
          "mean_modelled_source_Bombus_taxa_or_null":mean_b,
          "mean_modelled_source_all_bee_taxa_or_null":mean_all,
          "meets_pilot_exposure_minimum":nrecords>=MIN_USEFUL_GEO_RECORDS and ncells>=MIN_USEFUL_GEO_CELLS,
          "source_GBIF_plant_sample_not_species_native_range":True,
          "published_UV_trait_not_geographically_annotated_per_GBIF_record":True,
          "not_phylogeny_adjusted_statistical_claim":True,
        })
    if len(out)!=expected_pilot or len(set(x["gbif_accepted_species_key"] for x in out))!=expected_pilot:
        raise ValueError("NO_GO_PILOT_SOURCE_DUPLICATION")
    return out


def strict_latitude_and_genus_pairs(rows,maxlat=LAT_PAIR_MAX_DEGREES):
    """Greedy source-latitude/within-genus comparisons, diagnostics only."""
    subset=[r for r in rows if r["original_study"]=="2016"
            and r["meets_pilot_exposure_minimum"]
            and r["original_2016_mean_source_latitude_or_null"] is not None
            and r["original_2016_Genus_or_unknown"]
            and r["mean_modelled_source_Bombus_taxa_or_null"] is not None]
    a=[r for r in subset if r["source_direct_UV_pattern_binary"]==1]
    b=[r for r in subset if r["source_direct_UV_pattern_binary"]==0]
    candidates=[]
    for x in a:
        for y in b:
            if x["original_2016_Genus_or_unknown"]!=y["original_2016_Genus_or_unknown"]:
                continue
            difference=abs(
                x["original_2016_mean_source_latitude_or_null"]-
                y["original_2016_mean_source_latitude_or_null"]
            )
            if difference<=maxlat:
                candidates.append((difference,x,y))
    candidates.sort(key=lambda triple:(
        triple[0],triple[1]["gbif_accepted_species_key"],
        triple[2]["gbif_accepted_species_key"]))
    taken_a=set();taken_b=set();deltas=[]
    for distance,x,y in candidates:
        if x["gbif_accepted_species_key"] in taken_a or (
           y["gbif_accepted_species_key"] in taken_b):
            continue
        taken_a.add(x["gbif_accepted_species_key"])
        taken_b.add(y["gbif_accepted_species_key"])
        deltas.append(
           x["mean_modelled_source_Bombus_taxa_or_null"]-
           y["mean_modelled_source_Bombus_taxa_or_null"]
        )
    return {
       "n_viable_original_2016_species_in_pair_pool":len(subset),
       "n_disjoint_within_Genus_and_5degree_original_source_latitude_pairs":len(deltas),
       "matched_pair_pattern_minus_uniform_mean_modelled_Bombus_source_names":(
           _mean(deltas)),
       "matched_pair_contrast_only_descriptive_no_p_value":True,
       "insufficient_pairs_for_population_inference":len(deltas)<5,
       "not_a_causal_climate_or_phylogenetic_control":True
    }


def summarize(rows):
    summaries=[]
    for study in ("2016","2021"):
      for pat in (0,1):
        group=[x for x in rows if x["original_study"]==study
               and x["source_direct_UV_pattern_binary"]==pat]
        if len(group)!=15:
            raise ValueError("NO_GO_ORIGINAL_STUDY_SOURCE_PATTERN_SAMPLING_BALANCE")
        eligible=[r for r in group if r["meets_pilot_exposure_minimum"]]
        summaries.append({
          "study":study,"source_pattern_binary":pat,
          "n_pilot_species":len(group),
          "n_geographically_eligible_species":len(eligible),
          "mean_modelled_Bombus_in_eligible_source_cells":_mean(
              [r["mean_modelled_source_Bombus_taxa_or_null"] for r in eligible]),
          "mean_original_source_absolute_latitude_for_eligible_2016_species":_mean(
              [r["original_2016_mean_source_abs_latitude_or_null"] for r in eligible]),
          "mean_original_source_UVB_for_eligible_2016_species":_mean(
              [r["original_2016_source_mean_UVB_or_null"] for r in eligible]),
          "mean_original_source_annual_temp_for_eligible_2016_species":_mean(
              [r["original_2016_source_mean_annual_temp_or_null"] for r in eligible]),
          "n_2021_study_species_with_Brazil_in_bounded_GBIF_page_modelled_points":sum(
              r["original_2021_Cerrado_study_Brazil_in_sampled_eligible_GBIF_country_codes_or_unknown"]
              is True for r in group),
          "no_adjusted_UV_Bombus_inference":True,
        })
    original2016=[r for r in rows if r["original_study"]=="2016"]
    original2021=[r for r in rows if r["original_study"]=="2021"]
    return {
       "status":"SOURCE_VERIFIED_UV_BEE_OVERLAP_PILOT_WITH_ORIGINAL_LATITUDE_UVB_SAMPLING_AUDIT",
       "source_2016_n":len(original2016),
       "source_2021_n":len(original2021),
       "source_2016_published_UV_mean_latitude_available":sum(
          r["original_2016_mean_source_latitude_or_null"] is not None for r in original2016),
       "source_2016_source_UVB_available":sum(
          r["original_2016_source_mean_UVB_or_null"] is not None for r in original2016),
       "n_2016_published_mean_lat_inside_first_page_sampled_GBIF_lat_range":sum(
          r["original_2016_mean_source_latitude_within_bounded_GBIF_index_page_range_or_unknown"] is True
          for r in original2016),
       "n_2021_Cerrado_UV_taxa_with_model_eligible_sampled_GBIF_country_BR":sum(
          r["original_2021_Cerrado_study_Brazil_in_sampled_eligible_GBIF_country_codes_or_unknown"] is True
          for r in original2021),
       "study_pattern_descriptives":summaries,
       "strict_2016_within_genus_and_published_latitude_pilot":strict_latitude_and_genus_pairs(rows),
       "do_not_treat_source_UV_trait_as_measured_at_all_GBIF_localities":True,
       "first_page_not_a_population_sample_or_native_range":True,
       "no_species_trait_sdm_effect_adjusted_or_significant":True,
       "no_true_plant_fitness_or_bee_use_of_UV_guide":True,
    }


def _read_csv(path):
    with Path(path).open(encoding="utf8",newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--stage50-pilot-csv",required=True)
    ap.add_argument("--original-2016-Gbif-csv",required=True)
    args=ap.parse_args()
    input_pilot=_read_csv(args.stage50_pilot_csv)
    input_2016=_read_csv(args.original_2016_Gbif_csv)
    panel=prepare(input_pilot,input_2016)
    receipt=summarize(panel)
    folder=Path("stage50_published_latitude_UVB_sensitivity")
    folder.mkdir(exist_ok=True)
    with (folder/"source_60_pilot_plant_species_orig2016_UVB_and_sample_sensitivity.csv").open(
         "w",encoding="utf8",newline="") as f:
        data=[{k:(json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v)
               for k,v in r.items()} for r in panel]
        wr=csv.DictWriter(f,fieldnames=list(data[0]))
        wr.writeheader();wr.writerows(data)
    (folder/"source_latitude_sensitivity_receipt.json").write_text(
        json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE50_UV_PATTERN_VS_BOMBUS_SOURCE_LATITUDE_UVB_CONFOUNDING",
          json.dumps(receipt,sort_keys=True,ensure_ascii=False,allow_nan=False))
    print("NO_ADJUSTED_POPULATION_OR_POLLINATOR_FITNESS_TEST")

if __name__=="__main__":
    main()
