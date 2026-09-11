"""Build a deterministic scientific submission bundle for Theoretical Ecology.

The bundle contains only scientific upload material that is already frozen:
assembled manuscript body, supplement, four SVG figures, and a generated manifest.
Author-controlled title-page metadata and declarations are intentionally excluded.
"""
from __future__ import annotations

from argparse import ArgumentParser
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / "manuscript"
FIGURE_DIR = MANUSCRIPT_DIR / "figures"
ASSEMBLER = MANUSCRIPT_DIR / "assemble_submission_markdown.py"
SOURCE = MANUSCRIPT_DIR / "MANUSCRIPT_V1.md"
LEGENDS = MANUSCRIPT_DIR / "FIGURE_LEGENDS_V1.md"
SUPPLEMENT = MANUSCRIPT_DIR / "SUPPLEMENT_V1.md"
DEFAULT_OUTPUT = ROOT / "dist" / "theoretical-ecology-scientific-bundle-v1.zip"
SOURCE_RELEASE_REF = "release/theoretical-ecology-submission-finalization-v1"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

FIGURES = (
    FIGURE_DIR / "figure1_state_space.svg",
    FIGURE_DIR / "figure2_reachability.svg",
    FIGURE_DIR / "figure3_extremal_envelope.svg",
    FIGURE_DIR / "figure4_long_time_outcomes.svg",
)


def _load_assembler():
    spec = importlib.util.spec_from_file_location("submission_assembler", ASSEMBLER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load submission assembler")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _hash(data: bytes) -> str:
    return sha256(data).hexdigest()


def _zipinfo(name: str) -> ZipInfo:
    info = ZipInfo(name, date_time=FIXED_ZIP_TIME)
    info.compress_type = ZIP_STORED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def _payloads() -> dict[str, bytes]:
    assembler = _load_assembler()
    manuscript = assembler.assemble(
        SOURCE.read_text(encoding="utf-8"),
        LEGENDS.read_text(encoding="utf-8"),
    ).encode("utf-8")

    payloads: dict[str, bytes] = {
        "MANUSCRIPT_SUBMISSION.md": manuscript,
        "SUPPLEMENT_V1.md": SUPPLEMENT.read_bytes(),
    }
    for figure in FIGURES:
        payloads[figure.name] = figure.read_bytes()
    return payloads


def _manifest(payloads: dict[str, bytes]) -> bytes:
    roles = {
        "MANUSCRIPT_SUBMISSION.md": "assembled manuscript body with controlled figure callouts and legends",
        "SUPPLEMENT_V1.md": "supplementary theory and implementation details",
        "figure1_state_space.svg": "main figure 1",
        "figure2_reachability.svg": "main figure 2",
        "figure3_extremal_envelope.svg": "main figure 3",
        "figure4_long_time_outcomes.svg": "main figure 4",
    }
    manifest = {
        "bundle_spec": "theoretical_ecology_scientific_bundle_v1",
        "status": "scientific_content_complete_author_metadata_pending",
        "source_release_ref": SOURCE_RELEASE_REF,
        "scientific_source": "manuscript/MANUSCRIPT_V1.md",
        "assembled_with": "manuscript/assemble_submission_markdown.py",
        "author_controlled_metadata_included": False,
        "excluded_author_controlled_fields": [
            "final author list and order",
            "affiliations",
            "corresponding author and correspondence address",
            "ORCIDs",
            "funding statement",
            "competing-interests declaration",
            "author-contribution statement",
        ],
        "files": [
            {
                "name": name,
                "role": roles[name],
                "bytes": len(payloads[name]),
                "sha256": _hash(payloads[name]),
            }
            for name in sorted(payloads)
        ],
    }
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build(output: Path = DEFAULT_OUTPUT) -> Path:
    payloads = _payloads()
    payloads["BUNDLE_MANIFEST.json"] = _manifest(payloads)
    output.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output, "w", compression=ZIP_STORED) as archive:
        for name in sorted(payloads):
            archive.writestr(_zipinfo(name), payloads[name])
    return output


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.output)
