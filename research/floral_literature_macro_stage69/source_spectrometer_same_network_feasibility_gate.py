"""Stage69B: prospectively audit whether original optical taxa co-occur
within *the same* corrected EuPPollNet observation networks.

No outcome is fitted, no p-value, no source-site native or phenotype equivalence
assumed. This is the design/independence gate for any later field ecology test.
"""
from __future__ import annotations
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

MIN_VISITS_EACH = 3
MIN_ORIGINAL_UV_DIFFERENCE_PERCENT = 1.0
MIN_SOURCE_STUDIES_FOR_FURTHER_EXPLORATION = 3


def read(path):
    with Path(path).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def key(name):
    return " ".join(str(name).strip().casefold().split())


def actual_spectra_by_name(rows):
    if len(rows)!=73 or sum(r["NHM_literal_species_name_match"]=="YES" for r in rows)!=55:
        raise ValueError("STAGE69B_ORIGINAL_STAGE68_SOURCE_73_55_GRAIN_FAILED")
    out={}
    for s in rows:
        name=key(s["spectral_original_species_name"])
        if not name or name in out:
            raise ValueError("STAGE69B_DUPLICATE_OR_BLANK_SPECTRAL_SPECIES")
        uv=float(s["original_2024_true_petal_UV_300_399_percent"])
        vis=float(s["original_2024_true_petal_visible_400_700_percent"])
        if not(0<=uv<=100 and 0<=vis<=100):
            raise ValueError("STAGE69B_ORIGINAL_PHYSICAL_SPECTRAL_VALUES_INVALID")
        out[name]={"uv":uv,"vis":vis,"nhm":s["NHM_literal_species_name_match"]=="YES",
                   "taxonomic_status":s.get("accepted_taxonomy_scope","")}
    return out


def inspect(network_rows,source_spectra):
    spectra=actual_spectra_by_name(source_spectra)
    network=defaultdict(dict)
    n_optical_rows=0
    for r in network_rows:
        if r["Stage67_direct_petal_spectra_name_match"]!="1":
            continue
        name=key(r["Original_plant_accepted_name_literal"])
        if name not in spectra:
            raise ValueError("STAGE69B_ORIGINAL_SPECTRAL_TAXON_NOT_AUTHENTIC")
        n_optical_rows+=1
        unit=(r["Study_id"],r["Network_id"],r["Year_from_original_date"])
        if name in network[unit]:
            raise ValueError("STAGE69B_DUPLICATE_SOURCE_TAXON_WITHIN_NETWORK")
        network[unit][name]=r
    if n_optical_rows!=2557:
        raise ValueError(f"STAGE69B_ORIGINAL_NETWORK_2557_SOURCE_UNITS_CHANGED_{n_optical_rows}")
    receipts=[]
    studies_all_multi=set()
    studies_optical_mixed=set()
    studies_native_valid=set()
    names_multi=set()
    names_mixed=set()
    across_same_genus=0
    for (study,net,year),plants in sorted(network.items()):
        allnames=sorted(plants)
        n_all=len(allnames)
        n_both=sum(spectra[n]["nhm"] for n in allnames)
        genera={n.split()[0] for n in allnames}
        bombus=sum(int(plants[n].get("n_observed_Bombus",0)) for n in allnames)
        nonbombus=sum(sum(int(plants[n].get("n_observed_"+g,0)) for g in (
              "other_bee","other_hymenoptera","diptera","lepidoptera","coleoptera"))
              for n in allnames)
        eligible=[
            n for n in allnames if sum(int(plants[n].get("n_observed_"+g,0))
                                      for g in ("Bombus","other_bee","other_hymenoptera",
                                                "diptera","lepidoptera","coleoptera","other_or_unknown"))
                                      >=MIN_VISITS_EACH
        ]
        eligible_both=[n for n in eligible if spectra[n]["nhm"]]
        novel_genera={n.split()[0] for n in eligible_both}
        uv_delta=(max(spectra[n]["uv"] for n in eligible_both) -
                  min(spectra[n]["uv"] for n in eligible_both)) if len(eligible_both)>=2 else 0.0
        source_same_network_two=(n_both>=2)
        strict_within=(
            len(eligible_both)>=2 and len(novel_genera)>=2
            and bombus>0 and nonbombus>0
            and uv_delta>=MIN_ORIGINAL_UV_DIFFERENCE_PERCENT
        )
        # IMPORTANT: this does not establish same-population optical observations;
        # the original 2024 petal spectrum came from a botanical garden.
        if n_all>=2:
            studies_all_multi.add(study)
            names_multi.update(allnames)
        if strict_within:
            studies_optical_mixed.add(study)
            names_mixed.update(eligible_both)
        if source_same_network_two and len(genera)==1:
            across_same_genus+=1
        receipts.append({
            "Study_id":study, "Network_id":net,"Year":year,
            "n_source_spectrometer_species_observed":n_all,
            "n_original_source_NHM_spectral_species":n_both,
            "n_source_spectrometer_genera":len(genera),
            "n_both_NHM_spectra_with_at_least_3_visits":len(eligible_both),
            "n_distinct_genera_eligible":len(novel_genera),
            "n_source_Bombus_records_in_spectral_plant_set":bombus,
            "n_source_nonBombus_visitor_records_in_spectral_plant_set":nonbombus,
            "within_network_spectral_UV_range_percent_point_eligible":round(uv_delta,5),
            "two_real_spectrometer_names_in_one_network":int(n_all>=2),
            "two_real_spectrometer_NHM_names_in_one_network":int(source_same_network_two),
            "eligible_two_different_genera_Bombus_and_other_UV_range":int(strict_within),
            "original_optics_same_field_site_and_individual":"NOT_ESTABLISHED",
            "native_source_range":"NOT_VERIFIED",
        })
    n_multi=sum(x["two_real_spectrometer_names_in_one_network"] for x in receipts)
    n_multi_nhm=sum(x["two_real_spectrometer_NHM_names_in_one_network"] for x in receipts)
    n_strict=sum(x["eligible_two_different_genera_Bombus_and_other_UV_range"] for x in receipts)
    summary={
        "schema":"stage69b_corrected_EuPPollNet_source_spectra_same_network_feasibility",
        "original_source_spectrum_name_universe":len(spectra),
        "source_spectrum_plant_network_year_units":n_optical_rows,
        "networks_containing_at_least_one_source_spectrometer_species":len(receipts),
        "networks_containing_at_least_two_source_spectrometer_species":n_multi,
        "networks_containing_at_least_two_spectrometer_and_NHM_text_species":n_multi_nhm,
        "networks_containing_at_least_two_spectral_species_one_genus":across_same_genus,
        "independent_Study_ids_with_at_least_two_source_spectrometer_species":len(studies_all_multi),
        "distinct_spectral_taxa_in_multi_optical_networks":len(names_multi),
        "exploratory_strict_networks_min3_each_two_genera_Bombus_other_UVrange1pt":n_strict,
        "independent_Study_ids_with_strict_exploratory_networks":len(studies_optical_mixed),
        "distinct_spectral_taxa_in_strict_exploratory_networks":len(names_mixed),
        "enough_independent_studies_to_consider_descriptive_study_holdout":
             len(studies_optical_mixed)>=MIN_SOURCE_STUDIES_FOR_FURTHER_EXPLORATION,
        "source_field_observed_true_absences":False,
        "source_study_NHM_and_spectra_field_same_population":False,
        "native_distribution_and_wind_coincident_source":False,
        "causal_signal_guild_selection_ready":False,
        "fitted_beta_or_p_value":None,
    }
    return receipts,summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-network-plant-guilds",type=Path,required=True)
    p.add_argument("--original-73-spectra-text",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    rows,rec=inspect(read(a.original_network_plant_guilds),read(a.original_73_spectra_text))
    a.outdir.mkdir(exist_ok=True,parents=True)
    with (a.outdir/"original_same_network_measured_optical_pair_opportunity.csv").open(
      "w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    (a.outdir/"original_source_optical_within_network_design_gate.json").write_text(
       json.dumps(rec,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE69B_REAL_SOURCE_SPECTRAL_NETWORK_MATCH_FEASIBILITY",
          json.dumps(rec,sort_keys=True))
    print("NO_SAME_FIELD_SPECTRAL_PHENOTYPE_NO_NATIVE_MATCH_NO_FITTED_CAUSAL_BETA")


if __name__=="__main__":
    main()
