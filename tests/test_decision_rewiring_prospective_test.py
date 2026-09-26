from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "manuscript" / "DECISION_REWIRING_PROSPECTIVE_TEST_V1.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_prospective_rewiring_test_has_primary_contrast():
    text = _text()
    for phrase in (
        "Among ecological-network changes with similar species turnover and similar opportunity to rewire",
        "decision-equivalence boundary",
        "Confirmatory prediction P1",
        "greater rewiring among shared species",
        "low taxonomic turnover",
    ):
        assert phrase in text


def test_prospective_rewiring_test_separates_filters():
    text = _text()
    for phrase in (
        "availability / compatibility",
        "decision structure",
        "behaviorally accessible set",
        "observed interaction network",
        "must therefore be defined independently of the observed rewiring response",
    ):
        assert phrase in text


def test_prospective_rewiring_test_has_threshold_prediction():
    text = _text()
    for phrase in (
        "Confirmatory prediction P3",
        "loss of a **non-final representative**",
        "loss of the **final representative**",
        "larger discontinuity",
        "same one-species richness decrement",
    ):
        assert phrase in text


def test_prospective_rewiring_test_has_same_species_regime():
    text = _text()
    for phrase in (
        "Confirmatory prediction P4",
        "same species",
        "low taxonomic turnover",
        "cue reliability",
    ):
        assert phrase in text


def test_prospective_rewiring_test_blocks_circularity():
    text = _text()
    for phrase in (
        "Not acceptable for the confirmatory test",
        "clustering partners by their observed network links",
        "choosing class boundaries to maximize association with rewiring",
        "redefining equivalence after seeing the transition outcome",
    ):
        assert phrase in text


def test_prospective_rewiring_test_has_null_models_and_falsification():
    text = _text()
    for phrase in (
        "taxonomic-only",
        "functional-trait-only",
        "environment-only",
        "class-label null",
        "Falsification criteria",
        "shuffled class labels perform as well as or better",
    ):
        assert phrase in text


def test_prospective_rewiring_test_keeps_claim_firewall():
    text = _text().lower()
    for phrase in (
        "do not say decision-structural turnover is a third additive component",
        "do not say routeability determines observed rewiring",
        "do not infer decision-equivalence classes from the same rewiring response",
        "do not call the final-representative prediction ecosystem resilience",
        "do not treat a positive",
        "do not promote the reserve into v5 merely because the prediction is interesting",
    ):
        assert phrase in text


def test_frozen_v5_surface_remains_present():
    assert (ROOT / "manuscript" / "MANUSCRIPT_EVOLUTION_LETTERS_V5_ROUTEABILITY.md").exists()
    readiness = (
        ROOT / "manuscript" / "EVOLUTION_LETTERS_V5_ROUTEABILITY_READINESS_V1.json"
    ).read_text(encoding="utf-8")
    assert "v5_machine_submission_bundle_frozen_human_metadata_pending" in readiness
