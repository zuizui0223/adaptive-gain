import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE = (
    ROOT
    / "validation"
    / "routeability_final_n_threshold_rule_v1.json"
)


def _rule():
    return json.loads(RULE.read_text(encoding="utf-8"))


def test_final_n_threshold_rule_is_frozen_before_power_surface():
    data = _rule()
    assert data["status"] == "frozen_before_pilot_and_final_power_surface"
    assert data["minimum_fit_success_fraction"] == 0.95
    assert data["minimum_h1_directional_rejection_fraction"] == 0.80
    assert data["minimum_h2_hierarchical_pass_fraction"] == 0.80


def test_final_n_threshold_rule_keeps_counterbalance_and_mc_precision():
    data = _rule()
    assert data["counterbalance_multiple"] == 4
    assert data["minimum_scenarios_per_n"] == 12
    assert data["minimum_simulations_per_scenario"] >= 1000


def test_final_n_threshold_rule_uses_worst_scenario_selection():
    data = _rule()
    assert "every frozen robustness scenario" in data["selection"]
    assert any("cannot be changed" in item for item in data["firewalls"])
    assert any("cannot be averaged away" in item for item in data["firewalls"])
