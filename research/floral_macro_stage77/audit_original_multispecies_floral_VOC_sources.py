"""Stage77C: primary 2020 multispecies floral scent source availability/overlap.

Farré-Armengol et al. 2020, Front Plant Sci DOI 10.3389/fpls.2020.01154
published 305 plant species across 66 families/851 VOCs, 58 input
studies. Exact original downloadable supplementary material is required
before treating any source species as measured. The original authors
already analyzed climate+pollinator+VOC associations: PRIOR ART.

Purpose: audit whether a 305-species chemical dataset could be joined
(with documented SOURCE POPULATION mismatch) to 963 NHM×EuPPollNet real
plant names and 233 positively recorded one-hue lexical species.

No photos. No inference of absent fragrance from unmeasured VOC. No
false same-site/visit-year linkage. No new global causal VOC mediation.
"""
from __future__ import annotations
import argparse,csv,hashlib,html,io,json,re,tarfile,urllib.parse,urllib.request,urllib.error,xml.etree.ElementTree as ET,zipfile
from collections import Counter,defaultdict
from pathlib import Path

ARTICLE="10.3389/fpls.2020.01154"
PMCID="PMC7412988"
FRONTIERS="https://www.frontiersin.org/journals/plant-science/articles/"+ARTICLE+"/full"
EPMC_XML="https://www.ebi.ac.uk/europepmc/webservices/rest/"+PMCID+"/fullTextXML"
EPMC_SUPP="https://www.ebi.ac.uk/europepmc/webservices/rest/"+PMCID+"/supplementaryFiles"
PMC_OA="https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id="+PMCID
HOSTS={"www.frontiersin.org","public-pages-files-2025.frontiersin.org",
       "www.ebi.ac.uk","www.ncbi.nlm.nih.gov","ftp.ncbi.nlm.nih.gov",
       "pmc.ncbi.nlm.nih.gov"}
MAX_ARCHIVE=50000000
MAX_WEB=5000000
SOURCE_PUBLISHED_NOT_RECALCULATED={"plants":305,"families":66,
    "VOC_compounds":851,"source_studies":58}
HUED_NHM_SHA="b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a"
EUPP_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"

def source_get(uri,cap=MAX_ARCHIVE):
    url=urllib.parse.urlparse(uri)
    if url.scheme!="https" or url.netloc not in HOSTS:
        raise ValueError("STAGE77C_NON_AUTHORITATIVE_SCIENTIFIC_SOURCE_URL")
    req=urllib.request.Request(uri,headers={
        "User-Agent":"adaptive-gain-original-floral-scent-source-audit/2026-11-18",
        "Accept":"text/html,application/xml,application/zip,application/octet-stream,*/*"})
    with urllib.request.urlopen(req,timeout=60) as response:
        raw=response.read(cap+1)
        final=response.geturl()
        mime=response.headers.get("Content-Type","")
    if not raw or len(raw)>cap:
        raise ValueError("STAGE77C_SCIENTIFIC_SOURCE_EMPTY_OR_SIZE_OVER")
    return raw,final,mime

def failure(where,e):
    return {"source":where,"status":"NOT_RETRIEVED_NOT_BIOLOGICAL_ABSENCE",
      "error_class":type(e).__name__,"http_status":getattr(e,"code",None)}

def checksum(b):
    return hashlib.sha256(b).hexdigest()

def original_supp_links(raw):
    text=raw.decode("utf-8",errors="replace")
    # Open-source publisher HTML source is the sole authority for generated
    # file URLs. Do not invent article IDs or spray guessed URLs.
    found=[]
    for m in re.finditer(r'''(?:href|src)\s*=\s*["']([^"'<>]+)["']''',text,re.I):
        href=html.unescape(m.group(1))
        url=urllib.parse.urljoin(FRONTIERS,href)
        u=urllib.parse.urlparse(url)
        if u.netloc not in HOSTS or u.scheme!="https":continue
        if re.search(r'(?:supplement|/files/Articles/|\.zip(?:\?|$)|\.xlsx?(?:\?|$)|\.csv(?:\?|$)|\.docx(?:\?|$)|s00\d)',url,re.I):
            if url not in found:
                found.append(url)
    return found

def archive_inventory(raw,name):
    result={"source_original_biological_numeric_data_admitted":False,
      "source_archive_format":"NOT_RECOGNIZED",
      "original_supplement_members":[]}
    if zipfile.is_zipfile(io.BytesIO(raw)):
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            files=[f for f in z.infolist() if not f.is_dir()]
            result.update(source_archive_format="ZIP",
                original_supplement_members=[{"path":f.filename,"bytes":f.file_size}
                     for f in files[:45]])
            result["n_original_archive_files"]=len(files)
            result["n_actual_original_spreadsheets"]=sum(f.filename.lower().endswith((".xlsx",".xls",".csv")) for f in files)
            result["source_original_biological_numeric_data_admitted"]=bool(result["n_actual_original_spreadsheets"])
    elif raw[:2]==b"\x1f\x8b":
        try:
            with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as tar:
                files=[m for m in tar.getmembers() if m.isfile()]
            result.update(source_archive_format="TARGZ",
                original_supplement_members=[{"path":m.name,"bytes":m.size}
                    for m in files[:45]])
            result["n_original_archive_files"]=len(files)
            result["n_actual_original_spreadsheets"]=sum(m.name.lower().endswith((".xlsx",".xls",".csv")) for m in files)
            result["source_original_biological_numeric_data_admitted"]=bool(result["n_actual_original_spreadsheets"])
        except tarfile.TarError:
            result["source_archive_format"]="GZIP_NOT_PARSABLE_TARGZ"
    elif raw.startswith(b"PK\x03\x04"):
        result["source_archive_format"]="ZIP_NOT_PARSABLE"
    elif raw.lstrip()[:6].lower().startswith((b"<html",b"<!doct")):
        result["source_archive_format"]="HTTP200_HTML_NOT_SOURCE_BINARY"
    else:
        result["source_archive_format"]="NON_ARCHIVE_BINARY_OR_XML"
    return result

def lookup_source_accepted_taxa(nhm_path,eu_path):
    for p,sha in ((nhm_path,HUED_NHM_SHA),(eu_path,EUPP_SHA)):
        if checksum(p.read_bytes())!=sha:
            raise ValueError("STAGE77C_ORIGINAL_963_PLANT_NAME_ARTIFACT_SHA_NOT_VERIFIED")
    with eu_path.open(newline="",encoding="utf-8") as f:
        source=list(csv.DictReader(f))
    eu={r["Original_plant_accepted_name_literal"].casefold().strip() for r in source}
    if len(eu)!=1408:raise ValueError("STAGE77C_EUPP_ORIGINAL_1408_NAME_DENOMINATOR_CHANGED")
    nhm=set();mono=set()
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage75"))
    from authentic_continental_text_signal_guild_macro import source_text_trait
    with nhm_path.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        for row in reader:
            name=row["taxon"].casefold().strip()
            if name not in eu:continue
            nhm.add(name)
            if source_text_trait(row)["source_exclusive_lexical_hue"]:
                mono.add(name)
    if len(nhm)!=963 or len(mono)!=233:
        raise ValueError("STAGE77C_NHM_963_OR_233_SOURCE_LABELS_CHANGED")
    return eu,nhm,mono

def source_study_file_record():
    results=[]
    # First try official machine-readable Europe PMC package (no guessed
    # Frontiers article ID, no scraping private data).
    for url,cap in ((EPMC_SUPP,MAX_ARCHIVE),(EPMC_XML,MAX_WEB),(PMC_OA,MAX_WEB),(FRONTIERS,MAX_WEB)):
        try:
            raw,final,mime=source_get(url,cap)
            d={"source_url":url,"actual_source_bytes":len(raw),
              "original_downloaded_source_sha256":checksum(raw),
              "original_retrieved_mime":mime,
              "source_status":"PUBLIC_SOURCE_BYTES_RETRIEVED"}
            if url==EPMC_SUPP:
                d.update(archive_inventory(raw,"europepmc_original_supplementZIP"))
            elif url==FRONTIERS:
                direct=original_supp_links(raw)
                d["original_article_disclosed_supplement_links"]=direct[:60]
                d["original_source_HTML_links_without_binary_not_a_dataset"]=True
            elif url==EPMC_XML:
                txt=raw.decode("utf-8",errors="replace")
                d["original_fulltext_supplement_element_count"]=txt.count("<supplementary-material")
                d["original_FullText_source_PMCID_present"]=PMCID in txt
                d["fulltext_xml_is_NOT_raw_VOC_compound_matrix"]=True
            else:
                try:
                    root=ET.fromstring(raw)
                    links=[
                      z.attrib.get("href","") for z in root.findall(".//link")
                      if z.attrib.get("format") in ("tgz","tar.gz")]
                    d["original_official_OA_package_urls"]=links[:6]
                    d["PMC_source_archive_not_automatically_downloaded"]=True
                except ET.ParseError:d["source_XML_valid"]=False
            results.append(d)
        except Exception as ex:
            results.append(failure(url,ex))
    return results

def run(nhm,eu):
    e,n,mono=lookup_source_accepted_taxa(nhm,eu)
    resources=source_study_file_record()
    return {
       "schema":"stage77c_original_305species_floral_VOC_crosssource_availability_feasibility",
       "source_original_review_article_DOI":ARTICLE,
       "source_original_review_PMCID":PMCID,
       "source_author_reported_VOC_corpus_NOT_reanalysed":SOURCE_PUBLISHED_NOT_RECALCULATED,
       "source_study_review_analyzed_climate_and_pollinator_effects_ALREADY_PRIOR_ART":True,
       "source_original_EuPP_accepted_plant_names":len(e),
       "source_original_exact_botanical_description_names":len(n),
       "source_original_visual_single_explicit_hue_names":len(mono),
       "source_actual_original_primary_VOC_archive_access_receipts":resources,
       "source_real_compounds_per_matched_plant_EXTRACTED":False,
       "real_same_site_scent_versus_Bombus_visits_join_verified":False,
       "wind_driven_scent_plume_mediation_identified":False,
       "source_missing_VOC_is_unknown_not_zero_scent":True,
       "source_original_UV_guide_phenotype_not_imputed":True,
       "data_screen_not_repeat_2020_climate_VOC_hypothesis_as_novelty":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-NHM",type=Path,required=True)
    p.add_argument("--source-EuPP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    a.outdir.mkdir(exist_ok=True,parents=True)
    d=run(a.source_NHM,a.source_EuPP)
    (a.outdir/"original_2020_305species_VOC_public_archive_access_receipt.json").write_text(
       json.dumps(d,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE77C_ORIGINAL_MULTI_SPECIES_VOC_MACRO_DATA_ACCESS_GATE",
          json.dumps(d,sort_keys=True,ensure_ascii=False))
    print("NO_IMPUTED_VOC_PATH_NO_REPEAT_PREVIOUS_VOC_CLIMATE_FINDING")
if __name__=="__main__":
    main()
