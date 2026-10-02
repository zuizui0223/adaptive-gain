from adaptive_gain.bumblebee_public_bridge import spaethe_public_bridge_receipt


def test_spaethe_secondary_cue_recruitment_matches_registered_direction():
    receipt = spaethe_public_bridge_receipt()
    assert receipt.registered_direction_holds_for_pattern
    assert receipt.registered_direction_holds_for_shape
    assert receipt.registered_direction_holds_pooled

    rows = {(row.secondary_feature, row.difficulty): row for row in receipt.rows}
    assert rows[("pattern", "easy")].n == 20
    assert rows[("pattern", "hard")].n == 20
    assert rows[("shape", "easy")].n == 15
    assert rows[("shape", "hard")].n == 15

    assert abs(rows[("pattern", "easy")].mean_secondary_recruitment - 0.025) < 1e-12
    assert abs(rows[("pattern", "hard")].mean_secondary_recruitment - 0.38) < 1e-12
    assert abs(rows[("shape", "easy")].mean_secondary_recruitment - (2 / 75)) < 1e-12
    assert abs(rows[("shape", "hard")].mean_secondary_recruitment - (11 / 30)) < 1e-12
    assert abs(receipt.pooled_recruitment_difference - (61 / 175)) < 1e-12
    assert "not a direct estimate" in receipt.claim_ceiling
