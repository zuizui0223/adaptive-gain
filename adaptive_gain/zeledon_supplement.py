"""Audit retrieval of the Zeledon et al. 2024 supplementary chemistry methods.

This helper does not infer chemical structures or synthesis routes from the main paper.
It queries the NCBI PMC-SM-BioC supplementary-material API for the published
Supplementary Material 3 and records only machine-checkable availability signals.

The output intentionally avoids copying the supplementary-methods prose.  It reports
whether the two preregistered Phase-1 compounds occur and whether chemistry-method
keywords occur near those identifiers.  A positive receipt is evidence that the
published supplement contains auditable material for chemistry-core review; it is
not by itself a declaration that a resynthesis has been validated.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Iterable
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

PMCID = "PMC11212260"
SUPPLEMENT_FILENAME = "13071_2024_6347_MOESM3_ESM.docx"
LOCKED_COMPOUNDS = ("TDI-014188", "TDI-014186")
BIOC_ENDPOINT = (
    "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/"
    "supplmat_relevant.cgi/bioc_xml/{pmcid}/{filename}"
)

CHEMISTRY_KEYWORDS = (
    "synthesis",
    "synthesized",
    "yield",
    "mmol",
    "nmr",
    "lcms",
    "lc-ms",
    "mass spectrometry",
    "intermediate",
    "purification",
    "chromatography",
)


@dataclass(frozen=True)
class CompoundAudit:
    compound_id: str
    occurrence_count: int
    chemistry_keyword_counts_nearby: dict[str, int]
    chemistry_context_present: bool


@dataclass(frozen=True)
class SupplementAuditReceipt:
    pmcid: str
    supplement_filename: str
    source_url: str
    response_sha256: str
    text_character_count: int
    compound_audits: tuple[CompoundAudit, ...]
    both_locked_compounds_found: bool
    both_have_chemistry_context: bool
    interpretation: str


def supplement_url(
    pmcid: str = PMCID,
    filename: str = SUPPLEMENT_FILENAME,
) -> str:
    """Return the canonical PMC-SM-BioC retrieval URL for the chemistry supplement."""

    return BIOC_ENDPOINT.format(pmcid=quote(pmcid), filename=quote(filename))


def bioc_text(xml_text: str) -> str:
    """Collect textual passages from BioC XML without preserving full document markup."""

    root = ET.fromstring(xml_text)
    passages: list[str] = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1].lower() == "text" and node.text:
            value = " ".join(node.text.split())
            if value:
                passages.append(value)
    return "\n".join(passages)


def _keyword_counts_near_matches(
    text: str,
    compound_id: str,
    *,
    radius: int = 1800,
    keywords: Iterable[str] = CHEMISTRY_KEYWORDS,
) -> tuple[int, dict[str, int]]:
    normalized = text.lower()
    target = compound_id.lower()
    starts = [m.start() for m in re.finditer(re.escape(target), normalized)]
    counts: Counter[str] = Counter()
    for start in starts:
        left = max(0, start - radius)
        right = min(len(normalized), start + len(target) + radius)
        window = normalized[left:right]
        for keyword in keywords:
            n = window.count(keyword.lower())
            if n:
                counts[keyword] += n
    return len(starts), dict(sorted(counts.items()))


def audit_bioc_xml(xml_text: str, *, source_url: str | None = None) -> SupplementAuditReceipt:
    """Return a non-verbatim availability receipt from retrieved supplementary BioC XML."""

    text = bioc_text(xml_text)
    audits: list[CompoundAudit] = []
    for compound_id in LOCKED_COMPOUNDS:
        occurrence_count, keyword_counts = _keyword_counts_near_matches(text, compound_id)
        audits.append(
            CompoundAudit(
                compound_id=compound_id,
                occurrence_count=occurrence_count,
                chemistry_keyword_counts_nearby=keyword_counts,
                chemistry_context_present=bool(occurrence_count and keyword_counts),
            )
        )

    both_found = all(a.occurrence_count > 0 for a in audits)
    both_chemistry = all(a.chemistry_context_present for a in audits)
    if both_chemistry:
        interpretation = (
            "PUBLISHED_CHEMISTRY_CONTEXT_LOCATED__CORE_REVIEW_STILL_REQUIRED"
        )
    elif both_found:
        interpretation = (
            "COMPOUNDS_LOCATED__CHEMISTRY_CONTEXT_NOT_YET_QUALIFIED"
        )
    else:
        interpretation = "SUPPLEMENT_RETRIEVED__LOCKED_COMPOUNDS_NOT_BOTH_LOCATED"

    return SupplementAuditReceipt(
        pmcid=PMCID,
        supplement_filename=SUPPLEMENT_FILENAME,
        source_url=source_url or supplement_url(),
        response_sha256=sha256(xml_text.encode("utf-8")).hexdigest(),
        text_character_count=len(text),
        compound_audits=tuple(audits),
        both_locked_compounds_found=both_found,
        both_have_chemistry_context=both_chemistry,
        interpretation=interpretation,
    )


def fetch_supplement_xml(*, timeout: float = 30.0) -> tuple[str, str]:
    """Retrieve the supplement through the official NCBI PMC-SM-BioC API."""

    url = supplement_url()
    request = Request(
        url,
        headers={"User-Agent": "adaptive-gain-supplement-audit/1.0"},
    )
    with urlopen(request, timeout=timeout) as response:  # nosec B310: fixed HTTPS host
        body = response.read().decode("utf-8")
    return url, body


def live_audit(*, timeout: float = 30.0) -> SupplementAuditReceipt:
    url, xml_text = fetch_supplement_xml(timeout=timeout)
    return audit_bioc_xml(xml_text, source_url=url)


def receipt_json(receipt: SupplementAuditReceipt) -> str:
    payload = asdict(receipt)
    return json.dumps(payload, indent=2, sort_keys=True)
