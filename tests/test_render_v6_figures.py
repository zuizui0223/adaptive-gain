"""Source-backed publication figure generation and XML integrity tests.

No image model, no network data or external plotting library is needed.
All 3 SVGs use numeric theorem utilities or frozen empirical receipts.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from scripts.render_v6_figures import render


def test_v6_three_figure_svg_generation_is_deterministic_and_parseable(tmp_path):
    output = render(tmp_path)
    assert output["status"] == "V6_SVG_FIGURES_GENERATED_FROM_FROZEN_RECEIPTS"
    assert len(output["figures"]) == 3
    observed = {}
    for figure, item in output["figures"].items():
        f = tmp_path / item["filename"]
        raw = f.read_bytes()
        assert len(raw) > 2500, (figure,len(raw))
        assert hashlib.sha256(raw).hexdigest() == item["sha256"]
        root = ET.fromstring(raw)
        assert root.tag.endswith("svg")
        titles = [t.text for t in root.findall("{http://www.w3.org/2000/svg}title")]
        assert len(titles) == 1
        text = raw.decode("utf-8")
        assert "NOT" in text or "not" in text
        observed[figure] = text
    assert "Ratio-optimal depth" in observed["figure_1"]
    assert "Optimal depth shifts: 4 → 3 → 2" in observed["figure_1"]
    assert "Minimum robust arity b=3" in observed["figure_2"]
    assert "Cue arity is NOT receptor number" in observed["figure_2"]
    assert "Finite n=10,m=9: threshold p1 ≈ 0.6166" in observed["figure_3"]
    assert "Aggregate effect; NOT individual latency" in observed["figure_3"]

    manifest=json.loads((tmp_path/"svg_manifest.json").read_text(encoding="utf-8"))
    assert manifest["figures"] == output["figures"]
    tables=json.loads((tmp_path/"data"/"manifest.json").read_text(encoding="utf-8"))
    assert tables["figure_2"]["minimum_robust_arity"] == 3
    assert tables["figure_3"]["finite_one_step_threshold_n10_m9_K060_mu03"] > .6166

    second = render(tmp_path)
    assert second == output
    assert second["figures"] == manifest["figures"]


def test_v6_figure_staging_requires_no_external_raw_mosquito_files(tmp_path):
    manifest=render(tmp_path)
    data_dir=tmp_path/"data"
    expected={
        "fig1_frontier.csv",
        "fig1_urgency_ranking.csv",
        "fig2_arity_ceiling.csv",
        "fig3_expected_rescue.csv",
        "fig3_uehara_cdf.csv",
        "fig3_chandel_timing.json",
        "manifest.json",
    }
    assert expected.issubset({p.name for p in data_dir.iterdir()})
    figure3=(tmp_path/manifest["figures"]["figure_3"]["filename"]).read_text()
    for name in ("Ae. aegypti","Ae. albopictus","An. gambiae"):
        assert name in figure3
    assert "46.2 s" in figure3
    assert "46.5 s" in figure3



def test_v6_figure3_uses_interval_step_cdf_and_source_signed_auc_points(tmp_path):
    """No linear interpolation implying unknown within-minute event times."""
    manifest=render(tmp_path)
    path=tmp_path/manifest["figures"]["figure_3"]["filename"]
    xml=ET.parse(path).getroot()
    svg_source=path.read_text(encoding="utf-8")
    assert "Fraction of signed effect" in svg_source
    assert "Seconds since CO2 pulse end" in svg_source
    assert "Pulse 1: 50% at 46.2 s" in svg_source
    assert "Pulse 2: 50% at 46.5 s" in svg_source
    assert "censored 3/28" in svg_source
    assert "censored 15/38" in svg_source
    assert "censored 2/14" in svg_source

    paths=[
        el.attrib.get("d","")
        for el in xml.findall("{http://www.w3.org/2000/svg}path")
    ]
    # The C1 discrete first-probe curves start at x=95 (0 min) and
    # consist of 1 initial point plus two points per 1-minute bin.
    cdf_paths=[]
    for d in paths:
        points=[part.strip() for part in d.replace("M ","").split(" L ")]
        coords=[tuple(map(float,pt.split())) for pt in points]
        if len(coords)==17 and abs(coords[0][0]-95)<.01:
            cdf_paths.append(coords)
    assert len(cdf_paths)==3
    for coords in cdf_paths:
        assert abs(coords[0][1]-588)<1e-6
        for i in range(1,17,2):
            # Step curve holds the previous CDF to the interval end,
            # then jumps at the minute-end x; no invented fractional time.
            assert coords[i][0]==pytest.approx(coords[i+1][0])
            assert coords[i][1]==pytest.approx(coords[i-1][1])
    # Aggregate signed advantage curves carry seven plotted points:
    # 0, 10, 30, 45, 60, 75, 90 seconds.
    aggregate=[
        d for d in paths
        if len(d.replace("M ","").split(" L "))==7
        and d.startswith("M 832.00 ")
    ]
    assert len(aggregate)==2
