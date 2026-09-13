from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V1.md"
FORMAT_RECEIPT = ROOT / "manuscript" / "EVOLUTION_LETTERS_FORMAT_RECEIPT_20260913.md"


def _section(text: str, heading: str, next_heading: str) -> str:
    start = text.index(heading) + len(heading)
    end = text.index(next_heading, start)
    return text[start:end].strip()


def _words(text: str) -> list[str]:
    # Count prose-like word tokens while treating displayed equations and markdown
    # punctuation as non-words. This is an internal conservative surface check,
    # not a claim about the journal portal's eventual counter.
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text)


def test_evolution_letters_surface_exists_and_format_receipt_is_current():
    assert MANUSCRIPT.exists()
    receipt = FORMAT_RECEIPT.read_text(encoding="utf-8")
    for phrase in (
        "5,000 words",
        "300 words maximum",
        "150 words maximum",
        "theoretical studies",
        "dispatch-time recheck",
    ):
        assert phrase in receipt


def test_title_abstract_teaser_and_keyword_limits():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    title = text.splitlines()[0].removeprefix("# ").strip()
    assert len(_words(title)) <= 30

    teaser = _section(text, "## Teaser text", "## Abstract")
    abstract = _section(text, "## Abstract", "**Keywords:**")
    assert len(_words(teaser)) <= 150
    assert len(_words(abstract)) <= 300

    keyword_line = next(line for line in text.splitlines() if line.startswith("**Keywords:**"))
    keywords = [x.strip() for x in keyword_line.split(":", 1)[1].split(";") if x.strip()]
    assert len(keywords) <= 10


def test_main_text_is_within_letter_length_and_has_required_sections():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for heading in ("## Introduction", "## Methods", "## Results", "## Discussion", "## References"):
        assert heading in text

    # Evolution Letters excludes tables, figure captions and references from the
    # ~5000-word Letter guide. This candidate currently has no tables or figure
    # captions in the manuscript surface, so count from Introduction to end matter.
    start = text.index("## Introduction")
    end = text.index("## Data and code availability")
    main_text = text[start:end]
    assert len(_words(main_text)) <= 5000


def test_no_go_claim_ceiling_is_explicit():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = text.lower()
    assert "no sensing-to-selection map" in lower
    assert "crossing the bound is only necessary" in lower
    assert "does not guarantee" in lower
    assert "within the declared model class" in lower

    # The broad nonlinear theorem must not be written as a generic sufficiency claim.
    forbidden = (
        "gap 2 guarantees oscillation for every nonlinear",
        "above the threshold oscillation must occur",
        "finite sensing architecture determines natural feedback magnitude",
    )
    for phrase in forbidden:
        assert phrase not in lower


def test_theoretical_ecology_fallback_is_not_rewritten_by_promotion_surface():
    fallback = ROOT / "manuscript" / "MANUSCRIPT_V1.md"
    assert fallback.exists()
    fallback_text = fallback.read_text(encoding="utf-8")
    assert fallback_text.startswith("# Finite sensing structure constrains eco-evolutionary feedback regimes")
    assert "## 3. Results" in fallback_text
