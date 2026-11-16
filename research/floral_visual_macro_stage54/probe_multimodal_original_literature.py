"""Stage54: ORIGINAL multi-modal floral signal literature source discovery.

The aim is a cross-modality species atlas, NOT cumulative effect sizes:
- original 2016/2021 spatial UV image phenotypes from Stage49 (230 species);
- original 2015 Ohashi et al 219 species across floral age and bee/fly/
  butterfly colour vision; 101 source study species with detectable
  change to some pollinator types, including *real measured negatives*.
- 2025 review of 151 whole-flower colour-changing species, a non-independent
  literature-derived positive compendium, not a 151-species random sample.
- 2025 Dryad 51 clades with explicit floral hue and independent phylogenies:
  colour only (neither nectar guide nor "no signal" by default).

This program inspects genuine source metadata and file schemas. Failure to
download is NOT a plant trait value or false zero. No user images or raw
copyrighted supplemental tables are redistributed, only evidence receipts.
"""
from __future__ import annotations
import hashlib
import io
import json
import csv
from pathlib import Path
import urllib.request
import urllib.error
import zipfile
import xml.etree.ElementTree as ET

EUROPE_PMC="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12299958/supplementaryFiles"
ZENODO_API="https://zenodo.org/api/records/4942515"
DRYAD_API=("https://datadryad.org/api/v2/datasets/"
           "doi%3A10.5061%2Fdryad.r4xgxd2sc")
WILEY_TABLE=("https://besjournals.onlinelibrary.wiley.com/doi/suppl/"
             "10.1111/1365-2435.12420/supinfo/"
             "fec12420-sup-0005-TableS1a.pdf")
URLS={"2025_review_151_supplement":EUROPE_PMC,
      "2015_Ohashi_219_Zenodo_metadata":ZENODO_API,
      "2025_51clade_Dryad_metadata":DRYAD_API,
      "2015_Ohashi_219_Wiley_S1_a":WILEY_TABLE}
SOURCE_DOIS={
    "2025_review_151_supplement":"10.3390/plants14142185",
    "2015_Ohashi_219_Zenodo_metadata":"10.1111/1365-2435.12420",
    "2025_51clade_Dryad_metadata":"10.5061/dryad.r4xgxd2sc",
    "2015_Ohashi_219_Wiley_S1_a":"10.1111/1365-2435.12420",
}
MAX_DOWNLOAD=35_000_000


def _fetch(url,maxbytes=MAX_DOWNLOAD):
    allowed=("https://www.ebi.ac.uk/europepmc/",
             "https://zenodo.org/api/records/",
             "https://datadryad.org/api/v2/datasets/",
             "https://besjournals.onlinelibrary.wiley.com/doi/suppl/")
    if not any(url.startswith(p) for p in allowed):
        raise ValueError("NO_GO_UNTRUSTED_VISUAL_TRAIT_SOURCE_URL")
    req=urllib.request.Request(url,headers={
        "Accept":"application/json,application/zip,application/pdf,*/*",
        "User-Agent":"adaptive-gain-floral-multimodal-source-audit/2026",
    })
    with urllib.request.urlopen(req,timeout=45) as response:
        raw=response.read(maxbytes+1)
        mime=response.headers.get("Content-Type","")
    if len(raw)>maxbytes:
        raise ValueError("NO_GO_VISUAL_TRAIT_SOURCE_TOO_LARGE")
    return raw,mime


def _xlsx_schema(data):
    if not zipfile.is_zipfile(io.BytesIO(data)):
        return {"format":"NOT_XLSX_ZIP"}
    ns={"x":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        if "xl/workbook.xml" not in z.namelist():
            return {"format":"ZIP_NOT_XLSX"}
        book=ET.fromstring(z.read("xl/workbook.xml"))
        names=[s.attrib.get("name") for s in book.findall("x:sheets/x:sheet",ns)]
        sheets=[{"file":x.filename,"uncompressed_bytes":x.file_size}
                for x in z.infolist()
                if x.filename.startswith("xl/worksheets/") and x.filename.endswith(".xml")]
    return {"format":"XLSX","sheet_names":names,"worksheet_sizes":sheets[:25]}


def _pdf_schema(data):
    import fitz
    with fitz.open(stream=data,filetype="pdf") as pdf:
        n_pages=len(pdf)
        table_pages=[]
        for i,page in enumerate(pdf):
            t=page.get_text("text")
            if any(word in t.lower() for word in (
                "supplementary table","table s1","species","flower","colour change")):
                table_pages.append({
                  "page_1_based":i+1,
                  "text_chars":len(t),
                  "mentions_table_S1":("Table S1" in t),
                  "first_160_characters":t[:160].replace("\n"," "),
                })
    return {"format":"PDF","pages":n_pages,
            "possible_species_table_pages":table_pages[:20]}


def _supplement_entry(raw):
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("NO_GO_ORIGINAL_EUROPEPMC_SUPPLEMENT_NOT_ZIP")
    out=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for item in z.infolist():
            if item.is_dir():continue
            n=Path(item.filename).name
            if item.file_size>24_000_000:
                out.append({"file":n,"original_uncompressed_bytes":item.file_size,
                            "status":"SKIPPED_TOO_LARGE"})
                continue
            b=z.read(item)
            info={"file":n,"original_uncompressed_bytes":len(b),
                  "member_sha256":hashlib.sha256(b).hexdigest()}
            try:
                if b.startswith(b"%PDF-"):
                    info["table_schema"]=_pdf_schema(b)
                elif n.lower().endswith(".xlsx"):
                    info["table_schema"]=_xlsx_schema(b)
                elif n.lower().endswith((".csv",".tsv",".txt")):
                    sample=b.decode("utf-8-sig",errors="replace").splitlines()
                    info["table_schema"]={"format":"TEXT",
                        "first_2_lines":[s[:200] for s in sample[:2]],
                        "total_lines":len(sample)}
                else:info["table_schema"]={"format":"OTHER"}
            except Exception as err:
                info["table_parse_error"]=type(err).__name__
            out.append(info)
    return {"zip_container_sha256":hashlib.sha256(raw).hexdigest(),
            "source_supplement_members":out,
            "any_species_table_supplement":any(
                ("species" in x["file"].lower() or
                 "s001" in x["file"].lower() or "table" in x["file"].lower())
                for x in out)}


def _summarize_json_source(raw,kind):
    o=json.loads(raw)
    if not isinstance(o,dict):
        raise ValueError("NO_GO_ORIGINAL_ARCHIVE_METADATA_NOT_OBJECT")
    if kind=="2015_Ohashi_219_Zenodo_metadata":
        return {"format":"ZENODO_V2_METADATA",
                "record_id":o.get("id"),
                "files":[{"name":x.get("key"),"bytes":x.get("size"),
                          "checksum":x.get("checksum"),
                          "url":(x.get("links") or {}).get("self")}
                         for x in o.get("files",[])],
                "no_285MB_zip_download_here":True}
    return {"format":"DRYAD_DATASET_METADATA",
            "top_keys":list(o)[:30],
            "dataset_id":o.get("id"),
            "version_link":(o.get("_links") or {}).get("stash:version"),
            "files_link":(o.get("_links") or {}).get("stash:files"),
            "doi":o.get("identifier") or o.get("doi")}


def probe():
    result={"status":"SOURCE_FIRST_MULTI_MODAL_FLOWER_VISUAL_TRAIT_DISCOVERY",
            "sources":{},"never_sum_publication_record_denominators":True,
            "unverified_signals_never_marked_absent":True}
    for source,url in URLS.items():
        e={"source_DOI":SOURCE_DOIS[source],"source_URL":url}
        try:
            raw,ctype=_fetch(url)
            e.update({"access":"SOURCE_BYTES_RETRIEVED",
                      "content_type":ctype,"original_download_bytes":len(raw),
                      "sha256":hashlib.sha256(raw).hexdigest()})
            if source=="2025_review_151_supplement":
                e.update(_supplement_entry(raw))
            elif source.endswith("metadata"):
                e.update(_summarize_json_source(raw,source))
            elif raw.startswith(b"%PDF-"):
                e.update(_pdf_schema(raw))
            else:
                e["access"]="NOT_AUTHENTIC_PDF_SOURCE_NO_219_TRAIT_LABELS"
        except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
                TimeoutError,zipfile.BadZipFile,ET.ParseError,
                json.JSONDecodeError) as exc:
            e={"source_DOI":SOURCE_DOIS[source],"source_URL":url,
               "access":"UNAVAILABLE_NOT_NEGATIVE_TRAIT",
               "error_type":type(exc).__name__,"error":str(exc)[:220]}
        result["sources"][source]=e
    return result


def main():
    report=probe()
    out=Path("stage54_multimodal_source_receipts")
    out.mkdir(exist_ok=True)
    (out/"2025_2015_51clades_original_supplement_manifest.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",
        encoding="utf-8")
    print("STAGE54_VISUAL_SIGNAL_SOURCE_ACCESS_MANIFEST",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("NO_SPECIES_LEVEL_COLOUR_CHANGE_GUESSED_FROM_METADATA")


if __name__=="__main__":
    main()
