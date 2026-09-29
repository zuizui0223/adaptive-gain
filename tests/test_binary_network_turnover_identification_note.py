import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "binary_network_turnover_identification_note_v1.json"
NOTE = ROOT / "manuscript" / "BINARY_NETWORK_TURNOVER_IDENTIFICATION_NOTE_V1.md"


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def _note():
    return NOTE.read_text(encoding="utf-8")


def test_methods_note_does_not_modify_v5_or_claim_generic_detection_novelty():
    data = _gate()
    assert data["v5_submission_surface_modified"] is False
    assert data["generic_imperfect_detection_novelty_claimed"] is False
    assert "Methods-note reserve only" in data["claim_ceiling"]


def test_methods_note_freezes_exact_turnover_identities():
    data = _gate()
    identities = " ".join(data["core_exact_results"])
    assert "#gain-#loss" in identities
    assert "P(0->1)-P(1->0)" in identities
    assert "q_current-q_previous" in identities
    assert "opposite latent prevalence changes" in identities


def test_methods_note_preserves_villavicencio_detection_boundary():
    data = _gate()
    role = data["villavicencio_role"]
    assert "state-side opportunity support 1/6" in role
    assert "detection-side support 4/6" in role
    assert "beta-binomial preference 6/6" in role
    assert "AUC 0.852" in role


def test_methods_note_contains_fail_closed_identification_ladder():
    text = _note()
    for phrase in (
        "Level 0 — aggregated binary networks only",
        "Level 1 — effort inventory / rarefaction",
        "Level 2 — effort-standardized interaction incidence",
        "Level 3 — repeated-detection latent-state model",
        "Level 4 — independent state or experimental manipulation",
        "Do not add increasingly flexible Villavicencio observation models",
    ):
        assert phrase in text


def test_methods_note_explicitly_positions_against_existing_literature():
    text = _note()
    for doi in (
        "10.1016/j.fooweb.2017.05.002",
        "10.1111/1365-2656.12459",
        "10.1111/2041-210X.14366",
        "10.1007/s00442-025-05771-8",
        "10.1111/j.1365-2664.2005.01098.x",
    ):
        assert doi in text
    assert "No claim is made that imperfect detection or sampling-sensitive rewiring is new." in text
