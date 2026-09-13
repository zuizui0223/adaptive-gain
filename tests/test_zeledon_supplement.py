from adaptive_gain.zeledon_supplement import (
    LOCKED_COMPOUNDS,
    SUPPLEMENT_FILENAME,
    audit_bioc_xml,
    supplement_url,
)


def _bioc(*passages: str) -> str:
    body = "".join(
        f"<passage><text>{text}</text></passage>" for text in passages
    )
    return f"<collection><document>{body}</document></collection>"


def test_canonical_supplement_url_is_locked_to_published_docx():
    url = supplement_url()
    assert "PMC11212260" in url
    assert SUPPLEMENT_FILENAME in url
    assert url.startswith("https://www.ncbi.nlm.nih.gov/")


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
