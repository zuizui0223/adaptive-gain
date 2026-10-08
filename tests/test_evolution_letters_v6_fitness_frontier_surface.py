from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V6_FITNESS_FRONTIER.md"
SPINE = ROOT / "theory" / "CANONICAL_FITNESS_THEOREM_SPINE_V1.md"
READINESS = ROOT / "manuscript" / "EVOLUTION_LETTERS_V6_FITNESS_FRONTIER_READINESS_V1.json"
FIGPLAN = ROOT / "manuscript" / "FIGURE_PLAN_EVOLUTION_LETTERS_V6_FITNESS_FRONTIER.md"
LEGENDS = ROOT / "manuscript" / "FIGURE_LEGENDS_EVOLUTION_LETTERS_V6_FITNESS_FRONTIER.md"


def _text(path: Path) -> str:
    assert path.exists(), path
    return path.read_text(encoding="utf-8")


def _section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def _flat(text: str) -> str:
    return " ".join(text.split())


def _words(text: str) -> int:
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\\\(.*?\\\)", " ", text, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text))


def test_v6_letter_length_surface():
    text = _text(MAIN)
    title = text.splitlines()[0].lstrip("# ")
    abstract = _section(text, "## Abstract", "Keywords:")
    main = text.split("## Introduction", 1)[1].split("## References", 1)[0]

    assert _words(title) <= 30
    assert _words(abstract) <= 300
    assert _words(main) <= 5000


def test_v6_has_three_novelty_results_and_one_supporting_frequency_section():
    text = _text(MAIN)
    for phrase in (
        "Finite information constraints define an exact attainable frontier",
        "Natural history re-ranks the structural frontier",
        "Architecture cost can be inverted into minimum information structure",
        "Biological consequence: encounter frequencies can rescue expected value",
    ):
        assert phrase in text

    spine = _text(SPINE)
    assert "## MAIN 1" in spine
    assert "## MAIN 2" in spine
    assert "## MAIN 3" in spine
    assert "## SUPPORT 1" in spine
    assert "## MAIN 4" not in spine


def test_v6_keeps_structural_and_fitness_objects_separate():
    text = _flat(_text(MAIN))
    lower = text.lower()
    assert "a structural advantage in information acquisition is not itself a fitness advantage" in lower
    assert "structural adaptive gain is evolutionary potential, not fitness" in lower
    assert "robust value of contingent over fixed resolution" in lower
    assert "expected value" in lower


def test_v6_expected_frequency_result_is_not_promoted_as_independent_novelty():
    text = _flat(_text(MAIN))
    assert "interpretive extension rather than a separate novelty theorem" in text
    assert "prior-weighted expected decision-tree cost itself is established theory" in text

    readiness = json.loads(_text(READINESS))
    assert len(readiness["main_results"]) == 3
    assert any(
        "frequency" in item.lower()
        for item in readiness["supporting_biological_consequences"]
    )


def test_v6_prior_art_firewalls_include_flattening_and_test_collection():
    text = _text(MAIN)
    paragraph = _section(text, "### What the theory does not claim", "## Current empirical requirements")
    flat = _flat(paragraph).lower()

    for phrase in (
        "sequential value of information",
        "worst-versus-expected decision trees",
        "deadline-sensitive action utility",
        "adaptive-versus-nonadaptive expected-value gaps",
        "minimum/generalized test-collection problems",
    ):
        assert phrase in flat

    assert "fixed resolver is closely related to a test collection" in flat
    assert "exact joint frontier" in flat


def test_v6_empirical_anchors_are_individual_and_aggregate_but_not_fitness():
    text = _text(MAIN)
    anchor = _section(
        text,
        "## Empirical process anchors: temporal effect shape and individual completion profiles",
        "## Discussion",
    )

    assert "46.2 s" in anchor
    assert "46.5 s" in anchor
    assert "10 of 38 individuals (26.3%)" in anchor
    assert "12/14 *Anopheles" in anchor
    assert "sample CDFs also cross" in anchor
    assert "population-level ordering" in anchor
    assert "two-sided Fisher exact" in anchor
    assert "process anchors, not fitness validations" in anchor
    assert "one-minute interval-censored" in anchor


def test_v6_payoff_relation_is_upstream_downstream_not_duplicate_theory():
    text = _text(MAIN)
    relation = _section(text, "### Relation to PAYOFF", "### What the theory does not claim")
    flat = _flat(relation)
    assert "upstream recoverable benefit" in flat
    assert "R-K" in flat
    assert "generic" in flat
    assert "sharp information-structural limits" in flat


def test_v6_canonical_spine_has_three_main_result_stop_rule():
    text = _text(SPINE)
    assert "MAIN 1" in text
    assert "MAIN 2" in text
    assert "MAIN 3" in text
    assert "SUPPORT 1" in text
    assert "MAIN 4" not in text
    assert "MAIN 1-3 only" in text


def test_v6_readiness_declares_draft_three_result_spine_and_preserves_v5():
    data = json.loads(_text(READINESS))
    assert data["target"] == "Evolution Letters"
    assert "not_submission_ready" in data["status"]
    assert data["preserved_v5_freeze"]["preserved"] is True
    assert data["promotion_rule"]["new_main_theorem_stop_rule"] is True
    assert len(data["main_results"]) == 3
    assert "MAIN 1-3" in data["promotion_rule"]["rule"]


def test_v6_figure_plan_tracks_three_result_plus_empirical_story():
    text = _text(FIGPLAN)
    for phrase in (
        "Natural history re-ranks an exact structural frontier",
        "Finite information constraints impose exact evolutionary no-go regions",
        "Encounter frequencies create value unavailable to robust architecture",
        "Individual discrete completion profiles",
        "Aggregate temporal effect shape",
    ):
        assert phrase in text


def test_v6_legends_keep_visual_claim_firewalls_and_two_empirical_objects():
    text = _text(LEGENDS)
    assert text.count("**Alt text:**") == 3
    assert "Structural ratios are not interpreted as fitness." in text
    assert "not biological receptor count" in text
    assert "Uehara et al. (2026)" in text
    assert "Chandel et al. (2024)" in text
    assert "Neither estimates fitness" in text


def test_v6_manuscript_has_no_known_broken_tex_tokens_or_control_chars():
    text = _text(MAIN)
    forbidden = (
        "C_Ale",
        "hmapsto",
        "toinfty",
        "notRightarrow",
        ",qquad",
        ")quad(",
    )
    for token in forbidden:
        assert token not in text

    controls = [
        char
        for char in text
        if ord(char) < 32 and char not in "\n\r\t"
    ]
    assert controls == []


def test_v6_references_include_fixed_test_collection_and_both_mosquito_anchors():
    text = _text(MAIN)
    refs = _flat(text.split("## References", 1)[1])
    for phrase in (
        "The generalized test collection problem",
        "Thermal infrared directs host-seeking behaviour",
        "Behavioral heterogeneity in host seeking and post-feeding suppression",
    ):
        assert phrase in refs



def test_v6_display_math_never_contains_nested_inline_delimiters():
    """Catch an actual math-rendering bug in earlier manuscript versions.

    A LaTeX display block delimited by \[ and \] must not contain the
    Markdown inline math delimiters \( and \). Otherwise formulas like
    U\(C_A\) do not represent the function evaluation U(C_A).
    """
    source = _text(MAIN)
    assert source.count(r"\[") == source.count(r"\]") > 0
    parts = re.split(r"(\\\[|\\\])", source)
    active = False
    for part in parts:
        if part == r"\[":
            assert not active, "nested display math"
            active = True
        elif part == r"\]":
            assert active, "unmatched display math close"
            active = False
        elif active:
            assert r"\(" not in part, "inline opener inside display math"
            assert r"\)" not in part, "inline closer inside display math"
    assert not active
    assert r"R_{\rm expected}(\pi)" in source
    assert r"U(T_\pi(w))" in source
    assert "U[T_pi(w)]" not in source
    assert r"U(C_A)-U(C_F)" in source
    assert r"J_K(h)" in source



def test_v6_canonical_spine_has_complete_comparison_operators():
    """Protect mathematical *meaning* against lost LaTeX backslashes.

    A dropped backslash in \neq, \le or \sup can silently turn
    a theorem into malformed plain text while all numerical tests pass.
    """
    source = _text(SPINE)
    assert source.count(r"\neq") >= 2
    assert source.count(r"\le") >= 2
    assert r"\ge" in source
    assert r"\sup R_{\rm expected}" in source
    assert r"\sup R_{\rm robust}" in source
    assert r"\min\{m,F_b(n,h)\}" in source
    assert r"\min\{j\ge h:U(h)-U(j)>K\}" in source
    assert r"\min\{b\ge2:K<K_{\rm crit,robust}^{(b)}\}" in source
    assert r"h\mapsto(h,I_h)" in source
    assert not re.search(r"(?m)^\s*(?:eq|le K|sup R|hmapsto)\s*$", source)
    assert r"I_hge" not in source
    assert r"Kge0" not in source


def test_v6_references_are_not_accidentally_counted_inside_math_blocks():
    """A simple parity lint: inline math can appear in prose but not in display."""
    for path in (MAIN, SPINE):
        source = _text(path)
        parts = re.split(r"(\\\[|\\\])", source)
        state = False
        for part in parts:
            if part == r"\[":
                assert not state, f"nested display opener: {path}"
                state = True
            elif part == r"\]":
                assert state, f"unmatched display closer: {path}"
                state = False
            elif state:
                assert r"\(" not in part, f"nested inline opener: {path}"
                assert r"\)" not in part, f"nested inline closer: {path}"
        assert not state



def test_v6_theory_prior_art_explicitly_covers_query_set_tree_coupling():
    text = _text(MAIN)
    boundary = _section(text, "### What the theory does not claim",
                        "## Current empirical requirements")
    assert "Wieczorek et al. 2021" in boundary
    assert "sharp all-depth joint extremum" in boundary
    assert "The proposed MAIN contribution is restricted to three results" in boundary
    assert "not a fourth independent novelty claim" in boundary
    assert "Minimum query set for decision tree construction" in text
    assert "https://doi.org/10.3390/e23121682" in text
