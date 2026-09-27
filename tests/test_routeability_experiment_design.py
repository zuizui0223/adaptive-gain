from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "manuscript" / "ROUTEABILITY_EXPERIMENT_DESIGN_V1.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_experiment_design_freezes_exact_two_by_two_contrast():
    text = _text()
    for phrase in (
        "Primary 2 × 2 manipulation",
        "routeable",
        "matched bypass control",
        "contingent",
        "fixed",
        "1.00 | 0.75",
        "1.00 | 1.00",
        "25 percentage-point value is an information ceiling contrast",
    ):
        assert phrase in text


def test_experiment_design_targets_budget_window():
    text = _text()
    for phrase in (
        "B = 1 — below adaptive cost",
        "B = 2 — routeability-sensitive window",
        "B = 3 — above fixed cost",
        "`2 <= 2 < 3`",
        "budget-window interaction",
    ):
        assert phrase in text


def test_experiment_design_uses_individual_not_trial_as_unit():
    text = _text()
    assert "independent biological unit is the individual forager" in text
    assert "Trials are repeated observations, not independent animals." in text
    assert "Do not report trial count as the biological sample size." in text


def test_experiment_design_keeps_claim_ceiling():
    text = _text()
    for phrase in (
        "Do not require the observed interaction to equal 0.25.",
        "A failed behavioral experiment does not falsify the exact finite theorem.",
        "would not by itself establish that routeability explains natural plant-pollinator network rewiring",
    ):
        assert phrase in text
