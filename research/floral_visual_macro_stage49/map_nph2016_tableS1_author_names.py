"""Stage49: recover full original genus and binomial from same 2016 NPH S1.

The 177 original UV trait rows use abbreviated genus-source codes (e.g.
P_eriocarpa). Table S1 in the SAME checksum-authenticated PDF contains
author full genus/species names for the source phylogeny. Join only when
genus-initial+epithet has exactly one possible original author genus.
Keep infraspecific UV codes distinct; never silently treat different
varieties as independent accepted species or force a guessed name.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile
from extract_nph2016_original_uv_177 import (
    parse_source_rows,summarize,PAGES,MEMBER,ORIGINAL_TABLE_PDF_SHA256
)
from probe_nph2016_177_europepmc_supplement import _fetch,API

KNOWN_SOURCE_GENE=("Argentina","Dasiphora","Drymocallis","Duchesnea","Fragaria",
                   "Horkelia","Ivesia","Potentilla","Sibbaldia")
STUDY_DOI="10.1111/nph.13921"
NAME_RE=re.compile(r"^("+"|".join(KNOWN_SOURCE_GENE)+r")\s+([a-z][a-z-]+)\b")

def s1_author_name_index(pages):
    # Excludes Table S2 to avoid deriving a full name from abbreviations.
    genes=defaultdict(set)
    seen_full=set()
    for i,txt in sorted(pages.items()):
        if i not in range(3,17):
            raise ValueError("NO_GO_NOT_SOURCE_TABLE_S1_PAGE")
        for raw in txt.splitlines():
            line=raw.strip()
            m=NAME_RE.match(line)
            if not m:
                continue
            genus,epithet=m.groups()
            genes[(genus[0],epithet)].add(genus)
            seen_full.add(genus+" "+epithet)
    return genes,seen_full

def source_match_rows(rows,genes):
    out=[]
    issues=Counter()
    for row in rows:
        code=row["original_taxon_code"]
        parts=code.split("_")
        if len(parts)<2 or not parts[0] or not parts[1]:
            raise ValueError("NO_GO_BAD_ORIGINAL_S2_CODE")
        prefix=parts[0];epithet=parts[1]
        opts=genes.get((prefix,epithet),set())
        if len(opts)==1:
            full=next(iter(opts))+" "+epithet
            status="AUTHOR_S1_EXACT_GENUS_INITIAL_EPITHET_MATCH"
        elif len(opts)>1:
            full=""
            status="AMBIGUOUS_AUTHOR_S1_GENUS_EPITHET"
        else:
            full=""
            status="NO_AUTHOR_S1_NAME_MATCH_NOT_ABSENT"
        reassembled=dict(row)
        reassembled.update({
          "original_S1_author_full_binomial_candidate":full,
          "S1_source_match_status":status,
          "S1_multiple_source_infraspecific_tokens":int(len(parts)>2),
          "source_S1_study_doi":STUDY_DOI,
          "GBIF_accepted_species_key":"NOT_QUERIED",
          "UV_pattern_source_taxon_unit":"original_paper_S2_row_not_accepted_species",
        })
        out.append(reassembled)
        issues[status]+=1
    species=Counter(x["original_S1_author_full_binomial_candidate"]
                    for x in out if x["original_S1_author_full_binomial_candidate"])
    duplicates={k:v for k,v in species.items() if v>1}
    return out,{
        "status":"NPH2016_ORIGINAL_S1_TO_S2_UV_SOURCE_NAME_CROSSWALK",
        "n_original_S2_UV_measured_taxon_rows":len(rows),
        "n_full_author_binomial_lexical_candidates":issues[
            "AUTHOR_S1_EXACT_GENUS_INITIAL_EPITHET_MATCH"
        ],
        "n_S1_original_author_names_missing":issues["NO_AUTHOR_S1_NAME_MATCH_NOT_ABSENT"],
        "n_S1_ambiguous_genus_candidates":issues["AMBIGUOUS_AUTHOR_S1_GENUS_EPITHET"],
        "unique_full_binomial_source_name_count":len(species),
        "original_source_binomials_with_multiple_infraspecific_source_traits":duplicates,
        "S1_genus_epithet_join_is_not_accepted_species_taxonomy":True,
        "no_uv_guide_Bombus_plant_fitness_association":True,
    }

def main():
    import fitz
    blob,_=_fetch(API)
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        pdfbytes=z.read(MEMBER)
    if hashlib.sha256(pdfbytes).hexdigest()!=ORIGINAL_TABLE_PDF_SHA256:
        raise ValueError("NO_GO_2016_S1_S2_ORIGINAL_SUPPLEMENT_PDF_MISMATCH")
    with fitz.open(stream=pdfbytes,filetype="pdf") as pdf:
        if len(pdf)!=23:
            raise ValueError("NO_GO_2016_S1_S2_PAGE_COUNT")
        names={i:pdf[i].get_text("text") for i in range(3,17)}
        traits={i:pdf[i].get_text("text") for i in PAGES}
    index,author_full=s1_author_name_index(names)
    rows=parse_source_rows(traits)
    validated=summarize(rows)
    assigned,report=source_match_rows(rows,index)
    report["author_S1_source_binomial_strings_found"]=len(author_full)
    report["author_S1_source_unique_genus_epithet_initials"]=len(index)
    report["original_supplement_PDF_SHA256"]=ORIGINAL_TABLE_PDF_SHA256
    report["UV_2016_patterned_source_rows"]=validated["n_UV_pattern_present_from_0"]
    report["UV_2016_uniform_source_rows"]=validated["n_uniform_UV_absorbing_from_1"]
    p=Path("stage49_2016_UV_author_names")
    p.mkdir(exist_ok=True)
    with (p/"Koski_Ashman2016_original_177_UV_with_S1_author_binomials.csv").open(
        "w",encoding="utf8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(assigned[0]))
        wr.writeheader()
        wr.writerows(assigned)
    (p/"original_S1_S2_author_taxonomic_join_receipt.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf8")
    print("STAGE49_ORIGINAL_177_UV_AUTHOR_NAME_CROSSWALK",
          json.dumps(report,ensure_ascii=False,sort_keys=True))
    print("STAGE49_UNMATCHED_2016_SOURCE_CODES",json.dumps(
      [x["original_taxon_code"] for x in assigned
       if not x["original_S1_author_full_binomial_candidate"]][:35]))
    if report["n_full_author_binomial_lexical_candidates"]<120:
        raise SystemExit("NO_GO_TOO_FEW_VALIDATED_AUTHOR_ORIGINAL_BINOMIALS")

if __name__=="__main__":
    main()
