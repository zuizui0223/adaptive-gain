from io import BytesIO
from zipfile import ZipFile

from adaptive_gain.zeledon_supplement import (
    LOCKED_COMPOUNDS,
    SUPPLEMENT_FILENAME,
    audit_bioc_xml,
    audit_docx_bytes,
    aws_supplement_url,
    docx_text,
    supplement_url,
)


def _bioc(*passages: str) -> str:
    body = "".join(
        f"<passage><text>{text}</text></passage>" for text in passages
    )
    return f"<collection><document>{body}</document></collection>"


def _docx(*paragraphs: str) -> bytes:
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    body = "".join(
        f'<w:p><w:r><w:t>{text}</w:t></w:r></w:p>' for text in paragraphs
    )
    xml = f'<w:document xmlns:w="{ns}"><w:body>{body}</w:body></w:document>'
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr("word/document.xml", xml)
    return buffer.getvalue()


def test_canonical_supplement_urls_are_locked_to_published_docx():
    bioc_url = supplement_url()
    aws_url = aws_supplement_url()

    assert "PMC11212260" in bioc_url
    assert SUPPLEMENT_FILENAME in bioc_url
    assert bioc_url.startswith("https://www.ncbi.nlm.nih.gov/")

    assert "PMC11212260.1" in aws_url
    assert SUPPLEMENT_FILENAME in aws_url
    assert aws_url.startswith("https://pmc-oa-opendata.s3.amazonaws.com/")


def test_both_locked_compounds_with_chemistry_context_are_detected():
    xml = _bioc(
        "Synthesis of TDI-014188. The intermediate was purified by chromatography and the yield was recorded.",
        "TDI-014186 was synthesized from an intermediate; NMR and LCMS were used for characterization.",
    )
    receipt = audit_bioc_xml(xml, source_url="https://example.test/supp")

    assert tuple(a.compound_id for a in receipt.compound_audits) == LOCKED_COMPOUNDS
    assert receipt.both_locked_compounds_found is True
    assert receipt.both_have_chemistry_context is True
    assert receipt.interpretation == (
        "PUBLISHED_CHEMISTRY_CONTEXT_LOCATED__CORE_REVIEW_STILL_REQUIRED"
    )


def test_compound_mentions_without_chemistry_context_do_not_overclaim():
    xml = _bioc(
        "Behavioral comparison includes TDI-014188 and TDI-014186 in the active set."
    )
    receipt = audit_bioc_xml(xml)

    assert receipt.both_locked_compounds_found is True
    assert receipt.both_have_chemistry_context is False
    assert receipt.interpretation == (
        "COMPOUNDS_LOCATED__CHEMISTRY_CONTEXT_NOT_YET_QUALIFIED"
    )


def test_missing_locked_compound_stays_unqualified():
    xml = _bioc("Synthesis of TDI-014188 with NMR characterization and purification.")
    receipt = audit_bioc_xml(xml)

    assert receipt.compound_audits[0].occurrence_count == 1
    assert receipt.compound_audits[1].occurrence_count == 0
    assert receipt.both_locked_compounds_found is False
    assert receipt.both_have_chemistry_context is False
    assert receipt.interpretation == (
        "SUPPLEMENT_RETRIEVED__LOCKED_COMPOUNDS_NOT_BOTH_LOCATED"
    )


def test_docx_fallback_extracts_text_and_audits_without_network():
    data = _docx(
        "Synthesis of TDI-014188 gave the target after chromatography; NMR and yield were recorded.",
        "TDI-014186 was synthesized through an intermediate and checked by LCMS.",
    )

    extracted = docx_text(data)
    assert "TDI-014188" in extracted
    assert "TDI-014186" in extracted

    receipt = audit_docx_bytes(data, source_url="https://example.test/supp.docx")
    assert receipt.both_locked_compounds_found is True
    assert receipt.both_have_chemistry_context is True
    assert receipt.response_sha256
