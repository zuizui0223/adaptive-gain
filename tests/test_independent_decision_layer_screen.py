from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "manuscript" / "INDEPENDENT_DECISION_LAYER_SCREEN_V1.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_screen_admits_kent_as_independent_cognition_not_exact_routeability():
    text = _text()
    for phrase in (
        "A-cognition source — strongest current independent decision-layer candidate, but not confirmatory-ready.",
        "It is **not A-exact**",
        "independent colour-learning experiment",
        "not the full ecological cue hierarchy",
        "pseudoreplication",
    ):
        assert phrase in text


def test_screen_preserves_kent_novelty_boundary():
    text = _text()
    assert "merely regresses specialization on learning score is **not novel**" in text
    assert "restricted colour-channel structure" in text
    assert "do not use network specialization to define the decision exposure" in text


def test_screen_triangulates_network_cognition_and_experiment():
    text = _text()
    for phrase in (
        "System N — repeated network response",
        "System C — independent cognition plus network",
        "System X — controlled decision-cost experiment",
        "Villavicencio",
        "Kent Island",
        "Austin et al. floral marketplace",
    ):
        assert phrase in text


def test_screen_keeps_exact_claim_firewall():
    text = _text()
    for phrase in (
        "do not call perceptual colour classes exact decision-equivalence classes",
        "do not claim that colour learning alone determines realized interactions",
        "restricted-channel or cognition-layer tests rather than exact routeability confirmation",
        "NO-GO for a standalone confirmatory routeability claim",
    ):
        assert phrase in text
