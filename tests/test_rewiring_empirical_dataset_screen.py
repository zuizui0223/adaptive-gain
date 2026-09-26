from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "manuscript" / "REWIRING_EMPIRICAL_DATASET_SCREEN_V1.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_dataset_screen_has_admission_tiers():
    text = _text()
    for phrase in (
        "Tier A — confirmatory-ready",
        "Tier B — strong pilot",
        "Tier C — response-only / aggregate",
        "No Tier A public dataset has yet been identified.",
    ):
        assert phrase in text


def test_villavicencio_is_strongest_pilot_not_confirmation():
    text = _text()
    for phrase in (
        "Tier B — strongest current public pilot candidate.",
        "yearly plant–pollinator matrices for six consecutive years",
        "proboscis length/width",
        "morphology and phenology describe compatibility and accessibility constraints",
        "Do **not** call a morphology clustering result an exact empirical decision-equivalence test.",
    ):
        assert phrase in text


def test_dataset_screen_keeps_independent_exposure_rule():
    text = _text()
    for phrase in (
        "define decision-equivalence structure independently of the observed rewiring response",
        "defining decision-equivalence classes directly from the same network links would be circular",
        "decision classes can only be obtained by inspecting the same link outcomes to be predicted",
        "Do not label a trait cluster as “decision equivalence” merely because it improves prediction.",
    ):
        assert phrase in text


def test_screen_has_two_stage_program():
    text = _text()
    for phrase in (
        "Stage 1 — feasibility reanalysis on Villavicencio",
        "Stage-1 success does not validate routeability.",
        "Stage 2 — independent decision-structure layer",
        "freeze decision classes before joining them to the network response",
    ):
        assert phrase in text


def test_screen_has_experimental_fallback_and_stop_rules():
    text = _text()
    for phrase in (
        "Preferred experimental fallback",
        "manipulate whether an early cue partitions alternatives into informative branches",
        "non-final versus final representative",
        "Stop rules",
        "Until then, the public-data work is feasibility analysis, not empirical confirmation",
    ):
        assert phrase in text


def test_screen_prioritizes_subseason_response_without_overclaiming():
    text = _text()
    for phrase in (
        "Villavicencio 18-subseason response surface",
        "10.5061/dryad.j6q573n9j",
        "12 within-year adjacent transitions",
        "Year-end to next-year early transitions should be sensitivity analyses",
        "verified crosswalk",
        "detection-sensitive fallback rather than true species turnover",
    ):
        assert phrase in text
