"""Stage68: Source-pinned botanical TEXT traits, NEVER plant photographs.

This ingests only NHM 'output/raw/ocr-traits' NLP descriptions. It does not
measure UV spatial patterns, flower-age cue transitions, scent or pollinator
guilds. A missing descriptor is UNKNOWN, never a measured trait negative.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

REPO = "NaturalHistoryMuseum/plant-traits"
RAW = "https://raw.githubusercontent.com/" + REPO + "/main/output/raw/ocr-traits/"
# Confirmed from the original repository's Git objects on 2026-11-17.
SOURCE_GIT_BLOBS = {
    "ecoflora.csv": "dbdc6b4469583743b8b35e26912d21d05b550f32",
    "combined.csv": "e1cfd2d5c518c2061ec91d1a9e8b64fc7ca69389",
}
REQUIRED = (
    "taxon", "flower colour", "petal colour", "corolla colour",
    "flower shape", "flower symmetry", "flower orientation",
    "corolla tube min. length [cm]", "corolla tube max. length [cm]",
)
COLOUR = ("flower colour", "petal colour", "corolla colour")
STRUCTURE = (
    "flower shape", "flower symmetry", "flower orientation",
    "corolla tube min. length [cm]", "corolla tube max. length [cm]",
)
OTHER = ("pollination", "reward", "reproduction system", "source", "wfo")
EXTRACT = ("taxon",) + COLOUR + STRUCTURE + OTHER
BINOMIAL = re.compile(r"^[A-Z][a-zA-Z-]+ [a-z][a-z-]+$")


def github_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def verify_blob(raw: bytes, expected_sha: str) -> None:
    got = github_blob_sha(raw)
    if got != expected_sha:
        raise ValueError(f"STAGE68_ORIGINAL_SOURCE_GIT_BLOB_SHA_MISMATCH expected={expected_sha} actual={got}")


def download(name: str) -> bytes:
    if name not in SOURCE_GIT_BLOBS:
        raise ValueError("STAGE68_UNKNOWN_SOURCE_FILE")
    req = urllib.request.Request(
        RAW + name,
        headers={"User-Agent": "adaptive-gain-stage68-text-trait-verified-source/2026",
                 "Accept": "text/csv"},
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        raw = response.read(26_000_001)
    if not raw or len(raw) > 26_000_000:
        raise ValueError("STAGE68_SOURCE_EMPTY_OR_TOO_LARGE")
    verify_blob(raw, SOURCE_GIT_BLOBS[name])
    return raw


def extract(raw: bytes, name: str):
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if not reader.fieldnames:
        raise ValueError("STAGE68_MISSING_SOURCE_HEADER")
    missing = set(REQUIRED) - set(reader.fieldnames)
    if missing:
        raise ValueError(f"STAGE68_REQUIRED_TEXT_COLUMNS_MISSING {sorted(missing)}")
    nonempty = Counter()
    name_counts = Counter()
    n_colour = n_structure = n_both = n_binomial = 0
    compact = []
    for i, row in enumerate(reader, start=1):
        if any(key is None for key in row):
            raise ValueError(f"STAGE68_EXTRA_OR_BROKEN_CSV_COLUMNS_AT_ROW_{i}")
        original = {key: (row.get(key) or "").strip() for key in EXTRACT}
        if not original["taxon"]:
            raise ValueError(f"STAGE68_EMPTY_TAXON_AT_ROW_{i}")
        original["source_row_number"] = i
        original["visible_text_colour_recorded"] = int(any(original[k] for k in COLOUR))
        original["structural_text_trait_recorded"] = int(any(original[k] for k in STRUCTURE))
        original["literal_binomial_heuristic_only"] = int(bool(BINOMIAL.fullmatch(original["taxon"])))
        original["UV_spatial_guide_measurement"] = "UNKNOWN_NOT_MEASURED_IN_TEXT_SOURCE"
        original["pollinator_guild_from_colour"] = "UNKNOWN_NOT_INFERRED"
        original["same_site_receiver_cooccurrence"] = "UNKNOWN_NOT_MEASURED"
        n_colour += original["visible_text_colour_recorded"]
        n_structure += original["structural_text_trait_recorded"]
        n_both += original["visible_text_colour_recorded"] * original["structural_text_trait_recorded"]
        n_binomial += original["literal_binomial_heuristic_only"]
        for k in COLOUR + STRUCTURE + ("pollination", "reward", "reproduction system"):
            nonempty[k] += bool(original[k])
        name_counts[original["taxon"]] += 1
        compact.append(original)
    summary = {
        "schema": "stage68_authentic_NHM_plant_trait_NLP_TEXT_not_images_v1",
        "source_dataset": "NaturalHistoryMuseum/plant-traits",
        "source_repository_file": "output/raw/ocr-traits/" + name,
        "source_Git_blob_sha1": github_blob_sha(raw),
        "source_byte_sha256": hashlib.sha256(raw).hexdigest(),
        "source_raw_bytes": len(raw),
        "source_license": "CC-BY, attributed to Natural History Museum source repository",
        "original_text_description_taxon_rows": len(compact),
        "distinct_literal_taxon_labels": len(name_counts),
        "duplicated_literal_taxon_labels": sum(x - 1 for x in name_counts.values()),
        "simple_literal_binomial_rows_not_validated_species": n_binomial,
        "visible_colour_any_of_three_organs_recorded": n_colour,
        "structure_any_of_five_text_fields_recorded": n_structure,
        "visible_colour_and_structure_recorded": n_both,
        "per_field_nonempty_counts": dict(nonempty),
        "unmeasured_UV_spatial_guide_negative_states": 0,
        "native_site_pollinator_visits_extracted": 0,
        "stage67_species_atlas_taxonomic_overlap_calculated": False,
        "photo_input_or_derived_photo_colour": False,
        "claim_global_colour_x_bee_effect": False,
        "missing_field_is_unknown_not_negative": True,
        "source_measurement_grain": "automated botanical description trait per source taxon label",
    }
    return compact, summary


def save(compact, summary, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "original_NHM_text_trait_source_coverage.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with (outdir / "original_NHM_text_traits_compact.csv").open(
        "w", encoding="utf-8", newline=""
    ) as f:
        writer = csv.DictWriter(f, fieldnames=list(compact[0]))
        writer.writeheader()
        writer.writerows(compact)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=sorted(SOURCE_GIT_BLOBS), default="ecoflora.csv")
    p.add_argument("--outdir", type=Path, required=True)
    a = p.parse_args()
    raw = download(a.source)
    compact, summary = extract(raw, a.source)
    if a.source == "ecoflora.csv":
        # Frozen independent read of the original authenticated source (2026-11-17).
        expected = (1989, 1141, 304, 249)
        found = tuple(summary[k] for k in (
            "original_text_description_taxon_rows",
            "visible_colour_any_of_three_organs_recorded",
            "structure_any_of_five_text_fields_recorded",
            "visible_colour_and_structure_recorded",
        ))
        if found != expected:
            raise ValueError(f"STAGE68_ORIGINAL_ECOFLORA_COVERAGE_NOT_REPRODUCED found={found}")
    save(compact, summary, a.outdir)
    print("STAGE68_ORIGINAL_SOURCE_TEXT_ONLY_COVERAGE_VERIFIED",
          json.dumps(summary, sort_keys=True))
    print("NO_PHOTOS_NO_UV_NEGATIVES_NO_POLLINATOR_GUILD_INFERENCE_NO_SEM")


if __name__ == "__main__":
    main()
