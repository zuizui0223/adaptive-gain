import math

import pytest

from scripts.analyze_uehara_probe_latency import (
    extract_workbook,
    first_code_frame,
)


def test_first_code_frame_observed_and_absent():
    values = [0, 0, 1, 2, 2, 0]
    assert first_code_frame(
        values,
        code=2,
        start_frame=1,
        end_frame=6,
    ) == 3
    assert first_code_frame(
        values,
        code=2,
        start_frame=4,
        end_frame=6,
    ) == 4
    assert first_code_frame(
        values,
        code=2,
        start_frame=5,
        end_frame=6,
    ) is None


def test_extract_workbook_returns_individual_latencies(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    Workbook = openpyxl.Workbook

    path = tmp_path / "behaviors.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["mosquito_A", "mosquito_B"])
    rows = [
        (0, 0),
        (0, 0),
        (2, 0),
        (2, 0),
        (0, 0),
    ]
    for row in rows:
        ws.append(row)
    wb.save(path)

    result = extract_workbook(
        path,
        fps=1.0,
        start_frame=0,
        end_frame=5,
        probe_code=2,
    )

    assert len(result) == 2
    assert result[0]["animal"] == "mosquito_A"
    assert result[0]["latency_s"] == 2.0
    assert result[0]["status"] == "observed_probe"
    assert result[1]["animal"] == "mosquito_B"
    assert result[1]["latency_s"] == "inf"
    assert result[1]["status"] == "no_probe_in_window"
