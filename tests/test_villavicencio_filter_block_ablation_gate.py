import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "validation" / "villavicencio_filter_block_ablation_gate_v1.json"


def _gate():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_filter_block_ablation_freezes_four_ecological_blocks():
    data = _gate()
    assert data["status"] == "effect_blind_block_ablation_specification_frozen"
    assert data["blocks"] == {
        "phenology": ["phenological_overlap"],
        "abundance": ["flower_abundance"],
        "plant_morphology": [
            "corolla_length",
            "corolla_aperture",
            "height_mean",
        ],
        "pollinator_morphology": [
            "body_length",
            "proboscis_length",
            "proboscis_width",
            "body_width",
            "body_thickness",
        ],
    }


def test_filter_block_ablation_uses_same_temporal_holdout_design():
    data = _gate()
    analysis = data["analysis"]
    assert data["primary_scope"] == "strict_core_2008_2011"
    assert "leave-one-transition-out" in analysis["cross_validation"]
    assert analysis["primary_metric"].startswith("delta held-out log-loss")
    assert analysis["coefficient_inference"] is False
    assert analysis["statistical_significance_testing"] is False


def test_filter_block_ablation_freezes_strict_reproducibility_rule():
    data = _gate()
    rule = data["classification_rule"]
    assert "every primary held-out transition" in rule[
        "reproducible_incremental_information"
    ]
    assert "at least one primary held-out transition" in rule[
        "positive_but_fold_unstable"
    ]
    assert "does not worsen" in rule[
        "no_reproducible_incremental_information"
    ]


def test_filter_block_ablation_keeps_claim_firewall():
    data = _gate()
    forbidden = data["interpretation"]["forbidden"]
    assert "causal interpretation of a block" in forbidden
    assert "post-hoc regrouping of predictors" in forbidden
    assert "calling any block decision structure or routeability" in forbidden
    assert "cannot validate environmental routeability" in data["claim_ceiling"]
