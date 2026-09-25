from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "manuscript" / "ECOLOGICAL_NOVELTY_EXTENSION_V1.md"


def _text() -> str:
    assert EXT.exists()
    return EXT.read_text(encoding="utf-8")


def test_decision_novelty_extension_has_exact_basis():
    text = _text()
    assert "Compositional novelty is not necessarily decision novelty." in text
    assert "decision-equivalence class" in text
    assert "world-side quotient" in text
    assert "preserves the adaptive continuation value" in text
    assert "no new theorem family is required" in text


def test_decision_novelty_extension_reaches_ecological_domains():
    text = _text()
    for phrase in (
        "Species invasion",
        "Local extinction",
        "Community turnover",
        "Climate-driven community change",
        "functional redundancy",
    ):
        assert phrase in text


def test_decision_novelty_extension_keeps_claim_firewall():
    text = _text().lower()
    assert "do not claim that decision novelty predicts invasion success" in text
    assert "do not equate decision equivalence with functional redundancy" in text
    assert "do not claim every introduced species increases effective complexity" in text
    assert "do not call decision novelty a universal community metric" in text
    assert "no new theorem is introduced" in text


def test_frozen_v5_is_not_overwritten_by_extension():
    assert (ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V5_ROUTEABILITY.md").exists()
    readiness = (ROOT / "manuscript" / "EVOLUTION_LETTERS_V5_ROUTEABILITY_READINESS_V1.json").read_text(encoding="utf-8")
    assert "v5_machine_submission_bundle_frozen_human_metadata_pending" in readiness
