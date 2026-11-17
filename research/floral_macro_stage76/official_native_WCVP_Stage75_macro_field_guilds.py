"""Stage76 MACRO: official plant native range × field network source hue × real bee guilds.

NO PHOTOS. This is the Stage75 59,369 botanical text x corrected 54-study,
1,864-network continental observational macro analysis, now cross-validating
the botanical *regional-native* origin of all species using ORIGINAL official
Kew WCVP accepted species×TDWG-L3 area and exact EuPPollNet field coordinates.

The historical 19 source-invalid TDWG polygons were conservatively rejected
in Stage70, repaired geometry is a SEPARATE sensitivity, not primary.

Critical inference ceilings:
- WCVP native in a TDWG region does NOT establish any individual is native.
- WCVP unlisted region does NOT establish absence or introduction.
- Original hue words are not a spectrometer-derived floral UV guide.
- Recorded Bombus is a visitation channel, NOT site Bombus SDM suitability,
  pollen deposition, preference, or fitness.
- GBIF-based island Bombus hypervolume old artifact expired October 10 2026;
  this stage DOES NOT relabel its stale predictions as verified current data.
- Flower colour selection must precede looking at guild visit records.
"""
from __future__ import annotations

import argparse,csv,hashlib,json,sys
from pathlib import Path
from collections import Counter,defaultdict

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_literature_macro_stage70"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage75"))
import official_wcvp_native_tdwg_original_field_network as native
from historic_tdwg_invalid_geometry_diagnostic import source_polygons_plus_repaired
from authentic_continental_text_signal_guild_macro import (
    null_score_pair,study_block_summary,key
)

STAGE75_MAIN_SHA="e63f97c8cafc9d649531b247e5f0559f8c399e0cb72dfa503178806854739d93"
STAGE75_HUES_SHA="c55836c115b013ecbe41d00c20ac9348913ce4edbc23178ab3249de024314de5"
STAGE69_NETWORKS_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
CONTRASTS={
    "yellow_vs_white":("yellow","white",345),
    "yellow_vs_purple":("yellow","purple",65),
}
MODES=("original_valid_polygon","repaired_invalid_polygon_sensitivity")
ORIGIN_CEILING="REGIONAL_COMPATIBILITY_NOT_SOURCE_FIELD_INDIVIDUAL_NATIVENESS"

def verify_sha(path,want):
    h=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if h!=want:raise ValueError("STAGE76_SOURCE_DERIVED_SHA_CHANGED")
    return h

def read(path):
    with Path(path).open("r",encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def original_species_catalog(stage69_rows):
    accepted=set()
    with_nhm=set()
    with_colour=set()
    for row in stage69_rows:
        tax=key(row["Original_plant_accepted_name_literal"])
        if not tax:raise ValueError("STAGE76_SOURCE_ACCEPTED_PLANT_LABEL_MISSING")
        accepted.add(tax)
        if row["NHM_text_name_match"]=="1":
            with_nhm.add(tax)
        if row["NHM_colour_text_recorded"]=="1":
            with_colour.add(tax)
    if len(accepted)!=1408 or len(with_nhm)!=963 or len(with_colour)!=809:
        raise ValueError(
            f"STAGE76_ORIGINAL_SOURCE_FRAME_CHANGED_{len(accepted)}_"
            f"{len(with_nhm)}_{len(with_colour)}")
    if not with_colour<=with_nhm:
        raise ValueError("STAGE76_COLOR_SOURCE_NOT_IN_ORIGINAL_NHM")
    return accepted,with_nhm,with_colour

def classify_site_networks(coords,valid,repaired):
    result={}
    for k,locations in coords.items():
        code,status,edge=native.locate_l3(locations,valid)
        code2,status2,edge2=native.locate_l3(locations,repaired)
        result[k]={
            "original_valid_polygon":(code,status,edge),
            "repaired_invalid_polygon_sensitivity":(code2,status2,edge2),
            "original_site_coordinates_in_source":len(locations)
        }
    return result

def original_site_plant_range_coverage(stage69,contexts,acc,states,catalogs):
    _,nhm,col=catalogs
    status=defaultdict(Counter)
    taxa_by_status=defaultdict(lambda:defaultdict(set))
    for row in stage69:
        s=row["Study_id"];n=row["Network_id"];y=row["Year_from_original_date"]
        tax=key(row["Original_plant_accepted_name_literal"])
        k=(s,n,y)
        ctx=contexts.get(k)
        if ctx is None:raise ValueError("STAGE76_SOURCE_SITE_NOT_IN_CORRECTED_ORIGINAL_NETWORK")
        for mode in MODES:
            code,quality,edge=ctx[mode]
            origin=native.classify_origin(tax,code,acc,states)
            if origin=="WCVP_NATIVE_L3_COMPATIBLE" and edge:
                status[mode]["WCVP_NATIVE_L3_NEAR_BORDER_SENSITIVITY_EXCLUDED"]+=1
            elif origin=="WCVP_NATIVE_L3_COMPATIBLE":
                status[mode]["WCVP_NATIVE_L3_COMPATIBLE_BORDER_SAFE"]+=1
            else:
                status[mode][origin]+=1
            subset="original_exact_NHM_colour" if tax in col else (
                 "original_exact_NHM_text" if tax in nhm else "original_without_NHM_name")
            status[mode]["source_plant_network_units_"+subset]+=1
            if origin=="WCVP_NATIVE_L3_COMPATIBLE" and not edge:
                taxa_by_status[mode][subset].add(tax)
    return {mode:{
        "original_plant_network_unit_counts_by_source_area_and_trait":dict(status[mode]),
        "native_L3_compatible_border_safe_distinct_plants_by_source_trait_scope":{
            scope:len(taxa) for scope,taxa in taxa_by_status[mode].items()},
        "zero_plant_network_units_proves_true_visitor_absence":False
        } for mode in MODES}

def define_pre_guild_native_hue_frames(hues,contexts,acc,states):
    """This function intentionally reads NO source B/O visitor fields at all."""
    frozen=defaultdict(lambda:defaultdict(list))
    audits=defaultdict(Counter)
    for r in hues:
        contrast=r["color_contrast"]
        if contrast not in CONTRASTS:
            raise ValueError("STAGE76_SOURCE_ORIGINAL_HUE_PAIR_NOT_IN_FROZEN_FRAME")
        k=(r["Study_id"],r["Network_id"],r["Year"])
        tax=key(r["species"])
        if key(r["genus"])!=tax.split(" ")[0]:
            raise ValueError("STAGE76_ORIGINAL_HUE_GENUS_NOT_EXPECTED")
        if r["hue"] not in CONTRASTS[contrast][:2]:
            raise ValueError("STAGE76_SOURCE_HUE_CONTRAST_MISMATCH")
        ctx=contexts.get(k)
        if ctx is None:raise ValueError("STAGE76_FIELD_SITE_YEAR_NETWORK_MISSING")
        for mode in MODES:
            code,geostatus,edge=ctx[mode]
            state=native.classify_origin(tax,code,acc,states)
            audit_state=state
            if state=="WCVP_NATIVE_L3_COMPATIBLE" and edge:
                audit_state="WCVP_NATIVE_L3_NEAR_BORDER_SENSITIVITY_EXCLUDED"
            audits[(mode,contrast)][audit_state]+=1
            if state=="WCVP_NATIVE_L3_COMPATIBLE" and not edge:
                frozen[(mode,contrast)][k].append({
                  # Explicit name/site/guild-outcome-INDEPENDENT source fields.
                  "Study_id":r["Study_id"],"Network_id":r["Network_id"],
                  "Year":r["Year"],"species":tax,
                  "genus":tax.split()[0],"hue":r["hue"],
                  "original_sampling_method":r["original_sampling_method"],
                  "original_reported_pollinator_taxa_scope":r["original_reported_pollinator_taxa_scope"],
                  "Bioregion":r["Bioregion"],"Country":r["Country"],
                  "EuPPollNet_habitat":r["EuPPollNet_habitat"],
                  "source_TDWG_L3":code,"source_polygon_status":geostatus,
                  "source_WCVP_native_region_not_individual":True,
                })
    # For each contrast, keep only >=2 positive SOURCE hue categories in
    # the same recorded field network. Still ZERO knowledge of bee outcomes.
    selected={}
    for contrast,(_,_,expected) in CONTRASTS.items():
        original_nets={ (r["Study_id"],r["Network_id"],r["Year"])
                        for r in hues if r["color_contrast"]==contrast}
        if len(original_nets)!=expected:
            raise ValueError(f"STAGE76_STAGE75_PREGUILD_SOURCE_NETWORK_COUNT_CHANGED_{contrast}")
        for mode in MODES:
            k=(mode,contrast)
            elected={net:plants for net,plants in frozen[k].items()
                     if {p["hue"] for p in plants}==set(CONTRASTS[contrast][:2])}
            selected[k]=elected
            audits[k]["source_original_networks_with_both_hues_before_WCVP"]=len(original_nets)
            audits[k]["source_original_net_after_WCVP_native_before_guild"]=len(elected)
            audits[k]["source_studies_after_WCVP_native_before_guild"]=len({n[0] for n in elected})
            audits[k]["source_plant_species_after_WCVP_native_before_guild"]=len({
                p["species"] for rows in elected.values() for p in rows})
    return selected,audits

def load_guild_outcome_only_after_frame_frozen(hues):
    events={}
    for r in hues:
        k=((r["Study_id"],r["Network_id"],r["Year"]),key(r["species"]))
        counts=(int(r["original_strict_Bombus_species_visit_records"]),
                int(r["original_strict_other_bee_species_visit_records"]))
        if counts[0]<0 or counts[1]<0:
            raise ValueError("STAGE76_INVALID_ORIGINAL_VISITOR_RECORD_COUNT")
        if k in events and events[k]!=counts:
            raise ValueError("STAGE76_DUPLICATE_ORIGINAL_PLANT_SOURCE_GUILD_DATA_DISAGREES")
        events[k]=counts
    return {k:{"B":b,"O":o} for k,(b,o) in events.items()}

def sensitivity_guild_eval(selected,events,source_original):
    results={};scores=[];cohorts=[]
    for contrast,(a,b,original_expected) in CONTRASTS.items():
        for mode in MODES:
            k=(mode,contrast)
            frame=selected[k]
            rec=[];reasons=Counter()
            for net,plants in sorted(frame.items()):
                # Original null_score_pair uses guild data after site/native
                # source selection; source absence stays unknown.
                one,why=null_score_pair(plants,events,(a,b))
                reasons[why]+=1
                if one:
                    one["mode"]=mode;one["color_contrast"]=contrast
                    one.update({z:plants[0][z] for z in (
                         "Bioregion","Country","EuPPollNet_habitat",
                         "source_TDWG_L3","source_polygon_status")})
                    rec.append(one)
                for plant in plants:
                    ev=events.get((net,plant["species"]),{"B":0,"O":0})
                    cohorts.append({**plant,
                      "source_contrast":contrast,"source_native_geo_mode":mode,
                      "source_actual_strict_Bombus_records":ev["B"],
                      "source_actual_strict_other_bee_records":ev["O"],
                      "original_no_visitor_record_is_not_true_absence":True})
            stats,by_study=study_block_summary(rec)
            parent=source_original["effect_test_output"][contrast]
            results[mode+"__"+contrast]={
                "source_original_Stage75_hue_eligible_networks":original_expected,
                "source_original_Stage75_Bombus_guild_informative_networks":parent["informative_networks"],
                "source_original_Stage75_study_ids_informative":parent["informative_study_ids"],
                "source_new_WCVP_native_region_networks_before_guild":len(frame),
                "source_new_WCVP_studies_before_guild":len({n[0] for n in frame}),
                "source_new_after_Bombus_strict_observability":dict(reasons),
                **stats,
                "original_colors_source_positive_prose_not_measured_UV_guides":True,
                "WCVP_TDWG_L3_does_not_prove_plant_is_local_native_individual":True,
                "nonobserved_Bombus_is_not_true_site_Bombus_absence":True,
                "original_Europe_field_site_visitor_study_not_global_SDModel":True,
                "source_plant_species_fixed_effect_would_absorb_hue_label":True,
                "real_Bombus_environmental_suitability_fitted":False,
                "new_mediation_selection_or_fitness_effect_estimated":False,
                "formal_confirmatory_p_value":None,
            }
            scores.extend(rec)
    return results,scores,cohorts

def source_bioregions(scores):
    data=defaultdict(list)
    for r in scores:
        data[(r["mode"],r["color_contrast"],r["Bioregion"])].append(r)
    out=[]
    for (mode,contrast,bio),rows in sorted(data.items()):
        S=sum(float(x["original_null_score"]) for x in rows)
        I=sum(float(x["original_null_information"]) for x in rows)
        out.append({
            "source_mode":mode,"source_hue_pair":contrast,
            "original_Bioregion":bio,
            "source_guild_informative_network_count":len(rows),
            "original_distinct_source_studies":len({x["Study_id"] for x in rows}),
            "source_null_score":S,"source_null_information":I,
            "source_local_null_score_ratio_if_information":S/I if I>0 else "",
            "regional_bioregion_not_wind_VOC_climate_temperature":True,
        })
    return out

def run(args):
    for path,expected in (
        (args.stage75_hues,STAGE75_HUES_SHA),
        (args.stage75_receipt,STAGE75_MAIN_SHA),
        (args.stage69_original_networks,STAGE69_NETWORKS_SHA)):
        verify_sha(path,expected)
    original=json.loads(args.stage75_receipt.read_text(encoding="utf-8"))
    if not original["all_field_networks_eligible_hue_group_selection_unconditioned_on_Bombus"]:
        raise ValueError("STAGE76_SOURCE_STAGE75_HUE_SELECTION_NOT_OUTCOME_BLIND")
    units=read(args.stage75_hues)
    allplants=read(args.stage69_original_networks)
    catalogs=original_species_catalog(allplants)
    accepted,states,report=native.load_wcvp_exact_species(args.wcvp_zip,catalogs[0])
    valid,poly_report=native.read_tdwg_geojson(args.tdwg_geojson)
    source_valid,repaired,unrepaired=source_polygons_plus_repaired(args.tdwg_geojson)
    if len(repaired)!=19 or unrepaired:
        raise ValueError("STAGE76_HISTORIC_19_INVALID_POLYGONS_CHANGED")
    if len(source_valid)!=len(valid):
        raise ValueError("STAGE76_SOURCE_VALID_GEOMETRY_NOT_SAME")
    coords,network_report=native.source_network_coordinates()
    spatial=classify_site_networks(coords,valid,valid+[(code,geom) for code,geom,_ in repaired])
    original_site_status=original_site_plant_range_coverage(allplants,spatial,accepted,states,catalogs)
    selected,design=define_pre_guild_native_hue_frames(units,spatial,accepted,states)
    events=load_guild_outcome_only_after_frame_frozen(units)
    results,scores,cohorts=sensitivity_guild_eval(selected,events,original)
    bioregions=source_bioregions(scores)
    return {
       "schema":"stage76_original_2026_continental_floral_TEXT_x_native_WCVP_x_real_guild_macro",
       "source_original_EuPPollNet_623476_record_rows":network_report["original_source_network_visitation_records"],
       "source_original_EuPPollNet_1864_networks":network_report["original_study_network_year_keys_with_coordinates"],
       "source_actual_distinct_original_plant_taxa":len(catalogs[0]),
       "source_actual_distinct_NHM_matched_plant_taxa":len(catalogs[1]),
       "source_actual_distinct_plant_taxa_with_NHM_flower_colour":len(catalogs[2]),
       "source_WCVP_exact_accepted_species_catalog":report,
       "source_original_valid_TDWG_polygon_provenance":poly_report,
       "source_source_raw_network_coordinates":network_report,
       "source_EuPPollNet_all_18798_plant_site_WCVP_native_original_vs_georepaired":original_site_status,
       "source_original_native_hue_network_design_before_guild":{
          mode+"__"+pair:dict(counter) for (mode,pair),counter in design.items()},
       "original_site_native_HUE_vs_Bombus_strict_recorded_comparisons":results,
       "source_origins_unlisted_unknown_not_invasive_absent":True,
       "raw_tdwg_region_not_exact_species_population_native_proof":True,
       "flower_visual_text_is_not_real_UV_guide_or_spectra":True,
       "global_Bombus_hypervolume_artifact_reused":False,
       "global_Bombus_hypervolume_original_expired_2026_10_10":True,
       "observed_site_guild_presence_not_predicted_suitability":True,
       "study_and_species_phylogenetic_nonindependence_unresolved":True,
       "no_new_selection_or_causal_SEM":True,
       "source_results":scores,"source_cohort_rows":cohorts,
       "source_field_bioregion_source_only":bioregions,
    }

def save_csv(path,rows):
    if not rows:return
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage75-hues",required=True,type=Path)
    p.add_argument("--stage75-receipt",required=True,type=Path)
    p.add_argument("--stage69-original-networks",required=True,type=Path)
    p.add_argument("--wcvp-zip",required=True,type=Path)
    p.add_argument("--tdwg-geojson",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    result=run(a)
    a.outdir.mkdir(exist_ok=True,parents=True)
    for field,filename in (
        ("source_cohort_rows","original_macro_plant_hue_WCVP_native_bio_euppollnet.csv"),
        ("source_results","original_macro_native_site_guild_score_networks.csv"),
        ("source_field_bioregion_source_only","original_macro_source_bioregion_native_sensitivity.csv")):
        save_csv(a.outdir/filename,result.pop(field))
    (a.outdir/"official_wcvp_native_stage75_macro_source_and_guild_receipt.json").write_text(
        json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE76_REAL_SOURCE_WCVP_NATIVE_963_NHM_EUPPOLLNET_MACRO",
          json.dumps(result,sort_keys=True))
    print("NO_FALSE_NATIVE_INDIVIDUAL_OR_GLOBAL_BOMBUS_SDM_OR_MACRO_SELECTION_CLAIM")

if __name__=="__main__":
    main()
