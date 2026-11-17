"""Stage67 public Dryad original 2025/2026 rival receiver and visitation data.

Evidence acquisition, not survey of photographed flowers. Fetch the official
Dryad API dataset metadata and version-listed file metadata. We do NOT infer
individual species count from presence of '98' spectra columns/65 population
repeats or generically call bird-vs-bee syndrome a realized visitation count.
Preserve actual dataset DOI, requested archived original version and file IDs.
"""
from __future__ import annotations
import argparse,hashlib,json,re,urllib.parse,urllib.request,urllib.error
from pathlib import Path

ROOT="https://datadryad.org/api/v2"
TARGETS={
  "Xie2025_flower_spectral_41_islands_and_bee_visits":"10.5061/dryad.612jm64gq",
  "Coetzee2026_Erica_64_species_receiver_contrast_nectar_robbing":"10.5061/dryad.6djh9w1gz",
  "BadenBohm2022_FloRes_flower_phenology_nectar_pollen_tube":"10.5061/dryad.djh9w0w29",
}
MAX_META=2_000_000
MAX_VERSION_PAGES=4
APPROVED_FILE_NAMES={
 "Xie2025_flower_spectral_41_islands_and_bee_visits":{
  "flower_color_reflectance_spectra.xlsx",
  "bee_visitation_frequency_to_each_floral_color_within_each_island.xlsx",
  "plant_bee_interactions_on_islands.zip","README.md"},
 "Coetzee2026_Erica_64_species_receiver_contrast_nectar_robbing":{
   "Data_Is_bee-avoidance_driven_by_nectar_robbing__Data_Dryad_20Jan2026.xlsx",
   "Erica.population.spectra.1.csv","README.md"},
 "BadenBohm2022_FloRes_flower_phenology_nectar_pollen_tube":{
   "Data.zip","README.docx","Attachments.zip"}
}
def check(x,reason):
    if not x:raise ValueError("ORIGINAL_DRYAD_MACRO_SOURCE_METADATA_NO_GO_"+reason)
def safe_get(endpoint,opener=urllib.request.urlopen):
    check(endpoint.startswith(ROOT+"/"),"NONOFFICIAL_PUBLIC_DRYAD_API")
    req=urllib.request.Request(endpoint,headers={"Accept":"application/json",
       "User-Agent":"adaptive-gain-stage67-independent-original-floral-primary-data/2026"})
    with opener(req,timeout=40) as res: b=res.read(MAX_META+1)
    check(len(b)<=MAX_META,"SOURCE_METADATA_TOO_BIG")
    return json.loads(b)
def audit(typ,doi):
    u=ROOT+"/datasets/"+urllib.parse.quote("doi:"+doi,safe="")
    source=safe_get(u)
    # Dryad dataset record has a stable canonical DOI and version references.
    got=str(source.get("identifier") or source.get("doi") or "")
    check(doi in got or doi in json.dumps(source)[:4000],
          "DATASET_DOI_DISAGREES_WITH_REQUEST")
    out={"query_DOI":doi,"dataset_API":u,
         "metadata_title":str(source.get("title") or "")[:250],
         "license":source.get("license"),
         "metadata_harvested_not_species_trait_estimate":True,
         "original_experimental_design_from_landing_page_not_auto_extracted":True,
         "dataset_keys":sorted(source),
         "link_relations":sorted((source.get("_links") or {}))}
    versions_url=u+"/versions"
    versions=safe_get(versions_url)
    out["source_versions_URL"]=versions_url
    out["versions_payload_keys"]=sorted(versions)
    collections=versions.get("_embedded") or {}
    out["versions_collection_keys"]=sorted(collections)
    allvers=[]
    for key,vals in collections.items():
        if isinstance(vals,list):
            allvers.extend(v for v in vals if isinstance(v,dict) and v.get("id"))
    # If API versions response schema differs, do not invent a version id.
    if not allvers and isinstance(versions.get("data"),list):
        allvers=[v for v in versions["data"] if isinstance(v,dict) and v.get("id")]
    check(bool(allvers),"CANNOT_RESOLVE_REAL_PUBLIC_DRYAD_VERSION")
    latest=max(allvers,key=lambda v:int(v["id"]))
    ver_id=int(latest["id"])
    files_url=ROOT+"/versions/"+str(ver_id)+"/files"
    files_payload=safe_get(files_url)
    file_collection=[]
    for key,vals in (files_payload.get("_embedded") or {}).items():
        if isinstance(vals,list):
            file_collection.extend(v for v in vals if isinstance(v,dict))
    if not file_collection and isinstance(files_payload.get("data"),list):
        file_collection=files_payload["data"]
    check(bool(file_collection),"CANNOT_RESOLVE_ORIGINAL_FILES")
    out["version_id"]=ver_id
    out["number_original_files"]=len(file_collection)
    out["files"]=[]
    for f in file_collection:
        name=str(f.get("filename") or f.get("path") or f.get("name") or "")
        size=f.get("size") or f.get("filesize") or f.get("sizeBytes")
        links=f.get("_links") or {}
        out["files"].append({
          "filename":name,
          "file_id":f.get("id"),
          "file_size_source_bytes_or_null":size,
          "hash_source_or_unknown":f.get("digest") or f.get("md5") or f.get("sha256"),
          "source_download_link_relations":sorted(links),
          "source_download_URL":(links.get("stash:download") or links.get("download") or {}).get("href"),
          "source_metadata_only_not_downloaded_file":True,
          "candidate_for_next_source_ingestion":name.rsplit("/",1)[-1] in APPROVED_FILE_NAMES[typ]})
    out["n_files_whitelisted_for_ingestion"]=sum(f["candidate_for_next_source_ingestion"] for f in out["files"])
    return out
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",type=Path,default=Path("stage67_authentic_public_Dryad_multisource_ingestion_index"))
    args=ap.parse_args();results={}
    for name,doi in TARGETS.items():
        try:
            out=audit(name,doi)
        except Exception as e:
            out={"query_DOI":doi,"status":"UNAVAILABLE_NOT_NO_SOURCE_FILES",
                 "error_type":type(e).__name__,"error_detail":str(e)[:250]}
        results[name]=out
        print("STAGE67_ORIGINAL_DRYAD_PRIMARY_SOURCES",name,json.dumps({
          "doi":doi,"version":out.get("version_id"),
          "n_files":out.get("number_original_files"),
          "n_approved":out.get("n_files_whitelisted_for_ingestion"),
          "error":out.get("error_detail")
        },sort_keys=True))
    receipt={"schema":"source_only_2022_2025_2026_Dryad_original_dataset_version_files",
        "datasets":results,
        "no_FCP_or_iNaturalist_photographic_traits":True,
        "no_original_spectral_sample_count_claim_from_repository_file_count":True,
        "no_GBIF_pseudo_visitation_or_imputed_UV_spatial_guide":True}
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"official_Dryad_original_versions_and_file_ids.json").write_text(
       json.dumps(receipt,sort_keys=True,ensure_ascii=False,indent=2)+"\n")
    print("STAGE67_REAL_PRIMARY_DRYAD_SOURCE_METADATA_DISCOVERY",
      json.dumps({"n_targets":len(TARGETS),
         "n_versions_resolved":sum(bool(v.get("version_id")) for v in results.values()),
         "n_file_ids_resolved":sum(v.get("number_original_files",0) for v in results.values())},sort_keys=True))
if __name__=="__main__":main()
