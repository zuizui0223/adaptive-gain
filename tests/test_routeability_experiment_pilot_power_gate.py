import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "routeability_experiment_pilot_power_gate_v1.json"
EXPORTER = ROOT / "examples" / "plan_routeability_experiment.py"


def test_pilot_power_gate_blocks_focal_effect_leakage():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    assert data["status"] == "nuisance_input_contract_and_conservative_screening_calculator_frozen"
    forbidden = data["pilot"]["forbidden_inputs"]
    assert "observed H1 architecture-by-access interaction" in forbidden
    assert "observed H2 budget-localization contrast" in forbidden
    assert "the exact theoretical 0.25 information-ceiling interaction used as a behavioral effect size" in forbidden
    assert data["final_sample_size_gate"]["no_final_N_in_this_gate"] is True


def test_pilot_power_gate_requires_external_sesoi():
    data = json.loads(GATE.read_text(encoding="utf-8"))
    sesoi = data["sesoi"]
    assert sesoi["required"] is True
    assert "external_biological_criterion" in sesoi["allowed_provenance"]
    assert "theoretical_information_ceiling" in sesoi["forbidden_provenance"]
    assert sesoi["freeze_before_final_power_simulation"] is True


def test_power_screening_exporter_emits_nonfinal_receipt(tmp_path):
    input_path = tmp_path / "planning_input.json"
    output_path = tmp_path / "planning_receipt.json"
    input_path.write_text(
        json.dumps(
            {
                "pilot_nuisance": {
                    "trial_icc": 0.2,
                    "randomized_individual_dropout": 0.1,
                    "full_information_success": 0.9,
                    "timeout_fraction": 0.05,
                    "source": "architecture_neutral_procedural_pilot",
                    "focal_architecture_access_contrast_opened": False
                },
                "sesoi": {
                    "h1_probability_interaction": 0.15,
                    "h2_probability_localization": 0.15,
                    "provenance": "practical_decision_threshold"
                },
                "planning": {
                    "trials_per_individual": 12,
                    "alpha_two_sided": 0.05,
                    "target_power": 0.8,
                    "counterbalance_multiple": 4
                }
            }
        ),
        encoding="utf-8"
    )

    completed = subprocess.run(
        [sys.executable, str(EXPORTER), str(input_path), str(output_path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True
    )
    assert completed.returncode == 0, completed.stderr

    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["final_sample_size_frozen"] is False
    assert result["receipt"]["randomized_individuals_per_cell"] % 4 == 0
    assert result["receipt"]["factorial_cell_count"] == 12
    assert "final GLMM simulation" in result["next_gate"]
