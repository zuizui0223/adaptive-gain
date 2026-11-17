"""Stage57: bounded, source-date-captured Europe PMC floral visual literature discovery.

This is an exhaustive *query-frame* inventory under stated six searches, not
an exhaustive species-level UV atlas, original spectra, or a meta-analysis.
No source abstract body or supplementary copyrighted table is redistributed.
Candidate papers cannot be counted as measured visual-pattern species.
Use structured metadata DOI+title/year and independent duplicate detection.
"""
from __future__ import annotations
from collections import Counter
from datetime import date
import csv,json,re,urllib.error,urllib.parse,urllib.request
from pathlib import Path

API="https://www.ebi.ac.uk/europepmc/webservices/rest/search"
SEARCH_DATE="2026-11-17"
MAX_RESULTS_PER_QUERY=50
TOPICS={
    "measured_UV_pattern":'TITLE_ABS:"UV pattern" AND (TITLE_ABS:"flower" OR TITLE_ABS:"floral")',
    "spatial_nectar_guide":'TITLE_ABS:"nectar guide" AND TITLE_ABS:"flower"',
    "spectral_flower_reflectance":'TITLE_ABS:"floral reflectance"',
    "age_colour_change":'TITLE_ABS:"floral colour change"',
    "visible_color_pattern":'TITLE_ABS:"floral color pattern"',
    "pollinator_vision_visual_signal":'TITLE_ABS:"pollinator" AND TITLE_ABS:"visual signal" AND TITLE_ABS:"flower"',
    "UV_protection_pigment":'TITLE_ABS:"ultraviolet" AND TITLE_ABS:"floral pigmentation"',
    "spectral_visual_contrast":'TITLE_ABS:"flower colour" AND TITLE_ABS:"contrast"',
}
MAX_BYTES=2_800_000

def query_params(q):
    return {"query":f"({q}) AND FIRST_PDATE:[2000-01-01 TO {SEARCH_DATE}]",
            "format":"json","resultType":"core",
            "pageSize":MAX_RESULTS_PER_QUERY,"page":1}

def url_for(q):
    return API+"?"+urllib.parse.urlencode(query_params(q))

def parse_source_payload(topic,json_obj):
    if not isinstance(json_obj,dict) or "resultList" not in json_obj or (
       not isinstance(json_obj["resultList"].get("result"),list)):
        raise ValueError("NO_GO_EUROPE_PMC_SEARCH_SCHEMA")
    rows=json_obj["resultList"]["result"]
    hit=int(json_obj.get("hitCount",0))
    if len(rows)>MAX_RESULTS_PER_QUERY or hit<len(rows):
        raise ValueError("NO_GO_EUROPE_PMC_PAGE_OR_HIT_COUNT_INCONSISTENT")
    out=[]
    for r in rows:
        doi=str(r.get("doi") or "").strip().lower()
        pmid=str(r.get("id") or "").strip()
        if not doi and not pmid:continue
        title=" ".join(str(r.get("title") or "").split())
        year=str(r.get("pubYear") or "")
        if not title or (year and not year.isdigit()):continue
        if len(title)>300:title=title[:300]
        out.append({
           "literature_query_topic":topic,
           "DOI_or_unresolved":doi,
           "Europe_PMC_ID_or_unresolved":pmid,
           "publication_year":year,
           "source_article_title":title,
           "source_authored_article_only_NOT_taxon_UV_state":True,
           "potentially_original_phenotype_measurement_NEEDS_FULLTEXT_AUDIT":True
        })
    return out,{"total_matching_index_count":hit,
                "records_returned_first_page":len(rows),
                "records_with_author_identifiers":len(out),
                "truncated_first_page_not_exhaustive":hit>len(rows)}

def retrieve(topic,query,opener=urllib.request.urlopen):
    url=url_for(query)
    if not url.startswith(API+"?"):raise ValueError("NO_GO_SEARCH_ENDPOINT")
    req=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-stage57-pollinator-visual-trait-source-index/2026",
        "Accept":"application/json"})
    with opener(req,timeout=50) as res:
        raw=res.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:
            raise ValueError("NO_GO_LITERATURE_METADATA_TOO_LARGE")
    rows,receipt=parse_source_payload(topic,json.loads(raw))
    receipt["recorded_query"]=query_params(query)["query"]
    return rows,receipt

def assemble(parsed):
    d={}
    for topic,records in parsed.items():
        for row in records:
            key=row["DOI_or_unresolved"] or "PMID:"+row["Europe_PMC_ID_or_unresolved"]
            if not key or key=="PMID:":continue
            if key not in d:
                d[key]={"DOI_or_unresolved":row["DOI_or_unresolved"],
                        "Europe_PMC_ID_or_unresolved":row["Europe_PMC_ID_or_unresolved"],
                        "publication_year":row["publication_year"],
                        "source_article_title":row["source_article_title"],
                        "query_categories":[]}
            if topic not in d[key]["query_categories"]:
                d[key]["query_categories"].append(topic)
    return sorted(d.values(),key=lambda x:(-(int(x["publication_year"]) if x["publication_year"].isdigit() else 0),x["DOI_or_unresolved"],x["Europe_PMC_ID_or_unresolved"]))

def main():
    report={"status":"CAPPED_SOURCE_ORIGINAL_EUROPEPMC_FLORAL_VISUAL_LITERATURE_DISCOVERY",
            "date_of_query":SEARCH_DATE,
            "n_prespecified_source_queries":len(TOPICS),
            "query_results":{},
            "no_individual_species_UV_phenotype_labels_from_literature_metadata":True,
            "first_page_is_not_exhaustive_if_hitCount_exceeds_50":True}
    found={}
    for topic,query in TOPICS.items():
        try:
            rows,counts=retrieve(topic,query)
            found[topic]=rows
            report["query_results"][topic]={
                "access":"LIVE_EUROPE_PMC_INDEX_METADATA",
                **counts}
        except (ValueError,urllib.error.URLError,urllib.error.HTTPError,
                TimeoutError,json.JSONDecodeError) as err:
            found[topic]=[]
            report["query_results"][topic]={
                "access":"SOURCE_QUERY_UNAVAILABLE_NOT_NO_PUBLICATIONS",
                "error_type":type(err).__name__,
                "error_detail":str(err)[:170]}
    uniq=assemble(found)
    report["n_distinct_doi_or_pmid_candidates_in_bounded_query_frame"]=len(uniq)
    report["n_source_query_success"]=sum(
      x["access"]=="LIVE_EUROPE_PMC_INDEX_METADATA" for x in report["query_results"].values())
    report["candidate_articles_are_not_accepted_plant_species_or_independent_effects"]=True
    out=Path("stage57_systematic_original_source_discovery")
    out.mkdir(exist_ok=True)
    (out/"source_discovery_original_date_query_provenance.json").write_text(
       json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf8")
    path=out/"EuropePMC_visual_trait_papers_bounded_source_metadata.csv"
    with path.open("w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["DOI_or_unresolved",
            "Europe_PMC_ID_or_unresolved","publication_year",
            "source_article_title","query_categories"])
        w.writeheader()
        for r in uniq:
            w.writerow({**r,"query_categories":json.dumps(r["query_categories"])})
    print("STAGE57_FLORAL_VISUAL_LITERATURE_ORIGINAL_INDEX_QUERY",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("NO_STUDY_QUALIFICATION_SPECTRA_UV_PATTERN_OR_BOMBUS_ASSOCIATION_INFERRED")
if __name__=="__main__":
    main()
