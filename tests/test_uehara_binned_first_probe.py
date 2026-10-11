import csv
from pathlib import Path

from scripts.analyze_uehara_binned_first_probe import analyze


SPECIES = (
    "Aedes aegypti",
    "Aedes albopictus",
    "Anopheles gambiae",
    "Anopheles stephensi",
    "Culex tarsalis",
    "Culex quinquefasciatus",
)


def _write_fixture(tmp_path: Path):
    fig = tmp_path / "fig.csv"
    excl = tmp_path / "excl.csv"

    rows = []
    for species in SPECIES:
        rows.append(["", "", species])
        rows.append(["", "", "Flight"] + [""] * 8 + ["Probe"])
        header = [""] * 20
        header[11:20] = [
            "-1–0", "0–1", "1–2", "2–3", "3–4",
            "4–5", "5–6", "6–7", "7–8",
        ]
        rows.append(header)

        # Clean onset in first minute.
        row = [""] * 20
        row[11:20] = ["0", "1", "0", "0", "0", "0", "0", "0", "0"]
        rows.append(row)

        # Clean onset in third post-stimulus minute.
        row = [""] * 20
        row[11:20] = ["0", "0", "0", "2", "0", "0", "0", "0", "0"]
        rows.append(row)

        # Right-censored.
        row = [""] * 20
        row[11:20] = ["0"] * 9
        rows.append(row)

        # Excluded because pre-stimulus probing was positive.
        row = [""] * 20
        row[11:20] = ["3", "1", "0", "0", "0", "0", "0", "0", "0"]
        rows.append(row)

    with fig.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(rows)

    exclusion_rows = [["", "Species", "Timepoint", "loaded", "inactive"]]
    for species in SPECIES:
        exclusion_rows.append(["", species, "0", "4", "4"])
    with excl.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(exclusion_rows)

    return fig, excl


def test_binned_first_probe_parser_and_censoring(tmp_path):
    fig, excl = _write_fixture(tmp_path)
    result, intervals = analyze(fig, excl)

    assert len(intervals) == 24
    for species in SPECIES:
        summary = result["species"][species]
        assert summary["n_all_source_individuals"] == 4
        assert summary["n_primary_pre_probe_zero"] == 3
        assert summary["n_excluded_pre_probe_positive"] == 1
        assert summary["n_probe_by_8min"] == 2
        assert summary["n_right_censored_at_8min"] == 1
        assert summary["probe_by_1min_probability"] == 1 / 3
        assert summary["probe_by_8min_probability"] == 2 / 3
        assert summary["discrete_cdf_by_minute_end"]["1"] == 1 / 3
        assert summary["discrete_cdf_by_minute_end"]["3"] == 2 / 3
        assert summary["median_interval_end_min"] == 3


def test_row_count_validation_uses_exclusion_table(tmp_path):
    fig, excl = _write_fixture(tmp_path)
    result, _ = analyze(fig, excl)
    assert all(
        row["match"]
        for row in result["row_count_validation"].values()
    )
