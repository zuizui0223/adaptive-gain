"""Stage68 original-data crosswalk: NHM botanical TEXT × Stage67 real PETAL spectra.

Join is literal source binomial only (not evidence of native sympatry, nectar
guides, pollinator-mediated selection, or equivalence of taxonomic concepts).
Original Stage67 73-species ZIP and its digest are pinned.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.request
import zipfile

STAGE67_ARTIFACT_ID = 14307499126
STAGE67_ZIP_SHA256 = "e5625a7202d8404e33281c9a4d4ef15d5af3e46f9070a67edcb253b60b4c0728"
STAGE67_FILENAME = "original_2024_73_petal_spectra_taxonomic_source_match_and_UV_modes.csv"
STAGE67_CSV_SHA256 = "373816146a88f69ef23883817d04271b420ab820182e8db034df9df6f424ba21"
STAGE67_SOURCE_DOI = "10.6084/m9.figshare.21081025.v2"
NHM_SOURCE_GIT_BLOB = "e1cfd2d5c518c2061ec91d1a9e8b64fc7ca69389"


def read_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def retrieve_prior_spectral_archive(token: str) -> bytes:
    if not token:
        raise ValueError("STAGE68_SOURCE_ARTIFACT_TOKEN_REQUIRED")
    req = urllib.request.Request(
        f"https://api.github.com/repos/zuizui0223/adaptive-gain/actions/artifacts/{STAGE67_ARTIFACT_ID}/zip",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "adaptive-gain-stage68-original-source-spectra-join"},
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        raw = r.read(2_000_001)
    if len(raw) > 2_000_000:
        raise ValueError("STAGE67_SPECTRAL_ARTIFACT_TOO_LARGE")
    verify_prior_archive(raw)
    return raw


def verify_prior_archive(raw: bytes):
    actual = hashlib.sha256(raw).hexdigest()
    if actual != STAGE67_ZIP_SHA256:
        raise ValueError(f"STAGE67_ORIGINAL_SPECTRA_ARTIFACT_DIGEST_CHANGED {actual}")


def read_prior_spectra(raw_zip: bytes):
    verify_prior_archive(raw_zip)
    with zipfile.ZipFile(io.BytesIO(raw_zip), "r") as z:
        info = z.getinfo(STAGE67_FILENAME)
        if info.file_size > 200_000:
            raise ValueError("STAGE67_SPECTRA_CSV_SIZE_UNEXPECTED")
        with z.open(info) as f:
            rows = list(csv.DictReader(io.StringIO(f.read().decode("utf-8"))))
    if len(rows) != 73:
        raise ValueError(f"STAGE67_REAL_SOURCE_EXPECTED_73_SPECTRA_NOT_{len(rows)}")
    if any(x["original_2024_Figshare_DOI"] != STAGE67_SOURCE_DOI for x in rows):
        raise ValueError("STAGE67_SPECTRA_NOT_ORIGINAL_FIGSHARE_SOURCE")
    if sum(bool(x["gbif_accepted_species_key_or_unknown"]) for x in rows) != 70:
        raise ValueError("STAGE67_70_STRICT_GBIF_TAXONOMIC_MAPPING_CHANGED")
    if len({x["original_2024_species_name"] for x in rows}) != 73:
        raise ValueError("STAGE67_ORIGINAL_SPECTRAL_TAXON_DUPLICATE")
    return rows


def join_text_and_spectra(nhm, spectra):
    # Literal source name exact matching only. Do not silently try synonym,
    # genus, fuzzy or WFO vs GBIF identifier imputation.
    nhm_by_name = {}
    for r in nhm:
        key = r["taxon"].strip().casefold()
        if not key:
            raise ValueError("STAGE68_NHM_EMPTY_SOURCE_TAXON")
        if key in nhm_by_name:
            raise ValueError("STAGE68_NHM_DUPLICATE_LITERAL_TAXON")
        nhm_by_name[key] = r
    output = []
    for s in spectra:
        name = s["original_2024_species_name"]
        n = nhm_by_name.get(name.strip().casefold())
        optical_accepted = bool(s["gbif_accepted_species_key_or_unknown"])
        out = {
            "spectral_original_species_name": name,
            "spectral_original_DOI": STAGE67_SOURCE_DOI,
            "spectral_GBIF_exact_accepted_key_or_unknown":
                s["gbif_accepted_species_key_or_unknown"],
            "NHM_literal_species_name_match": "YES" if n else "NO",
            "NHM_WFO_identifier_or_unknown": n["wfo"] if n else "",
            "NHM_original_recorded_flower_colour": n["flower colour"] if n else "",
            "NHM_original_recorded_petal_colour": n["petal colour"] if n else "",
            "NHM_original_recorded_corolla_colour": n["corolla colour"] if n else "",
            "NHM_original_recorded_flower_shape": n["flower shape"] if n else "",
            "NHM_original_recorded_flower_symmetry": n["flower symmetry"] if n else "",
            "NHM_original_recorded_flower_orientation": n["flower orientation"] if n else "",
            "NHM_original_recorded_corolla_tube_min_length":
                n["corolla tube min. length [cm]"] if n else "",
            "NHM_original_recorded_corolla_tube_max_length":
                n["corolla tube max. length [cm]"] if n else "",
            "NHM_any_reported_colour": int(n["visible_text_colour_recorded"]) if n else "",
            "NHM_any_reported_structure": int(n["structural_text_trait_recorded"]) if n else "",
            "original_2024_true_petal_UV_300_399_percent":
                s["source_UV_300_399_mean_reflectance_original_percent"],
            "original_2024_true_petal_visible_400_700_percent":
                s["source_visible_400_700_mean_reflectance_original_percent"],
            "prior_817_original_evidence_atlas_overlap":
                s["prior_817_atlas_accepted_taxon_overlap"],
            "source_join_scope":
                "SAME_LITERAL_SPECIES_NAME_NOT_NATIVE_SITE_OR_VISITOR" if n else
                "NO_LITERAL_SPECIES_MATCH_NOT_TRUE_NEGATIVE",
            "NHM_text_optical_spatial_UV_guide": "NOT_MEASURED",
            "native_source_site_visitor_data": "NOT_MEASURED",
            "accepted_taxonomy_scope":
                "SPECTRAL_GBIF_CONFIDENT_NHM_LITERAL_ONLY" if optical_accepted and n
                else "TAXONOMIC_CONCEPT_MATCH_NOT_ESTABLISHED",
        }
        output.append(out)
    matched = [r for r in output if r["NHM_literal_species_name_match"] == "YES"]
    both = [r for r in matched if r["NHM_any_reported_colour"] == 1 and
            r["NHM_any_reported_structure"] == 1]
    summary = {
        "schema": "stage68_NHM_botanical_text_x_stage67_original_73_petal_spectra_literal_join",
        "original_NHM_59369_file_Git_blob": NHM_SOURCE_GIT_BLOB,
        "original_Stage67_73_spectra_artifact_id": STAGE67_ARTIFACT_ID,
        "original_Stage67_spectra_artifact_sha256": STAGE67_ZIP_SHA256,
        "original_Stage67_petals_source_DOI": STAGE67_SOURCE_DOI,
        "n_original_spectral_botanical_names": len(spectra),
        "n_original_GBIF_strict_accepted_spectra": sum(bool(
            r["gbif_accepted_species_key_or_unknown"]) for r in spectra),
        "n_NHM_botanical_text_taxon_labels": len(nhm),
        "n_exact_literal_name_overlap": len(matched),
        "n_GBIF_strict_accepted_spectral_names_with_NHM_literal_match": sum(
            bool(r["spectral_GBIF_exact_accepted_key_or_unknown"]) for r in matched),
        "n_matched_with_text_colour_recorded": sum(
            r["NHM_any_reported_colour"] == 1 for r in matched),
        "n_matched_with_text_structure_recorded": sum(
            r["NHM_any_reported_structure"] == 1 for r in matched),
        "n_matched_with_both_text_colour_and_structure": len(both),
        "n_NHM_literal_overlap_already_in_prior_817_atlas": sum(
            r["prior_817_original_evidence_atlas_overlap"] == "True" for r in matched),
        "UV_spatial_guide_presence_or_absence_from_text": "NOT_MEASURED",
        "native_site_Bombus_or_other_visitors": "NOT_MEASURED",
        "new_global_effect_or_causal_medation": "NOT_ESTIMATED",
        "same_taxonomic_concept_guaranteed_by_literal_name": False,
    }
    return output, summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nhm-compact", required=True, type=Path)
    p.add_argument("--nhm-source-receipt", required=True, type=Path)
    p.add_argument("--prior-artifact-zip", type=Path)
    p.add_argument("--prior-extracted-csv", type=Path)
    p.add_argument("--outdir", required=True, type=Path)
    a = p.parse_args()
    n = read_csv(a.nhm_compact)
    receipt = json.loads(a.nhm_source_receipt.read_text(encoding="utf-8"))
    if (receipt["source_Git_blob_sha1"] != NHM_SOURCE_GIT_BLOB or
            receipt["original_text_description_taxon_rows"] != 59369 or
            len(n) != 59369):
        raise ValueError("STAGE68_NHM_ORIGINAL_SOURCE_IDENTITY_NOT_VERIFIED")
    if a.prior_extracted_csv:
        original_bytes = a.prior_extracted_csv.read_bytes()
        if hashlib.sha256(original_bytes).hexdigest() != STAGE67_CSV_SHA256:
            raise ValueError("STAGE67_AUTHENTIC_ORIGINAL_EXTRACTED_CSV_SHA_CHANGED")
        original = list(csv.DictReader(io.StringIO(original_bytes.decode("utf-8"))))
        if (len(original) != 73 or
                sum(bool(x["gbif_accepted_species_key_or_unknown"]) for x in original) != 70 or
                len({x["original_2024_species_name"] for x in original}) != 73 or
                any(x["original_2024_Figshare_DOI"] != STAGE67_SOURCE_DOI for x in original)):
            raise ValueError("STAGE67_SOURCE_DATA_73_70_OR_DOI_NOT_VERIFIED")
    else:
        raw = (a.prior_artifact_zip.read_bytes() if a.prior_artifact_zip
               else retrieve_prior_spectral_archive(os.environ.get("GH_TOKEN", "")))
        original = read_prior_spectra(raw)
    joined, summary = join_text_and_spectra(n, original)
    a.outdir.mkdir(parents=True, exist_ok=True)
    with (a.outdir / "stage67_real73_NHM_original_text_exact_literal_join.csv").open(
            "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(joined[0]))
        w.writeheader()
        w.writerows(joined)
    (a.outdir / "stage68_original_73_spectra_x_NHM_text_overlap_receipt.json").write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print("STAGE68_SOURCE_AUTHENTICATED_SPECTRA_X_TEXT_OVERLAP",
          json.dumps(summary, sort_keys=True))
    print("NO_UV_GUIDE_BINARY_NO_NATIVE_POLLINATOR_COOCURRENCE_NO_SEM")


if __name__ == "__main__":
    main()
