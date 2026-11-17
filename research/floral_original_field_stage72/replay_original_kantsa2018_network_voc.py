"""Stage72B authentic Kantsa et al. (2018) Figshare raw XLSX structural audit.

Original 2018 field community, ONE site/region with 41 published plant species,
168 insect visitors, 403 links, 7,955 visits. Exact source Figshare item
5663455, raw source file IDs & SHA256/MD5 frozen from Stage72 author API
retrieval run 44078684547. Original VOC units ng/g/h. Do not infer
species-independent visits, true plant fitness, or novel color×scent result.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,io,json,posixpath,re,urllib.request,xml.etree.ElementTree as ET,zipfile
from pathlib import Path

SOURCE_FILES={
 "network":{
  "figshare_file_id":10377684,
  "file_name":"Kantsa_etal_Supp_Data1.xlsx",
  "size":33745,
  "sha256":"41d0c650cd9c1e02597aacf0631491615cd5214fa34a1eb18ae51a37c369b7b7",
  "md5":"9a625c56e8528b00fcc556ac0a9798c7",
 },
 "voc":{
  "figshare_file_id":10389468,
  "file_name":"Kantsa_2018_Supp_Data2.xlsx",
  "size":90627,
  "sha256":"72a5ae89b85ac3216071560b5db36585efbba0af9ea0bef5b99c73268de557ea",
  "md5":"49ad9d082cf27823202348f9f8f762c2",
 },
}
NS={"s":"http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p":"http://schemas.openxmlformats.org/package/2006/relationships"}
CELL_REF=re.compile(r"^([A-Z]+)(\d+)$")
KNOWN_2018={"published_plant_species":41,"published_insect_species":168,
    "published_nonzero_plant_insect_links":403,"published_visitor_events":7955,
    "published_field_regions":1}
MAX_XLSX=500_000


def fetch_original(kind):
    d=SOURCE_FILES[kind]
    url=f"https://ndownloader.figshare.com/files/{d['figshare_file_id']}"
    req=urllib.request.Request(url,headers={"User-Agent":"adaptive-gain-stage72-real-original-kantsa-field/2026",
                 "Accept":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
    with urllib.request.urlopen(req,timeout=40) as res:
        data=res.read(MAX_XLSX+1)
    verify_source(kind,data)
    return data


def verify_source(kind,data):
    expected=SOURCE_FILES[kind]
    if len(data)!=expected["size"] or len(data)>MAX_XLSX:
        raise ValueError("STAGE72B_AUTHENTIC_SOURCE_BYTE_LENGTH_NOT_PINNED_"+kind)
    if hashlib.sha256(data).hexdigest()!=expected["sha256"]:
        raise ValueError("STAGE72B_AUTHENTIC_SOURCE_SHA256_NOT_PINNED_"+kind)
    if hashlib.md5(data).hexdigest()!=expected["md5"]:
        raise ValueError("STAGE72B_AUTHOR_SUPPLIED_ORIGINAL_FIGSHARE_MD5_NOT_PINNED_"+kind)
    if not zipfile.is_zipfile(io.BytesIO(data)):
        raise ValueError("STAGE72B_ORIGINAL_SOURCE_NOT_VALID_XLSX_ZIP")


def cell_column_idx(cellref):
    m=CELL_REF.fullmatch(cellref)
    if not m:raise ValueError("STAGE72B_UNEXPECTED_CELL_REFERENCE")
    n=0
    for c in m.group(1):
        n=n*26+(ord(c)-ord("A")+1)
    return n-1


def read_xlsx_sparse(source,kind=None):
    if kind:verify_source(kind,source)
    with zipfile.ZipFile(io.BytesIO(source)) as archive:
        names=set(archive.namelist())
        if "xl/workbook.xml" not in names:
            raise ValueError("STAGE72B_AUTHENTIC_SHEET_MANIFEST_MISSING")
        wb=ET.fromstring(archive.read("xl/workbook.xml"))
        sheets=wb.find("s:sheets",NS)
        shared=[]
        if "xl/sharedStrings.xml" in names:
            sr=ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared=[
                "".join((t.text or "") for t in node.findall(".//s:t",NS))
                for node in sr.findall("s:si",NS)
            ]
        rels={}
        if "xl/_rels/workbook.xml.rels" in names:
            rr=ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
            for rel in rr.findall("p:Relationship",NS):
                target=rel.attrib["Target"].lstrip("/")
                if not target.startswith("xl/"):
                    target=posixpath.normpath("xl/"+target)
                rels[rel.attrib["Id"]]=target
        books={}
        for i,sheet in enumerate(sheets.findall("s:sheet",NS),start=1):
            name=sheet.attrib["name"].strip()
            key=sheet.attrib.get("{"+NS["r"]+"}id","")
            entry=rels.get(key,f"xl/worksheets/sheet{i}.xml")
            if entry not in names:raise ValueError("STAGE72B_MISSING_DECLARED_SHEET_"+name)
            root=ET.fromstring(archive.read(entry))
            data=root.find("s:sheetData",NS)
            rows={}
            for row in data.findall("s:row",NS) if data is not None else []:
                rn=int(row.get("r") or 0)
                cells={}
                for cell in row.findall("s:c",NS):
                    ref=cell.attrib.get("r","")
                    col=cell_column_idx(ref)
                    val=cell.find("s:v",NS)
                    inline=cell.find("s:is",NS)
                    v=(val.text or "") if val is not None else ""
                    t=cell.get("t","")
                    if t=="s" and v:
                        idx=int(v);v=shared[idx] if 0<=idx<len(shared) else ""
                    elif inline is not None:
                        v="".join(x.text or "" for x in inline.findall(".//s:t",NS))
                    if v.strip():
                        cells[col]=v.strip()
                if cells:rows[rn]=cells
            if name in books:raise ValueError("STAGE72B_DUPLICATE_ORIGINAL_SHEET_NAME")
            books[name]=rows
        return books


def safe_float(value):
    v=str(value).strip()
    if not v or v.lower() in {"na","nan","n/a","null"}:return None
    try: num=float(v)
    except ValueError: return None
    if not (num>=0 and num<1e15):return None
    return num


def summarize_network(source):
    workbook=read_xlsx_sparse(source,"network")
    if list(workbook)!=["p-p_network"]:
        raise ValueError("STAGE72B_ORIGINAL_NETWORK_SHEET_NAME_CHANGED")
    sheet=workbook["p-p_network"]
    # Preview original actual row positions before defining plant×insect grain.
    preview=[
      {"Excel_original_row":i,"cells_by_original_1based_col":{
          str(col+1):v for col,v in sorted(row.items())[:18]}}
      for i,row in sorted(sheet.items())[:8]
    ]
    numeric=[]
    for i,row in sheet.items():
        if i<=3:continue
        for col,v in row.items():
            value=safe_float(v)
            if value is not None and value.is_integer():
                numeric.append((i,col,int(value)))
    counts=collections.Counter()
    for _,_,v in numeric:
        counts["numeric_cells_in_data_region"]+=1
        counts["numeric_cells_positive"]+=v>0
        counts["sum_positive_integer_cells"]+=v if v>0 else 0
    return {
       "original_2018_network_sheet_names":list(workbook),
       "original_2018_nonempty_rows":len(sheet),
       "original_2018_numeric_grid_provisional":dict(counts),
       "published_network_counts_not_automatically_data_replay":KNOWN_2018,
       "first_eight_original_rows_with_real_cell_coordinates":preview,
    },workbook


def summarize_voc(source):
    workbook=read_xlsx_sparse(source,"voc")
    plant_sheets=[k for k in workbook if k.casefold()!="title"]
    emission=collections.Counter()
    records=[]
    for species in plant_sheets:
        rows=workbook[species]
        measured=[]
        for index,row in sorted(rows.items()):
            if index==1:continue
            compound=row.get(0,"")
            val=safe_float(row.get(1,""))
            if compound and val is not None and val>0:
                measured.append((compound,val))
        emission["plant_sheets"]+=1
        emission["plant_sheets_with_positive_compound_mean_ER"]+=bool(measured)
        emission["positive_compound_species_entries"]+=len(measured)
        records.append({"original_Figshare_source_sheet_plant":species,
             "n_source_positive_compound_entries":len(measured),
             "sum_source_mean_emission_ng_g_h":sum(v for _,v in measured) if measured else "",
             "source_dataset2_unit":"ng/g/h",
             "missing_unmeasured_compounds_not_recorded_as_absent":1})
    return {
       "original_figshare_voc_sheet_count_including_title":len(workbook),
       "original_voc_taxon_sheet_count":len(plant_sheets),
       "source_voc_compound_statistics":dict(emission),
       "voc_taxa_names":plant_sheets,
       "source_emission_sums_not_synthetic_plant_fitness_or_wind":True,
    },records


def write_csv(file,rows):
    with Path(file).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    a.outdir.mkdir(parents=True,exist_ok=True)
    network=fetch_original("network")
    voc=fetch_original("voc")
    n,wb=summarize_network(network)
    v,compound=summarize_voc(voc)
    report={
      "schema":"stage72b_original_Kantsa2018_figshare_authentic_network_and_VOC_source",
      "original_source_article_DOI":"10.1038/s41467-018-03448-w",
      "original_Figshare_article_DOI":"10.6084/m9.figshare.5663455.v2",
      "original_network_source_file":SOURCE_FILES["network"],
      "original_voc_source_file":SOURCE_FILES["voc"],
      "original_network":n,
      "original_volatiles":v,
      "published_source_network_sample_sizes_distinct_from_recomputed":True,
      "original_network_and_VOC_are_one_geographic_study_region":True,
      "no_identified_original_flower_UV_pattern_spatial_measurement":True,
      "no_field_measured_wind_speed_in_source_tables":True,
      "no_plant_reproduction_or_fitness_in_source_tables":True,
      "source_visitation_network_and_scent_same_study_not_new_external_replication":True,
    }
    (a.outdir/"original_Kantsa2018_source_replay_network_VOC_grain.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    write_csv(a.outdir/"original_Kantsa2018_VOC_source_compound_plant_coverage.csv",compound)
    print("STAGE72B_REAL_ORIGINAL_KANTSA_2018_NETWORK_VOC_AUDIT",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("ORIGINAL_RAW_SOURCE_DIGEST_MATCH_NO_UNSUPPORTED_PUBLISHED_EFFECT_RECOMPUTATION")
if __name__=="__main__": main()
