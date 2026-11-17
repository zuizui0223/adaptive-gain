"""Stage72: original public data access & measurement-grain audit, NEVER photo-derived traits.

Kantsa 2018 Mediterranean: same field community, true floral spectra/scent/
visitation source files (Figshare + Nature supplementary). 
Albor et al. 2022: 39 species Californian source field optical + pollinator sharing.
Xie et al. 2025: 98 taxa source spectrometer, 41 islands+16 mainland localities
in ONE reservoir system, not 57 evolutionarily independent regions.

This stage logs only actual bytes retrieved from ORIGINAL source services.
A publisher statement or dataset abstract is NOT a downloaded original file.
No inferred UV nectar-guide negatives, trait-guild coefficient or causal SEM.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import posixpath
import re
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path

SOURCE_DATE = "2026-11-17"
USER_AGENT="adaptive-gain-stage72-original-field-trait-source-audit/2026-11-17"
BYTE_MAX=28_000_000
ATTEMPTS=2
FIGSHARE_ARTICLE_ID=5663455
FIGSHARE_METADATA="https://api.figshare.com/v2/articles/5663455"
PUBLISHER_DATA = {
  "kantsa_2018_network_original_supplement_xlsx":
  "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-018-03448-w/MediaObjects/41467_2018_3448_MOESM4_ESM.xlsx",
  "kantsa_2018_scent_original_supplement_xlsx":
  "https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-018-03448-w/MediaObjects/41467_2018_3448_MOESM5_ESM.xlsx",
}
DRYAD_IDS={
 "xie_2025_island_field_spectra_bees":"10.5061/dryad.612jm64gq",
 "albor_2022_california_field_spectra_guild":"10.5061/dryad.2ngf1vhrb",
}
ATTRIBUTIONS={
 "kantsa_2018":{"doi":"10.1038/s41467-018-03448-w","region":"one Lesvos Greece field community",
    "source_reported_plants":41,"source_reported_visits":7955,
    "important_novelty_limit":"original paper already tested scent,color,abundance,phenology,phylogeny"},
 "xie_2025":{"doi":"10.1016/j.biocon.2025.111322",
    "region":"one China Thousand Island Lake archipelago and adjacent mainland",
    "source_reported_sites_islands":41,"source_reported_mainland_sites":16,
    "source_reported_spectral_plant_columns":98},
 "albor_2022":{"doi":"10.1111/1365-2435.14142",
    "region":"one California serpentine seep coflowering community",
    "source_reported_plants":39,"field_spectral_wavelength_min_nm":340,
    "important_novelty_limit":"original publication already tested colour/phenology/pollinator sharing"}
}
NS={"s":"http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p":"http://schemas.openxmlformats.org/package/2006/relationships"}

def download_bytes(url, limit=BYTE_MAX):
    if not url.startswith("https://"):
        raise ValueError("STAGE72_ONLY_HTTPS_ORIGINAL_AUTHOR_PUBLISHER_ARCHIVES")
    error=None
    for t in range(ATTEMPTS):
        req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,
             "Accept":"application/json,application/octet-stream,*/*"})
        try:
            with urllib.request.urlopen(req,timeout=35) as response:
                data=response.read(limit+1)
                final=response.geturl()
            if len(data)>limit: raise ValueError("STAGE72_ORIGINAL_BINARY_EXCEEDS_BOUND")
            return data,final
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            error=exc
            if t+1<ATTEMPTS:time.sleep(0.35)
    raise error

def source_receipt(name,source_url,body,final=None):
    return {"source_id":name, "source_url":source_url,
        "final_url_host_path":re.sub(r"^https?://","",str(final or source_url)).split("?")[0][:250],
        "status":"ORIGINAL_SOURCE_BYTES_RETRIEVED",
        "byte_count":len(body),"original_source_sha256":hashlib.sha256(body).hexdigest(),
        "no_inferred_plant_species_or_visits":True}

def failed_receipt(name,url,err):
    status=(
        "SOURCE_OAUTH_REQUIRED_401" if isinstance(err,urllib.error.HTTPError) and err.code==401
        else "SOURCE_ACCESS_FORBIDDEN_403" if isinstance(err,urllib.error.HTTPError) and err.code==403
        else "SOURCE_NOT_FOUND_404" if isinstance(err,urllib.error.HTTPError) and err.code==404
        else "SOURCE_OTHER_HTTP_FAILURE" if isinstance(err,urllib.error.HTTPError)
        else "SOURCE_NOT_RETRIEVED_ERROR"
    )
    return {"source_id":name, "source_url":url, "status":status,
            "exception_type":type(err).__name__,
            "http_code":getattr(err,"code",None),
            "no_inferred_plant_species_or_visits":True}

def xlsx_workbook_metadata(raw):
    # Reads OOXML structure using stdlib ZIP/XML, NOT guessed sheet counts.
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("STAGE72_XLSX_CONTENT_NOT_ZIP")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=set(z.namelist())
        if "xl/workbook.xml" not in names:
            raise ValueError("STAGE72_XLSX_NO_WORKBOOK")
        root=ET.fromstring(z.read("xl/workbook.xml"))
        sheets=root.find("s:sheets",NS)
        if sheets is None:raise ValueError("STAGE72_XLSX_NO_SHEETS")
        shared=[]
        if "xl/sharedStrings.xml" in names:
            share=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for node in share.findall("s:si",NS):
                shared.append("".join((t.text or "") for t in node.findall(".//s:t",NS)))
        rel_lookup={}
        if "xl/_rels/workbook.xml.rels" in names:
            rr=ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
            for r in rr.findall("p:Relationship",NS):
                target=r.attrib["Target"].lstrip("/")
                if not target.startswith("xl/"):target=posixpath.normpath("xl/"+target)
                rel_lookup[r.attrib["Id"]]=target
        summaries=[]
        for i,sheet in enumerate(sheets.findall("s:sheet",NS),start=1):
            sheet_name=sheet.get("name","")
            rid=sheet.get("{"+NS["r"]+"}id","")
            entry=rel_lookup.get(rid,f"xl/worksheets/sheet{i}.xml")
            if entry not in names:
                summaries.append({"sheet_name":sheet_name,"source_entry":"NOT_PRESENT",
                                  "original_xml_accessible":False})
                continue
            xml=ET.fromstring(z.read(entry))
            dimension=xml.find("s:dimension",NS)
            sd=xml.find("s:sheetData",NS)
            sheet_rows=sd.findall("s:row",NS) if sd is not None else []
            count=0;sample=[]
            for row in sheet_rows:
                nonempty=0; preview=[]
                for cell in row.findall("s:c",NS):
                    t=cell.get("t")
                    v=cell.find("s:v",NS)
                    inline=cell.find("s:is",NS)
                    value=(v.text or "") if v is not None else ""
                    if t=="s" and value:
                        ix=int(value);value=shared[ix] if ix<len(shared) else ""
                    elif inline is not None:
                        value="".join((z.text or "") for z in inline.findall(".//s:t",NS))
                    if value.strip():
                        nonempty+=1
                        if len(preview)<9:preview.append(value[:90])
                if nonempty:count+=1
                if len(sample)<3 and preview:sample.append(preview)
            summaries.append({
                "sheet_name":sheet_name,"original_xml_accessible":True,
                "source_xml_entry":entry,"source_dimension_text":dimension.get("ref") if dimension is not None else "",
                "source_nonempty_record_rows_in_sheet":count,
                "preview_first_three_nonempty_rows_first9cells":sample
            })
    return summaries

def figshare_inventory():
    payload,url=download_bytes(FIGSHARE_METADATA,limit=2_000_000)
    meta=json.loads(payload)
    if not isinstance(meta,dict) or str(meta.get("id"))!=str(FIGSHARE_ARTICLE_ID):
        raise ValueError("STAGE72_FIGSHARE_ARTICLE_ID_MISMATCH")
    files=meta.get("files") or []
    return meta,files,source_receipt("kantsa2018_figshare_author_article_metadata",FIGSHARE_METADATA,payload,url)

def dryad_inventory(doi):
    import urllib.parse
    urls=[
      "https://datadryad.org/api/v2/datasets/doi%3A"+urllib.parse.quote(doi,safe=""),
      "https://api.datadryad.org/api/v2/datasets/doi%3A"+urllib.parse.quote(doi,safe=""),
    ]
    last_error=None;tried=[]
    for uri in urls:
        try:
            raw,url=download_bytes(uri,limit=2_000_000)
            data=json.loads(raw)
            if not isinstance(data,dict):raise ValueError("STAGE72_DRYAD_API_NOT_JSON_OBJECT")
            return data,source_receipt("dryad_metadata_"+doi,uri,raw,url),tried
        except Exception as e:
            tried.append(failed_receipt("dryad_metadata_"+doi,uri,e))
            last_error=e
    return None,None,tried

def dataset_files(data):
    # Treat _links as pointers only and never invent file IDs or official hashes.
    paths=[]
    for v in (data.get("_links") or {}).values():
        if isinstance(v,dict) and str(v.get("href","")).startswith("https://"):
            paths.append(v["href"])
    if isinstance(data.get("files"),list):
        for f in data["files"]:
            if isinstance(f,dict):
                for key in ("download_url","downloadUrl","download"):
                    if str(f.get(key,"")).startswith("https://"):paths.append(f[key])
    return sorted(set(paths))

def process_file(name, original_url, raw, outdir, max_preview=3):
    info=source_receipt(name,original_url,raw)
    # A publisher/CDN may return HTTP 200 HTML to a nominal .xlsx URL.
    # That response is NOT an original workbook and must not count as data.
    expects_xlsx=(name.lower().endswith(".xlsx") or name.endswith("_xlsx"))
    if expects_xlsx:
        if not zipfile.is_zipfile(io.BytesIO(raw)):
            info["status"]="SOURCE_HTTP200_NOT_GENUINE_XLSX"
            info["original_XLSX_source_identity_verified"]=False
            return info
        with zipfile.ZipFile(io.BytesIO(raw)) as test_archive:
            if "xl/workbook.xml" not in test_archive.namelist():
                info["status"]="SOURCE_ZIP_NOT_GENUINE_XLSX"
                info["original_XLSX_source_identity_verified"]=False
                return info
        info["original_XLSX_source_identity_verified"]=True
    if raw.startswith(b"PK\x03\x04") and zipfile.is_zipfile(io.BytesIO(raw)):
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                entries=[{"name":x.filename,"uncompressed_bytes":x.file_size}
                         for x in z.infolist() if not x.is_dir()]
            info["archive_members_first25"]=entries[:25]
            info["archive_member_count"]=len(entries)
            if "xl/workbook.xml" in {x["name"] for x in entries}:
                info["xlsx_sheets"]=xlsx_workbook_metadata(raw)
        except (ValueError,ET.ParseError,KeyError) as exc:
            info["structured_parse_status"]=f"ORIGINAL_BYTES_DOWNLOADED_BUT_SCHEMA_ERROR_{type(exc).__name__}"
    elif raw.startswith(b"<?xml") or raw.startswith(b"<"):
        info["structured_parse_status"]="ORIGINAL_BYTES_NOT_XLSX"
    elif raw[:2] == b"\x1f\x8b":
        info["structured_parse_status"]="GZIP_SOURCE_REQUIRES_SEPARATE_SEMANTICS"
    else:
        info["structured_parse_status"]="SOURCE_BINARY_OR_TEXT_NOT_AUTOMATICALLY_TRAIT_SCORED"
    return info

def run(outdir):
    receipts=[];search_summary={}
    for name,url in PUBLISHER_DATA.items():
        try:
            raw,location=download_bytes(url)
            receipts.append(process_file(name,url,raw,outdir))
        except Exception as e:
            receipts.append(failed_receipt(name,url,e))
    try:
        metadata,files,rec=figshare_inventory()
        receipts.append(rec)
        search_summary["figshare_original_article_id"]=FIGSHARE_ARTICLE_ID
        search_summary["figshare_original_file_name_size_checksum_inventory"]=[
            {"name":f.get("name"),"size":f.get("size"),"md5":f.get("supplied_md5") or f.get("computed_md5"),
             "id":f.get("id")} for f in files if isinstance(f,dict)
        ]
        for f in files:
            if not isinstance(f,dict):continue
            name=str(f.get("name") or "")
            url=str(f.get("download_url") or "")
            if not url.startswith("https://") or len(receipts)>18:continue
            if int(f.get("size") or 0)>BYTE_MAX:
                receipts.append({"source_id":"figshare_"+name,"status":"SOURCE_FILE_SIZE_ABOVE_BOUND",
                                 "source_declared_bytes":f.get("size")})
                continue
            try:
                raw,location=download_bytes(url)
                receipts.append(process_file("figshare_"+name,url,raw,outdir))
            except Exception as e:
                receipts.append(failed_receipt("figshare_"+name,url,e))
    except Exception as e:
        receipts.append(failed_receipt("kantsa2018_figshare_article_metadata",FIGSHARE_METADATA,e))
    for dataset,doi in DRYAD_IDS.items():
        data,receipt,tried=dryad_inventory(doi)
        receipts+=tried
        if data is None:continue
        receipts.append(receipt)
        summary={
           "original_dataset_DOI":doi,
           "original_metadata_version":data.get("versionNumber") or data.get("version"),
           "original_title":data.get("title"),
           "source_API_file_link_objects_not_parsed_as_data":True,
           "original_data_urls":dataset_files(data)[:12]
        }
        search_summary[dataset]=summary
    report={
      "schema":"stage72_authentic_original_primary_site_sensory_visitor_sources_only",
      "date":SOURCE_DATE,
      "original_source_candidate_regions":["Lesvos Greece","California USA","Zhejiang China"],
      "number_of_candidate_independent_geographic_study_regions":3,
      "geographically_independent_communities_not_raw_site_counts":True,
      "original_source_published_design_background_not_this_source_extraction":ATTRIBUTIONS,
      "source_receipts":receipts,
      "source_inventories":search_summary,
      "n_original_source_content_files_retrieved":len({
            r["original_source_sha256"] for r in receipts
            if r.get("status")=="ORIGINAL_SOURCE_BYTES_RETRIEVED"
            and r.get("source_id","")!="kantsa2018_figshare_author_article_metadata"
            and not r.get("source_id","").startswith("dryad_metadata_")}),
      "n_original_source_file_fetch_occurrences_including_SHA_duplicates":sum(
            r.get("status")=="ORIGINAL_SOURCE_BYTES_RETRIEVED"
            and r.get("source_id","")!="kantsa2018_figshare_author_article_metadata"
            and not r.get("source_id","").startswith("dryad_metadata_")
            for r in receipts),
      "http200_nonworkbook_never_counted_as_original_XLSX":True,
      "n_actual_species_site_visitor_x_spectral_effects_extracted":0,
      "original_field_site_meteorological_wind_and_VOC_jointly_matched":False,
      "published_source_sample_sizes_are_NOT_recomputed_data_points":True,
      "no_photo_derived_trait_or_UV_guide_negative":True,
      "no_global_optical_effect_claimed":True,
    }
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    a.outdir.mkdir(parents=True,exist_ok=True)
    report=run(a.outdir)
    (a.outdir/"stage72_original_public_sources_access_and_workbook_schema.json").write_text(
        json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE72_ORIGINAL_FIELD_SENSORY_VISITOR_SOURCE_ACCESS_RECEIPT",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("ORIGINAL_ACCESS_INVENTORY_NO_IMPUTED_GUILDS_NO_UNVERIFIED_CROSS_STUDY_ORIGIN")
if __name__=="__main__":main()
