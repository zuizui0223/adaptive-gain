import json
from pathlib import Path

from adaptive_gain.network_response_validity import (
    NetworkResponseEvidence,
    ResponseValidity,
    assess_network_response_validity,
)

ROOT = Path(__file__).resolve().parents[1]
VALIDITY = ROOT / "validation" / "dominguez2026_response_validity_v1.json"
RESULT = ROOT / "validation" / "dominguez2026_external_axis_replication_result_v1.json"


def _validity():
    return json.loads(VALIDITY.read_text(encoding="utf-8"))


def test_external_response_fails_closed_at_observed_link_turnover():
    data = _validity()
    evidence = NetworkResponseEvidence(**data["gate_evidence"])
    assessment = assess_network_response_validity(evidence)
    assert assessment.response_validity == ResponseValidity.OBSERVED_LINK_TURNOVER_ONLY
    assert assessment.routeability_bridge_eligible is False
    assert data["gate_result"]["response_validity"] == assessment.response_validity.value


def test_external_axis_result_is_not_latent_state_replication():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validity = data["response_validity"]
    assert validity["classification"] == "observed_link_turnover_only"
    assert validity["detection_defensible_state_replication"] is False
    ceiling = data["claim_ceiling"].lower()
    assert "recorded annual links" in ceiling
    assert "latent ecological state" in ceiling
    assert "routeability" in ceiling
