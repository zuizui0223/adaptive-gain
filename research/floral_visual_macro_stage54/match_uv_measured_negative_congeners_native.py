"""Stage54: ORIGINAL UV-pattern positive versus *measured UV-uniform* congeners.

Use independent source-verifiable inputs:
- Koski & Ashman 2016: 159 GBIF accepted species, original paper UV state,
  original paper mean latitude/UV-B/temperature per source species.
- Royal Botanic Gardens Kew (WCVP) original accepted/synonym reconciliation:
  153 of those 159 have explicit native extant TDWG WGSRPD L3 area records.
Find measured-opposite states in the SAME original genus with ≥1
original Kew native botanical area overlap; rank pairs by source climate
similarity and greedily prevent multiple pairing of a single plant.

A shared genus/native botanical region is NOT confirmed sister species,
not measured sympatry, not native polygon within the bee HEX, not an
experiment, and NOT proof of pollinator-dependent selection.
No false negative "absence of all visual signals": only measured UV
spatial contrast absent under the 2016 source's 0/1 coding.
"""
from __future__ import annotations
from collections import Counter
import argparse,csv,json,math,statistics
from pathlib import Path

FULL_N=159
WCVP_NATIVE_MAPPED_N=153
SOURCE_N=159
UV_EXPECTED={"0":81,"1":78}
TIERS=(
    ("same_genus_and_overlapping_native_WGSRPD_L3",None,None,None),
    ("source_lat10_UVB1200_temp6",10.0,1200.0,6.0),
    ("source_lat5_UVB700_temp4",5.0,700.0,4.0),
)


def _read(path):
    with Path(path).open(encoding="utf8",newline="") as f:
        return list(csv.DictReader(f))


def _json_list(raw,label):
    try:
        parsed=json.loads(raw)
    except (ValueError,TypeError) as e:
        raise ValueError("NO_GO_WCVP_SOURCE_AREA_JSON_"+label) from e
    if not isinstance(parsed,list) or not all(isinstance(x,str) for x in parsed):
        raise ValueError("NO_GO_WCVP_SOURCE_L3_NOT_STR_LIST_"+label)
    return parsed


def data_join(climate,wcvp,expected=FULL_N):
    if len(climate)!=expected or len(wcvp)!=expected:
        raise ValueError("NO_GO_ORIGINAL_159_SOURCE_SPECIES_FRAME")
    keys_a={r["gbif_accepted_species_key"] for r in climate}
    keyed_b={r["gbif_accepted_species_key"]:r for r in wcvp}
    if len(keys_a)!=expected or len(keyed_b)!=expected or set(keyed_b)!=keys_a:
        raise ValueError("NO_GO_GBIF_ACCEPTED_TAXON_JOIN_UNIQUE_ID")
    if expected==FULL_N and Counter(r["source_2016_UV_pattern"] for r in climate)!=Counter(UV_EXPECTED):
        raise ValueError("NO_GO_PUBLISHED_DIRECTLY_MEASURED_UV_STATES")
    out=[]
    for r in climate:
        p=int(r["source_2016_UV_pattern"])
        b=keyed_b[r["gbif_accepted_species_key"]]
        areas=_json_list(b["WCVP_confirmed_native_extant_WGSRPD_L3_areas"],"NATIVE")
        if b["original_UV_spatial_pattern_binary"] not in (p,str(p)):
            raise ValueError("NO_GO_ORIGINAL_UV_STATUS_CONFLICT_WCVP")
        status=b["WCVP_match_status"]
        if status!="EXACT_AUTHOR_GENUS_SPECIES_SINGLE_WCVP_ACCEPTED_CONCEPT" and areas:
            raise ValueError("NO_GO_NATIVE_AREAS_WITH_UNRESOLVED_WCVP_NAME")
        if len(areas)!=len(set(areas)):
            raise ValueError("NO_GO_DUPLICATED_NATIVE_BOTANICAL_AREA")
        source_lat=float(r["published_latitude_mean"])
        uvb=float(r["published_uvb_mean"])
        t=float(r["published_annual_temp_mean"])
        if not all(math.isfinite(x) for x in (source_lat,uvb,t)):
            raise ValueError("NO_GO_ORIGINAL_SOURCE_CLIMATE_NONFINITE")
        out.append({
            "GBIF_accepted_species_key":r["gbif_accepted_species_key"],
            "UV_2016_original_measured_pattern":p,
            "2016_original_genus":r.get("original_2016_source_genus_or_unknown",""),
            "2016_original_latitude_N":source_lat,
            "2016_original_UVB":uvb,
            "2016_original_mean_temperature_C":t,
            "WCVP_original_accepted_id":b.get("WCVP_accepted_plant_name_id_or_unknown",""),
            "WCVP_original_taxon_match_status":status,
            "WCVP_verified_native_L3_areas":areas,
            "WCVP_native_area_count":len(areas)
        })
    if expected==FULL_N and sum(bool(r["WCVP_verified_native_L3_areas"]) for r in out)!=WCVP_NATIVE_MAPPED_N:
        raise ValueError("NO_GO_AUTHENTIC_WCVP_153_NATIVE_SPECIES_COVERAGE")
    return out


def candidates(records,calipers):
    _,latlim,uvblim,templim=calipers
    uniform=[x for x in records if x["UV_2016_original_measured_pattern"]==0
             and x["WCVP_verified_native_L3_areas"]]
    patterned=[x for x in records if x["UV_2016_original_measured_pattern"]==1
               and x["WCVP_verified_native_L3_areas"]]
    pairs=[]
    for a in patterned:
        for b in uniform:
            if not a["2016_original_genus"] or a["2016_original_genus"]!=b["2016_original_genus"]:
                continue
            overlap=sorted(set(a["WCVP_verified_native_L3_areas"])&
                           set(b["WCVP_verified_native_L3_areas"]))
            if not overlap:
                continue
            diff_lat=abs(a["2016_original_latitude_N"]-b["2016_original_latitude_N"])
            diff_uvb=abs(a["2016_original_UVB"]-b["2016_original_UVB"])
            diff_temp=abs(a["2016_original_mean_temperature_C"]-b["2016_original_mean_temperature_C"])
            if latlim is not None and (diff_lat>latlim or diff_uvb>uvblim or diff_temp>templim):
                continue
            # Source metadata-only ranking, never bees and never pattern outcome
            # beyond requiring opposite original source-measured statuses.
            score=diff_lat/10+diff_uvb/1200+diff_temp/6
            pairs.append({
               "UV_patterned_GBIF_key":a["GBIF_accepted_species_key"],
               "UV_uniform_GBIF_key":b["GBIF_accepted_species_key"],
               "same_original_study_genus":a["2016_original_genus"],
               "n_shared_Kew_verified_native_WGSRPD_L3":len(overlap),
               "shared_original_native_area_codes":overlap,
               "original_published_mean_latitude_gap_deg":diff_lat,
               "original_published_UVB_gap":diff_uvb,
               "original_published_annual_temperature_gap_C":diff_temp,
               "source_environment_ranking_score":score,
               "signal_comparison":"measured UV spatial contrast versus measured UV uniform; NOT all floral signals",
               "not_verified_sister_pair_or_native_sympatry":True,
               "does_not_prove_absence_of_visual_information_in_uniform_flower":True
            })
    return sorted(pairs,key=lambda q:(
        q["source_environment_ranking_score"],
        -q["n_shared_Kew_verified_native_WGSRPD_L3"],
        q["UV_patterned_GBIF_key"],q["UV_uniform_GBIF_key"]))


def nonoverlap(pairs):
    used_pattern=set()
    used_uniform=set()
    out=[]
    for p in pairs:
        a=p["UV_patterned_GBIF_key"]
        b=p["UV_uniform_GBIF_key"]
        if a in used_pattern or b in used_uniform:
            continue
        used_pattern.add(a);used_uniform.add(b)
        out.append(p)
    return out


def analysis(records):
    totals={}
    rows=[]
    for tier in TIERS:
        candidate=candidates(records,tier)
        chosen=nonoverlap(candidate)
        name=tier[0]
        totals[name]={
          "n_eligible_candidate_congener_pairs":len(candidate),
          "n_nonoverlapping_opposite_UV_source_measured_congener_pairs":len(chosen),
          "n_distinct_original_source_genera":len(set(x["same_original_study_genus"] for x in chosen)),
          "n_pair_nativity_overlap_areas_mean":(
              statistics.mean(x["n_shared_Kew_verified_native_WGSRPD_L3"] for x in chosen)
              if chosen else None),
          "pair_source_lat_gap_mean":(
              statistics.mean(x["original_published_mean_latitude_gap_deg"] for x in chosen)
              if chosen else None),
          "source_pairing_not_a_phylogenetic_sister_test":True,
          "unmeasured_visual_modalities_remain_unknown":True
        }
        rows.extend([{"comparison_tier":name,**r} for r in chosen])
    return rows,{
       "status":"ORIGINAL_2016_UV_PATTERN_NEGATIVE_CONGENERIC_CANDIDATE_PAIRS_WITH_KEW_NATIVE_AREAS",
       "source_original_2016_accepted_species":len(records),
       "source_WCVP_species_with_any_native_L3":sum(bool(x["WCVP_verified_native_L3_areas"]) for x in records),
       "source_directly_measured_UV_state_counts":dict(sorted(Counter(x["UV_2016_original_measured_pattern"] for x in records).items())),
       "tiers":totals,
       "only_original_study_UV_positive_and_measured_UV_uniform_negative_are_compared":True,
       "not_actual_sister_species_or_confirmed_native_cooccurrence":True,
       "WCVP_WGSRPD_native_area_is_not_original_spectral_photo_location":True,
       "no_pollinator_richness_model_or_wind_interaction_estimated":True,
       "no_reproductive_fitness_phenotype_from_plant_native_range":True
    }


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--source-2016-159",required=True)
    a.add_argument("--source-WCVP-159",required=True)
    args=a.parse_args()
    joined=data_join(_read(args.source_2016_159),_read(args.source_WCVP_159))
    pairs,summary=analysis(joined)
    output=Path("stage54_UV_measured_negative_congener_candidates")
    output.mkdir(exist_ok=True)
    csvfile=output/"2016_UV_pattern_vs_UV_uniform_native_overlapping_congener_pairs.csv"
    with csvfile.open("w",encoding="utf8",newline="") as f:
        if pairs:
            flat=[{k:json.dumps(v) if isinstance(v,list) else v for k,v in r.items()} for r in pairs]
            w=csv.DictWriter(f,fieldnames=list(flat[0]))
            w.writeheader();w.writerows(flat)
        else:
            f.write("comparison_tier,UV_patterned_GBIF_key,UV_uniform_GBIF_key\n")
    (output/"source_verified_UV_negative_congeners_coverage.json").write_text(
        json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf8")
    print("STAGE54_REAL_SOURCE_MEASURED_UV_NEGATIVE_CONGENERIC_COMPARATORS",
          json.dumps(summary,ensure_ascii=False,sort_keys=True))
    print("NO_MISSING_SIGNAL_AS_ZERO_NO_BOMBUS_OR_WIND_EFFECT")

if __name__=="__main__":
    main()
