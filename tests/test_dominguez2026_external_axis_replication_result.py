import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "dominguez2026_external_axis_replication_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_external_replication_is_explicitly_mixed():
    data = _result()
    assert data["status"] == (
        "external_replication_mixed_loss_axis_matches_gain_axis_does_not"
    )
    assert data["primary_plant_phenology_axis"]["gain"]["replication"] == "NO"
    assert (
        data["primary_plant_phenology_axis"]["loss"]["replication"]
        == "YES_DIRECTIONAL"
    )


def test_gain_direction_is_not_rewritten_as_replication():
    gain = _result()["primary_plant_phenology_axis"]["gain"]
    assert gain["frozen_pollinator_minus_plant_contrast"] < 0
    assert gain["sites_matching_frozen_direction"] == "2/12"
    assert gain["plant_availability_increment"] > gain["pollinator_activity_increment"]


def test_loss_direction_replication_is_cross_site():
    loss = _result()["primary_plant_phenology_axis"]["loss"]
    assert loss["frozen_plant_minus_pollinator_contrast"] > 0
    assert loss["sites_matching_frozen_direction"] == "10/12"
    assert loss["plant_availability_increment"] > loss["pollinator_activity_increment"]


def test_abundance_sensitivity_does_not_rescue_gain_but_preserves_loss():
    data = _result()["plant_abundance_sensitivity"]
    assert data["gain"]["frozen_pollinator_minus_plant_contrast"] <= 0
    assert data["loss"]["frozen_plant_minus_pollinator_contrast"] > 0


def test_external_claim_ceiling_blocks_latent_state_and_routeability_promotion():
    data = _result()
    ceiling = data["claim_ceiling"].lower()
    assert "recorded annual links" in ceiling
    assert "latent ecological state" in ceiling
    assert "causal" in ceiling
    assert "routeability" in ceiling
