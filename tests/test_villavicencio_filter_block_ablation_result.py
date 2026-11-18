import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "validation" / "villavicencio_filter_block_ablation_result_v1.json"


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_filter_block_ablation_result_preserves_frozen_rule():
    data = _result()
    assert data["status"] == "green_phenology_reproducible_both_endpoints"
    assert data["frozen_rule"]["primary_scope"] == "strict_core_2008_2011"
    assert "every primary held-out transition" in data["frozen_rule"][
        "reproducible_incremental_information"
    ]


def test_filter_block_ablation_result_has_phenology_both_endpoints():
    data = _result()
    for risk in ("gain", "loss"):
        block = data["primary"][risk]["blocks"]["phenology"]
        assert block["classification"] == "reproducible_incremental_information"
        assert block["positive_folds"] == "3/3"
        assert block["delta_log_loss_drop_minus_full"] > 0


def test_filter_block_ablation_result_does_not_overclaim_morphology():
    data = _result()
    assert data["primary"]["gain"]["blocks"]["plant_morphology"][
        "classification"
    ] == "no_reproducible_incremental_information"
    assert data["primary"]["gain"]["blocks"]["pollinator_morphology"][
        "classification"
    ] == "no_reproducible_incremental_information"
    assert data["primary"]["loss"]["blocks"]["plant_morphology"][
        "classification"
    ] == "positive_but_fold_unstable"
    assert data["primary"]["loss"]["blocks"]["pollinator_morphology"][
        "classification"
    ] == "no_reproducible_incremental_information"


def test_filter_block_ablation_result_keeps_claim_ceiling():
    data = _result()
    assert "causal primacy of phenology" in data["not_established"]
    assert "decision-equivalence classes" in data["not_established"]
    assert "environmental routeability" in data["not_established"]
    assert "not a causal decomposition" in data["claim_ceiling"]
