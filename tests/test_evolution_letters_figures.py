from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / "manuscript" / "figures"
LEGENDS = ROOT / "manuscript" / "FIGURE_LEGENDS_EVOLUTION_LETTERS_V1.md"

FIGURES = {
    "figure_el1_no_go.svg": (
        "Finite sensing architecture creates a dynamical no-go region",
        "UNREACHABLE",
        "not guaranteed",
    ),
    "figure_el2_architecture.svg": (
        "Required dynamics imply finite natural-history architecture",
        "(n*, m*, E*) = (6, 5, 5)",
        "Neither point dominates the other",
    ),
    "figure_el3_recurrence.svg": (
        "Ecology filters structurally generated selection through time",
        "same slow mode",
        "Persistence alone is insufficient",
    ),
}


def test_all_evolution_letters_svg_files_are_well_formed_and_claim_safe():
    for name, required in FIGURES.items():
        path = FIGDIR / name
        assert path.exists(), name
        ET.parse(path)
        text = path.read_text(encoding="utf-8")
        assert 'width="1600"' in text
        assert 'height="900"' in text
        for phrase in required:
            assert phrase in text


def test_no_go_figure_does_not_turn_necessary_condition_into_sufficiency():
    text = (FIGDIR / "figure_el1_no_go.svg").read_text(encoding="utf-8").lower()
    assert "not ruled out" in text
    assert "not guaranteed" in text
    assert "unreachable" in text
    assert "guaranteed oscillation" not in text


def test_figure_legends_preserve_scope_boundaries():
    text = LEGENDS.read_text(encoding="utf-8")
    assert "does not guarantee oscillation" in text
    assert "cannot reach a regime requiring gap at least two" in text
    assert "ecological persistence alone does not determine" in text
