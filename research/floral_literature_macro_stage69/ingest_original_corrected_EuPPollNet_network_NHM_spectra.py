"""Stage69: genuinely OBSERVED plant-visitor interactions × Stage68 botanical text.

Input is original corrected EuPPollNet v1.3.0 CSV.GZ from the AUTHOR's
immutable GitHub release tag, not pre-correction v1.0.0 or main.
Only text-extracted NHM flower traits and directly measured published Stage67
petal spectra are joined, by literal species binomial (no photos).
This script is a source audit and coverage/observation-grain bridge, NOT a
native-range association, causal pollinator SEM, pollination-effectiveness
test, or adaptive evolution model.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

TAG = "v1.3.0"
SOURCE_DOI = "10.5281/zenodo.15183272"
CORRECTION_DOI = "10.1111/geb.70054"
ROOT = "https://raw.githubusercontent.com/joseblanuza/EuPPollNet/" + TAG + "/Data/3_Final_data/"
PIN = {
    "Interaction_data.csv.gz": ("6e639d4af81feee76eefa6804622f8b901c39feb", 2374060),
    "Metadata.csv": ("f9708e2f2b142ab2437a8be9d16e33aaefdef0ed", 28483),
}
EXPECTED_INTERACTIONS = 623476
FIELDS = (
    "Study_id", "Network_id", "Date", "Country", "Latitude", "Longitude",
    "Plant_accepted_name", "Plant_rank", "Plant_unsure_id",
    "Pollinator_accepted_name", "Pollinator_order", "Pollinator_family",
    "Pollinator_genus", "Pollinator_unsure_id", "Sampling_method",
)
BEE_FAMILIES = {
    "apidae", "andrenidae", "halictidae", "megachilidae",
    "colletidae", "melittidae", "stenotritidae",
}
GUILDS = ("Bombus", "other_bee", "other_hymenoptera", "diptera",
          "lepidoptera", "coleoptera", "other_or_unknown")
YEAR = re.compile(r"(?:19|20)\d{2}")


def git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def fetch_original(name: str) -> bytes:
    if name not in PIN:
        raise ValueError("STAGE69_UNREGISTERED_SOURCE_FILE")
    req = urllib.request.Request(ROOT + name, headers={
        "User-Agent": "adaptive-gain-stage69-pinned-corrected-visits/2026",
        "Accept": "application/octet-stream"})
    with urllib.request.urlopen(req, timeout=120) as res:
        raw = res.read(PIN[name][1] + 1)
    if len(raw) != PIN[name][1] or git_blob_sha(raw) != PIN[name][0]:
        raise ValueError("STAGE69_AUTHENTIC_SOURCE_GIT_BLOB_CHANGED_" + name)
    return raw


def dict_rows(raw: bytes, compressed: bool = False):
    buffer = (gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb")
              if compressed else io.BytesIO(raw))
    text = io.TextIOWrapper(buffer, encoding="utf-8-sig", newline="")
    reader = csv.DictReader(text)
    if not reader.fieldnames:
        raise ValueError("STAGE69_CSV_MISSING_HEADER")
    for i, r in enumerate(reader, 1):
        if None in r or any(k is None for k in r):
            raise ValueError(f"STAGE69_CSV_MALFORMED_ROW_{i}")
        yield r


def verify_header(raw: bytes):
    with gzip.open(io.BytesIO(raw), "rt", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        head = next(reader)
    if not set(FIELDS).issubset(set(head)) or len(head) != 30:
        raise ValueError("STAGE69_CORRECTED_EUPPOLLNET_SCHEMA_CHANGED")
    return head


def strict_name(name: str) -> str:
    # Do NOT synonym match, fuzzy match, or accept unverified genus proxies.
    return str(name).strip().casefold()


def guild_of(row):
    order = row.get("Pollinator_order", "").strip().casefold()
    genus = row.get("Pollinator_genus", "").strip().casefold()
    family = row.get("Pollinator_family", "").strip().casefold()
    if order == "hymenoptera":
        if genus == "bombus":
            return "Bombus"
        if family in BEE_FAMILIES:
            return "other_bee"
        return "other_hymenoptera"
    if order == "diptera":
        return "diptera"
    if order == "lepidoptera":
        return "lepidoptera"
    if order == "coleoptera":
        return "coleoptera"
    return "other_or_unknown"


def is_species(row):
    return (row.get("Plant_rank", "").strip().casefold() == "species" and
            row.get("Plant_unsure_id", "").strip().casefold() not in
            {"yes", "true", "1", "y"})


def year_of(value):
    m = YEAR.search(str(value))
    return m.group(0) if m else "UNKNOWN"


def load_nhm(rows):
    byname = {}
    for r in rows:
        k = strict_name(r["taxon"])
        if not k or k in byname:
            raise ValueError("STAGE69_NHM_SOURCE_DUPLICATE_OR_EMPTY")
        byname[k] = r
    if len(byname) != 59369:
        raise ValueError("STAGE69_EXPECTED_AUTHENTIC_59369_NHM_TEXT_ROWS")
    return byname


def load_spectra(rows):
    byname = {}
    for r in rows:
        k = strict_name(r["spectral_original_species_name"])
        if not k or k in byname:
            raise ValueError("STAGE69_SPECTRA_SOURCE_DUPLICATE_OR_EMPTY")
        byname[k] = r
    if len(byname) != 73:
        raise ValueError("STAGE69_EXPECTED_73_ORIGINAL_PETAL_SPECTRA")
    if sum(r["NHM_literal_species_name_match"] == "YES" for r in rows) != 55:
        raise ValueError("STAGE69_ORIGINAL_STAGE68_TEXT_SPECTRA_CROSSWALK_NOT_55")
    return byname


def study_metadata(metadata_rows):
    # Author Metadata.csv has 80 distinct STUDY×YEAR rows, NOT 80 studies.
    # Seventeen study IDs repeat in different years. Preserve the year key.
    d = {}
    for r in metadata_rows:
        k = (r["Study_id"].strip(), r["Year"].strip())
        if not all(k) or k in d:
            raise ValueError("STAGE69_METADATA_STUDY_YEAR_DUPLICATE_OR_EMPTY")
        d[k] = r
    if len(d) != 80 or len({k[0] for k in d}) != 54:
        raise ValueError("STAGE69_EXPECTED_80_STUDY_YEAR_54_DISTINCT_STUDY_IDS")
    return d


def summarize(raw_gz: bytes, metadata_rows, nhm_rows, spectra_rows):
    header = verify_header(raw_gz)
    meta = study_metadata(metadata_rows)
    nhm = load_nhm(nhm_rows)
    spectra = load_spectra(spectra_rows)
    counts = Counter()
    guilds = Counter()
    plant_names = set()
    plant_species_names = set()
    eligible_plant_names = set()
    obs_by_network = Counter()
    obs_by_study = Counter()
    by_plant_network = defaultdict(Counter)
    original_sites = set()
    malformed_geography = 0
    uncert_plant = 0
    unknown_year = 0
    unmatched_study_year = 0
    observed_taxonomic_rank = Counter()

    for row in dict_rows(raw_gz, compressed=True):
        counts["original_corrected_record_rows"] += 1
        plant = row["Plant_accepted_name"].strip()
        source = row["Study_id"].strip()
        net = row["Network_id"].strip()
        when = year_of(row["Date"])
        observed_taxonomic_rank[row["Plant_rank"].strip()] += 1
        if when == "UNKNOWN":
            unknown_year += 1
        if (source, when) not in meta:
            unmatched_study_year += 1
        plant_names.add(strict_name(plant))
        original_sites.add((source, net, row["Latitude"], row["Longitude"]))
        key = (source, net, when)
        obs_by_network[key] += 1
        obs_by_study[source] += 1
        grp = guild_of(row)
        guilds[grp] += 1
        if not row["Latitude"].strip() or not row["Longitude"].strip():
            malformed_geography += 1
        else:
            try:
                lat, lon = float(row["Latitude"]), float(row["Longitude"])
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    malformed_geography += 1
            except ValueError:
                malformed_geography += 1
        if row["Plant_unsure_id"].strip().casefold() in {"yes","true","1","y"}:
            uncert_plant += 1
        if is_species(row):
            tax = strict_name(plant)
            plant_species_names.add(tax)
            if tax in nhm:
                eligible_plant_names.add(tax)
            # Do not treat an unrecorded guild as biologically absent.
            pk = (source, net, when, tax)
            by_plant_network[pk][grp] += 1
        elif row["Plant_rank"].strip().casefold() == "species":
            counts["plant_unsure_species_record_rows"] += 1

    if counts["original_corrected_record_rows"] != EXPECTED_INTERACTIONS:
        raise ValueError(f"STAGE69_WRONG_OR_UNCORRECTED_INTERACTION_DENOMINATOR_{counts['original_corrected_record_rows']}")
    # Retain unresolved study-year joins as unknown, never borrow a nearby year.
    # The source data are valid independently of metadata association.
    stats = Counter()
    joined = []
    spectrum_target = {k for k, s in spectra.items() if
                       s["NHM_literal_species_name_match"] == "YES"}
    plant_bombus = set()
    cross_guild = set()
    distinct_used_spectra = set()
    site_multiorders = 0
    for (study, net, year, tax), g in sorted(by_plant_network.items()):
        desc = nhm.get(tax)
        sp = spectra.get(tax)
        if desc:
            stats["network_species_units_NHM_literal"] += 1
            if desc["visible_text_colour_recorded"] == "1":
                stats["network_species_units_NHM_text_colour"] += 1
            if desc["visible_text_colour_recorded"] == "1" and desc["structural_text_trait_recorded"] == "1":
                stats["network_species_units_NHM_colour_and_structure"] += 1
        if sp:
            stats["network_species_units_direct_petal_spectra_73"] += 1
            distinct_used_spectra.add(tax)
            if tax in spectrum_target:
                stats["network_species_units_original_73_x_NHM_55"] += 1
                if g.get("Bombus", 0) > 0:
                    plant_bombus.add(tax)
                if g.get("Bombus", 0) > 0 and (g.get("other_bee", 0)+g.get("diptera", 0)+g.get("lepidoptera", 0)) > 0:
                    cross_guild.add(tax)
        # "0 observed" does not mean studied absent at the site.
        yr_meta = meta.get((study, year), {})
        row = {
            "Study_id": study, "Network_id": net, "Year_from_original_date": year,
            "Original_plant_accepted_name_literal": tax,
            "Author_study_sampling_method": yr_meta.get("Sampling_method",""),
            "Author_study_taxa_recorded": yr_meta.get("Taxa_recorded",""),
            "Author_study_DOI": yr_meta.get("DOI", ""),
            "Study_Year_metadata_join_verified": int(bool(yr_meta)),
            "NHM_text_name_match": int(desc is not None),
            "NHM_colour_text_recorded": desc["visible_text_colour_recorded"] if desc else "",
            "NHM_structure_text_recorded": desc["structural_text_trait_recorded"] if desc else "",
            "Stage67_direct_petal_spectra_name_match": int(sp is not None),
            "n_all_observed_visitor_records_this_plant_network": sum(g.values()),
        }
        row.update({f"n_observed_{guild}": g.get(guild,0) for guild in GUILDS})
        joined.append(row)
    # Count distinct matched plant taxa once, not per network or row.
    observed_nhm = plant_species_names & set(nhm)
    observed_spectra = plant_species_names & set(spectra)
    observed_55 = plant_species_names & spectrum_target
    observed_color = {k for k in observed_nhm if nhm[k]["visible_text_colour_recorded"] == "1"}
    observed_struct = {k for k in observed_nhm if nhm[k]["structural_text_trait_recorded"] == "1"}
    n_studies_with_multiple_source_orders = len({
        study for (study, year), v in meta.items()
        if v.get("Number_of_main_orders_recorded", "").strip() not in
            {"", "0", "1", "NA"}
    })
    summary = {
        "schema": "stage69_original_corrected_EuPPollNet_v1_3_0_network_x_NHM_text_x_real_spectra",
        "original_network_source_DOI": SOURCE_DOI,
        "correction_DOI": CORRECTION_DOI,
        "original_source_repository_release": "joseblanuza/EuPPollNet@v1.3.0",
        "original_source_gzip_Git_blob_SHA1": PIN["Interaction_data.csv.gz"][0],
        "original_source_metadata_Git_blob_SHA1": PIN["Metadata.csv"][0],
        "original_source_gzip_file_sha256": hashlib.sha256(raw_gz).hexdigest(),
        "source_author_correction_row_count": EXPECTED_INTERACTIONS,
        "actual_original_corrected_interaction_record_rows": counts["original_corrected_record_rows"],
        "source_interaction_columns": len(header),
        "source_guild_record_count_by_independent_pollinator_taxon": dict(guilds),
        "distinct_Study_ids_in_metadata": len({k[0] for k in meta}),
        "distinct_Study_Year_metadata_rows": len(meta),
        "original_interaction_rows_without_matching_study_year_metadata": unmatched_study_year,
        "distinct_Study_ids_in_observations": len(obs_by_study),
        "distinct_Study_Network_Year_keys": len(obs_by_network),
        "distinct_Study_Network_site_coordinate_keys": len(original_sites),
        "species_rank_confident_plant_names": len(plant_species_names),
        "all_plant_accepted_name_strings_all_ranks": len(plant_names),
        "uncertain_plant_name_observation_rows": uncert_plant,
        "plant_taxon_rank_observation_rows": dict(observed_taxonomic_rank),
        "records_with_missing_or_invalid_coordinates": malformed_geography,
        "records_without_parseable_year": unknown_year,
        "plant_species_confident_x_NHM_text_exact_names": len(observed_nhm),
        "plant_species_confident_x_NHM_text_any_colour": len(observed_color),
        "plant_species_confident_x_NHM_text_colour_and_structure": len(observed_color & observed_struct),
        "plant_species_confident_x_73_original_spectra_names": len(observed_spectra),
        "plant_species_confident_x_55_original_spectra_NHM_overlap": len(observed_55),
        "spectral_and_text_55_original_taxa_with_recorded_Bombus": len(plant_bombus),
        "spectral_and_text_55_original_taxa_with_Bombus_and_alternative_guild_in_same_network": len(cross_guild),
        "n_plant_species_x_network_year_units": len(joined),
        "n_plant_species_x_network_year_units_with_NHM": stats["network_species_units_NHM_literal"],
        "n_plant_species_x_network_year_units_with_NHM_colour": stats["network_species_units_NHM_text_colour"],
        "n_plant_species_x_network_year_units_with_original_real_spectra": stats["network_species_units_direct_petal_spectra_73"],
        "author_studies_with_multi_main_order_coverage_label": n_studies_with_multiple_source_orders,
        "sampling_effort_by_plant_and_guild_comparable": False,
        "recorded_visits_are_not_proven_pollination": True,
        "no_observed_guild_does_not_prove_absence": True,
        "no_bird_or_hummingbird_guild_in_EuPPollNet": True,
        "source_native_range_is_not_verified": True,
        "no_global_signal_causal_association_estimated": True,
        "uses_photographic_phenotypes": False,
    }
    return joined, summary


def read_stage68_csv(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nhm-original-compact", type=Path, required=True)
    p.add_argument("--spectral-text-join", type=Path, required=True)
    p.add_argument("--outdir", type=Path, required=True)
    a = p.parse_args()
    network = fetch_original("Interaction_data.csv.gz")
    metadata = list(dict_rows(fetch_original("Metadata.csv")))
    nhm = read_stage68_csv(a.nhm_original_compact)
    spectra = read_stage68_csv(a.spectral_text_join)
    joined, s = summarize(network, metadata, nhm, spectra)
    a.outdir.mkdir(parents=True, exist_ok=True)
    (a.outdir / "corrected_EuPPollNet_v130_NHM_text_original_spectra_receipt.json").write_text(
        json.dumps(s, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    if joined:
        with (a.outdir / "original_plant_network_year_observed_guilds_text_spectra.csv").open(
                "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=joined[0].keys())
            w.writeheader()
            w.writerows(joined)
    print("STAGE69_REAL_CORRECTED_EUPPOLLNET_TEXT_SPECTRA_SOURCE_AUDIT",
          json.dumps(s, ensure_ascii=False, sort_keys=True))
    print("NO_PHOTO_NO_SYNDROME_IMPUTED_GUILDS_NO_GUILD_ABSENCE_NO_CAUSAL_SEM")


if __name__ == "__main__":
    main()
