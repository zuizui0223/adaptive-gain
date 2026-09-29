"""Build the effect-blind Dominguez-Garcia external axis-replication table.

The response is annual focal-dyad gain/loss among species present in two
adjacent years at the same site. Plant-side availability uses current-year
plant phenology (PhenologyP), measured at species x site x year. Pollinator-side
activity uses the number of distinct *other* plant partners in the current-year
interaction network, explicitly excluding the focal plant.

The published pollinator abundance field is not used in the primary analysis
because it may share observation support with the focal interaction response.
Current-year plant abundance (AbundanceP) is exported only for a prespecified
sensitivity analysis.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


YEARS = tuple(range(2015, 2023))


def _read(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _text(value):
    return "" if value is None else str(value).strip().lower()


def _number(value):
    text = "" if value is None else str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("interactions", type=Path)
    parser.add_argument("pollinator_table", type=Path)
    parser.add_argument("plant_table", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    links = defaultdict(set)
    for row in _read(args.interactions):
        site = _text(row.get("Site_ID"))
        year = int(float(row["Year"]))
        pollinator = _text(row.get("Pollinator_gen_sp"))
        plant = _text(row.get("Plant_gen_sp"))
        if not site or not plant or not pollinator or year not in YEARS:
            continue
        links[(site, year)].add((plant, pollinator))

    poll_presence = defaultdict(set)
    for row in _read(args.pollinator_table):
        site = _text(row.get("Site_ID"))
        year = int(float(row["Year"]))
        pollinator = _text(row.get("Pol_gen_sp"))
        if site and pollinator and year in YEARS:
            poll_presence[(site, year)].add(pollinator)

    plant_presence = defaultdict(set)
    plant_phenology = {}
    plant_abundance = {}
    for row in _read(args.plant_table):
        site = _text(row.get("Site_ID"))
        year = int(float(row["Year"]))
        plant = _text(row.get("Plant_gen_sp"))
        phenology = _number(row.get("PhenologyP"))
        abundance = _number(row.get("AbundanceP"))
        if not site or not plant or year not in YEARS:
            continue
        plant_presence[(site, year)].add(plant)
        plant_phenology[(site, year, plant)] = phenology
        plant_abundance[(site, year, plant)] = abundance

    site_years = defaultdict(set)
    for site, year in set(links) | set(poll_presence) | set(plant_presence):
        site_years[site].add(year)
    sites = sorted(site_years)

    rows = []
    transition_receipts = []
    for site in sites:
        years = sorted(site_years[site])
        for previous_year, current_year in zip(years, years[1:]):
            if current_year != previous_year + 1:
                continue

            shared_plants = (
                plant_presence[(site, previous_year)]
                & plant_presence[(site, current_year)]
            )
            shared_polls = (
                poll_presence[(site, previous_year)]
                & poll_presence[(site, current_year)]
            )
            if not shared_plants or not shared_polls:
                continue

            previous_links = links[(site, previous_year)]
            current_links = links[(site, current_year)]

            current_poll_other_plants = defaultdict(set)
            for plant, pollinator in current_links:
                current_poll_other_plants[pollinator].add(plant)

            gain_events = loss_events = 0
            gain_rows = loss_rows = 0

            for plant in sorted(shared_plants):
                phenology = plant_phenology.get((site, current_year, plant))
                abundance = plant_abundance.get((site, current_year, plant))
                if phenology is None or abundance is None:
                    continue

                for pollinator in sorted(shared_polls):
                    previous_link = (plant, pollinator) in previous_links
                    current_link = (plant, pollinator) in current_links

                    otherplants = current_poll_other_plants.get(
                        pollinator, set()
                    ) - {plant}
                    poll_activity = len(otherplants)

                    if previous_link:
                        risk_set = "loss"
                        outcome = int(not current_link)
                        loss_rows += 1
                        loss_events += outcome
                    else:
                        risk_set = "gain"
                        outcome = int(current_link)
                        gain_rows += 1
                        gain_events += outcome

                    rows.append(
                        {
                            "site": site,
                            "previous_year": previous_year,
                            "current_year": current_year,
                            "transition": f"{previous_year}->{current_year}",
                            "plant": plant,
                            "pollinator": pollinator,
                            "risk_set": risk_set,
                            "outcome": outcome,
                            "previous_link": int(previous_link),
                            "current_link": int(current_link),
                            "plant_phenology_days": phenology,
                            "plant_abundance": abundance,
                            "pollinator_otherplant_degree": poll_activity,
                        }
                    )

            transition_receipts.append(
                {
                    "site": site,
                    "transition": f"{previous_year}->{current_year}",
                    "shared_plants": len(shared_plants),
                    "shared_pollinators": len(shared_polls),
                    "gain_rows": gain_rows,
                    "gain_events": gain_events,
                    "loss_rows": loss_rows,
                    "loss_events": loss_events,
                }
            )

    if not rows:
        raise SystemExit("external replication table is empty")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    site_counts = {}
    for site in sites:
        site_rows = [row for row in rows if row["site"] == site]
        if not site_rows:
            continue
        site_counts[site] = {
            "rows": len(site_rows),
            "gain_rows": sum(row["risk_set"] == "gain" for row in site_rows),
            "gain_events": sum(
                int(row["outcome"])
                for row in site_rows
                if row["risk_set"] == "gain"
            ),
            "loss_rows": sum(row["risk_set"] == "loss" for row in site_rows),
            "loss_events": sum(
                int(row["outcome"])
                for row in site_rows
                if row["risk_set"] == "loss"
            ),
        }

    result = {
        "schema": "adaptive-gain-dominguez2026-external-axis-table-v1",
        "date": "2026-09-29",
        "site_count": len(site_counts),
        "year_range": [min(YEARS), max(YEARS)],
        "row_count": len(rows),
        "transition_count": len(transition_receipts),
        "site_counts": site_counts,
        "transition_receipts": transition_receipts,
        "predictors": {
            "primary_plant_axis": "plant_phenology_days",
            "primary_pollinator_axis": "pollinator_otherplant_degree",
            "plant_abundance_sensitivity": "plant_abundance",
        },
        "focal_dyad_excluded_from_pollinator_activity": True,
        "published_pollinator_abundance_used": False,
        "species_presence_sources": {
            "plants": "Abn_Pheno_P.csv site-year rows",
            "pollinators": "Abn_Pheno.csv site-year rows",
        },
    }
    args.summary.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
