"""Stage71B: outcome-blind ecological sampling of optical species × native-region field networks.

Scientific target: original 2024 *petal mean UV reflectance*, not UV spatial nectar guides;
source 2025 corrected v1.3.0 EuPPollNet *recorded bee visits*, not measured true
pollination or plant fitness; independent botanical species-level spectra, not the
field-plant phenotype. No photographic flower-trait extraction.

Do NOT select source study networks on which visitor guilds were observed.
"""
from __future__ import annotations
import argparse,csv,json,sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_literature_macro_stage70"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_literature_macro_stage69"))
import official_wcvp_native_tdwg_original_field_network as st
from historic_tdwg_invalid_geometry_diagnostic import source_polygons_plus_repaired
from ingest_original_corrected_EuPPollNet_network_NHM_spectra import (
    fetch_original, dict_rows, strict_name, is_species, year_of, guild_of, EXPECTED_INTERACTIONS,
)

SOURCE_73_NAMES=73
SOURCE_SPECTRAL_PLANT_NETWORK_UNITS=2557
SOURCE_VISITOR_NETWORKS_WITH_AT_LEAST_TWO_OPTICAL_SPECIES=685


def original_spectra(rows):
    if len(rows)!=SOURCE_73_NAMES:raise ValueError("STAGE71B_SPECTRAL_SOURCE_NOT_73")
    out={}
    for row in rows:
        name=strict_name(row["spectral_original_species_name"])
        if name in out or not name:raise ValueError("STAGE71B_SPECTRAL_NON_UNIQUE_NAME")
        value=float(row["original_2024_true_petal_UV_300_399_percent"])
        vis=float(row["original_2024_true_petal_visible_400_700_percent"])
        if not 0<=value<=100 or not 0<=vis<=100:
            raise ValueError("STAGE71B_SPECTRAL_PHYSICAL_SCALE_NOT_PERCENT")
        out[name]={
            "uv":value,"visible":vis,
            "nhm":row["NHM_literal_species_name_match"]=="YES",
            "accepted_spectra_GBIF":bool(row.get("spectral_GBIF_exact_accepted_key_or_unknown","")),
        }
    return out


def freeze_before_outcome(source_species_units,spectra,acc,states,coords,valid_poly,repair_poly):
    # Only fields defining study/site/original spectrum botanical species are read;
    # no Bombus or other guild counts are used to select the analytical universe.
    bynetwork=defaultdict(dict)
    n_original_spectral_units=0
    for row in source_species_units:
        if row["Stage67_direct_petal_spectra_name_match"]!="1":continue
        tax=strict_name(row["Original_plant_accepted_name_literal"])
        if tax not in spectra:raise ValueError("STAGE71B_SPECTRAL_SOURCE_TAXON_UNAVAILABLE")
        k=(row["Study_id"],row["Network_id"],row["Year_from_original_date"])
        if tax in bynetwork[k]:raise ValueError("STAGE71B_DUPLICATE_NETWORK_TAXON")
        bynetwork[k][tax]={"study":row["Study_id"],
          "sampling_method":row["Author_study_sampling_method"],
          "source_taxa_recorded":row["Author_study_taxa_recorded"],
          "source_DOI":row["Author_study_DOI"]}
        n_original_spectral_units+=1
    if n_original_spectral_units!=SOURCE_SPECTRAL_PLANT_NETWORK_UNITS:
        raise ValueError("STAGE71B_STAGE69_2557_ORIGINAL_SOURCE_UNITS_CHANGED")
    two_species={k:v for k,v in bynetwork.items() if len(v)>=2}
    if len(two_species)!=SOURCE_VISITOR_NETWORKS_WITH_AT_LEAST_TWO_OPTICAL_SPECIES:
        raise ValueError("STAGE71B_685_OUTCOME_BLIND_ORIGINAL_NETWORKS_CHANGED")
    freeze=[];network_status=[];summary=Counter()
    n_primary=0;n_repair=0;study_primary=set();study_repair=set()
    for k,plants in sorted(two_species.items()):
        study,network,year=k
        coord=coords.get(k,set())
        primary_code,primary_location,primary_edge=st.locate_l3(coord,valid_poly)
        secondary_code,secondary_location,secondary_edge=st.locate_l3(coord,repair_poly)
        natives_primary=[]
        natives_repair=[]
        for name in sorted(plants):
            source_trait=spectra[name]
            primary_origin=st.classify_origin(name,primary_code,acc,states)
            secondary_origin=st.classify_origin(name,secondary_code,acc,states)
            primary_ok=primary_origin=="WCVP_NATIVE_L3_COMPATIBLE" and not primary_edge
            repaired_ok=secondary_origin=="WCVP_NATIVE_L3_COMPATIBLE" and not secondary_edge
            if primary_ok:natives_primary.append(name)
            if repaired_ok:natives_repair.append(name)
            freeze.append({
              "Study_id":study,"Network_id":network,"Year":year,
              "original_plant_species":name,
              "petal_UV_300_399nm_mean_reflectance_percent_original_garden":source_trait["uv"],
              "petal_visible_400_700nm_mean_reflectance_percent_original_garden":source_trait["visible"],
              "NHM_text_source_exact_literal":int(source_trait["nhm"]),
              "spectra_original_GBIF_strict_accepted_species":int(source_trait["accepted_spectra_GBIF"]),
              "source_sampling_method":plants[name]["sampling_method"],
              "author_source_taxa_recorded_scope":plants[name]["source_taxa_recorded"],
              "original_field_network_unique_coordinates":len(coord),
              "original_valid_polygon_TDWG_L3":primary_code,
              "original_valid_polygon_site_quality":primary_location,
              "repaired_polygon_TDWG_L3":secondary_code,
              "repaired_polygon_site_quality":secondary_location,
              "original_WCVP_native_area_primary_status":primary_origin,
              "original_WCVP_native_area_repaired_status":secondary_origin,
              "cohort_primary_WCVP_regional_native_eligible":int(primary_ok),
              "cohort_geo_repair_WCVP_regional_native_eligible":int(repaired_ok),
              "native_status_not_same_field_plant":"SOURCE_REGION_COMPATIBILITY_ONLY",
            })
            summary["primary_plant_"+primary_origin]+=1
            summary["repaired_plant_"+secondary_origin]+=1
        all_cov=lambda names: (len(names)>=2 and
            len({n.split()[0] for n in names})>=2 and
            len({spectra[n]["uv"] for n in names})>=2)
        primary=all_cov(natives_primary)
        repaired=all_cov(natives_repair)
        n_primary+=primary;n_repair+=repaired
        if primary:study_primary.add(study)
        if repaired:study_repair.add(study)
        network_status.append({
          "Study_id":study,"Network_id":network,"Year":year,
          "source_Spectral_species_recorded":len(plants),
          "source_Spectral_species_region_native_primary":len(natives_primary),
          "source_Spectral_species_region_native_repaired":len(natives_repair),
          "primary_original_geometry_study_eligible":int(primary),
          "geo_repair_geometry_study_eligible":int(repaired),
          "original_primary_L3_code":primary_code,
          "original_geo_repair_L3_code":secondary_code,
          "original_primary_geometry_status":primary_location,
          "original_geo_repair_geometry_status":secondary_location,
          "selection_used_Bombus_or_other_guild_outcome":0,
        })
    receipt={
      "schema":"stage71b_original_spectral_36_species_visit_network_native_outcome_blind_frame",
      "source_spectral_original_taxon_count":len(spectra),
      "source_original_spectral_species_network_year_units":n_original_spectral_units,
      "networks_with_at_least_two_original_spectrometer_species_before_outcomes":len(two_species),
      "source_spectra_species_network_x_network_unselected_units":len(freeze),
      "source_original_networks_native_area_primary_without_guild_outcome_filter":n_primary,
      "source_original_networks_native_area_repaired_sensitivity_without_guild_outcome_filter":n_repair,
      "source_original_studies_native_area_primary_without_guild_outcome_filter":len(study_primary),
      "source_original_studies_native_area_repaired_without_guild_outcome_filter":len(study_repair),
      "unselected_WCVP_region_match_classes":dict(summary),
      "source_guild_information_used_in_cohort_selection":False,
      "source_plant_visited_is_conditioned_on_at_least_one_record":True,
      "original_petal_spectra_measured_in_field_population":False,
      "source_DTWG_polygon_repair_is_diagnostic_only":True,
      "source_visitor_absence_or_fitness_established":False,
    }
    return freeze,network_status,receipt


def read_strict_bee_events(cohort_rows):
    # Calculate outcomes *after* the native-region/network set has been frozen.
    eligible={(r["Study_id"],r["Network_id"],r["Year"],r["original_plant_species"])
              for r in cohort_rows}
    events=defaultdict(Counter);status=Counter()
    raw=fetch_original("Interaction_data.csv.gz")
    records=0
    for _,r in dict_rows(raw,compressed=True):
        records+=1
        study=r["Study_id"].strip();network=r["Network_id"].strip()
        year=year_of(r["Date"]);name=strict_name(r["Plant_accepted_name"])
        k=(study,network,year,name)
        if k not in eligible:continue
        status["source_candidate_plant_record_rows"]+=1
        if not is_species(r):
            status["source_candidate_non_species_or_uncertain_plant_rows"]+=1
            continue
        order=r.get("Pollinator_order","").strip().casefold()
        if order!="hymenoptera":continue
        status["source_candidate_hymenoptera_rows"]+=1
        if r.get("Pollinator_rank","").strip().casefold()!="species":
            status["source_candidate_bee_non_species_rank"]+=1
            continue
        if r.get("Pollinator_unsure_id","").strip().casefold() in ("yes","true","1","y"):
            status["source_candidate_bee_unsure_taxon"]+=1
            continue
        g=guild_of(r)
        if g=="Bombus":
            events[k]["Bombus"]+=1
        elif g=="other_bee":
            events[k]["other_bee"]+=1
        else:
            status["source_candidate_nonbee_hymenoptera_or_unknown_family"]+=1
    if records!=EXPECTED_INTERACTIONS:
        raise ValueError("STAGE71B_NOT_CORRECTED_EUPPOLLNET_SOURCE_623476")
    return events,{"source_actual_corrected_visit_rows":records,
                   "source_guild_classification_checks":dict(status)}


def attach_outcomes(freeze_rows,network_status,raw_events):
    net={ (n["Study_id"],n["Network_id"],n["Year"]):n for n in network_status }
    outcome=[]
    meta=Counter()
    strict_studies=defaultdict(set)
    strict_taxa=defaultdict(set)
    bynetwork=defaultdict(list)
    for r in freeze_rows:
        x=dict(r)
        k=(r["Study_id"],r["Network_id"],r["Year"],r["original_plant_species"])
        observed=raw_events.get(k,Counter())
        x["source_bumblebee_species_rank_records"]=observed["Bombus"]
        x["source_other_bee_species_rank_records"]=observed["other_bee"]
        x["source_total_accepted_species_rank_bee_records"]=observed["Bombus"]+observed["other_bee"]
        x["source_no_bee_record_is_not_biological_absence"]=1
        x["source_bee_recorded_share_if_denominator_positive"]=(
            observed["Bombus"]/(observed["Bombus"]+observed["other_bee"])
            if observed["Bombus"]+observed["other_bee"] else "")
        outcome.append(x)
        nk=k[:3]
        bynetwork[nk].append(x)
    for mode in ("primary","repaired"):
        column="cohort_primary_WCVP_regional_native_eligible" if mode=="primary" else "cohort_geo_repair_WCVP_regional_native_eligible"
        netcol="primary_original_geometry_study_eligible" if mode=="primary" else "geo_repair_geometry_study_eligible"
        chosen=[n for n in network_status if n[netcol]==1]
        studyset={n["Study_id"] for n in chosen}
        taxa={r["original_plant_species"] for n in chosen
              for r in bynetwork[n["Study_id"],n["Network_id"],n["Year"]] if r[column]==1}
        mixedbee=0;bothbee=0;bothbee3=0;beeobserved=0;guildzero=0
        for n in chosen:
            rr=[r for r in bynetwork[n["Study_id"],n["Network_id"],n["Year"]] if r[column]==1]
            q=[r for r in rr if r["source_total_accepted_species_rank_bee_records"]>0]
            q3=[r for r in rr if r["source_total_accepted_species_rank_bee_records"]>=3]
            if len(q)>=2:bothbee+=1
            if len(q3)>=2:bothbee3+=1
            if sum(r["source_total_accepted_species_rank_bee_records"] for r in rr)>0:beeobserved+=1
            if not q:guildzero+=1
            if sum(r["source_bumblebee_species_rank_records"] for r in rr)>0 and sum(
                r["source_other_bee_species_rank_records"] for r in rr)>0:
                mixedbee+=1
        meta[mode]={
          "outcome_blind_source_networks":len(chosen),
          "source_distinct_study_ids":len(studyset),
          "source_distinct_spectrometer_species":len(taxa),
          "networks_with_any_strict_species_rank_bee_event":beeobserved,
          "networks_with_two_or_more_native_spectral_species_each_any_strict_bee":bothbee,
          "networks_with_two_or_more_native_spectral_species_each_at_least_3_strict_bee":bothbee3,
          "networks_with_Bombus_and_nonBombus_bee_events_post_selection_diagnostic":mixedbee,
          "networks_without_any_strict_species_rank_bee_event":guildzero,
          "cross_species_uv_slope_identified_under_species_fixed_effects":False,
        }
    return outcome,dict(meta)


def write(rows,path):
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    p=argparse.ArgumentParser()
    for flag in ("--stage69-network-units","--stage68-original-spectra","--wcvp-zip","--tdwg-geojson","--outdir"):
        p.add_argument(flag,required=True,type=Path)
    a=p.parse_args()
    spectral=original_spectra(st.read_csv(a.stage68_original_spectra))
    source=st.read_csv(a.stage69_network_units)
    targets=set(spectral)
    accepted,states,wcvp=st.load_wcvp_exact_species(a.wcvp_zip,targets)
    valid,geo=st.read_tdwg_geojson(a.tdwg_geojson)
    _,repaired,notrepaired=source_polygons_plus_repaired(a.tdwg_geojson)
    if len(repaired)!=19 or notrepaired:
        raise ValueError("STAGE71B_ORIGINAL_19_TDWG_INVALID_SHAPES_NO_LONGER_REPAIRABLE")
    locations,locinfo=st.source_network_coordinates()
    frozen,networks,design=freeze_before_outcome(
        source,spectral,accepted,states,locations,valid,
        valid+[(code,g) for code,g,_ in repaired])
    # frozen and network designs are now independent of the visitor guild outcome.
    measured,visits=read_strict_bee_events(frozen)
    with_y,outcome=attach_outcomes(frozen,networks,measured)
    report={**design,
      "source_WCVP_accepted_species":wcvp,
      "source_original_TDWG_geometry":geo,
      "source_original_field_site_keys":locinfo,
      "original_strict_bee_record_audit":visits,
      "post_freeze_guild_observability":outcome,
      "analysis_trait_variable":"source_measured_garden_petal_UV_reflectance_300_399_percent",
      "analysis_biological_endpoint":"relative_species_rank_Bombus_share_among_observed_bees",
      "stage69_156_and_stage70_73_135_outcome_selected_sets_NOT_reused":True,
      "source_garden_vs_field_phenotype_transfer_unverified":True,
      "plant_species_fixed_effect_identifies_species_constant_UV_slope":False,
      "no_causal_bumblebee_adaptation_or_plant_fitness_result":True}
    a.outdir.mkdir(exist_ok=True,parents=True)
    write(frozen,a.outdir/"original_species_site_native_cohort_FROZEN_BEFORE_GUILD.csv")
    write(networks,a.outdir/"original_study_network_native_sample_frame_NOT_GUILD_FILTERED.csv")
    write(with_y,a.outdir/"original_strict_species_bee_observations_ONLY_AFTER_FREEZE.csv")
    (a.outdir/"source_unselected_native_recorded_bee_audit.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE71B_REAL_UNSELECTED_NATIVE_SPECTRA_VISITOR_COHORT",
          json.dumps(report,sort_keys=True))
    print("NO_PHOTOS_NO_PRE_GUILD_SELECTION_NO_TRUE_POLLINATOR_ABSENCE_NO_ADAPTATION")


if __name__=="__main__":
    main()
