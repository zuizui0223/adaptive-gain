"""Stage70: source-version-pinned WCVP botanical native L3 × field-network coordinates.

Do not infer individual origin or native population from regional WCVP. Do not
turn WCVP unlisted areas into confirmed absences. Original petal optical data
were measured in a German botanical garden, not EuPPollNet field sites.
Source original v1.3.0 corrected plant-visitor network and Stage69 gates.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from shapely.geometry import Point, shape

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "floral_literature_macro_stage69"))
from ingest_original_corrected_EuPPollNet_network_NHM_spectra import (
    fetch_original, dict_rows, year_of, strict_name, guild_of, EXPECTED_INTERACTIONS
)

WCVP_ZIP_EXPECTED_SHA256 = "d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa"
TDWG_GEOJSON_EXPECTED_BLOB_SHA1 = "91104e5159e31f88154833a51d3b0d1c9271083f"
EDGE_ANGLE_DEG = 0.02
VISITS_PER_TAXON_MIN = 3
UV_RANGE_PERCENT_POINTS_MIN = 1.0
ORIGINAL_STRICT_SOURCE_NETWORKS = 156


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def original_git_blob_sha(b: bytes):
    return hashlib.sha1(f"blob {len(b)}\0".encode() + b).hexdigest()


def read_csv(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def string_flag(value):
    # explicit binary 0/1 only: blanks become unknown
    v = str(value).strip()
    if v in ("0", "0.0"):
        return 0
    if v in ("1", "1.0"):
        return 1
    return None


def load_wcvp_exact_species(zip_path, targets):
    if sha256(zip_path) != WCVP_ZIP_EXPECTED_SHA256:
        raise ValueError("STAGE70_WCVP_SOURCE_DIGEST_NOT_ORIGINAL_ISLAND_PIN")
    accepted = defaultdict(set)
    source_name_rows = 0
    with zipfile.ZipFile(zip_path) as archive:
        if not {"wcvp_names.csv", "wcvp_distribution.csv"}.issubset(set(archive.namelist())):
            raise ValueError("STAGE70_WCVP_EXPECTED_ORIGINAL_TABLES_MISSING")
        with io.TextIOWrapper(archive.open("wcvp_names.csv"), encoding="utf-8", errors="replace", newline="") as f:
            for row in csv.DictReader(f, delimiter="|"):
                if row["taxon_rank"].strip().casefold() != "species":
                    continue
                if row["taxon_status"].strip().casefold() != "accepted":
                    continue
                name = strict_name(row["taxon_name"])
                if name not in targets or "\ufffd" in name:
                    continue
                source_name_rows += 1
                pid = row["plant_name_id"].strip()
                if pid:
                    accepted[name].add(pid)
        idmap = {pid: name for name, ids in accepted.items() if len(ids) == 1 for pid in ids}
        states = defaultdict(lambda: defaultdict(set))
        with io.TextIOWrapper(archive.open("wcvp_distribution.csv"), encoding="utf-8", errors="replace", newline="") as f:
            for row in csv.DictReader(f, delimiter="|"):
                pid = row["plant_name_id"].strip()
                if pid not in idmap:
                    continue
                l3 = row["area_code_l3"].strip().upper()
                if not l3:
                    continue
                if string_flag(row["extinct"]) != 0 or string_flag(row["location_doubtful"]) != 0:
                    continue
                intro = string_flag(row["introduced"])
                if intro is None:
                    continue
                states[idmap[pid]][l3].add("introduced" if intro else "native")
    report = {
        "input_source_species_names": len(targets),
        "matched_accepted_WCVP_species_names": sum(len(ids) == 1 for ids in accepted.values()),
        "unmatched_or_nonaccepted_WCVP_names": len(targets) - sum(len(ids) == 1 for ids in accepted.values()),
        "ambiguous_accepted_WCVP_same_name_multiple_ids": sum(len(ids) > 1 for ids in accepted.values()),
        "original_WCVP_accepted_taxon_rows": source_name_rows,
        "native_L3_taxa": sum(any("native" in v for v in ss.values()) for ss in states.values()),
        "introduced_L3_taxa": sum(any("introduced" in v for v in ss.values()) for ss in states.values()),
        "native_data_missing_is_not_introduced": True,
    }
    return accepted, states, report


def classify_origin(name, code, accepted, states):
    if not code:
        return "SITE_TDWG_L3_UNRESOLVED"
    if len(accepted.get(name, set())) != 1:
        return "WCVP_SPECIES_NOT_EXACT_ACCEPTED"
    tags = states[name].get(code, set())
    if tags == {"native"}:
        return "WCVP_NATIVE_L3_COMPATIBLE"
    if tags == {"introduced"}:
        return "WCVP_INTRODUCED_L3_RECORDED"
    if tags == {"native", "introduced"}:
        return "WCVP_L3_CONFLICTING_ORIGINS"
    return "WCVP_L3_NOT_RECORDED_UNKNOWN"


def read_tdwg_geojson(path):
    raw = Path(path).read_bytes()
    if original_git_blob_sha(raw) != TDWG_GEOJSON_EXPECTED_BLOB_SHA1:
        raise ValueError("STAGE70_TDWG_ORIGINAL_GEOJSON_GIT_SHA_CHANGED")
    geo = json.loads(raw)
    if geo.get("type") != "FeatureCollection" or len(geo.get("features", [])) < 350:
        raise ValueError("STAGE70_TDWG_GEOJSON_NOT_ORIGINAL_L3")
    polygons = []
    codes = Counter()
    invalid = 0
    for f in geo["features"]:
        props = f["properties"]
        code = str(props.get("LEVEL3_COD", "")).strip().upper()
        if not code:
            raise ValueError("STAGE70_TDWG_MISSING_L3_CODE")
        g = shape(f["geometry"])
        if g.is_empty or not g.is_valid:
            invalid += 1
            continue
        polygons.append((code, g))
        codes[code] += 1
    if not polygons:
        raise ValueError("STAGE70_TDWG_NO_VALID_GEOMETRIES")
    return polygons, {"tdwg_source_features": len(geo["features"]),
                      "tdwg_valid_polygon_features": len(polygons),
                      "tdwg_invalid_polygon_features_excluded": invalid,
                      "tdwg_distinct_L3_codes": len(codes)}


def locate_l3(latlon, polygons):
    if not latlon or len(latlon) != 1:
        return "", "NO_SINGLE_UNAMBIGUOUS_SOURCE_COORDINATE", False
    lat, lon = next(iter(latlon))
    p = Point(lon, lat)
    hits = [(code, poly) for code, poly in polygons
            if poly.bounds[0] <= lon <= poly.bounds[2]
            and poly.bounds[1] <= lat <= poly.bounds[3]
            and poly.contains(p)]
    if len(hits) != 1:
        return "", "MULTIPLE_OR_ZERO_TDWG_POLYGON_CONTAINS", False
    code, poly = hits[0]
    edge = poly.boundary.distance(p) <= EDGE_ANGLE_DEG
    return code, ("NEAR_BOUNDARY_SENSITIVITY" if edge else "WITHIN_TDWG_L3_POLYGON"), edge


def source_network_coordinates():
    coords = defaultdict(set)
    n = 0
    original = fetch_original("Interaction_data.csv.gz")
    for r in dict_rows(original, compressed=True):
        n += 1
        k = (r["Study_id"].strip(), r["Network_id"].strip(), year_of(r["Date"]))
        try:
            lat, lon = float(r["Latitude"]), float(r["Longitude"])
        except (ValueError, TypeError):
            continue
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            coords[k].add((round(lat, 7), round(lon, 7)))
    if n != EXPECTED_INTERACTIONS:
        raise ValueError("STAGE70_CORRECTED_ORIGINAL_EUPPOLLNET_SOURCE_DENOMINATOR_CHANGED")
    return coords, {"original_source_network_visitation_records": n,
                    "original_study_network_year_keys_with_coordinates": len(coords),
                    "original_source_multiple_coordinate_networks": sum(len(v) > 1 for v in coords.values())}


def gate_join(source_networks, species_network, original_optical):
    # Only Stage69B frozen 156 networks, not fitted/effect-selected.
    eligible = {
        (r["Study_id"], r["Network_id"], r["Year"])
        for r in source_networks
        if r["eligible_two_different_genera_Bombus_and_other_UV_range"] == "1"
    }
    if len(eligible) != ORIGINAL_STRICT_SOURCE_NETWORKS:
        raise ValueError(f"STAGE70_SOURCE_156_EXPLORATION_DESIGN_CHANGED_{len(eligible)}")
    spectra = {}
    for r in original_optical:
        k = strict_name(r["spectral_original_species_name"])
        if k in spectra:
            raise ValueError("STAGE70_ORIGINAL_SPECTRA_DUPLICATE_NAME")
        spectra[k] = float(r["original_2024_true_petal_UV_300_399_percent"])
    if len(spectra) != 73:
        raise ValueError("STAGE70_ORIGINAL_SPECTRAL_73_NAME_FRAME_CHANGED")
    selected = defaultdict(list)
    for row in species_network:
        key = (row["Study_id"], row["Network_id"], row["Year_from_original_date"])
        if key not in eligible or row["Stage67_direct_petal_spectra_name_match"] != "1":
            continue
        name = strict_name(row["Original_plant_accepted_name_literal"])
        if name not in spectra:
            raise ValueError("STAGE70_NETWORK_SOURCE_SPECTRAL_TAXON_NOT_IN_ORIGINAL_73")
        if row["NHM_text_name_match"] != "1":
            continue
        visits = int(row["n_all_observed_visitor_records_this_plant_network"])
        if visits < VISITS_PER_TAXON_MIN:
            continue
        selected[key].append((name, row, spectra[name]))
    # Every source strict network contains the required eligible pair.
    if set(selected) != eligible:
        raise ValueError("STAGE70_MISSING_STAGE69B_SOURCE_NETWORK_OR_TAXON")
    return eligible, selected, spectra


def audit(inputs):
    gate_rows = read_csv(inputs.gate_csv)
    units = read_csv(inputs.original_network_units_csv)
    petal = read_csv(inputs.original_spectra_csv)
    expected, selected, spectra = gate_join(gate_rows, units, petal)
    target = {s for rows in selected.values() for s, _, _ in rows}
    accepted, wcvp_states, wcvp_report = load_wcvp_exact_species(inputs.wcvp_zip, target)
    polygons, poly_report = read_tdwg_geojson(inputs.tdwg_geojson)
    coords, network_report = source_network_coordinates()
    result = []
    network_summaries = []
    area_status = Counter()
    status_species = defaultdict(set)
    site_status = Counter()
    retained_species = set()
    retained_studies = set()
    for study, net, year in sorted(expected):
        rows = selected[(study, net, year)]
        l3, spatial_status, edge = locate_l3(coords.get((study,net,year), set()), polygons)
        site_status[spatial_status] += 1
        qualifying = []
        for name, row, uv in rows:
            origin = classify_origin(name, l3, accepted, wcvp_states)
            if edge and origin == "WCVP_NATIVE_L3_COMPATIBLE":
                robust = "NEAR_BOUNDARY_NOT_ROBUST"
            else:
                robust = origin
            area_status[origin] += 1
            status_species[origin].add(name)
            if robust == "WCVP_NATIVE_L3_COMPATIBLE":
                qualifying.append((name,row,uv))
                retained_species.add(name)
            result.append({
              "Study_id": study, "Network_id": net, "Year": year,
              "Original_source_taxon_name": name,
              "TDWG_L3_from_original_field_coordinates": l3,
              "Field_coordinate_polygon_admission": spatial_status,
              "Author_original_network_unique_coordinate_count": len(coords.get((study,net,year),set())),
              "WCVP_exact_accepted_name": int(len(accepted.get(name,set())) == 1),
              "WCVP_native_L3_status": origin,
              "source_boundary_0_02_degree_sensitivity_status": robust,
              "original_petal_UV_300_399_percent": uv,
              "real_observed_Bombus_visits": row["n_observed_Bombus"],
              "real_observed_other_bee_visits": row["n_observed_other_bee"],
              "real_observed_diptera_visits": row["n_observed_diptera"],
              "real_observed_lepidoptera_visits": row["n_observed_lepidoptera"],
              "real_observed_nonbee_hymenoptera": row["n_observed_other_hymenoptera"],
              "real_observed_coleoptera_visits": row["n_observed_coleoptera"],
              "plant_source_receptor_guidance_uv_bullseye": "NOT_MEASURED",
              "original_spectroscopy_same_field_population": "NOT_ESTABLISHED",
              "original_field_visit_effective_pollen_transfer": "NOT_MEASURED",
            })
        mixed = (
            len(qualifying) >= 2
            and len({n.split()[0] for n,_,_ in qualifying}) >= 2
            and max(uv for _,_,uv in qualifying) - min(uv for _,_,uv in qualifying) >= UV_RANGE_PERCENT_POINTS_MIN
            and sum(int(r["n_observed_Bombus"]) for _,r,_ in qualifying) > 0
            and sum(sum(int(r["n_observed_"+x]) for x in
                ("other_bee","other_hymenoptera","diptera","lepidoptera","coleoptera"))
                for _,r,_ in qualifying) > 0
        )
        if mixed:
            retained_studies.add(study)
        network_summaries.append({
             "Study_id":study, "Network_id":net,"Year":year,
             "TDWG_L3_code":l3, "spatial_status":spatial_status,
             "n_source_optical_taxa_at_least3_visits":len(rows),
             "n_WCVP_native_L3_compatible_and_boundary_safe_optical_taxa":len(qualifying),
             "source_network_original_exploratory_gate_pass":1,
             "after_WCVP_native_L3_and_edge_sensitivity_gate":int(mixed),
        })
    n_pass = sum(r["after_WCVP_native_L3_and_edge_sensitivity_gate"] for r in network_summaries)
    summary = {
      "schema": "stage70_20261117_WCVP_native_TDWG_L3_corrected_EuPPollNet_original_optical",
      "source_corrected_EuPPollNet_tag": "joseblanuza/EuPPollNet@v1.3.0",
      "source_original_optical_figshare_DOI": "10.6084/m9.figshare.21081025.v2",
      "source_WCVP_archive_sha256": WCVP_ZIP_EXPECTED_SHA256,
      "source_TDWG_level3_geojson_git_blob_SHA1": TDWG_GEOJSON_EXPECTED_BLOB_SHA1,
      "source_WCVP_matches": wcvp_report,
      "source_TDWG_geometry": poly_report,
      "source_EuPPollNet_coordinates": network_report,
      "original_Stage69B_exploratory_networks":len(expected),
      "source_eligible_species_name_count":len(target),
      "original_selected_plant_network_units":len(result),
      "field_network_coordinate_polygon_status":dict(site_status),
      "source_species_original_WCVP_area_status_counts":dict(area_status),
      "distinct_original_species_by_WCVP_area_status":{k:len(v) for k,v in status_species.items()},
      "native_compatible_border_safe_taxa_with_any_record":len(retained_species),
      "native_compatible_border_safe_requalified_networks":n_pass,
      "independent_study_ids_with_requalified_networks":len(retained_studies),
      "name_match_does_not_prove_native_individuals":True,
      "regional_native_L3_does_not_prove_source_same_population":True,
      "WCVP_unlisted_area_is_unknown_not_absent":True,
      "original_tdwg_geometry_is_not_site_position_uncertainty":True,
      "bird_pollination_missing_EuPPollNet":True,
      "original_field_spectra_wind_chemical_signals_matched":False,
      "plant_fitness_and_causal_mediation_estimated":False,
    }
    return result, network_summaries, summary


def write_csv(path, rows):
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gate-csv",type=Path,required=True)
    p.add_argument("--original-network-units-csv",type=Path,required=True)
    p.add_argument("--original-spectra-csv",type=Path,required=True)
    p.add_argument("--wcvp-zip",type=Path,required=True)
    p.add_argument("--tdwg-geojson",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    result,networks,summary=audit(a)
    a.outdir.mkdir(exist_ok=True,parents=True)
    write_csv(a.outdir/"original_species_network_WCVP_native_TDWG_L3_admission.csv",result)
    write_csv(a.outdir/"original_156_network_native_requalification.csv",networks)
    (a.outdir/"native_requalification_source_receipt.json").write_text(
        json.dumps(summary,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE70_OFFICIAL_WCVP_NATIVE_SITE_TDWG_SOURCE_RESULT",json.dumps(summary,sort_keys=True))
    print("NO_WCVP_UNLISTED_AS_ABSENT_NO_NATURAL_SITE_PETAL_SPECTRA_NO_SELECTION_OR_SEM")


if __name__ == "__main__":
    main()
