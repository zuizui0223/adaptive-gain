"""Stage70B diagnostic: source-invalid TDWG polygons and sensitivity recovery only.

DO NOT promote repaired geometries into primary source-backed native-site findings.
The original Stage70 73 requalified networks remain the primary conservative
count. This diagnoses why 68/156 source networks lacked a unique TDWG polygon.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from shapely.geometry import Point, shape
from shapely import make_valid

sys.path.insert(0,str(Path(__file__).resolve().parent))
import official_wcvp_native_tdwg_original_field_network as st


def source_polygons_plus_repaired(path):
    raw=Path(path).read_bytes()
    if st.original_git_blob_sha(raw)!=st.TDWG_GEOJSON_EXPECTED_BLOB_SHA1:
        raise ValueError("STAGE70B_TDWG_SOURCE_IDENTITY_CHANGED")
    j=json.loads(raw)
    valid=[];repaired=[];notrepairable=[]
    for f in j["features"]:
        g=shape(f["geometry"])
        code=str(f["properties"]["LEVEL3_COD"]).strip().upper()
        name=str(f["properties"].get("LEVEL3_NAM",""))
        if g.is_valid and not g.is_empty:
            valid.append((code,g))
        else:
            fix=make_valid(g)
            if fix.is_valid and not fix.is_empty:
                repaired.append((code,fix,name))
            else:
                notrepairable.append((code,name))
    if len(valid)!=350 or len(repaired)+len(notrepairable)!=19:
        raise ValueError("STAGE70B_ORIGINAL_350_VALID_19_INVALID_GEOMETRY_GRAIN_CHANGED")
    return valid,repaired,notrepairable


def candidate_polygon_codes(coords, polygons):
    if len(coords)!=1:
        return "NO_UNIQUE_SOURCE_COORDINATE",set()
    lat,lon=next(iter(coords))
    p=Point(lon,lat)
    codes=set()
    for code,g in polygons:
        if (g.bounds[0]<=lon<=g.bounds[2]
                and g.bounds[1]<=lat<=g.bounds[3]
                and g.contains(p)):
            codes.add(code)
    if not codes:
        return "ZERO_POLYGONS_CONTAIN",codes
    if len(codes)>1:
        return "MULTIPLE_POLYGON_CODES_CONTAIN",codes
    return "ONE_POLYGON_CONTAINS",codes


def audit(gate_csv,network_units_csv,spectra_csv,wcvp_zip,tdwg_geojson,original_networks_csv):
    old=st.read_csv(original_networks_csv)
    if len(old)!=156:
        raise ValueError("STAGE70B_PREVIOUS_156_SOURCE_NETWORKS_MISSING")
    prev={ (r["Study_id"],r["Network_id"],r["Year"]):r for r in old}
    gate,selected,spectra=st.gate_join(st.read_csv(gate_csv),st.read_csv(network_units_csv),st.read_csv(spectra_csv))
    if gate!=set(prev):
        raise ValueError("STAGE70B_ORIGINAL_STAGE69B_NETS_CHANGED")
    target={name for rs in selected.values() for name,_,_ in rs}
    acc,origin,_=st.load_wcvp_exact_species(wcvp_zip,target)
    valid,repaired,unrepairable=source_polygons_plus_repaired(tdwg_geojson)
    coords,location_report=st.source_network_coordinates()
    # Only as sensitivity; source original invalid geometry was removed in
    # conservative Stage70 and could contain historic topology faults.
    repaired_shapes=[(code,g) for code,g,_ in repaired]
    all_polygons=valid+repaired_shapes
    out=[]
    reasons=Counter()
    input_original_unknown=0
    recovered=0
    additional_requalified=0
    still_unknown=0
    candidate_repaired_studies=set()
    invalid_names=Counter(name for _,_,name in repaired)
    original_requalified=sum(int(r["after_WCVP_native_L3_and_edge_sensitivity_gate"]) for r in old)
    if original_requalified!=73:
        raise ValueError("STAGE70B_FROZEN_STAGE70_PRIMARY_73_CHANGED")

    for key in sorted(gate):
        study,network,year=key
        original=prev[key]
        subset=selected[key]
        c=coords.get(key,set())
        valid_reason, valid_codes=candidate_polygon_codes(c,valid)
        repaired_reason, repair_codes=candidate_polygon_codes(c,all_polygons)
        reasons[(valid_reason,repaired_reason)]+=1
        was_missing=original["spatial_status"]=="MULTIPLE_OR_ZERO_TDWG_POLYGON_CONTAINS"
        if was_missing:
            input_original_unknown+=1
            if repaired_reason=="ONE_POLYGON_CONTAINS":
                recovered+=1
                candidate_repaired_studies.add(study)
            else:
                still_unknown+=1
        # Do not reuse invalid or multi-coordinate for original primary.
        code, spatial, boundary=st.locate_l3(c, all_polygons)
        included=[]
        for name,row,uv in subset:
            if boundary:
                continue
            if st.classify_origin(name,code,acc,origin)=="WCVP_NATIVE_L3_COMPATIBLE":
                included.append((name,row,uv))
        mixed=(
           len(included)>=2
           and len({n.split()[0] for n,_,_ in included})>=2
           and max(uv for _,_,uv in included)-min(uv for _,_,uv in included)>=1.0
           and sum(int(r["n_observed_Bombus"]) for _,r,_ in included)>0
           and sum(sum(int(r["n_observed_"+x]) for x in (
               "other_bee","other_hymenoptera","diptera","lepidoptera","coleoptera"))
               for _,r,_ in included)>0
        )
        prev_ok=original["after_WCVP_native_L3_and_edge_sensitivity_gate"]=="1"
        if mixed and not prev_ok and was_missing:
            additional_requalified+=1
        out.append({
          "Study_id":study,"Network_id":network,"Year":year,
          "original_primary_spatial_status":original["spatial_status"],
          "original_primary_native_requalified":int(prev_ok),
          "source_original_valid_polygon_reason":valid_reason,
          "secondary_original_invalid_geometries_repaired_reason":repaired_reason,
          "secondary_TDWG_L3_code_only_if_unique":code,
          "secondary_polygon_near_angular_boundary":int(boundary),
          "secondary_repaired_geometry_native_qualified":int(mixed),
          "rescue_is_source_topology_sensitivity_NOT_PRIMARY":int(mixed and not prev_ok),
        })
    summary={
     "schema":"stage70b_historic_TDWG_invalid_geometry_repair_sensitivity_not_primary",
     "original_source_TDWG_geojson_SHA1":st.TDWG_GEOJSON_EXPECTED_BLOB_SHA1,
     "original_geometry_valid_features":len(valid),
     "original_geometry_invalid_but_repaired_for_sensitivity":len(repaired),
     "original_geometry_invalid_unrepairable":len(unrepairable),
     "invalid_historic_polygon_names":[{"name":n,"n":c} for n,c in invalid_names.most_common(19)],
     "source_original_stage69b_exploratory_networks":len(gate),
     "conservative_original_Stage70_native_requalified":original_requalified,
     "original_unmatched_polygon_networks":input_original_unknown,
     "unmatched_polygon_networks_get_unique_L3_only_in_repaired_sensitivity":recovered,
     "original_unmatched_polygon_networks_still_unknown_after_repair":still_unknown,
     "extra_original_source_networks_native_requalified_only_in_geom_repair_sensitivity":additional_requalified,
     "study_ids_with_source_geometry_repair_candidate_networks":len(candidate_repaired_studies),
     "original_valid_vs_secondary_repaired_containment_reasons":{
         f"{a} -> {b}":n for (a,b),n in sorted(reasons.items())},
     "primary_stage70_network_73_not_promoted_to_sensitivity":True,
     "source_native_L3_is_not_field_native_population_proof":True,
     "source_field_phenotypes_not_source_measured_at_wild_sites":True,
     "plant_fitness_and_causal_effects_estimated":False
    }
    return out,summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-156-network",type=Path,required=True)
    p.add_argument("--gate-csv",type=Path,required=True)
    p.add_argument("--original-network-units-csv",type=Path,required=True)
    p.add_argument("--original-spectra-csv",type=Path,required=True)
    p.add_argument("--wcvp-zip",type=Path,required=True)
    p.add_argument("--tdwg-geojson",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    rows,summary=audit(
      a.gate_csv,a.original_network_units_csv,a.original_spectra_csv,
      a.wcvp_zip,a.tdwg_geojson,a.original_156_network)
    a.outdir.mkdir(exist_ok=True,parents=True)
    st.write_csv(a.outdir/"historic_TDWG_geometry_repair_network_sensitivity.csv",rows)
    (a.outdir/"historic_TDWG_geometry_repair_source_receipt.json").write_text(
      json.dumps(summary,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE70B_ORIGINAL_TDWG_GEOMETRY_REPAIR_SENSITIVITY_AUDIT",
          json.dumps(summary,sort_keys=True))
    print("DIAGNOSTIC_ONLY_NO_PRIMARY_RECLASSIFICATION_NO_CAUSALITY")


if __name__=="__main__":
    main()
