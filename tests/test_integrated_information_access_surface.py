from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md"
V5 = ROOT / "manuscript/EVOLUTION_LETTERS_V5_ROUTEABILITY_READINESS_V1.json"
SECTION5 = ROOT / "validation/independent_section5_audit_v1.json"


def _text():
    return MANUSCRIPT.read_text()


def test_integrated_ecology_letters_structure_and_figures():
    text = _text()
    for heading in (
        "## 1. Introduction",
        "## 2. Material and methods",
        "## 3. Results",
        "## 4. Discussion",
    ):
        assert heading in text
    for old in ("## 5.", "## 6.", "## 7.", "## 8.", "## 9.", "## 10.", "## 11.", "## 12.", "## 13.", "## 14."):
        assert old not in text
    for figure_ref in ("Fig. 1", "Fig. 2a", "Fig. 2b", "Fig. 2c", "Fig. 2d"):
        assert figure_ref in text


def test_integrated_notation_and_claim_firewalls():
    text = _text()
    assert r"\(B_f=-\beta e>0\)" in text
    assert r"\(B_fLq_{\max}\le G_{\rm osc}\)" in text
    assert r"\(BLq_{\max}\le G_{\rm osc}\)" not in text
    assert "not a sufficiency" in text
    assert "does not guarantee oscillation" in text
    assert "it does not establish an unbounded separation for a fixed binary action" in text


def test_bombus_claim_ceiling_is_preserved():
    text = _text()
    assert "bioRxiv preprint" in text
    assert "Yuan et al. (2026)" in text
    assert "0.207" in text
    assert "unresolved raw-field anomaly" in text
    assert "not a test of the routeability theorem" in text


def test_classical_identification_prior_art_is_present():
    text = _text()
    for citation in (
        "Katona 1966",
        "Garey 1972",
        "Hyafil & Rivest 1976",
        "Chakaravarthy et al. 2009",
        "Moshkov & Zielosko 2011",
    ):
        assert citation in text


def test_independent_section5_receipt_and_v5_retirement():
    section5 = json.loads(SECTION5.read_text())
    assert section5["status"] == "INDEPENDENT_IMPLEMENTATION_MATCHES_SECTION5"
    assert section5["one_copy"]["complete_shannon_entropy_vector_match"]
    assert section5["one_copy"]["fixed_costs"] == {"A": 4, "B": 4}
    assert section5["one_copy"]["adaptive_costs"] == {"A": 4, "B": 3}
    assert section5["two_copy"]["fixed_costs"] == {"A": 8, "B": 8}
    assert section5["two_copy"]["adaptive_costs"] == {"A": 8, "B": 6}

    v5 = json.loads(V5.read_text())
    assert v5["status"] == "v5_machine_submission_bundle_frozen_human_metadata_pending"
    assert v5["portfolio_status"] == "RETIRED_DO_NOT_SUBMIT_STANDALONE"
    assert "DO NOT SUBMIT V5 AS A SEPARATE MANUSCRIPT" in v5["promotion_rule"]
