"""Stage54: inspect the NESTED original 2025 151-species colour-change table.

The Europe PMC OA ZIP holds an inner supplemental zip
plants-14-02185-s001.zip. Its original SHA256 was obtained from a
successful real-source Action, not guessed.
DO NOT reproduce copyrighted article/supplement text; report a document
schema, tables, sheet names, and brief SOURCE HEADER previews only.
Separately inspect the small original 2015 Ohashi 219-taxa Zenodo README,
and Dryad 51-clade version file metadata. Real trait labels require a
dedicated, independently tested extraction after this inspection.
"""
from __future__ import annotations
import io
import zipfile
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import urllib.error

from probe_multimodal_original_literature import _fetch,_pdf_schema,_xlsx_schema,EUROPE_PMC,ZENODO_API
REVIEW_INNER="plants-14-02185-s001.zip"
PINNED_INNER_SHA="a2af585bdc42cdc6e990c624c4328b808526e259bd21e0bd91fa39b5c316ff28"
DRYAD_VERSION_FILES="https://datadryad.org/api/v2/versions/402189/files"
ZENODO_README=("https://zenodo.org/api/records/4942515/files/"
               "README_for_Ohashi_etal.txt/content")
OHASHI_README_MD5="0c173d6081578a8c45f6a662429d8889"


def _body_docx(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        return {"format":"NOT_DOCX"}
    with zipfile.ZipFile(io.BytesIO(blob)) as f:
        if "word/document.xml" not in f.namelist():
            return {"format":"ZIP_NOT_DOCX"}
        root=ET.fromstring(f.read("word/document.xml"))
        ns={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        tables=root.findall(".//w:tbl",ns)
        tab=[]
        for t in tables[:4]:
            rows=t.findall("w:tr",ns)
            # Only extract original table column headers, not full text table
            first=[]
            for row in rows[:2]:
                first.append([
                    " ".join(x.text or "" for x in col.findall(".//w:t",ns))[:120]
                    for col in row.findall("w:tc",ns)
                ][:24])
            tab.append({"n_rows":len(rows),"first_two_rows_as_schema":first})
        text_nodes=root.findall(".//w:t",ns)
    return {"format":"DOCX","n_tables":len(tables),"table_schemas":tab,
            "n_word_text_runs":len(text_nodes)}


def original_review_nested():
    blob,_=_fetch(EUROPE_PMC)
    with zipfile.ZipFile(io.BytesIO(blob)) as container:
        inner=[r for r in container.namelist()
               if Path(r).name==REVIEW_INNER]
        if len(inner)!=1:
            raise ValueError("NO_GO_ORIGINAL_2025_SUPPLEMENT_NESTED_ZIP_MISSING")
        sub=container.read(inner[0])
    if hashlib.sha256(sub).hexdigest()!=PINNED_INNER_SHA:
        raise ValueError("NO_GO_ORIGINAL_2025_SUPPLEMENT_NESTED_ZIP_HASH_CHANGED")
    if not zipfile.is_zipfile(io.BytesIO(sub)):
        raise ValueError("NO_GO_2025_ORIGINAL_INNER_SUPPLEMENT_NOT_ZIP")
    with zipfile.ZipFile(io.BytesIO(sub)) as doc:
        out=[]
        for m in doc.infolist():
            if m.is_dir():continue
            if m.file_size>8_000_000:
                out.append({"name":m.filename,"status":"TOO_LARGE_FOR_SCHEMA_AUDIT"})
                continue
            data=doc.read(m)
            extension=m.filename.lower()
            if extension.endswith(".xlsx"):
                table=_xlsx_schema(data)
            elif extension.endswith(".docx"):
                table=_body_docx(data)
            elif extension.endswith(".pdf") and data.startswith(b"%PDF"):
                table=_pdf_schema(data)
            elif extension.endswith((".csv",".tsv",".txt")):
                lines=data.decode("utf8",errors="replace").splitlines()
                table={"format":"TEXT","n_lines":len(lines),
                       "source_header_preview":[x[:120] for x in lines[:2]]}
            else:table={"format":"OTHER"}
            out.append({"name":m.filename,
                        "original_bytes":len(data),
                        "source_member_sha256":hashlib.sha256(data).hexdigest(),
                        "table_structure":table})
    return {"status":"AUTHENTIC_2025_COLOUR_CHANGE_151_SUPPLEMENT_NESTED_SCHEMA",
            "doi":"10.3390/plants14142185",
            "original_outer_zip_sha256":hashlib.sha256(blob).hexdigest(),
            "original_inner_zip_sha256":PINNED_INNER_SHA,
            "source_files":out,
            "species_positive_count_151_from_review_not_extracted_in_this_step":True,
            "no_absent_species_inferred_from_review_list":True}


def original_ohashi_small_readme():
    # Original Zenodo evidence, do not try to cache huge 285MB spectra ZIP
    import urllib.request
    req=urllib.request.Request(ZENODO_README,headers={
        "Accept":"text/plain,*/*",
        "User-Agent":"adaptive-gain-2015-Ohashi-spectral-data-reference/2026"})
    with urllib.request.urlopen(req,timeout=40) as res:
        content=res.read(10_000)
    if hashlib.md5(content).hexdigest()!=OHASHI_README_MD5:
        raise ValueError("NO_GO_OHASHI_219_ORIGINAL_ZENODO_README_HASH")
    lines=content.decode("utf8",errors="replace").splitlines()
    return {"status":"AUTHENTIC_OHASHI_219_AGE_SPECTRA_ARCHIVE_README",
            "source_DOI":"10.5061/dryad.8fh42",
            "real_Zenodo_file_MD5":OHASHI_README_MD5,
            "n_readme_lines":len(lines),
            "first_32_reference_lines":[l[:240] for l in lines[:32]],
            "not_species_change_phenotype_yet":True}


def dryad_version_index():
    import urllib.request
    req=urllib.request.Request(DRYAD_VERSION_FILES,headers={
        "Accept":"application/json",
        "User-Agent":"adaptive-gain-2025-51-plant-colour-clades-source/2026"})
    with urllib.request.urlopen(req,timeout=35) as res:
        raw=res.read(400_000)
    body=json.loads(raw)
    files=((body.get("_embedded") or {}).get("stash:files")
           or body.get("files") or [])
    return {"status":"OFFICIAL_2025_DRYAD_51_CLADE_DATA_FILE_INDEX",
            "dataset_doi":"10.5061/dryad.r4xgxd2sc",
            "version_id":402189,
            "index_keys":list(body),
            "n_files_in_index":len(files),
            "file_metadata":[{"id":x.get("id"),"path":x.get("path"),
                              "name":x.get("filename"),
                              "bytes":x.get("size"),
                              "sha256":x.get("digest"),
                              "links":x.get("_links")}
                             for x in files[:14]],
            "no_colour_or_guides_inferred_from_file_metadata":True}


def main():
    report={"status":"ORIGINAL_MULTI_MODAL_SPECIES_TABLE_ARCHIVE_STRUCTURE",
            "sources":{}}
    for key,callback in (
       ("2025_color_change_151",original_review_nested),
       ("2015_Ohashi_219",original_ohashi_small_readme),
       ("2025_color_51clades",dryad_version_index)):
        try:
            report["sources"][key]=callback()
        except (ValueError,urllib.error.URLError,urllib.error.HTTPError,
                TimeoutError,zipfile.BadZipFile,ET.ParseError,
                KeyError,json.JSONDecodeError) as e:
            report["sources"][key]={"status":"NOT_VERIFIED_NO_SPECIES_RECORD",
                                   "error_kind":type(e).__name__,
                                   "error":str(e)[:250]}
    folder=Path("stage54_source_nested_tables")
    folder.mkdir(exist_ok=True)
    (folder/"actual_151_219_51_source_table_schemas.json").write_text(
      json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
      encoding="utf8")
    print("STAGE54_ORIGINAL_MULTI_MODAL_NESTED_SOURCE_TABLES",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("NO_PHYLOGENETIC_NEGATIVE_OR_VISUAL_GUIDE_STATE_INFERRED_FROM_MISSING_SOURCE")

if __name__=="__main__":
    main()
