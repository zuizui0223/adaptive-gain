import csv
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "build_villavicencio_transition_pairs.py"

spec = importlib.util.spec_from_file_location("villavicencio_transition_builder", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_verified_six_by_three_map_builds_12_primary_and_5_sensitivity():
    rows = []
    for year in range(2006, 2012):
        for subseason in ("early", "mid", "late"):
            rows.append((f"{year}_{subseason}", year, subseason))

    transitions = module.build_transition_rows(rows)

    primary = [row for row in transitions if row[2] == "primary"]
    sensitivity = [row for row in transitions if row[2] == "sensitivity"]
    assert len(primary) == 12
    assert len(sensitivity) == 5
    assert primary[0] == ("2006_early", "2006_mid", "primary")
    assert primary[1] == ("2006_mid", "2006_late", "primary")
    assert sensitivity[0] == ("2006_late", "2007_early", "sensitivity")


def test_period_map_requires_explicit_verification(tmp_path):
    path = tmp_path / "period_map.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["period", "year", "subseason", "verified"])
        writer.writerow(["p1", 2006, "early", "false"])

    with pytest.raises(ValueError, match="not explicitly verified"):
        module.read_period_map(path)


def test_period_map_rejects_missing_or_duplicate_cells():
    rows = []
    for year in range(2006, 2012):
        for subseason in ("early", "mid", "late"):
            rows.append((f"{year}_{subseason}", year, subseason))

    with pytest.raises(ValueError, match="exactly 18"):
        module.build_transition_rows(rows[:-1])

    duplicate = rows[:-1] + [("duplicate", 2006, "early")]
    with pytest.raises(ValueError, match="duplicate year/subseason"):
        module.build_transition_rows(duplicate)
