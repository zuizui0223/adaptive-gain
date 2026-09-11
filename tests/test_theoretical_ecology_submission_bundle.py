from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import runpy
import subprocess
import sys
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "manuscript" / "build_submission_bundle.py"
EXPECTED_NAMES = [
    "BUNDLE_MANIFEST.json",
    "MANUSCRIPT_SUBMISSION.md",
    "SUPPLEMENT_V1.md",
    "figure1_state_space.svg",
    "figure2_reachability.svg",
    "figure3_extremal_envelope.svg",
    "figure4_long_time_outcomes.svg",
]


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_scientific_bundle_is_byte_reproducible(tmp_path: Path) -> None:
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"

    subprocess.run([sys.executable, str(BUILDER), "--output", str(first)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(BUILDER), "--output", str(second)], cwd=ROOT, check=True)

    assert first.read_bytes() == second.read_bytes()
    assert _sha256(first) == _sha256(second)


def test_bundle_contains_only_declared_scientific_payloads(tmp_path: Path) -> None:
    output = tmp_path / "bundle.zip"
    namespace = runpy.run_path(str(BUILDER), run_name="bundle_builder_import")
    namespace["build"](output)

    with ZipFile(output, "r") as archive:
        assert archive.namelist() == EXPECTED_NAMES
        for info in archive.infolist():
            assert info.date_time == (1980, 1, 1, 0, 0, 0)
            assert info.compress_type == 0

        manifest = json.loads(archive.read("BUNDLE_MANIFEST.json"))
        assert manifest["bundle_spec"] == "theoretical_ecology_scientific_bundle_v1"
        assert manifest["status"] == "scientific_content_complete_author_metadata_pending"
        assert manifest["author_controlled_metadata_included"] is False

        recorded = {entry["name"]: entry for entry in manifest["files"]}
        assert set(recorded) == set(EXPECTED_NAMES) - {"BUNDLE_MANIFEST.json"}
        for name, entry in recorded.items():
            data = archive.read(name)
            assert len(data) == entry["bytes"]
            assert sha256(data).hexdigest() == entry["sha256"]

        manuscript = archive.read("MANUSCRIPT_SUBMISSION.md").decode("utf-8")
        assert "## Figure legends" in manuscript
        for number in range(1, 5):
            assert f"Figure {number} |" in manuscript
        assert "AUTHOR INPUT REQUIRED" not in manuscript
        assert "SUBMISSION_DECLARATIONS_V1" not in manuscript


def test_bundle_reuses_committed_supplement_and_figures_exactly(tmp_path: Path) -> None:
    output = tmp_path / "bundle.zip"
    namespace = runpy.run_path(str(BUILDER), run_name="bundle_builder_import")
    namespace["build"](output)

    with ZipFile(output, "r") as archive:
        assert archive.read("SUPPLEMENT_V1.md") == (ROOT / "manuscript" / "SUPPLEMENT_V1.md").read_bytes()
        for name in EXPECTED_NAMES:
            if not name.endswith(".svg"):
                continue
            assert archive.read(name) == (ROOT / "manuscript" / "figures" / name).read_bytes()
