"""Stage79A: original source accession for distal-vs-proximal floral visual signals.

PRIMARY macro question: Does *strong wind* change how a bumblebee visitor
community uses distant floral visual extent versus near-field floral colour
change, markings and landing geometry? This source probe is OUTCOME BLIND.
No islands, no image-derived colours. 2015 Ohashi spectral early/late
measurement is a SCREENED 219-species panel, not 219 bee-perceptible positive
changes; Rezende 2025 reviewed 151 POSITIVE literature reports only.

Retrieve the original peer-reviewed Rezende PMC supporting files and the
original author Ohashi Zenodo 4942515 README; identify machine-readable
species tables (not falsely turn a PDF or HTML landing into raw spreadsheet).
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,urllib.error,urllib.parse,urllib.request,zipfile,xml.etree.ElementTree as ET,posixpath
from pathlib import Path
from collections import Counter

REZENDE_DOI="10.3390/plants14142185"
REZENDE_PMID="PMC12299958"
REZENDE_URL="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12299958/supplementaryFiles"
OHASHI_DOI="10.1111/1365-2435.12420"
OHASHI_RECORD="https://zenodo.org/api/records/4942515"
ALLOWED_HOSTS={"www.ebi.ac.uk","zenodo.org","www.zenodo.org",
               "mdpi-res.com","www.mdpi.com"}
ARCHIVE_BOUND=40_000_000
NO_PDF_AUTOPARSE=True
NS={"s":"http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p":"http://schemas.openxmlformats.org/package/2006/relationships"}

def source_sha(b):return hashlib.sha256(b).hexdigest()

def request(url,cap=ARCHIVE_BOUND):
    u=urllib.parse.urlparse(url)
    if u.scheme!="https" or u.hostname not in ALLOWED_HOSTS:
        raise ValueError("STAGE79A_NOT_ALLOWED_ORIGINAL_PUBLISHER_ARCHIVE_HOST")
    req=urllib.request.Request(url,headers={"User-Agent":"adaptive-gain-original-european-floral-distance-macro/2026",
                                            "Accept":"application/json,application/zip,application/octet-stream,*/*"})
    with urllib.request.urlopen(req,timeout=70) as r:
        body=r.read(cap+1);ctype=r.headers.get("Content-Type","");final=r.geturl()
    if not body or len(body)>cap:raise ValueError("STAGE79A_SOURCE_EMPTY_OR_OVERSIZE")
    return body,ctype,final

def failure(url,e):
    return {"source_url":url,"source_status":"ORIGINAL_DATA_NOT_RETRIEVED_NOT_BIOLOGICAL_ABSENCE",
      "source_error_class":type(e).__name__,"http":getattr(e,"code",None)}

def source_xlsx_schema(raw):
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("STAGE79A_ORIGINAL_XLSX_NOT_REAL_OOXML")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=set(z.namelist())
        if "xl/workbook.xml" not in names:
            raise ValueError("STAGE79A_NOT_GENUINE_XLSX_WORKBOOK")
        w=ET.fromstring(z.read("xl/workbook.xml"))
        sheets=w.find("s:sheets",NS)
        shared=[]
        if "xl/sharedStrings.xml" in names:
            s=ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared=["".join((t.text or "") for t in si.findall(".//s:t",NS))
                    for si in s.findall("s:si",NS)]
        rels={}
        if "xl/_rels/workbook.xml.rels" in names:
            for rel in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall("p:Relationship",NS):
                t=rel.attrib.get("Target","").lstrip("/")
                if not t.startswith("xl/"):t=posixpath.normpath("xl/"+t)
                rels[rel.attrib["Id"]]=t
        tables=[]
        for i,sh in enumerate(sheets.findall("s:sheet",NS),start=1):
            target=rels.get(sh.attrib.get("{"+NS["r"]+"}id",""),
                            f"xl/worksheets/sheet{i}.xml")
            if target not in names:continue
            root=ET.fromstring(z.read(target))
            data=root.find("s:sheetData",NS)
            rows=[]
            for row in data.findall("s:row",NS) if data is not None else []:
                values={}
                for cell in row.findall("s:c",NS):
                    x=cell.find("s:v",NS)
                    ins=cell.find("s:is",NS)
                    v=x.text or "" if x is not None else ""
                    if cell.get("t")=="s" and v:
                        ix=int(v);v=shared[ix] if 0<=ix<len(shared) else ""
                    elif ins is not None:
                        v="".join(t.text or "" for t in ins.findall(".//s:t",NS))
                    if v.strip():values[cell.attrib.get("r","?")]=v[:120]
                if values:rows.append(values)
            tables.append({"sheet":sh.get("name"),
                           "n_nonempty_source_rows":len(rows),
                           "source_first_8_rows":[dict(list(r.items())[:16]) for r in rows[:8]],
                           "source_first_row_is_not_automatically_taxon_header":True})
        return tables

def inventory_archive(raw,depth=0):
    if depth>2:return {"status":"ARCHIVE_NESTING_LIMIT"}
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        return {"status":"NOT_AUTHENTIC_ZIP"}
    out=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        files=[x for x in archive.infolist() if not x.is_dir()]
        for file in files:
            name=file.filename
            entry={"original_member_path":name,"original_uncompressed_bytes":file.file_size,
                   "source_original_archive_crc32":file.CRC,
                   "original_member_kind":Path(name).suffix.lower()}
            if file.file_size<20_000_000 and name.lower().endswith((".xlsx",".zip",".csv",".txt",".docx")):
                b=archive.read(file)
                entry["original_member_sha256"]=source_sha(b)
                if name.lower().endswith(".xlsx"):
                    try:entry["original_source_spreadsheet_sheets"]=source_xlsx_schema(b)
                    except (ValueError,ET.ParseError) as exc:
                        entry["original_source_spreadsheet_error"]=type(exc).__name__
                elif name.lower().endswith(".zip"):
                    entry["nested_original_archive"]=inventory_archive(b,depth+1)
                elif name.lower().endswith((".csv",".txt")):
                    try:
                        text=b.decode("utf-8-sig")
                        entry["original_text_first_lines"]=text.splitlines()[:12]
                    except UnicodeDecodeError:entry["status"]="UNKNOWN_ENCODING"
                elif name.lower().endswith(".docx"):
                    entry["original_docx_text_parse_status"]="NOT_EXTRACTED_SOURCE_TYPE_ONLY"
            out.append(entry)
    return {"status":"REAL_AUTHOR_ARCHIVE_MEMBERS_VERIFIED",
            "member_count":len(files),"original_source_members":out[:80]}

def rezende():
    try:
        b,mime,url=request(REZENDE_URL)
        x={"source_url":REZENDE_URL,
           "source_original_bytes":len(b),"source_sha256":source_sha(b),
           "source_mime":mime,"source_status":"ORIGINAL_BYTES_RETRIEVED",
           "original_2025_flower_colour_change_positives_published":151}
        x["source_archive_structure"]=inventory_archive(b)
        return x
    except Exception as exc:return failure(REZENDE_URL,exc)

def ohashi():
    try:
        b,mime,url=request(OHASHI_RECORD,cap=1_500_000)
        j=json.loads(b)
        if str(j.get("id"))!="4942515":
            raise ValueError("STAGE79A_ORIGINAL_OHASHI_ZENODO_SOURCE_RECORD_DIFFERENT")
        f=j.get("files") or []
        inv={"source_status":"ORIGINAL_AUTHOR_RECORD_METADATA_RETRIEVED",
             "source_record_SHA256":source_sha(b),
             "source_original_record_id":4942515,
             "original_2015_SCREENED_species_published":219,
             "original_2015_bee_visually_perceptible_change_published":48,
             "original_source_filenames":[{"name":row.get("key"),"size":row.get("size"),
                "checksum":row.get("checksum"),
                "public_content":(row.get("links") or {}).get("self")}
                for row in f],
             "source_original_README_receipts":[]}
        for f in f:
            if not f.get("key","").casefold().endswith((".txt",".md")):continue
            href=(f.get("links") or {}).get("self") or (f.get("links") or {}).get("content")
            if not href:continue
            try:
                raw,ctype,final=request(href,cap=120_000)
                digest=f.get("checksum","")
                passed=(not digest) or (
                    digest.split(":",1)[-1].casefold()==hashlib.md5(raw).hexdigest()
                    if digest.startswith("md5:") else
                    digest.split(":",1)[-1].casefold()==source_sha(raw))
                inv["source_original_README_receipts"].append({
                    "name":f.get("key"),"bytes":len(raw),"sha256":source_sha(raw),
                    "original_checksum_valid":passed,
                    "first20lines":raw.decode("utf-8-sig",errors="replace").splitlines()[:20]})
            except Exception as exc:
                inv["source_original_README_receipts"].append(failure(href,exc))
        return inv
    except Exception as exc:return failure(OHASHI_RECORD,exc)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args();a.outdir.mkdir(exist_ok=True,parents=True)
    r={"schema":"stage79a_verified_2025_151_positive_colour_change_and_2015_219_screened_spectra_origins",
       "original_sources":{"rezende_2025":rezende(),"ohashi_2015":ohashi()},
       "reviewed_positive_species_not_measured_negative_color_change":True,
       "Ohashi_219_are_screened_not_all_true_colour_changers":True,
       "not_photo_derived_visual_traits":True,
       "no_new_flower_Bombus_strong_gust_effect_fitted":True}
    (a.outdir/"stage79_original_rezende_ohashi_source_inventory.json").write_text(
       json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("STAGE79_ORIGINAL_FLOWER_COLOUR_CHANGE_SOURCES_INVENTORY",
          json.dumps(r,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
