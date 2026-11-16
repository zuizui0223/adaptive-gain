"""Stage45 original 2026 NHM angiosperm trait resource → first global visual-trait species registry.

Original data: CC BY (Araujo, Hartley & Brummit 2026, DOI 10.5519/p3dm31kc).
Read complete source CSV only in CI memory, calculate inspectable source-level
coverage, and emit a DERIVED table with source taxon and selected categorical
traits. Guide absence is NEVER inferred from missing/monochromatic data.
Multi-colour/markings keywords are review candidates, not confirmed guides.
No Bombus distribution suitability or association is estimated here.
"""
from __future__ import annotations

from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request

from probe_public_sources import _ckan,_safe_url,NHM_RESOURCE,NHM_DATASET_DOI

SOURCE_ROW_COUNT=59369
SOURCE_NAME="Araujo et al. 2026 NHM Angiosperm traits"
SOURCE_DOI=NHM_DATASET_DOI
MAX_CSV_BYTES=25_000_000
SELECTED_FIELDS=(
    "flower colour","petal colour","corolla colour","labellum colour",
    "flower symmetry","flower shape","flower architecture",
    "corolla tube lipped","corolla tube min_ length [cm]",
    "corolla tube max_ length [cm]","pollination","reward"
)
COLOUR_FIELDS=SELECTED_FIELDS[:4]
PATTERN_CANDIDATE=re.compile(
    r"\b(spott?ed|striped|streaked|blotch(?:ed|es)?|"
    r"bull.?s?.?eye|nectar.?guide|eye.?spot|vein(?:ed|s)?|"
    r"bicolou?red|two.?colou?red|marked|banded)\b",
    re.I
)
POLLINATOR_WORDS=re.compile(r"\b(bombus|bumble.?bee|bees?|apidae)\b",re.I)


def _get_source_bytes():
    manifest=_ckan("resource_show",{"id":NHM_RESOURCE})
    if manifest.get("id")!=NHM_RESOURCE:
        raise ValueError("NO_GO_RESOURCE_ID_CHANGED")
    expected=int(manifest.get("size") or 0)
    if expected<=100_000 or expected>MAX_CSV_BYTES:
        raise ValueError("NO_GO_RESOURCE_UNEXPECTED_SIZE")
    url=manifest.get("url")
    if not isinstance(url,str):
        raise ValueError("NO_GO_MISSING_SOURCE_CSV_URL")
    request=urllib.request.Request(_safe_url(url),headers={
       "User-Agent":"adaptive-gain-stage45-NHM-original-survey/2026",
       "Accept":"text/csv,application/octet-stream"
    })
    with urllib.request.urlopen(request,timeout=90) as stream:
        blob=stream.read(MAX_CSV_BYTES+1)
    if len(blob)>MAX_CSV_BYTES or len(blob)!=expected:
        raise ValueError("NO_GO_NHM_ORIGINAL_RESOURCE_BYTES_NOT_MATCHED")
    return blob,{"source_url":url,"declared_original_bytes":expected,
                 "download_sha256":hashlib.sha256(blob).hexdigest(),
                 "source_doi":SOURCE_DOI,"nhm_resource_id":NHM_RESOURCE}


def _value(row,key):
    value=row.get(key,"")
    if value is None:return ""
    return str(value).strip()


def summarize_and_extract(blob,expected_rows=SOURCE_ROW_COUNT):
    if not isinstance(blob,bytes):
        raise ValueError("NO_GO_ORIGINAL_SOURCE_NOT_BYTES")
    with io.StringIO(blob.decode("utf-8-sig"),newline="") as handle:
        rd=csv.DictReader(handle)
        columns=rd.fieldnames or []
        required={"taxon","wfo",*SELECTED_FIELDS}
        missing=required-set(columns)
        if missing:
            raise ValueError("NO_GO_SOURCE_SCHEMA_MISSING_"+",".join(sorted(missing)))
        coverage=Counter()
        country=Counter()
        source_taxa=set()
        rows=[]
        patterns=[]
        examples=Counter()
        for source_row in rd:
            taxon=_value(source_row,"taxon")
            if not taxon:
                raise ValueError("NO_GO_EMPTY_SOURCE_TAXON")
            wfo=_value(source_row,"wfo")
            source_taxa.add(taxon)
            filled={k:_value(source_row,k) for k in SELECTED_FIELDS}
            available={k:bool(filled[k]) for k in SELECTED_FIELDS}
            for k,yes in available.items():
                coverage[k]+=int(yes)
            colour_present=any(available[k] for k in COLOUR_FIELDS)
            morphology_present=any(available[k] for k in (
                "flower symmetry","flower shape","flower architecture",
                "corolla tube lipped"))
            pollination_present=available["pollination"]
            coverage["any_flower_color"]+=int(colour_present)
            coverage["any_morphology"]+=int(morphology_present)
            coverage["color_and_morphology"]+=int(colour_present and morphology_present)
            coverage["color_morphology_pollination"]+=int(
                colour_present and morphology_present and pollination_present)
            # Colour text is NEVER a direct guide presence/absence assertion.
            colour_text=" | ".join(filled[k] for k in COLOUR_FIELDS if filled[k])
            hits=sorted(set(m.group(0).lower() for m in PATTERN_CANDIDATE.finditer(colour_text)))
            if hits:
                coverage["unconfirmed_marking_text_cue"]+=1
                patterns.append({"taxon":taxon,"wfo":wfo,
                                 "observed_colour_text":"; ".join(
                                     filled[k] for k in COLOUR_FIELDS if filled[k])[:400],
                                 "search_tokens":"|".join(hits),
                                 "review_status":"unverified_visible_marking_candidate",
                                 "uv_guide_status":"not_measured",
                                 "source_doi":SOURCE_DOI})
            if POLLINATOR_WORDS.search(filled["pollination"]):
                coverage["pollination_text_mentions_bees_or_bombus"]+=1
            # Keep the full ACCEPTED species universe, no trait-zero imputation.
            rows.append({
              "taxon":taxon,"wfo":wfo,
              "floral_colour_reported":int(colour_present),
              "morphology_reported":int(morphology_present),
              "pollination_text_reported":int(pollination_present),
              "marking_text_review_candidate":int(bool(hits)),
              "nectar_guide_presence":"not_measured",
              "uv_guide_presence":"not_measured",
              "visual_information_use_by_pollinator":"not_measured",
              "flower_colour":filled["flower colour"],
              "petal_colour":filled["petal colour"],
              "corolla_colour":filled["corolla colour"],
              "flower_symmetry":filled["flower symmetry"],
              "flower_shape":filled["flower shape"],
              "flower_architecture":filled["flower architecture"],
              "corolla_tube_lipped":filled["corolla tube lipped"],
              "pollination_text":filled["pollination"],
              "source_doi":SOURCE_DOI
            })
        if len(rows)!=expected_rows:
            raise ValueError("NO_GO_NHM_SOURCE_ROW_COUNT_CHANGED")
        return rows,patterns,{
            "status":"SOURCE_VERIFIED_59369_GLOBAL_ANGIOSPERM_FLORAL_TRAIT_COVERAGE",
            "source_doi":SOURCE_DOI,
            "species_rows":len(rows),
            "unique_taxon_strings":len(source_taxa),
            "field_nonempty_counts":dict(sorted(coverage.items())),
            "unconfirmed_marking_candidates":len(patterns),
            "important_NO_GUIDE_FIELD_AVAILABLE_IN_NHM_SOURCE":True,
            "no_missing_trait_as_confirmed_absence":True,
            "no_visual_signal_as_proven_receiver_information_use":True,
            "no_Bombus_occurrences_treated_as_species_richness_or_suitability":True,
            "original_nhm_records_not_committed_or_uploaded_verbatim":True,
        }


def write_csv(path,rows,fieldnames):
    with open(path,"w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fieldnames,extrasaction="raise")
        wr.writeheader()
        wr.writerows(rows)


def main():
    blob,identity=_get_source_bytes()
    records,patterns,stats=summarize_and_extract(blob)
    stats["original_download"]=identity
    folder=Path("stage45_species_registry")
    folder.mkdir(parents=True,exist_ok=True)
    # Derived normalized registry (CC BY source attribution in every row).
    write_csv(folder/"nhm_59369_visual_trait_species_registry.csv",
              records,list(records[0]))
    write_csv(folder/"visible_marking_text_review_candidates.csv",
              patterns,list(patterns[0]) if patterns else [
                 "taxon","wfo","observed_colour_text","search_tokens",
                 "review_status","uv_guide_status","source_doi"])
    (folder/"nhm_trait_coverage.json").write_text(
        json.dumps(stats,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE45_NHM_REAL_TRAIT_COVERAGE",json.dumps(stats,sort_keys=True))
    print("STAGE45_FIRST_15_MARKING_REVIEW_TAXA",
          json.dumps([x["taxon"] for x in patterns[:15]],ensure_ascii=False))
    print("NO_CONFIRMED_UV_GUIDES_NO_BOMBUS_RANGE_MODEL_NO_CAUSAL_FIT")


if __name__=="__main__":
    main()
