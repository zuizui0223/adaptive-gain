import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "routeability_experiment_analysis_gate_v1.json"


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_routeability_analysis_gate_freezes_primary_and_localization_estimands():
    data = _gate()
    assert data["status"] == "prospective_confirmatory_estimands_frozen_before_data"
    assert data["estimands"]["H1"]["estimand"] == "Delta_B2"
    assert "Delta_B2 - 0.5*(Delta_B1 + Delta_B3)" in data["estimands"]["H2"]["estimand"]
    assert data["estimands"]["H1"]["confirmatory_role"] == "primary"


def test_routeability_analysis_gate_uses_hierarchical_multiplicity_control():
    data = _gate()
    mult = data["multiplicity"]
    assert mult["rule"] == "hierarchical gatekeeping"
    assert mult["order"] == ["H1", "H2"]
    assert mult["alpha"] == 0.05
    assert "H1 rejects" in mult["H2_confirmatory_only_if"]


def test_routeability_analysis_gate_keeps_biological_replication_correct():
    data = _gate()
    population = data["analysis_population"]
    assert population["independent_unit"] == "individual forager"
    assert population["repeated_unit"] == "trial"
    assert "counting trials as independent biological replicates" in population["forbidden"]


def test_routeability_analysis_gate_does_not_power_from_theory_ceiling():
    data = _gate()
    assert "do not power from the exact 0.25 information ceiling" in data["sample_size_boundary"]
    assert "does not establish natural-network rewiring" in data["claim_ceiling"]


def test_routeability_analysis_gate_blocks_treatment_dependent_training_exclusion():
    data = _gate()
    forbidden = data["analysis_population"]["forbidden"]
    assert (
        "excluding randomized individuals because architecture-specific training accuracy is low"
        in forbidden
    )
    firewall = data["training_selection_firewall"]
    assert "fixed-dose architecture-specific training" in firewall["preferred"]
    assert "per-protocol" in firewall["unavoidable_criterion_rule"]


def test_routeability_analysis_gate_keeps_timeout_trials_in_primary_denominator():
    data = _gate()
    assert "timeouts are both scored 0" in data["primary_endpoint"]
    timeout = data["timeout_policy"]
    assert timeout["primary_denominator"] == "all initiated test trials"
    assert timeout["timeout_score"] == 0
    assert "dropping timeout/abandonment trials" in timeout["forbidden"]
    assert "dropping timeout trials from the primary denominator" in data["reporting"]["forbidden"]
