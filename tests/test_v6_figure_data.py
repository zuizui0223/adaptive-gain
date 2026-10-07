import csv
import json
import math

import pytest

from scripts.build_v6_figure_data import build


def _read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_v6_figure_data_reproduces_canonical_frontier_and_arity_threshold(tmp_path):
    manifest = build(tmp_path)

    frontier = _read_csv(tmp_path / "fig1_frontier.csv")
    rows = {int(row["adaptive_depth_h"]): row for row in frontier}
    assert int(rows[2]["sharp_fixed_cost_Ih"]) == 3
    assert int(rows[3]["sharp_fixed_cost_Ih"]) == 7
    assert int(rows[4]["sharp_fixed_cost_Ih"]) == 9

    arity = _read_csv(tmp_path / "fig2_arity_ceiling.csv")
    b2 = next(row for row in arity if int(row["max_query_arity_b"]) == 2)
    b3 = next(row for row in arity if int(row["max_query_arity_b"]) == 3)
    assert float(b2["robust_cost_ceiling"]) == pytest.approx(
        0.2900852153739598
    )
    assert float(b3["robust_cost_ceiling"]) == pytest.approx(
        0.38632774829479477
    )
    assert manifest["figure_2"]["minimum_robust_arity"] == 3


def test_v6_figure_data_expected_ceiling_and_threshold(tmp_path):
    manifest = build(tmp_path)
    fig3 = manifest["figure_3"]

    assert fig3["robust_global_ceiling_mu03"] == pytest.approx(math.exp(-0.6))
    assert fig3["expected_global_ceiling_mu03"] == pytest.approx(math.exp(-0.3))
    assert fig3["finite_expected_ceiling_n10_m9_mu03"] == pytest.approx(
        math.exp(-0.3) - math.exp(-2.7)
    )
    assert fig3["finite_one_step_threshold_n10_m9_K060_mu03"] == pytest.approx(
        0.6166136276001076
    )


def test_v6_figure_data_contains_uehara_crossing_profiles(tmp_path):
    build(tmp_path)
    rows = _read_csv(tmp_path / "fig3_uehara_cdf.csv")
    by = {
        (row["species"], int(row["minute_end"])): float(row["cdf_first_probe"])
        for row in rows
    }
    assert by[("Anopheles gambiae", 3)] > by[("Anopheles stephensi", 3)]
    assert by[("Anopheles stephensi", 4)] > by[("Anopheles gambiae", 4)]


def test_v6_figure_data_chandel_half_area_times_are_frozen(tmp_path):
    build(tmp_path)
    data = json.loads(
        (tmp_path / "fig3_chandel_timing.json").read_text(encoding="utf-8")
    )
    assert data["post_first_pulse"]["half_signed_advantage_time_s_after_pulse"] == pytest.approx(
        46.2
    )
    assert data["post_second_pulse"]["half_signed_advantage_time_s_after_pulse"] == pytest.approx(
        46.5
    )
