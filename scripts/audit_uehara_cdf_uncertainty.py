"""Audit sampling uncertainty of the Uehara 2026 frozen first-probe receipt.

Usage:
    python scripts/audit_uehara_cdf_uncertainty.py
    python scripts/audit_uehara_cdf_uncertainty.py --output validation/uehara_cdf_uncertainty_v1.json

Uses binned per-individual event counts rather than frame-resolved latency.
Fisher tests are exploratory and assume independent individuals; neither
batch effects nor selection into the pre-probe-zero cohort are resolved.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from adaptive_gain.empirical_cdf_uncertainty import compare_cdfs


def cumulative_at(species: dict, minute: int) -> tuple[int, int]:
    n = int(species["n_primary"])
    counts = species["first_probe_interval_counts"]
    assert len(counts) == 8
    assert sum(counts) + species["right_censored_8min"] == n
    return sum(counts[:minute]), n


def analyze(receipt: dict) -> dict:
    species = receipt["species"]

    def contrast(first: str, second: str, minute: int) -> dict:
        k1, n1 = cumulative_at(species[first], minute)
        k2, n2 = cumulative_at(species[second], minute)
        result = asdict(compare_cdfs(k1, n1, k2, n2))
        result.update({"first_species": first, "second_species": second, "minute_end": minute})
        return result

    return {
        "status": "EXPLORATORY_SAMPLING_UNCERTAINTY_AUDIT",
        "source": "validation/uehara_binned_first_probe_v1.json",
        "endpoint": receipt["endpoint"],
        "comparisons": {
            "anopheles_1min": contrast("Anopheles gambiae", "Anopheles stephensi", 1),
            "anopheles_4min": contrast("Anopheles gambiae", "Anopheles stephensi", 4),
            "large_early_tail_1min": contrast("Anopheles gambiae", "Aedes albopictus", 1),
            "aedes_1min": contrast("Aedes aegypti", "Aedes albopictus", 1),
        },
        "interpretation": {
            "sample_crossing": "The two Anopheles empirical CDFs cross in the sample.",
            "population_crossing": "Not established: both Anopheles endpoint contrasts are only 2-3 percentage points and Fisher p=1.",
            "early_tail_difference": "An. gambiae vs Ae. albopictus differs strongly in the first-minute observed proportion.",
            "cautions": [
                "Fisher exact comparisons are post-hoc exploratory, not pre-registered.",
                "Individuals are treated as independent; experimental batch effects not modeled.",
                "Primary cohort excludes positive pre-stimulus probing and may be nonrepresentative.",
                "One-minute interval censoring and right-censoring are not frame-resolved latency.",
                "Species contrasts do not compare adaptive versus fixed sensing architectures.",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("validation/uehara_binned_first_probe_v1.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = json.loads(args.input.read_text(encoding="utf-8"))
    result = json.dumps(analyze(receipt), indent=2, ensure_ascii=False) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
