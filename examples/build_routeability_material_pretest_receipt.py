"""Build a hash-addressed routeability material-pretest receipt."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from adaptive_gain.routeability_material_pretest import (
    qualify_material_pretest,
    sha256_path,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("trial_log_csv", type=Path)
    parser.add_argument("material_spec_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    with args.trial_log_csv.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        rows = list(csv.DictReader(handle))

    material_spec = json.loads(
        args.material_spec_json.read_text(encoding="utf-8")
    )

    receipt = qualify_material_pretest(
        rows,
        material_spec=material_spec,
        trial_log_sha256=sha256_path(args.trial_log_csv),
        material_spec_sha256=sha256_path(args.material_spec_json),
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
