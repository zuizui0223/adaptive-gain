"""Stage49: exact source-verified original 2020 floral UV study taxon roster.

Extract Current Biology supplemental Table S1 from the previously SHA256-
audited open-access source PDF. Source table has CONTINENT × published
binomial rows, NOT one record per unique species; four names are sampled
across more than one continent. The article itself reports 42 species,
so if literal dedup count differs it is reported as source reconciliation
rather than silently changed.

UVP slope is a temporal standardized slope in 1941-2017 herbarium
samples, NOT physical guide presence, absence or cue use by bees.
"""
from __future__ import annotations

from collections import Counter,defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import urllib.request

from probe_current_biology_original_table_s1 import SOURCE_URL,MAX_BYTES

ORIGINAL_PDF_SHA256="180c0cfbfb74219edfeae8c3596b7a815968aa30fb10d82cd022debe426646e6"
SOURCE_DOI="10.1016/j.cub.2020.08.077"
TABLE_PAGES=(13,14)
FIELDS=(
    "continent","family","genus","epithet","floral_anther_position_code",
    "life_history_code","habitat_code","original_herbarium_samples",
    "standardized_UVP_slope_per_year","standardized_ozone_slope_per_year",
    "standardized_temperature_slope_per_year",
    "first_collection_year","last_collection_year","collection_year_span"
)
CONTINENTS=("Australia","Eurasia","N. America")
FAMILY=re.compile(r"^[A-Z][a-z]+aceae$")
GENUS=re.compile(r"^[A-Z][a-zA-Z-]+$")
EPITHET=re.compile(r"^[a-z][a-z-]+$")

def _record(cells):
    if len(cells)!=14:
        raise ValueError("NO_GO_ORIGINAL_S1_ROW_ARITY")
    d=dict(zip(FIELDS,cells))
    if d["continent"] not in CONTINENTS or not FAMILY.fullmatch(d["family"]) or (
        not GENUS.fullmatch(d["genus"])) or not EPITHET.fullmatch(d["epithet"]):
        raise ValueError("NO_GO_ORIGINAL_PUBLISHED_TAXON_STRUCTURE")
    if d["floral_anther_position_code"] not in ("E","C") or (
        d["life_history_code"] not in ("p","s") or
        d["habitat_code"] not in ("o","s")):
        raise ValueError("NO_GO_ORIGINAL_PUBLISHED_EXPOSURE_CODES")
    for key in ("original_herbarium_samples","first_collection_year",
                "last_collection_year","collection_year_span"):
        value=d[key]
        if not value.isdigit():
            raise ValueError("NO_GO_ORIGINAL_NUMERIC_COUNTS")
        d[key]=int(value)
    if d["original_herbarium_samples"]<1 or (
       d["last_collection_year"]-d["first_collection_year"]!=d["collection_year_span"]):
        raise ValueError("NO_GO_ORIGINAL_YEAR_SPAN")
    for k in ("standardized_UVP_slope_per_year",
              "standardized_ozone_slope_per_year",
              "standardized_temperature_slope_per_year"):
        try:
            d[k]=float(d[k].replace("−","-"))
        except ValueError as e:
            raise ValueError("NO_GO_PUBLISHED_SLOPE_NOT_NUMERIC") from e
    d["taxon_binomial_as_published"]=d["genus"]+" "+d["epithet"]
    d["source_paper_doi"]=SOURCE_DOI
    d["uv_area_spatiotemporal_measured"]=1
    d["uv_nectar_guide_presence"]="NOT_MEASURED_OR_NOT_REPORTED_IN_S1"
    d["bee_use_of_visual_signal"]="NOT_MEASURED_IN_S1"
    d["photo_or_specimen_linkage_to_Bombus_model"]="NOT_YET_DONE"
    d["original_source_pdf_sha256"]=ORIGINAL_PDF_SHA256
    return d

def parse_table_s1_text(pages):
    # PDF text is in row order on pages 13 and 14. Do not parse the
    # phylogenetic Figure S1 labels on page 12 as additional taxa.
    source=[]
    for page_no,txt in sorted(pages.items()):
        if page_no not in TABLE_PAGES:
            raise ValueError("NO_GO_TABLE_S1_WRONG_PAGES")
        lines=[x.strip() for x in txt.splitlines() if x.strip()]
        if page_no==13:
            # Last component of header's "Year Range".
            try:
                start=lines.index("Range")+1
            except ValueError as exc:
                raise ValueError("NO_GO_ORIGINAL_S1_HEADER_NOT_FOUND") from exc
        else:
            start=0
        if page_no==14:
            try:
                stop=next(i for i,s in enumerate(lines)
                          if s.startswith("Table S1: Taxa included"))
            except StopIteration as exc:
                raise ValueError("NO_GO_ORIGINAL_S1_FOOTER_NOT_FOUND") from exc
        else:
            stop=len(lines)
        core=lines[start:stop]
        if len(core)%14!=0:
            raise ValueError("NO_GO_S1_TABLE_LINES_NOT_MULTIPLE_OF_FOURTEEN")
        for i in range(0,len(core),14):
            source.append(_record(core[i:i+14]))
    return source

def evaluate(rows):
    if not rows:
        raise ValueError("NO_GO_SOURCE_TABLE_EMPTY")
    by_continent=Counter(x["continent"] for x in rows)
    names={x["taxon_binomial_as_published"] for x in rows}
    n_sample=sum(x["original_herbarium_samples"] for x in rows)
    taxa_to_continents=defaultdict(set)
    for x in rows:
        taxa_to_continents[x["taxon_binomial_as_published"]].add(x["continent"])
    repeated={k:sorted(v) for k,v in taxa_to_continents.items() if len(v)>1}
    return {
       "status":"SOURCE_PAPER_TABLE_S1_CONTINENT_BY_TAXON_UV_HERBARIUM_ROSTER",
       "source_paper_doi":SOURCE_DOI,
       "n_source_continent_by_taxon_rows":len(rows),
       "n_unique_literal_published_binomials":len(names),
       "repeated_taxon_names_across_continents":repeated,
       "source_continent_counts":dict(sorted(by_continent.items())),
       "source_herbarium_samples_sum":n_sample,
       "article_reports_42_species":True,
       "article_reports_1238_herbarium_samples":True,
       "literal_source_table_species_count_may_differ_from_paper_n":len(names)!=42,
       "one_row_per_continent_taxon_not_each_specimen":True,
       "do_not_treat_UVP_slope_as_UV_guide_presence":True,
       "study_1238_samples_not_independent_1238_taxa":True,
       "original_PDF_sha256":ORIGINAL_PDF_SHA256
    }

def main():
    import fitz
    req=urllib.request.Request(SOURCE_URL,headers={
       "User-Agent":"adaptive-gain-stage49-original-Current-Biology-Table-S1-2026",
       "Accept":"application/pdf,*/*"})
    with urllib.request.urlopen(req,timeout=50) as response:
        blob=response.read(MAX_BYTES+1)
    if len(blob)>MAX_BYTES or hashlib.sha256(blob).hexdigest()!=ORIGINAL_PDF_SHA256:
        raise ValueError("NO_GO_PUBLISHED_PDF_DIGEST_CHANGED")
    with fitz.open(stream=blob,filetype="pdf") as pdf:
        if len(pdf)!=15:
            raise ValueError("NO_GO_ORIGINAL_PAPER_SUPPLEMENT_PAGES_CHANGED")
        rows=parse_table_s1_text({p:pdf[p].get_text("text") for p in TABLE_PAGES})
    summary=evaluate(rows)
    out=Path("stage49_literature_species_registry")
    out.mkdir(exist_ok=True)
    fields=list(rows[0])
    with (out/"koski_2020_current_biology_original_TableS1_taxon_continent_uvp.csv").open(
         "w",newline="",encoding="utf8") as handle:
        w=csv.DictWriter(handle,fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (out/"original_TableS1_source_coverage.json").write_text(
        json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE49_SOURCE_VERIFIED_ORIGINAL_2020_UV_SPECIES_TABLE",
          json.dumps(summary,ensure_ascii=False,sort_keys=True))
    print("NO_UV_PATTERN_BINARY_IMPUTATION_NO_BOMBUS_ASSOCIATION")
if __name__=="__main__":
    main()
