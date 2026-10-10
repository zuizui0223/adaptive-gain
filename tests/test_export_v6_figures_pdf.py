"""Optional vector-PDF export regression from the frozen V6 SVG source."""

import hashlib
import json
from pathlib import Path

import pytest

from scripts.render_v6_figures import render
from scripts.export_v6_figures_pdf import export


def test_v6_three_journal_pdf_exports_have_sha256_and_unchanged_svg_sources(tmp_path):
    pytest.importorskip("cairosvg")
    render(tmp_path)
    result=export(tmp_path)
    assert result["status"] == "V6_SVG_TO_PDF_SUBMISSION_FORMAT_EXPORT_COMPLETED"
    assert len(result["figures"]) == 3
    for key,entry in result["figures"].items():
        pdf=(tmp_path/entry["pdf_filename"]).read_bytes()
        svg=(tmp_path/entry["source_svg_filename"]).read_bytes()
        assert pdf.startswith(b"%PDF-")
        assert len(pdf) > 500
        assert len(svg) > 2500
        assert hashlib.sha256(pdf).hexdigest() == entry["pdf_sha256"]
        assert hashlib.sha256(svg).hexdigest() == entry["source_svg_sha256"]
    manifest=json.loads((tmp_path/"pdf_manifest.json").read_text(encoding="utf-8"))
    assert manifest==result


def test_v6_pdf_export_refuses_unverified_or_modified_svg_source(tmp_path):
    pytest.importorskip("cairosvg")
    render(tmp_path)
    figure=tmp_path/"fig2_robust_no_go.svg"
    figure.write_bytes(figure.read_bytes()+b"\n<!-- mutation -->\n")
    with pytest.raises(ValueError,match="hash or size differs"):
        export(tmp_path)


def test_v6_pdf_export_requires_prior_verified_three_figure_manifest(tmp_path):
    pytest.importorskip("cairosvg")
    with pytest.raises(FileNotFoundError):
        export(tmp_path/"absent")
    (tmp_path/"svg_manifest.json").write_text(
        json.dumps({"figures":{"figure_1":{"filename":"no.svg","sha256":"x",
        "content_bytes":0}}}),encoding="utf-8"
    )
    with pytest.raises(ValueError,match="exactly three"):
        export(tmp_path)
