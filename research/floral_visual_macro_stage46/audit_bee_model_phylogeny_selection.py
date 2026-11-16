"""Stage46: assess modeled bee taxon pool versus published phylogenetic subset.

Uses original 2026 global bee Zenodo source: original 126MB ZIP only via
HTTP byte ranges to extract small tree, and 14KB author analysis script.
A tree-tip intersection is NOT proof of final published 3,370 taxon list.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

from discover_pollinator_sdm_sources import _get_json
from inspect_compact_source_tables import original_bytes
from zip_range_catalog import get_range,central_directory_location,parse_central_directory
from extract_bee_pa_matrix import decompress_original_member

RECORD="https://zenodo.org/api/records/20525240"
TREE_FILE="data/BEE_mat7_fulltree_tplo35_sf20lp.nwk"
MODEL_SCRIPT="4_Bee_bioregion_analysis_data_export.r"


def tree_tips(text):
    """Conservative tip extraction (not an inferred biological phylogeny)."""
    if not text.strip().endswith(";"):
        raise ValueError("NO_GO_INVALID_ORIGINAL_NEWICK_TERMINATOR")
    raw=re.findall(r"(?<=[,(])\s*('(?:[^']|'')+'|[^():,;\s]+)\s*(?=:)",text)
    return [x.strip().strip("'") for x in raw]


def audit():
    meta,_=_get_json(RECORD)
    files=meta.get("files") or []
    zipped=[x for x in files if x.get("key")=="data.zip"]
    scripts=[x for x in files if x.get("key")==MODEL_SCRIPT]
    if len(zipped)!=1 or len(scripts)!=1:
        raise ValueError("NO_GO_PUBLIC_RESEARCH_SOURCES_UNIDENTIFIED")
    z=zipped[0];url=(z.get("links") or {}).get("self");size=z.get("size")
    tail=get_range(url,size,max(0,size-262144),size-1)
    off,nbytes,n=central_directory_location(tail,size)
    cd=parse_central_directory(get_range(url,size,off,off+nbytes-1),n)
    trees=[x for x in cd if x["filename"]==TREE_FILE]
    if len(trees)!=1:
        raise ValueError("NO_GO_ORIGINAL_BEE_TREE_NOT_IN_ARCHIVE")
    source=decompress_original_member(url,size,trees[0])
    tree=source.decode("utf-8-sig",errors="replace")
    tips=tree_tips(tree)
    if len(tips)<100:
        raise ValueError("NO_GO_NOT_ACTUAL_BEE_PHYLOGENY")
    source_r=scripts[0]
    scode=original_bytes((source_r.get("links") or {}).get("self"))
    declared=source_r.get("checksum")
    md5="md5:"+hashlib.md5(scode).hexdigest()
    if declared and md5!=declared:
        raise ValueError("NO_GO_AUTHOR_SCRIPT_HASH_MISMATCH")
    lines=scode.decode("utf-8-sig",errors="replace").splitlines()
    matches=[{"line_number":i+1,
              "line_excerpt":line.strip()[:120]}
             for i,line in enumerate(lines) if any(k in line.lower()
              for k in ("bee_presence_only_matrix","filter","tree","prun","species","taxa","tip.label","pa_mat"))]
    bs=[x for x in tips if re.search(r"(?i)^bombus(?:_| )",x)]
    return {
      "status":"AUTHENTIC_BEE_PHYLOGENETIC_SOURCE_AND_ANALYSIS_FILTER_AUDIT",
      "original_tree_name":TREE_FILE,
      "original_tree_sha256":hashlib.sha256(source).hexdigest(),
      "tree_tip_count_unvalidated_taxonomy":len(tips),
      "source_tree_first_12_tips":tips[:12],
      "tree_tip_Bombus_like_count":len(bs),
      "tree_first_20_Bombus_like_tips":bs[:20],
      "source_analysis_script":MODEL_SCRIPT,
      "original_script_md5":md5,
      "analysis_script_line_count":len(lines),
      "candidate_processing_line_number_and_snippet":matches[:65],
      "not_final_3370_taxon_population_until_source_proven":True,
      "not_a_genuine_Bombus_richness_map":True
    }


if __name__=="__main__":
    obj=audit()
    d=Path("stage46_study_taxa_audit");d.mkdir(exist_ok=True)
    (d/"original_bee_tree_and_sampling_filter_evidence.json").write_text(
        json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print("STAGE46_BEE_MODELLED_VERSUS_PAPER_TAXON_AUDIT",json.dumps(obj,ensure_ascii=False,sort_keys=True))
