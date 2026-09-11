from __future__ import annotations

import hashlib
from pathlib import Path
import runpy
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / "manuscript"
SOURCE = MANUSCRIPT_DIR / "MANUSCRIPT_V1.md"
LEGENDS = MANUSCRIPT_DIR / "FIGURE_LEGENDS_V1.md"
ASSEMBLER = MANUSCRIPT_DIR / "assemble_submission_markdown.py"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_namespace() -> dict[str, object]:
    return runpy.run_path(str(ASSEMBLER), run_name="submission_assembly_import")


def test_submission_assembly_is_pure_insertion() -> None:
    namespace = _load_namespace()
    source = SOURCE.read_text(encoding="utf-8")
    legends_text = LEGENDS.read_text(encoding="utf-8")
    assembled = namespace["assemble"](source, legends_text)

    callouts = namespace["CALLOUTS"]
    extracted_legends = namespace["_extract_legends"](legends_text)
    reference_heading = namespace["REFERENCE_HEADING"]
    legend_block = "## Figure legends\n\n" + "\n\n".join(extracted_legends) + "\n\n"

    stripped = assembled
    for _, callout in callouts:
        assert assembled.count(callout) == 1
        stripped = stripped.replace("\n\n" + callout, "", 1)
    stripped = stripped.replace(legend_block, "", 1)

    assert stripped == source
    assert assembled.count(reference_heading) == 1
    assert assembled.count("## Figure legends") == 1
    assert assembled.index("## Figure legends") < assembled.index(reference_heading)
    for number in range(1, 5):
        assert assembled.count(f"Figure {number} |") == 1


def test_cli_assembly_does_not_mutate_scientific_source(tmp_path: Path) -> None:
    source_sha_before = _sha256(SOURCE)
    output = tmp_path / "MANUSCRIPT_SUBMISSION.md"

    subprocess.run(
        [sys.executable, str(ASSEMBLER), "--output", str(output)],
        cwd=ROOT,
        check=True,
    )

    assert output.exists()
    assert _sha256(SOURCE) == source_sha_before
    text = output.read_text(encoding="utf-8")
    assert "## Figure legends" in text
    assert "AUTHOR INPUT REQUIRED" not in text
    namespace = _load_namespace()
    for _, callout in namespace["CALLOUTS"]:
        assert text.count(callout) == 1
    for number in range(1, 5):
        assert f"Figure {number} |" in text
