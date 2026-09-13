from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V2.md"
FORMAT_RECEIPT = ROOT / "manuscript" / "EVOLUTION_LETTERS_FORMAT_RECEIPT_20260913.md"


def _section(text: str, heading: str, next_heading: str) -> str:
    start = text.index(heading) + len(heading)
    end = text.index(next_heading, start)
    return text[start:end].strip()


def _words(text: str) -> list[str]:
    # Internal conservative surface check; not a claim about the portal counter.
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

    start = text.index("## Introduction")
    end = text.index("## Data and code availability")
    assert len(_words(text[start:end])) <= 5000


def test_state_gap_and_between_state_contrast_are_not_collapsed():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "g_i=C_F(i)-C_A(i)" in text
    assert "Delta g=g_2-g_1" in text
    assert "Delta g=C_F-C_A" not in text
    assert "Because every state gap is nonnegative" in text
    assert "at least one ecological state must support `g_i>=q`" in text


def test_no_go_claim_ceiling_is_explicit():
    lower = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "no sensing-to-selection map" in lower
    assert "crossing the bound is only necessary" in lower
    assert "does not guarantee" in lower
    assert "within the declared model class" in lower
    for phrase in (
        "gap 2 guarantees oscillation for every nonlinear",
        "above the threshold oscillation must occur",
        "finite sensing architecture determines natural feedback magnitude",
    ):
        assert phrase not in lower


def test_theoretical_ecology_fallback_is_not_rewritten_by_promotion_surface():
    fallback = ROOT / "manuscript" / "MANUSCRIPT_V1.md"
    assert fallback.exists()
    fallback_text = fallback.read_text(encoding="utf-8")
    assert fallback_text.startswith("# Finite sensing structure constrains eco-evolutionary feedback regimes")
    assert "## 3. Results" in fallback_text
