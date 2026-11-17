"""Stage58 — audit original published cross-species floral VOC source tables.

Source original Farré-Armengol et al. 2020 (Frontiers Plant Sci),
DOI 10.3389/fpls.2020.01154, PMCID PMC7412988.
Published scent source-frame: 305 species, 851 compounds and
climate/pollination group annotations, with 58 underlying studies.
This is a SECONDARY multi-study source, not 305 new independent
genetic experiments nor a validated floral VOC for 817 accepted visual
taxa. Locate tables and inspect schema first; never label missing
VOC evidence as a scentless flower.
"""
from __future__ import annotations
from collections import Counter
import hashlib,io,json,urllib.request,urllib.error,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

PAPER_DOI="10.3389/fpls.2020.01154"
PMC_ID="PMC7412988"
URL=f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMC_ID}/supplementaryFiles"
MAX_ARCHIVE=20_000_000
MAX_MEMBER=5_000_000

def unpack_original_source(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError("NO_GO_2020_VOC_SOURCE_SUPPLEMENT_NOT_ZIP")
    original=[]
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for meta in z.infolist():
            if meta.is_dir() or "__MACOSX" in meta.filename:
                continue
            name=Path(meta.filename).name
            record={"original_member_name":name,
                    "uncompressed_bytes":meta.file_size,
                    "original_member_extension":Path(name).suffix.lower()}
            if meta.file_size>MAX_MEMBER:
                record["status"]="ORIGINAL_MEMBER_TOO_LARGE_NOT_READ"
                original.append(record);continue
            content=z.read(meta)
            record["sha256"]=hashlib.sha256(content).hexdigest()
            lower=name.lower()
            if lower.endswith((".csv",".tsv",".txt")):
                data=content.decode("utf8-sig",errors="replace").splitlines()
                record.update({"status":"TEXT_SOURCE_HEADER_AUDIT_ONLY",
                    "source_line_count":len(data),
                    "first_2_lines_source_schema":[q[:180] for q in data[:2]]})
            elif lower.endswith(".xlsx"):
                with zipfile.ZipFile(io.BytesIO(content)) as wb:
                    n=wb.namelist()
                    xml_sheets=[q for q in n if q.startswith("xl/worksheets/")
                        and q.endswith(".xml")]
                    record.update({"status":"XLSX_SOURCE_WORKBOOK_SCHEMA_ONLY",
                        "source_worksheet_xml_count":len(xml_sheets),
                        "source_worksheet_byte_sizes":[wb.getinfo(q).file_size for q in xml_sheets[:15]]})
            elif lower.endswith((".docx",".doc")):
                record.update({"status":"WORD_SOURCE_MEMBER_IDENTIFIED_NOT_SPECIES_EXTRACTED"})
            elif lower.endswith(".pdf"):
                record.update({"status":"PDF_SOURCE_MEMBER_IDENTIFIED_NOT_SPECIES_EXTRACTED"})
            else:
                record.update({"status":"OTHER_SOURCE_MEMBER_NOT_TRAIT_ABSENCE"})
            original.append(record)
    return {"status":"ORIGINAL_VOC_305_SOURCE_SUPPLEMENT_MANIFEST_ONLY",
            "original_archive_sha256":hashlib.sha256(blob).hexdigest(),
            "n_original_source_supplement_members":len(original),
            "original_members":original,
            "source_paper_305_species_not_yet_imported":True,
            "source_paper_851_VOC_names_not_independently_row_audited":True,
            "source_reported_58_primary_studies_not_new_independent_2026_experiments":True,
            "source_odour_unknown_not_absent":True,
            "source_climate_guild_and_species_raw_join_not_verified":True}

def main():
    receipt={"source_doi":PAPER_DOI,
             "source_url":URL,
             "expected_published_VOC_plant_species":305,
             "expected_published_VOC_compounds":851,
             "expected_published_underlying_studies":58}
    try:
        req=urllib.request.Request(URL,headers={
           "Accept":"application/zip,application/octet-stream,*/*",
           "User-Agent":"adaptive-gain-stage58-original-floral-VOC305-supplement/2026"})
        with urllib.request.urlopen(req,timeout=55) as res:
            raw=res.read(MAX_ARCHIVE+1)
        if len(raw)>MAX_ARCHIVE:
            raise ValueError("NO_GO_ORIGINAL_VOC_SUPPLEMENT_TOO_LARGE")
        receipt.update(unpack_original_source(raw))
    except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
            TimeoutError,zipfile.BadZipFile,ET.ParseError) as e:
        receipt.update({"status":"VOC_ORIGINAL_SUPPLEMENT_UNAVAILABLE_UNKNOWN_NOT_SCENTLESS",
                        "error_type":type(e).__name__,
                        "error_context":str(e)[:190]})
    out=Path("stage58_original_305_scent_source")
    out.mkdir(exist_ok=True)
    (out/"FArmegnol2020_305_VOC_species_original_source_manifest.json").write_text(
       json.dumps(receipt,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf8")
    print("STAGE58_ORIGINAL_FLORAL_SCENT_305_SOURCE_MANIFEST",
          json.dumps(receipt,sort_keys=True,ensure_ascii=False))
    print("NO_SCENT_OR_NO_SCENT_LABELS_OR_VOC_817_ACCEPTED_SPECIES_JOIN_CLAIMED")

if __name__=="__main__":
    main()
