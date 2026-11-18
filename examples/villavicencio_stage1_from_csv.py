"""Run the Stage-1 rewiring feasibility audit from standardized CSV inputs.

This script does not infer decision-equivalence classes. It only measures
shared-species link change, species-turnover-linked change, and opportunity
denominators for prespecified network transitions.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

from adaptive_gain.empirical_rewiring import (
    networks_by_period_from_rows,
    rewiring_estimability_audit,
    transition_dyad_rows,
    transition_rewiring_receipt,
)


def _read_interactions(path: Path):
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"period", "plant", "pollinator", "weight"}
        if not required <= set(reader.fieldnames or ()):
            raise ValueError(f"interaction CSV must contain {sorted(required)}")
        for row in reader:
            rows.append(
                (
                    row["period"],
                    row["plant"],
                    row["pollinator"],
                    float(row["weight"]),
                )
            )
    return networks_by_period_from_rows(rows)


def _read_transition_pairs(path: Path):
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"previous_period", "current_period", "role"}
        if not required <= set(reader.fieldnames or ()):
            raise ValueError(f"transition CSV must contain {sorted(required)}")
        for row in reader:
            role = row["role"].strip().lower()
            if role not in {"primary", "sensitivity"}:
                raise ValueError("transition role must be primary or sensitivity")
            rows.append(
                (
                    row["previous_period"],
                    row["current_period"],
                    role,
                )
            )
    if not rows:
        raise ValueError("transition CSV contains no transitions")
    if len({(a, b) for a, b, _ in rows}) != len(rows):
        raise ValueError("transition CSV contains duplicate period pairs")
    return rows


def _read_presence(path: Path | None, *, allow_unverified: bool):
    if path is None:
        return None

    by_period = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"period", "guild", "species", "basis"}
        if not required <= set(reader.fieldnames or ()):
            raise ValueError(f"presence CSV must contain {sorted(required)}")
        for row in reader:
            basis = row["basis"].strip().lower()
            verified = basis.startswith("independent_") or basis.startswith("verified_")
            if not verified and not allow_unverified:
                raise ValueError(
                    "presence basis is not independently verified; "
                    "use --allow-unverified-presence only for detection-sensitive QC"
                )
            guild = row["guild"].strip().lower()
            if guild not in {"plant", "pollinator"}:
                raise ValueError("presence guild must be plant or pollinator")
            bucket = by_period.setdefault(
                row["period"],
                {"plant": set(), "pollinator": set(), "bases": set()},
            )
            bucket[guild].add(row["species"])
            bucket["bases"].add(row["basis"])

    return by_period


def _read_permitted(path: Path | None):
    if path is None:
        return None
    permitted = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"plant", "pollinator", "allowed"}
        if not required <= set(reader.fieldnames or ()):
            raise ValueError(f"permitted CSV must contain {sorted(required)}")
        for row in reader:
            allowed = row["allowed"].strip().lower()
            if allowed in {"1", "true", "yes", "y"}:
                permitted.add((row["plant"], row["pollinator"]))
            elif allowed not in {"0", "false", "no", "n"}:
                raise ValueError(f"unrecognized allowed value: {row['allowed']!r}")
    return permitted


def _receipt_dict(receipt):
    out = asdict(receipt)
    out.update(
        {
            "shared_species_rewiring_count": receipt.shared_species_rewiring_count,
            "species_turnover_link_count": receipt.species_turnover_link_count,
            "exact_partition": receipt.exact_partition,
            "link_jaccard_dissimilarity": receipt.link_jaccard_dissimilarity,
            "shared_species_rewiring_fraction_of_union": (
                receipt.shared_species_rewiring_fraction_of_union
            ),
            "species_turnover_fraction_of_union": (
                receipt.species_turnover_fraction_of_union
            ),
            "rewiring_opportunity_rate": receipt.rewiring_opportunity_rate,
        }
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("interactions", type=Path)
    parser.add_argument("transitions", type=Path)
    parser.add_argument("--presence", type=Path)
    parser.add_argument("--permitted", type=Path)
    parser.add_argument("--allow-unverified-presence", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dyad-output", type=Path)
    args = parser.parse_args()

    networks = _read_interactions(args.interactions)
    transitions = _read_transition_pairs(args.transitions)
    presence = _read_presence(
        args.presence,
        allow_unverified=args.allow_unverified_presence,
    )
    permitted = _read_permitted(args.permitted)

    output_rows = []
    dyad_output_rows = []
    primary_dyad_rows = {}
    for previous_period, current_period, role in transitions:
        if previous_period not in networks or current_period not in networks:
            raise ValueError(
                f"transition refers to absent network: "
                f"{previous_period!r}->{current_period!r}"
            )

        kwargs = {}
        presence_bases = []
        if presence is not None:
            if previous_period not in presence or current_period not in presence:
                raise ValueError(
                    "presence file does not cover every prespecified transition period"
                )
            prev = presence[previous_period]
            curr = presence[current_period]
            kwargs = {
                "previous_plants": prev["plant"],
                "previous_pollinators": prev["pollinator"],
                "current_plants": curr["plant"],
                "current_pollinators": curr["pollinator"],
            }
            presence_bases = sorted(prev["bases"] | curr["bases"])

        receipt = transition_rewiring_receipt(
            networks[previous_period],
            networks[current_period],
            permitted_dyads=permitted,
            **kwargs,
        )
        output_rows.append(
            {
                "previous_period": previous_period,
                "current_period": current_period,
                "role": role,
                "presence_bases": presence_bases,
                "receipt": _receipt_dict(receipt),
            }
        )

        transition_rows = transition_dyad_rows(
            networks[previous_period],
            networks[current_period],
            permitted_dyads=permitted,
            **kwargs,
        )
        if role == "primary":
            primary_dyad_rows[f"{previous_period}->{current_period}"] = transition_rows

        if args.dyad_output is not None:
            for dyad in transition_rows:
                dyad_output_rows.append(
                    {
                        "previous_period": previous_period,
                        "current_period": current_period,
                        "role": role,
                        **asdict(dyad),
                    }
                )

    primary = [row for row in output_rows if row["role"] == "primary"]
    estimability = rewiring_estimability_audit(primary_dyad_rows)
    estimability_dict = asdict(estimability)
    estimability_dict.update(
        {
            "changed_fraction": estimability.changed_fraction,
            "global_outcome_nondegenerate": estimability.global_outcome_nondegenerate,
            "has_within_transition_contrast": estimability.has_within_transition_contrast,
        }
    )
    result = {
        "schema": "adaptive-gain-villavicencio-stage1-rewiring-v1",
        "interactions_file": str(args.interactions),
        "transitions_file": str(args.transitions),
        "presence_file": None if args.presence is None else str(args.presence),
        "permitted_file": None if args.permitted is None else str(args.permitted),
        "decision_equivalence_inferred": False,
        "primary_transition_count": len(primary),
        "primary_external_presence_count": sum(
            row["receipt"]["presence_basis"] == "externally_supplied_presence"
            for row in primary
        ),
        "primary_nonzero_shared_opportunity_count": sum(
            row["receipt"]["shared_species_dyad_count"] > 0 for row in primary
        ),
        "primary_estimable_permitted_rate_count": sum(
            row["receipt"]["rewiring_opportunity_rate"] is not None for row in primary
        ),
        "primary_estimability": estimability_dict,
        "transitions": output_rows,
    }

    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output is None:
        print(rendered)
    else:
        args.output.write_text(rendered + "\n", encoding="utf-8")

    if args.dyad_output is not None:
        fields = [
            "previous_period",
            "current_period",
            "role",
            "plant",
            "pollinator",
            "previous_weight",
            "current_weight",
            "previous_link",
            "current_link",
            "changed",
            "direction",
            "permitted",
        ]
        with args.dyad_output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(dyad_output_rows)


if __name__ == "__main__":
    main()
