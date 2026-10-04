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
        root = ET.parse(ROOT / row["path"]).getroot()
        visible_text = " ".join("".join(root.itertext()).split())
        for phrase in row["required_labels"]:
            assert phrase in visible_text


def test_figure2_values_match_temporal_and_spaethe_receipts():
    temporal = json.loads((ROOT / "validation/temporal_routing_threshold_v1.json").read_text())
    panel = json.loads((ROOT / "validation/bombus_empirical_convergence_panel_v1.json").read_text())
    svg = (ROOT / "manuscript/figures/figure_routeability_decision_ecology_v2.svg").read_text()

    assert temporal["closed_form"]["temporal_adaptive_gain"] == "abs(2*rho-1)/4"
    assert "G_time = |2rho - 1| / 4" in svg
    assert "rho=0.5" in svg
    assert f'{panel["spaethe_2026"]["easy_mean"]:.3f}' in svg
    assert f'{panel["spaethe_2026"]["hard_mean"]:.3f}' in svg
    assert f'{panel["spaethe_2026"]["cliffs_delta"]["pooled"]:.3f}' in svg
    assert "Yuan et al." not in svg
    assert "Chow 2022" not in svg
