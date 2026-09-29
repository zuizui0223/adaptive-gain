import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESOI = ROOT / "validation" / "routeability_sesoi_gate_v1.json"


def _data():
    return json.loads(SESOI.read_text(encoding="utf-8"))


def test_sesoi_is_frozen_on_probability_scale():
    data = _data()
    assert data["status"] == "frozen_before_confirmatory_data"
    assert data["estimands"]["H1"]["sesoi_probability_points"] == 0.10
    assert data["estimands"]["H2"]["sesoi_probability_points"] == 0.10


def test_sesoi_uses_practical_not_theoretical_provenance():
    data = _data()
    assert data["provenance"]["type"] == "practical_decision_threshold"
    assert "0.25" in data["firewalls"]["theoretical_information_ceiling"]
    assert "forbidden" in data["firewalls"]["theoretical_information_ceiling"]


def test_sesoi_cannot_be_reestimated_from_pilot():
    data = _data()
    assert "may alter" in data["firewalls"]["pilot"]
    assert "cannot be changed" in data["firewalls"]["confirmatory"]


def test_power_interface_is_constant():
    data = _data()["power_interface"]
    assert data["h1_sesoi"] == 0.10
    assert data["h2_sesoi"] == 0.10
    assert data["sesoi_provenance"] == (
        "practical_decision_threshold_frozen_2026-09-29"
    )
