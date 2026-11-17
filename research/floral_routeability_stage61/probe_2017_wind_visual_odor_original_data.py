"""Stage61: source-original Lawson/Whitney/Rands 2017 windy odor/visual backup.

Paper DOI 10.1098/rsos.170996, PMCID PMC5717666. Original public
supplement reported as rsos170996supp2.xlsx and Dryad DOI
10.5061/dryad.3g591. This work searches EuropePMC OA ORIGINAL package,
not retyping already published effects as independent new evidence.

The published wind experiment had FOUR arms, 18 bees each:
  calm odor-only, wind odor-only, wind odor+colour, wind colour-only.
Critically NOT a fully crossed wind(2) x odor(2) x colour(2) design:
the relevant no-wind colour and no-wind mixed arms do not exist.
Paper reports learning/choice endpoints, not randomized first-cue
conditional next-action policies or real plant pollen fitness.

Reading an XLSX source sheet doesn't prove a wind-triggered cognitive
information routing effect; raw source columns must be audited first.
"""
from __future__ import annotations
import hashlib,io,json,zipfile,urllib.error,urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

PAPER="10.1098/rsos.170996"
DATA="10.5061/dryad.3g591"
PMC="PMC5717666"
SOURCE=f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMC}/supplementaryFiles"
MAX_ZIP=14_000_000
MAX_MEMBER=5_000_000
M="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

def get_source():
    req=urllib.request.Request(SOURCE,headers={
       "Accept":"application/zip,application/octet-stream,*/*",
       "User-Agent":"adaptive-gain-stage61-source-original-windy-visual-odor-backup/2026"})
    with urllib.request.urlopen(req,timeout=65) as res:
        body=res.read(MAX_ZIP+1)
    if len(body)>MAX_ZIP or not zipfile.is_zipfile(io.BytesIO(body)):
        raise ValueError("NO_GO_ORIGINAL_2017_BACKUP_EPMC_OA_ZIP_NOT_AVAILABLE")
    return body

def workbook_schema(data):
    if not zipfile.is_zipfile(io.BytesIO(data)):
        raise ValueError("NO_GO_ORIGINAL_BACKUP_SUPPLEMENT_NOT_XLSX_ZIP")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=z.namelist()
        if "xl/workbook.xml" not in names:
            raise ValueError("NO_GO_SOURCE_BACKUP_NOT_XLSX_WORKBOOK")
        book=ET.fromstring(z.read("xl/workbook.xml"))
        sheets=[s.attrib.get("name","") for s in book.iter(M+"sheet")]
        all_strings=[]
        if "xl/sharedStrings.xml" in names:
            root=ET.fromstring(z.read("xl/sharedStrings.xml"))
            all_strings=["".join((t.text or "") for t in si.iter(M+"t"))
                         for si in root.iter(M+"si")]
        sheet_summary=[]
        for name in sorted(s for s in names if s.startswith("xl/worksheets/sheet") and s.endswith(".xml")):
            if z.getinfo(name).file_size>8_000_000:
                raise ValueError("NO_GO_ORIGINAL_BACKUP_WORKSHEET_XML_TOO_LARGE")
            root=ET.fromstring(z.read(name))
            dim=next(root.iter(M+"dimension"),None)
            schema=[]
            row_count=0
            nonempty=0
            for r in root.iter(M+"row"):
                row_count+=1
                if row_count>10:break
                vals=[]
                for cell in r.findall(M+"c"):
                    v=cell.find(M+"v")
                    if cell.attrib.get("t")=="s" and v is not None:
                        k=int(v.text)
                        if not 0<=k<len(all_strings):
                            raise ValueError("NO_GO_2017_XLSX_SHARED_STRING_OOB")
                        x=all_strings[k]
                    elif cell.attrib.get("t")=="inlineStr":
                        x="".join((t.text or "") for t in cell.iter(M+"t"))
                    elif v is not None:x=v.text or ""
                    else:x=""
                    if x.strip():
                        nonempty+=1
                        vals.append(x[:120])
                    if len(vals)>=20:break
                schema.append(vals)
            sheet_summary.append({
              "source_xlsx_internal_path":name,
              "declared_range_or_unknown":dim.attrib.get("ref","") if dim is not None else "",
              "sheet_XML_uncompressed_bytes":z.getinfo(name).file_size,
              "first_10_source_row_schema_only":schema,
              "preview_nonempty_cells":nonempty,
              "no_2017_trial_cue_order_inferred_from_header_only":True,
            })
    return {"status":"SOURCE_AUTHENTIC_2017_XLSX_SUPPLEMENT_SCHEMA_ONLY",
            "source_inner_SHA256":hashlib.sha256(data).hexdigest(),
            "source_workbook_sheet_names":sheets,
            "source_worksheets":sheet_summary,
            "original_2017_individual_trial_rows_not_yet_reconstructed":True}

def inspect_archive(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError("NO_GO_NOT_AUTHOR_PUBLIC_EUROPE_PMC_ZIP")
    records=[]
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for m in z.infolist():
            if m.is_dir() or "__MACOSX" in m.filename:continue
            name=Path(m.filename).name
            data=None
            rec={"source_archive_member_name":name,
                 "member_length_bytes":m.file_size,
                 "source_document_extension":Path(name).suffix.lower()}
            if m.file_size<=MAX_MEMBER and name.lower().endswith(".xlsx"):
                data=z.read(m)
                rec["source_workbook"]=workbook_schema(data)
            elif m.file_size<=MAX_MEMBER:
                data=z.read(m)
                rec["source_member_SHA256"]=hashlib.sha256(data).hexdigest()
                rec["status"]="ORIGINAL_NON_XLSX_SOURCE_NOT_A_TRIAL"
            else:
                rec["status"]="SOURCE_FILE_LARGE_NOT_READ"
            records.append(rec)
    return {
      "status":"ORIGINAL_LAWSON_2017_BACKUP_SOURCE_SUPPLEMENT_MANIFEST",
      "published_paper_DOI":PAPER,
      "published_original_Dryad_dataset":DATA,
      "europe_PMC":PMC,
      "source_archive_sha256":hashlib.sha256(blob).hexdigest(),
      "number_original_supplement_members":len(records),
      "source_files":records,
      "number_detected_xlsx_members":sum(r["source_document_extension"]==".xlsx" for r in records),
      "2017_wind_four_arms_n18_each_not_complete_three_way_factorial":True,
      "published_wind_no_calm_multimodal_or_calm_visual_control":True,
      "no_conditional_first_cue_policy_or_pollen_deposition_label_inferred":True,
      "existing_visual_backup_wind_result_NOT_NEW_FLORAL_FINDING":True,
    }

def main():
    out=Path("stage61_2017_wind_visual_odor_backup_original_source")
    out.mkdir(exist_ok=True)
    try:
        report=inspect_archive(get_source())
    except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
            TimeoutError,zipfile.BadZipFile,ET.ParseError) as exc:
        report={
          "status":"LAWSON_2017_ORIGINAL_SOURCE_NOT_RETRIEVED_NO_DATA_CLAIM",
          "published_paper_DOI":PAPER,
          "published_original_Dryad_dataset":DATA,
          "error_type":type(exc).__name__,
          "error_message":str(exc)[:200],
        }
    (out/"original_2017_Lawson_wind_scent_visual_backup_source_ledger.json").write_text(
       json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",
       encoding="utf8")
    print("STAGE61_LAWSON_2017_ORIGINAL_WIND_VISUAL_ODOR_BACKUP_SOURCE",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("NO_ROUTE_POLICY_BEYOND_EXISTING_MULTIMODAL_BACKUP")
if __name__=="__main__":
    main()
