"""Build frozen numerical/source-data tables for the V6 three-figure story.

The script intentionally separates figure *data* from plotting aesthetics.
It uses only repository theorem functions and committed validation receipts, so
all numbers used in the V6 manuscript can be regenerated without manual
transcription.

Outputs:
- fig1_frontier.csv
- fig1_urgency_ranking.csv
- fig2_arity_ceiling.csv
- fig3_expected_rescue.csv
- fig3_uehara_cdf.csv
- fig3_chandel_timing.json
- manifest.json
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from adaptive_gain.bounded_arity_extremal_bounds import (
    bounded_arity_fixed_cost_bound,
)
from adaptive_gain.evolutionary_resource_frontier import (
    exponential_arity_limited_cost_ceiling,
    exponential_minimum_robust_cue_arity,
    exponential_unrestricted_expected_cost_ceiling,
    exponential_unrestricted_information_cost_ceiling,
    finite_scope_expected_value_ceiling,
    finite_scope_one_step_mass_threshold,
)


ROOT = Path(__file__).resolve().parents[1]


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build(outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)

    # Figure 1A/B: exact binary n=10,m=9 frontier.
    frontier = []
    for h in range(1, min(10 - 1, 9) + 1):
        cf = bounded_arity_fixed_cost_bound(10, 9, h, 2)
        frontier.append(
            {
                "adaptive_depth_h": h,
                "sharp_fixed_cost_Ih": cf,
                "additive_gap": cf - h,
                "fixed_to_adaptive_ratio": cf / h,
            }
        )
    _write_csv(outdir / "fig1_frontier.csv", frontier)

    # Figure 1C: natural-history reranking.
    urgency_rows = []
    mus = [round(x / 1000.0, 3) for x in range(10, 1201, 10)]
    for mu in mus:
        values = {}
        for h in range(1, min(9, 9) + 1):
            cf = bounded_arity_fixed_cost_bound(10, 9, h, 2)
            values[h] = math.exp(-mu * h) - math.exp(-mu * cf)
        best = max(values.values())
        for h, value in values.items():
            urgency_rows.append(
                {
                    "mu": mu,
                    "adaptive_depth_h": h,
                    "robust_value": value,
                    "is_optimum": int(
                        math.isclose(value, best, rel_tol=0.0, abs_tol=1e-12)
                    ),
                }
            )
    _write_csv(outdir / "fig1_urgency_ranking.csv", urgency_rows)

    # Figure 2: scalable robust arity ceiling at mu=.3.
    arity_rows = []
    for b in range(2, 11):
        ceiling, depths = exponential_arity_limited_cost_ceiling(
            b,
            closure_rate=0.3,
            resolution_value=1.0,
        )
        arity_rows.append(
            {
                "max_query_arity_b": b,
                "robust_cost_ceiling": ceiling,
                "maximizing_depths": ";".join(str(x) for x in depths),
                "K_example": 0.30,
                "K_is_robustly_repayable": int(0.30 < ceiling),
            }
        )
    _write_csv(outdir / "fig2_arity_ceiling.csv", arity_rows)

    b_min = exponential_minimum_robust_cue_arity(
        0.30,
        closure_rate=0.3,
        resolution_value=1.0,
    )

    # Figure 3A/B: robust/expected ceilings and finite p1 rescue.
    mu = 0.3
    robust_global = exponential_unrestricted_information_cost_ceiling(
        closure_rate=mu,
        resolution_value=1.0,
    )
    expected_global = exponential_unrestricted_expected_cost_ceiling(
        closure_rate=mu,
        resolution_value=1.0,
    )
    finite_expected = finite_scope_expected_value_ceiling(
        10,
        9,
        lambda t: math.exp(-mu * t),
    )
    finite_threshold = finite_scope_one_step_mass_threshold(
        10,
        9,
        0.60,
        lambda t: math.exp(-mu * t),
    )
    p_rows = []
    u1 = math.exp(-mu)
    u2 = math.exp(-2 * mu)
    u9 = math.exp(-9 * mu)
    for i in range(101):
        p = i / 100.0
        # Exact finite-scope conditional supremum at fixed p1.
        advantage = p * u1 + (1.0 - p) * u2 - u9
        p_rows.append(
            {
                "one_step_mass_p1": p,
                "finite_scope_expected_advantage_supremum": advantage,
                "K_example": 0.60,
                "above_K": int(advantage > 0.60),
            }
        )
    _write_csv(outdir / "fig3_expected_rescue.csv", p_rows)

    # Figure 3C1: committed Uehara individual discrete CDFs.
    uehara_path = ROOT / "validation" / "uehara_binned_first_probe_v1.json"
    uehara = json.loads(uehara_path.read_text(encoding="utf-8"))
    cdf_rows = []
    for species, values in uehara["species"].items():
        # Support both the current receipt keys and the earlier explicit CDF form.
        counts = values.get("first_probe_interval_counts")
        n = values.get("n_primary") or values.get("n_primary_pre_probe_zero")
        if counts is not None and n is not None:
            cumulative = 0
            for minute, count in enumerate(counts, start=1):
                cumulative += count
                cdf_rows.append(
                    {
                        "species": species,
                        "minute_end": minute,
                        "cdf_first_probe": cumulative / n,
                        "n_primary": n,
                        "right_censored_8min": values.get(
                            "right_censored_8min",
                            values.get("n_right_censored_at_8min"),
                        ),
                    }
                )
        else:
            cdf = values["discrete_cdf_by_minute_end"]
            for minute in range(1, 9):
                cdf_rows.append(
                    {
                        "species": species,
                        "minute_end": minute,
                        "cdf_first_probe": float(cdf[str(minute)]),
                        "n_primary": n,
                        "right_censored_8min": values.get(
                            "n_right_censored_at_8min"
                        ),
                    }
                )
    _write_csv(outdir / "fig3_uehara_cdf.csv", cdf_rows)

    # Figure 3C2: committed Chandel timing receipt.
    chandel_path = ROOT / "validation" / "chandel_fig3a_value_kernel_v1.json"
    chandel = json.loads(chandel_path.read_text(encoding="utf-8"))
    chandel_summary = {
        "source_receipt": str(chandel_path.relative_to(ROOT)),
        "post_first_pulse": chandel["post_first_pulse"],
        "post_second_pulse": chandel["post_second_pulse"],
        "claim_ceiling": chandel["interpretation"]["claim_ceiling"],
    }
    (outdir / "fig3_chandel_timing.json").write_text(
        json.dumps(chandel_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    manifest = {
        "status": "V6_FIGURE_DATA_FROZEN_FROM_THEOREM_AND_VALIDATION_RECEIPTS",
        "figure_1": {
            "frontier": "fig1_frontier.csv",
            "urgency_ranking": "fig1_urgency_ranking.csv",
            "canonical_switches_mu": [0.15469679775892664, 0.6562559792369758],
        },
        "figure_2": {
            "arity_ceiling": "fig2_arity_ceiling.csv",
            "canonical_K": 0.30,
            "minimum_robust_arity": b_min,
        },
        "figure_3": {
            "expected_rescue": "fig3_expected_rescue.csv",
            "uehara_individual_cdf": "fig3_uehara_cdf.csv",
            "chandel_timing": "fig3_chandel_timing.json",
            "robust_global_ceiling_mu03": robust_global,
            "expected_global_ceiling_mu03": expected_global,
            "finite_expected_ceiling_n10_m9_mu03": finite_expected,
            "finite_one_step_threshold_n10_m9_K060_mu03": finite_threshold,
        },
        "claim_firewall": (
            "Figure data reproduce theorem/receipt quantities only. Uehara and "
            "Chandel panels are temporal-process anchors, not adaptive/fixed "
            "fitness validation."
        ),
    }
    (outdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("v6_figure_data"),
    )
    args = parser.parse_args()
    print(json.dumps(build(args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
