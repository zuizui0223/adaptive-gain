"""Stage46: real published modeled bee species × 1.5deg grid → Bombus map table.

Laborieux et al. (2026) original 396,703-row model/range-derived presence
matrix, Zenodo record 20525240, sourced from the original data.zip.
This is a MODELED/RECONSTRUCTED geographic cell occurrence, not bee abundance,
not a true species absence and not a Bombus pollination probability.
Some source ranges are SDMs, others are polygons for sparse taxa: label
accordingly. Source ZIP central CRC and exact CSV SHA256 pinned.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv
import io
import json
from pathlib import Path
import re

from extract_bee_pa_matrix import (
    SOURCE_NAME,decompress_original_member,source_matrix_schema
)
from zip_range_catalog import get_range,parse_central_directory,central_directory_location
from discover_pollinator_sdm_sources import _get_json

ZENODO="https://zenodo.org/api/records/20525240"
SOURCE_INNER_SHA256="641c0bb832781d3c41402a6e8158d971d0d0f663557c3f53a3b81a69dbbacd15"
SOURCE_CRC32=1022223877
NAME_BOMBUS=re.compile(r"^Bombus\s+\S+",re.I)


def modelled_bombus_coverage(content):
    original=source_matrix_schema(content)
    if (original["source_matrix_member_SHA256"]!=SOURCE_INNER_SHA256 or
        original["n_data_rows"]!=396703 or original["first_30_columns"]!=["siteid","species"]):
        raise ValueError("NO_GO_BEE_SPECIES_GRID_SOURCE_BYTES_CHANGED")
    reader=csv.DictReader(io.StringIO(content.decode("utf8-sig"),newline=""))
    seen=set()
    duplicated=0
    allspecies=set()
    alls=defaultdict(set)
    bombus=defaultdict(set)
    b_species=defaultdict(set)
    for row in reader:
        cell=(row.get("siteid") or "").strip()
        taxon=(row.get("species") or "").strip()
        if not re.fullmatch(r"HEX[0-9]+",cell) or not taxon:
            raise ValueError("NO_GO_BAD_MODELED_BEE_TAXON_OR_HEX_GRID")
        idkey=(cell,taxon)
        if idkey in seen:
            duplicated+=1
            continue
        seen.add(idkey)
        alls[cell].add(taxon)
        allspecies.add(taxon)
        if NAME_BOMBUS.match(taxon):
            bombus[cell].add(taxon)
            b_species[taxon].add(cell)
    values=sorted((c,len(bombus[c]),len(alls[c]))
                  for c in alls)
    byspecies=sorted((s,len(cells)) for s,cells in b_species.items())
    byrich=Counter(b for _,b,_ in values)
    byother=Counter(x for _,_,x in values)
    return {
      "status":"SOURCE_VERIFIED_ORIGINAL_PREDICTED_BOMBUS_HEX_RICHNESS",
      "source_doi":"10.5281/zenodo.20525239",
      "source_record_version":20525240,
      "original_input_rows":original["n_data_rows"],
      "duplicate_source_species_cell_pairs":duplicated,
      "n_unique_modeled_bee_taxon_strings":len(allspecies),
      "n_grid_cells_with_any_modeled_bee_taxon":len(alls),
      "n_distinct_modelled_Bombus_taxon_strings":len(b_species),
      "n_grid_cells_with_Bombus_modelled_presence":sum(b>0 for _,b,_ in values),
      "n_grid_cells_zero_Bombus_in_covered_source_grid":sum(b==0 for _,b,_ in values),
      "number_of_Bombus_by_grid_cell_distribution":dict(sorted(byrich.items())),
      "min_modelled_bombus_richness":min((b for _,b,_ in values),default=None),
      "max_modelled_bombus_richness":max((b for _,b,_ in values),default=None),
      "source_member_SHA256":SOURCE_INNER_SHA256,
      "source_member_crc32":SOURCE_CRC32,
      "source_matrix_type":"published bee range model / sparse-species polygons, thresholded presence at native HEX spatial cells",
      "bee_source_species_names_not_yet_independently_accepted_taxonomy":True,
      "zero_is_no_modelled_genus_in_supplied_grid_not_true_biological_absence":True,
      "not_plant_X_Bombus_joint_model_or_realized_visitation":True,
      "not_raw_GBIF_occurrence_counts_or_relative_abundance":True,
      "source_only_modelled_distribution_derived_values":True,
    },values,byspecies


def _get_model_source():
    meta,_=_get_json(ZENODO)
    m=[x for x in meta.get("files") or [] if x.get("key")=="data.zip"]
    if len(m)!=1:raise ValueError("NO_GO_MISSING_PUBLISHED_DATA_ZIP")
    f=m[0];url=(f.get("links") or {}).get("self");size=f.get("size")
    tail_start=max(0,size-262144)
    tail=get_range(url,size,tail_start,size-1)
    offset,length,count=central_directory_location(tail,size)
    cd=parse_central_directory(get_range(url,size,offset,offset+length-1),count)
    matched=[x for x in cd if x["filename"]==SOURCE_NAME]
    if len(matched)!=1 or matched[0]["crc32"]!=SOURCE_CRC32:
        raise ValueError("NO_GO_SOURCE_ZIP_MEMBER_CHANGED")
    return decompress_original_member(url,size,matched[0])


def main():
    source=_get_model_source()
    report,grid,taxa=modelled_bombus_coverage(source)
    folder=Path("stage46_Bombus_prediction")
    folder.mkdir(exist_ok=True)
    with (folder/"source_Bombus_predicted_hex_richness.csv").open(
            "w",encoding="utf8",newline="") as output:
        writer=csv.writer(output)
        writer.writerow(["source_siteid","n_modelled_Bombus_taxa",
                         "n_all_modelled_bee_taxa","source_doi",
                         "distribution_meaning"])
        for cell,b,anybee in grid:
            writer.writerow([cell,b,anybee,"10.5281/zenodo.20525239",
                             "source_modelled_presence_not_observed_pollination"])
    with (folder/"original_Bombus_model_taxon_hex_coverage.csv").open(
            "w",encoding="utf8",newline="") as output:
        writer=csv.writer(output)
        writer.writerow(["source_Bombus_taxon_name","n_source_hex_cells",
                         "taxonomic_acceptance_status","source_doi"])
        for species,ncells in taxa:
            writer.writerow([species,ncells,"needs_independent_accepted_taxonomy",
                            "10.5281/zenodo.20525239"])
    (folder/"source_Bombus_predicted_hex_coverage.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True,allow_nan=False)+"\n")
    print("STAGE46_REAL_PUBLISHED_MODELED_BOMBUS_HEX_RESULTS",json.dumps(report,sort_keys=True))
    print("STAGE46_BOMBUS_SOURCE_TAXON_EXAMPLES",json.dumps(taxa[:35]))
    print("MODELLED_HEX_GRID_HAS_NO_LONG_LAT_TO_JOIN_PLANTS_UNTIL_SHAPEFILE_MAPPING")


if __name__=="__main__":
    main()
