from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V4_ECOLOGY.md"
SUPP = ROOT / "manuscript" / "SUPPLEMENT_EVOLUTION_LETTERS_V3_ECOLOGY.md"
FRAMING = ROOT / "manuscript" / "ECOLOGICAL_FRAMING_V1.md"
FIGPLAN = ROOT / "manuscript" / "FIGURE_PLAN_EVOLUTION_LETTERS_V4_ECOLOGY.md"
LEGENDS = ROOT / "manuscript" / "FIGURE_LEGENDS_EVOLUTION_LETTERS_V4_ECOLOGY.md"
FIGURES = {
    ROOT / "manuscript" / "figures" / "figure_el1_ecological_deadline_v4.svg": (
        "branch-specific cue",
        "C_A",
        "C_F",
        "intermediate",
        "unique contingent advantage",
    ),
    ROOT / "manuscript" / "figures" / "figure_el2_conditional_cues_v4.svg": (
        "Same marginals, different structure",
        "Routed system",
        "Conditional cue dependence",
        "branch exclusivity",
    ),
    ROOT / "manuscript" / "figures" / "figure_el3_recurrence_alignment_v4.svg": (
        "Recurring states carry different sensing payoffs",
        "Same persistence, different alignment",
        "payoff-mode alignment",
        "autocorrelation should matter",
    ),
}


def _text(path: Path) -> str:
    assert path.exists(), path
    return path.read_text(encoding="utf-8")


def _section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def _words(text: str) -> int:
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\\\(.*?\\\)", " ", text, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text))


def test_v4_letter_length_surface():
    text = _text(MAIN)
    title = text.splitlines()[0].lstrip("# ")
    teaser = _section(text, "## Teaser text", "## Abstract")
    abstract = _section(text, "## Abstract", "**Keywords:**")
    main = _section(text, "## Introduction", "## Data and code availability")

    assert _words(title) <= 30
    assert _words(teaser) <= 150
    assert _words(abstract) <= 300
    assert _words(main) <= 5000


def test_v4_opens_with_ecological_problem_not_theorem_catalogue():
    text = _text(MAIN)
    intro = _section(text, "## Introduction", "## Methods")
    assert "unlimited time and complete information" in intro
    assert "Predator attacks" in text
    assert "speed–accuracy trade-offs" in intro
    assert "branch-specific cue requirements" in intro
    assert "When the organization of information acquisition becomes a target of selection" in intro


def test_v4_main_promotes_ecological_predictions():
    text = _text(MAIN)
    for phrase in (
        "intermediate ecological constraint",
        "Conditional cue dependence",
        "Environmental heterogeneity matters when it changes decision architecture",
        "Small state differences cannot generate arbitrarily strong feedback",
        "Environmental persistence amplifies only aligned sensing-generated selection",
        "Empirical tests",
    ):
        assert phrase in text


def test_v4_main_demotes_exact_extremal_machinery():
    text = _text(MAIN)
    assert "h_2^*" not in text
    assert "h_b^*" not in text
    assert "(7,6,6)" not in text
    assert "(8,5,5)" not in text
    assert "Bellman recursion" not in text
    assert "certificate machinery" not in text


def test_v4_keeps_core_claim_firewalls():
    text = _text(MAIN).lower()
    assert "crossing this threshold is not sufficient for oscillation" in text
    assert "not a claim that sensing architecture alone generates observed cycles" in text
    assert "illustrative" in text
    assert "environmental variability alone" not in text


def test_v4_supplement_starts_with_natural_history_and_empirical_workflow():
    text = _text(SUPP)
    assert "From natural history to a finite sensing problem" in text
    assert "Define one decision episode" in text
    assert "Record cue order, not only cue presence" in text
    assert "Empirical workflow" in text
    assert "Manipulate the ecological budget" in text
    assert "Illustrative natural-history mappings" in text


def test_v4_supplement_retains_exact_mathematical_support():
    text = _text(SUPP)
    for phrase in (
        "Exact finite adaptive gain",
        "Exact target-relevant reduction",
        "Finite structural requirements and branch exclusivity",
        "Hard-budget evolutionary selection",
        "Nonlinear structural no-go for feedback",
        "Ecological recurrence and reward-mode alignment",
    ):
        assert phrase in text


def test_v4_figure_plan_is_ecology_first():
    text = _text(FIGPLAN)
    assert "When does contingent sensing pay?" in text
    assert "What kind of natural-history structure creates the advantage?" in text
    assert "When does state-dependent sensing selection persist through time?" in text
    assert "Move the V3 sharp binary corner" in text
    assert "Do not display the full exact extremal construction in the main figure" in text


def test_v4_preserves_machine_frozen_v3():
    assert (ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V3.md").exists()
    assert (ROOT / "manuscript" / "SUPPLEMENT_EVOLUTION_LETTERS_V2.md").exists()
    assert (ROOT / "manuscript" / "EVOLUTION_LETTERS_V3_READINESS_V1.json").exists()


def test_v4_figure_files_are_ecology_first_and_well_formed():
    import xml.etree.ElementTree as ET

    for path, required in FIGURES.items():
        assert path.exists(), path
        ET.parse(path)
        text = _text(path)
        assert 'width="1600"' in text
        assert 'height="900"' in text
        for phrase in required:
            assert phrase in text, (path.name, phrase)


def test_v4_figures_do_not_reintroduce_theorem_catalogue():
    text = "\n".join(_text(path) for path in FIGURES)
    forbidden = (
        "h_2*",
        "h_b*",
        "(7,6,6)",
        "(8,5,5)",
        "Pareto",
        "sharp maximum",
        "certificate",
    )
    for phrase in forbidden:
        assert phrase not in text


def test_v4_legends_keep_ecological_claim_boundaries():
    text = _text(LEGENDS)
    assert text.count("**Alt text:**") == 3
    assert "counterfactual non-contingent benchmark" in text
    assert "positive selection additionally requires" in text
    assert "not a universal scalar measure of ecological complexity" in text
    assert "environmental autocorrelation alone is insufficient" in text
    assert "generic illustrations rather than fitted empirical examples" in text
