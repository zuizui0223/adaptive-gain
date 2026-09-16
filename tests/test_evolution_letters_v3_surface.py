from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V3.md"
SUPPLEMENT = ROOT / "manuscript" / "SUPPLEMENT_EVOLUTION_LETTERS_V2.md"
ATLAS = ROOT / "manuscript" / "MATHEMATICAL_ATLAS_V1.md"


def _text(path: Path) -> str:
    assert path.exists(), path
    return path.read_text(encoding="utf-8")


def _section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def _prose_word_count(text: str) -> int:
    # Submission-facing guardrail, not a typesetter-exact Oxford count.
    # Remove display math and Markdown punctuation, then count word-like prose tokens.
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"`[^`]+`", " ", text)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text))


def test_v3_letter_surface_stays_within_recorded_length_guidance():
    text = _text(MANUSCRIPT)
    title = text.splitlines()[0].lstrip("# ")
    teaser = _section(text, "## Teaser text", "## Abstract")
    abstract = _section(text, "## Abstract", "**Keywords:**")
    main = _section(text, "## Introduction", "## Data and code availability")

    assert _prose_word_count(title) <= 30
    assert _prose_word_count(teaser) <= 150
    assert _prose_word_count(abstract) <= 300
    assert _prose_word_count(main) <= 5000


def test_v3_contains_exact_adaptive_only_budget_window_and_three_regions():
    text = _text(MANUSCRIPT)
    assert "C_A\\le B<C_F" in text
    assert "If `B<C_A`" in text
    assert "Once `B>=C_F`" in text
    assert "adaptive-only" in text
    assert "hard ecological deadline" in text


def test_v3_uses_balanced_unbounded_result_without_overclaiming_fixed_scope_sharpness():
    text = _text(MANUSCRIPT)
    assert "exactly 50/50 balanced" in text
    assert "\\frac{2^d}{d+1}" in text
    assert "\\longrightarrow\\infty" in text
    assert "global cue prevalence or marginal balance is not the structural quantity" in text
    assert "existence result rather than a sharp maximum at fixed `(n,m)`" in text


def test_v3_retains_nonlinear_no_go_and_necessary_not_sufficient_firewall():
    text = _text(MANUSCRIPT)
    assert "nondecreasing" in text
    assert "bounded marginal effect" in text
    assert "G\\le B_fL\\Delta g" in text
    assert "no sensing-to-selection map" in text
    assert "Crossing the bound is only necessary" in text
    assert "guarantees oscillation" not in text.lower()


def test_v3_keeps_finite_architecture_distinct_from_shannon_information():
    text = _text(MANUSCRIPT)
    assert "We do not propose a new general minimum-information principle" in text
    assert "finite deterministic architecture" in text
    assert "Shannon information" in text


def test_v3_retains_recurrence_alignment_and_feedback_identifiability_limits():
    text = _text(MANUSCRIPT)
    assert "Slow ecological modes therefore matter only when sensing-generated selection variation projects onto them" in text
    assert "does not identify feedback magnitude" in text
    assert "causal contribution of sensing architecture" in text


def test_v3_kernel_is_target_relevant_coarse_graining_not_generic_ecological_equivalence():
    text = _text(MANUSCRIPT)
    assert "C_A^{\\mathrm{kernel}}=C_A^{\\mathrm{direct}}" in text
    assert "descriptive differences that preserve the declared target-relevant continuation structure" in text
    assert "noisy Bayesian" in text


def test_v3_supplement_and_atlas_cover_all_five_roles():
    supplement = _text(SUPPLEMENT)
    atlas = _text(ATLAS)

    for phrase in (
        "Exact finite adaptive gain",
        "Target-relevant natural-history reduction",
        "Exactly balanced binary cues do not bound adaptive gain",
        "Hard-budget evolutionary selection",
        "Nonlinear structural no-go theorem",
        "Ecological recurrence as spectral filtering",
        "Feedback-existence diagnostic",
    ):
        assert phrase in supplement

    for phrase in (
        "Foundation: exact adaptive gain",
        "Target-relevant reduction and exact kernels",
        "Sharp finite extremal geometry",
        "Evolutionary lifts",
        "Temporal filtering and dynamical interpretation",
    ):
        assert phrase in atlas


def test_v3_preserves_v2_surfaces_as_fallback():
    assert (ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V2.md").exists()
    assert (ROOT / "manuscript" / "SUPPLEMENT_EVOLUTION_LETTERS_V1.md").exists()
    assert (ROOT / "manuscript" / "EVOLUTION_LETTERS_READINESS_V1.json").exists()
