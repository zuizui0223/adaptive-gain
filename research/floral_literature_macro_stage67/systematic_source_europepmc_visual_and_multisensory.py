"""Stage67 literature and PUBLIC DATABASE source-only macro discovery.

Searches are reproducibly prespecified Europe PMC title/abstract query frames.
Metadata discovery IS NOT original floral trait extraction and never yields
new species, UV measurements, negative trait states, or effect sizes.
Uses multi-page retrieval; every query reports exact hitCount, ceiling and
failure/truncation, rather than treating first 50 hits as the universe.
No photography, generated visual phenotypes, GBIF proxies or iNat images.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import date
from pathlib import Path
import argparse,csv,json,re,time
import urllib.parse,urllib.request,urllib.error

API="https://www.ebi.ac.uk/europepmc/webservices/rest/search"
FREEZE_DATE="2026-11-17"
FIRST_DATE="2000-01-01"
PAGE_SIZE=100
MAX_PAGES=10
MAX_SOURCE_BYTES=3_500_000
RETRIES=2
# First 8 exact Stage57 query definitions stay unchanged, so source query
# frame can be compared without silently shifting previously searched terms.
SEARCHES={
    "measured_UV_pattern":'TITLE_ABS:"UV pattern" AND (TITLE_ABS:"flower" OR TITLE_ABS:"floral")',
    "spatial_nectar_guide":'TITLE_ABS:"nectar guide" AND TITLE_ABS:"flower"',
    "spectral_flower_reflectance":'TITLE_ABS:"floral reflectance"',
    "age_colour_change":'TITLE_ABS:"floral colour change"',
    "visible_color_pattern":'TITLE_ABS:"floral color pattern"',
    "pollinator_vision_visual_signal":'TITLE_ABS:"pollinator" AND TITLE_ABS:"visual signal" AND TITLE_ABS:"flower"',
    "UV_protection_pigment":'TITLE_ABS:"ultraviolet" AND TITLE_ABS:"floral pigmentation"',
    "spectral_visual_contrast":'TITLE_ABS:"flower colour" AND TITLE_ABS:"contrast"',
    "nectar_guide_general":'TITLE_ABS:"nectar guides"',
    "UV_bullseye":'TITLE_ABS:"bullseye" AND (TITLE_ABS:"flower" OR TITLE_ABS:"floral")',
    "ultraviolet_petal_visual":'TITLE_ABS:"ultraviolet" AND (TITLE_ABS:"petal" OR TITLE_ABS:"corolla")',
    "nectar_guide_orienting_function":'TITLE_ABS:"nectar guide" AND (TITLE_ABS:"learning" OR TITLE_ABS:"orientation")',
    "floral_plant_pattern_visually":'TITLE_ABS:"flower" AND TITLE_ABS:"colour pattern"',
    "floral_multispectral_measurement":'TITLE_ABS:"spectral reflectance" AND TITLE_ABS:"flower"',
    "floral_colour_bee_bird":'TITLE_ABS:"flower colour" AND TITLE_ABS:"bird"',
    "floral_colour_fly_butterfly":'TITLE_ABS:"flower colour" AND (TITLE_ABS:"fly" OR TITLE_ABS:"butterfly")',
    "reward_state_color_change":'TITLE_ABS:"flower color change" AND TITLE_ABS:"pollinator"',
    "floral_scent_multispecies":'TITLE_ABS:"floral scent" AND (TITLE_ABS:"species" OR TITLE_ABS:"dataset")',
    "floral_multimodal_odor_vision":'TITLE_ABS:"floral" AND TITLE_ABS:"scent" AND TITLE_ABS:"visual"',
    "wind_visual_olfactory":'TITLE_ABS:"wind" AND TITLE_ABS:"flower" AND TITLE_ABS:"olfactory"',
    "floral_movement_vision":'TITLE_ABS:"flower movement" AND TITLE_ABS:"bee"',
    "pollination_syndrome_traits":'TITLE_ABS:"pollination syndrome" AND TITLE_ABS:"floral traits"',
    "plant_pollinator_database":'TITLE_ABS:"plant-pollinator" AND TITLE_ABS:"database"',
    "pollinator_flower_network":'TITLE_ABS:"pollination network" AND TITLE_ABS:"flower colour"',
    "floral_thermal_patterns":'TITLE_ABS:"floral temperature" AND TITLE_ABS:"pattern"',
    "floral_resource_database":'TITLE_ABS:"floral resources" AND TITLE_ABS:"database"',
    "floral_iridescence":'TITLE_ABS:"iridescence" AND TITLE_ABS:"flower"',
    "flower_visual_signal_phylogeny":'TITLE_ABS:"flower" AND TITLE_ABS:"colour" AND TITLE_ABS:"phylogeny"'
}
SOURCE_CATEGORIES={
 "visual_direct":["UV","nectar","spectral","colour","color","bullseye","iridescence"],
 "co_modalities":["scent","olfactory","wind","temperature","movement"],
 "guild_ecology":["pollination","pollinator","resource"]
}

def source_query(term):
    return f"({term}) AND FIRST_PDATE:[{FIRST_DATE} TO {FREEZE_DATE}]"

def source_url(term,page):
    args={"query":source_query(term),"format":"json","resultType":"core",
          "pageSize":PAGE_SIZE,"page":page}
    return API+"?"+urllib.parse.urlencode(args)

def fetch_payload(term,page,opener=urllib.request.urlopen):
    url=source_url(term,page)
    if not url.startswith(API+"?"):raise ValueError("UNAUTHENTIC_EUROPE_PMC_ENDPOINT")
    req=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-stage67-systematic-floral-sensory-data-primary-literature/2026",
        "Accept":"application/json"})
    last=None
    for attempt in range(RETRIES+1):
        try:
            with opener(req,timeout=45) as res:
                raw=res.read(MAX_SOURCE_BYTES+1)
            if len(raw)>MAX_SOURCE_BYTES:raise ValueError("EUROPE_PMC_PAGE_EXCEEDED_BYTES")
            result=json.loads(raw)
            if not isinstance(result,dict) or not isinstance(
                    (result.get("resultList") or {}).get("result"),list):
                raise ValueError("EUROPE_PMC_SCHEMA_CHANGED")
            return result
        except (TimeoutError,urllib.error.HTTPError,urllib.error.URLError) as err:
            last=err
            if attempt<RETRIES:
                time.sleep(.5*(2**attempt))
    raise last

def source_row(item,topic):
    # Record only source-index metadata and exact identifier, never infer
    # species label, study design, measured trait, sign or effect size.
    doi=str(item.get("doi") or "").strip().lower()
    doi=re.sub(r"^https?://(?:dx\.)?doi\.org/","",doi)
    pmid=str(item.get("id") or "").strip()
    if not doi and not pmid:return None
    if doi and not doi.startswith("10.") and ":" in doi:return None
    title=" ".join(str(item.get("title") or "").split())
    yr=str(item.get("pubYear") or "")
    if not title or (yr and not re.fullmatch(r"\d{4}",yr)):return None
    return {"doi":doi,"europepmc_id":pmid,
           "year":yr,"title":title[:350],"query_topics":[topic],
           "trait_observation_status":"NOT_READ_FROM_SOURCE_DATA",
           "primary_data_download_status":"NOT_SCREENED",
           "original_species_count_verified_from_this_index":"UNKNOWN"}

def source_topic(name,term,puller=fetch_payload):
    rows={}
    total=None;successful_pages=0
    for page in range(1,MAX_PAGES+1):
        payload=puller(term,page)
        hits=int(payload.get("hitCount",-1))
        original=(payload["resultList"]["result"])
        if hits<0 or len(original)>PAGE_SIZE:
            raise ValueError("EUROPE_PMC_SOURCE_PAGE_INVALID")
        if total is None:total=hits
        if total!=hits:raise ValueError("EUROPE_PMC_HITCOUNT_CHANGED_WITHIN_QUERY")
        successful_pages+=1
        for item in original:
            one=source_row(item,name)
            if one is None:continue
            key=one["doi"] or "PMID:"+one["europepmc_id"]
            rows[key]=one
        # Query is complete only after the full advertised hit count is seen,
        # including incomplete end pages. Exact count of read records is kept.
        if successful_pages*PAGE_SIZE>=hits or len(original)<PAGE_SIZE:break
    scanned_pages=successful_pages
    truncated=(total or 0)>successful_pages*PAGE_SIZE
    return list(rows.values()),{
       "term":term,"complete_source_query":source_query(term),
       "source_index_total_hits":total,
       "pages_downloaded":scanned_pages,"source_page_size":PAGE_SIZE,
       "matched_source_identifiers":len(rows),
       "page_ceiling_truncated":truncated,
       "query_returned_zero_is_not_trait_negative":True}

def aggregate(results):
    byid={}
    for topic,rows in results.items():
        for row in rows:
            key=row["doi"] or "PMID:"+row["europepmc_id"]
            prev=byid.get(key)
            if prev is None:byid[key]={**row,"query_topics":list(row["query_topics"])}
            else:
                prev["query_topics"]=sorted(set(prev["query_topics"]+row["query_topics"]))
    return sorted(byid.values(),key=lambda x:(
       -int(x["year"] or 0),x["doi"],x["europepmc_id"]))

def crawl():
    results={};reports={}
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks={executor.submit(source_topic,name,q):name for name,q in SEARCHES.items()}
        for task in as_completed(tasks):
            topic=tasks[task]
            try:
                rows,source=task.result()
                results[topic]=rows;reports[topic]={"status":"ORIGINAL_EUROPE_PMC_SEARCH_OK",**source}
            except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
                    TimeoutError,json.JSONDecodeError) as e:
                results[topic]=[]
                reports[topic]={"status":"SEARCH_FAILED_UNRESOLVED_NOT_ZERO_HITS",
                                "source_query":source_query(SEARCHES[topic]),
                                "error_type":type(e).__name__,"detail":str(e)[:150]}
    combined=aggregate(results)
    receipt={"schema":"source_only_europe_pmc_original_search_literature_topics_2026_11_17",
       "query_date":FREEZE_DATE,"no_images_or_iNaturalist_in_workflow":True,
       "n_prespecified_query_topics":len(SEARCHES),
       "n_source_queries_ok":sum(r["status"]=="ORIGINAL_EUROPE_PMC_SEARCH_OK" for r in reports.values()),
       "n_source_queries_failed":sum(r["status"]!="ORIGINAL_EUROPE_PMC_SEARCH_OK" for r in reports.values()),
       "n_source_queries_truncated_by_ceiling":sum(r.get("page_ceiling_truncated",False) for r in reports.values()),
       "n_distinct_article_identifiers_not_species":len(combined),
       "n_identified_DOI":sum(bool(x["doi"]) for x in combined),
       "first_8_queries_identical_to_stage57":True,
       "no_abstract_count_misinterpreted_as_measured_plant_trait":True,
       "no_claim_of_exhaustive_all_repositories_or_all_global_papers":True,
       "query_reports":{k:reports[k] for k in SEARCHES}}
    return combined,receipt

def save(rows,receipt,out):
    out.mkdir(parents=True,exist_ok=True)
    (out/"original_EuropePMC_expanded_flower_information_query_receipt.json").write_text(
       json.dumps(receipt,sort_keys=True,ensure_ascii=False,indent=2)+"\n")
    with (out/"expanded_original_flower_sensory_literature_metadata_candidates.csv").open(
        "w",newline="",encoding="utf8") as handle:
        fields=["doi","europepmc_id","year","title","query_topics",
                "trait_observation_status","primary_data_download_status",
                "original_species_count_verified_from_this_index"]
        w=csv.DictWriter(handle,fieldnames=fields);w.writeheader()
        for row in rows:
            w.writerow({**row,"query_topics":json.dumps(row["query_topics"],ensure_ascii=False)})

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="stage67_original_database_literature_inventory")
    args=p.parse_args()
    rows,receipt=crawl()
    save(rows,receipt,Path(args.output))
    print("STAGE67_GENUINE_SOURCE_PAGED_LITERATURE_INVENTORY",json.dumps({
      k:receipt[k] for k in ("n_prespecified_query_topics",
              "n_source_queries_ok","n_source_queries_failed",
              "n_source_queries_truncated_by_ceiling",
              "n_distinct_article_identifiers_not_species")},sort_keys=True))
    print("NO_ABSTRACT_AS_SPECIES_NEGATIVE_NO_UV_VOC_MACRO_EFFECT_FROM_TITLE")
if __name__=="__main__":main()
