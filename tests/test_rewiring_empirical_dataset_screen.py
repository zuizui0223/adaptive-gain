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


def test_villavicencio_is_detection_testbed_not_routeability_pilot():
    text = _text()
    for phrase in (
        "Tier C — high-value response/detection test bed, not a routeability pilot.",
        "yearly plant–pollinator matrices for six consecutive years",
        "proboscis length/width",
        "raw records permit focal-response-excluded availability/activity opportunity",
        "state-transition support in only 1/6",
        "detection/activity component is supported in 4/6",
        "A trait- or network-derived class system can only be exploratory",
    ):
        assert phrase in text


def test_dataset_screen_keeps_independent_exposure_rule():
    text = _text()
    for phrase in (
        "define decision-equivalence structure independently of the observed rewiring response",
        "availability, activity and morphology still do not establish an independent cue hierarchy or decision-equivalence structure.",
        "Do not label a trait cluster as “decision equivalence” merely because it improves prediction.",
    ):
        assert phrase in text


def test_screen_has_observational_stop_then_direct_mechanism_program():
    text = _text()
    for phrase in (
        "Villavicencio observational result — stop here",
        "state-side support appears in only **1/6** transitions",
        "detection/activity-side support appears in **4/6**",
        "Villavicencio natural-network routeability bridge is **not promoted**",
        "Next empirical mechanism test",
        "decision classes must be frozen before joining them to the network response",
    ):
        assert phrase in text


def test_screen_has_experimental_fallback_and_stop_rules():
    text = _text()
    for phrase in (
        "Preferred direct experiment",
        "manipulate whether an early cue partitions alternatives into informative branches",
        "non-final versus final representative",
        "Stop rules",
        "Villavicencio itself is retained as a response/detection boundary case, not empirical confirmation of V5 routeability.",
    ):
        assert phrase in text


def test_screen_prioritizes_subseason_response_without_overclaiming():
    text = _text()
    for phrase in (
        "Villavicencio 18-subseason response surface",
        "10.5061/dryad.j6q573n9j",
        "12 within-year adjacent transitions",
        "Year-end to next-year early transitions should be sensitivity analyses",
        "4,581 shared-dyad rows and 853 changed links",
        "detection-sensitive rather than true species turnover",
        "seven links occur only in positive rows lacking a date",
    ):
        assert phrase in text
