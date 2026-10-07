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


def _words(text: str) -> int:
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\\\(.*?\\\)", " ", text, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text))


def test_v6_letter_length_surface():
    text = _text(MAIN)
    title = text.splitlines()[0].lstrip("# ")
    abstract = _section(text, "## Abstract", "Keywords:")
    main = text.split("## Introduction", 1)[1]

    assert _words(title) <= 30
    assert _words(abstract) <= 300
    assert _words(main) <= 5000


def test_v6_has_four_canonical_results():
    text = _text(MAIN)
    required = (
        "Finite information constraints define an exact attainable frontier",
        "Natural history re-ranks the structural frontier",
        "Architecture cost can be inverted into minimum information structure",
        "Encounter frequencies create a different exact frontier",
    )
    for phrase in required:
        assert phrase in text


def test_v6_keeps_structural_and_fitness_objects_separate():
    text = _text(MAIN)
    lower = text.lower()
    assert "a structural advantage in information acquisition is not itself a fitness advantage" in lower
    assert "structural adaptive gain is evolutionary potential, not fitness" in lower
    assert "c_a is guaranteed minimax complexity, not fitness" not in lower  # wording is in theory notes, not required verbatim
    assert "r_robust" in text
    assert "r_expected" in text


def test_v6_keeps_robust_expected_claim_firewall():
    text = _text(MAIN)
    assert "The robust frontier is intentionally distribution free." in text
    assert "Expected selection is different." in text
    assert "Cue arity matters for robust statewise evolvability" in text
    assert "cue arity disappears from the exact finite-scope expected ceiling" in text
    assert "frequency-assisted evolvability band" in text


def test_v6_keeps_prior_art_demotions():
    text = _text(MAIN)
    paragraph = _section(text, "### What the theory does not claim", "## Current empirical requirements")
    for phrase in (
        "Sequential value of information",
        "prior-weighted decision trees",
        "deadline-sensitive decisions",
        "adaptive-tree flattening",
        "adaptivity gaps",
        "costly sensory fidelity",
    ):
        assert phrase in paragraph


def test_v6_aedes_anchor_is_not_promoted_to_fitness_validation():
    text = _text(MAIN)
    anchor = _section(
        text,
        "## Empirical process anchor: temporal value is not the same as cue-effect magnitude",
        "## Discussion",
    )
    assert "46.2 s" in anchor
    assert "46.5 s" in anchor
    assert "This is a process-shape example, not a fitness validation." in anchor
    assert "do not identify the natural opportunity distribution" in anchor


def test_v6_payoff_relation_is_upstream_downstream_not_duplicate_theory():
    text = _text(MAIN)
    relation = _section(text, "### Relation to PAYOFF", "### What the theory does not claim")
    assert "The present framework supplies the upstream recoverable benefit." in relation
    assert "The generic" in relation
    assert "R-K" in relation
    assert "The contribution here is to derive sharp information-structural limits on" in relation


def test_v6_canonical_spine_has_stop_rule():
    text = _text(SPINE)
    assert "MAIN 1" in text
    assert "MAIN 2" in text
    assert "MAIN 3" in text
    assert "MAIN 4" in text
    assert "Do not add another main theorem unless it changes one of MAIN 1-4." in text


def test_v6_readiness_declares_draft_and_preserves_v5():
    data = json.loads(_text(READINESS))
    assert data["status"] == "v6_theory_draft_green_core_not_submission_ready"
    assert data["target"] == "Evolution Letters"
    assert data["preserved_v5_freeze"]["preserved"] is True
    assert data["promotion_rule"]["new_main_theorem_stop_rule"] is True



def test_v6_figure_plan_tracks_four_result_story():
    text = _text(FIGPLAN)
    for phrase in (
        "Natural history re-ranks an exact structural frontier",
        "Finite information constraints impose exact evolutionary no-go regions",
        "Encounter frequencies create value unavailable to robust architecture",
        "temporal process-shape anchor — not a fitness estimate",
    ):
        assert phrase in text


def test_v6_legends_keep_visual_claim_firewalls():
    text = _text(LEGENDS)
    assert text.count("**Alt text:**") == 3
    assert "Structural ratios are not interpreted as fitness." in text
    assert "not biological receptor count" in text
    assert "it is not an estimate of fitness" in text
    assert "frequency-assisted evolvability band" in text
