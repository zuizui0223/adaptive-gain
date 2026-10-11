"""Export reproducible V6 SVG figures to one-page submission PDF files.

Evolution Letters accepts vector PDF figures; SVG is retained as an editable
source and is not represented as the publisher's accepted upload format.

This is an OPTIONAL authoring step requiring CairoSVG (pip install cairosvg).
It does not affect theorem tests or main figure SVG regeneration.
The PDF pages retain the SVG viewBox dimensions (1200 x 740 in
CSS pixels, exported as 900 x 555 PDF points at 96 dpi).
It is the author's responsibility to review actual PDF appearance,
fonts, clipping and figure legend / data presentation before submission.

Usage:
    python -m scripts.render_v6_figures --output-dir v6_figures
    python -m scripts.export_v6_figures_pdf --figure-dir v6_figures
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def export(directory: Path) -> dict:
    """Convert the deterministic current SVG triptych, with source hashes."""
    try:
        import cairosvg
    except ImportError as exc:
        raise RuntimeError(
            "CairoSVG is optional; install cairosvg to export journal-ready PDF"
        ) from exc

    if not directory.is_dir():
        raise FileNotFoundError(f"figure directory not found: {directory}")
    original_manifest=directory/"svg_manifest.json"
    document=json.loads(original_manifest.read_text(encoding="utf-8"))
    figure_map=document.get("figures",{})
    if set(figure_map) != {"figure_1","figure_2","figure_3"}:
        raise ValueError("require exactly three verified SVG figure keys")
    outputs={}
    for figure,entry in sorted(figure_map.items()):
        svg_file=directory/entry["filename"]
        source=svg_file.read_bytes()
        svg_sha=hashlib.sha256(source).hexdigest()
        if svg_sha != entry["sha256"] or len(source) != entry["content_bytes"]:
            raise ValueError(f"source SVG hash or size differs from its receipt: {figure}")
        pdf_file=svg_file.with_suffix(".pdf")
        # Convert vector SVG geometry and text, not low-resolution screenshots.
        cairosvg.svg2pdf(bytestring=source,write_to=str(pdf_file))
        pdf=pdf_file.read_bytes()
        if not pdf.startswith(b"%PDF-") or len(pdf)<500:
            raise ValueError(f"invalid or empty PDF export: {pdf_file}")
        outputs[figure]={
            "pdf_filename":pdf_file.name,
            "pdf_sha256":hashlib.sha256(pdf).hexdigest(),
            "pdf_bytes":len(pdf),
            "source_svg_filename":svg_file.name,
            "source_svg_sha256":svg_sha,
            "intended_submission_format":"vector PDF, one page per figure",
        }
    manifest={
        "status":"V6_SVG_TO_PDF_SUBMISSION_FORMAT_EXPORT_COMPLETED",
        "source_svg_manifest":"svg_manifest.json",
        "figures":outputs,
        "claim_ceiling":(
            "Machine PDF generation does not imply human visual approval, "
            "font embedding check, journal editorial acceptance or scientific "
            "validation beyond the SVG/data source receipts."
        ),
    }
    (directory/"pdf_manifest.json").write_text(
        json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8"
    )
    return manifest


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--figure-dir",type=Path,default=Path("v6_figures"))
    args=cli.parse_args()
    print(json.dumps(export(args.figure_dir),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
