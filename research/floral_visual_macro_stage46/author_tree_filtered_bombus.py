"""Stage46: source-reproduced bee species/HEX eligibility from original R methods.

Compare 396,703-row publicly modeled bee range input with the ORIGINAL
phylogeny and author R code from Laborieux et al. (2026), Zenodo 20525240.
Keep first two underscores of tree tip labels (same source R script), intersect
with original species matrix and enforce only the explicit source per-cell
pa_cutoff; do not claim phylogenetic name strings are taxonomically accepted.

Join eligible source hex cells to authentic 10,242 original hex centroids.
Source-modelled zeros, excluded cells and unsampled hexes differ.
No correlation with UV vegetation, no Bombus abundance/visits inferred.
"""
from __future__ import annotations

from collections import Counter,defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re

from discover_pollinator_sdm_sources import _get_json
from audit_bee_model_phylogeny_selection import (
    tree_tips,TREE_FILE,MODEL_SCRIPT
)
from derive_bombus_hex_prediction import (
    _get_model_source,modelled_bombus_coverage,SOURCE_INNER_SHA256
)
from zip_range_catalog import get_range,central_directory_location,parse_central_directory
from extract_bee_pa_matrix import decompress_original_member
from inspect_compact_source_tables import original_bytes
from georeference_bombus_prediction import load_original_hex_centroids

ZENODO="https://zenodo.org/api/records/20525240"
SOURCE_MATRIX_ROWS=396703
BOMBUS=re.compile(r"^Bombus\s+\S+",re.I)


def source_parameter_and_taxa(original_script,tree_nwk):
    script=original_script.decode("utf-8-sig",errors="replace")
    params=re.findall(r"(?m)^\s*pa_cutoff\s*(?:<-|=)\s*(\d+)",script)
    if len(params)!=1:
        # Report actual lines to distinguish absent variable from source drift
        hints=[x[:140] for x in script.splitlines() if "pa_cutoff" in x]
        raise ValueError("NO_GO_SOURCE_PA_CUTOFF_UNIDENTIFIED "+repr(hints[:8]))
    n=int(params[0])
    if n<1 or n>300:
        raise ValueError("NO_GO_SOURCE_PA_CUTOFF_OUTSIDE_EXPECTED_RANGE")
    text=tree_nwk.decode("utf-8-sig",errors="replace")
    original_tips=tree_tips(text)
    if len(original_tips)<3000:
        raise ValueError("NO_GO_SOURCE_TREE_TOO_FEW_TIPS")
    names=[]
    for tip in original_tips:
        parts=tip.split("_")
        if len(parts)<2:
            raise ValueError("NO_GO_SOURCE_TREE_TIP_NO_TWO_PART_SPECIES")
        names.append(" ".join(parts[:2]))
    if len(set(names))!=len(names):
        raise ValueError("NO_GO_COLLAPSED_DUPLICATE_SOURCE_PHYLOGENY_TAXA")
    if "shared_species <- intersect(pa_all$species, bee_phylo_consensus$tip.label)" not in script:
        raise ValueError("NO_GO_SOURCE_PHYLOGENY_INTERSECTION_SEMANTIC_CHANGED")
    if "filter(n_distinct(species) >= pa_cutoff)" not in script:
        raise ValueError("NO_GO_SOURCE_PA_CELL_CUTOFF_SEMANTIC_CHANGED")
    return {"pa_cutoff":n,
            "original_tree_tip_count":len(original_tips),
            "source_original_tree_tip_to_species_count":len(names),
            "tree_bombus_tip_count":sum(BOMBUS.match(x) is not None for x in names),
            "source_R_script_MD5":"md5:"+hashlib.md5(original_script).hexdigest(),
            "source_newick_SHA256":hashlib.sha256(tree_nwk).hexdigest(),
            "assumes_source_R_phylogenetic_shared_species_and_site_filter":True
           },set(names)


def trim_original_bee_matrix(matrix,phylo_taxa,cutoff):
    reader=csv.DictReader(io.StringIO(matrix.decode("utf-8-sig"),newline=""))
    if reader.fieldnames!=["siteid","species"]:
        raise ValueError("NO_GO_SOURCE_BEE_MATRIX_GRAIN_CHANGED")
    raw_species=set()
    original_hex=defaultdict(set)
    accepted_hex=defaultdict(set)
    for row in reader:
        siteid=row["siteid"]
        taxon=row["species"]
        if not siteid.startswith("HEX") or not taxon:
            raise ValueError("NO_GO_RAW_SOURCE_MATRIX_BAD")
        raw_species.add(taxon)
        original_hex[siteid].add(taxon)
        if taxon in phylo_taxa:
            accepted_hex[siteid].add(taxon)
    retained={cell: taxa for cell,taxa in accepted_hex.items()
              if len(taxa)>=cutoff}
    accepted_species=set().union(*retained.values()) if retained else set()
    shared_species=raw_species & phylo_taxa
    return {
      "raw_model_taxon_strings":len(raw_species),
      "original_raw_model_hex_cells":len(original_hex),
      "n_shared_phylogeny_original_model_taxa":len(shared_species),
      "source_cells_with_at_least_one_tree_matched_species":len(accepted_hex),
      "source_cells_after_original_pa_cutoff":len(retained),
      "source_taxa_after_tree_and_cell_cutoff":len(accepted_species),
      "source_Bombus_species_after_tree_cell_cutoff":sum(bool(BOMBUS.match(x)) for x in accepted_species),
      "n_hex_with_Bombus_after_paper_filter":sum(any(BOMBUS.match(s) for s in taxa)
                                                for taxa in retained.values()),
      "not_confirmed_global_model_3370_without_full_R_replay":True,
      "no_lack_of_records_included_as_bee_absence":True,
    },retained,shared_species


def fetch_author_small_sources():
    meta,_=_get_json(ZENODO)
    files=meta.get("files") or []
    zipped=[x for x in files if x.get("key")=="data.zip"]
    scripts=[x for x in files if x.get("key")==MODEL_SCRIPT]
    if len(zipped)!=1 or len(scripts)!=1:
        raise ValueError("NO_GO_ORIGINAL_ANALYSIS_SOURCE_MISSING")
    z=zipped[0]
    url=(z.get("links") or {}).get("self");size=z.get("size")
    tail=get_range(url,size,max(0,size-262144),size-1)
    off,length,n=central_directory_location(tail,size)
    entries=parse_central_directory(get_range(url,size,off,off+length-1),n)
    match=[x for x in entries if x["filename"]==TREE_FILE]
    if len(match)!=1:
        raise ValueError("NO_GO_PHYLOGENETIC_TREE_MEMBER_MISSING")
    tree=decompress_original_member(url,size,match[0])
    script=scripts[0]
    txt=original_bytes((script.get("links") or {}).get("self"))
    if script.get("checksum")!="md5:"+hashlib.md5(txt).hexdigest():
        raise ValueError("NO_GO_AUTHOR_SCRIPT_CHECKSUM_CHANGED")
    return txt,tree


def materialize_join(retained,centroids):
    if not set(retained).issubset(centroids):
        raise ValueError("NO_GO_PAPER_FILTERED_HEX_NOT_IN_SOURCE_GEOMETRY")
    rows=[]
    for hexid,(longitude,latitude) in sorted(centroids.items()):
        eligible=hexid in retained
        taxa=retained.get(hexid,set())
        n_bombus=sum(bool(BOMBUS.match(s)) for s in taxa) if eligible else None
        rows.append({
            "source_siteid":hexid,"longitude":longitude,"latitude":latitude,
            "n_source_tree_and_pa_cutoff_Bombus_taxa":n_bombus,
            "n_source_tree_and_pa_cutoff_all_bee_taxa":len(taxa) if eligible else None,
            "eligibility":("AUTHOR_TREE_AND_PA_CELL_CUTOFF" if eligible
                     else "OUTSIDE_AUTHOR_FILTERED_MODEL_NO_ABSENCE_INFERENCE"),
            "model_origin":"10.5281/zenodo.20525239",
            "source_taxa_not_independently_accepted_or_native":True
        })
    return rows


def main():
    script,tree=fetch_author_small_sources()
    p,phylo=source_parameter_and_taxa(script,tree)
    matrix=_get_model_source()
    raw,_,_=modelled_bombus_coverage(matrix)
    if raw["original_input_rows"]!=SOURCE_MATRIX_ROWS or raw["source_member_SHA256"]!=SOURCE_INNER_SHA256:
        raise ValueError("NO_GO_ORIGINAL_BEE_INPUT_CHANGED")
    stats,retained,shared=trim_original_bee_matrix(matrix,phylo,p["pa_cutoff"])
    centroids,geo=load_original_hex_centroids()
    rows=materialize_join(retained,centroids)
    summary={
      "status":"AUTHENTIC_ORIGINAL_BEE_PHYLOGENY_FILTERED_HEX_BOMBUS_MODEL",
      "provenance":"Laborieux et al 2026 source tree, CSV, R pa_cutoff, ZIP and original geo DBF",
      "source_decisions":p,
      "source_filter_result":stats,
      "global_hex_rows":len(rows),
      "unique_eligible_original_Bombus_model_source_strings":stats["source_Bombus_species_after_tree_cell_cutoff"],
      "source_modelled_coverage_is_not_true_bee_absence_or_observed_visitation":True,
      "no_plant_visual_trait_x_Bombus_association_tested":True,
      "not_independently_accepted_nativity_or_phylogenetic_method_validation":True,
    }
    folder=Path("stage46_paper_filtered_Bombus")
    folder.mkdir(exist_ok=True)
    pth=folder/"original_tree_and_PA_filtered_Bombus_hex_geographic_10242.csv"
    with pth.open("w",encoding="utf8",newline="") as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (folder/"paper_species_filter_source_receipt.json").write_text(
        json.dumps(summary,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("STAGE46_AUTHOR_PHYLOGENY_FILTERED_BOMBUS_RESULTS",json.dumps(summary,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
