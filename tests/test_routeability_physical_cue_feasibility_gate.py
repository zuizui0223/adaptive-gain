import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = (
    ROOT
    / "validation"
    / "routeability_physical_cue_feasibility_gate_v1.json"
)


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_context_is_persistent_not_pure_delayed_priming():
    data = _gate()
    route = data["physical_roles"]["q_route"]
    assert "remains visible" in route["implementation"]
    assert any(
        "disappears before the terminal cue" in item
        for item in route["forbidden"]
    )


def test_fixed_and_contingent_arms_match_timing_semantics():
    data = _gate()["access_timing"]
    assert "keep q_route visible" in data["contingent_B2"]
    assert "keep the first terminal cue visible" in data["fixed_B2"]
    assert "state-independent counterbalanced order" in data["fixed_B2"][2]
    assert "simultaneous-versus-sequential" in data["principle"]


def test_material_pretest_is_architecture_neutral_and_80_percent():
    data = _gate()["architecture_neutral_material_pretest"]
    assert "pre-randomization" in data["cohort"]
    assert "80% correct" in data["admission_criterion_each_cue"]
    assert "<= 0.10" in data["salience_balance_rule"]
    assert "do not exclude randomized confirmatory individuals" in data[
        "failure_policy"
    ]


def test_physical_environment_is_matched_across_architectures():
    data = _gate()["physical_matching"]
    assert data["same_cue_vectors_between_architectures"] is True
    assert data["same_context_symbols_between_architectures"] is True
    assert data["same_terminal_symbols_between_architectures"] is True
    assert data["same_spatial_layout_between_architectures"] is True
    assert "target/reward mapping" in data[
        "only_allowed_architecture_difference"
    ]


def test_gate_does_not_pretend_local_materials_or_ethics_are_done():
    data = _gate()
    assert "exact bumblebee species and colony source" in data[
        "human_material_inputs_still_required"
    ]
    ceiling = data["claim_ceiling"].lower()
    assert "does not establish" in ceiling
    assert "final n" in ceiling
    assert "ethics" in ceiling
