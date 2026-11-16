"""Stage52: original Koski 2016 UV signal × modelled bee guild composition.

Original source paper states mean species latitude 21.07–76.49 N:
https://doi.org/10.1111/nph.13921 . Stage52 southern search is a
negative-control only. Inputs are the precommitted 60 accepted-species
original-source latitude pilot and original bee source HEX model.
The modelled Bombus/all-bee ratio is not Bombus abundance, pollinator
availability, UV guide use or plant fitness. No p-values: lineage,
GBIF effort and source-study exchangeability have not been validated.
"""
from __future__ import annotations
import argparse,csv,json,statistics
from pathlib import Path
from collections import Counter

def read_rows(path):
    with Path(path).open(encoding="utf8",newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=60 or len({r["gbif_accepted_species_key"] for r in rows})!=60:
        raise ValueError("NO_GO_PRESPECIFIED_60_UV_SOURCE_SPECIES")
    result=[]
    for r in rows:
        pattern=int(r["original_source_UV_pattern_binary"])
        latbin=int(r["original_latitude_tercile_within_pattern"])
        if pattern not in (0,1) or latbin not in (1,2,3):
            raise ValueError("NO_GO_SOURCE_UV_OR_LATITUDE_STRATA")
        try:
            n=json.loads(r["source_hemisphere_N_GBIF"])
            s=json.loads(r["source_hemisphere_S_GBIF"])
        except (KeyError,ValueError,TypeError) as err:
            raise ValueError("NO_GO_SOURCE_HEMISPHERE_SCHEMA") from err
        count=int(n["n_qualified_original_source_bee_HEX_records"])
        hexes=int(n["n_distinct_visited_eligible_bee_hex_cells"])
        south_n=int(s["n_qualified_original_source_bee_HEX_records"])
        south_hex=int(s["n_distinct_visited_eligible_bee_hex_cells"])
        if count<0 or hexes<0 or south_n<0 or south_hex<0:
            raise ValueError("NO_GO_NEGATIVE_GBIF_QUALITY_COUNTS")
        good=count>=5 and hexes>=2
        strict=count>=10 and hexes>=3
        b=n.get("modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null")
        allbee=n.get("modelled_all_bee_names_per_visited_bee_hex_equal_cell_mean_or_null")
        if good:
            if b is None or allbee is None or not 0<=b<=allbee or allbee<=0:
                raise ValueError("NO_GO_BOMBUS_GUILD_NUMERIC_SOURCE")
        else:
            b=None;allbee=None
        result.append({
            "gbif_accepted_species_key":r["gbif_accepted_species_key"],
            "original_UV_pattern_binary":pattern,
            "source_latitude_tercile":latbin,
            "original_author_genus":r.get("original_source_genus",""),
            "source_mean_latitude_N":float(r["original_mean_published_latitude_positive_deg"]),
            "source_mean_UVB":float(r["original_source_UVB"]),
            "source_mean_temperature":float(r["original_source_mean_temperature"]),
            "n_qualified_N_first_page_GBIF_records":count,
            "n_visited_N_author_eligible_hex":hexes,
            "n_qualified_S_negative_control_GBIF_records":south_n,
            "n_visited_S_author_eligible_hex":south_hex,
            "viable_N_5records_2hex":good,
            "strict_N_10records_3hex":strict,
            "source_modelled_Bombus_taxa_N":b,
            "source_modelled_all_bee_taxa_N":allbee,
            "source_modelled_Bombus_share_proxy_N":b/allbee if good else None,
            "source_UV_phenotype_not_measured_at_GBIF_points":True
        })
    counts=Counter((x["original_UV_pattern_binary"],x["source_latitude_tercile"]) for x in result)
    if len(counts)!=6 or any(c!=10 for c in counts.values()):
        raise ValueError("NO_GO_ORIGINAL_UV_LATITUDINAL_BALANCE_CHANGED")
    return result

METRICS=("source_modelled_Bombus_taxa_N","source_modelled_all_bee_taxa_N",
         "source_modelled_Bombus_share_proxy_N")

def contrast(rows,metric):
    a=[x[metric] for x in rows if x["original_UV_pattern_binary"]==1
       and x[metric] is not None]
    b=[x[metric] for x in rows if x["original_UV_pattern_binary"]==0
       and x[metric] is not None]
    return {"n_pattern":len(a),"n_uniform":len(b),
            "pattern_mean":statistics.mean(a) if a else None,
            "uniform_mean":statistics.mean(b) if b else None,
            "pattern_minus_uniform":(statistics.mean(a)-statistics.mean(b)) if a and b else None}

def summarize(rows):
    viable=[x for x in rows if x["viable_N_5records_2hex"]]
    strict=[x for x in rows if x["strict_N_10records_3hex"]]
    groups=[]
    for label,selection in [
       ("all_viable_N",viable),
       ("strict_N",strict),
       ("Potentilla_viable_N",[r for r in viable if r["original_author_genus"]=="Potentilla"]),
       *[(f"latitude_tercile_{i}",[r for r in viable if r["source_latitude_tercile"]==i])
         for i in (1,2,3)]
    ]:
        groups.append({"stratum":label,"metrics":{m:contrast(selection,m) for m in METRICS}})
    loo={}
    for metric in METRICS:
        deltas=[contrast(viable[:i]+viable[i+1:],metric)["pattern_minus_uniform"]
                for i in range(len(viable))]
        deltas=[v for v in deltas if v is not None]
        loo[metric]={"n":len(deltas),"min":min(deltas) if deltas else None,
                     "max":max(deltas) if deltas else None,
                     "sign_stable_all_single_species_deletions":(
                         all(x>0 for x in deltas) or all(x<0 for x in deltas))
                         if deltas else False}
    return {
       "status":"SOURCE_2016_UV_ORIGINAL_N_LAT_GUILD_COMPOSITION_DESCRIPTIVE",
       "n_prespecified_source_species":len(rows),
       "n_viable_source_N":len(viable),
       "n_viable_strict_source_N":len(strict),
       "n_source_genus_Potentilla_viable":sum(
           r["original_author_genus"]=="Potentilla" for r in viable),
       "n_source_south_negative_control_viable":sum(
           r["n_qualified_S_negative_control_GBIF_records"]>=5 and
           r["n_visited_S_author_eligible_hex"]>=2 for r in rows),
       "stratum_species_equal_descriptive_contrasts":groups,
       "single_source_species_deletion_robustness":loo,
       "original_2016_article_states_source_latitudes_21_07_to_76_49_N":True,
       "source_Bombus_fraction_proxy_is_ratio_of_modelled_species_name_richness":True,
       "source_GBIF_index_page_not_native_range_or_source_UV_measurement_location":True,
       "no_species_exchangeable_null_or_phylogeny_climate_adjustment":True,
       "no_floral_signal_use_by_bee_or_reproductive_fitness_measurement":True
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-hemisphere-pilot",required=True)
    args=p.parse_args()
    rows=read_rows(args.source_hemisphere_pilot)
    summary=summarize(rows)
    out=Path("stage52_guild_composition")
    out.mkdir(exist_ok=True)
    with (out/"original_60_UV_taxa_Bombus_share_source_model.csv").open(
        "w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    (out/"guild_composition_source_2016_UV_robustness.json").write_text(
        json.dumps(summary,indent=2,ensure_ascii=False,sort_keys=True,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE52_UV_VS_MODELLED_BOMBUS_RELATIVE_GUILD_DESCRIPTIVES",
          json.dumps(summary,ensure_ascii=False,sort_keys=True))
    print("NO_UV_BOMBUS_BEHAVIOURAL_OR_CAUSAL_EFFECT")

if __name__=="__main__":
    main()
