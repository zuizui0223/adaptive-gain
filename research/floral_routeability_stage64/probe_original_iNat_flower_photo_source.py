"""Stage64: prospectively frozen original iNaturalist flower PHOTO metadata audit.

NOT a new measured nectar-guide atlas and NOT a replay of the exact FCP
source 100 photos/taxon. Stage60 verified genuine FCP-4475 per-species
photo opportunity; Stage64 queries the official original iNaturalist
API for *fresh* photographic records of 4 source-selected taxa.

Those 4 taxa were pre-selected *before inspecting new photos* from
Stage60's 80 VOC/FCP names: the two NHM visible marking TEXT leads with
>=40 historical FCP coarse-color-classifiable photos (Dianthus
deltoides, D. barbatus) and two other high-photo source opportunities
(Helichrysum stoechas, Antirrhinum majus) as UNLABELLED comparators.
NHM textual lead is not positive guide, and comparator is not negative.

Only source observation IDs, photo IDs, exact returned photo URLs,
image copyright licence, month, and pseudonymized user identity are
saved. Do not rehost bytes, do not save precise GPS or observer name.
Choose at most one original photo per observation and per observer.
No UV-spectral state can ever be inferred from RGB photos.
"""
from __future__ import annotations
from collections import Counter
from datetime import date
import argparse,csv,hashlib,json,urllib.error,urllib.parse,urllib.request
from pathlib import Path

API="https://api.inaturalist.org/v1/observations"
TIME="2026-11-17"
FCP_TARGETS=(
  ("Dianthus deltoides",76647,82,"NHM_VISIBLE_MARKING_TEXT_LEAD_NOT_MEASURED"),
  ("Dianthus barbatus",60015,71,"NHM_VISIBLE_MARKING_TEXT_LEAD_NOT_MEASURED"),
  ("Helichrysum stoechas",82641,81,"SOURCE_PHOTO_CONTROL_UNLABELED"),
  ("Antirrhinum majus",48969,66,"SOURCE_PHOTO_CONTROL_UNLABELED"),
)
MAX_ITEMS_API=50
MAX_BYTES=12_000_000  # bounded first-page JSON: large iNaturalist identification arrays can exceed 2.5MB
MAX_PER_TAXON=8
ACCEPT_PHOTO_LICENSE={"cc0","cc-by","cc-by-sa"}
SOURCE_ONLY_DOMAINS={
  "inaturalist-open-data.s3.amazonaws.com",
  "static.inaturalist.org",
  "www.inaturalist.org",
  "inaturalist.org",
}

def original_url(taxon_id):
    if type(taxon_id) is not int or taxon_id<1:
        raise ValueError("NO_GO_SOURCE_INAT_TAXON_ID")
    params=urllib.parse.urlencode({
       "taxon_id":taxon_id,"quality_grade":"research",
       "captive":"false","photos":"true","per_page":MAX_ITEMS_API,
       "order_by":"id","order":"desc"})
    return API+"?"+params

def get_source(id,opener=urllib.request.urlopen):
    u=original_url(id)
    req=urllib.request.Request(u,headers={
       "User-Agent":"adaptive-gain-stage64-authentic-inaturalist-visual-mark-review/2026",
       "Accept":"application/json"})
    with opener(req,timeout=50) as r:
        url=r.geturl()
        if urllib.parse.urlparse(url).hostname!="api.inaturalist.org":
            raise ValueError("NO_GO_ORIGINAL_INAT_API_UNVERIFIED_REDIRECT")
        raw=r.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:raise ValueError("NO_GO_INAT_SOURCE_JSON_TOO_LARGE")
    return json.loads(raw),hashlib.sha256(raw).hexdigest()

def verified_photo_url(raw):
    if not isinstance(raw,str) or len(raw)>500 or not raw.startswith("https://"):
        return ""
    parsed=urllib.parse.urlsplit(raw)
    if (parsed.hostname not in SOURCE_ONLY_DOMAINS
        or parsed.username is not None or parsed.password is not None
        or parsed.query):
        return ""
    return raw

def source_sample(payload,taxon_id,taxon_name,tier):
    results=payload.get("results")
    if not isinstance(results,list) or len(results)>MAX_ITEMS_API:
        raise ValueError("NO_GO_SOURCE_INAT_RESPONSE_RESULTS_SCHEMA")
    total=payload.get("total_results")
    if not isinstance(total,int) or total<0:
        raise ValueError("NO_GO_SOURCE_INAT_RESULT_COUNT_SCHEMA")
    eligible=[]
    seen_observer=set()
    seen_observation=set()
    seen_photo=set()
    counters=Counter()
    for record in results:
        counters["api_original_observations"]+=1
        if not isinstance(record,dict):
            counters["malformed_observation"]+=1;continue
        tax=record.get("taxon") or {}
        if tax.get("id")!=taxon_id:
            counters["not_exact_original_taxon"]+=1;continue
        if record.get("quality_grade")!="research":
            counters["not_research_grade"]+=1;continue
        if record.get("captive") is True:
            counters["source_captive_record"]+=1;continue
        oid=record.get("id")
        owner=(record.get("user") or {}).get("id")
        if not isinstance(oid,int) or not isinstance(owner,int) or owner<1:
            counters["missing_unique_observation_user_id"]+=1;continue
        if oid in seen_observation:
            counters["duplicate_observation"]+=1;continue
        if owner in seen_observer:
            counters["second_photo_same_observer"]+=1;continue
        photos=record.get("photos") or []
        photo=None
        for candidate in photos:
            if not isinstance(candidate,dict):continue
            code=str(candidate.get("license_code") or "").lower()
            url=verified_photo_url(candidate.get("url"))
            pid=candidate.get("id")
            if code in ACCEPT_PHOTO_LICENSE and url and isinstance(pid,int) and pid>0:
                photo=(pid,url,code,candidate.get("attribution",""))
                break
        if photo is None:
            counters["no_approved_licensed_photo_URL"]+=1;continue
        pid,purl,code,attrib=photo
        if pid in seen_photo:
            counters["duplicate_photo_id"]+=1;continue
        month=str(record.get("observed_on") or "")[:7]
        if month and (len(month)!=7 or not month[:4].isdigit() or not month[5:].isdigit()):
            month=""
        eligible.append({
           "source_original_iNat_species":taxon_name,
           "source_original_inat_taxon_id":taxon_id,
           "original_fcp_classifiable_photo_opportunity":next(x[2] for x in FCP_TARGETS if x[1]==taxon_id),
           "source_text_review_tier_not_a_verified_guide":tier,
           "fresh_2026_original_iNaturalist_photo_id":pid,
           "fresh_2026_original_iNaturalist_observation_id":oid,
           "original_photo_url_as_source_returned":purl,
           "original_photo_licence_code":code,
           "source_photo_attribution_as_returned":str(attrib)[:200],
           "original_observer_stable_hash_for_QC_only":hashlib.sha256(("stage64-observer|"+str(owner)).encode()).hexdigest()[:16],
           "original_observation_month_or_unknown":month,
           "photo_is_open_flower_verified":"UNKNOWN_UNREAD_IMAGE",
           "real_visible_intrapetal_guide_state":"UNKNOWN_UNREAD_IMAGE",
           "UV_spatial_pattern_state":"UNKNOWN_NOT_MEASURED_BY_RGB",
           "photo_image_pixels_downloaded":False,
           "this_is_NEW_iNat_photo_sample_not_same_FCP_original_photo_IDs":True,
           "not_a_pollinator_VOC_or_wind_association":True,
        })
        seen_observation.add(oid)
        seen_observer.add(owner)
        seen_photo.add(pid)
        if len(eligible)>=MAX_PER_TAXON:break
    return eligible,{
       "source_total_observations_api_original_query_or_unknown":total,
       "actual_approved_source_image_metadata_selected":len(eligible),
       "first_50_original_observations_audited":len(results),
       "source_exclusion_counts":dict(sorted(counters.items())),
       "license_allowlist":sorted(ACCEPT_PHOTO_LICENSE),
       "distinct_original_observer_stable_hashes":len(seen_observer),
       "no_photo_pixels_yet":True,
    }

def validate_source_candidates(stage60):
    if len(stage60)!=80:raise ValueError("NO_GO_SOURCE_STAGE60_ORIGINAL_80_SPECIES_FRAME")
    rows={r["source_original_VOC_binomial"]:r for r in stage60}
    for name,tid,n,tier in FCP_TARGETS:
        r=rows.get(name)
        if (r is None or int(r["original_FCP_inat_taxon_id"])!=tid
            or int(r["original_FCP_coarse_colour_classifiable_photos"])!=n
            or n<40):
            raise ValueError("NO_GO_FROZEN_ORIGINAL_VOC_FCP_TAXA_CHANGED")
        expected=r["precommitted_review_tier"]
        if tier.startswith("NHM") and not expected.startswith("A_TEXT"):
            raise ValueError("NO_GO_VISIBLE_TEXT_POSITIVE_REVIEW_SOURCE_WRONG")
        if tier.startswith("SOURCE") and not expected.startswith("B_40"):
            raise ValueError("NO_GO_UNLABELED_PHOTO_CONTROL_SOURCE_WRONG")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--frozen-source-stage60-80",required=True)
    a=p.parse_args()
    with Path(a.frozen_source_stage60_80).open(newline="",encoding="utf8") as f:
        stage60=list(csv.DictReader(f))
    validate_source_candidates(stage60)
    out=Path("stage64_original_iNat_photo_metadata")
    out.mkdir(exist_ok=True)
    receipts={}
    allrows=[]
    for name,tid,n,tier in FCP_TARGETS:
        try:
            data,sha=get_source(tid)
            rows,meta=source_sample(data,tid,name,tier)
            receipts[name]={"status":"LIVE_ORIGINAL_INAT_SOURCE_PHOTO_METADATA",
                           "source_API_SHA256":sha,
                           "source_query_url":original_url(tid),
                           **meta}
            allrows.extend(rows)
        except (ValueError,TimeoutError,urllib.error.HTTPError,urllib.error.URLError,
                json.JSONDecodeError) as exc:
            receipts[name]={"status":"SOURCE_API_UNAVAILABLE_UNKNOWN_NOT_NO_PHOTOS",
                            "error_type":type(exc).__name__,
                            "error_summary":str(exc)[:160],
                            "source_query_url":original_url(tid)}
    if not allrows:
        allrows=[{k:"" for k in ("source_original_iNat_species",
                 "source_original_inat_taxon_id","fresh_2026_original_iNaturalist_photo_id",
                 "fresh_2026_original_iNaturalist_observation_id",
                 "original_photo_url_as_source_returned","photo_is_open_flower_verified",
                 "real_visible_intrapetal_guide_state","UV_spatial_pattern_state")}]
    filename=out/"new_iNat_CC_licensed_four_species_original_photo_review_queue.csv"
    with filename.open("w",newline="",encoding="utf8") as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)
    meta={
       "status":"ORIGINAL_INAT_FOUR_SPECIES_FROZEN_SOURCE_PHOTO_METADATA_PILOT",
       "matched_stage60_VOC_FCP_original_review_species":80,
       "intentionally_selected_original_FCP_taxa":len(FCP_TARGETS),
       "real_iNaturalist_current_new_photo_records":sum(len([r for r in allrows
                  if r.get("source_original_iNat_species")==name]) for name,*_ in FCP_TARGETS),
       "source_sample_result":receipts,
       "not_original_FCP_100_exact_photos_retrieval":True,
       "source_images_not_downloaded":True,
       "not_source_measured_visible_or_UV_guides":True,
       "original_four_species_source_selection_before_photograph_inspection":True,
       "no_COI_or_specimen_VOC_local_source_joins":True,
       "no_wind_scent_visual_behavioral_effect_claim":True,
    }
    (out/"source_four_species_iNat_new_photo_API_verification_receipt.json").write_text(
        json.dumps(meta,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("STAGE64_LIVE_ORIGINAL_INAT_PHOTOGRAPH_SOURCE_METADATA",json.dumps(
        meta,ensure_ascii=False,sort_keys=True))
    print("NO_4_SPECIES_WITH_REAL_GUIDES_ORIGINAL_FCP_IMAGE_IDENTITIES_CLAIM")
if __name__=="__main__":
    main()
