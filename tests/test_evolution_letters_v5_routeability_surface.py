from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V5_ROUTEABILITY.md"
SUPP = ROOT / "manuscript" / "SUPPLEMENT_EVOLUTION_LETTERS_V5_ROUTEABILITY.md"
FIGPLAN = ROOT / "manuscript" / "FIGURE_PLAN_EVOLUTION_LETTERS_V5_ROUTEABILITY.md"
LEGENDS = ROOT / "manuscript" / "FIGURE_LEGENDS_EVOLUTION_LETTERS_V5_ROUTEABILITY.md"
FIGURES = {
    ROOT / "manuscript" / "figures" / "figure_el1_routeability_v5.svg": (
        "Same ecological diversity can have different effective complexity",
        "Routeable community",
        "Non-routeable community",
        "Diversity is not complexity.",
    ),
    ROOT / "manuscript" / "figures" / "figure_el2_equivalence_niche_v5.svg": (
        "Raw richness and interaction-relevant richness can diverge",
        "same decision class",
        "new branch",
        "Routeable resource environment",
    ),
    ROOT / "manuscript" / "figures" / "figure_el3_accessible_network_v5.svg": (
        "Same compatibility-permitted network",
        "Different behaviorally accessible subnetworks",
        "Decision-relevant recurrence",
        "Decision-equivalent recurrence",
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


def test_v5_letter_length_surface():
    text = _text(MAIN)
    title = text.splitlines()[0].lstrip("# ")
    teaser = _section(text, "## Teaser text", "## Abstract")
    abstract = _section(text, "## Abstract", "**Keywords:**")
    main = _section(text, "## Introduction", "## Data and code availability")

    assert _words(title) <= 30
    assert _words(teaser) <= 150
    assert _words(abstract) <= 300
    assert _words(main) <= 5000


def test_v5_opens_with_environmental_problem():
    text = _text(MAIN)
    intro = _section(text, "## Introduction", "## Methods")
    assert "Environmental heterogeneity is one of ecology's most general explanations" in intro
    assert "equal amounts of heterogeneity need not pose equal ecological problems" in intro
    assert "environmental routeability" in intro.lower()
    assert "When does ecological diversity translate into decision-relevant complexity" in intro
    assert "heterogeneity can be routeable or non-routeable" in intro


def test_v5_main_promotes_ecological_conclusions():
    text = _text(MAIN)
    required = (
        "Ecological diversity and effective complexity can be decoupled",
        "Species richness need not increase decision complexity",
        "Routeability changes the information cost of broad niche use",
        "Routeability filters otherwise permitted interactions",
        "Ecological constraints expose the cost of non-routeable heterogeneity",
        "Temporal heterogeneity matters when it changes decision-relevant structure",
        "Biodiversity need not imply information burden",
        "Routeability adds an information filter to adaptive-foraging ecology",
    )
    for phrase in required:
        assert phrase in text


def test_v5_main_does_not_center_measurement_program():
    text = _text(MAIN)
    assert "## Empirical tests" not in text
    assert "A first experiment can" not in text
    assert "A second manipulation can" not in text
    assert "monitor individual decisions" not in text


def test_v5_main_keeps_claim_boundaries():
    text = _text(MAIN)
    lower = text.lower()
    assert "routeability is not an intrinsic scalar property" in lower
    assert "this does not imply that routeability alone causes generalism" in lower
    assert "not a claim that sensing alone determines food-web structure" in lower
    assert "compatibility-permitted network" in lower
    assert "otherwise permitted" in lower
    assert "not empirical demonstrations" in lower
    assert "not a separate theorem" in lower
    assert "environmental variability alone" not in lower


def test_v5_main_demotes_proof_internal_mathematics():
    text = _text(MAIN)
    forbidden = (
        "h_2^*",
        "h_b^*",
        "h_{2,\\mathrm{thr}}",
        "h_{b,\\mathrm{thr}}",
        "(7,6,6)",
        "(8,5,5)",
        "Bellman recursion",
        "certificate machinery",
    )
    for phrase in forbidden:
        assert phrase not in text


def test_v5_supplement_starts_with_ecological_structure():
    text = _text(SUPP)
    assert "Environmental routeability" in text
    assert "Raw heterogeneity versus decision-relevant heterogeneity" in text
    assert "Decision-equivalence classes" in text
    assert "Ecological consequences" in text
    assert "Compatibility-permitted versus behaviorally accessible interactions" in text
    assert "Natural-history mappings and empirical use" in text


def test_v5_supplement_demotes_measurement_to_optional_application():
    text = _text(SUPP)
    s1 = _section(text, "## S1.", "## S2.")
    assert "empirical workflow" not in s1.lower()
    assert "Optional empirical reconstruction" in text
    assert "not a premise required for the theoretical conclusions" in text


def test_v5_supplement_retains_exact_support():
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


def test_v5_figure_plan_is_environment_and_community_centered():
    text = _text(FIGPLAN)
    assert "Can equally diverse environments differ in effective complexity?" in text
    assert "Can biodiversity increase without increasing decision complexity?" in text
    assert "Can information structure filter realized community interactions and temporal effects?" in text
    assert "Diversity is not complexity." in text
    assert "compatibility-permitted network" in text
    assert "behaviorally accessible" in text


def test_v5_preserves_frozen_v4():
    assert (ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V4_ECOLOGY.md").exists()
    assert (ROOT / "manuscript" / "EVOLUTION_LETTERS_V4_ECOLOGY_READINESS_V1.json").exists()
    readiness = _text(ROOT / "manuscript" / "EVOLUTION_LETTERS_V4_ECOLOGY_READINESS_V1.json")
    assert "v4_machine_submission_bundle_frozen_human_metadata_pending" in readiness


def test_v5_figures_are_environment_and_community_centered():
    import xml.etree.ElementTree as ET

    for path, required in FIGURES.items():
        assert path.exists(), path
        ET.parse(path)
        text = _text(path)
        assert 'width="1600"' in text
        assert 'height="900"' in text
        for phrase in required:
            assert phrase in text, (path.name, phrase)


def test_v5_figures_do_not_restore_individual_theorem_catalogue():
    text = "\n".join(_text(path) for path in FIGURES)
    forbidden = (
        "Bellman",
        "Pareto",
        "certificate",
        "h_2",
        "h_b",
        "(7,6,6)",
        "(8,5,5)",
        "sharp maximum",
        "guaranteed oscillation",
    )
    for phrase in forbidden:
        assert phrase not in text


def test_v5_legends_keep_ecological_claim_boundaries():
    text = _text(LEGENDS)
    assert text.count("**Alt text:**") == 3
    assert "not a universal scalar property of a community" in text
    assert "does not imply routeability alone causes generalism" in text
    assert "Behaviorally accessible interactions are not automatically realized interactions" in text
    assert "compatibility-permitted" in text
    assert "not autocorrelation alone" in text
    assert "rather than fitted empirical demonstrations" in text


def test_v5_does_not_collapse_network_filters():
    text = _text(MAIN).lower()
    assert "forbidden links" in text
    assert "after those compatibility constraints" in text
    assert "routeability acts only on this last transition" in text
    assert "routeability determines realized connectance" not in text


def test_v5_keeps_environment_as_subject():
    text = _text(MAIN)
    assert "The central ecological conclusion is that heterogeneity and effective complexity are different properties." in text
    assert "diversity is not complexity" in text.lower()
    assert "routeable resource environment" not in text  # figure wording only; main remains conceptual
    assert "## Empirical tests" not in text
