from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / "manuscript" / "figures"
LEGENDS = ROOT / "manuscript" / "FIGURE_LEGENDS_EVOLUTION_LETTERS_V2.md"

FIGURES = {
    "figure_el1_no_go_v2.svg": (
        "Finite sensing architecture creates a dynamical no-go region",
        "gᵢ = C",
        "Δg = g₂ − g₁",
        "not guaranteed",
    ),
    "figure_el2_architecture_v2.svg": (
        "Required feedback contrast forces a finite state-specific architecture",
        "(n*, m*, E*) = (6, 5, 5)",
        "0 ≤ gᵢ ≤ 1",
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


def test_v2_figures_separate_state_gap_from_between_state_contrast():
    fig1 = (FIGDIR / "figure_el1_no_go_v2.svg").read_text(encoding="utf-8")
    fig2 = (FIGDIR / "figure_el2_architecture_v2.svg").read_text(encoding="utf-8")
    assert "state-specific structural gap" in fig1
    assert "between-state contrast" in fig1
    assert "Δg = g₂ − g₁" in fig1
    assert "some gᵢ ≥ q" in fig2
    assert "|Δg| ≤ 1" in fig2
    assert "Δg = C" not in fig1


def test_no_go_figure_does_not_turn_necessary_condition_into_sufficiency():
    text = (FIGDIR / "figure_el1_no_go_v2.svg").read_text(encoding="utf-8").lower()
    assert "not ruled out" in text
    assert "not guaranteed" in text
    assert "unreachable" in text
    assert "guaranteed oscillation" not in text


def test_figure_legends_preserve_scope_boundaries():
    text = LEGENDS.read_text(encoding="utf-8")
    assert "g_i=C_F(i)-C_A(i)" in text
    assert "Delta g=g_2-g_1" in text
    assert "does not guarantee oscillation" in text
    assert "cannot meet a requirement of two" in text
    assert "ecological persistence alone does not determine" in text
