from pathlib import Path
import json
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def _receipt():
    return json.loads((ROOT / "validation/routeability_main_figures_v1.json").read_text())


def test_routeability_main_figures_are_well_formed_svg():
    receipt = _receipt()
    for row in receipt["figures"].values():
        path = ROOT / row["path"]
        assert path.exists()
        root = ET.parse(path).getroot()
        assert root.tag.endswith("svg")


def test_routeability_main_figures_keep_their_claim_labels():
    receipt = _receipt()
    for row in receipt["figures"].values():
        text = (ROOT / row["path"]).read_text()
        for phrase in row["required_labels"]:
            assert phrase in text


def test_figure2_values_match_frozen_bombus_receipts():
    panel = json.loads((ROOT / "validation/bombus_empirical_convergence_panel_v1.json").read_text())
    yuan = json.loads((ROOT / "validation/yuan_free_cue_acquisition_interaction_v1.json").read_text())
    svg = (ROOT / "manuscript/figures/figure_routeability_bombus_bridge_v1.svg").read_text()

    assert f'{panel["yuan_2026"]["regular"]["Easy"]["request_rate"]:.3f}' in svg
    assert f'{panel["yuan_2026"]["regular"]["Impossible"]["request_rate"]:.3f}' in svg
    assert f'{panel["spaethe_2026"]["easy_mean"]:.3f}' in svg
    assert f'{panel["spaethe_2026"]["hard_mean"]:.3f}' in svg
    assert f'{panel["spaethe_2026"]["cliffs_delta"]["pooled"]:.3f}' in svg
    did = yuan["within_bee_difference_in_differences"]["Impossible_vs_Easy"]["mean"]
    assert f'{did:.3f}' in svg
